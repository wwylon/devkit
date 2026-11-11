# Public repository discoverability (agent recipe)

On-demand house recipe for making OSS mirrors findable and credible.
Read when preparing a public front door, running `/publish`, or promoting a
wwylon product. **Do not** import from parent `CLAUDE.md` (not every session).

Companion to [publish.md](publish.md) (export / verify / gated push). Copyable
stubs: [conventions/public-front-door/](../conventions/public-front-door/).

## Paste briefs (human → agent)

**Mode 1 — first front-door** (new or thin public repo):

```text
Prepare the public front door for <project> at <portfolio-root>\<path>.
Follow <portfolio-root>\devkit\rules\public-discoverability.md (Mode 1) and
<portfolio-root>\devkit\rules\publish.md. Copy stubs from
devkit/conventions/public-front-door/. Use /publish for gated push.
Do not push with --i-mean-it until I explicitly OK. One product only.
```

**Mode 2 — repeat release** (front door already live):

```text
Public release for <project>: Mode 2 in
<portfolio-root>\devkit\rules\public-discoverability.md + publish.md / /publish.
Dry-run via operator queue if verify >~2 min. Ask before --i-mean-it.
```

Pick **one mode**. Do not bulk-apply this recipe to every portfolio repo in one
session unless the user asks — use inbox or a dedicated session.

## Why this matters

Google and GitHub search reward **age, stars, topics, and an owned docs URL**
more than “better code.” Bare generic names are crowded—optimize for
**distinctive queries** and a credible front door, not overnight #1 for the
bare token.

## Portfolio (light)

| Project | Status |
|---------|--------|
| taskqueue | public — **pilot** for this recipe (worked example) |
| upscale | public — next consumer of Mode 1 gaps |
| devkit | public |
| llm_localize | planned public |
| sky | planned public |

**Worked example (cite, do not duplicate trees):** private taskqueue —
`site/`, `docs/assets/`, `llms.txt`, `AGENTS.public.md`,
`publish.manifest.yaml` allow list, `.github/workflows/pages.yml`.

## Modes

| Mode | When | What to run |
|------|------|-------------|
| **1 First front-door** | Missing `site/`, visuals, slim README, or Pages Actions | Gap-check → phases **A→F** once |
| **2 Repeat release** | Front door already live; shipping a version | SemVer/CHANGELOG → clean tree → dry-run → user OK → `--i-mean-it`; re-run **E/F** only if `site/` or GitHub metadata changed |

## Gap-check (existing public repos)

Before Mode 1 work, tick against the **private** tree and public GitHub. Then
implement only missing items (do not reinvent a working publish pipeline).

| Check | OK? |
|-------|-----|
| `publish.manifest.yaml` exists; `doctor` green | |
| `site/` + `.github/workflows/pages.yml` present and **allowlisted** | |
| `docs/assets/hero.*` + `social.*` present | |
| README slim (pitch / install / first win) vs CLI dump | |
| Public homepage = `https://<owner>.github.io/<repo>/` | |
| Pages `build_type=workflow` (not branch folder `/site`) | |
| Description + topics set via `gh repo edit` | |
| Social preview still a **human** Settings reminder | |

## File inventory (Mode 1)

### Required

- Slim stranger-facing `README.md` — pitch, install, first win; deep refs in `docs/`
- `docs/assets/hero.jpg` (~1600×900) + `docs/assets/social.jpg` (1280×640); optional `icon.png` (512×512)
- Top-level `site/` — `index.html`, `robots.txt`, `sitemap.xml`, visuals (or copies), maintainer `README.md`
- `.github/workflows/pages.yml` — Actions deploy of `site/` (GitHub branch Source only allows `/` or `/docs`, **not** `/site`)
- `publish.manifest.yaml` allow entries for `site/`, asset roots, `.github/`, and any new top-level files (see [ALLOWLIST.md](../conventions/public-front-door/ALLOWLIST.md))
- Overlays when agents are an audience: `AGENTS.public.md` → `AGENTS.md`, `CLAUDE.public.md` → `CLAUDE.md`
- LICENSE + stranger-facing CHANGELOG notes + SemVer

### When applicable

- `README.<lang>.md` siblings only if the product already localizes (English canonical; update siblings in the same change or delete them)
- `llms.txt` when agents are an audience
- English `docs/help/*` + `scripts/build_docs.py` / `check_docs` — do **not** update pl/zh/ar help locale bodies for content changes
- Privacy / no phone-home blurb in security docs or README
- `pyproject.toml` description, keywords, Project URLs; one-line disambiguation if the name collides
- GSC file `site/google….html` only when the human drops the Search Console download

## Phases (Mode 1)

| Phase | Agent | Human |
|-------|--------|--------|
| **A Preconditions** | Manifest (or `init-manifest` then stop); overlays; `doctor`; remotes; SemVer/CHANGELOG | Fill allow/deny/verify if new manifest |
| **B Front door** | Inventory above; customize copy from product facts only | Supply or approve hero/social images if missing |
| **C site/ + allowlist** | Copy [public-front-door](../conventions/public-front-door/); customize pitch; wire allow list + `pages.yml` | — |
| **D Publish** | Private local fast gate (no GitHub CI); **clean working tree** (export copies the filesystem); queue `release --dry-run` if verify >~2 min; fix failures in **private**; report | Explicit OK before `--i-mean-it` |
| **E Post-push** | `gh repo edit` description/topics; enable Pages `build_type=workflow`; `--homepage https://<owner>.github.io/<repo>/`; trigger `pages` workflow; confirm URL HTTP 200; remind Social preview | Settings → Social preview ← `docs/assets/social.*` |
| **F Search Console** | After human drops `google….html`: place under `site/`, publish, confirm Pages 200 | Add URL-prefix property; Verify; submit **full** sitemap URL; URL Inspection on `/` |

Mode 2 skips B/C unless those files change; still enforces clean tree and ask-before-push.

### Pages (phase E) — required commands

```text
# Enable Actions-based Pages (branch Source cannot use /site)
gh api repos/<owner>/<repo>/pages -X POST -f build_type=workflow

gh repo edit <owner>/<repo> --homepage "https://<owner>.github.io/<repo>/"
gh workflow run pages.yml -R <owner>/<repo>
```

Confirm `https://<owner>.github.io/<repo>/` returns 200 before calling the front door “live.”

### Search Console (phase F)

1. Human: Search Console → **Add property** → **URL prefix** → `https://<owner>.github.io/<repo>/`
2. Human: download the HTML verification file
3. Agent: copy to `site/google….html`, allowlist already covers `site/`, publish (or gated put under `site/` only if verify is blocked — prefer private + publish)
4. Human: **Verify**; **Sitemaps** → submit `https://<owner>.github.io/<repo>/sitemap.xml` (full URL)
5. Human: URL Inspection on `/` → Request indexing

If GSC says **Couldn't fetch** on first try but `curl`/browser get HTTP 200 on the sitemap, wait and **Resubmit** — common on new `github.io` properties.

## Lessons hardened (taskqueue pilot)

| Failure | Rule |
|---------|------|
| Branch Pages Source `/site` → HTTP 422 | Actions workflow only for `site/` |
| Export includes uncommitted WIP → ruff/pytest fail | Clean tree / stash before dry-run |
| Long verify in-session | Operator-queue YAML + `tq wait` |
| Hand-edit `<portfolio-root>\public\<project>` features | Forbidden; fix private + re-export |
| Stamp skip after new private commits | New dry-run or `--force-verify` when SHA/export_id change |
| Social preview via `gh` | Unreliable — maintainer UI; agent reminds only |
| Operator `docs/` as Pages | Never — marketing is top-level `site/` |

## Anti-patterns

- Pages branch Source folder `/site`
- GitHub homepage pointed at raw operator `docs/`
- Silent telemetry / phone-home in daemon, CLI, or local UI
- Exporting `plan/`, tokens, `.mcp.json`, dogfood `experiments/` for other products
- Hand-editing public mirror product code
- Shrinking public verify pytest markers to save time
- `--i-mean-it` without explicit user OK in this session
- Bulk front-door work across the portfolio in one session

## Visual assets

| Asset | Size | Use |
|-------|------|-----|
| `social` | 1280×640 | Repo Settings → Social preview; link cards |
| `hero` | ~1600×900 (16:9) | README + `site/` landing |
| `icon` (optional) | 512×512 | Favicon / mark |

Style: one clear metaphor; dark-friendly; no purple-on-white gradient cliché, no cream+terracotta poster, no neon soup, no emoji collage.

### Prompt skeleton (Gemini / ChatGPT)

Ask for PNG/JPG, no watermark. Fill in PRODUCT and METAPHOR:

> Wide 1280x640 (or 16:9 hero) banner for open-source PRODUCT. Flat modern illustration. METAPHOR. Deep slate background, limited accent palette, high contrast, readable wordmark. No purple gradients, no neon bloom, no stock datacenter photo, no other-product logos, no watermark.

## Transparent analytics

- **Public:** GitHub stars/forks badges; PyPI download badges after a real distinct package name.
- **Maintainer-only:** GitHub Traffic (views/clones ≈ 14 days). Clones ≠ installs.
- **Forbidden:** silent telemetry / phone-home.

PyPI: if the bare package name is taken, publish under a distinct name (e.g. `tq-taskqueue`); keep console script names as designed.

## Inbox handoff snippet (do not auto-send)

When the user asks to notify another project that this recipe is ready, send **one**
P1 `type: info` per [cross-project-messages.md](cross-project-messages.md). Example body for upscale:

```text
---
from: <your-project>
to: upscale
type: info
priority: P1
summary: Public front-door recipe ready (Mode 1/2) for wwylon products
thread: <this-filename>
re: none
blocks: none
---
## R1 - house publish front-door recipe

Follow <portfolio-root>\devkit\rules\public-discoverability.md (Mode 1 gap-check)
and <portfolio-root>\devkit\rules\publish.md. Copy stubs from
devkit/conventions/public-front-door/. Worked example: taskqueue site/ +
docs/assets/ + pages.yml. Do not invent branch Pages Source /site.
```

## Related

- [publish.md](publish.md) — export / verify / gated push
- Skill `/publish` — agent workflow for release CLI
- [conventions/public-front-door/](../conventions/public-front-door/) — copyable `site/` + Pages workflow
- [cross-project-messages.md](cross-project-messages.md) — inbox protocol
- [queue.md](queue.md) — long dry-run / verify via operator queue
