# Convention — new card-bot family repo

Portable process: [card-bot-programme.md](../rules/card-bot-programme.md).  
Survey template: [card-bot-survey.md](card-bot-survey.md).

## Checklist

1. Create `<portfolio-root>\<repo>/` (e.g. meldbot).
2. Add `CLAUDE.md` with `@` imports:
   - `plan-structure.md`, `data-and-results.md`, `queue.md`, `engine-purity.md`, `card-bot-programme.md`
3. Add `AGENTS.md`, `README.md`, `.gitignore`, `docs/agent_read_path.md`.
4. Plan hub: `NOW.md`, `tasks.md`, `problems.md`, `problems_open.md`, `problems_fixed.md`,
   `optimization_log.md`, `GAME_STATUS.md`, `survey.md`, `development_journal.md`.
5. Stub dirs: `games/<key>/`, `bot-engine/`, `harness/`, `arena/`, `docs/game_rules/`,
   `experiments/operator_queue/`.
6. `arena/README.md`: L2 play/verify target; no UI until L1 green.
7. `inbox/<repo>/_README.md` under `<portfolio-root>\inbox\`.
8. `git init -b main` + initial commit (remote only if owner asks).
9. Update [devkit README](../README.md) consumer table in the same change set as first CLAUDE import.
10. First NOW task = **L0a survey** for game zero (simplest title). Do not start L1 until survey AC met.
11. Taskqueue project: register when first long job appears (not at empty scaffold).
12. Language default: C++; build system deferred to L1.

## Game zero examples

| Repo | Key | Later |
| :-- | :-- | :-- |
| meldbot | gin | Rummy 500, Canasta |
| climbbot | big_two | Dou Dizhu, Tien Len |
| fishbot | go_fish | Scopa, Casino |
| shedbot | crazy_eights | Uno-like; non-combo President |
| addbot | cribbage | other pegging / 15-family if any |
| bankbot | blackjack | Baccarat (near zero decisions) |
| patiencebot | freecell | Klondike, Spider, … |
| tilebot | mahjong | regional variants after basic |
| durakbot | durak | Podkidnoy, Perevodnoy, … |
