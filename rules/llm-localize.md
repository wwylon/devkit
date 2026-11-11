# llm_localize — cross-project agent rules

Applies when working in any repo that registers a `.llm-localize.toml`
(bridge, llm_localize dogfood, taskqueue, etc.).

## What it is

The **llm_localize** package translates, validates, and scans message catalogues
with a local LLM (Ollama). Consumer repos own all catalogue data; the package
supplies machinery only.

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
| `llm-localize validate` | local gates, no LLM |
| `llm-localize status` | coverage check |
| `llm-localize guide --json` | what to do next (agents) |
| `llm-localize web` | browse, inline edit, Ops drawer |
| `llm-localize translate` / `improve` | batch fill or quality passes |
| `llm-localize agent-hardcoded` | hardcoded UI string report for agents |
| taskqueue YAML under `experiments/operator_queue/` | long sweeps |

CLI and web share `llm_localize/ops/` (ADR-14). Web binds `127.0.0.1` only.

## Hardcoded UI strings (dual loop)

Run from **this** project’s checkout (consumer agent owns wiring source;
llm_localize never rewrites consumer files). Prefer `agent-hardcoded` over
bare `scan` for agent paste reports.

1. `llm-localize agent-hardcoded --split auto --out-dir reports/hardcoded --refresh`
2. Wire hits to `t()` / `uiT` / `data-i18n` in **this** repo; `scan-decide` /
   `apply` for accepted EN keys only.
3. Visual leftover hunt when the review UI supports it: opt-in
   `[web] qa_locales = ["en-XX"]`, `pseudo --locale en-XX`, browse/crawl,
   then re-pseudo after EN growth. Production keeps `qa_locales` empty.
4. Scanner gaps (missed sinks) → message `inbox/llm_localize/` — do not bump
   `_SCAN_VERSION` from a consumer without filing there.

Full runbook: `llm_localize/docs/scanners.md` § Operator / agent workflow.
Short paste: `llm_localize/docs/agents.md` § UI QA.

## In consumer repos

1. Config lives at `.llm-localize.toml` in the project root.
2. Register in `~/.llm_localize/projects.yaml` for multi-project web UI.
3. Run `llm-localize validate` locally before merge (no GitHub CI).
4. Queue long translation jobs via generated taskqueue blueprints, not
   background shells.

## Docs entry points

- Consumer setup: `llm_localize/docs/getting-started.md`
- CLI reference: `llm_localize/docs/cli.md`
- Web UI: `llm_localize/docs/web.md`
- Hardcoded hunt: `llm_localize/docs/scanners.md` § Operator / agent workflow
- Engine constraints: `llm_localize/AGENTS.md`

## taskqueue UI catalogues

Catalogues live at `taskqueue/static/locales/{locale}.json` (flat JSON). Source locale is `en`. Targets in `.llm-localize.toml` include **pl**, **zh**, and **ar**. Keep `en` complete; never invent keys outside the scan of `taskqueue/static`. Arabic UI sets `dir=rtl` via `i18n.js`.
