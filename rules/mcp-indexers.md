# MCP indexers, search routing and machine resources

Agents **query** search tools; they never index. One contested PC: compile, CPE, sims and GPU jobs own it, and search/index tools must not slow coding. (Merged with the former resource-policy; [resource-policy.md](resource-policy.md) is a stub.)

## Rules
- **R1** No auto-update after changes: no watchers, save hooks or git hooks that reindex or pack. **R2** Idle is free: MCP servers burn CPU only on a call. **R3** Heavy work (cold ctags regen) only on operator cadence, never mid-compile/CPE/GPU. **R4** Live Grep beats a stale DB: do not refresh indexes "to be sure". **R5** Scoped packs only (always `--include`; never whole-tree or all of `D:\antigravity`). **R6** No GPU for search tools. **R7** One heavy agent workspace when CPU is tight.

## Allowed
Editor Grep / `rg` (exact text, `-C 2|5`), `fd`, ast-grep-mcp (structural), mcp-ctags `find_symbol` (prefer Grep if tags miss), one-shot `refresh_tags` only if a symbol is missing and the machine is idle. Scoped Repomix compress via `agent_search/skeleton_pack.py` only when a ticket asks for an architecture dump; optional `agent_search/sg_scan.py --rule dds-firewall --project bridge2`.

## Retired (do not enable)
GrepAI, Arbor, and Repowise are **retired** from agent use. Do not enable them via MCP profiles, scheduled tasks, or CLI. Daily MCP is Grep / ast-grep / ctags only. Operator recovery artifacts (binaries, `devkit/tools/indexers/*`, compose files, skill bodies) may remain on disk — agents must not call them.

## Forbidden for agents
`grepai` (any subcommand including `watch` / `mcp-serve`); `arbor` (any subcommand); `repowise` (any subcommand); any `dev_index` refresh/index for those tools; habitual `refresh_tags` / cold index mid-session; `scip-clang` / LSIF generators; unscoped `repomix` or whole-repo packs.

## Operator-only
ctags / scoped Repomix only when needed. Never chain heavy index work into `make.bat`, CPE or session start. Tools in `devkit/tools/` (`agent_search/regen_tags.py`, `skeleton_pack.py`). GrepAI/Arbor/Repowise cold-index scripts are legacy — do not run.

## Routing (prefer top rows)
Exact text: Grep/`rg` · structural/AST: ast-grep-mcp · symbol signature: ctags find (else Grep) · semantic/wiki/callers: Grep, ctags refs, plan docs · architecture skeleton: scoped Repomix `--compress` (rare) · prior research / techniques / what other projects found: librarian MCP `advise` (lite profile).

## L0 -> L1 -> L2
L0 NOW + short ARCH (~0.5-2k tokens) -> L1 Grep/ast-grep/ctags probes -> L2 one function/class window Read. Do not full-read large `.cpp`/`.hpp` "to understand".
