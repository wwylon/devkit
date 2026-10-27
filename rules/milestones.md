# Milestone Rules

Shared milestone discipline for all antigravity projects. These rules apply whenever you are advancing, closing, or opening a milestone.

## What a milestone is

A milestone is a named checkpoint in the project roadmap (M0, M1, … or equivalent). Each milestone has:
- A set of tasks (in `tasks.md` or equivalent) whose acceptance criteria must all be **checked in CI**.
- An optional **gate condition** (operator compute job, human sign-off, external measurement) that must complete before the milestone closes.
- A one-line entry in the **CLAUDE.md milestone line** reflecting its current state.

## Milestone states

| State | Meaning |
|-------|---------|
| `in progress` | Active — at least one task not yet `done`. |
| `✅` | Closed — all tasks `done`, gate (if any) passed, journal entry written. |
| `blocked (reason)` | Waiting on an external dependency (compute job, human decision, external service). |

## Closing a milestone

Do all of the following **in a single commit**:

1. **Verify every acceptance checkbox is checked** in `tasks.md`. Never mark a milestone done with an unchecked AC or a failing test.
2. **Update `tasks.md`** — mark milestone tasks `done`; move long acceptance prose to `plan/archive/` (keep stable task IDs). See `rules/plan-structure.md`.
3. **Update `plan/NOW.md`** — remove finished items from Doing/Next; set the next ordered work.
4. **Update the CLAUDE.md milestone line** — mark the closed milestone done, open the next one as active, and record the key result inline. Keep the line compact (one sentence per milestone).
5. **Write a journal entry** in `development_journal.md` — date, milestone name, key results, gate outcome. Link to relevant experiments/ledger paths. Do not host problem write-ups here. Journal is not a status board.
6. **Do not advance the milestone line** if any gate condition is pending (e.g., overnight compute job not yet complete). Put the blocker under `NOW.md` → Waiting and use `blocked (gate: reason)` on the milestone line.

## Opening the next milestone

When a milestone closes:
1. Add the next milestone to the CLAUDE.md milestone line as `**Active:**`.
2. Ensure the first `todo` task of the new milestone has its `Depends` satisfied; list it under `NOW.md` → Next.
3. Do not pre-fill task status — tasks start as `todo` and agents pick them up from `NOW.md` (session protocol in `plan-structure.md`).

## CLAUDE.md milestone line format

The milestone line is the single most-read line across sessions. Keep it accurate and compact:

```
- **Milestone:** **M3** — M0 ✅ · M1 ✅ · M2 ✅. **Active:** T3.1 (brief description). <any blocking gates or queue jobs>.
```

Rules:
- Closed milestones: `MN ✅ (key result)` — one clause each.
- Active milestone: `**Active:** TN.N — description; queue jobs in flight.`
- Blocking gates: name the gate and its status inline (e.g., "M4 gate T4.9 pending — Slumbot run queued").
- Update this line every session that changes milestone state. Stale milestone lines mislead the next agent.

## Gate conditions

Some milestones require a gate before closing — a compute job, an external calibration, or a human decision. Rules:

- **Document the gate in `tasks.md`** on the relevant task: what must happen, what evidence suffices, what the accept/reject criterion is.
- **Gate is compute-only:** queue the job, mark milestone `blocked (gate: job queued YYYY-MM-DD)`, close the milestone when the job completes and evidence is recorded.
- **Gate is a human decision:** write the evidence clearly (results, CI, link to ledger), mark `blocked (gate: owner review)`, and present it in the session handoff. Do not close the milestone yourself.
- **Losing is acceptable in calibration gates** — the point is to have a result with CI, not to win. Record the loss rate and move on.

## What NOT to do

- Do not mark a milestone `done` from within a compute job's YAML or a long-running operator run — milestones are closed by an agent session that reads results and checks ACs.
- Do not skip the journal entry — it is the permanent record of what was shipped and what was measured.
- Do not merge open milestone state into a closed one's `✅` — once closed, a milestone line is a historical fact, not an accumulator.
