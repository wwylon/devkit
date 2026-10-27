# Optimization Log — <Project Name>

Records all performance experiments. See `<portfolio-root>\devkit\rules\data-and-results.md`.

**Not a status board.** Adopt/park decisions live in `STATUS.md` (and ADRs under `decisions/`). This file is the chronological proof trail. Experiment catalogs (if any) index ledger runs separately.

Format per entry:

```
## YYYY-MM-DD — <commit> — <kernel or target name>

**Machine:** <CPU model, RAM GiB, GPU if used>
**Benchmark:** <target name> <params (seed, scale, threads)>
**Runs (ms):** <all 5+ raw values>
**Median:** <value ms>
**Speedup:** <ratio vs previous baseline, or "baseline">
**Output changed:** no (fixture hash: <hash>) | yes (<what and why>)
**Equivalence test:** <test name> | N/A
**Gate coverage:** both sides tested | N/A
**Decision:** adopt | park | reject | n/a — link STATUS / ADR if applicable
**Notes:** <anything unusual>
```

---

<!-- First entry below -->
