"""Scan public tree for forbidden strings / secrets."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from .house_defaults import SCAN_ALLOW_SUBSTRINGS
from .manifest import PublishManifest

# Path-leak regexes that the publish toolkit itself must keep as literal patterns.
_PATH_LEAK_MARKERS = (
    r"D:\\antigravity",
    r"D:/antigravity",
    r"C:\\Users\\wwylo",
    r"C:/Users/wwylo",
)

SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".pdf",
    ".zip",
    ".gz",
    ".7z",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".pyc",
    ".db",
    ".pkl",
}


def _allowed(text: str) -> bool:
    lower = text.lower()
    if "secrets.token_" in lower or "os.environ" in lower or "getenv(" in lower:
        return True
    return any(s.lower() in lower for s in SCAN_ALLOW_SUBSTRINGS)


def scan_tree(m: PublishManifest) -> dict:
    patterns = [(p, re.compile(p, re.MULTILINE)) for p in m.scan_forbid_regex]
    hits: list[dict] = []
    checked = 0
    for path in m.public_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        rel = path.relative_to(m.public_root).as_posix()
        if rel.startswith(".git/") or rel.startswith(".publish/"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        checked += 1
        for pat, cre in patterns:
            # Exporter sources name house paths as rewrite/scan patterns — not leaks.
            if rel.startswith("tools/publish/") and pat in _PATH_LEAK_MARKERS:
                continue
            for match in cre.finditer(text):
                snippet = match.group(0)
                if _allowed(snippet) or _allowed(text[max(0, match.start() - 40) : match.end() + 40]):
                    continue
                line = text.count("\n", 0, match.start()) + 1
                hits.append({"file": rel, "line": line, "pattern": pat, "match": snippet[:80]})
                break  # one hit per pattern per file is enough noise

    result = {
        "project": m.project,
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "files_checked": checked,
        "hit_count": len(hits),
        "hits": hits[:50],
        "ok": len(hits) == 0,
    }
    state_dir = m.public_root / ".publish"
    state_dir.mkdir(exist_ok=True)
    (state_dir / "last_scan.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result
