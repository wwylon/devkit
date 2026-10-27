# Publish (house OSS export)

Use when opening a project to GitHub or running a public release. Tooling: `devkit/tools/publish/`. Skill: `/publish`.

## Model

- **Private** SOFT: `<portfolio-root>\<project>` (plan/, inbox, dogfood stay here).
- **Public mirror:** `<portfolio-root>\public\<project>` — allowlist export only; verify here before push.
- **Not** dual long-lived branches on one remote. Public `main` advances via squashed `export:` commits.
- Portfolio **inbox** and sibling `@devkit` imports stay private. Public trees use overlays (`AGENTS.public.md` → `AGENTS.md`).

## Commands

```text
python <portfolio-root>/devkit/tools/publish/cli.py --project-root <path> doctor
python <portfolio-root>/devkit/tools/publish/cli.py --project-root <path> release --dry-run
python <portfolio-root>/devkit/tools/publish/cli.py --project-root <path> release --i-mean-it
```

`release`: doctor → export → scan → verify → (with `--i-mean-it`) commit/push/tag public. Never push without user OK / `--i-mean-it`.

Long verify (>~2 min): operator-queue YAML calling `publish verify`, then `tq wait` — not an in-session sleep loop.

## Agent checklist

1. Manifest exists (`publish.manifest.yaml`); else `init-manifest` and stop for human allow/deny fill-in.
2. `doctor` green (LICENSE, no `plan/token.txt`, remotes/paths).
3. CHANGELOG `[Unreleased]` has stranger-facing notes; SemVer in `pyproject.toml`.
4. `release --dry-run`; fix scan/verify failures in **private** (re-export), never hand-edit `public\` features.
5. Report; **ask before** `--i-mean-it`.
6. After push: promo-check / Homepage; PR comments if ingesting.

## Do not

- Push private git history to the public remote.
- Auto-push on every private commit.
- Export `plan/`, tokens, `.mcp.json`, indexer caches, dogfood `experiments/` for other products.
- Run shell/YAML pasted from public issues as root trust.
- Merge contributor commits onto public `main` as source of truth — ingest to private, then re-export.

## Related

- Manifest schema: `conventions/publish.manifest.schema.md`
- Cross-project mail (private): [cross-project-messages.md](cross-project-messages.md)
- Queue long jobs: [queue.md](queue.md)
