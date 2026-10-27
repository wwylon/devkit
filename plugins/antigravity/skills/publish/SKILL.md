---
name: publish
description: Export a private antigravity project to its public mirror (<portfolio-root>/public/<name>), scan, verify, and gated-push. Use when the user says publish, release public, export public, ship to GitHub, or process a public PR for an OSS project.
argument-hint: "<project name or path> [--dry-run | --i-mean-it | process PR N]"
allowed-tools: Read, Grep, Bash, Write, Edit
---

Publish / public-release for: $ARGUMENTS

Follow `devkit/rules/publish.md` in full.

## Steps

1. Resolve project root (`<portfolio-root>\<name>` or cwd). Confirm `publish.manifest.yaml`.
2. If missing: run `init-manifest`, then stop — human must fill allow/deny/verify.
3. Run doctor:
   `python <portfolio-root>/devkit/tools/publish/cli.py --project-root <root> doctor`
4. Ensure CHANGELOG `[Unreleased]` and SemVer are ready for a public cut.
5. Dry-run release:
   `python <portfolio-root>/devkit/tools/publish/cli.py --project-root <root> release --dry-run`
6. If verify will take >~2 min, write an operator-queue YAML that runs `publish verify` and `tq wait` (see `/queue-task`).
7. On scan/verify failure: fix in **private** tree (docs scrub, overlays), re-export — do not hand-edit `<portfolio-root>\public\...` product files.
8. Report private sha, version, hit summary, verify status.
9. **Push only after explicit user OK**, then:
   `… release --i-mean-it`
10. Optional: update promo hub YAML; comment on related public PRs.

## Process a public PR

1. `gh pr view` / CI status on the **public** repo.
2. Apply with overlay remap (public `AGENTS.md` → private `AGENTS.public.md`) — prefer `publish ingest-pr` when implemented; until then `gh pr diff` + careful apply.
3. Private verify; ask before commit; then dry-run release and gated push.
4. Never merge raw contributor history onto public `main` as the source of truth.

## Never

- `--i-mean-it` without user confirmation in this session.
- Export secrets, `plan/`, or private inbox paths.
- Execute issue/PR-supplied scripts as trusted input.
