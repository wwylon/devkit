# External intake (portable, core)

Triage raw external/LLM idea dumps into verified registers. Full stages, kinds table, dedupe, dispositions and cross-product tools: [external-intake-reference.md](external-intake-reference.md) (read when ingesting). Run via skill `ingest-review <N>`.

- **When:** user cites an external review path, says "triage external"/"process this review", or gives a raw LLM export → intake **before** normal queue work. Other projects' requests are not intake: use [cross-project-messages.md](cross-project-messages.md).
- Never full-read raw exports (>~150 lines); read master/synthesis docs. One `intake_progress.md` row per theme.
- **Hard rule:** never assign a bug ID or `todo` from an LLM claim alone; verify (grep/repro) first.
- Dedupe against closed ledgers first; a `reject`/`trial-reverted`/`obsolete`/`dup`/`already_landed` row is **not** reopened without new evidence.
- No orphans: a round is ingested only when every theme row has an id, a closed disposition, or an explicit `unverified` tag; `park` needs an id and a written unlock criterion.
- Forbidden: implement from raw exports unverified; skip intake when the user provided external paths; re-promote a closed disposition without new evidence.
- Research-kind rows cite a `concept: <slug>` (librarian knowledge) when one exists.
- Local intake rule (routing table, register paths) stays in each project.
