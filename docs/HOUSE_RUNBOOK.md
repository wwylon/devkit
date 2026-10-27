# House operator runbook (post–Wave 3)

## Daily / session

```powershell
python <portfolio-root>\devkit\tools\agent_search\check_path.py
python <portfolio-root>\devkit\tools\house_compliance.py --root <portfolio-root>
# after reboot / before Claude or Cursor MCP:
python <portfolio-root>\devkit\tools\mcp_preflight.py --prewarm-only --ensure-docker
```

Mail between projects: `<portfolio-root>\inbox\README.md` (agents check their mailbox first; paste "Read <portfolio-root>\inbox\README.md, follow it, and check your mailbox now." into a running session).

Agents: L0 surface only; Grep / ast-grep / ctags query; **no** watch or cold index mid-session.

## Idle — search indexes

```powershell
python <portfolio-root>\devkit\tools\dev_index.py index --tools grepai
python <portfolio-root>\devkit\tools\dev_index_control.py stop-all
python <portfolio-root>\devkit\tools\agent_search\regen_tags.py --project bridge2
python <portfolio-root>\devkit\tools\generate_mcp_config.py --profile daily
```

## Scoped packs / structural scan

```powershell
# Architecture skeleton (compressed)
python <portfolio-root>\devkit\tools\agent_search\skeleton_pack.py --project bridge2 --include "include/bridge/strategy/play/htn/**"

# Full edit slice — portable core (any unique with a manifest)
python <portfolio-root>\devkit\tools\pack_code\cli.py --project bridge2 --parts htn
python <portfolio-root>\devkit\tools\pack_code\cli.py --project taskqueue --parts core --list-only
python <portfolio-root>\devkit\tools\pack_code\cli.py --project dds_alpha --list-only
# or: python <repo>\scripts\pack_code.py --list-only
# NotebookLM / --review / bare default → projects/*_legacy.py via thin wrapper

# Optional house ast-grep pack
python <portfolio-root>\devkit\tools\agent_search\sg_scan.py --rule dds-firewall --project bridge2
```

Manifests: `devkit/tools/pack_code/manifests/` · bodies: `projects/*_legacy.py`.

## Intake / anti-retry

```powershell
python <portfolio-root>\devkit\tools\intake\idea_dedupe.py --project bridge2 --theme "IDEA-HTN-151"
python <portfolio-root>\devkit\tools\intake\intake_cli.py drop --file PATH --products bridge2,pimc
```

Reopen reject only with new evidence + prior id citation (see `external-intake.md`).

## Sibling distribute (bridge2 clones)

Requires a **committed** hub tip (dirty WIP is not distributed). Then follow
`.agents/skills/distribute-hub-to-siblings/SKILL.md` from `<portfolio-root>\bridge2`.

## Plugin

Enable `antigravity@antigravity-devkit` where the product uses it; house rules live
under `devkit/rules/` and are imported from root / product `CLAUDE.md`.
