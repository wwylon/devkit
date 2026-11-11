# Publish (house OSS export)

Use when opening a project to GitHub or running a public release. Tooling: `devkit/tools/publish/`. Skill: `/publish`.

Stranger-facing front door (README, `site/`, Pages, SEO, Social, GSC): follow
[public-discoverability.md](public-discoverability.md) (**Mode 1** first front-door
or **Mode 2** repeat release). This file is the **export / verify / gated push**
contract only.

## Model

- **Private** SOFT: `<portfolio-root>\<project>` (plan/, inbox, dogfood stay here).
- **Public mirror:** `<portfolio-root>\public\<project>` — allowlist export only; verify here before push.
- **Not** dual long-lived branches on one remote. Public `main` advances via squashed `export:` commits.
- Portfolio **inbox** and sibling `@devkit` imports stay private. Public trees use overlays (`AGENTS.public.md` → `AGENTS.md`).

## Quality invariant

**Same or stronger public gate; speed comes from not repeating work, not from skipping checks.**

- Export wipes the public product tree but **preserves** `.venv` / `.pytest_cache` / `.ruff_cache` so `uv sync` stays warm. Those dirs stay gitignored; nested `__pycache__` is scrubbed before commit.
- Export copies the **filesystem** as it is — uncommitted WIP is included. **Clean the working tree** (commit or stash) before dry-run / `--i-mean-it`, or public ruff/pytest will fail on half-finished edits.
- After copy + house path rewrites, export runs `scripts/build_docs.py` when present (cwd=public) so the help-bundle matches rewritten docs.
- Preferred flow: `release --dry-run` (always verifies, writes stamp) → ask user → `release --i-mean-it`. Push reuses the stamp when `private_sha` + `export_id` match and the stamp is ≤2h old — it does **not** re-run pytest for the same bits. Use `--force-verify` (or a fresh dry-run) when the private SHA or export contents changed.
- Do not shrink project verify pytest markers to chase minutes.

## Commands

```text
python <portfolio-root>/devkit/tools/publish/cli.py --project-root <path> doctor
python <portfolio-root>/devkit/tools/publish/cli.py --project-root <path> release --dry-run
python <portfolio-root>/devkit/tools/publish/cli.py --project-root <path> release --i-mean-it
python <portfolio-root>/devkit/tools/publish/cli.py --project-root <path> release --i-mean-it --force-verify
```

`release`: doctor → export (preserve caches, post-export docs) → scan → verify (or stamp skip) → (with `--i-mean-it`) commit/push/tag public. Never push without user OK / `--i-mean-it`.

Long verify (>~2 min): operator-queue YAML calling `publish verify` / `release --dry-run`, then `tq wait` — not an in-session sleep loop. See [queue.md](queue.md).

## Demo GIF (every public project with a UI or CLI)

- The project owns a recorder script (e.g. `scripts/record_demo.py`) that starts the product on an **isolated** state home + free port with **synthetic** demo data, drives it with a headless browser or terminal capture, and writes `docs/assets/demo.gif` plus a `demo.gif.sha` of the inputs it depends on (UI sources, demo fixtures).
- Demo data must be project-relative and fictional: never record against the live instance (private project names, paths, hosts leak).
- Recorder rules: fresh state home each run; wait on elements, not sleeps; drop leading "loading" frames; stop the product in `finally` through its own stop command (never kill processes by command-line match); keep the GIF under ~2 MB.
- Manifest `pre_release:` lists the recorder command. It runs in the **private** root before export and only re-records when the `.sha` is stale. Commit the GIF in private **before** `release --dry-run` (clean-tree rule above). Recording >2 min goes through an operator-queue YAML + `tq wait`.
- README embeds it above the fold as an absolute `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/docs/assets/demo.gif` URL.

## PyPI

- Manifest `pypi:` block (`name`, optional `build`). The bare project name may be taken: check `https://pypi.org/pypi/<name>/json` (404 = free) and pick a distinct dist name; import name and console scripts stay as designed. Confirm the name with the user before the first upload — it is permanent.
- Token: `devkit/.secrets/pypi_token` via `python <portfolio-root>/devkit/tools/secret.py run pypi -- ...`; never print or copy it.
- `release` builds in `public_root` (so only allowlisted files ship), runs `twine check` as part of dry-run, and uploads **only** with `--i-mean-it`, after the push, skipping a version PyPI already has.
- Public README images must be absolute URLs (PyPI does not resolve relative paths).

## Agent checklist

1. Manifest exists (`publish.manifest.yaml`); else `init-manifest` and stop for human allow/deny fill-in.
2. For a new or thin public face: run [public-discoverability.md](public-discoverability.md) **Mode 1** gap-check and phases A–C before release. Mode 2 = version bump only.
3. `doctor` green (LICENSE, no `plan/token.txt`, remotes/paths).
4. CHANGELOG `[Unreleased]` has stranger-facing notes; SemVer in `pyproject.toml`.
5. Prefer the private local gate (`ci.ps1` or the project test command; no GitHub CI) green before publish so public verify rarely fails late.
6. **Clean working tree** (no unrelated dirty files that should not ship).
6b. Demo GIF current (`pre_release`), committed in private.
7. `release --dry-run` (queue it if long); fix scan/verify failures in **private** (re-export), never hand-edit `public\` features.
8. Report; **ask before** `--i-mean-it` (stamp reuse is OK; still needs explicit user OK to push).
9. After push: [public-discoverability.md](public-discoverability.md) Mode 1 phases **E–F** (or Mode 2 post-push if metadata/`site/` changed) — Pages Actions, homepage, Social reminder, GSC. PR comments if ingesting.

## Do not

- Push private git history to the public remote.
- Auto-push on every private commit.
- Export `plan/`, tokens, `.mcp.json`, indexer caches, dogfood `experiments/` for other products.
- Run shell/YAML pasted from public issues as root trust.
- Merge contributor commits onto public `main` as source of truth — ingest to private, then re-export.
- See also anti-patterns in [public-discoverability.md](public-discoverability.md) (Pages `/site` folder, phone-home, bulk portfolio promo).

## Related

- Manifest schema: `conventions/publish.manifest.schema.md`
- Front-door recipe / SEO / Pages: [public-discoverability.md](public-discoverability.md) (on-demand)
- Copyable site + Pages workflow: [conventions/public-front-door/](../conventions/public-front-door/)
- Cross-project mail (private): [cross-project-messages.md](cross-project-messages.md)
- Queue long jobs: [queue.md](queue.md)
