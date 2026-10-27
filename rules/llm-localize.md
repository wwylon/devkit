# llm_localize — cross-project agent rules

Applies when working in any repo that registers a `.llm-localize.toml`
(bridge, llm_localize dogfood, taskqueue, etc.).

## What it is

Package at `<portfolio-root>\llm_localize`. Translates, validates, and scans
message catalogues with a local LLM (Ollama). Consumer repos own all catalogue
data; the package supplies machinery only.

## Hard constraints (do not violate)

- Never import `taskqueue` from llm_localize — integration is YAML blueprints +
  `tq` subprocess only.
- Never write into a consumer repo except through configured paths in
  `.llm-localize.toml`.
- State key format and hash algorithms are frozen — do not change without ADR.
- `core/` stays pure (no I/O, no project knowledge).

## Operator surfaces

| Surface | When to use |
|---------|-------------|
| `llm-localize validate` | CI gates, no LLM |
| `llm-localize status` | coverage check |
| `llm-localize web` | browse, inline edit, Ops drawer |
| `llm-localize translate` / `improve` | batch fill or quality passes |
| taskqueue YAML under `experiments/operator_queue/` | long sweeps |

CLI and web share `llm_localize/ops/` (ADR-14). Web binds `127.0.0.1` only.

## In consumer repos

1. Config lives at `.llm-localize.toml` in the project root.
2. Register in `~/.llm_localize/projects.yaml` for multi-project web UI.
3. Run `llm-localize validate` in CI before merge.
4. Queue long translation jobs via generated taskqueue blueprints, not
   background shells.

## Docs entry points

- Consumer setup: `llm_localize/docs/getting-started.md`
- CLI reference: `llm_localize/docs/cli.md`
- Web UI: `llm_localize/docs/web.md`
- Engine constraints: `llm_localize/AGENTS.md`

## taskqueue UI catalogues

Catalogues live at `taskqueue/static/locales/{locale}.json` (flat JSON). Source locale is `en`. Targets in `.llm-localize.toml` include **pl**, **zh**, and **ar**. Keep `en` complete; never invent keys outside the scan of `taskqueue/static`. Arabic UI sets `dir=rtl` via `i18n.js`.
