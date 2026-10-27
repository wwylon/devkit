# Agent context budget

Portable discipline for staying inside the context window; import from each project's `CLAUDE.md` (`@../devkit/rules/agent-context.md`).

- **Never full-read a file > ~150 lines.** Grep for line numbers, then read the target range with `offset`/`limit`.
- **Cap grep output** (`head_limit`); never paste large tool output. Find problems by ID (`grep "F-NNN" plan/problems_open.md`), not whole-register reads. Registers are split index/open/fixed ([plan-structure.md](plan-structure.md)): read the index row, then one entry.
- **One task per session.** If context runs heavy, update `NOW.md`/`tasks.md`, summarize, end cleanly.
- **Entry files stay indexes** (~120 lines); do not copy the same bootstrap into CLAUDE, AGENTS and always-on rules. Session read = NOW headings + one task section; specs, catalogs, journals and closed files are grep-only.
- **Before opening a new IDEA**, grep closed/`reject`/`trial-reverted` ledgers ([external-intake.md](external-intake.md)); no retry without new evidence. If it uses a known technique, also call librarian `advise <concept> --context <game>`.
- Respect [mcp-indexers.md](mcp-indexers.md): no watchers or mid-session cold reindex.

Project-specific bootstrap stays in each project's own session rules.
