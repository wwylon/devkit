# Manifest allow entries (front door)

Add these to `publish.manifest.yaml` `allow:` when introducing a public front
door (paths relative to private root). Keep project-specific package dirs.

```yaml
allow:
  # … existing package / tests / docs …
  - .github/
  - docs/          # if not already allowed; assets live under docs/assets/
  - site/
  - README.md
  - LICENSE
  - CHANGELOG.md
  - CONTRIBUTING.md
  - SECURITY.md
  - CODE_OF_CONDUCT.md
  # when applicable:
  # - README.pl.md
  # - README.zh.md
  # - README.ar.md
  # - llms.txt
  # - uv.lock
  # - pyproject.toml
```

Overlays (typical):

```yaml
overlays:
  - from: AGENTS.public.md
    to: AGENTS.md
  - from: CLAUDE.public.md
    to: CLAUDE.md
```

`site/` must be allowlisted or Pages has nothing to deploy after export.
