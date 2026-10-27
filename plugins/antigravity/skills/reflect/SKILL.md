---
name: reflect
description: Mid-task self-assessment. Produces a structured 5-section report on what you're doing, where you're wasting time, documentation staleness, one concrete improvement, and a single recommendation. Use when asked to stop and evaluate your current approach.
argument-hint: "<optional: context about what you're currently doing>"
allowed-tools: Read, Grep, Bash
---

Stop and reflect on the current work: $ARGUMENTS

## Output format

Write exactly five sections, numbered, in this order:

```
## 1. What I'm doing
One or two sentences: the immediate task and its broader goal.

## 2. Efficiency
Name the single biggest waste or inefficiency in the current approach. Be specific — name loops, deal counts, tools not used, regressions introduced. If the approach is sound, say so explicitly and say why.

## 3. Documentation staleness
Which docs are stale or unverified right now? Name them. If none, say so.

## 4. One improvement worth making
One concrete action, not a list. Something that can be done now.

## 5. Recommendation
**[Continue / Change approach / Pause]:** one sentence directive. Pick one.
```

## Rules

- Total length: 20–35 lines. Not a wall of text.
- Section 4 names exactly one improvement. No bullets, no numbered sub-list.
- Section 5 picks exactly one option and states it as a directive, not a question or multiple options.
- Direct and opinionated. No hedging ("perhaps", "might consider", "could potentially").
- Do not invent problems that aren't present. If the approach is fine, say so in section 2 and recommend Continue.
