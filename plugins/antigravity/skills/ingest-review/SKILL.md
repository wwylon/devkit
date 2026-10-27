---
name: ingest-review
description: Ingest an external-LLM review round (plan/external/<N>) into the project's registers using the shared kind taxonomy. Use when the user cites a round path, says "triage external" or "ingest round N".
argument-hint: "<round number>"
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

Ingest round $ARGUMENTS. Rules: `<portfolio-root>/devkit/rules/external-intake.md`. Local mapping: `plan/INTAKE.md`
(missing -> copy `devkit/conventions/INTAKE-template.md` and fill it first).

1. Read `plan/external/<N>/README.md` and `PACK_INFO.md`. Missing PACK_INFO: note it, continue, mark rows `pack_sha: unknown`.
2. Staleness: for files the findings cite, `git log --oneline <pack_sha>..HEAD -- <file>`; changed file = read the current code before judging.
3. Read synthesis / the findings table only. Never full-read a raw export over ~150 lines (Grep for ids).
4. One row per **theme** in `intake_progress.md` (template `conventions/intake_progress.md`): set `kind` (default `investigate`).
5. Dedupe before new ids: grep `plan/ideas_closed.md`, `STATUS.md`, prior `intake_progress.md`. Hit -> cite prior id, disposition `dup`/`reject`/`already_landed`; no new id without new evidence.
6. Verify each open row by grep/symbol/probe (⏳ -> 🔍 -> ✅/❌). Never create an F-/task from an LLM claim alone.
7. Promote by kind to the register named in `plan/INTAKE.md`; fill `id`/`task`. `park` needs id + "unlock" in notes.
8. Finding owned by another project: write an inbox message (`<portfolio-root>/inbox/README.md`), disposition `forwarded->file`.
9. List the round in `plan/external/README.md`; run `py <portfolio-root>/devkit/tools/intake/round_check.py --project .` until clean.
10. Stop after ingest. Implementing is a separate ticket (NOW / queue).
