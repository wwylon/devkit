"""Load and validate publish.manifest.yaml."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .house_defaults import HOUSE_DENY, HOUSE_SCAN_FORBID_REGEX


@dataclass
class Overlay:
    src: str
    dest: str


@dataclass
class PublishManifest:
    project: str
    license: str
    private_root: Path
    public_root: Path
    public_github: str
    private_github: str
    default_branch: str
    allow: list[str]
    deny: list[str]
    overlays: list[Overlay]
    rewrites: list[Overlay]
    scan_forbid_regex: list[str]
    verify: list[str]
    export_commit_template: str
    version_from: str
    changelog: str
    raw: dict[str, Any] = field(repr=False)

    @property
    def manifest_path(self) -> Path:
        return self.private_root / "publish.manifest.yaml"


def _as_list(val: Any) -> list[str]:
    if val is None:
        return []
    if isinstance(val, str):
        return [val]
    return [str(x) for x in val]


def _overlays(val: Any) -> list[Overlay]:
    out: list[Overlay] = []
    if not val:
        return out
    for item in val:
        if not isinstance(item, dict):
            raise ValueError(f"overlay must be mapping, got {item!r}")
        src = item.get("from") or item.get("src")
        dest = item.get("to") or item.get("dest")
        if not src or not dest:
            raise ValueError(f"overlay needs from/to: {item!r}")
        out.append(Overlay(str(src), str(dest)))
    return out


def load_manifest(path: Path | None = None, *, project_root: Path | None = None) -> PublishManifest:
    root = (project_root or Path.cwd()).resolve()
    mpath = (path or root / "publish.manifest.yaml").resolve()
    if not mpath.is_file():
        raise FileNotFoundError(f"missing manifest: {mpath}")
    data = yaml.safe_load(mpath.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a mapping")

    project = str(data.get("project") or root.name)
    private_root = Path(data.get("private_root") or "." )
    if not private_root.is_absolute():
        private_root = (mpath.parent / private_root).resolve()
    else:
        private_root = private_root.resolve()

    public_root_raw = data.get("public_root")
    if not public_root_raw:
        raise ValueError("public_root is required")
    public_root = Path(str(public_root_raw))
    if not public_root.is_absolute():
        public_root = (private_root / public_root).resolve()
    else:
        public_root = public_root.resolve()

    deny = list(dict.fromkeys(HOUSE_DENY + _as_list(data.get("deny"))))
    scan = list(dict.fromkeys(HOUSE_SCAN_FORBID_REGEX + _as_list(data.get("scan_forbid_regex"))))

    return PublishManifest(
        project=project,
        license=str(data.get("license") or "MIT"),
        private_root=private_root,
        public_root=public_root,
        public_github=str(data.get("public_github") or f"wwylon/{project}"),
        private_github=str(data.get("private_github") or f"wwylon/{project}-private"),
        default_branch=str(data.get("default_branch") or "main"),
        allow=_as_list(data.get("allow")),
        deny=deny,
        overlays=_overlays(data.get("overlays")),
        rewrites=_overlays(data.get("rewrites")),
        scan_forbid_regex=scan,
        verify=_as_list(data.get("verify")),
        export_commit_template=str(
            data.get("export_commit_template")
            or "export: {project} {version} (private {private_sha})"
        ),
        version_from=str(data.get("version_from") or "pyproject.toml"),
        changelog=str(data.get("changelog") or "CHANGELOG.md"),
        raw=data,
    )


def read_version(m: PublishManifest) -> str:
    if not m.version_from:
        return "0.0.0"
    path = m.private_root / m.version_from
    if not path.is_file():
        return "0.0.0"
    text = path.read_text(encoding="utf-8")
    # bare VERSION file
    if path.name.upper() == "VERSION":
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                return line
        return "0.0.0"
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("version") and "=" in line:
            # pyproject: version = "0.7.4"
            rhs = line.split("=", 1)[1].strip().strip("\"'")
            if rhs:
                return rhs
    return "0.0.0"
