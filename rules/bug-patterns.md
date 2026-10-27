# Bug & flaw patterns (portable catalog)

Recurring structural patterns that let bugs hide or propagate in research codebases
(C++/Python, solvers, training pipelines, job queues). Distilled from concrete
postmortems across the antigravity projects.

IDs are stable: cite them in problem entries (`**Pattern:** PAT-NNN`) so the same
taxonomy works across repos. PAT-004 is intentionally absent (iterative-solver
discount scope — domain-specific; kept in the originating project's local catalog).
Projects keep their own concrete bug-ID tables locally; this file is the shared
pattern list.

**Use:** when you fix a bug, classify it against this list, sweep for siblings of
the same pattern, and record the sweep in the problem entry (see
`data-and-results.md` → "Flaw found → sweep for siblings").

## PAT-001 — Silent Fallback to Incorrect Default

**Signal:** `return {}` / fallback-to-uniform / default answer on an error path; empty lookup result used without log or exception.
**Failure:** An invariant violation or failed lookup silently degrades to a plausible-looking but wrong default; the caller never learns a failure occurred.
**Remediation:** Every semantics-altering fallback emits a warning at minimum, or throws. Silent fallbacks to any "default" answer are prohibited. Same pattern: a CLI/flag that claims mode X but silently runs Y (e.g. "RL" wrapper that actually does supervised training) — surface the mismatch or refuse.

## PAT-002 — Non-Atomic File Write

**Signal:** `std::ofstream(path, ios::trunc)`, `path.write_text(...)`, `json.dump` straight to the final path.
**Failure:** Truncate-then-write leaves the file empty or partial if the process is interrupted mid-write — checkpoints and queue state destroyed.
**Remediation:** Write to `path.tmp`, verify the write succeeded, then rename over the target (Python `os.replace` / C++ `std::filesystem::rename`).

## PAT-003 — Wrong Clock Domain / Epoch Confusion

**Signal:** `steady_clock` and `system_clock` values in one subtraction; absolute timestamps sent across process or machine boundaries.
**Failure:** Epoch mismatch yields massive random deltas — instant timeouts or infinite deadlines.
**Remediation:** Transmit relative durations (`budget_ms: int`), never absolute `steady_clock` timestamps. `system_clock` absolutes are portable only on the same machine.

## PAT-005 — Cross-Language / Cross-Boundary Representation Drift

**Signal:** Two implementations of the same state on opposite sides of a boundary with no round-trip test; float vs integer money, enum packing, count assumptions.
**Failure:** Producer and consumer diverge silently; every downstream metric is wrong while each side's own tests pass.
**Remediation:** One documented canonical representation per field; an integration test that checks the consumer bit-for-bit against the producer on the same input.

## PAT-006 — Duplicate Algorithm with Silent Divergence

**Signal:** The same function (hash, kernel, selection) implemented in 2+ files.
**Failure:** Copies drift apart (different variants, different layouts); a fix lands in one copy and the other keeps the bug.
**Remediation:** Extract to a single shared implementation; add a test that compares both call sites' outputs on identical inputs.

## PAT-007 — Magic Number Silently Truncates Execution

**Signal:** Hardcoded guard (`guard < 16`, `MAX_BYTES = 128`, `pass < 64`) sized for typical cases; fixed-width integer for a quantity that can outgrow it.
**Failure:** Real inputs exceed the bound and execution silently truncates or wraps, returning a subtly wrong result instead of failing.
**Remediation:** Named constants derived from parameters; exceeding a bound is a logged error or exception, never silent truncation.

## PAT-008 — Mutable Shared State in Multi-Depth Recursion

**Signal:** Object-level `mutable` scratch buffer or flag read after recursive calls return.
**Failure:** Child recursion overwrites the parent's scratch; the unwinding parent reads stale/corrupted data.
**Remediation:** Per-depth state indexed by recursion level; object-level scratch must be stateless between calls; assert depth bounds on access. For sibling-branch search (e.g. PIMC world siblings), rebuild the cursor / scratch from the root prefix per branch — never share a ply cursor across siblings even if they share a prefix.

## PAT-009 — Byte-Level Coupling Between Format and Consumer

**Signal:** Consumer reads serialized bytes at hardcoded offsets (`key[-2]`, `buf >> 8`) with no version byte.
**Failure:** Any serializer change — even a bug fix — silently corrupts every consumer reading fixed offsets.
**Remediation:** Expose structured parsed state instead of raw bytes; if byte serialization is mandatory, add a version byte and a canonical deserializer co-located with the serializer.

## PAT-010 — Pinned Resource Never Released

**Signal:** Large `static` / Meyers-singleton allocation; gigabyte-scale tables built at first use and held for process lifetime.
**Failure:** Memory stays pinned long after the phase that needed it; RAM budgets are meaningless because the baseline is invisible.
**Remediation:** Allocate large objects via `shared_ptr` returned from init so the caller controls lifetime and can release explicitly after the consuming phase.

## PAT-011 — Stopping Criterion ≠ Selection Objective

**Signal:** Early stopping / pruning uses one objective (e.g. EV separation) but the final pick uses another (e.g. win-rate, posterior mean).
**Failure:** A branch survives stopping because it looks good on the proof metric, then wins on the selection metric for an unrelated reason; the reported "best" was never actually best on the metric that matters.
**Remediation:** Make the stopping metric and the selection metric the same, or prove a documented dominance relation between them. Never silently swap metrics between phases.

## PAT-012 — Merge Across Incompatible Likelihood Scales

**Signal:** Weights / particles / likelihoods from different sources or timesteps are combined (sum, normalize, top-up) without a common scale.
**Failure:** One source dominates not because it is more probable but because its units are larger; the merge is numerically fine and semantically wrong.
**Remediation:** Normalize each source to a documented common scale before any combine; assert the scales in a test. A merge is a tested operation, not arithmetic.

## PAT-013 — Soft Zero Treated as Positive Mass

**Signal:** A zero / missing likelihood or weight is represented as a small positive epsilon for numeric convenience; downstream samplers / rejections treat it as genuine support.
**Failure:** The model assigns positive probability to a state the evidence actually rules out; rare branches never die.
**Remediation:** Distinguish "zero" from "small" at the type level (optional / masked tensor, not a magic epsilon). Rejection and exact samplers must treat true zero as zero, not as epsilon.

## PAT-014 — Weighted Loss Backprops Zero-Weight Rows

**Signal:** A weighted loss (e.g. Bradley–Terry, cross-entropy) receives `row_weight=0` rows but the loss still produces a nonzero gradient for them.
**Failure:** Rows meant to be excluded still shape the model; "I weighted them out" is false.
**Remediation:** Mask zero-weight rows out of the loss entirely (multiply logits *and* targets by the mask, or skip them), not just scale the loss. Add a test that asserts zero-weight rows contribute zero gradient.

---

This file is a reference catalog: link it from session rules and read it during
fixes — it does not need to be loaded every session. To import anyway:

```
@../devkit/rules/bug-patterns.md
```
