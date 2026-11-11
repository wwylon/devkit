# tools/publish

Allowlist export from a private antigravity project into `D:/antigravity/public/<project>`.

```text
python D:/antigravity/devkit/tools/publish/cli.py --project-root D:/antigravity/taskqueue doctor
python D:/antigravity/devkit/tools/publish/cli.py --project-root D:/antigravity/taskqueue release --dry-run
python D:/antigravity/devkit/tools/publish/cli.py --project-root D:/antigravity/taskqueue release --i-mean-it
```

Export preserves `.venv` / pytest / ruff caches across wipe, runs `scripts/build_docs.py` post-rewrite when present, and writes `verify_stamp.json` so `--i-mean-it` can skip a second identical verify (`--force-verify` to ignore).

See `../../rules/publish.md` and `../../conventions/publish.manifest.schema.md`.
