# AdventureForge Engine Invariants

This rule is active for all agent interactions in this repository.

1. **Pure Determinism (R1)**:
   - State transition: `step(state, action, seed_cursor) -> StepResult`.
   - Never use wall-clock time, network, or unseeded randomness.
   - Use `DeterministicRNG` (SplitMix64) and SHA-256 state fingerprints.

2. **Hemingway Prose Standard (R3)**:
   - 1–3 short sentences per node/entity.
   - Max 18 words per sentence.
   - FKGL readability strictly Grade 6.0–8.0.
   - UI action labels: 1–3 words.
   - Zero purple prose words (`whispers`, `dance`, `loom`, `tapestry`, `cacophony`, `eldritch resonance`, `labyrinthine`, `ethereal`, `palpable`).

3. **Macro-World Scale & Density (R5)**:
   - 520 interconnected scenes across 5 provinces.
   - 100% reachability via BFS crawler.
   - >=3 interactables/entities in every scene (>= 260 density invariant).

4. **Information Firewall (R6)**:
   - Playtester agents interact exclusively through `new_game`, `step_game`, and `get_state`.
   - Observations must be sanitized with `sanitize_observation`.

5. **Canonical Verification**:
   - Always run `./verify` and `pytest -v` to ensure zero regressions before completing tasks.
