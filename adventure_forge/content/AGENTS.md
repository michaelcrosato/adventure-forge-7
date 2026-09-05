# AdventureForge Content Authoring Rules

Any agent or contributor modifying or creating content in `adventure_forge/content/` must strictly observe these rules:

---

## 1. Hemingway Prose & Action Label Constraints (R3)
- **Sentence Word Limit**: Maximum 18 words per sentence.
- **Sentence Count**: Exactly 1 to 3 short sentences per description (scene, entity, or event).
- **FKGL Readability**: Flesch-Kincaid Grade Level must be between Grade 6.0 and 8.0.
- **UI Action Labels**: Exactly 1 to 3 words (e.g., `"Inspect Ledger"`, `"Drink Potion"`). Never exceed 3 words.
- **Zero Purple Lexicon**: Banned words: `whispers`, `dance`, `dance of`, `shadows dance`, `loom`, `looming`, `tapestry`, `tapestries`, `ancient tapestry`, `tapestry of`, `cacophony`, `eldritch resonance`, `labyrinthine`, `ethereal`, `palpable`.
- **Validation**: Test content changes immediately with:
  ```bash
  python3 -c "from adventure_forge.linter.prose_linter import ProseLinter; from adventure_forge.content.loader import build_world_registry; linter = ProseLinter(); errs = linter.lint_registry(build_world_registry()); print('Violations:', len(errs)); assert len(errs) == 0"
  ```

---

## 2. Interactable Density Invariant (SYS-06)
- Every single scene should provide at least **3 meaningful interactables or entities** (`len([a for a in scene.base_actions if a.category != 'movement']) + len(scene.entities) >= 3`).
- Across the macro-world, at least 260 of 520 scenes must satisfy this invariant (currently 520/520 = 100%).
- Never delete interactables without replacing them.

---

## 3. World Graph Integrity & Reachability (R5 / SYS-05)
- All exits in `scene.exits` must map to valid target scene IDs in the world registry.
- Maintain 100% BFS reachability from all provincial hubs.
- After modifying scenes, always run `./verify` to verify link integrity and the BFS crawler.

---

## 4. Regional Mechanics Invariants
- **The Reach**: Features verticality, climbing stamina, and altitude hazards.
- **The Sunken Hollows**: Features underwater diving, air supply, and water pressure.
- **The Scorchwaste**: Features heat survival, hydration levels, and sunstroke.
- **The High Court**: Features court intrigue, noble decorum, and political favor.
- **The Lowlands**: Features social stealth, disguise layers, and suspicion meters.
