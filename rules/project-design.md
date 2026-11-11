# How our projects are designed (read when you add a feature, a UI, a port, a command or a new project)

Not imported by any `CLAUDE.md`; [house-standard.md](house-standard.md) links it. Each rule is one line
plus why. Project-specific design stays in the project; this is only what holds for all of them.

## Entry points

- **Web UI → `.\web.bat` in the repo root**, per [web-launcher.md](../conventions/web-launcher.md). Without a UI, no `web.bat`.
- **Every port is in `<portfolio-root>\ports.yaml`.** Take one with `python <portfolio-root>\devkit\tools\ports.py free`, run `ports.py check` after. Why: five ports collided before there was a list.
- **`--help` on every command and script** (also `-h`); exit 0, usage on the first lines.
- Servers bind `127.0.0.1` only; never expose a port without the owner asking.

## Layout and location

- **One repo, one root.** No nested git repos (akadelist's `apps/web` had to be merged); a second repo means a second project.
- **Nothing in tracked files may depend on where the repo sits.** Use paths relative to the file (`%~dp0`, `Path(__file__)`), never `<portfolio-root>\<project>\...`. Projects move between portfolio folders (`games`, `sci`, `apps`); absolute paths and build caches break on every move.
- Build output and caches (`build*/`, `node_modules/`, `.venv/`) are untracked and rebuildable by one documented command.
- Root holds `AGENTS.md`, `CLAUDE.md`, `README.md`, `plan/NOW.md`; plan rules in [plan-structure.md](plan-structure.md) (bots: devkit_bot).

## Behaviour

- **Prerequisite check before work:** a missing build, dependency or data file gives one line saying what to run, exit 1, no traceback.
- **Hermetic tests:** `pytest`/`ctest` run without network, daemons, the real taskqueue or another project's files; set the env flags that disable them.
- **No GitHub CI.** We have no Actions tokens and the runs always fail. Do not add `.github/workflows`, do not wait on, poll or fix GitHub checks (`gh run`, `gh pr checks`). The gate is local: the project's test command or `ci.ps1` that you run before committing or publishing. "CI" in a rule means that local gate.
- **Every number shown carries its source** (a path to the evidence); a missing or stale source shows as a gap, never a guess.
- No secrets, tokens or personal paths in the repo; configuration by environment variable with a documented default.

## Boundaries

- **Read-only towards other repos.** Need a change there: one message in `<portfolio-root>\inbox\<project>\` ([cross-project-messages.md](cross-project-messages.md)).
- **Layering:** devkit (generic) → devkit_bot (game layer) → game repos. A project never imports upward in the chain or sideways into another project; shared code goes to the layer below.
- **Domain isolation:** no game material in usg/sky (med/sci); devkit stays free of domain words.
- Contract changes between repos follow [cross-repo-contracts.md](cross-repo-contracts.md).

## Before you call a feature done

`--help` works · `ports.py check` is clean · tests pass hermetically · `git status` clean · `plan/NOW.md` updated · no absolute self-path added.
