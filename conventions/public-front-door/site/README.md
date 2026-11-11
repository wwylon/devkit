# Public marketing site (`site/`)

Static landing for GitHub Pages. **Not** the operator/help tree under `docs/`.

Replace `OWNER` / `REPO` below with the public GitHub coordinates.

## Enable Pages (maintainer)

GitHub’s branch Source only allows `/` or `/docs` — not `/site`. Deploy via
`.github/workflows/pages.yml` (Actions).

1. Push `site/` + the workflow to public `main` (house publish).
2. Repo **Settings → Pages**: Source = **GitHub Actions** (or
   `gh api repos/OWNER/REPO/pages -X POST -f build_type=workflow`).
3. Confirm https://OWNER.github.io/REPO/
4. `gh repo edit OWNER/REPO --homepage https://OWNER.github.io/REPO/`
5. **Settings → Social preview**: upload `../docs/assets/social.jpg` (or `social.jpg` here).
6. [Google Search Console](https://search.google.com/search-console): URL-prefix
   `https://OWNER.github.io/REPO/`, verify (`google….html` in this folder),
   submit `https://OWNER.github.io/REPO/sitemap.xml`, URL Inspection on `/`.
