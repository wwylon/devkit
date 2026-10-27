# Changes to devkit

Read this before adding or editing anything in this repo. Do not import it from a project `CLAUDE.md`.

- Re-read the consumer table in [README.md](../README.md). Grep who imports the file you are changing, including `<portfolio-root>\CLAUDE.md`. Do not trust memory or the quick-reference in `AGENTS.md`.
- The text must still be true for every consumer that will load that file. If it is only true for one project, leave it in that project.
- Recheck the diff: a few lines; no domain words in a file the parent or many projects import; no new `CLAUDE.md` import unless every session that loads it needs the text.
- If a project started or stopped importing a rule, update the consumer table in the same change.
