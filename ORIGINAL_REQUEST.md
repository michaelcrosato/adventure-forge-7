# Original User Request

## 2026-09-03T21:20:49Z

AdventureForge is an action-first, deeply reactive open-world RPG engine with Skyrim geographical breadth and Baldur's Gate 3 systemic depth, built on a deterministic rule kernel and an autonomous multi-agent development repository.

Working directory: /home/micha/dev/adventure-forge-7
Integrity mode: development

## Requirements

### R1. Pure Deterministic Game Kernel
The authoritative game transition must be pure deterministic code: `step(state, action, seed_cursor) -> state'`. No wall-clock time, network, or unseeded RNG inside the transition. Identical content, seed, character sheet, and canonical action sequence must produce identical state hashes and replay fingerprints. The LLM is never the physics engine.

### R2. Deep Character Customization & World Reactivity
Player characters must have at least 6 orthogonal axes (ancestry, background, traits, flaws, skills, reputation/markers). Content and scenes must dynamically query this state vector. Inhabitants and environment must react persistently and coherently to character capabilities and deeds across the single contiguous world.

### R3. High-Velocity Action Prose & Bounded Budget
Player-facing language must adhere to the Hemingway baseline: 1-3 short, active-voice sentences per node, max 18 words per sentence, grade 6-8 readability, zero ornamental filler, plain dialogue, 1-3 word UI action labels. Observations must lead with situation and legal actions; observation budget is strictly bounded.

### R4. Unbounded Scene Possibility Space
Choices are dynamically synthesized at runtime from base actions, inventory affordances, character traits, and environmental systemics. The engine imposes no artificial ceiling on legal actions (supporting 2 to 200+ actions), while the presentation interface provides clean categorization, grouping, and pagination without truncation.

### R5. Macro-World Graph with Unique Regional Mechanics
A single contiguous world graph spanning provinces, hubs, and POIs (each with 10-30 interlocking nodes). Scale targets 500+ distinct locations, with at least 5 region-defining unique mechanics (e.g. verticality/climbing, social stealth/disguise, survival crafting, legal/court intrigue, eldritch resonance) and at least 50% locations offering 3+ meaningful interactables.

### R6. Autonomous Flywheel, Verification Bar & Information Firewall
A non-LLM mechanical verification command (`verify`) checking determinism, reachability crawler proofs, simplicity linter, and counterfactual character witness pairs. Blind playtester fleet interacts solely through the player surface without access to repository source code or hidden state.

## Acceptance Criteria

### Determinism & Proofs
- [x] 100% of recorded action traces replay to identical state hashes across seeds.
- [x] Counterfactual witness pair: same opening scene evaluated with two opposite character builds yields observably distinct legal actions/dialogue.
- [x] Stress scene with 100+ legal actions operates without crash or truncation.

### Quality & Linter Gates
- [x] Plain-language linter rejects content exceeding sentence length or readability limits.
- [x] Graph solver crawls all active POIs to prove reachability and no softlocks.
- [x] At least two distinct regions implemented with unique systemic mechanics.
- [x] 520 interconnected nodes across 5 provinces with 100% reachability.

## 2026-09-04T19:54:56Z

Execute the approved teamwork plan in prompt_draft.md:
1. Audit the repository for performance and architectural bottlenecks (world loader, BFS crawler, SplitMix64 PRNG, ASGI API handlers).
2. Optimize any identified bottlenecks.
3. Design and code new rich multi-stage systemic encounters across all 5 provinces (The Reach, The Lowlands, The Scorchwaste, The High Court, The Sunken Hollows).
4. Run continuous blind playtester fleet (Explorer, Brute, Infiltrator, Speedrunner, Saboteur) and verify zero defects.
5. Ensure 100% pass rate across all 7 verification gates in ./verify, 180+ pytests, ruff, and mypy.
6. Commit and push all enhancements. Keep building and playtesting continuously.

## 2026-09-05T02:41:17Z

Continue to playtest and expand the game content for AdventureForge. Run an endless loop of multi-persona playtesting, triage defects, enrich provincial encounters across all 5 provinces, preserve Hemingway prose and all 7 verification gates, and commit and push all improvements to GitHub.

Working directory: /home/micha/dev/adventure-forge-7
Integrity mode: development
Verification command: ./verify

## Requirements
### R1. Continuous Playtest Fleet
Run multi-persona blind playtesting (Explorer, Brute, Infiltrator, Speedrunner, Saboteur, Nomad, Diver, Scout) via the flywheel orchestrator. Triage all friction notes and defects.

### R2. Content Expansion
Add new systemic encounters and rich interactive scenes to the 5 provinces. Maintain 7-axis character reactivity and unbounded legal choices.

### R3. Verification Invariants
Enforce bit-for-bit SHA-256 replay determinism, 100% BFS reachability across all scenes, Hemingway brevity (FKGL 6-8, <=18 words/sentence, <=3 words/UI label), and 100% interactable density.

## Acceptance Criteria
- 100% pass on all 7 gates in ./verify
- 100% pass on pytest -v
- Zero lint or type errors (ruff, mypy)
- Commit and push each batch of enhancements to origin/main via git post-commit hook.

