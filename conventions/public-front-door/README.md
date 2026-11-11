# public-front-door — copy into a product

House stubs for a wwylon OSS marketing face. **Not** imported by parent
`CLAUDE.md`. Recipe: `devkit/rules/public-discoverability.md`.

## Copy

From the **private** project root:

1. Copy `pages.yml` → `.github/workflows/pages.yml`
2. Copy `site/` → top-level `site/` (replace `OWNER`, `REPO`, `PRODUCT`, pitch)
3. Add allow entries from `ALLOWLIST.md` to `publish.manifest.yaml`
4. Add `docs/assets/{hero,social}` (and optional `icon`); copy into `site/` if the landing page references relative URLs
5. Dry-run / push via `devkit/rules/publish.md` — then phases E–F in the recipe

Do **not** set GitHub Pages branch Source to folder `/site` (API returns 422).
Use Actions (`build_type=workflow`) as documented in `site/README.md`.
