"""PyPI build / check / upload for the house release flow.

Manifest block (all optional except ``name``)::

    pypi:
      name: tqdaemon        # distribution name on PyPI
      build: uv build           # default; runs in public_root

The token never leaves ``devkit/.secrets``: upload goes through ``secret.py run pypi``.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from .manifest import PublishManifest, read_version

SECRET_PY = Path(__file__).resolve().parents[1] / "secret.py"


def pypi_cfg(m: PublishManifest) -> dict:
    cfg = m.raw.get("pypi")
    return cfg if isinstance(cfg, dict) else {}


def dist_name(m: PublishManifest) -> str:
    return str(pypi_cfg(m).get("name") or "")


def already_published(name: str, version: str, *, timeout: float = 15.0) -> bool:
    """True if PyPI already serves ``name==version`` (200). Network errors raise."""
    url = f"https://pypi.org/pypi/{name}/{version}/json"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise


def build_and_check(m: PublishManifest) -> int:
    """Build in public_root (allowlisted files only) and run ``twine check``."""
    cfg = pypi_cfg(m)
    dist = m.public_root / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    cmd = str(cfg.get("build") or "uv build")
    print(f"$ {cmd}")
    rc = subprocess.run(cmd, shell=True, cwd=str(m.public_root)).returncode
    if rc != 0:
        return rc
    files = sorted(p.name for p in dist.glob("*")) if dist.is_dir() else []
    if not files:
        print("pypi: build produced no files in dist/")
        return 1
    print("pypi: built " + ", ".join(files))
    print("$ uvx twine check dist/*")
    return subprocess.run("uvx twine check dist/*", shell=True, cwd=str(m.public_root)).returncode


def upload(m: PublishManifest) -> int:
    """Upload dist/* with the shared token; skip when this version is already on PyPI."""
    name, version = dist_name(m), read_version(m)
    if already_published(name, version):
        print(f"pypi: {name} {version} already published — skip upload")
        return 0
    print(f"pypi: uploading {name} {version}")
    cmd = [sys.executable, str(SECRET_PY), "run", "pypi", "--", "uvx", "twine", "upload", "--non-interactive", "dist/*"]
    # shell=False would not expand dist/*; let the shell expand it, secret.py only supplies env.
    line = " ".join(f'"{c}"' if " " in c else c for c in cmd)
    return subprocess.run(line, shell=True, cwd=str(m.public_root)).returncode
