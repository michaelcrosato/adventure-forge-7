---
name: af-content
description: >-
  Use this skill when authoring, modifying, or auditing AdventureForge scenes,
  regions, POIs, regional mechanics, interactables, or Hemingway prose across
  the 5 provinces.
---

# AdventureForge Content Authoring & World Graph Runbook

This skill provides step-by-step procedures for writing new scenes, interactables, regional mechanics, and systemic encounters while maintaining all engine invariants.

---

## 1. Content File Layout

All world content lives under `adventure_forge/content/`:
- `models.py`: Data classes (`Scene`, `Region`, `Entity`, `Action`, `Item`).
- `loader.py`: `build_world_registry()` combining all province modules.
- `data/provinces/`:
  * `reach.py`: The Reach (Mountainous, verticality, climbing).
  * `sunken_hollows.py`: Sunken Hollows (Subterranean / underwater, diving).
  * `scorchwaste.py`: Scorchwaste (Desert dunes, heat survival, hydration).
  * `high_court.py`: High Court (Palaces, court intrigue, noble favor).
  * `lowlands.py`: The Lowlands (Forests, towns, bazaar, social stealth).
- `data/mechanics/`: Handlers for regional environmental systemics.
- `tools/generate_provinces.py`: World graph generator script.

---

## 2. Invariants for Every Scene

When creating or modifying a scene:

### A. Hemingway Prose Rules
1. **Sentence Length**: Maximum **18 words** per sentence.
2. **Sentence Count**: Exactly **1 to 3 short sentences**.
3. **Reading Level**: Flesch-Kincaid Grade Level between **6.0 and 8.0**.
4. **Action Labels**: Exactly **1 to 3 words** (e.g., `"Climb Cliff"`, `"Drink Canteen"`, `"Pick Lock"`).
5. **Zero Banned Purple Words**:
   - Do NOT use: `whispers`, `dance`, `dance of`, `shadows dance`, `loom`, `looming`, `tapestry`, `tapestries`, `ancient tapestry`, `tapestry of`, `cacophony`, `eldritch resonance`, `labyrinthine`, `ethereal`, `palpable`.

### B. Interactable Density Rule
- Every scene must offer at least **3 meaningful interactables or entities**:
  $$\text{non-movement actions} + \text{entities} \ge 3$$
- Example interactables: containers, NPCs, environmental features, levers, water sources.

### C. Graph Connectivity
- Every exit must point to an existing `scene_id`.
- Ensure paths are bidirectional or have alternative paths to prevent dead-end softlocks.

---

## 3. Authoring Template for a Scene

```python
from adventure_forge.content.models import Scene, Entity, Action

Scene(
    id="reach_high_pass",
    title="High Pass",
    description="Wind cuts through the narrow gap. Snow covers the path ahead. Loose stone lines the ridge.",
    region_id="the_reach",
    exits={
        "north": "reach_frozen_peak",
        "south": "reach_crag_camp",
    },
    entities=[
        Entity(
            id="frozen_shrine",
            name="Frozen Shrine",
            description="Ancient stones stand in the drift. Carvings mark old gods.",
            interactable=True,
            actions=[
                Action(
                    id="pray_shrine",
                    label="Pray At Shrine",
                    description="Kneel before the cold stone.",
                    effects=[{"type": "modify_attribute", "attribute": "stamina", "amount": 10}],
                )
            ]
        ),
        Entity(
            id="loose_boulder",
            name="Loose Boulder",
            description="A heavy rock balances on the ledge.",
            interactable=True,
        )
    ],
    base_actions=[
        Action(
            id="scout_ridge",
            label="Scout The Ridge",
            description="Survey the mountain slope below.",
        ),
        Action(
            id="gather_firewood",
            label="Gather Dried Wood",
            description="Search the brush for kindling.",
        ),
    ]
)
```

---

## 4. Validating Your Content Changes

Run the validation suite after editing content:
```bash
# 1. Check prose linter
python3 -c "
from adventure_forge.linter.prose_linter import ProseLinter
from adventure_forge.content.loader import build_world_registry
errs = ProseLinter().lint_registry(build_world_registry())
assert not errs, f'Prose errors: {errs}'
print('Prose lint passed!')
"

# 2. Run verification bar
./verify
```
