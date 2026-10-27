---
name: benchmark
description: Run a bench target (median of 5+ runs), capture the result, and record it in plan/optimization_log.md. Use when benchmarking without a full optimization loop, or to establish a baseline before starting /optimize.
argument-hint: "<bench target name or description>"
disable-model-invocation: true
allowed-tools: Read, Grep, Bash, Write, Edit
---

Run and record a benchmark for: $ARGUMENTS

## Steps

1. Find the bench target. Check `CMakeLists.txt` or `docs/benchmarking.md` for the target name. If unknown, grep for "bench" in the build dir.

2. Build in release mode:
   ```
   cmake --build --preset release --target <bench_target>
   ```

3. Run 5+ times with the same parameters. Record all measurements. Compute median.

4. Note the machine: CPU model, RAM, GPU if relevant (run `tq detect` for a quick summary).

5. Append to `plan/optimization_log.md`:

```markdown
## <YYYY-MM-DD> — <commit> — <bench target> baseline

**Machine:** <CPU, RAM, GPU>
**Benchmark:** <target> <params>
**Runs (ms):** <all 5+ values>
**Median:** <value>
**Notes:** baseline | comparison to previous: <ratio if known>
```

6. Report: median time, machine, and where the result was recorded.

7. If this run wrote or updated `experiments/ledger/<id>/`, refresh the project's experiment index if it has one (`build_experiment_index` / `run_experiment` hook). If the bench supports an adopt/park decision, update `plan/STATUS.md` and note it under `plan/NOW.md` when it changes next work.

## Flags

- If this is a **before** measurement for an upcoming `/optimize` run, say so explicitly in the Notes field.
- If outputs need to be captured for the oracle, also save: `<bench_target>_fixture_<date>.bin` or a hash of the output in the same log entry.
