# AdventureForge Flywheel & Playtester Rules

Any agent or contributor working within `adventure_forge/flywheel/` must strictly observe these rules:

---

## 1. Blind Playtester Personas (R6)
- Playtesters must operate under the **I6 Information Firewall**.
- Personas must choose actions based solely on the player-visible observation (`legal_actions`, `description`, `events`, `title`):
  1. `Explorer`: Prioritizes unvisited scenes, exits, and lore interactables.
  2. `Brute`: Chooses high-risk combat and physical prowess actions.
  3. `Infiltrator`: Favors stealth, subterfuge, theft, and evasion.
  4. `Speedrunner`: Optimizes pathing towards provincial hubs and quest objectives.
  5. `Saboteur`: Intentionally tests boundary conditions, invalid actions, and stress limits.
- Personas must never inspect internal engine state or cheat by peeking at world files.

---

## 2. Automated Triage & Defect Reproduction
- When a playtester encounters an unexpected terminal state, softlock, or exception, the run trace must be recorded in `flywheel_audit.jsonl`.
- `adventure_forge.flywheel.triage` must be able to replay the trace using the recorded seed and action sequence to deterministically reproduce the defect.
- All triage reproductions must produce identical state fingerprints.
