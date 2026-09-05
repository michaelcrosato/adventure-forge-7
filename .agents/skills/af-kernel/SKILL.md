---
name: af-kernel
description: >-
  Use this skill when modifying or extending the AdventureForge deterministic
  engine kernel, SplitMix64 PRNG cursor, SHA-256 state fingerprints,
  condition/effect DSL, or dynamic affordance synthesis.
---

# AdventureForge Deterministic Engine Kernel Runbook

This skill provides architectural guidance for modifying or extending the core deterministic game engine in `adventure_forge/core/`.

---

## 1. Core Engine Architecture

The core engine is located in `adventure_forge/core/`:
- `state.py`: `GameState`, `CharacterSheet`, inventory, world flags, fingerprinting.
- `engine.py`: `AdventureEngine.step(state, action_id) -> Tuple[GameState, StepResult]`.
- `rng.py`: `DeterministicRNG` based on the SplitMix64 algorithm.
- `actions.py`: Dynamic affordance synthesis engine.
- `conditions.py`: Declarative condition evaluation DSL.
- `effects.py`: Pure state mutation effect processor.
- `character.py`: Character presets (`cutpurse`, `noble`, `warrior`, `pit_fighter`, etc.).

---

## 2. Invariants & Rules

### A. Pure Functional State Transitions
- State transitions must be pure functions with zero side effects:
  $$\text{step}(s, a) \to (s', \text{result})$$
- Never mutate state in-place without creating a clean snapshot or returning a new state.
- Do NOT use wall-clock time (`time.time()`, `datetime.now()`) or unseeded PRNG (`random.random()`).
- All randomness must consume the state's `DeterministicRNG` cursor.

### B. State Fingerprinting
- `state.fingerprint()` computes a canonical SHA-256 hash across:
  * Turn count
  * Character attributes, stamina, traits, flaws, skills, reputation
  * Inventory items and quantities
  * World flags (sorted keys)
  * Current scene and region
  * PRNG cursor position
- Never include non-deterministic objects, memory addresses, or unseeded floats in the hash.

### C. Declarative Condition & Effect DSL
- To add a new condition predicate:
  1. Add the predicate handler in `adventure_forge/core/conditions.py`.
  2. Implement unit tests in `tests/unit/test_conditions.py`.
- To add a new effect mutation:
  1. Add the mutation operator in `adventure_forge/core/effects.py`.
  2. Ensure bounds checking (e.g., stamina clamped to `[0, max_stamina]`).
  3. Implement unit tests in `tests/unit/test_effects.py`.

### D. Dynamic Affordance Equation
$$\text{Affordances} = \text{Base Actions} \cup \text{Inventory Affordances} \cup \text{Trait Exploits} \cup \text{Regional Systemics}$$
- Synthesized in `adventure_forge/core/actions.py`.
- Must support 2 to 200+ legal actions without degradation.

---

## 3. Verification Workflow
After any engine change, execute:
```bash
pytest tests/unit/ tests/integration/ tests/verification/ -v
./verify
```
