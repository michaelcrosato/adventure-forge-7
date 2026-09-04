# Project: AdventureForge

## Architecture
AdventureForge is an action-first, deeply reactive open-world RPG engine with Skyrim geographical breadth and Baldur's Gate 3 systemic depth, built on a deterministic rule kernel and an autonomous multi-agent development repository.

### Module Boundaries & Data Flow
- **`adventure_forge/core/`**:
  - `state.py`: Pure, immutable-style `GameState`, `CharacterSheet` (7 orthogonal axes), inventory, world flags, SplitMix64 PRNG cursor, canonical SHA-256 state fingerprinting.
  - `engine.py`: Authoritative pure deterministic transition `step(state, action_id, seed_cursor) -> StepResult`.
  - `actions.py`: Dynamic affordance synthesis combining Base Actions, Inventory Affordances, Trait Exploits, and Regional Systemics.
  - `conditions.py` & `effects.py`: Declarative condition evaluation and state mutation DSL.
- **`adventure_forge/content/`**:
  - `models.py`: Scene, Region, Entity, and Action definitions.
  - `loader.py`: World registry builder linking 520 nodes across 5 provinces and POIs.
  - `data/provinces/`: `reach.py`, `lowlands.py`, `scorchwaste.py`, `high_court.py`, `sunken_hollows.py`.
  - `data/mechanics/`: Regional systemic handlers (Verticality, Social Stealth, Heat Survival, Court Intrigue, Underwater Diving).
- **`adventure_forge/linter/`**:
  - `prose_linter.py`: Hemingway baseline linter enforcing sentence length (<=18 words), readability (Grade 6–8 FKGL), UI action labels (1–3 words), and forbidding purple prose.
- **`adventure_forge/verification/`**:
  - `verify.py`: 6-gate mechanical non-LLM verification bar.
  - `crawler.py`: Non-LLM BFS reachability and solvability crawler.
  - `counterfactual.py`: Counterfactual character witness pair validator (Silas vs Vivienne).
- **`adventure_forge/player/`**:
  - `cli.py`: Interactive CLI with paginated action display without truncation.
  - `mcp_server.py`: Agent player surface adhering to the I6 Information Firewall.
- **`adventure_forge/flywheel/`**:
  - `loop.py`, `playtester.py`: Multi-persona blind playtester fleet (Explorer, Brute, Infiltrator, Speedrunner, Saboteur).
  - `triage.py`: Automated defect reproduction and verification triage.

## Feature Inventory
Every feature from the Survey phase appears here with its assigned milestone.
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Pure Deterministic Transition | `step(state, action, seed_cursor) -> state'`, SplitMix64 PRNG, SHA-256 fingerprinting | M4 | R1, ORIGINAL_REQUEST |
| 2 | Replay Determinism Verification | Action trace replays yield identical state hashes across seeds | M4 | R1, AC Determinism #1 |
| 3 | 7-Axis Character Representation | Ancestry, background, attributes, skills, traits, flaws, reputation/markers | M4 | R2, ORIGINAL_REQUEST |
| 4 | Counterfactual Character Witness Pair | Same opening scene with two opposite builds yields distinct legal actions/dialogue | M4 | R2, AC Determinism #2 |
| 5 | Declarative Condition & Effect DSL | Pure functional evaluation of state conditions and clamped state mutations | M4 | R2, INITIAL_PLAN |
| 6 | Hemingway Sentence Length Enforcement | Max 18 words/sentence, 1–3 short active-voice sentences per node | M1 | R3, ORIGINAL_REQUEST |
| 7 | Readability Metric & FKGL Enforcement | Grade 6–8 Flesch-Kincaid Grade Level strictly checked and enforced | M1 | R3, AC Quality #1 |
| 8 | UI Action Label Length Enforcement | Strict 1–3 word UI action labels enforced by linter and content | M1 | R3, ORIGINAL_REQUEST |
| 9 | Purple Prose Banned Lexicon | Zero ornamental filler; 14 banned purple prose clichés rejected | M1 | R3, INITIAL_PLAN |
| 10 | Content Remediation (Prose & Labels) | Fix all scene descriptions exceeding Grade 8 and 10 labels exceeding 3 words | M1 | R3, Survey Findings |
| 11 | Type Safety & Clean Annotations | Fix missing imports (`Any` in crawler.py, `Tuple` in cli.py) | M1 | R1/R6, Survey Findings |
| 12 | Generator Synchronization | Fix `tools/generate_provinces.py` drift so node 520 is preserved | M1 | R5/AC Scale, Survey Findings |
| 13 | Unbounded Scene Choice Synthesis | Dynamic affordance equation ($\text{Base} \cup \text{Items} \cup \text{Traits} \cup \text{Systemics}$) | M4 | R4, ORIGINAL_REQUEST |
| 14 | Choice Scaling Stress Test | Scene with 100+ legal actions without crash or truncation (bazaar_center: 115) | M4 | R4, AC Determinism #3 |
| 15 | Paginated Player UI | Clean categorization, grouping, and pagination without truncation | M3 | R4, ORIGINAL_REQUEST |
| 16 | Agent MCP Player Surface | `player/mcp_server.py` implementing blind playtester tool contract under firewall | M3 | R4/R6, INITIAL_PLAN |
| 17 | Macro-World Graph Scale | 520 interconnected nodes across 5 provinces and hubs with 100% reachability | M4 | R5, AC Scale #2 |
| 18 | Non-LLM Reachability Crawler | BFS graph solver proving reachability and no softlocks | M4 | R5, AC Quality #2 |
| 19 | 5 Unique Regional Mechanics | Verticality, Social Stealth, Heat Survival, Court Intrigue, Underwater Diving | M4 | R5, AC Quality #3 |
| 20 | Macro-World Interactable Density Enrichment | Enrich >= 255 nodes so that >= 50% (260+) offer 3+ meaningful interactables | M2 | R5, ORIGINAL_REQUEST |
| 21 | Canonical Verification Command | Executable `./verify` script and `python -m adventure_forge.verify` module | M3 | R6, ORIGINAL_REQUEST |
| 22 | Flywheel Defect Triage Harness | Wire `flywheel/triage.py` to playtester reports and test defect triage | M3 | R6, ORIGINAL_REQUEST |
| 23 | Comprehensive 4-Tier Test Suite | Unit (Tier 1), Boundary (Tier 2), Integration (Tier 3), Scenario (Tier 4) | M4 | R6, ORIGINAL_REQUEST |
| 24 | Tier 5 Adversarial Coverage Hardening | White-box stress-testing, softlock hunting, and gap closure | M5 | R6, Dual Track |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Quality, Prose Linter & Type Safety Remediation | Fix type imports in `crawler.py` and `cli.py`; wire `flesch_kincaid_grade` (6-8) into linter; set max action label words to 3; remediate violating content and fix generator drift | None | COMPLETE |
| M2 | World Graph Interactable Density Enrichment | Augment >= 255 province nodes with a 3rd meaningful interactable or systemic entity to meet >= 50% (260+) threshold; maintain 100% reachability and Hemingway constraints | M1 | COMPLETE |
| M3 | Canonical Verification Command, MCP Surface & Triage | Implement `./verify`, `adventure_forge.verify`, `player/mcp_server.py`, and wire/test `flywheel/triage.py` | M1 | COMPLETE |
| M4 | 4-Tier Test Suite Expansion & E2E Gate Clearance | Comprehensive test suite covering Tiers 1–4 across all 23 modules, validating all acceptance criteria | M2, M3 | COMPLETE |
| M5 | Adversarial Coverage Hardening (Tier 5) | Adversarial challenger analysis, gap detection, and test coverage hardening | M4 | COMPLETE |

## Interface Contracts
### `adventure_forge.linter.prose_linter` ↔ `adventure_forge.content`
- `ProseLinter.lint_text(text: str) -> List[str]`: Enforces sentence count (1–3), word count (<=18), Grade 6–8 FKGL, zero purple words.
- `ProseLinter.lint_scene(scene: Scene) -> List[str]`: Enforces scene descriptions, entity descriptions, and action labels (<=3 words).
- `ProseLinter.lint_registry(registry: Dict[str, Region]) -> Dict[str, List[str]]`: Scans entire world graph.

### `adventure_forge.content.loader` ↔ `adventure_forge.core.engine`
- `build_world_registry() -> Dict[str, Region]`: Returns 520 immutable scenes across 11 regions.
- Density invariant: `sum(1 for s in scenes if len([a for a in s.base_actions if a.category != 'movement']) + len(s.entities) >= 3) >= 260`.

### `adventure_forge.verification.verify` ↔ Canonical Entry Points
- `./verify` (shell executable) and `python3 -m adventure_forge.verify`:
  - Runs all 6 mechanical verification gates.
  - Returns exit code 0 if and only if all gates pass.

### `adventure_forge.player.mcp_server` ↔ Playtester / Agent Fleet
- Functions: `new_game(preset: str) -> Dict`, `step_game(action_id: str) -> Dict`, `get_state() -> Dict`.
- Enforces information firewall: Returns only player-visible `StepResult` fields (scene id, prose, legal actions, status), never internal source code or raw engine objects.

## Code Layout
- `adventure_forge/core/`: Deterministic kernel, state, dynamic actions, condition/effect DSL.
- `adventure_forge/content/`: World models, loader, provinces, regional mechanics.
- `adventure_forge/linter/`: Hemingway prose and action label linter.
- `adventure_forge/verification/`: Verification gates, BFS crawler, counterfactual divergence.
- `adventure_forge/player/`: CLI and MCP server player surfaces.
- `adventure_forge/flywheel/`: Multi-persona blind playtester loop, defect triage.
- `adventure_forge/verify.py`: Top-level module entrypoint forwarding to verification bar.
- `verify`: Root executable wrapper script.
- `tests/`: 4-tier automated test suite.
