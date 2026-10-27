# devkit

Shared skills, agents, and rules for antigravity projects. Clones inherit their unique repo; they are not listed.

| Project | Kind | Imports |
|---------|------|---------|
| bridge2 | game engines | data-and-results, queue, engine-purity, cross-repo-contracts |
| pimc | search library | data-and-results, queue, plan-structure, engine-purity, cross-repo-contracts, bug-patterns, external-intake |
| pokerbot | game bot | queue |
| dds_alpha | solver | data-and-results, queue |
| omnicard | multi-game solver | parent only |
| omnicard3 | solver | plan-structure, data-and-results, queue |
| omnigames | full games/bots (omnicard3 DDS consumer) | plan-structure, data-and-results, queue, cross-repo-contracts |
| bridge | UI app | parent only (Face INDEX) |
| taskqueue | job service | queue, plan-structure |
| llm_localize | localisation tool | follows plan-structure; no `@` import |
| parent `<portfolio-root>\CLAUDE.md` | every repo under `<portfolio-root>` | agent-context, mcp-indexers (incl. resource policy), documentation-standards, house-standard, cross-project-messages, queue (external-intake: linked, not imported) |

Parent imports apply when the workspace is `<portfolio-root>`. Single-repo checkouts should `@` any parent rule they need every session (do not duplicate with `*`). The Imports column is only the extra `@` lines. Clones are not listed. Indexer membership (`tools/dev_index_projects.json`) is not this table.

## What lives here

| Path | Contents |
|------|----------|
| `rules/data-and-results.md` | Oracle + benchmark discipline |
| `rules/queue.md` | Task queue discipline |
| `rules/plan-structure.md` | Shared `plan/` hub: NOW / STATUS / tasks / archive / experiment index |
| `rules/llm-localize.md` | Localisation engine: CLI, web, taskqueue integration |
| `rules/milestones.md` | Milestone close-out |
| `rules/bug-patterns.md` | Portable flaw-pattern catalog (stable PAT IDs); read during fixes, not every session |
| `rules/devkit-changes.md` | Read before editing this repo |
| `rules/agent-context.md` | Agent context budget: read/grep discipline, one task per session |
| `rules/cross-repo-contracts.md` | Contract-first discipline for shared encodings / protocols / ABIs |
| `rules/engine-purity.md` | Engine families (rule / search / learned / mixture) stay pure |
| `rules/master-worker.md` | Remote YAML authoring + worker triage rules |
| `rules/queue-reference.md` | Queue operational reference: triage, CLI, wait patterns |
| `rules/documentation-standards.md` | Portable DoD: `--help`, docs with code, log behavior changes |
| `rules/agent-tool-surface.md` | Agent tool layering (L0 invent-ban / L1 skill / L2 operator) |
| `rules/external-intake.md` | Triage raw LLM exports → verified registers + queue tasks |
| `rules/cross-project-messages.md` | Mailbox protocol (`<portfolio-root>\inbox\`): requests/questions/answers between projects |
| `rules/publish.md` | OSS dual-tree export (`tools/publish/`); read when publishing — not every session |
| `rules/mcp-indexers.md` | GrepAI / Repowise / ast-grep / ctags: query only; Arbor parked; never watch |
| `rules/resource-policy.md` | Stub: R1-R7 and cold cadence now in `mcp-indexers.md` |
| `rules/*-reference.md`, `queue-authoring.md` | On-demand detail split from core rules (`external-intake`, `data-and-results`, `queue`); core files stay small because imports load eagerly |
| `tools/startup_cost.py` | Always-on context bytes/tokens per project (CLAUDE.md chain + `@` imports); run before/after editing any imported rule |
| `rules/house-standard.md` | Slim/rich tiers, session, orchestrator vs agents |
| `rules/external-intake.md` | Idea pipeline + anti-retry dispositions |
| `rules/test-audit-tiers.md` | Mid-task vs pre-merge test audit tiers, fail-first |
| `plugins/antigravity/` | Claude Code plugin: `/optimize`, `/queue-task`, `/publish`, `/idea`, `/handoff`, `/new-problem`, `/benchmark` |
| `tools/publish/` | Allowlist export → `<portfolio-root>/public/<project>`; scan/verify/gated push |
| `conventions/publish.manifest.template.yaml` | Per-project `publish.manifest.yaml` template + schema |
| `ideas/game-bot-theory.md` | Portfolio-level ideas with per-project applicability tags |
| `conventions/` | Templates: `tasks`, `NOW`, `STATUS`, plan README, archive, problems, optimization_log, `algorithm-doc` (on demand) |
| `tools/` | Indexers, `pack_code/`, `intake/`, `agent_search/`, house_compliance. Membership ≠ consumer table |
| `tools/msvc/` | `vswhere` locator for `vcvarsall` / bundled CMake+Ninja (bridge2 `scripts/find_vcvars.*`) |
| `docs/HOUSE_STANDARD_PLAN.md` | MVP→Wave3 house standardization plan |
| `docs/HOUSE_RUNBOOK.md` | Operator cheat sheet |

## Plugin install

The `antigravity` plugin is registered as a local marketplace:

```json
// ~/.claude/plugins/known_marketplaces.json
"antigravity-devkit": {
  "source": { "source": "local", "path": "<portfolio-root>\\devkit" },
  "installLocation": "<portfolio-root>\\devkit"
}
```

Each project's `.claude/settings.local.json` opts in:

```json
"enabledPlugins": { "antigravity@antigravity-devkit": true }
```

## Shared rules

Import only the rows in the consumer table. The parent file already loads `agent-context`, `mcp-indexers`, and `documentation-standards`. `bug-patterns.md` is for fixes, not every session.

## Plan hub (all projects)

Agents bootstrap from `plan/NOW.md` (see `rules/plan-structure.md`). Recommended layout:

- `plan/README.md` — dashboard
- `plan/NOW.md` — doing / next / waiting
- `plan/tasks.md` — active tasks only
- `plan/STATUS.md` — idea decisions (research portfolios)
- `plan/archive/` — completed acceptance prose

**Adoption:** the slim `NOW` / `tasks` layout is the default. If a project documents a different layout, do not migrate it back.

## Ideas repository

File ideas with `/idea <description>`. Pull an idea into a project with `/idea pull <slug> into <project>`.

See [ideas/game-bot-theory.md](ideas/game-bot-theory.md).
