#!/usr/bin/env python3
"""House publish CLI: export private trees to <portfolio-root>/public/<project>.

Examples:
  python <portfolio-root>/devkit/tools/publish/cli.py doctor --project-root <portfolio-root>/taskqueue
  python <portfolio-root>/devkit/tools/publish/cli.py release --project-root <portfolio-root>/taskqueue --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

_PKG = Path(__file__).resolve().parent
if str(_PKG.parent) not in sys.path:
    sys.path.insert(0, str(_PKG.parent))

from publish.export import export_tree, scrub_verify_artifacts  # noqa: E402
from publish.manifest import load_manifest, read_version  # noqa: E402
from publish.scan import scan_tree  # noqa: E402

TEMPLATE = Path(__file__).resolve().parents[2] / "conventions" / "publish.manifest.template.yaml"


def _cmd_doctor(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve()
    issues: list[str] = []
    mpath = root / "publish.manifest.yaml"
    if not mpath.is_file():
        print(f"FAIL: missing {mpath}")
        return 2
    try:
        m = load_manifest(mpath, project_root=root)
    except Exception as e:
        print(f"FAIL: manifest: {e}")
        return 2

    if m.license.upper() != "MIT":
        issues.append(f"license is {m.license!r}, expected MIT")
    lic = m.private_root / "LICENSE"
    if not lic.is_file():
        issues.append("LICENSE file missing at private root")
    if not m.allow:
        issues.append("allow list is empty")
    if not m.public_root.parent.exists():
        issues.append(f"public parent missing: {m.public_root.parent} (create <portfolio-root>/public)")
    token = m.private_root / "plan" / "token.txt"
    if token.is_file():
        issues.append("plan/token.txt still present — rotate and delete before any export")

    ver = read_version(m)
    init = m.private_root / "taskqueue" / "__init__.py"
    # generic: look for package/__init__.py matching project name
    pkg_init = m.private_root / m.project.replace("-", "_") / "__init__.py"
    for candidate in (pkg_init, init):
        if candidate.is_file():
            text = candidate.read_text(encoding="utf-8")
            if "__version__" in text and ver not in text:
                issues.append(f"__version__ drift vs {m.version_from} ({ver}) in {candidate.name}")
            break

    print(f"project: {m.project}")
    print(f"version: {ver}")
    print(f"private: {m.private_root}")
    print(f"public:  {m.public_root}  exists={m.public_root.exists()}")
    print(f"github:  public={m.public_github} private={m.private_github}")
    print(f"allow:   {len(m.allow)} entries; deny={len(m.deny)}")
    if issues:
        print("ISSUES:")
        for i in issues:
            print(f"  - {i}")
        return 1
    print("doctor: OK")
    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    m = load_manifest(project_root=Path(args.project_root).resolve())
    meta = export_tree(m)
    print(json.dumps({k: meta[k] for k in ("project", "version", "private_sha", "file_count")}, indent=2))
    print(f"exported → {m.public_root}")
    return 0


def _cmd_scan(args: argparse.Namespace) -> int:
    m = load_manifest(project_root=Path(args.project_root).resolve())
    if not m.public_root.exists():
        print(f"FAIL: public root missing: {m.public_root} (run export first)")
        return 2
    result = scan_tree(m)
    print(f"scanned {result['files_checked']} files; hits={result['hit_count']}")
    for h in result["hits"][:20]:
        print(f"  {h['file']}:{h['line']}: {h['match']!r}")
    return 0 if result["ok"] else 1


def _cmd_verify(args: argparse.Namespace) -> int:
    m = load_manifest(project_root=Path(args.project_root).resolve())
    if not m.verify:
        print("verify: no commands in manifest (skip)")
        return 0
    if not m.public_root.is_dir():
        print(f"FAIL: public root missing: {m.public_root}")
        return 2
    failed = 0
    results = []
    for cmd in m.verify:
        print(f"$ {cmd}")
        r = subprocess.run(cmd, shell=True, cwd=str(m.public_root))
        results.append({"cmd": cmd, "returncode": r.returncode})
        if r.returncode != 0:
            failed += 1
            if not args.keep_going:
                break
    state = {
        "project": m.project,
        "ok": failed == 0,
        "results": results,
    }
    state_dir = m.public_root / ".publish"
    state_dir.mkdir(exist_ok=True)
    (state_dir / "last_verify.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print("verify: OK" if failed == 0 else f"verify: FAIL ({failed})")
    return 0 if failed == 0 else 1


def _cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve()
    mpath = root / "publish.manifest.yaml"
    if not mpath.is_file():
        print(f"no manifest at {mpath}")
        return 1
    m = load_manifest(mpath, project_root=root)
    print(f"{m.project}  version={read_version(m)}")
    print(f"  private={m.private_root}")
    print(f"  public={m.public_root} exists={m.public_root.exists()}")
    for name in ("last_export.json", "last_scan.json", "last_verify.json"):
        p = m.public_root / ".publish" / name
        if p.is_file():
            data = json.loads(p.read_text(encoding="utf-8"))
            summary = {k: data[k] for k in data if k in ("ok", "hit_count", "file_count", "version", "private_sha", "exported_at")}
            print(f"  {name}: {summary}")
        else:
            print(f"  {name}: (none)")
    return 0


def _cmd_release(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve()
    rc = _cmd_doctor(argparse.Namespace(project_root=str(root)))
    if rc != 0 and not args.force:
        print("release aborted (doctor failed); use --force to continue")
        return rc
    m = load_manifest(project_root=root)
    if args.bump:
        print("bump: not implemented in this wave (edit pyproject + CHANGELOG manually)")
        return 2
    meta = export_tree(m)
    print(f"export: {meta['file_count']} files (private {meta['private_sha']})")
    scan = scan_tree(m)
    if not scan["ok"]:
        print(f"scan: FAIL ({scan['hit_count']} hits)")
        for h in scan["hits"][:10]:
            print(f"  {h['file']}:{h['line']}: {h['match']!r}")
        return 1
    print("scan: OK")
    vargs = argparse.Namespace(project_root=str(root), keep_going=False)
    vrc = _cmd_verify(vargs)
    if vrc != 0:
        return vrc
    if args.dry_run:
        print("release: dry-run complete (no commit/push)")
        return 0
    if not args.i_mean_it:
        print("release: verify green — re-run with --i-mean-it to commit/push public tree")
        print("         (or --dry-run was omitted intentionally; push still gated)")
        return 0
    # commit + push
    if not (m.public_root / ".git").exists():
        print(f"FAIL: {m.public_root} is not a git clone; run init-public-clone first")
        return 2
    msg = m.export_commit_template.format(
        project=m.project,
        version=read_version(m),
        private_sha=meta["private_sha"],
    )
    n_scrub = scrub_verify_artifacts(m.public_root)
    if n_scrub:
        print(f"scrubbed {n_scrub} verify artifact dirs before commit")
    # Ensure ignore rules exist even if an older export lacked them.
    gi = m.public_root / ".gitignore"
    if not gi.is_file():
        from publish.export import PUBLIC_GITIGNORE

        gi.write_text(PUBLIC_GITIGNORE, encoding="utf-8")
    subprocess.run(["git", "-C", str(m.public_root), "add", "-A"], check=True)
    # allow empty? skip if clean
    st = subprocess.run(
        ["git", "-C", str(m.public_root), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    if st.stdout.strip():
        subprocess.run(["git", "-C", str(m.public_root), "commit", "-m", msg], check=True)
    else:
        print("public tree clean — nothing to commit")
    tag = f"v{read_version(m)}"
    subprocess.run(["git", "-C", str(m.public_root), "push", "origin", "HEAD"], check=True)
    subprocess.run(
        ["git", "-C", str(m.public_root), "tag", "-f", tag],
        check=False,
    )
    subprocess.run(["git", "-C", str(m.public_root), "push", "-f", "origin", tag], check=False)
    print(f"release: pushed {m.public_github} tag {tag}")
    return 0


def _cmd_init_manifest(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve()
    dest = root / "publish.manifest.yaml"
    if dest.exists() and not args.force:
        print(f"exists: {dest} (use --force to overwrite)")
        return 1
    if not TEMPLATE.is_file():
        print(f"FAIL: template missing: {TEMPLATE}")
        return 2
    text = TEMPLATE.read_text(encoding="utf-8")
    name = args.name or root.name
    text = text.replace("{{PROJECT}}", name)
    text = text.replace("{{PUBLIC_ROOT}}", str(Path("<portfolio-root>/public") / name).replace("\\", "/"))
    dest.write_text(text, encoding="utf-8")
    print(f"wrote {dest}")
    return 0


def _cmd_init_public_clone(args: argparse.Namespace) -> int:
    m = load_manifest(project_root=Path(args.project_root).resolve())
    if m.public_root.exists() and any(m.public_root.iterdir()) and not args.force:
        print(f"public root already exists: {m.public_root}")
        return 1
    m.public_root.parent.mkdir(parents=True, exist_ok=True)
    url = args.url or f"https://github.com/{m.public_github}.git"
    if m.public_root.exists():
        shutil.rmtree(m.public_root)
    print(f"cloning {url} → {m.public_root}")
    r = subprocess.run(["git", "clone", url, str(m.public_root)])
    return r.returncode


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--project-root",
        default=".",
        help="private project root containing publish.manifest.yaml",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("doctor", help="validate manifest and preflight")
    sub.add_parser("status", help="show last export/scan/verify")
    sub.add_parser("export", help="sync allowlist into public_root")
    sub.add_parser("scan", help="scan public_root for leaks")
    v = sub.add_parser("verify", help="run manifest verify commands in public_root")
    v.add_argument("--keep-going", action="store_true")

    rel = sub.add_parser("release", help="doctor → export → scan → verify → optional push")
    rel.add_argument("--dry-run", action="store_true", help="stop after verify")
    rel.add_argument("--i-mean-it", action="store_true", help="commit and push public tree")
    rel.add_argument("--bump", choices=("patch", "minor", "major"))
    rel.add_argument("--force", action="store_true", help="continue despite doctor issues")

    im = sub.add_parser("init-manifest", help="write publish.manifest.yaml from template")
    im.add_argument("--name", help="project name (default: directory name)")
    im.add_argument("--force", action="store_true")

    ic = sub.add_parser("init-public-clone", help="git clone public repo into public_root")
    ic.add_argument("--url", help="override clone URL")
    ic.add_argument("--force", action="store_true")

    return ap


def main(argv: list[str] | None = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)
    # Ensure PUBLISH_ALLOW_PUSH alone cannot bypass without --i-mean-it flag on release
    if args.cmd == "doctor":
        return _cmd_doctor(args)
    if args.cmd == "status":
        return _cmd_status(args)
    if args.cmd == "export":
        return _cmd_export(args)
    if args.cmd == "scan":
        return _cmd_scan(args)
    if args.cmd == "verify":
        return _cmd_verify(args)
    if args.cmd == "release":
        if os.environ.get("PUBLISH_ALLOW_PUSH") == "1" and not args.dry_run:
            args.i_mean_it = True
        return _cmd_release(args)
    if args.cmd == "init-manifest":
        return _cmd_init_manifest(args)
    if args.cmd == "init-public-clone":
        return _cmd_init_public_clone(args)
    ap.error(f"unknown cmd {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
