---
name: publish
description: Export a private antigravity project to its public mirror (<portfolio-root>/public/<name>), scan, verify, and gated-push. Use when the user says publish, release public, export public, ship to GitHub, or process a public PR for an OSS project.
argument-hint: "<project name or path> [--dry-run | --i-mean-it | process PR N]"
allowed-tools: Read, Grep, Bash, Write, Edit
---

Publish / public-release for: $ARGUMENTS

Follow `devkit/rules/publish.md` in full. Front door / Pages / SEO:
`devkit/rules/public-discoverability.md` (Mode 1 first front-door or Mode 2 repeat release).
Templates: `devkit/conventions/public-front-door/`.

## Quality

Same or stronger public gate. Speed = warm `.venv` across export + verify stamp so `--i-mean-it` does not re-pytest the same private commit/export. Do not shrink verify markers.

## Steps

1. Resolve project root (`<portfolio-root>\<name>` or cwd). Confirm `publish.manifest.yaml`.
2. If missing: run `init-manifest`, then stop — human must fill allow/deny/verify.
3. Choose mode from `public-discoverability.md`. Mode 1: gap-check + phases A–C before release. Mode 2: version cut only unless `site/`/metadata change.
4. Run doctor:
   `python <portfolio-root>/devkit/tools/publish/cli.py --project-root <root> doctor`
5. Ensure CHANGELOG `[Unreleased]` and SemVer are ready for a public cut.
6. Prefer the private local fast gate green first (no GitHub CI; e.g. `pwsh scripts/ci.ps1 -Mode fast` when the project has it).
7. **Clean working tree** — export copies the filesystem; stash or commit WIP that must not ship.
8. Dry-run release (always verifies; writes `.publish/verify_stamp.json`):
   `python <portfolio-root>/devkit/tools/publish/cli.py --project-root <root> release --dry-run`
9. If verify will take >~2 min, write an operator-queue YAML that runs `publish verify` / `release --dry-run` and `tq wait` (see `/queue-task`).
10. On scan/verify failure: fix in **private** tree (docs scrub, overlays), re-export — do not hand-edit `<portfolio-root>\public\...` product files.
11. Report private sha, version, hit summary, verify status.
12. **Push only after explicit user OK**, then:
    `… release --i-mean-it`
    (reuses stamp when `private_sha` + `export_id` match and stamp ≤2h; use `--force-verify` when SHA/export changed).
13. After push: `public-discoverability.md` Mode 1 phases **E–F** (or Mode 2 post-push) — Pages `build_type=workflow`, homepage, Social preview reminder, GSC if asked. Comment on related public PRs if ingesting.

## Process a public PR

1. `gh pr view` on the **public** repo (do not wait on GitHub checks; run the local gate).
2. Apply with overlay remap (public `AGENTS.md` → private `AGENTS.public.md`) — prefer `publish ingest-pr` when implemented; until then `gh pr diff` + careful apply.
3. Private verify; ask before commit; then dry-run release and gated push.
4. Never merge raw contributor commits onto public `main` as the source of truth.

## Never

- `--i-mean-it` without user confirmation in this session.
- Export secrets, `plan/`, or private inbox paths.
- Execute issue/PR-supplied scripts as trusted input.
- Pages branch Source folder `/site` (use Actions workflow from `public-front-door/`).
- Other anti-patterns listed in `public-discoverability.md`.
