# Teamwork Specification: AdventureForge Autonomous Development & Audit Fleet

## 1. Project Overview
AdventureForge is an action-first, deeply reactive open-world RPG engine combining Skyrim geographical breadth (520 interconnected nodes across 5 distinct provinces) and Baldur's Gate 3 systemic depth (pure deterministic state transitions, 7-axis character reactivity, dynamic affordance synthesis, and regional mechanics). The system is driven by an autonomous flywheel with strict mechanical verification gates, blind playtester firewalls, and a Hemingway prose baseline.

- **Working directory:** `/home/micha/dev/adventure-forge-7`
- **Integrity mode:** `development`
- **Canonical Verification Command:** `./verify` (exit code 0 required)
- **Deployment Endpoint:** `https://adventure-forge-7.vercel.app`

---

## 2. Team Requirements (R1 – R4)

### Requirement 1 (R1): Audit & Bottleneck Remediation
- Profile the engine kernel, world loader (`loader.py`), BFS reachability crawler (`crawler.py`), and CLI/API response latency.
- Identify and eliminate any performance bottlenecks, unnecessary cache misses, redundant object instantiations, or graph traversal overheads.
- Ensure the live Vercel deployment API (`/api/game/*`) and ASGI entrypoints maintain sub-100ms response times and zero memory leaks in ephemeral execution.

### Requirement 2 (R2): World Expansion & Deep Systemic Mechanics
- Deepen reactive encounters and provincial quests across all 5 macro-regions:
  1. *The Reach* (Verticality, climbing, grapple mechanics)
  2. *The Lowlands* (Social stealth, disguise, rumor networks)
  3. *The Scorchwaste* (Heat survival, hydration depletion, sand navigation)
  4. *The High Court* (Court intrigue, favor exchange, etiquette duels)
  5. *The Sunken Hollows* (Underwater diving, breath limits, aquatic hazards)
- Ensure every enriched scene adheres to the dynamic affordance equation:
  $$\text{Legal Actions} = \text{Base} \cup \text{Items} \cup \text{Traits} \cup \text{Systemics}$$
  with zero artificial action limits or choice ceilings (preserving the 100+ choice unboundedness guarantee).

### Requirement 3 (R3): Autonomous Blind Playtester Loop & Defect Triage
- Deploy continuous multi-persona playtester fleet (`Explorer`, `Brute`, `Infiltrator`, `Speedrunner`, `Saboteur`) across the entire world graph via `adventure_forge.flywheel.loop` and `mcp_server.py`.
- Enforce the I6 Information Firewall: playtesters observe only player-facing state perceptions, never raw internal source data.
- Run automated triage (`triage.py`) on any reported failures, categorizing them strictly into `VERIFIED_DEFECT`, `CRASH_DEFECT`, or `REJECTED_UNREPLAYABLE`.
- Continuously compute session telemetry: retention heuristic, decision density, and branch coverage.

### Requirement 4 (R4): Hemingway Brevity Baseline & 100% Mechanical Verification
- All new and existing prose must pass the automated Hemingway Prose Linter (`prose_linter.py`):
  - Max 18 words per sentence.
  - 1 to 3 active-voice sentences per scene/entity description.
  - Grade 6–8 Flesch-Kincaid Grade Level.
  - 1 to 3 words per UI action label.
  - Zero banned purple prose terms.
- Preserve 100% passing status on all 7 verification gates in `./verify`:
  1. I1 Determinism & Replay Fingerprinting (SplitMix64 + SHA-256)
  2. World Graph Link Integrity (520+ nodes, 0 dangling links)
  3. G2 Hemingway Prose Linter
  4. I4 Counterfactual Character Divergence (Silas vs Vivienne)
  5. G6 Unbounded Choice Scaling (100+ actions in stress hubs)
  6. SYS-05 Non-LLM Reachability Crawler (100% reachability)
  7. SYS-06 Macro-World Interactable Density Invariant (>=260 scenes with >=3 interactables)
- Maintain zero errors across `pytest`, `ruff check .`, and `mypy adventure_forge`.
- Automatically sync all commits to `origin/main` via `.githooks/post-commit`.

---

## 3. Objective Acceptance Criteria

- [ ] **AC-1 (Audit & Performance):** Engine state transitions execute in < 1ms; world graph loading takes < 25ms; all Vercel serverless API handlers respond with status 200/OK in benchmark tests.
- [ ] **AC-2 (Systemic Expansion):** At least 10 new high-reactivity multi-stage systemic encounters integrated across the 5 provinces, fully wired to character axes and regional conditions.
- [ ] **AC-3 (Choice Freedom):** Stress scenes maintain >100 legal affordances without truncation or pagination degradation.
- [ ] **AC-4 (Playtester Fleet & Triage):** Flywheel executes >= 20 unattended cycles with 5 distinct personas, demonstrating >=0.95 average retention and 0 unhandled crash defects.
- [ ] **AC-5 (Prose & Style):** 100% compliance with Hemingway linter (<=18 words/sentence, Grade 6-8 FKGL, <=3 words/action label) across all newly created content.
- [ ] **AC-6 (Verification & Deployment):** `./verify` succeeds with all 7 gates green; all 180+ pytest unit/integration/adversarial tests pass; type check and lint are clean; changes committed and pushed to GitHub.
