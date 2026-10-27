# Queue Reference

Operational reference — triage, CLI, wait patterns. Read when running or debugging queue tasks.
Authoring rules: `devkit/rules/queue.md`. Standards: `taskqueue/docs/task_standards.md`.

## Waiting on a queue task

Do not busy-wait with sleep loops or repeated `my_tasks` calls. Right after `tq sync` / `tq add` / `tq retry`, run `tq wait project/task_id --timeout 3600` as a background command (Claude Code: `run_in_background`; the session is re-invoked when it exits — a watcher, not a job). Several tasks: list the keys, or `--suite S` / `--group G` / `--tag T` / `--project P`; add `--any` to wake on the first. Exit codes: 0 completed, 1 failed/stopped/suspended, 2 timeout (start it again), 3 not found. With the tq MCP server configured, `wait_for_task` (short `timeout_sec`, repeat on `timed_out`) then `task_result` does the same in-turn; `submit_task` / `retry_task` responses carry a ready-made `next` call. `notify_url` + `drain_notifications` is only for external webhooks/alerts. Use `tq status` / `tq diagnose` for triage. When the task reaches a terminal status, close it out and update `plan/NOW.md` (Waiting / Next / Doing) in the same session.

## Queue hygiene / cleanup

Failed and disabled rows accumulate unless agents triage them. Use **triage-first** — never mass-retry or silently delete without a decision.

**Status meanings**

| Status | Meaning | Default action |
|--------|---------|----------------|
| `failed` | Ran and died — needs a decision | Triage (below); do not leave as long-term state |
| `failed` + `[tq.run.nonzero]` | Real non-zero exit (not a wall-clock cap) | Diagnose; retry only if transient |
| `interrupted` + `[tq.run.cap]` | Hit `wall_clock_cap_sec` | Safe to `tq retry` (or wait for `auto_retry_on_cap` grinding / `cap×N/M`); not the same as a crash |
| `failed` + `max_attempts=N reached` | Attempt budget exhausted | `tq patch … max_attempts=0` (or raise N) then `tq retry` — bare retry alone will not admit |
| `unknown` | Lease / hung loss on non-idempotent task | Manual `tq retry` after triage — do not assume auto-restart |
| `disabled` (`enabled: false`) | Intentional shelf | Keep YAML if reusable; remove when abandoned |
| `completed` | Done | `tq remove` after results are filed |
| `queued` + `tq.block.*` | Waiting (deps / RAM / CPU / frozen) | **Not** a cleanup target |

**When to run**

- After overnight or when touching a project's queue: MCP `attention_list` / `tq status` for real terminals (`failed` / `interrupted` / `suspended` / `stopped` / `unknown`). Ignore pure `tq.block.resources` / `tq.block.deps` waits.
- Same session as closing out a finished job (update `plan/NOW.md`).

**Failed — pick one**

1. Transient / fixed → `tq diagnose` then `tq retry`. If `max_attempts` exhausted (status `failed`, block/error text mentions `max_attempts=… reached`), raise or clear the budget via `tq patch … max_attempts=0` (or a higher N) **then** retry.
2. Want later → set `enabled: false` in the YAML and sync (park as disabled).
3. Abandoned → delete or move the YAML out of `operator_queue/` and `tq remove project/task_id`.
4. Never mass-`tq retry --project` without diagnose. Prefer filtered batch: `tq retry --project P --status failed` or `… --status interrupted` (one DB transaction). Multi-ID: `tq retry proj/a proj/b`.
5. **Dead dependency / failed check:** if `block_reason` says `dead dependency: …-check [failed]`, fix and retry the **check** (or upstream), not the blocked consumer. Consumers stay blocked until the dep is `completed` again.

**Batch re-run**

- Filtered project retry: `tq retry --project P --status failed,interrupted` (daemon `/api/tasks/retry-batch`).
- Shared `group:` / `suite:` on re-runnable sets (tests, localization). `tq group retry` / `tq suite retry` re-queue **completed** members too.
- Dep pipe from a root: `tq retry project/root --downstream`.

**Disabled**

- Keep while the YAML remains and may be re-enabled.
- If the experiment is abandoned → remove YAML + `tq remove`.
- Do not use disabled to hide undiagnosed failures.

**Completed**

- After results landed (optimization_log / NOW / archive): `tq remove`.
- Weekly hygiene: prune completed older than ~14 days is fine (`tq prune` dry-run first).

**Hard don'ts**

- Do not treat `tq.block.resources` / `tq.block.deps` / `tq.block.frozen` / `tq.block.paused` as failures.
- Do not delete YAMLs the owner may still need without checking NOW / experiment notes.
- Cross-operator `tq remove` may need `--force` (same ownership gate as stop).

## tq CLI reference

Agent-critical subset. Full banner: `tq help`. Daemon log is `tq log`; task log is `tq logs` / `tq tail`.

```
Daemon
  tq start | stop-daemon | restart
  tq doctor                         Home, schema, pid, port, protocol
  tq log [--bytes N] [--grep PAT]   Daemon.log (not task logs)
  tq detect | master-status | master-migrate <url>

Inspect
  tq status [--project P] [--json]
  tq list [--project P] [-v] [--tag T] [--suite S]
  tq describe <project/task_id>
  tq watch | wait <project/task_id>
  tq my-tasks [--operator NAME]     Needs TQ_OPERATOR
  tq capacity | fair-share | report [--days N]
  tq metrics <project/task_id>      Same payload as UI / MCP progress_snapshot

Tasks
  tq sync                           Re-sync YAML dirs (prefer explicit sync after write)
  tq add|submit <yaml> --project P
  tq validate [path.yaml]           Lint before overnight leave
  tq stop | suspend | retry | force | remove <project/task_id>
  tq retry --project P [--status failed[,interrupted,…]]   # batch; one TX
  tq retry proj/a proj/b …                                 # multi-ID batch
  tq patch <project/task_id> k=v…   priority|enabled|wall_clock_cap_sec|max_attempts
  tq priority | logs | tail | diagnose | deps
  tq tag add|rm <project/task_id> <tags…>
  tq group list|stop|retry <project> <group>

Projects / workers
  tq projects | pause|resume | freeze|unfreeze
  tq suite enable|disable|retry <suite>
  tq bundle <project>
  tq worker list|remove|setup|sync | tq worker --master … --worker-id …
  tq config get|set k=v… | tq prune [--apply] | tq mcp
```

**Hygiene:** `tq.block.frozen` / `tq.block.paused` / `tq.block.deps` are **waits**, not failures — do not mass-retry them as if failed.

**Remote worker triage:** `tq worker list` · `tq capacity` · `tq diagnose <project/task_id>`. Architecture: `devkit/rules/master-worker.md` · taskqueue `docs/master_worker.md`. Task `unknown` after lease loss → manual `tq retry` (non-idempotent semantics).

### MCP tools (`tq mcp`)

| Tool | Role |
|------|------|
| `queue_status` | Compact daemon summary (home, port, counts) |
| `my_tasks` | Tasks for `TQ_OPERATOR` / `operator` arg |
| `attention_list` | failed / interrupted / suspended / stopped needing triage |
| `capacity` | Cluster free/reserved CPU RAM GPU |
| `diagnose` | Deep bundle for one task |
| `report` | Aggregate runs/errors |
| `progress_snapshot` | Live progress + resources (UI metrics) |
| `log_tail` | Byte-offset log tail (`offset` / `max_bytes` / optional `grep`) — not a `lines` arg |
| `wait_for_task` | Block until a task leaves queued/running (use `timeout_sec` 30–60, repeat on `timed_out`) |
| `task_result` | Structured result: exit_code, duration, peaks, metrics, error_code |
| `drain_notifications` | Terminal events from `notify.jsonl` (written for every task; `since` cursor, `wait_sec` long-poll). Other replies carry `finished_since_last_call` |
| `agent_usage_summary` / `tq agents` | Usage analytics: who calls what, task provenance + outcomes (counters only) |
| `enqueue_task` / `retry_task` | Re-queue **existing** terminal task only — cannot create |
| `patch_task` | `priority` / `enabled` / `wall_clock_cap_sec` / `max_attempts` |
| `stop_task` | Cooperative stop |

Schemas: active checkout `docs/mcp.md`. Prefer MCP when configured; fall back to CLI.

Queue web UI: `http://127.0.0.1:8765`. Locales EN/PL/ZH/AR. Queue page: status → project → **group** filter chips; **Block project** when a project is selected; **Deps ↑** sort; **?** help. Running cards and history show **`#<run_id>`**.

**Session planning:** priority lives in `plan/NOW.md` — tq does not parse plan markdown. See `rules/plan-structure.md`. When a queue job finishes, close it out and update NOW (Waiting / Next / Doing) in the same session.

## Project queue directory

Each project's queue YAMLs live in `experiments/operator_queue/` relative to the project root (default; set in `~/.taskqueue/projects.yaml` if different). Prefer `tq sync` after writing YAML (watchdog can pick up sooner; ~60 s is the fallback interval). Drop a YAML there with `enabled: true`; the daemon admits it — no separate “owner start” step unless the task is intentionally `enabled: false` or the project is frozen/paused.

## Large mmap training tasks

When authoring train YAMLs that read a large mmap / `np.memmap` cache:

- `mmap_mode="r"` alone is **not** enough — the train path must **stream from disc** (per-sample reads). Do not `np.asarray` / fancy-index / `concatenate` the full feature matrix into heap; do not `TensorDataset(torch.tensor(X_train))` over a full split.
- CUDA mmap trains must **feed the GPU**: `--workers` ≥2 + `--prefetch-factor` + pin_memory. Val DataLoader uses `num_workers=0`.
- On Windows, each worker's working set can hold ~1–2 GiB of the mmap on a large split. Declare `ram_gib` from **process-tree RSS** (parent + workers), not parent alone.
- **Mid-epoch `(X.X%)` required** for streamed epochs that can take hours.
- Re-measure `ram_gib` after any corpus-size jump; never copy an old small-split hint onto a large one.
- Do **not glue epochs across trainer-code changes**: if trainer/dataset code changed since the run was stamped, start a new `--out` + `--init-from`. Resuming into a stale checkpoint under changed code is the anti-pattern.
- mmap cache > 2 GiB → `teardown:` flush_page_cache.py (**not** `on_complete`).
- Resume must prefer **per-unit checkpoints** over aggregate `metrics.json`.
- `group:` GPU admission estimates can block unrelated CPU work — put CPU-only gates in a non-GPU group.
- `metadata:` in queue YAML is **doc-only** until the queue preserves it; never write code that reads it via `tq list` output.

### Worked RAM estimate

```
cache_gib = n_rows × (2706×feat_bytes + 2652×4 + 1326) / 2^30
peak_train_gib ≈ cache_gib / shard_count
resources.ram_gib = peak_train_gib + 2.0
```

| Gate | Rule |
|------|------|
| `cache_gib > 50%` host RAM | `--shard-count 0` (auto) + `--write-val-pack` at prepare time |
| `gpu_vram_gib > 0` | sibling `*_smoke` YAML with `--smoke-batches 20 --require-gpu` + `depends_on` |
| mmap cache > 2 GiB | `teardown:` flush_page_cache.py (not `on_complete`) |
| `resume_args` | use `--resume` (not `--warmstart-pt`) once the `last.pt` contract is available |

Shard layout for that estimate: `pokerbot/docs/data_contracts.md`.

