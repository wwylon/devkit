---
name: optimize
description: Run the shared research optimization loop: capture baseline + same-seed fixture → implement change → equivalence oracle → re-bench (median 5+) → record in optimization_log.md → optionally file transferable idea. Use when asked to optimize, speed up, or improve a kernel.
argument-hint: "<kernel or module name to optimize>"
allowed-tools: Read, Grep, Bash, Write, Edit, Glob
---

Run the optimization loop for: $ARGUMENTS

## The loop (from devkit/rules/data-and-results.md — all steps mandatory)

### Step 1 — Baseline

Before touching any code:
1. Identify the bench target for this kernel (look in `CMakeLists.txt` for bench targets, or check `docs/benchmarking.md`).
2. Build the bench target in release mode.
3. Run 5+ times, record the median. Save to scratchpad.
4. Run the kernel with a fixed seed and save the output fixture (hash or full output). This is the oracle.

### Step 2 — Implement

Make the optimization. Keep the scope minimal — don't refactor beyond what's needed.

### Step 3 — Equivalence oracle

1. Build again.
2. Run with the same fixed seed. Compare output to the Step 1 fixture.
3. If outputs differ: stop. Explain what changed and why it is acceptable before continuing.
4. Write or update an equivalence test that: (a) runs the optimized path, (b) compares to the naive oracle, (c) exercises the divergent logic (not a vacuous case).
5. Force-test both sides of any threshold gate (e.g., k≥256 vs k<256).

### Step 4 — Re-benchmark

Run 5+ iterations again. Record median before and after.

### Step 5 — Record

Append to `plan/optimization_log.md`:

```
## <Date> — <commit> — <kernel name>

**Machine:** <CPU, RAM, GPU if relevant>
**Benchmark:** <target name> <params>
**Before:** <median time>
**After:** <median time>
**Speedup:** <ratio>
**Output changed:** no (same fixture) | yes (<what changed, and why acceptable>)
**Equivalence test:** <test name or "added">
**Gate coverage:** both sides tested | N/A
**Decision:** adopt | park | reject | n/a — update `plan/STATUS.md` when applicable
```

If the project has an experiment ledger index (`docs/results/EXPERIMENT_INDEX.md` or `scripts/build_experiment_index.py`), refresh it after writing a new ledger entry (or remind the owner). Contaminated runs: set `cite: false` in the meta overlay.

### Step 6 — Optional: file transferable idea

If the optimization pattern (algorithmic, data-layout, parallelism strategy) is not specific to this project, offer to file it in `<portfolio-root>\devkit\ideas\game-bot-theory.md` with applicability tags. Use `/idea` for this.

If NOW / STATUS changed (new next experiment, adopt/park), update `plan/NOW.md` and `plan/STATUS.md` in the same session (`rules/plan-structure.md`).

## Signals to stop and report

- "Too good" output: iteration time collapses or convergence is 10× faster than a smaller run would predict. This is a bug signal. Stop, report, do not record as a win.
- Equivalence failure: outputs differ without a clear justification. Stop, report, revert.
