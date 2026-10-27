---
name: idea
description: File an entry in the shared game-bot-theory ideas repository, or pull an existing idea into a project's tasks.md. Use when you spot a technique that might transfer across projects, or when the user wants to browse or schedule shared ideas.
argument-hint: "<idea description | list | pull <idea-slug> into <project>>"
allowed-tools: Read, Write, Edit, Grep, Glob
---

## Ideas repository

Location: `<portfolio-root>\devkit\ideas\game-bot-theory.md`

Each project also has its own local backlog (e.g., `plan/new_ideas/ideas002.md`). The shared repo holds ideas that might transfer to 2+ projects. Per-project ideas that are clearly domain-specific stay local.

## If $ARGUMENTS starts with "list"

Read `<portfolio-root>\devkit\ideas\game-bot-theory.md` and summarize all entries with their applicability tags.

## If $ARGUMENTS starts with "pull"

Parse: pull `<idea-slug>` into `<project>`.
1. Find the idea in `game-bot-theory.md` by slug.
2. If the project has `plan/STATUS.md`, add a row with Decision `design` (or `coded` if already implemented) and Next = schedule when ready.
3. Add or update an entry in that project's `plan/tasks.md` ideas backlog / active table when scheduling, tagged with the idea slug.
4. If scheduling immediately, also list it under `plan/NOW.md` → Next.
5. Report what was added.


## Otherwise — file a new idea

1. Identify a short kebab-case slug for this idea.
2. Determine which projects it applies to from the consumer table in `<portfolio-root>\devkit\README.md` (not only the game repos).
3. Append to `<portfolio-root>\devkit\ideas\game-bot-theory.md`:

```markdown
## <slug>

**Applies to:** <project1>, <project2> | all
**Domain:** <algorithmic | data-layout | parallelism | benchmarking | gpu | sampling | abstraction | search>
**Status:** idea (not scheduled)
**Source:** <project/commit or "conversation YYYY-MM-DD">

<2-4 sentence description of the idea, the mechanism, and why it might transfer.>

**Transfer notes:** <what would be different in each target project, or "straightforward port">
```

4. Confirm what was written and offer to pull it into a specific project's STATUS / tasks / NOW.
