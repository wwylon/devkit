# Queue Rules

Shared queue discipline for all antigravity projects. These rules apply whenever you are authoring a YAML task or running any long job.

## Official Standards & Reference Docs

For detailed technical specifications on writing task scripts and configuring them under the taskqueue system, see (https://github.com/wwylon/taskqueue or your local checkout):
* **[Task Standards](https://github.com/wwylon/taskqueue/blob/main/docs/task_standards.md)** — Progress `(XX.X%)` contract, checkpoint/`resume_args`, resources, YAML fields, dispatch/workers, `notify_url`.
* **[MCP server](https://github.com/wwylon/taskqueue/blob/main/docs/mcp.md)** — `tq mcp` tools including `drain_notifications`, `progress_snapshot`, `diagnose`.
* **[Project README](https://github.com/wwylon/taskqueue/blob/main/README.md)** — state home, CLI (`tq metrics`, `tq diagnose`, …).
* **[Master–worker configuration](https://github.com/wwylon/taskqueue/blob/main/docs/WORKER_SETUP.md)** — bind, auth, `worker.yaml`, setup checklist.
* **[Master–worker architecture](master-worker.md)** — dispatch, sync, disconnect, logs — for remote YAML and triage.

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

### Daemon home

| | Default |
|--|---------|
| Tree | `<portfolio-root>\taskqueue` @ `main` |
| Home | `~/.taskqueue` |
| UI | `:8765` |

Before overnight leave or queue edits, run `tq doctor` and confirm home, port, and `protocol`.

## Long-running jobs go in the queue

Any command expected to take more than ~2 minutes must be written as a YAML in the project's `experiments/operator_queue/` directory, then `tq sync` (and `tq validate` before overnight leave). With `enabled: true`, the daemon admits the task — there is no separate “owner start” step. Leave `enabled: false` (or use `tq freeze` / `tq pause`) only when the owner must gate admission. Never launch these as background shell tasks inside an agent session (a background `tq wait` watcher is fine — it only waits). This keeps long jobs restartable, logged, and off the session context.

## Preflight before enqueueing

Before any medium+ or overnight job:

1. **Audit the code path** you are about to run: data contracts, label provenance (config hash / checkpoint), train/val leakage, atomic writes ([PAT-002](bug-patterns.md)), kill/resume paths, silent-fallback risk ([PAT-001](bug-patterns.md)).
2. **Write a one-paragraph preflight note** (`preflight.md` next to the run dir, or a journal bullet) listing what you checked.
3. **Smoke tier green first:** the project's smoke/tiny config must pass after the audit, before the full run. GPU tasks already require a sibling `*_smoke` YAML with `depends_on` (see [queue-reference.md](queue-reference.md)) — reuse that convention, don't invent a new one.
4. **New idea gate:** any new optimizer, architecture, or loader change needs a timed smoke run with telemetry (throughput, peak RAM/VRAM) logged before the long job.
5. **Do not start additional heavy jobs under load** without owner confirmation.

## Large mmap training tasks

Stream from disc; do not load the full matrix into heap. Formulas and the worked example are in [queue-reference.md](queue-reference.md).

## YAML authoring rules

**Before writing a YAML that references a checkpoint or binary artifact:**
Run the project's inspect command and copy the relevant fields verbatim. Never guess paths or parameter values.

**`resume_args` is mandatory for restartable tasks:**
Set `resume_args` in the YAML for any task whose tool supports `--resume`. When a task is retried the daemon uses `resume_args` automatically; without it the task restarts from scratch. If a tool does not support `--resume`, note this in the YAML description.

**`wall_clock_cap_sec` is mandatory for any task that can deadlock or hang:**
Subgame solving, arena runs, and any process that reads from a network or socket can deadlock silently. Without a cap the process runs forever. Use 3600 for pilots, 86400 for full runs. There is no good reason to omit this. Cap kills land as `interrupted` / `tq.run.cap` (not `failed` / `tq.run.nonzero`). Long checkpointable jobs that regularly hit the cap should set `auto_retry_on_cap: true` + `execution_semantics: checkpointable` (and `resume_args`) so the daemon re-queues without babysitting — see taskqueue `docs/task_standards.md`.

**Do not call a shared build script from concurrent tasks.**
Two tasks rebuilding the same binary will overwrite it mid-run. Use the project's wrapper that serializes build and execute.

**Always pass resource-consuming directories explicitly:**
Never rely on tool defaults for bucket-dir, grid, or similar multi-scale parameters. The default often points at a dev-scale fixture. Specify the production path explicitly in the YAML args.

**`(X.X%)` progress contract:**
The daemon parses `(XX.X%)` from subprocess output and displays progress + ETA. Any CLI that runs as a queue task emits that form. Do not change the format. Helpers, checkpoint cadence, and suspend handling are in taskqueue `docs/task_standards.md`.

**`dispatch: remote` is a hint:** Prefer an online remote worker; if none are online, the master runs the task locally (still subject to `requires`). Do not use `dispatch: remote` to park work when you have no remote fleet — use `local` or wait for workers.

**`resources.ram_gib` is a hint:** Soft host gate `ram_limit_pct` blocks new starts when the machine is over soft used%; hard gate `ram_hard_limit_pct` stops the highest-RSS local queue task (`status=stopped`, `tq.stop.ram`). Set `ram_gib` near expected peak RSS (not process ram-caps). The scheduler may auto-restart `stopped` tasks when soft clears unless last peak would hit hard again (`tq force` bypasses).

**GPU: prefer `gpu_vram_gib` over blanket `exclusive`:** `exclusive: true` blocks **all** other tasks (CPU included). For GPU isolation while CPU work should continue, set `gpu_vram_gib` to the full card size (or near-full model footprint). Use `exclusive: true` mainly when a runtime keeps weights loaded across tasks (Ollama/vLLM `keep_alive`) and overlap is unsafe. Details: taskqueue `docs/task_standards.md` §3.

**`group` field for task sets:**
Use the `group:` YAML field to cluster related tasks for `tq group list|stop|retry` and the web UI group filter. Convention: `<project>/<phase>`. Groups are an operational label — they do **not** change admission priority. Prefer `suite:` when you need enable/disable/retry of a labeled batch via `tq suite`. Both `group retry` and `suite retry` re-queue **completed** members.

## Pipelines (after results)

One model for sequencing and gates — do not invent workflow DSLs or call `tq` from inside a task:

| Need | What to do |
|------|------------|
| **Sequence** | Consumer `depends_on: [producer]` |
| **Verify then continue** | Insert a **check** task (`tags: [check]` or `*-check`); consumer depends on the check. Fail ⇒ dead dependency (expected) — fix/retry the check, not mass-retry consumers |
| **Choose B or C** | Pre-author both `enabled: false`; after notify, enable **one** via MCP/`tq patch` |
| **Re-run a bunch** | Shared `group:` / `suite:` + batch retry; `tq retry --project P --status failed,interrupted`; multi-ID `tq retry proj/a proj/b`; or `tq retry <root> --downstream` for a dep pipe |

Shell cleanup after exit → YAML `teardown`, not `on_complete`. (`on_complete` / `on_fail` are advanced wake lists of task IDs only.)

Canonical fixture: `tqdemo` `dummy-pipe-a` → `dummy-pipe-check` → `dummy-pipe-b` (`group: tqdemo/pipe`).

**Block new starts for a project (`tq freeze`):**
`tq freeze <project>` / UI **Block project** (when a project is selected) sets `project_frozen_<name>` so the scheduler skips **new starts** for that project only (`tq.block.frozen`). Running tasks continue. `tq unfreeze` clears it. Softer cousin: `tq pause` / `tq resume`. Do not invent a separate “block sync” flag.

**`tq force`:**
One-shot soft resource / anti-flap bypass; re-queues the task. Expect UI toast “Forced — starts when admitted”; deps and mutex locks still apply.

**Verify before leaving the queue overnight:**
Run `tq validate` (path or all registered) and `tq list` after writing the YAML. Check all args are correct. A wrong arg discovered 8 hours in costs a full overnight window. Close finished jobs in the same session by updating the project's `plan/NOW.md` (Waiting / Next / Doing) — see [queue-reference.md](queue-reference.md).

**Cite `#run_id` when talking about a run:**
Once a task starts (or after it finishes), the dashboard and history show a numeric **`#<run_id>`** for that attempt. When reporting status to the owner, asking about a failure, or coordinating with another agent, include that number (e.g. `#142`) along with `project/task_id`. It disambiguates retries and is shorter than full paths. MCP tools and `tq` output expose the same value as `run_id`.

**Every task must be restartable:**
If a task is interrupted (power loss, OOM, manual stop) or RAM-stopped, the next start/`tq retry` should resume from the last checkpoint when `resume_args` exist. Design tasks and their tools to support this.

**Opt-in end-of-task notify (`notify_url`):**
Agents do not need this to wait (use `wait_for_task` / `tq wait`). When the owner wants a real notification when the task ends, set `notify_url` to a loopback HTTP(S) webhook in the YAML (see task_standards). Omit otherwise. The master appends every terminal event to `{TASKQUEUE_HOME}/notify.jsonl` regardless of `notify_url`. Remote webhook hosts need `tq config set notify_allow_remote=1`.

## Triage / CLI / wait patterns

See [queue-reference.md](queue-reference.md) — triage decision tree, status meanings, `tq` CLI, web UI ports, wait patterns, project queue directory.
