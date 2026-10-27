# Intake progress (round N) — template

Copy to `plan/external/<N>/intake_progress.md`. One **theme** per row (not one per source file).

`pack_sha:` <git sha from PACK_INFO.md>  ·  kinds: bug perf code investigate research request (see `rules/external-intake.md`)

Legend: ⏳ unverified · 🔍 verifying · ✅ promoted/closed · ❌ false/N/A

| theme | source | status | kind | disposition | id | task | notes / evidence |
|-------|--------|--------|------|-------------|----|------|------------------|
| Example theme | glm §1 | ⏳ | investigate | unverified | | | fingerprint: `slug` + symbol |

**No orphans:** every row needs a `kind` and an `id`, a closed disposition, or an explicit `unverified` tag; `park` needs an id and an unlock criterion in `notes`. List the round in the project's index of rounds.

**Anti-retry:** before new ids, grep this file + `plan/ideas_closed.md` / STATUS / idea Archive for `reject` / `trial-reverted` / `obsolete` / `dup` / `already_landed`. See `devkit/rules/external-intake.md`.
