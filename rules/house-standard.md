# Antigravity house standard (charter)

Thin charter for projects under `<portfolio-root>`; detail is in the linked rules. Do not fork per product.

- **Roles:** orchestrator (human) sets priority, idea drops, which directory runs, cold index when idle; agents do all coding, one department directory and one ticket per session.
- **Plan tiers:** Slim (default) = [plan-structure.md](plan-structure.md) (`plan/NOW.md` + `plan/tasks.md`); Rich (bridge2 + domain clones) = `plan/ops/NOW-*`, queues, idea registers, do not migrate to slim; Face (bridge) = `plan/INDEX.md`.
- **Session:** (0) check mailbox ([cross-project-messages.md](cross-project-messages.md); other projects' requests outrank local work); (1) user dropped external ideas -> [external-intake.md](external-intake.md) first; (2) read NOW -> one ticket; (3) discover code L0->L1->L2 ([mcp-indexers.md](mcp-indexers.md)); (4) close ticket and idea disposition; (5) cross-repo change -> `devkit/tools/product_chains.yaml` + [cross-repo-contracts.md](cross-repo-contracts.md).
- **Shared:** devkit rules, conventions, portfolio tools, ignore bases, idea stages. **Local:** build/test, domain invariants, project-specific CPE/multi-clone, Face modules.
- Durable plan copy: `devkit/docs/HOUSE_STANDARD_PLAN.md` (when present).
