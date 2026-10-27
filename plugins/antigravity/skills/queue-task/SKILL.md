---
name: queue-task
description: Author a valid operator-queue YAML for a long-running task and verify it with tq list. Use when the user wants to enqueue a new task (train, gen, arena, equity, benchmark run). Invoke proactively when a requested action would take more than ~2 minutes.
argument-hint: "<task description or existing command to queue>"
allowed-tools: Read, Grep, Bash, Write, Edit
---

Author a queue YAML for: $ARGUMENTS

## Rules (from devkit/rules/queue.md — apply all)

1. **>2 min jobs always go in the queue.** Never launch as a background shell task. Create = write YAML + `tq sync`; MCP `enqueue_task` cannot create new tasks.
2. **`resume_args` is mandatory** if the tool supports `--resume`. Omit only if it genuinely does not. Restartable scripts should checkpoint when work units **or** ~10 minutes is due (`CheckpointCadence`); reset both counters after each write.
3. **`wall_clock_cap_sec` is mandatory** for any task that can deadlock (solvers, arena, network reads). Pilot: 3600. Full run: 86400. Cap kills are `interrupted` / `tq.run.cap` (not `failed` / `tq.run.nonzero`). Long checkpointable jobs that regularly hit the cap: add `auto_retry_on_cap: true` + `execution_semantics: checkpointable` (and `resume_args`) so the daemon re-queues without babysitting.
4. **Never guess paths.** Before writing args that reference a checkpoint or binary:
   - Run the inspect command (e.g., `pokerbot_inspect <path>`) and copy fields verbatim.
   - Check `tq list` for the project's known canonical args.
5. **Specify resource-consuming dirs explicitly** (e.g., `--bucket-dir`, `--grid`). Dev-scale defaults are wrong for production runs.
6. **GPU isolation:** prefer maximizing `gpu_vram_gib` (full card) so CPU tasks can still run. Use `exclusive: true` only when overlap is unsafe (Ollama/vLLM keep_alive, or owner requires machine-wide exclusivity). See taskqueue `docs/task_standards.md` §3.
7. **`(X.X%)` contract** — if writing a new CLI that queues tasks, it must emit `(X.X%)` on progress lines (prefer taskqueue `clients/python` or `clients/cpp`).
8. **`resources.ram_gib` is a hint** — set near expected peak RSS, not process ram-caps. Host soft/hard limits gate starts/stops.
9. **`dispatch: remote` is a prefer-remote hint** — with no online workers the master runs locally; do not use remote to park tasks.
10. **Queue hygiene** — after overnight / when finishing work on a project, triage that project's `failed` / `unknown` / cap `interrupted` tasks (diagnose → retry / `enabled: false` / `tq remove`); distinguish `[tq.run.cap]` (often just retry) from `[tq.run.nonzero]`. Prefer `tq retry --project P --status failed` over rapid single retries. Ignore `tq.block.*` waits. See `devkit/rules/queue-reference.md` § Queue hygiene / cleanup.
11. **Choose `dispatch` deliberately** — `local` for WSL/build; `remote` for GPU overnight (confirm `tq worker list` first); `any` only when either machine is fine. See `devkit/rules/master-worker.md`.
12. **Set `execution_semantics`** for pipelines that must not auto-restart (`at_most_once` / `non_idempotent` → `unknown` on lease loss; operator `tq retry`).
13. **Use `transfer:` for small round-trip artifacts** (<64 MiB upload); not for multi-GB datasets.
14. **Remote overnight:** run `tq worker list` before leaving `dispatch: remote` tasks — no workers means master fallback, not a parked queue.
15. **Pipelines:** sequence with `depends_on`. Quality gate = insert a check task (`tags: [check]`). Never use `on_complete` for “run next step”. Re-runnable sets (tests, i18n) must share `group:` or `suite:`. Restart a pipe with `tq retry <root> --downstream`, `tq group retry`, or filtered `tq retry --project P --status failed,interrupted`.

## Steps

1. Identify which project this task belongs to (check cwd or ask).
2. If editing the queue tool itself, work in `<portfolio-root>\taskqueue` (`main`, port **8765**). Do not use the retired `taskqueue-dev` tree.
3. Run `tq doctor` and confirm home / port / protocol before leaving overnight verification.
4. Look up the relevant CLI's `--help` output to get exact flags.
5. If the task references a checkpoint, run the inspect command and read the output.
6. Write the YAML to `experiments/operator_queue/<task_id>.yaml` in the project root (`enabled: true` admits after sync unless frozen/paused).
7. If this is part of a produce→check→consume pipe, write the check YAML too and wire `depends_on`.
8. Run `tq sync`, then `tq validate` on the new file (or project), then `tq list --project <project>` to confirm args.
9. Start the waiter: `tq wait <project>/<task_id> --timeout 3600` as a background command (Claude Code `run_in_background`), so the session is woken when the task settles.
10. Report: task_id, estimated resources, wall_clock_cap, whether resume_args / auto_retry_on_cap were set, `exclusive` vs `gpu_vram_gib` choice. Field details: active checkout `docs/task_standards.md`.
11. If the project already has failed/disabled clutter, clear it per queue hygiene before leaving the queue overnight.

## YAML template

```yaml
task_id: <short-kebab-id>
description: "<one sentence: what and why>"
priority: <50=normal, 10=high, 90=low>
enabled: true
command: <exe or bat name>
args: >
  <all flags, one per line with \ continuation or YAML block scalar>
resume_args: >
  --resume <same flags>
wall_clock_cap_sec: <3600 or 86400>
# auto_retry_on_cap: true          # checkpointable long jobs that grind across caps
# max_auto_retries: 20             # 0 = unlimited; shown in tq list as cap×N/M
group: <project>/<phase>   # required for re-runnable batches
# depends_on: [upstream-or-check]
# tags: [check]            # on verify tasks only
# dispatch: local          # or remote / any — see master-worker.md
# execution_semantics: checkpointable   # or non_idempotent for remote non-restartable
# notify_url: http://127.0.0.1:<port>/...   # opt-in end notify only
resources:
  cpu_cores: <N>
  ram_gib: <N>
  gpu_vram_gib: <0 or N>   # full card for GPU isolation without blocking CPU
# exclusive: true          # only if overlap unsafe (keep_alive / machine lock)
```
