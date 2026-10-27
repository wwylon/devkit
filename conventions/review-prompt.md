# Review prompt (paste with the pack; append the focus line)

You review attached code from project `<project>` at commit `<pack_sha>` (see PACK_INFO.md).
Return ONE markdown table, no prose before it, max 40 rows, highest value first. Columns:
`id | file:symbol | claim | kind | severity | suggested check`
- `kind`: bug (wrong behaviour) | perf (measurable speed/memory) | code (refactor/dev-process/tooling) | investigate (value unknown, name a cheap probe) | research (algorithm/model hypothesis)
- `severity`: high | med | low. `claim` is one sentence naming the failing input or the measurable gain.
- Cite only code you see in the pack. If unsure, kind = investigate. No duplicates; no style nits.
Then a 5-line "themes" list grouping the ids.

Focus (pick one): **bugs** - correctness, races, error paths, boundary values ·
**perf** - hot paths, allocations, algorithmic cost, with how to measure ·
**design** - coupling, duplicated logic, dead code, missing tests/docs ·
**ideas** - improvements to the algorithm/product, each with an experiment to test it.
