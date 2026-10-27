# tools/publish

Allowlist export from a private antigravity project into `<portfolio-root>/public/<project>`.

```text
python <portfolio-root>/devkit/tools/publish/cli.py --project-root <portfolio-root>/taskqueue doctor
python <portfolio-root>/devkit/tools/publish/cli.py --project-root <portfolio-root>/taskqueue release --dry-run
python <portfolio-root>/devkit/tools/publish/cli.py --project-root <portfolio-root>/taskqueue release --i-mean-it
```

See `../../rules/publish.md` and `../../conventions/publish.manifest.schema.md`.
