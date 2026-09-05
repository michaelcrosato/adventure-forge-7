# AdventureForge: The Unbounded Action Engine

[![Verify](https://github.com/michaelcrosato/adventure-forge-7/actions/workflows/ci.yml/badge.svg)](https://github.com/michaelcrosato/adventure-forge-7)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"Freedom in design. Honesty in verification. The model never is the world."**

AdventureForge is an action-first, deeply reactive open-world RPG engine built on a pure deterministic state transition kernel (`step(state, action, seed_cursor) -> state'`). It combines the geographical travel breadth of **Skyrim** with the systemic, choice-rich depth of **Baldur's Gate 3**.

---

## Key Pillars & Invariants

1. **Pure Deterministic Authority (R1):** State transitions are 100% pure code: `step(state, action_id, seed_cursor) -> (state', StepResult)`. No wall clock, network, or unseeded randomness. Replays reproduce state hashes bit-for-bit via the authoritative `SplitMix64` PRNG cursor.
2. **7-Axis Character Reactivity (R2):** Characters are represented across 7 orthogonal axes: Ancestry, Background, Attributes, Skills, Traits, Flaws, and Reputation/Faction Markers. Counterfactual witness pairs (e.g., Silas vs. Vivienne) yield demonstrably distinct legal actions and narrative responses.
3. **High-Velocity Hemingway Prose (R3):** Exactly 1–3 short sentences per observation, active voice, FKGL clamped between Grade 6.0 and Grade 8.0, maximum 18 words per sentence, strict 1–3 word UI action labels, and zero purple prose clichés.
4. **Unbounded Scene Possibility Space (R4):** Dynamic affordance synthesis supporting 2 to 200+ legal actions without artificial ceilings (`Choices = Base ∪ Inventory ∪ Traits ∪ Systemics`).
5. **Continuous 520-Scene World Graph (R5):** 520 interconnected scenes spanning 5 provinces and interlocking hubs with 100% BFS reachability and 100% interactable density (>=3 interactables per scene).
6. **Information Firewall (R6 / I6):** External clients and agent playtesters interact solely through the sanitized player observation contract (`MCPServer` or CLI), never inspecting internal engine objects or raw condition/effect DSL payloads.
7. **Autonomous Multi-Agent Flywheel:** Unattended self-healing and expansion loop using multi-persona blind playtester fleets (Explorer, Brute, Infiltrator, Speedrunner, Saboteur, Nomad, Diver, Scout) with automated defect triage.

---

## 5 Shipped Provinces & Regional Mechanics

| Province | Primary Mechanic | Environmental Systemics & Hazards |
|---|---|---|
| **The Reach** | Verticality & Climbing Stamina | Mountain blizzards, high wind bluffs, rope ascents, altitude hazards |
| **The Sunken Hollows** | Underwater Diving & Hydrostatic Pressure | Bioluminescence, water submersion, conductive shock, abyssal ruins |
| **The Scorchwaste** | Heat Survival & Hydration Management | Desert heatwaves, sunstroke, sandstorms, water oasis cisterns |
| **The High Court** | Court Intrigue & Noble Decorum | Sentried curfews, diplomatic dossiers, tribunal rhetoric, legal decrees |
| **The Lowlands** | Social Stealth & Bounty Infiltration | Sewer miasma, thief signets, customs broker ciphers, watch permits |

---

## 7 Character Archetypes

- **Silas the Cutpurse** (Plainsman / Street Drifter): Stealth, lockpicking, thief signets, agile evasion.
- **Lady Vivienne** (High-Kin / Noble Exile): High-court rhetoric, legal dossiers, aristocratic influence.
- **Garron** (Ashenborn / Pit Fighter): Brute strength, athletics, crowbar leverage, raw endurance.
- **Kael** (Nomad / Dune Strider): Desert survival, heat tolerance, sandstorm navigation, bartering.
- **Mara** (Deep-Dweller / Abyssal Diver): Underwater breathing, keen night vision, submerged ruins salvage.
- **Torin** (Reachman / Mountain Scout): Cliff scaling, rope climbing, highland lookout navigation.
- **Garron (Pit Fighter)**: Canonical combat-ready warrior alias.

---

## Verification & Testing

Before committing, all 7 gates of the mechanical verification bar must pass cleanly:

```bash
# 1. Run the 7-Gate Mechanical Verification Bar
./verify
# or:
python3 -m adventure_forge.verify

# 2. Run the Full Pytest Suite (330+ tests)
pytest -v

# 3. Static Type Checking and Linting
ruff check .
mypy adventure_forge
```

### The 7 Mechanical Verification Gates
1. **Determinism & Replay Fingerprinting:** Bit-for-bit SHA-256 state replay fidelity.
2. **World Graph Link Integrity:** 100% resolution of all scene targets, entity destinations, and transition effects.
3. **Hemingway Prose Linter:** Grade 6–8 FKGL, <=18 words/sentence, <=3 words/label, zero purple lexicon.
4. **Counterfactual Character Divergence:** Silas vs. Vivienne witness proofs across shared scenes.
5. **Unbounded Choice Scaling:** 100+ actions in `bazaar_center` without degradation.
6. **Non-LLM BFS Reachability Crawler:** 100% reachability across all 520 scenes.
7. **Macro-World Interactable Density:** 100% of scenes (520/520) offer >= 3 interactables.

---

## Interactive Play & Autonomous Flywheel

```bash
# Interactive CLI Player (Action-First, Paginated UI)
python3 -m adventure_forge.player.cli [preset]

# Multi-Persona Autonomous Flywheel Loop (10 cycles)
./loop.sh
# or:
python3 -m adventure_forge.flywheel.loop run --cycles 10
```

---

## Deployment & Stateless Serverless Architecture

AdventureForge deploys seamlessly to Vercel with zero configuration:
- **`GET /`**: Full interactive playable web application with Hemingway UI, preset selection, and live action execution.
- **`GET /health` & `HEAD /health`**: Machine-readable JSON health monitor (`service`, `status`, `version`).
- **`POST /api/game/new`**: Stateless session initialization with preset character and deterministic seed.
- **`POST /api/game/step`**: Stateless transition step returning sanitized observations and updated state.
- **`GET /api/game/presets`**: Archetype catalogue and starting scene metadata.
- **`GET /api/game/quests`**: Continental campaign and 5 provincial subquest DAGs.
- **`GET /api/game/hazards`**: Deterministic hazard combo definitions and status reactions.
- **`POST /api/mcp` & `/mcp`**: JSON-RPC 2.0 Model Context Protocol endpoint for AI coding agents.

### Local Development Preview
```bash
npx vercel dev
```

### Git Automatic Push
The repository includes an active post-commit hook in `.githooks/post-commit` configured via `core.hooksPath`. Whenever any commit is made, it is automatically pushed to `origin/main`.

