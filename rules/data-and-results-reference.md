# Data and Results Rules

Shared discipline for all antigravity projects. These rules apply whenever you are making an optimization, running an accelerated kernel, or processing results from any long-running job.

## Oracle discipline

**External claims stay unverified:**
A paper, blog, or other project's number is not evidence until this repo's oracle agrees on the same case.

**Before/after same-seed proof (mandatory for every optimization commit):**
Every optimization commit records proof that outputs are unchanged. Run the kernel with a fixed seed before the change and after, compare outputs on a committed fixture (hash, inertia, assignment vector, equity table checksum — whatever the kernel produces). "It's faster" is not evidence. "Same bytes out, N× faster" is. If outputs legitimately change (better convergence), say so explicitly and show both numbers before and after.

**Equivalence test ships in the same commit:**
An accelerated or alternate implementation ships in the same commit with an equivalence test against its naive oracle. The test must prove its own power: assert the fixture actually exercises the divergent logic (e.g., assignments change after init). A vacuous test is worse than none — passing a broken path because the test case never exercises it defeats the purpose.

**Both sides of every threshold gate:**
Threshold-gated paths (k ≥ N, n > X, SIMD-vs-scalar, GPU-vs-CPU) are test-forced on both sides of the gate. Production must never be the first execution of a branch.

**Self-check at end of multi-hour runs:**
Multi-hour accelerated kernels end with a self-check: one exact pass (full or random-subsample) validating the fast path's output, failing loudly on mismatch. One naive pass worth of time is noise against a multi-hour wrong run.

**Binary provenance before citing tests:**
"Tests pass" is not "current source is verified" if the binary is stale. Before citing a test run as evidence for a change, confirm the binary was rebuilt after the source edit (build timestamp newer than source mtime, or a clean rebuild). A passing run against an August binary does not verify a September source change.

**"Too good" is a bug signal:**
When a bigger run behaves qualitatively unlike a smaller one (iteration time collapses, convergence 10× earlier than expected), treat outputs as suspect until explained. Cross-check with an independent implementation where cheap. This signal, not any test, is often what exposes a silent bug.

**Flaw found → sweep for siblings:**
Every confirmed flaw triggers a same-session search for the same class of flaw elsewhere (same author-pattern, same idiom, same API misuse). Record the sweep and its result — "checked X, Y, Z: clean" is as valuable as another finding.

- Classify the flaw against [rules/bug-patterns.md](bug-patterns.md); record the PAT ID in the problem entry when one matches.
- Sweep the siblings of that pattern, not just the exact code line you fixed.
- Record the sweep result in the problem entry, tied to the PAT ID: `PAT-002 sweep: checked X, Y, Z: clean`.

## Benchmark discipline

**Reduced-scale runs record every reduced dimension:**
Not just "smaller". Name each axis that was cut (problem size, iterations, sample count, hardware) so the number cannot be cited as the full run.

**Every optimization must be benchmarked:**
Static analysis is not a benchmark. Build the relevant bench target and run before and after. Record median of 5+ runs, not best-of-one.

**Record results in optimization_log.md:**
Each entry: date, commit, machine, benchmark name + params, before/after times, speedup ratio, output-changed status. If you improved quality (not just speed), say what changed and show both metric values. Note adopt/park in the entry and update `plan/STATUS.md` when the project maintains an idea matrix (see `rules/plan-structure.md`).

**Machine-specific defaults:**
Benchmark numbers are tied to a specific machine. Record the machine (CPU, RAM, GPU) in the entry. A number from a different machine is not a comparison point.

**Same-machine ratio, not absolute time:**
On a shared host, report `time_ratio = T_candidate / T_baseline` from one session. Absolute milliseconds are not a comparison.

**Stale numbers are debt:**
If a commit changes logic, defaults, or a bug on a path a published number used, record which runs are no longer current. Do not cite them.

## Fixed-size samples

- An aggregate over a fixed sample is valid only when the finished count equals the declared size. A partial aggregate is not a result.
- Compare it to the previous result of the same configuration. Worse beyond a stated epsilon is a regression.
- A crash or an illegal output fails the gate.
- Losing some cases to an oracle is a warning, not the ship gate.

## Monte Carlo gates

- Default CI stays on fast tests; long gates are marked slow and stay out of the default suite. State whether seed count or samples-per-seed moves each gate.

## Experiment ledger index

See `rules/plan-structure.md` § Experiment ledger index — same rules, don't duplicate here.

## GPU work — additional requirements
- Record GPU device (name, VRAM) in every GPU benchmark entry.
- GPU-vs-CPU oracle: when a GPU kernel replaces a CPU path, run both on the same input and compare outputs with an explicit tolerance policy (e.g., "max abs diff < 1e-5 on all elements"). Tolerance must be justified, not guessed.
- GPU tasks on the shared card: prefer full `gpu_vram_gib` so CPU-only work can still run; use `exclusive: true` only when overlap is unsafe (e.g. Ollama/vLLM keep_alive). See `rules/queue.md` and taskqueue `docs/task_standards.md` §3.

## File format / contract discipline

When changing binary file formats, adding header fields, or introducing new shared files between processes:
- Update `docs/data_contracts.md` in the same commit.
- Every reader validates format parameters at startup. Silent k-mismatch or format-version mismatch is a production crash waiting to happen.
