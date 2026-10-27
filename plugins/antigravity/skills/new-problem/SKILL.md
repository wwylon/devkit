---
name: new-problem
description: File a new problem entry (F-ID) with UTC timestamp in problems_open.md and add a row to problems.md index. Use when a confirmed bug, data contract violation, or systemic issue is discovered.
argument-hint: "<brief problem description>"
disable-model-invocation: true
allowed-tools: Read, Grep, Write, Edit, Bash
---

File a new problem entry for: $ARGUMENTS

## Steps

1. Get current UTC timestamp: run `date -u +"%Y-%m-%dT%H%MZ"` (Linux/WSL) or check the date.

2. Read `plan/problems.md` to find the next F-ID (look for the highest F-NNN in the index table).

3. Append to `plan/problems_open.md`:

```markdown
## F-NNN — <short title>

**Filed:** <YYYY-MM-DDTHHMMZ>
**Severity:** <critical | high | medium | low>
**Status:** open
**Affected:** <component or file>
**Pattern:** <PAT-NNN from devkit/rules/bug-patterns.md, or "none">

### Description

<What is wrong. Be specific: what input, what output, what was expected.>

### Root cause (if known)

<Or: unknown — needs investigation>

### Fix plan

<Or: unknown — diagnose first>

### Acceptance criteria

- [ ] <specific, verifiable criterion>
```

If the flaw matches a pattern in `<portfolio-root>\devkit\rules\bug-patterns.md`, record the PAT ID in `**Pattern:**` and plan the sibling sweep for that pattern inside **Fix plan** (see `data-and-results.md` → "Flaw found → sweep for siblings").

4. Add a row to `plan/problems.md` index table:

```
| F-NNN | <short title> | <severity> | open | <YYYY-MM-DDTHHMMZ> |
```

5. Report: F-ID assigned, severity, what needs investigation next.

6. If the problem **blocks scheduled work**, add a line under `plan/NOW.md` → Waiting (and keep Status `open` in the index). See `<portfolio-root>\devkit\rules\plan-structure.md`.
