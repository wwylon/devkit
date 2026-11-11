# Card-bot family programmes (portable)

Import from family bot `CLAUDE.md` only (meldbot, climbbot, fishbot, shedbot,
addbot, bankbot, patiencebot, tilebot, durakbot, and optionally linked from
omnigames/pokerbot). **Do not** import from parent `<portfolio-root>\CLAUDE.md`.

Scaffold checklist: [card-bot-family.md](../conventions/card-bot-family.md).  
Survey template: [card-bot-survey.md](../conventions/card-bot-survey.md).

## Route title → repo

| If… | Repo |
| :-- | :-- |
| Must-follow trick (+ optional auction); multi-game | **omnigames** (+ omnicard3 DDS) |
| Bridge product / deep Bridge AI | **bridge** / **bridge2** (+ dds_alpha, pimc) |
| Betting / poker | **pokerbot** |
| Meld / rummy | **meldbot** |
| Combo climbing | **climbbot** |
| Fishing / ask-capture | **fishbot** |
| Simple single-card shed | **shedbot** |
| Pegging / cribbage-like | **addbot** |
| Banking (Blackjack / Baccarat) | **bankbot** (not pokerbot) |
| Solitaire / patience | **patiencebot** |
| Tile melds (Mahjong) | **tilebot** (not meldbot) |
| Attack / defend (Durak-like) | **durakbot** (not shedbot / omnigames) |
| Polished multi-game website | **omnisite** (**later** — parked) |

Gate: *one card to a must-follow trick under trump/suit law?* → omnigames. Else → matching family.  
President with climb combos → climbbot; plain race shed → shedbot.  
Blackjack ≠ Hold’em (bankbot vs pokerbot). Mahjong tiles ≠ card rummy (tilebot vs meldbot).  
Durak attack/defend ≠ DDS tricks, climb combos, or single-card race shed.

## Layers (every family repo)

| Layer | Owns | Forbidden |
| :-- | :-- | :-- |
| `games/<key>/` | State, `legal_actions`, `apply`, score | Search, NN, solver I/O |
| `bot-engine/` | `human`, weak bots, family LEAF, later `nn` | Rewriting legality |
| `harness/` | Gates; reject illegal engine output | Game rules text |
| `arena/` | Match, seat×phase, local play UI, compare | Owning rules |

## L0–L6

| Stage | Exit |
| :-- | :-- |
| **L0a** Survey | `plan/survey.md` filled (or “none found” + sources searched). No L1 before this. |
| **L0b** Rules stub | Pagat-based rules stub; `GAME_STATUS` row |
| **L1** Rules engine | `legal_actions` / `apply` / score; unit+property |
| **L2** Weak bots + arena | `human`/`random`/`heuristic`; playable local arena (HvH/HvB) |
| **L3** Family LEAF | Named leaf wired; seed gate or metric written |
| **L4** Belief / NN | Optional |
| **L5** Arena ladder | Seed-fixed ledger; **required before strength claims** |
| **L6** Face export | Stable ABI when a product face needs it |

**Simplest game first** in each family. Harder sibling only after game zero ≥ L2 (or owner parks).  
One primary title per family NOW; ≤2–3 active L1+ programmes across the portfolio.

## Web UI

- **Near term:** family `arena/` local research web (omnigames Arena pattern). From L2.
- **omnisite:** **later** multi-backend product face over L6 — do not start until owner unparks.
- Never host non-trick tables in omnigames arena. Never put bot search in omnisite.

## Rules text

- Pagat wins on conflict.
- **Non-trick families:** local `docs/game_rules/<key>.md` (create here).
- **omnigames / omnicard3:** trick rules stay in `omnicard3/docs/game_rules/` (omnigames does not fork them).

## Other hard rules

- Read `plan/NOW.md` first; one task per session; check `inbox/<repo>/`.
- Long jobs → that project’s `experiments/operator_queue/` + tqdaemon project id = repo name.
- Cross-repo: inbox only; no silent edits to another family.
- Engine purity: [engine-purity.md](engine-purity.md) — classify human / heuristic / search / learned / mixture.
