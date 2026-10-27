#devkit

Shared agent rules, conventions, and Claude Code skills for multi-project workflows
(queue discipline, plan hubs, publish/export, intake).

This public tree is the portable subset. Clone it next to your projects, or `@`-import
individual files from `rules/`.

## What ships here

| Path | Contents |
|------|----------|
| `rules/` | Portable rules (`queue`, `plan-structure`, `house-standard`, `publish`, …) |
| `conventions/` | Templates for `plan/NOW`, `tasks`, STATUS, archive, publish manifests |
| `plugins/antigravity/` | Claude Code plugin: `/optimize`, `/queue-task`, `/publish`, `/idea`, `/handoff`, … |
| `tools/publish/` | Allowlist export → public GitHub mirrors (scan / verify / gated push) |
| `docs/` | House runbook and standardization notes |

Companion OSS product: [taskqueue](https://github.com/wwylon/taskqueue) (daemon, `tq` CLI, web UI, MCP).

## Plugin install

Point a local Claude Code marketplace at this checkout:

```json
// ~/.claude/plugins/known_marketplaces.json
"antigravity-devkit": {
  "source": { "source": "local", "path": "/path/to/devkit" },
  "installLocation": "/path/to/devkit"
}
```

Each project's `.claude/settings.local.json`:

```json
"enabledPlugins": { "antigravity@antigravity-devkit": true }
```

## Using the rules

Import the rules you need from `rules/` (e.g. `@devkit/rules/queue.md`). Typical set for a
queued research project: `queue`, `plan-structure`, `documentation-standards`, `agent-context`.

`bug-patterns.md` is for fixes, not every session. `publish.md` only when shipping a public mirror.

## Plan hub (in *your* projects)

devkit itself has no `plan/` directory. Consumer projects keep session priority in their own
`plan/NOW.md` (see [`rules/plan-structure.md`](rules/plan-structure.md)). Recommended layout:

- `plan/README.md` — dashboard
- `plan/NOW.md` — doing / next / waiting
- `plan/tasks.md` — active tasks only
- `plan/STATUS.md` — idea decisions (research portfolios)
- `plan/archive/` — completed acceptance prose

Templates live under [`conventions/`](conventions/).

## Publish tooling

```text
python tools/publish/cli.py --project-root /path/to/your-project doctor
python tools/publish/cli.py --project-root /path/to/your-project release --dry-run
python tools/publish/cli.py --project-root /path/to/your-project release --i-mean-it
```

See [`rules/publish.md`](rules/publish.md) and [`tools/publish/README.md`](tools/publish/README.md).

## License

MIT — see [LICENSE](LICENSE).
