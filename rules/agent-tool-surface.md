# Agent tool surface (portable)

Shared tool-surface discipline for antigravity projects where most work is done by
agents. Project-specific recipe *contents* (which scripts, which flags, which
targets) stay in each repo's own surface document — this file is only the
**layer model** and the invent-ban rule.

## Why

Agents that discover tools by reading binary `--help` or auto-generated catalogs
invent flags the project never blessed: wrong targets, stale flags, unsafe
combinations. A small curated surface per project, plus a strict layering rule,
keeps agent tool use auditable.

## Three layers

| Layer | Where it lives | Invent? |
|-------|-----------------|---------|
| **L0 Bootstrap** | Project surface doc (e.g. `docs/developer/AGENT_TOOL_SURFACE.md`) + `CLAUDE.md` + session rules | **No** — only recipes listed here |
| **L1 Skill** | `.agents/skills/*`, `.agents/workflows/*`, agent skill files | Only flags named in that skill's `SKILL.md` |
| **L2 Operator** | Long-form dev docs, binary `--help`, occasional catalog | Humans only, or explicit operator request |

## Rules

- **L0 is a closed set.** If a flag, target, or recipe is not on the project's
  L0 surface, the agent must not run it. Do not derive flags from `--help` or
  auto-catalogs during a task.
- **Adding to L0 is a doc change.** When a needed flag is missing, add it to the
  project surface doc with a one-line recipe + provenance (where it came from,
  why it is safe). Do not ad-hoc it in a prompt and hope it sticks.
- **L1 skills are read-first.** Invoke a skill only after reading its
  `SKILL.md`; stay within the flags that file lists.
- **L2 is not an agent fallback.** Binary `--help` and catalogs are reference
  for humans. An agent may *read* them to draft an L0 addition, not to run
  commands directly.
- **One surface per project.** Do not maintain parallel inventories; the
  project's surface doc is canonical. Session rules cite it, they do not
  re-list it.
- **Search / index CLIs are invent-banned** unless on the project L0 surface:
  no `grepai watch`, `arbor *`, `repowise update|watch`, `dev_index` refresh,
  `scip-clang`, unscoped `repomix`, or habitual `refresh_tags`. See
  [mcp-indexers.md](mcp-indexers.md) and [resource-policy.md](resource-policy.md).
- **Code discovery default:** L0 short docs → L1 Grep/ast-grep/ctags → L2 window
  Read. Do not invent pack/index commands to “load the repo.”

## Project adoption

Each project keeps a surface doc (filename is project-specific) listing its L0
recipes in a when-matrix. `CLAUDE.md` imports this rule and points at that doc.

Import from a project's `CLAUDE.md`:

```
@../devkit/rules/agent-tool-surface.md
```
