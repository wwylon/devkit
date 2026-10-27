# Test audit tiers (portable)

Shared test-audit strategy for agent-driven development in repos whose test
suites are too large to run in full mid-task. Project-specific suite names,
filter strings, and config files stay in each repo's local audit rule — this
file is only the **tier model**, the fail-first rule, and the status-summary
rule.

## Why

When a repo has thousands of subtests, full obligatory runs are correct for
pre-merge but too slow for mid-task iteration. Domain-only selection is still
hundreds of tests. The goal is the **smallest batch that maximizes failure
signal**, stopping early on failures.

## Four tiers

| Tier | Name | When | Scope |
|------|------|------|-------|
| **L0** | Baseline floor | Every mid-task audit | Always included: foundation + smoke (seconds) |
| **L1** | Fast batch | Mid-task after a domain edit | Curated pinned subtests per domain covering distinct subsystems (minutes) |
| **L2** | Changed selection | Mid-task default | Tests intersecting changed files (git diff) |
| **L3** | Full obligatory | PREMERGE, queue `done`, nightly | Full domain / obligatory suite |

L1 and L2 are **screening** — they do not replace L3.

## Rules

- **Fail-first.** Stop on the first N failures, fix, re-run. Do not wait for
  the full batch to finish before reacting.
- **Status summary, not full logs.** Agents read a compact status / todo file
  produced by the audit tool, not full parallel suite stdout. Do not paste
  large suite logs into context.
- **Never lock build output during long audits.** Audit tooling must not hold
  a lock on the build directory that blocks concurrent builds; stage or
  snapshot as needed instead.
- **L3 is mandatory before merge.** Screening tiers do not satisfy pre-merge
  or queue-`done` gates.
- **Curate L1, do not sample it.** L1 is a pinned list of subtests that cover
  distinct subsystems (invariants, regressions, idea pins) — not a random
  subset. Re-measure L1 timing after corpus or suite growth.

## Project adoption

Each project keeps a local audit rule naming its audit script, suite groups,
fast-batch config, and filter strings. `CLAUDE.md` imports this rule and
points at the local one.

Import from a project's `CLAUDE.md`:

```
@../devkit/rules/test-audit-tiers.md
```
