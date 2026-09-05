---
name: af-playtest
description: >-
  Use this skill when running the blind playtester fleet (zu-loop / flywheel),
  executing multi-persona simulations (Explorer, Brute, Infiltrator, Speedrunner,
  Saboteur), inspecting flywheel audit logs, or reproducing and triaging defects.
---

# AdventureForge Flywheel & Playtester Runbook

This skill guides the execution of the autonomous multi-agent playtester loop, persona profiling, audit log analysis, and defect reproduction triage.

---

## 1. Quick Playtester Commands

```bash
# Run 10 flywheel simulation cycles
python3 -m adventure_forge.flywheel.loop run --cycles 10

# Or using the root wrapper
./loop.sh

# Run with specific persona
python3 -m adventure_forge.flywheel.loop run --persona explorer --cycles 5
```

---

## 2. The 5 Playtester Personas

Each persona embodies a distinct gameplay style operating under the **I6 Information Firewall** (blind playtesting via player observations only):

1. **Explorer**:
   - Heuristic: Prioritizes unvisited scenes, exits to new POIs, and lore interactables.
   - Purpose: Validates world graph reachability, discovery flags, and atmospheric text.
2. **Brute**:
   - Heuristic: Favors high-risk physical actions, aggressive confrontation, and combat stunts.
   - Purpose: Stresses stamina depletion, survival thresholds, and death conditions.
3. **Infiltrator**:
   - Heuristic: Prioritizes stealth, lockpicking, social disguise, and theft affordances.
   - Purpose: Tests faction suspicion meters, stealth status effects, and intrigue branches.
4. **Speedrunner**:
   - Heuristic: Optimizes direct paths toward provincial hubs, seals, and quest milestones.
   - Purpose: Verifies quest progression flags and critical path completion.
5. **Saboteur**:
   - Heuristic: Selects edge cases, invalid IDs, stress conditions, and rapid state reversals.
   - Purpose: Tests boundary stability, error recovery, and engine firewall integrity.

---

## 3. Inspecting Audit Logs (`flywheel_audit.jsonl`)

The flywheel logs each simulation run as a JSON object:
```bash
# View last 5 runs
tail -n 5 flywheel_audit.jsonl | jq .

# Check for failed or exceptional runs
grep -i '"success": false' flywheel_audit.jsonl | jq .

# Count runs by persona
cat flywheel_audit.jsonl | jq -r .persona | sort | uniq -c
```

---

## 4. Automated Defect Triage Harness

When an audit log identifies a defect or unexpected terminal state:
```bash
# Reproduce a specific run seed deterministically
python3 -c "
from adventure_forge.flywheel.triage import reproduce_trace
result = reproduce_trace(seed=999, preset='cutpurse', action_sequence=['examine_lock', 'pick_lock'])
print('Reproduction match:', result.matches_expected)
print('Final state hash:', result.actual_fingerprint)
"
```
Because the engine is 100% deterministic (R1), replaying the exact seed and action trace will reproduce the issue bit-for-bit.
