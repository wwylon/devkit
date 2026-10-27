# External intake (portable)

Shared pipeline for external / LLM idea dumps. Project-specific **routing tables
and register paths** stay in each repo's local intake rule. This file owns the
**stages**, verify-before-promote gate, and **anti-retry** dispositions.

## When

Requests from **other projects** are not intake: they use [cross-project-messages.md](cross-project-messages.md) (`<portfolio-root>/inbox/`).

User cites an external review path, says "triage external", "process this
review", or provides a raw LLM export. **Before** normal queue work, run intake.
Intake-only sessions may end without a `doing` task.

## Standard round and kinds (all projects)

Run via skill `ingest-review <N>` (`plugins/antigravity/skills/ingest-review`; Cursor: follow its SKILL.md).
Round folder `plan/external/<N>/`: `README.md`, `PACK_INFO.md` (from `pack_code`: git SHA, dirty),
`raw/<llm>.md`, `intake_progress.md` (columns add `kind`, header `pack_sha`). List the round in
`plan/external/README.md`. Prompts: `conventions/review-prompt.md`. Check: `tools/intake/round_check.py`.
Before verifying, compare `pack_sha` with HEAD (`git log <sha>..HEAD -- <file>`); changed file = re-read first.

Every theme gets exactly one **kind** (the project's `plan/INTAKE.md` maps kinds to its registers;
template `conventions/INTAKE-template.md`):

| kind | meaning | register | verify gate |
|------|---------|----------|-------------|
| `bug` | logic flaw | `problems*.md` F-NNN | repro or cite code |
| `perf` | speed/memory | `optimization_log.md` | bench |
| `code` | refactor, dev-process, tooling | `plan/ideas/code_{open,done}.md` | not already landed |
| `investigate` | unknown value, cheap probe (safe default) | `plan/ideas/investigate_{open,done}.md` | probe written |
| `research` | algorithm/model hypothesis | `plan/ideas/research_{open,done}.md` + `STATUS.md` | experiment design |
| `request` | owned by another project | inbox message; disposition `forwarded->file` | n/a |

Closed on arrival (`reject`/`dup`/`obsolete`/`already_landed`): `plan/ideas_closed.md`.

## Stages

### 0 — Drop

Land files under `plan/external/<round>/` (or product inbox). Record path, date, source.

### 1 — Ingest (no code changes)

1. Confirm round folder; create next round for new batches.
2. Read **master** / synthesis docs — never full-read raw exports (>~150 lines).
3. Append **one row per theme** (not per source file) to `intake_progress.md`.
4. Update the cross-round manifest / index of rounds in the same commit (one row per round, with its intake file or "backfill").
5. Optional: `products: [a,b]` for cross-repo ideas; fingerprint = slug + primary symbol/path.

### 1b — Dedupe (before new ids)

Search closed ledgers for the theme / fingerprint:

- Bridge2: idea Archive, `reject` / `trial-reverted` rows, ADRs.
- Slim: `plan/STATUS.md`, `plan/ideas_closed.md`, prior `intake_progress`.

On hit → cite prior id; **do not** open a new IDEA/T-* unless the orchestrator
cites **new evidence** (new metric, new API, explicit reopen).

### 2 — Verify (mandatory)

For each unverified row: grep / symbol-search. Status: ⏳ → 🔍 → ✅ or ❌.

Classify:

- **Already landed** → `already_landed`; link existing fix.
- **Correctness bug** → F-register path (local).
- **Perf** → OPT / queue (local).
- **Speculative** → idea register, column until confirmed.
- **Obsolete / wrong** → `obsolete` / ❌ with reason.

**Hard rule:** never assign a bug ID or `todo` from an LLM claim alone.

**No orphans:** a round is ingested only when every theme row has an id, a closed disposition, or an explicit `unverified` tag. `park` needs an id **and** a written unlock criterion; a parked row without an id is lost.

### 3 — Promote

Local routing tables map types → registers / queues / STATUS rows. Set intake
`Task ID` + ✅ when promoted. Use `doing` only when implementation starts.

### 4 — Work

One ticket per session (NOW / queue).

### 5 — Close (mandatory)

When tried or discarded, set a **disposition** (see below) with one-line reason
and evidence link. Never delete closed rows.

## Dispositions (anti-retry)

Task verbs (`doing` / `todo` / `done`) live in tasks/queues. Idea dispositions:

| Disposition | Meaning | Retry? |
|-------------|---------|--------|
| `unverified` | Ingested, not checked | Continue verify |
| `open` / scheduled | Verified, on backlog | Yes |
| `shipped` / `adopt` / `opt-in` | Done or kept | No (unless regression) |
| `park` | Measured; not now | Only if unlock criteria written |
| `reject` | Wrong / worse / failed | **No** without new evidence |
| `trial-reverted` | Coded then rolled back | **No** without new evidence + note/ADR |
| `obsolete` / `dup` | Superseded | **No** — cite survivor |
| `already_landed` | Already fixed | **No** |

## Cross-product

If `products: [...]`, dedupe in each product's closed ledger and follow
`devkit/tools/product_chains.yaml` when present (provide-then-consume). Upstream
`reject` / `trial-reverted` should be noted on downstream intake as `dup` /
`obsolete` (use `intake_cli.py chain-note`).

```powershell
python <portfolio-root>\devkit\tools\intake\idea_dedupe.py --project bridge2 --theme "IDEA-HTN-151"
python <portfolio-root>\devkit\tools\intake\intake_cli.py drop --file PATH --products bridge2,pimc
python <portfolio-root>\devkit\tools\intake\intake_cli.py chain-note --upstream dds_alpha --downstream bridge2 --theme theme-slug --disposition reject
```

**Reopen a reject:** only with **new evidence** (new metric, API change, or
operator unlock note). Cite the prior id; do not mint a parallel IDEA.

## Forbidden

- Implement from raw exports without verification.
- Full-read raw exports in normal sessions.
- Skip intake when the user provided external paths.
- Re-promote a closed disposition without new evidence.

## Project adoption

Local intake rule = routing table + register paths + helpers. Import portable
phases here; point at the local rule for promote details. A project should also
keep an index of rounds and a closure check (script) that fails on an unindexed
round or a park/todo row without an id.

Templates: `devkit/conventions/intake_progress.md`, `ideas_closed.md`.

```
@../devkit/rules/external-intake.md
```
