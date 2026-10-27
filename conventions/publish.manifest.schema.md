# publish.manifest.yaml — field reference

Per-project file at the **private** repo root. Never exported to the public tree (house deny).

| Field | Required | Meaning |
|-------|----------|---------|
| `project` | yes | Short name (`taskqueue`) |
| `license` | yes | Must be `MIT` for this wave |
| `private_root` | yes | Usually `.` |
| `public_root` | yes | Absolute path, e.g. `<portfolio-root>/public/taskqueue` |
| `public_github` | yes | `owner/repo` for the public face |
| `private_github` | yes | `owner/repo-private` |
| `default_branch` | no | `main` or `master` |
| `allow` | yes | Paths relative to private root to copy |
| `deny` | no | Extra deny (merged with house defaults) |
| `overlays` | no | `{from, to}` copy/rename into public tree |
| `rewrites` | no | Same shape; used for portable rule variants |
| `scan_forbid_regex` | no | Extra content scans (merged with house) |
| `verify` | no | Shell commands, cwd = public_root |
| `version_from` | no | Default `pyproject.toml` |
| `changelog` | no | Default `CHANGELOG.md` |
| `export_commit_template` | no | Supports `{project}` `{version}` `{private_sha}` |

House deny and scan defaults: `devkit/tools/publish/house_defaults.py`.

CLI: `python <portfolio-root>/devkit/tools/publish/cli.py --help`
