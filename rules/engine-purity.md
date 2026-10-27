# Engine purity

Applies when a repo keeps more than one engine family side by side.

## Families

| Family | Characteristic |
|--------|----------------|
| Rule / heuristic | Deterministic logic; no solver or learned model inside |
| Search / solver | Calls a combinatorial solver at its frontier |
| Learned | Inference from trained weights |
| Mixture | Composes two or more of the above |

## Rules

1. A rule engine must not call a solver or a learned model. That makes benchmarks non-comparable.
2. A solver library must not fall back to heuristics on failure. Return an error; the host decides the fallback.
3. A mixture is its own named engine, composed at the dispatch layer. Never a silent patch to a pure engine.

## Classify a new component

- Calls a solver: search, not a rule engine.
- Runs inference: learned, or a mixture if it also calls solvers or rules.
- Composes engines: a mixture. Give it its own name and its own benchmark row.

Import from a project's `CLAUDE.md`:

```
@../devkit/rules/engine-purity.md
```
