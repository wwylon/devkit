---
name: handoff
description: Produce an end-of-session ranked next-steps list per the session protocol. Use at the end of any session where the user is blocked waiting for a long-running job or has finished a task. Invoke proactively when the work is done or stalled.
argument-hint: "<optional context: what was just completed or what we're waiting for>"
allowed-tools: Read, Grep, Bash
---

Produce the end-of-session handoff for: $ARGUMENTS

## What to do

1. Read plan state in this order (see `<portfolio-root>\devkit\rules\plan-structure.md`):
   - **`plan/NOW.md`** (required) — Doing / Next / Waiting / Do not reopen
   - `plan/STATUS.md` if present — idea decisions that affect next work
   - `plan/tasks.md` — active task detail only
   - `plan/problems_open.md` — open blockers
   - Optionally MCP `my_tasks` / `attention_list` / `queue_status` (or `tq status` / `tq list --project <name>`) for queue jobs

2. Build a ranked list from NOW (do not invent a parallel priority from old status words):
   - **Doing** first — already started.
   - **Waiting** that just unblocked (queue finished, dep landed) — promote to Next with close-out steps.
   - **Next** in the order written in NOW.
   - Open **problems** that block Next items.
   - Do **not** reopen items listed under Do not reopen.

3. For each item, include:
   - Task/problem ID and one-line description
   - Estimated effort: XS / S / M / L
   - Why it's the right next step (one sentence)

4. Note any items from `<portfolio-root>\devkit\ideas\game-bot-theory.md` that are newly applicable given today's work.

5. If NOW is stale vs completed work this session, say so and list the NOW edits the owner should make (or make them if still in the same session).

## Format

```
## Handoff — <date>

**Completed this session:** <one line>
**Waiting on:** <queue task or "nothing">

### Next steps (ranked)

1. [doing] **T5.3** — <task> (M) — already started
2. [next] **T5.2** — <description> (S) — <why now>
3. [waiting→ready] **T4.9** — queue finished; close out ledger (XS) — <why>
```
