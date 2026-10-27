# Queue Rules (core)

Shared queue discipline. Authoring YAML, preflight, pipelines, `tq` details: [queue-authoring.md](queue-authoring.md) (read when writing a task YAML or planning a pipeline); triage/CLI/wait patterns: [queue-reference.md](queue-reference.md); skill `/queue-task`. Specs (taskqueue repo): `docs/task_standards.md`, `README.md`, `docs/mcp.md`, `docs/WORKER_SETUP.md` — https://github.com/wwylon/taskqueue

### First calls (every session that touches the queue)

1. **Create tasks** = write YAML under `<project>/experiments/operator_queue/` then `tq sync`. MCP `enqueue_task` only re-queues *existing* terminal tasks — it cannot create new ones.
2. Set **`TQ_OPERATOR`** in the environment so `started_by` / `my_tasks` work.
3. Run **`tq doctor`** (and/or MCP `queue_status`) before overnight leave — confirm home `~/.taskqueue` and port **8765**.
4. **After `tq sync` / `tq add` / `tq retry`, start a waiter in the same turn:** `tq wait <project>/<task_id> --timeout 3600` as a background command (Claude Code `run_in_background` wakes you when it exits; `tq` prints this as a `Next:` line). Exit 0 = completed, 1 = failed/stopped → `tq diagnose`, 2 = timeout → start it again. On wake, report the result and update `plan/NOW.md`. MCP `wait_for_task` is the same thing where the tq MCP server is configured; never poll with sleep loops. `notify_url` is only an external webhook.
5. Prefer **`dispatch: local`** unless you mean remote; `resources.ram_gib` ≈ expected peak RSS; cite **`#run_id`** when talking about a run.
6. For live CPU/RAM/VRAM/GPU like the UI metrics dialog: MCP **`progress_snapshot`** / **`diagnose`**, or CLI **`tq metrics project/task_id`**.
7. Remote: set **`execution_semantics`** (or `idempotent`); prefer **`git_patch`/`bundle`** workspaces over shared `project_root`.

### Do not

* Launch >~2 min jobs as in-session background shells — use operator-queue YAMLs.
* Invent YAML keys / worker APIs — use `task_standards.md` + README.
* Invent a parallel taskqueue “dev” tree — use the product `main` checkout only.
* Treat `dispatch: remote` as a way to park work with no fleet (it falls back to local when no workers are online).
* Mass-`tq retry` without triage — see [queue-reference.md](queue-reference.md) hygiene.


## Long-running jobs go in the queue

Any command expected to take more than ~2 minutes must be written as a YAML in the project's `experiments/operator_queue/` directory, then `tq sync` (and `tq validate` before overnight leave). With `enabled: true`, the daemon admits the task — there is no separate “owner start” step. Leave `enabled: false` (or use `tq freeze` / `tq pause`) only when the owner must gate admission. Never launch these as background shell tasks inside an agent session (a background `tq wait` watcher is fine — it only waits). This keeps long jobs restartable, logged, and off the session context.

Mandatory in every YAML (details in queue-authoring.md): `resume_args` for restartable tools; `wall_clock_cap_sec` for anything that can hang (3600 pilot / 86400 full); explicit production paths for resource directories; the `(XX.X%)` progress contract; one **smoke** tier green before a long run; copy checkpoint/binary fields verbatim from the project's inspect command, never guess. Run `tq validate` + `tq list` after writing the YAML. Cite `#run_id` when reporting a run. Before overnight leave run `tq doctor` (home `~/.taskqueue`, UI `:8765`).
