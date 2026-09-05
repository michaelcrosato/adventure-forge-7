# AdventureForge Agent Guidelines & Engine Invariants

This file defines the authoritative rules, architectural invariants, prose constraints, and operational commands for any AI agent or developer operating within the AdventureForge repository.

---

## 1. Core Architectural Pillars & Non-Negotiable Invariants

### Invariant 1: Pure Deterministic State Kernel (R1)
- The state transition kernel is strictly pure and deterministic:
  $$\text{step}(\text{state}, \text{action\_id}, \text{seed\_cursor}) \to (\text{state}', \text{StepResult})$$
- **Zero non-deterministic inputs**: No `datetime.now()`, no `time.time()`, no unseeded `random`, and no network or I/O calls inside transition logic.
- **Authoritative PRNG**: All randomness must flow strictly through the engine's deterministic `SplitMix64` PRNG cursor.
- **Replay Fidelity**: Given the same initial seed and action sequence, replay execution must produce bit-for-bit identical SHA-256 state fingerprints.

### Invariant 2: 7-Axis Character Reactivity (R2)
- Characters are represented across 7 orthogonal axes:
  1. Ancestry
  2. Background
  3. Attributes
  4. Skills
  5. Traits
  6. Flaws
  7. Reputation & Faction Markers
- World content, dialogue, and affordances must query this state vector dynamically.
- Counterfactual witness pairs (e.g., Silas the Cutpurse vs. Vivienne the High Noble) in the same opening scene must yield demonstrably distinct legal actions and narrative responses.

### Invariant 3: High-Velocity Hemingway Prose & Label Limits (R3)
- **Sentence Length**: Maximum **18 words** per sentence.
- **Sentence Count**: Exactly **1 to 3 short sentences** per scene observation, entity description, or dialogue beat.
- **Readability**: Flesch-Kincaid Grade Level (FKGL) strictly clamped between **Grade 6.0 and Grade 8.0**.
- **Voice**: Active voice only. High action tempo.
- **UI Action Labels**: Exactly **1 to 3 words** per label (e.g., `"Examine Lock"`, `"Drink Water"`).
- **Banned Purple Lexicon**: Zero ornamental filler clichés. The following words/phrases are strictly forbidden:
  * `whispers` / `whispering`
  * `dance` / `dance of` / `shadows dance`
  * `loom` / `looming`
  * `tapestry` / `tapestries` / `ancient tapestry` / `tapestry of`
  * `cacophony`
  * `eldritch resonance`
  * `labyrinthine`
  * `ethereal`
  * `palpable`

### Invariant 4: Unbounded Choice Synthesis & Presentation (R4)
- Choices are synthesized dynamically at runtime using the affordance equation:
  $$\text{Affordances} = \text{Base Actions} \cup \text{Inventory Affordances} \cup \text{Trait Exploits} \cup \text{Regional Systemics}$$
- **Zero artificial ceilings**: The engine must support scaling from 2 to 200+ legal actions without crashing or truncating choices.
- Presentation layers (CLI, MCP, Web) must provide clean categorization, grouping, and pagination without truncation.

### Invariant 5: Macro-World Graph & Regional Mechanics (R5)
- **World Scale**: Exactly **520 interconnected scenes** spanning 5 provinces and interlocking hubs.
- **Reachability Invariant**: 100% graph reachability proven via non-LLM BFS crawler. No dead-ends or unreachable islands.
- **Interactable Density Invariant**: At least 50% (>= 260 scenes, currently 520/520) must provide **3 or more meaningful interactables or entities**.
- **5 Province Mechanics**:
  1. *The Reach*: Verticality, climbing stamina, and altitude hazards.
  2. *The Sunken Hollows*: Underwater diving, air conservation, and hydrostatic pressure.
  3. *The Scorchwaste*: Heat survival, hydration management, and sunstroke.
  4. *The High Court*: Court intrigue, political favor, and noble decorum.
  5. *The Lowlands*: Social stealth, disguises, and bounty/suspicion.

### Invariant 6: Information Firewall (R6 / I6)
- Agent playtesters and external clients interact with the game engine **solely through the player surface** (`adventure_forge.player.mcp_server` or `adventure_forge.player.cli`).
- The player surface sanitizes observations (`sanitize_observation`), returning only player-visible fields: `scene_id`, `region_id`, `title`, `description`, `events`, `legal_actions`, `turn_count`, `is_terminal`, `outcome`, `fingerprint`.
- Agents acting as playtesters must **never** inspect internal engine state, raw conditions/effects, world flags, or hidden source code to make gameplay decisions.

---

## 2. Mechanical Verification Bar & Quality Gates

Before committing or concluding any task, verify that all mechanical gates pass cleanly:

### 1. The 7-Gate Canonical Verification Bar
```bash
./verify
# or:
python3 -m adventure_forge.verify
```
All 7 gates must pass:
1. Determinism & Replay Fingerprinting (100% replay fidelity).
2. World Graph Link Integrity (zero dangling scene or entity links).
3. Hemingway Prose Linter (FKGL 6–8, <=18 words/sent, <=3 words/label, no purple prose).
4. Counterfactual Character Divergence (Silas vs. Vivienne witness proofs).
5. Unbounded Choice Scaling (100+ actions in `bazaar_center`).
6. Non-LLM BFS Reachability Crawler (100% reachability across 520 scenes).
7. Macro-World Interactable Density (>= 260 scenes with >= 3 interactables).

### 2. Full Test Suite
```bash
pytest -v
```
All 324+ tests across unit, integration, verification, and scenario tiers must pass.

### 3. Static Type Checking & Linting
```bash
ruff check .
mypy adventure_forge
```
Zero lint warnings or type errors permitted.

---

## 3. Autonomous Playtesting & Flywheel Operations

Run the multi-persona playtester fleet to audit world content and mechanics:
```bash
python3 -m adventure_forge.flywheel.loop run --cycles 10
# or:
./loop.sh
```
- Personas: `Explorer`, `Brute`, `Infiltrator`, `Speedrunner`, `Saboteur`.
- Inspect reports in `flywheel_audit.jsonl`.
- Defect triage: `adventure_forge.flywheel.triage`.

---

## 4. Deployment & Git Sync Rules

- **Git Automatic Push**: The repository has an active post-commit hook (`.githooks/post-commit`). Every local commit triggers an automatic `git push origin <branch>`.
- **Stateless ASGI Entrypoint**: `app.py` and `api/index.py` provide stateless serverless request handling. Never rely on mutable in-memory state or filesystem persistence across requests.
- **Health Check**: `/health` must always respond with JSON containing `service`, `status`, and `version` on both `GET` and `HEAD` requests.
- **MCP HTTP Surface**: `/api/mcp` serves JSON-RPC 2.0 requests over HTTP.
