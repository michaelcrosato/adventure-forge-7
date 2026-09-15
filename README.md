# AdventureForge: The Unbounded Action Engine

[![Verify](https://github.com/michaelcrosato/adventure-forge-7/actions/workflows/ci.yml/badge.svg)](https://github.com/michaelcrosato/adventure-forge-7)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"Freedom in design. Honesty in verification. The model never is the world."**

AdventureForge is an action-first, deeply reactive open-world RPG engine built on a pure deterministic state transition kernel (`step(state, action, seed_cursor) -> state'`). It combines the geographical travel breadth of **Skyrim** with the systemic, choice-rich depth of **Baldur's Gate 3**.

---

## Key Pillars & Invariants

1. **Pure Deterministic Authority (R1):** State transitions are 100% pure code: `step(state, action_id, seed_cursor) -> (state', StepResult)`. No wall clock, network, or unseeded randomness. Replays reproduce state hashes bit-for-bit via the authoritative `SplitMix64` PRNG cursor.
2. **7-Axis Character Reactivity (R2):** Characters are represented across 7 orthogonal axes: Ancestry, Background, Attributes, Skills, Traits, Flaws, and Reputation/Faction Markers. Counterfactual witness pairs (e.g., Silas vs. Vivienne) yield demonstrably distinct legal actions and narrative responses.
3. **High-Velocity Hemingway Prose (R3):** Exactly 1–3 short sentences per observation, active voice, FKGL clamped between Grade 6.0 and Grade 8.0, maximum 18 words per sentence, strict 1–3 word UI action labels, and zero purple prose clichés.
4. **Unbounded Scene Possibility Space (R4):** Dynamic affordance synthesis supporting 2 to 200+ legal actions without artificial ceilings (`Choices = Base ∪ Inventory ∪ Traits ∪ Systemics`).
5. **Continuous 520-Scene World Graph (R5):** 520 interconnected scenes spanning 5 provinces and interlocking hubs with 100% BFS reachability and 100% interactable density (>=3 interactables per scene).
6. **Information Firewall (R6 / I6):** External clients and agent playtesters interact solely through the sanitized player observation contract (`MCPServer` or CLI), never inspecting internal engine objects or raw condition/effect DSL payloads.
7. **Autonomous Multi-Agent Flywheel:** Unattended self-healing and expansion loop using multi-persona blind playtester fleets (Explorer, Brute, Infiltrator, Speedrunner, Saboteur, Nomad, Diver, Scout) with automated defect triage.

---

## 5 Shipped Provinces & Regional Mechanics

| Province | Primary Mechanic | Environmental Systemics & Hazards |
|---|---|---|
| **The Reach** | Verticality & Climbing Stamina | Mountain blizzards, high wind bluffs, rope ascents, altitude hazards |
| **The Sunken Hollows** | Underwater Diving & Hydrostatic Pressure | Bioluminescence, water submersion, conductive shock, abyssal ruins |
| **The Scorchwaste** | Heat Survival & Hydration Management | Desert heatwaves, sunstroke, sandstorms, water oasis cisterns |
| **The High Court** | Court Intrigue & Noble Decorum | Sentried curfews, diplomatic dossiers, tribunal rhetoric, legal decrees |
| **The Lowlands** | Social Stealth & Bounty Infiltration | Sewer miasma, thief signets, customs broker ciphers, watch permits |

---

## 7 Character Archetypes

- **Silas the Cutpurse** (Plainsman / Street Drifter): Stealth, lockpicking, thief signets, agile evasion.
- **Lady Vivienne** (High-Kin / Noble Exile): High-court rhetoric, legal dossiers, aristocratic influence.
- **Garron** (Ashenborn / Pit Fighter): Brute strength, athletics, crowbar leverage, raw endurance.
- **Kael** (Nomad / Dune Strider): Desert survival, heat tolerance, sandstorm navigation, bartering.
- **Mara** (Deep-Dweller / Abyssal Diver): Underwater breathing, keen night vision, submerged ruins salvage.
- **Torin** (Reachman / Mountain Scout): Cliff scaling, rope climbing, highland lookout navigation.
- **Garron (Pit Fighter)**: Canonical combat-ready warrior alias.

---

## Verification & Testing

Before committing, all 7 gates of the mechanical verification bar must pass cleanly:

```bash
# 1. Run the 7-Gate Mechanical Verification Bar
./verify
# or:
python3 -m adventure_forge.verify

# 2. Run the Full Pytest Suite (330+ tests)
pytest -v

# 3. Static Type Checking and Linting
ruff check .
mypy adventure_forge
```

### The 7 Mechanical Verification Gates
1. **Determinism & Replay Fingerprinting:** Bit-for-bit SHA-256 state replay fidelity.
2. **World Graph Link Integrity:** 100% resolution of all scene targets, entity destinations, and transition effects.
3. **Hemingway Prose Linter:** Grade 6–8 FKGL, <=18 words/sentence, <=3 words/label, zero purple lexicon.
4. **Counterfactual Character Divergence:** Silas vs. Vivienne witness proofs across shared scenes.
5. **Unbounded Choice Scaling:** 100+ actions in `bazaar_center` without degradation.
6. **Non-LLM BFS Reachability Crawler:** 100% reachability across all 520 scenes.
7. **Macro-World Interactable Density:** 100% of scenes (520/520) offer >= 3 interactables.

---

## Interactive Play & Autonomous Flywheel

```bash
# Interactive CLI Player (Action-First, Paginated UI)
python3 -m adventure_forge.player.cli [preset]

# Multi-Persona Autonomous Flywheel Loop (10 cycles)
./loop.sh
# or:
python3 -m adventure_forge.flywheel.loop run --cycles 10
```

---

## Deployment & Stateless Serverless Architecture

AdventureForge deploys seamlessly to Vercel with zero configuration:
- **`GET /`**: Full interactive playable web application with Hemingway UI, preset selection, and live action execution.
- **`GET /health` & `HEAD /health`**: Machine-readable JSON health monitor (`service`, `status`, `version`).
- **`POST /api/game/new`**: Stateless session initialization with preset character and deterministic seed.
- **`POST /api/game/step`**: Stateless transition step returning sanitized observations and updated state.
- **`POST /api/game/observe`**: Stateless state re-observation for turn undo, state inspection, and checkpointing.
- **`POST /api/game/replay`**: Pure deterministic trace verification executing action sequences and matching state hashes.
- **`GET /api/game/presets`**: Archetype catalogue and starting scene metadata.
- **`GET /api/game/quests`**: Continental campaign, 5 provincial subquests, and 5 faction intrigue quest lines.
- **`GET /api/game/hazards`**: Deterministic hazard combo definitions and status reactions.
- **`GET /api/game/codex`**: Ancient lore codex catalogue and provincial mastery specifications.
- **`GET /api/game/transit`**: Chartered continental transit network, route prerequisites, and player progress.
- **`GET /api/game/trade`**: Continental commodity manifest, trading hubs, import price bonuses, and trade progress.
- **`GET /api/game/weather`**: Continental weather dynamics, 12 atmospheric conditions, and provincial forecasts.
- **`GET /api/game/bounties`**: Continental mercenary contracts, 6 regional bounty boards, target scenes, and hunter rank progression.
- **`GET /api/game/companions`**: Provincial companion recruitment status, active follower, fellowship milestones, and companion roster.
- **`GET /api/game/bestiary`**: Continental apex beasts, lair scenes, weaknesses, trophies, and hunter rank progression.
- **`GET /api/game/survival`**: Continental survival foraging sites, campsite hearths, field cooking recipes, and survivalist rank progression.
- **`GET /api/game/orders`**: Provincial renown orders, sworn oaths, regional war banners, field morale auras, and Grand Marshal rank progression.
- **`GET /api/game/shrines`**: Continental ancient shrines, titan altars, divine celestial blessings, and pilgrim rank progression.
- **`GET /api/game/landmarks`**: Continental survey landmarks, overlook summits, regional terrain mastery, and cartographer rank progression.
- **`GET /api/game/vaults`**: Continental dungeon vaults, arcane keystones, delve masteries, and delver rank progression.
- **`POST /api/mcp` & `/mcp`**: JSON-RPC 2.0 Model Context Protocol endpoint for AI coding agents.

### Web UI Suite & Interactive Features
The browser player at `/` provides an immersive, action-first interface:
- **Interactive Quest Journal (`📜 Quests`, Key: `Q`):** 3-tab modal tracking the Five Seals of Sovereignty, 5 Provincial Narrative Chains, and 5 Faction Intrigue Arcs.
- **Continental Dungeon Vaults, Arcane Keystones & Ancient Crypt Raids (`🗝️ Vaults`, Key: `V`):** 6 Canonical Legendary Vaults situated at deep regional crypts and crossroads (Frost Titan Glacial Vault, Sunfire Serpent Tomb Vault, Abyssal Drowned Temple Vault, Palatine Ducal Treasury Vault, Harbor Bell Catacomb Vault, Grand Sovereign Under-Vault). Features 7-axis lock breach affordances (lockpicks, traits, attributes $\ge 14$, skills, stamina) granting unique Arcane Keystones and regional delve masteries (+3 stamina). Players can attune keystones anywhere in the field (+3 stamina), return to vault reliquaries to realign locking pins (+2 stamina), and advance through Delver Rank progression (Unproven Delver, Crypt Breacher, Tomb Raider, Vault Specialist, Master Infiltrator, Lord of Five Vaults, Grandmaster of Crypts) with a dedicated HUD modal and live vault counter.
- **Continental Survey Landmarks, Lookout Panoramas & Master Cartographer (`🔭 Landmarks`, Key: `L`):** 6 Canonical Apex Landmarks situated at regional overlook summits (Eagle Wing Pass Apex, Razor Dune Ridge Panorama, Drowned Shrine Vista, White Spire Parapet Zenith, Harbor Bell Tower Crow's Nest, Grand Crossroads Watchpost). Features 7-axis survey affordances (instruments, traits, attributes $\ge 14$, skills, or stamina exertion) granting unique topographical charts and regional terrain masteries (+3 stamina). Players can study charts anywhere in the field (+3 stamina), return to summit overlooks to re-triangulate and renew horizons (+2 stamina), and advance through Cartographer Rank progression (Uncharted Drifter, Regional Scout, Topographer, Continental Cartographer, Grand Surveyor, Master of Five Panoramas, Grand Royal Cartographer) with a dedicated HUD modal and live summit counter.
- **Continental Ancient Shrines & Titan Blessings (`🏛️ Shrines`, Key: `G`):** 6 Ancient Shrines (5 Provincial Titans + 1 Crossroads Pantheon) situated at regional sanctums (Shrine of Khoros, Altar of Sol-Ankh, Altar of Thalassa, Altar of Aurelius, Altar of Mara, Shrine of the Five Winds). Features 7-axis devotion offerings (item tributes, traits, attributes, or stamina) awarding unique divine Titan Blessings. Blessings can be invoked anywhere in the field to empower characters with celestial aura buffs (+4 stamina or health), with sanctum attunement renewals (+2 stamina) and Continental Pilgrim rank progression (Unanointed Wanderer, Shrine Pilgrim, Consecrated Devotee, Temple Hierophant, Provincial Exarch, Continental Hierarch, Avatar of the Five Titans).
- **Provincial Faction Heraldry, Renown Orders & Continental War Banners (`🛡️ Orders`, Key: `O`):** 5 Provincial Renown Orders (Order of the Iron Peak, Order of the Sunfire Sands, Order of the Salted River, Order of the Gilded Rose, Order of the Abyssal Trench) situated at regional council sanctums. Features 7-axis sworn oaths (reputation $\ge 5$, or attribute $\ge 14$, or faction traits) awarding unique provincial war banners. Banners can be raised anywhere in the field to grant enduring provincial battle morale auras restoring +3 stamina, alongside the Central Crossroads Heraldic Rally at the Great Bazaar (+5 stamina). Features dedicated HUD modal and Grand Marshal rank progression (Unsworn Wayfarer, Order Knight-Errant, Provincial Banneret, Continental Commander, High Faction Marshal, Grandmaster of the Five Realms).
- **Continental Province World Map Atlas (`🗺️ Map`, Key: `M`):** Interactive map showing active player location, regional mechanics, environmental hazard warnings, and transit connections across the 5 provinces and Central Bazaar.
- **Continental Survival Camping & Field Rations (`🏕️ Camp`, Key: `K`):** 15 wilderness foraging sites (3 per province) yielding edible ingredients (Frost Lichen, Dune Succulents, Marsh Parsley, Royal Truffles, Glow Mushrooms) and 6 regional campsite rest hearths for vitality recovery (+5 HP, +5 SP). Features 6 field recipes cooked over hearths (Highland Frost Stew, Sunfire Cured Jerky, Marsh Parsley Broth, Gilded Truffle Roast, Luminescent Grotto Mash, Continental Grand Feast) that grant unique survival markers, consumable anywhere in the field, with live Survivalist Rank tracking (Trail Wanderer, Camp Cook, Provincial Chef, Continental Master Forager).
- **Continental Bestiary & Apex Trophy Hunting System (`🦁 Bestiary`, Key: `H`):** 10 Continental Apex Beasts (2 per province) dwelling in remote wilderness lairs. Features dynamic anatomical study affordances that reveal weaknesses and reduce stamina costs, high-stakes apex hunts, unique trophy harvesting, Central Bazaar Menagerie mounting & inspection, and Hunter Rank progression (Novice Trapper, Provincial Tracker, Apex Hunter, Grandmaster Hunter, Continental Apex Slayer) with dedicated UI modal and live hunt counter.
- **Provincial Companion Recruiter & Follower Synergy System (`👥 Party`, Key: `P`):** 5 provincial companions (Kaelen Stonebreaker, Sariyah Dune-Walker, Bram the Smuggler, Lady Elenore of Veras, Tarek Deep-Delver) stationed at regional fortress courtyards. Features 7-axis recruitment requirements (attributes, traits, backgrounds, faction reputation, silver fee), dynamic field consultations, camp summoning at Central Bazaar & garrisons, dismissal mechanics, and Fellowship Milestones (Provincial Partner, Continental Warband, Master of the Fellowship) with dedicated modal and live party badge.
- **Chartered Continental Transit & Regional Caravan Network (`[TRANSIT]`):** 10 bidirectional routes linking Central Bazaar directly to the 5 provincial gateway fortresses (Highland Cable Lift, Canal River Barge, Desert Silt-Skiff, Imperial High Carriage, Submersible Siphon Ferry) reacting dynamically to character background, traits, equipment, and coinage, awarding the `Continental Wayfarer` milestone.
- **Continental Trade Economy & Regional Commodity Exchange (`[TRADE]`, Key: `T`):** 5 provincial trade goods (Highland Iron Ore, Aged Bog Whiskey, Sunfire Spice, Imperial Silk Bolt, Abyssal Pearl Essence) with supply-demand price arbitrage across 6 trading hubs. Features 7-axis barter alternatives and clan discounts, Merchant Consortium Recognition, and Master Trader milestones.
- **Continental Weather Dynamics & Provincial Micro-Climates (`⛅ Weather`, Key: `W`):** 12 deterministic atmospheric conditions cycling every 6 turns across the 5 provinces and Central Crossroads (e.g., Clear Alpine Air vs Blinding Blizzard in the Reach; Dusk Dune Chill vs Solar Heatwave in the Scorchwaste; Canal River Breeze vs Marsh Low Fog in the Lowlands). Dynamically synthesizes systemic environmental affordances (melt gathering, grotto shelter, shade rigging, marsh skulking) with turn cycle deduplication and live HUD weather badges.
- **Continental Mercenary Contract Board (`🎯 Bounties`, Key: `B`):** 10 provincial mercenary contracts (2 per province) available at regional gate fortresses and the Central Bazaar master board. Features a 3-phase lifecycle (Accept -> Hunt -> Claim) rewarding silver, rare gear, and faction reputation. Tracks Hunter Rank progression (Novice Drifter, Registered Bounty Hunter, Provincial Lawkeeper, Continental Master Hunter) with a dedicated modal, progress bar, and live HUD counter.
- **Session Auto-Save & Resume:** Automatically persists game state in browser `localStorage` across turns with an instant resume card on the character selection screen.
- **Real-Time Action Search (`🔍 Search`):** Dynamic instant text filtering for seamless navigation in scenes with 100+ legal actions.
- **7-Axis Character Sheet Modal (`📊 Sheet`, Key: `C`):** Full inspection of ancestry, background, attributes, skills, traits, flaws, active markers, and inventory.
- **Instant Turn Undo (`↩ Undo`, Key: `U`):** Stateless rollback stack to safely experiment with high-risk choices.
- **Deterministic Replay Verification (`📜 Replay`):** Export or paste JSON traces to verify bit-for-bit SHA-256 state matching in engine.
- **Tactical Combat Stances & Systemic Exploits (`[TACTICAL]`):** Dynamic stances (Aggressive, Guarded, Elusive, Focused) gated across 7-axis attributes, skills, traits, and flaws. Allows stance shifting, posture exploits (Brutal Strike, Brace Impact, Feint Maneuver, Spot Weakness), and stance drops with live HUD stance badges.
- **Master Field Crafting & Alchemical Synthesis (`[CRAFTING]`):** Deterministic recipe synthesis (lockpicks, torches, crowbar levers, filter masks, detox salves, waterproof pitch seals, climbing ropes, desert cowls, acid vials, and fire strikers) dynamically synthesized when holding required salvage, instantly unlocking downstream world affordances.
- **Continental Dynamic Event & World Calamities (`[SYSTEMIC]` / `[SOCIAL]`):** Turn-cyclical provincial incursions (Crag Tremor, Siphon Surge, Glass Tempest, Inquisitor Lockdown, Sluice Breach) challenging players with environmental threats and yielding dynamic mitigations that award crafting salvage and unlock safe passage.
- **Continental Ancient Lore Codex & Relic Deciphering Engine (`[CODEX]`, Key: `X`):** 15 ancient lore codices (3 per province across 5 provinces) situated at historical sanctums and shrines. Deciphering relics leverages 7-axis traits, skills, and tools to unlock rich Hemingway lore excerpts, and mastering all 3 relics in a province awards prestigious provincial lore masteries (Reach Archivist, Lowlands Chronicler, Dune Antiquarian, Court Historian, Abyssal Scholar).
- **Hotkeys:** `1`–`9` (action selection), `Q` (quest journal), `P` (party & companions), `H` (bestiary & apex hunts), `K` (survival camp & foraging), `O` (faction orders & war banners), `G` (ancient shrines & divine blessings), `L` (survey landmarks & panoramas), `V` (dungeon vaults & crypt keystones), `X` (ancient codex), `T` (commodity exchange), `W` (weather forecast), `B` (mercenary contracts), `M` (continental map), `C` (character sheet), `U` (undo), `Escape` (close modals).

### CLI Player Features & Deterministic Replay
```bash
# Interactive play with 7-axis sheet ('sheet'), quest log ('quest'), companions ('party'), bestiary ('hunt'), survival camp ('camp'/'cook'/'rations'), orders ('orders'/'banners'), shrines ('shrines'/'blessings'), codex ('codex'), trade ('trade'), weather ('weather'), bounties ('bounties'), and undo ('u')
python3 -m adventure_forge.player.cli [preset]

# Replay and verify an action trace bit-for-bit
python3 -m adventure_forge.player.cli --replay '{"preset":"cutpurse","seed":42,"actions":["flash_thief_signet"]}'
```

### Local Development Preview
```bash
npx vercel dev
```

### Git Automatic Push
The repository includes an active post-commit hook in `.githooks/post-commit` configured via `core.hooksPath`. Whenever any commit is made, it is automatically pushed to `origin/main`.

