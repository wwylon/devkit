# Master–worker rules (agents)

Short rules for research-project agents authoring remote YAML or triaging worker runs.

Canonical docs in the active taskqueue checkout:
- **Configure** (simple steps first): `docs/WORKER_SETUP.md` → section **Quick start — step by step**
- **Architecture** (sync, disconnect, logs): `docs/master_worker.md`

---

## When to use `dispatch`

| Value | Use when |
|-------|----------|
| `local` (default) | WSL builds, fast debug, master-only tools |
| `remote` | Prefer worker GPU/RAM overnight; **requires online worker** or master falls back |
| `any` | Either machine is acceptable; best-fit among online workers (default `placement_mode=binpack`), else local |

Do **not** use `dispatch: remote` to park tasks when no workers exist — use `local` or wait for `tq worker list` to show online workers.

---

## What syncs on remote runs

| Mechanism | Direction | Notes |
|-----------|-----------|-------|
| `code.provider` (git_patch / bundle) | Master → worker at claim | Per-attempt workspace under `{home}/runs/<run_id>/work` |
| `data/` directory | Master → worker before each task | Full manifest diff; not opt-out per task |
| `transfer` push | Master → worker before spawn | Small artifacts only |
| `transfer` pull | Worker → master after success | |
| Logs | Worker → master **during run** | Every ~5s / 100 lines via log-chunk; **not** bulk at finalize |

View logs before task completes: `tq logs`, web UI, MCP `log_tail`.

---

## Required YAML for remote

- **`requires`** — OS, RAM, GPU tags so the worker can claim the task.
- **`resources.ram_gib`** — hint near expected peak RSS (not process cap).
- **`execution_semantics`** — non-idempotent pipelines: use `at_most_once` or `non_idempotent`; lease loss → `unknown` (manual `tq retry`).
- **`transfer`** — round-trip files under ~64 MiB per upload; not for multi-GB datasets.

---

## Do not

- Point a WIP experimental worker at prod master (`:8765` / default `~/.taskqueue`).
- Assume logs appear only after finalize on remote runs.
- Leave `dispatch: remote` overnight without checking `tq worker list`.

---

## Disconnect expectations

| Semantics | Lease lost / hung (idempotent path) |
|-----------|--------------------------------------|
| `idempotent` / `checkpointable` | Auto re-queue |
| `non_idempotent` / `at_most_once` | Status **`unknown`** — operator runs `tq retry` |

Worker restart is safe: pending finalizes flush from `{worker_home}/pending_finalize/`.

---

## Verify before overnight remote

```powershell
tq doctor
tq worker list
tq capacity
tq list --project <project>
```

Triage: `tq diagnose <project/task_id>` · MCP `capacity` / `diagnose`.

---

## Related

- [queue.md](queue.md) — general queue discipline
- [queue-reference.md](queue-reference.md) — CLI quick reference
- taskqueue `docs/task_standards.md` §4 — full field reference
