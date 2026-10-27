# MCP indexers, search routing and machine resources

Agents **query** search tools; they never index. One contested PC: compile, CPE, sims and GPU jobs own it, and search/index tools must not slow coding. (Merged with the former resource-policy; [resource-policy.md](resource-policy.md) is a stub.)

## Rules
- **R1** No auto-update after changes: no watchers, save hooks or git hooks that reindex or pack. **R2** Idle is free: MCP servers burn CPU only on a call. **R3** Heavy work (cold GrepAI/Repowise/ctags regen) only on operator cadence, never mid-compile/CPE/GPU. **R4** Live Grep beats a stale DB: do not refresh indexes "to be sure". **R5** Scoped packs only (always `--include`; never whole-tree or all of `<portfolio-root>`). **R6** No GPU for search tools. **R7** One heavy agent workspace when CPU is tight.

## Allowed
Editor Grep / `rg` (exact text, `-C 2|5`), `fd`, ast-grep-mcp (structural), mcp-ctags `find_symbol` (prefer Grep if tags miss), one-shot `refresh_tags` only if a symbol is missing and the machine is idle. GrepAI / Arbor / Repowise MCP only when an opt-in profile (`grepai-only` / `full`) enables them; soft-parked from daily. Scoped Repomix compress via `agent_search/skeleton_pack.py` only when a ticket asks for an architecture dump; optional `agent_search/sg_scan.py --rule dds-firewall --project bridge2`.

## Forbidden for agents
`grepai watch` (any variant); `arbor watch|index|setup|status`; `repowise watch|update|init`; any refresh that starts a watch (`--allow-watch`); `dev_index` refresh; habitual `refresh_tags` / cold index mid-session; `scip-clang` / LSIF generators; unscoped `repomix` or whole-repo packs.

## Operator-only
Cold index, then **stop** (`stop-all`); never chain into `make.bat`, CPE or session start. Tools in `devkit/tools/` (`dev_index.py`, `dev_index_control.py`, `indexers/`, `dev_index_projects.json`; `agent_search/regen_tags.py`, `skeleton_pack.py`). Typical triggers: after hub distribute if semantic search is wrong, quiet weekly window, tags miss a symbol Grep finds, scoped Repomix before an external-LLM architecture review.

## Routing (prefer top rows; Grep when an indexer is down/stale)
Exact text: Grep/`rg` · structural/AST: ast-grep-mcp · symbol signature: ctags find (else Grep) · semantic/wiki/callers: Grep, ctags refs, plan docs (GrepAI/Repowise/Arbor soft-parked) · architecture skeleton: scoped Repomix `--compress` (rare) · prior research / techniques / what other projects found: librarian MCP `advise` (lite profile).

## L0 -> L1 -> L2
L0 NOW + short ARCH (~0.5-2k tokens) -> L1 Grep/ast-grep/ctags probes -> L2 one function/class window Read. Do not full-read large `.cpp`/`.hpp` "to understand".
