# Data and Results Rules (core)

Applies when optimizing, running accelerated kernels, or reporting results. Detail, benchmark recording, GPU and file-format rules: [data-and-results-reference.md](data-and-results-reference.md) (read for optimization/benchmark work; `optimize`/`benchmark` skills load it).

- **External claims are unverified** until this repo's oracle agrees on the same case.
- **Same-seed before/after proof** on a committed fixture for every optimization commit; the **equivalence test ships in the same commit** and must prove its own power (fixture exercises the divergent logic).
- **Test both sides of every threshold gate** (k>=N, SIMD/scalar, GPU/CPU); production is never the first execution of a branch.
- **Multi-hour runs end with a self-check** (one exact pass, fail loudly).
- **Binary provenance:** "tests pass" counts only if the binary was rebuilt after the source edit.
- **"Too good" is a bug signal:** a bigger run behaving unlike a smaller one is suspect until explained.
- **Flaw found -> sweep siblings** in the same session; classify against [bug-patterns.md](bug-patterns.md) (PAT id) and record `PAT-NNN sweep: checked X, Y: clean`.
- **Benchmarks:** record every reduced dimension; median of 5+; same-machine ratio, not absolute time; record in `optimization_log.md`; stale numbers are debt.
- **Fixed-size samples:** an aggregate is valid only when finished count equals declared size; worse beyond a stated epsilon is a regression; crash/illegal output fails the gate.
- Changing a binary file format/contract: update `docs/data_contracts.md` in the same commit; readers validate format params at startup.
- Experiment ledger index: see `rules/plan-structure.md`. Long gates are marked slow and stay out of the default suite.
