# AdventureForge Core Engine Rules

Any agent or contributor working within `adventure_forge/core/` must strictly observe these rules:

---

## 1. Pure Deterministic Authority (R1)
- State transitions are authoritative pure functions:
  $$\text{step}(\text{state}, \text{action\_id}, \text{seed\_cursor}) \to (\text{state}', \text{StepResult})$$
- `GameState` is immutable-style: transitions return a new or updated `GameState` and an authoritative `StepResult`.
- **Zero non-deterministic calls**: Absolutely no calls to `time.time()`, `datetime.now()`, or unseeded `random` anywhere in transition code.
- **PRNG Discipline**: All randomness uses the deterministic `SplitMix64` PRNG cursor (`DeterministicRNG`). Advance the cursor systematically.
- **Fingerprinting**: `state.fingerprint()` must use canonical SHA-256 serialization. Replays with identical seed and action history must yield identical fingerprints.

---

## 2. Declarative Condition & Effect DSL
- Conditions and mutations must be evaluated through the declarative DSL in `conditions.py` and `effects.py`.
- Never execute arbitrary strings (`eval` / `exec`).
- Support declarative predicates: `has_item`, `trait_active`, `attribute_gte`, `skill_gte`, `reputation_gte`, `flag_equals`, `region_equals`, `weather_equals`.
- Clamped mutations: all attribute/stamina changes must respect bounded minimum and maximum values.

---

## 3. Dynamic Affordance Synthesis (R4)
- Legal actions for any scene are dynamically computed:
  $$\text{Actions} = \text{Base Actions} \cup \text{Inventory Affordances} \cup \text{Trait Exploits} \cup \text{Regional Systemics}$$
- Never hardcode action lists without passing through condition checks.
- Support scaling from 2 to 200+ legal actions without crash or performance degradation.
