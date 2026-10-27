# Plan Structure Rules

Shared `plan/` discipline for all antigravity projects. Import this rule from each project's `CLAUDE.md` / agent entry so agents bootstrap the same way everywhere.

## Required files

| File | Role |
|------|------|
| `plan/tasks.md` | Active scheduled work only (slim tables). Human-facing checklist — tq does not parse this. |
| `plan/problems.md` | Problem index (open rows first). |
| `plan/problems_open.md` | Full write-ups for open problems. |
| `plan/problems_fixed.md` | Institutional memory for closed problems. |
| `plan/optimization_log.md` | Chronological bench proofs (append-only). |

Keep these filenames stable — shared skills and agents depend on them.

## Recommended hub files

| File | Role |
|------|------|
| `plan/README.md` | Dashboard (≤40 lines): product default, links to NOW / STATUS / tasks / experiments / problems. |
| `plan/NOW.md` | **What next** — Inbound / Doing / Next / Waiting / Do not reopen. Must fit on one screen. **Inbound** = accepted cross-project requests (message filename; [cross-project-messages.md](cross-project-messages.md)); first when it holds P0/P1 items. |
| `plan/archive/` | Completed milestone acceptance prose (stable task IDs preserved). |
| `plan/development_journal.md` | Session narrative — **not** a status board. |

## Optional research files

| File | When to use |
|------|-------------|
| `plan/STATUS.md` | Idea / algorithm decision matrix (`adopt` / `park` / …). |
| `plan/RESEARCH_PLAN.md` (or equivalent catalogue) | Idea text, deps, expected effect — **not** a second decision matrix. |
| `plan/decisions/` | ADRs for non-trivial adopt/park/reject calls. |
| `experiments/ledger/` + experiment index | Immutable A/B runs + regenerable catalog (see below). |

Templates: `devkit/conventions/`.

## Ownership map (one owner per question)

| Question | Owner | Everyone else |
|----------|-------|---------------|
| What do I do next / waiting on? | **`plan/NOW.md`** | `tasks.md` links to it at top |
| Which tasks are active? | **`plan/tasks.md`** (slim) | Completed ACs → `plan/archive/` |
| What is each idea's decision? | **`plan/STATUS.md`** (if used) | Catalogue keeps idea text only |
| Product default today? | Top of STATUS + one sentence in README | Survey docs link STATUS |
| Did we run experiment X? Outcome? | Experiment index (if used) | Ledger dirs immutable; opt-log chronological |
| Is bug F-NNN open? | **`plan/problems.md`** | open / fixed write-ups |
| Why adopt/park | **`plan/decisions/`** | STATUS Evidence column |
| Session narrative | **`plan/development_journal.md`** | Header: not a status board |

If two files disagree, the **owner** wins; update the owner, then fix pointers.

## Task workflow status (`tasks.md` / `NOW.md`)

| Value | Meaning |
|-------|---------|
| `doing` | Actively in progress this session |
| `todo` | Scheduled, unblocked |
| `waiting` | Blocked on external/dep (state the blocker in Notes / NOW) |
| `done` | Acceptance checked; prose may live in `plan/archive/` |
| `parked` | Intentionally not pursuing |
| `postponed` | Deferred to a later milestone |

Do **not** use: `partial`, `needs_attention`, `ready`, `deferred` (legacy Plan-tab computed states — map into the table above).

## Idea decision status (`STATUS.md` / idea registers only)

| Value | Meaning | Retry? |
|-------|---------|--------|
| `adopt` | Product default / default-ON | No (unless regression) |
| `opt-in` | Shipped, default-OFF, kept | No |
| `park` | Measured; not default; code may remain | Only if unlock criteria written |
| `reject` | Measured worse / failed — **keep the row** | **No** without new evidence |
| `trial-reverted` | Coded then rolled back | **No** without new evidence + note |
| `obsolete` / `dup` | Superseded | **No** — cite survivor |
| `already_landed` | Already fixed elsewhere | **No** |
| `design` | Spec only | Continue |
| `coded` | Implemented; A/B missing or inconclusive | Continue |
| `measuring` | Next / in-flight experiment | Continue |

Do not mix task workflow verbs into STATUS, or idea decisions into task Status
columns. Closed idea rows must not be deleted (anti-retry). Full pipeline:
[external-intake.md](external-intake.md). Slim products may use
`plan/ideas_closed.md` for reject/trial-reverted archive.

## Session protocol

1. Read **`plan/NOW.md`** first (then `STATUS.md` if the project has one).
2. Open `tasks.md` only for active task detail / acceptance criteria.
3. When finishing a task or changing priority, update **`NOW.md` in the same session**.
4. When adopting/parking an idea, update **STATUS** + optimization_log / ledger evidence; ADR if non-trivial.
5. Append non-obvious findings to `development_journal.md` — do not treat the journal as the schedule.

## Closing completed work

1. Check every acceptance checkbox; cite ledger / test / CI evidence.
2. Mark the task `done` in `tasks.md`, then **move** long AC prose to `plan/archive/` (keep stable IDs).
3. Update `NOW.md` (remove from Next / Doing).
4. Journal entry for non-obvious outcomes (see also `rules/milestones.md`).

## Experiment ledger index (when the project has A/B ledgers)

Immutable store: `experiments/ledger/<id>/` (`metrics.json`, config copy, report).

Maintain a regenerable catalog (typical paths):

- `docs/results/EXPERIMENT_INDEX.md` (+ optional `.json`)
- `experiments/ledger_index_meta.yaml` — overlay: `r_ids`, `task`, `decision`, `cite`, notes

Rules:

- Index lists **all** ledger ids; meta tags important runs with idea/task/decision.
- Contaminated or do-not-cite runs: `cite: false` in meta (called out at top of the index).
- Refresh the index after successful experiment runs (project hook), or run the project’s `build_experiment_index` script.
- Unit/regression tests live under `tests/` + CI — they are **not** the experiment archive.

## What NOT to do

- Do not bury “what’s next” inside a 300-line done-task dump.
- Do not keep two decision matrices (STATUS vs catalogue §audit vs survey).
- Do not delete ledger or optimization_log history.
- Do not invent project-private status vocabularies that diverge from this rule.
- The slim `NOW` / `tasks` layout is the default. If a project documents a different layout, do not migrate it back.
