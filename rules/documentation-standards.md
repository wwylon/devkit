# Documentation standards (portable)

Portable Definition-of-Done for tools and docs; project-specific paths stay in each repo's local rules.

## Rules

- **`--help` required** for any script run more than once: usage, arguments, output format, one example.
- **Docs are part of DoD:** a change is not complete until README and relevant `doc(s)/` pages reflect install/run/args/outputs.
- **Log behavior changes** (parameters, behavior, config switches) in the project's design notes or optimization log in the same session.
- **Solver or oracle write-ups** use [algorithm-doc.md](../conventions/algorithm-doc.md) when the project ships one (read, do not import).
