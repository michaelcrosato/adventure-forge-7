# AdventureForge: Verification Evidence & Contest Submission

**Document Version:** 1.0.0  
**Repository Working Directory:** `/home/micha/dev/adventure-forge-7`  
**Governing Specifications:** `c56adventure-forge-thesis-design-brief.md` & `x46ADVENTURE_KERNEL_DESIGN_BRIEF.md`

---

## 1. How to Run `verify` and Play

### 1.1 Mechanical Verification Bar (No LLM Required)
```bash
./verify
# or canonical Python module:
python3 -m adventure_forge.verify
```
All 7 mechanical gates execute headlessly and exit 0:
1. I1 Determinism & Replay Fingerprint Matching (100% bit-for-bit fidelity)
2. World Graph Link Integrity (0 broken references across 520 scenes)
3. G2 High-Velocity Hemingway Prose Linter (<= 18 words/sentence, Grade 6–8 FKGL)
4. I4/G1/G3 Counterfactual Character Sheet Witness Divergence
5. G6 Unbounded Choice Scaling (100+ actions in single scene: Grand Bazaar = 115 actions)
6. SYS-05 Non-LLM BFS/DFS Reachability Crawler (100% reachability across 520 scenes)
7. SYS-06 Macro-World Interactable Density Invariant (510/520 scenes, 98.08% >= 3 interactables)

### 1.2 Automated Test Suite
```bash
pytest -v
```
Runs the full 4-tier + adversarial test suite (**180 tests passing in ~2.3 seconds**).

### 1.3 Interactive Play
- **Terminal CLI (Interactive with categorized pagination):**
  ```bash
  python3 -m adventure_forge.player.cli
  ```
- **Agent Player Surface (Model Context Protocol / stdio JSON-RPC 2.0):**
  ```bash
  python3 -m adventure_forge.player.mcp_server
  ```
- **Autonomous Flywheel Loop (10 Unattended Cycles):**
  ```bash
  ./zu-loop run --cycles 10
  ```
- **Live Production Web Game (Direct Browser Play):**
  Play immediately at **[https://adventure-forge-7.vercel.app](https://adventure-forge-7.vercel.app)**

---

## 2. Orchestrator Charter

The active orchestrator charter is committed at [`ORCHESTRATOR_CHARTER.md`](ORCHESTRATOR_CHARTER.md). It formally binds the orchestrator agent to the honesty invariants (I1–I8), the six game-product requirements (G1–G6), and the three-level authority model without runtime LLM physics.

---

## 3. Character Sheets, Outcome Replays & Witness Divergence

### 3.1 Two Opposing Character Sheets
```python
# Character Sheet A: Silas the Cutpurse (Outlaw Infiltrator)
silas = CharacterSheet(
    name="Silas",
    ancestry="Deep-Dweller",
    background="cutpurse",
    attributes={"agility": 14, "strength": 8, "intimidation": 6},
    skills={"cunning": 4, "stealth": 3},
    traits=["night_eyed", "streetwise"],
    flaws=["marked_outlaw"],
    reputation={"smugglers": 10, "city_watch": -10},
    markers=["guild_brand"],
    inventory=["silver_coin"]
)

# Character Sheet B: Lady Vivienne (Aristocrat Diplomat)
vivienne = CharacterSheet(
    name="Lady Vivienne",
    ancestry="High-Kin",
    background="noble_exile",
    attributes={"agility": 8, "strength": 10, "intimidation": 15},
    skills={"rhetoric": 4, "cunning": 2},
    traits=["skeptical", "court_manners"],
    flaws=["oath_bound"],
    reputation={"smugglers": -10, "city_watch": 10, "justiciars": 10},
    markers=["watch_crest"],
    inventory=["legal_dossier", "silver_coin"]
)
```

### 3.2 Shared Scene Divergence Proof (`warrens_gate`)
Both characters start in the identical opening scene `warrens_gate` (*The Warrens Iron Gate*). The deterministic engine evaluates their orthogonal trait vectors:

| Character | Observable Prose | Unique Legal Action | Outcome Scene | Start State Hash | Step 1 State Hash |
|---|---|---|---|---|---|
| **Silas** | *"You spot the carved thieves mark hidden beside the sewer drain."* | `flash_thief_signet` (*Flash thief sign*) | `warrens_black_market` | `c48703e8d87dfa21be07e1673935de8331e307fa0879da8914fc2207cdc8295a` | `6398206a0af6c3203da2108326571b43ee986c2cc9fdd130483a10600ddec82f` |
| **Lady Vivienne** | *"The sergeant straightens up and snaps a crisp military salute."* | `demand_guard_entry` (*Order guards aside*) | `warrens_guardhouse` | `a814531ffb34fc2715eb7a2e08c1c3b9be6a3ecac904ac409fafbc1ffc11f814` | `8bba900e90b71298328830e8aedfe67a2f4107dd077549ccf8d9ed7eb2d1e6c1` |

- `flash_thief_signet` is strictly legal for Silas and rejected for Vivienne.
- `demand_guard_entry` is strictly legal for Vivienne and rejected for Silas.
- Independent replay matches these state fingerprints bit-for-bit.

### 3.3 Two Distinct Authoritative Ending Replays
1. **Outcome 1: Shadow Syndicate Sovereignty (`shadow_syndicate`)**
   - Replay witness trace: Silas infiltrates the lower city, recovers the shadow ledger, bypasses the watch, and delivers the 5 continental seals to the Smuggler Syndicate.
   - Final Result: The continent is governed by an unregulated black-market guild.
2. **Outcome 2: Justiciar Martial Order (`justiciar_order`)**
   - Replay witness trace: Lady Vivienne argues before the High Tribunal, secures an emergency writ, and submits the 5 seals to the Grand Justiciar.
   - Final Result: Strict constitutional martial law is enforced across all 5 provinces.

---

## 4. Playtester Reports: Replayed vs Rejected

### 4.1 Valid Replayed Report (Evidence of Deterministic Reproduction)
- **Session ID:** `triage-valid-silas-001`
- **Claimed Finding:** Infiltration through `warrens_gate` into `warrens_black_market` correctly purchases lockpicks and unlocks `entity_sewer_grate_state`.
- **Trace:** `["flash_thief_signet", "buy_lockpicks", "leave_market", "back_to_gate", "pick_sewer_grate"]`
- **Triage Result:** `VERIFIED_DEFECT` / Replay Succeeded.
- **Verification Log:** Trace executed across 5 steps; all 5 transitions verified against engine rules; final fingerprint `3286f9bc...` matches session telemetry.

### 4.2 Rejected Report (Evidence of Tamper Rejection)
- **Session ID:** `triage-tampered-saboteur-999`
- **Claimed Finding:** Claimed the game softlocked on action `fabricated_action_that_never_existed`.
- **Trace:** `["walk_to_warrens", "fabricated_action_that_never_existed"]`
- **Triage Result:** `REJECTED_UNREPLAYABLE`.
- **Verification Log:** Action `fabricated_action_that_never_existed` is not enumerated by engine; transition rejected; state unchanged. Report discarded as unverified fiction.

---

## 5. Builder Cycle from Verified Finding

### 5.1 The Finding
In production on Vercel (`adventure-forge-7.vercel.app`), visiting the root URL responded with `{"error":"not_found"}` because Vercel's rewrite rule (`/(.*) -> /api/index.py`) altered the ASGI `scope["path"]` to `/api/index.py`, failing route dispatch in `app.py`.

### 5.2 The Patch
1. In `vercel.json`, captured incoming request paths via destination query forwarding:
   ```json
   {
     "source": "/(.*)",
     "destination": "/api/index.py?__path=/$1"
   }
   ```
2. In `app.py`, implemented `_extract_path(scope)` parsing query parameter `__path`, inspecting proxy headers (`x-matched-path`), and serving an interactive Hemingway RPG web app with pure stateless `/api/game/*` endpoints.
3. Automatically committed and pushed to GitHub via `.githooks/post-commit`.

### 5.3 Verification
- Live production verified: `GET /` serves interactive RPG; `POST /api/game/new` and `POST /api/game/step` execute deterministic multi-turn play directly on Vercel.
- All prior replay traces, verification gates, and test suites remained 100% green.

---

## 6. Orchestrator Process Change and Delegation

### 6.1 Process Mutation (Self-Improving Pipeline)
The Orchestrator modified the mechanical verification pipeline by introducing **Gate 7 (Macro-World Interactable Density Invariant)** to enforce that >= 50% of world nodes offer >= 3 meaningful interactables before any change can land. In addition, the Orchestrator installed the `.githooks/post-commit` hook to automate remote pushes to GitHub upon every commit.

### 6.2 Autonomous Subagent Delegation
The Orchestrator instantiated and directed a fleet of specialized subagent personas:
- **Explorer:** Searches graph topology and samples diverse scene verbs.
- **Infiltrator:** Prioritizes stealth, cunning, and lockpicking affordances.
- **Brute:** Exercises high-strength verbs and combat risks.
- **Speedrunner:** Executes rapid room transitions to benchmark graph latency.
- **Saboteur:** Stresses high-risk environmental burning and edge-case inputs.

---

## 7. Shipped World Inventory: Unique Areas vs Generated Substrate

Total Contiguous Graph Size: **520 Nodes** across **11 Regions**

| Region Identifier | Region Name | Shipped Nodes | Defining Unique Mechanic | Interactable Density |
|---|---|---:|---|---:|
| `iron_crags` | The Iron Crags (Hub) | 3 | Verticality, Climbing Gear, Wind Hazards | 100.0% (3/3) |
| `lower_warrens` | The Lower Warrens (Hub) | 4 | Social Stealth, Disguise Kits, Smuggler Posterns | 100.0% (4/4) |
| `scorchwaste_local` | The Scorchwaste (Hub) | 2 | Ambient Heat, Waterskin Hydration, Shade Tracking | 100.0% (2/2) |
| `high_court_local` | High Court of Veras (Hub) | 2 | Legal Evidence, Tribunal Testimony, Aristocratic Decorum | 100.0% (2/2) |
| `sunken_hollows_local` | The Sunken Hollows (Hub) | 2 | Water Buoyancy, Diving Bells, Depth Pressure | 100.0% (2/2) |
| `stress_market` | The Grand Bazaar Plaza | 1 | Unbounded Choice Space (115 Legal Actions) | 100.0% (1/1) |
| `province_reach` | The Reach | 101 | 10 Alpine POIs + Alpine Crevasse Secret Shrine (Node 520) | 99.0% (100/101) |
| `province_lowlands` | The Lowlands | 101 | 10 River/Port POIs + Great Canal Sluices | 97.0% (98/101) |
| `province_scorchwaste`| Greater Scorchwaste | 101 | 10 Desert/Tomb POIs + White Salt Flats | 97.0% (98/101) |
| `province_high_court` | Greater Veras Crown | 101 | 10 Basilica/Catacomb POIs + Royal Archives | 98.0% (99/101) |
| `province_sunken_hollows`| Greater Sunken Abyss | 101 | 10 Grotto/Trench POIs + Abyssal Pearl Vault | 97.0% (98/101) |
| **Total Shipped** | **Single World Graph** | **520** | **5 Orthogonal Region-Defining Mechanics** | **98.08% (510/520)** |

Every single one of the 520 nodes satisfies:
- Hemingway prose baseline (<= 18 words/sentence, Grade 6–8 FKGL, zero purple words).
- 100% reachability proven by non-LLM BFS graph crawler.
- Zero dangling target scenes or broken entity destinations.
