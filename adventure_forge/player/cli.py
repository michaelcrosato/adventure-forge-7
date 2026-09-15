"""Player Interface CLI (Interactive Terminal Runner).

Enforces:
- G2 / G5: Action-first display, concise observation, legal verb list.
- I6: Information Firewall — player sees only player-safe observations.
- I8: Observation budget with clean pagination for large action sets.
"""
import json
import sys
from typing import Tuple, Optional, Dict, Any, List
from adventure_forge.core.character import get_preset
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.trade import COMMODITIES, TRADE_HUBS
from adventure_forge.core.weather import get_weather_for_region


def render_character_sheet(state: GameState) -> None:
    """Display full 7-axis character state vector."""
    c = state.character
    print("\n" + "=" * 65)
    print(f" CHARACTER SHEET: {c.name.upper()} ({c.ancestry} • {c.background})")
    print("=" * 65)
    print(f" Health: {c.health}/{c.max_health} | Stamina: {c.stamina}/{c.max_stamina}")
    print("\n [ATTRIBUTES]")
    for attr, val in sorted(c.attributes.items()):
        print(f"   {attr.capitalize():14s}: {val}")
    print("\n [SKILLS]")
    for skill, val in sorted(c.skills.items()):
        print(f"   {skill.capitalize():14s}: {val}")
    print(f"\n [TRAITS]  ({len(c.traits)}): {', '.join(c.traits) if c.traits else 'None'}")
    print(f" [FLAWS]   ({len(c.flaws)}): {', '.join(c.flaws) if c.flaws else 'None'}")
    print(f" [MARKERS] ({len(c.markers)}): {', '.join(c.markers) if c.markers else 'None'}")
    print("\n [FACTION REPUTATION]")
    if c.reputation:
        for faction, rep in sorted(c.reputation.items()):
            sign = "+" if rep > 0 else ""
            print(f"   {faction.replace('_', ' ').capitalize():18s}: {sign}{rep}")
    else:
        print("   Neutral with all factions.")
    print(f"\n [INVENTORY] ({len(c.inventory)} items):")
    if c.inventory:
        for item in sorted(c.inventory):
            print(f"   • {item}")
    else:
        print("   (Empty)")
    print("=" * 65 + "\n")


def render_quest_log(quest_info: Dict[str, Any]) -> None:
    """Display comprehensive continental and provincial quest progress."""
    print("\n" + "=" * 65)
    print(" QUEST LOG: CONTINENTAL CAMPAIGN & PROVINCIAL SUBQUESTS")
    print("=" * 65)
    active_stg = quest_info.get("active_stage", "None")
    is_fin = quest_info.get("is_finished", False)
    comp_stages = quest_info.get("completed_stages", [])
    print(" Main Campaign: The Five Seals of Sovereignty")
    print(f" Status       : {'COMPLETED' if is_fin else f'Active Stage -> {active_stg}'}")
    print(f" Seals Won    : {len(comp_stages)}/5 ({', '.join(comp_stages) if comp_stages else 'None'})")

    subquests = quest_info.get("subquests", {})
    if subquests:
        print("\n [PROVINCIAL SUBQUESTS]")
        for qid, qprog in sorted(subquests.items()):
            q_name = qid.replace("subquest_", "").replace("quest_", "").replace("_", " ").title()
            if qprog.get("is_finished"):
                print(f"   • {q_name:32s}: [COMPLETED]")
            elif qprog.get("active_stage"):
                print(f"   • {q_name:32s}: Stage -> {qprog['active_stage']}")
            else:
                print(f"   • {q_name:32s}: [Undiscovered]")

    intrigue = quest_info.get("intrigue_quests", {})
    if intrigue:
        print("\n [FACTION INTRIGUE ARCS]")
        for qid, qprog in sorted(intrigue.items()):
            q_name = qid.replace("subquest_", "").replace("quest_", "").replace("_", " ").title()
            if qprog.get("is_finished"):
                ending = f" ({qprog['ending']})" if qprog.get("ending") else ""
                print(f"   • {q_name:32s}: [RESOLVED]{ending}")
            elif qprog.get("active_stage"):
                print(f"   • {q_name:32s}: Stage -> {qprog['active_stage']}")
            else:
                print(f"   • {q_name:32s}: [Undiscovered]")
    print("=" * 65 + "\n")


def render_continental_map(state: GameState) -> None:
    """Display ASCII schematic of the 5 provinces and Central Bazaar."""
    reg = state.current_region
    print("\n" + "=" * 65)
    print(" CONTINENTAL ATLAS: THE FIVE PROVINCES")
    print("=" * 65)

    provinces = [
        ("The Reach", ["province_reach", "iron_crags"], "Highland peaks. Verticality & climbing stamina."),
        ("The High Court", ["province_high_court", "high_court_local"], "Imperial halls. Court intrigue & noble decorum."),
        ("The Grand Bazaar", ["stress_market"], "Continental crossroads. Unbounded choice market hub."),
        ("The Sunken Hollows", ["province_sunken_hollows", "sunken_hollows_local"], "Flooded grottos. Underwater diving & pressure."),
        ("The Lowlands", ["province_lowlands", "lower_warrens"], "Canal warrens. Social stealth & suspicion."),
        ("The Scorchwaste", ["province_scorchwaste", "scorchwaste_local"], "Arid desert. Heat survival & hydration."),
    ]

    for name, regions, desc in provinces:
        is_here = reg in regions
        badge = " [YOU ARE HERE]" if is_here else ""
        print(f"\n  • {name.upper()}{badge}")
        print(f"    Mechanic: {desc}")

    print("\n [CHARTERED CONTINENTAL TRANSIT]")
    routes = [
        ("Highland Cable Lift", "The Reach", "route_reach"),
        ("Canal River Barge", "The Lowlands", "route_lowlands"),
        ("Desert Silt-Skiff", "The Scorchwaste", "route_scorchwaste"),
        ("Imperial High Carriage", "The High Court", "route_high_court"),
        ("Submersible Siphon Ferry", "The Sunken Hollows", "route_sunken_hollows"),
    ]
    for r_name, r_prov, r_flag in routes:
        status = "[TRAVELED]" if state.world_flags.get(r_flag) else "[AVAILABLE]"
        print(f"   • {r_name:24s} -> {r_prov:20s}: {status}")

    if state.world_flags.get("continental_wayfarer_unlocked"):
        print("\n [CONTINENTAL MILESTONE]")
        print("   • Continental Wayfarer: Traveled all five chartered routes across the realm!")

    print("\n" + "=" * 65 + "\n")


def render_codex_log(codex_info: Dict[str, Any]) -> None:
    """Display ancient lore codex inscriptions and provincial masteries."""
    disc_count = codex_info.get("discovered_count", 0)
    total_count = codex_info.get("total_entries", 15)
    print("\n" + "=" * 65)
    print(f" ANCIENT CODEX & RELIC ARCHIVES ({disc_count} / {total_count} DISCOVERED)")
    print("=" * 65)

    prog = codex_info.get("province_progress", {})
    if prog:
        print("\n [PROVINCIAL DISCOVERY]")
        for p_key, p_data in prog.items():
            status = "[MASTERED]" if p_data.get("mastery_unlocked") else f"{p_data.get('discovered', 0)} / {p_data.get('total', 3)}"
            print(f"   • {p_data.get('title', p_key):24s}: {status}")

    entries = codex_info.get("entries", [])
    unlocked = [e for e in entries if e.get("unlocked")]
    if unlocked:
        print("\n [DISCOVERED INSCRIPTIONS]")
        for e in unlocked:
            print(f"   • [{e['province']}] {e['title']} ({e['category']})")
            print(f"     Location : {e['scene_id']}")
            print(f"     Lore     : \"{e.get('lore_text', '')}\"")
    else:
        print("\n [DISCOVERED INSCRIPTIONS]")
        print("   No ancient inscriptions deciphered yet. Search provincial sanctums.")

    masteries = codex_info.get("masteries_unlocked", [])
    if masteries:
        print("\n [PROVINCIAL MASTERIES]")
        for m in masteries:
            print(f"   • {m['title']}: {m['description']}")

    print("=" * 65 + "\n")


def render_trade_market(state: GameState, engine: AdventureEngine) -> None:
    """Display continental trade commodities, cargo held, and merchant progress."""
    prog = engine.get_trade_progress(state)
    held = prog.get("commodities_held", [])
    trades = prog.get("completed_trades", 0)
    arbitrage = prog.get("arbitrage_completed", 0)
    hubs = prog.get("hubs_visited", [])

    print("\n" + "=" * 65)
    print(f" CONTINENTAL COMMODITY EXCHANGE ({trades} Trades, {arbitrage} Arbitrage)")
    print("=" * 65)

    print("\n [CARGO IN INVENTORY]")
    if held:
        for cid in held:
            comm = COMMODITIES.get(cid)
            name = comm.name if comm else cid
            print(f"   • {name} ({cid})")
    else:
        print("   No trade commodities currently held.")

    print("\n [PROVINCIAL TRADING HUBS VISITED]")
    for hub_id, hub_data in TRADE_HUBS.items():
        status = "[TRADED]" if hub_id in hubs else "[UNVISITED]"
        print(f"   • {hub_data['hub_name']:28s}: {status}")

    print("\n [MERCHANT RECOGNITION]")
    consortium = "[RECOGNIZED]" if prog.get("is_consortium_recognized") else "[LOCKED] (Trade at 3+ hubs)"
    master = "[ACHIEVED]" if prog.get("is_master_trader") else "[LOCKED] (Trade all 5 commodities + 2 arbitrage)"
    print(f"   • Merchant Consortium Status : {consortium}")
    print(f"   • Master Trader Milestone    : {master}")
    print("=" * 65 + "\n")


def render_weather_forecast(state: GameState, engine: AdventureEngine) -> None:
    """Display current continental weather conditions across all provinces."""
    forecast = engine.get_weather_forecast(state)
    local = engine.get_weather_state(state)

    print("\n" + "=" * 65)
    print(f" CONTINENTAL WEATHER FORECAST (Turn {state.turn_count})")
    print("=" * 65)
    print(f"\n [LOCAL ATMOSPHERE: {local['name'].upper()}]")
    print(f"   {local['description']}")

    print("\n [PROVINCIAL CLIMATE FORECAST]")
    for prov, w in forecast.items():
        hazard = f" [{w['hazard_type'].upper()}]" if w.get("hazard_type") else ""
        print(f"   • {prov:20s}: {w['name']}{hazard}")
        print(f"     \"{w['description']}\"")
    print("=" * 65 + "\n")


def render_bounty_board(state: GameState, engine: AdventureEngine) -> None:
    """Display continental mercenary contract board and hunter progress."""
    prog = engine.get_bounty_progress(state)
    print("\n" + "=" * 65)
    print(f" CONTINENTAL MERCENARY CONTRACT BOARD ({prog['rank_title']})")
    print("=" * 65)
    print(f"\n Progress: {prog['completed_count']}/{prog['total_contracts']} Contracts Cleared | Active Hunts: {prog['accepted_count'] + prog['hunted_count']}")

    contracts = prog.get("contracts", {})
    for cid, c in contracts.items():
        if c["is_completed"]:
            status_tag = "[CLAIMED ✓]"
        elif c["is_hunted"]:
            status_tag = "[HUNTED - READY]"
        elif c["is_accepted"]:
            status_tag = "[ACTIVE HUNT]"
        else:
            status_tag = "[OPEN CONTRACT]"
        print(f"\n {status_tag} {c['name']} ({c['province']})")
        print(f"   Target: {c['target_scene']} | Hub: {c['hub_scene']}")
        print(f"   Reward: {c['reward_silver']} Silver + {c['reward_item']} (+{c['reputation_value']} {c['reputation_faction']})")
        print(f"   \"{c['description']}\"")
    print("=" * 65 + "\n")


def render_companion_roster(state: GameState, engine: AdventureEngine) -> None:
    """Display recruited continental warband companions and active follower."""
    prog = engine.get_companion_progress(state)
    print("\n" + "=" * 65)
    print(f" CONTINENTAL WARBAND FELLOWSHIP ({prog['rank_title']})")
    print("=" * 65)
    print(f"\n Recruited: {prog['recruited_count']}/{prog['total_companions']} Companions | Active Follower: {prog['active_companion_name']} ({prog['active_companion_perk']})")

    comps = prog.get("companions", {})
    for cid, c in comps.items():
        if c["is_active"]:
            status_tag = "[ACTIVE FOLLOWER ★]"
        elif c["is_recruited"]:
            status_tag = "[RECRUITED ✓]"
        else:
            status_tag = "[AVAILABLE IN PROVINCE]"
        print(f"\n {status_tag} {c['name']} — {c['title']} ({c['province']})")
        print(f"   Home: {c['home_scene']} | Perk: {c['perk_name']} ({c['perk_description']})")
        print(f"   \"{c['description']}\"")
    print("=" * 65 + "\n")


def render_bestiary_log(state: GameState, engine: AdventureEngine) -> None:
    """Display continental apex bestiary, trophies held, and hunter rank."""
    prog = engine.get_bestiary_progress(state)
    hunted = prog.get("hunted_count", 0)
    studied = prog.get("studied_count", 0)
    mounted = prog.get("mounted_count", 0)
    total = prog.get("total_beasts", 10)
    rank = prog.get("rank_title", "Novice Trapper")

    print("\n" + "=" * 65)
    print(f" CONTINENTAL APEX BESTIARY ({hunted} / {total} Slain | Rank: {rank})")
    print("=" * 65)
    print(f" Studied Anatomies: {studied}/{total} | Trophies Mounted: {mounted}/{total}")
    print("\n [APEX BEASTS]")
    beasts = prog.get("beasts", {})
    for bid, b in beasts.items():
        if b.get("is_hunted"):
            status = "🏆 SLAIN"
        elif b.get("is_studied"):
            status = "🔍 STUDIED"
        else:
            status = "❓ UNKNOWN"

        trophy_info = f" [Trophy: {b.get('trophy_name')}]" if (b.get("has_trophy") or b.get("is_mounted")) else ""
        print(f"   • [{b.get('province')}] {b.get('name')}: {status}{trophy_info}")
        print(f"     Title   : {b.get('title')}")
        print(f"     Lair    : {b.get('lair_scene')}")
        if b.get("is_studied") or b.get("is_hunted"):
            print(f"     Weakness: {b.get('weakness')}")
            print(f"     Perk    : {b.get('trophy_perk')}")
    print("=" * 65 + "\n")


def render_survival_camp(state: GameState, engine: AdventureEngine) -> None:
    """Display survival foraging, campfire recipes, and rations held."""
    prog = engine.get_survival_progress(state)
    foraged = prog.get("foraged_count", 0)
    total_spots = prog.get("total_spots", 15)
    meals = prog.get("meals_cooked", 0)
    rank = prog.get("rank_title", "Trail Wanderer")

    print("\n" + "=" * 65)
    print(f" SURVIVAL CAMP & FORAGING ({meals} Meals Cooked | Rank: {rank})")
    print("=" * 65)
    print(f" Foraging Sites Harvested: {foraged} / {total_spots}")
    print("\n [FIELD COOKING RECIPES]")
    recipes = prog.get("recipes", {})
    for rid, r in recipes.items():
        cook_status = "[CAN COOK]" if r.get("can_cook") else "[NEED INGREDIENTS]"
        held = r.get("count_held", 0)
        held_str = f" ({held} In Pack)" if held > 0 else ""
        print(f"   • [{r.get('province')}] {r.get('name')}: {cook_status}{held_str}")
        print(f"     Requires : {', '.join(r.get('required_ingredients', []))}")
        print(f"     Benefits : +{r.get('stamina_restored', 0)} SP, +{r.get('health_restored', 0)} HP")
        if r.get("granted_marker"):
            print(f"     Perk     : {r.get('granted_marker')}")
    print("=" * 65 + "\n")


def render_orders_log(state: GameState, engine: AdventureEngine) -> None:
    """Display provincial faction renown orders, pledged fealties, and war banners."""
    prog = engine.get_orders_progress(state)
    pledged = prog.get("pledged_count", 0)
    total = prog.get("total_orders", 5)
    banners = prog.get("banners_held", 0)
    rank = prog.get("rank_title", "Unsworn Wayfarer")
    active_marker = prog.get("active_banner_marker")

    print("\n" + "=" * 65)
    print(f" CONTINENTAL HERALDRY & RENOWN ORDERS ({banners}/{total} Banners | Rank: {rank})")
    print("=" * 65)
    print(f" Orders Sworn: {pledged} / {total}")
    if active_marker:
        print(f" Active War Banner Aura: {active_marker}")
    print("\n [PROVINCIAL FACTION ORDERS]")
    orders = prog.get("orders", {})
    for oid, o in orders.items():
        pledge_status = "[PLEDGED]" if o.get("is_pledged") else "[UNSWORN]"
        banner_status = "[HELD IN PACK]" if o.get("has_banner") else "[NO BANNER]"
        raised_str = " (RAISED)" if o.get("is_raised") else ""
        print(f"   • {o.get('crest_icon')} [{o.get('province')}] {o.get('name')}: {pledge_status} | {banner_status}{raised_str}")
        print(f"     Sanctum : {o.get('sanctum_scene')}")
        print(f"     Banner  : {o.get('banner_name')}")
        print(f"     Perk    : {o.get('granted_marker')}")
    print("=" * 65 + "\n")


def render_shrines_log(state: GameState, engine: AdventureEngine) -> None:
    """Display continental ancient shrines, consecrated altars, and divine blessings."""
    prog = engine.get_shrines_progress(state)
    consecrated = prog.get("consecrated_count", 0)
    total = prog.get("total_shrines", 6)
    rank = prog.get("pilgrim_rank", "Unanointed Wanderer")
    active_blessings = prog.get("active_blessings_count", 0)
    active_auras = prog.get("active_auras_count", 0)

    print("\n" + "=" * 65)
    print(f" CONTINENTAL SHRINES & TITAN BLESSINGS ({consecrated}/{total} Consecrated | Rank: {rank})")
    print("=" * 65)
    print(f" Active Blessings: {active_blessings} | Active Invocations: {active_auras}")
    print(f" Pilgrim Status  : {prog.get('rank_desc', '')}")
    print("\n [ANCIENT SHRINES & ALTARS]")
    shrines = prog.get("shrines", [])
    for s in shrines:
        status_str = "[CONSECRATED]" if s.get("is_consecrated") else "[UNCONSECRATED]"
        bless_str = " (BLESSING HELD)" if s.get("has_blessing") else ""
        inv_str = " [AURA ACTIVE]" if s.get("is_aura_active") else (" [INVOKED]" if s.get("is_invoked") else "")
        print(f"   • {s.get('icon')} [{s.get('province')}] {s.get('name')}: {status_str}{bless_str}{inv_str}")
        print(f"     Deity    : {s.get('deity')}")
        print(f"     Domain   : {s.get('domain')}")
        print(f"     Sanctum  : {s.get('sanctum_scene')}")
        print(f"     Blessing : {s.get('blessing_name')}")
    print("=" * 65 + "\n")


def render_landmarks_log(state: GameState, engine: AdventureEngine) -> None:
    """Display continental survey landmarks, overlook panoramas, and cartographer rank."""
    prog = engine.get_landmarks_progress(state)
    surveyed = prog.get("surveyed_count", 0)
    total = prog.get("total_landmarks", 6)
    rank = prog.get("cartographer_rank", "Uncharted Drifter")
    active_charts = prog.get("active_charts_count", 0)
    active_masteries = prog.get("active_masteries_count", 0)

    print("\n" + "=" * 65)
    print(f" CONTINENTAL SURVEY LANDMARKS ({surveyed}/{total} Surveyed | Rank: {rank})")
    print("=" * 65)
    print(f" Active Charts: {active_charts} | Regional Masteries: {active_masteries}")
    print(f" Cartographer Status: {prog.get('rank_desc', '')}")
    print("\n [APEX PANORAMAS & LOOKOUT SUMMITS]")
    landmarks = prog.get("landmarks", [])
    for lm in landmarks:
        status_str = "[SURVEYED]" if lm.get("is_surveyed") else "[UNCHARTED]"
        chart_str = " (CHART HELD)" if lm.get("has_chart") else ""
        mast_str = " [TERRAIN MASTERY]" if lm.get("has_mastery") else ""
        stud_str = " [STUDIED]" if lm.get("is_studied") else ""
        print(f"   • {lm.get('icon')} [{lm.get('province')}] {lm.get('name')}: {status_str}{chart_str}{stud_str}{mast_str}")
        print(f"     Summit   : {lm.get('overlook_scene')}")
        print(f"     Domain   : {lm.get('domain')}")
        print(f"     Tool     : {lm.get('required_tool')}")
    print("=" * 65 + "\n")


def render_history(state: GameState) -> None:
    """Display turn-by-turn history of actions and recent events."""
    print("\n" + "=" * 65)
    print(f" ACTION & EVENT HISTORY ({len(state.history)} steps, Turn {state.turn_count})")
    print("=" * 65)
    if not state.history:
        print("  No actions taken yet.")
    else:
        for idx, act in enumerate(state.history, start=1):
            print(f"  Turn {idx:2d}: {act}")
    if state.event_log:
        print("\n [RECENT EVENTS]")
        for ev in state.event_log[-5:]:
            print(f"  • {ev}")
    print("=" * 65 + "\n")


def render_ui(
    obs,
    page: int = 0,
    page_size: int = 15,
    state: Optional[GameState] = None,
    quest_info: Optional[Dict[str, Any]] = None
):
    """Render a clean, high-velocity, action-first player screen with categorized pagination."""
    print("\n" + "=" * 65)
    print(f" {obs.title.upper()}  [{obs.region_id}]")
    if state:
        c = state.character
        status_str = f" | Status: {', '.join(c.markers)}" if c.markers else " | Status: Normal"
        items_str = f" | Items: {len(c.inventory)}"
        w = get_weather_for_region(state.turn_count, state.current_region)
        print(f" HP: {c.health}/{c.max_health} | SP: {c.stamina}/{c.max_stamina}{status_str}{items_str} | Weather: {w.name}")
    if quest_info:
        active_stg = quest_info.get("active_stage", "Exploring Continent")
        print(f" Quest: {active_stg}")
    print("=" * 65)
    print(f"\n{obs.description}\n")

    if obs.events:
        print("EVENTS:")
        for ev in obs.events:
            print(f"  • {ev}")
        print()

    total_actions = len(obs.legal_actions)
    total_pages = max(1, (total_actions + page_size - 1) // page_size)
    page = max(0, min(page, total_pages - 1))
    start_idx = page * page_size
    end_idx = min(start_idx + page_size, total_actions)
    page_actions = obs.legal_actions[start_idx:end_idx]

    if total_actions == 0:
        print("AVAILABLE ACTIONS (0 total | Page 1 of 1):")
        print("  No actions available.")
    else:
        print(f"AVAILABLE ACTIONS ({total_actions} total | Page {page + 1} of {total_pages} | Showing {start_idx + 1}-{end_idx}):")
        current_cat = None
        for i, act in enumerate(page_actions, start=start_idx + 1):
            cat = act.get("category", "interaction").replace("_", " ").upper()
            if cat != current_cat:
                current_cat = cat
                print(f"\n  [{current_cat}]")
            risk_str = f" [{act['risk'].upper()}]" if act.get('risk') and act['risk'] != 'low' else ""
            cost_str = f" (Stamina -{act['stamina_cost']})" if act.get('stamina_cost', 0) > 0 else ""
            print(f"    [{i:3d}] {act['label']}{risk_str}{cost_str}")

    print("-" * 65)
    nav_hints = []
    if page + 1 < total_pages:
        nav_hints.append("'n' for next page")
    if page > 0:
        nav_hints.append("'p' for prev page")
    if total_pages > 1:
        nav_hints.append("'page <num>' to jump")
    nav_hints.append("'sheet' for stats")
    nav_hints.append("'quest' for log")
    nav_hints.append("'codex' for lore")
    nav_hints.append("'trade' for market")
    nav_hints.append("'weather' for climate")
    nav_hints.append("'bounty' for contracts")
    nav_hints.append("'party' for companions")
    nav_hints.append("'hunt' for bestiary")
    nav_hints.append("'camp' for survival")
    nav_hints.append("'orders' for banners")
    nav_hints.append("'shrines' for blessings")
    nav_hints.append("'landmarks' for panoramas")
    nav_hints.append("'map' for atlas")
    if state and state.turn_count > 0:
        nav_hints.append("'u' to undo")
    nav_hints.append("'q' to quit")
    print("Commands: " + ", ".join(nav_hints))


def start_new_game(char_preset: str = "cutpurse") -> Tuple[AdventureEngine, GameState]:
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    try:
        preset = get_preset(char_preset)
    except KeyError:
        preset = get_preset("warrior")

    state = GameState(
        build_id="af-build-001",
        session_id=f"cli-session-{preset.id}",
        character=preset.character,
        current_region=preset.start_region,
        current_scene=preset.start_scene,
        rng=DeterministicRNG.from_seed(999)
    )

    return engine, state


def execute_replay(
    replay_data: Dict[str, Any],
    engine: Optional[AdventureEngine] = None,
) -> Tuple[GameState, Any, List[str]]:
    """Deterministically execute an action trace and return final state, obs, and fingerprints."""
    if engine is None:
        registry = build_world_registry()
        engine = AdventureEngine(registry)

    preset_name = str(replay_data.get("preset", "cutpurse"))
    seed = int(replay_data.get("seed", 42))
    actions = replay_data.get("actions", replay_data.get("history", []))

    try:
        preset = get_preset(preset_name)
    except KeyError:
        preset = get_preset("cutpurse")

    state = GameState(
        build_id="af-build-001",
        session_id=f"cli-replay-{preset.id}-{seed}",
        character=preset.character,
        current_region=preset.start_region,
        current_scene=preset.start_scene,
        rng=DeterministicRNG.from_seed(seed),
    )
    obs = engine.observe(state)
    fingerprints = [state.fingerprint()]

    for act_id in actions:
        state, obs = engine.step(state, str(act_id))
        fingerprints.append(state.fingerprint())
        if not obs.success or obs.is_terminal:
            break

    return state, obs, fingerprints


def main():
    import os
    if len(sys.argv) > 1 and sys.argv[1] == "--replay":
        if len(sys.argv) < 3:
            print("Usage: python3 -m adventure_forge.player.cli --replay <replay.json>")
            sys.exit(1)
        src = sys.argv[2]
        if os.path.exists(src):
            with open(src, "r", encoding="utf-8") as f:
                replay_payload = json.load(f)
        else:
            replay_payload = json.loads(src)

        registry = build_world_registry()
        engine = AdventureEngine(registry)
        state, obs, fps = execute_replay(replay_payload, engine)

        print("\n" + "=" * 65)
        print(" ADVENTUREFORGE DETERMINISTIC REPLAY EXECUTION")
        print("=" * 65)
        print(f" Preset           : {replay_payload.get('preset', 'cutpurse')}")
        print(f" Seed             : {replay_payload.get('seed', 42)}")
        print(f" Executed Steps   : {state.turn_count}")
        print(f" Final Scene      : {state.current_scene} [{state.current_region}]")
        print(f" Final SHA-256    : {state.fingerprint()}")
        expected_fp = replay_payload.get("fingerprint")
        if expected_fp:
            matches = (expected_fp == state.fingerprint())
            status_text = "BIT-FOR-BIT IDENTICAL ✓" if matches else f"MISMATCH (expected {expected_fp})"
            print(f" Fingerprint Match: {status_text}")
        print("=" * 65 + "\n")

        if obs.is_terminal:
            print(f"*** OUTCOME REACHED: {obs.outcome or 'JOURNEY CONCLUDED'} ***\n")
            return
        preset = str(replay_payload.get("preset", "cutpurse"))
    else:
        preset = sys.argv[1] if len(sys.argv) > 1 else "cutpurse"
        engine, state = start_new_game(preset)
        obs = engine.observe(state)

    state_history: List[GameState] = [state]
    page = 0
    page_size = 15

    while True:
        quest_info = engine.get_quest_progress(state)
        render_ui(obs, page=page, page_size=page_size, state=state, quest_info=quest_info)
        try:
            choice = input("\nChoose action [number or command]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting AdventureForge.")
            break

        if choice in ("q", "quit", "exit"):
            print("Session ended.")
            break
        elif choice in ("sheet", "c", "stats"):
            render_character_sheet(state)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("quest", "quests", "log"):
            render_quest_log(quest_info)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("codex", "relics", "lore", "x"):
            codex_info = engine.get_codex_progress(state)
            render_codex_log(codex_info)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("map", "m", "atlas"):
            render_continental_map(state)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("trade", "t"):
            render_trade_market(state, engine)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("weather", "w"):
            render_weather_forecast(state, engine)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("bounties", "bounty", "b"):
            render_bounty_board(state, engine)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("party", "companions", "comp", "fellowship"):
            render_companion_roster(state, engine)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("hunt", "bestiary", "beasts", "trophy", "trophies", "h"):
            render_bestiary_log(state, engine)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("camp", "camping", "cook", "cooking", "rations", "survival", "k"):
            render_survival_camp(state, engine)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("orders", "order", "banners", "banner", "heraldry", "o"):
            render_orders_log(state, engine)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("shrines", "shrine", "blessings", "blessing", "altars", "altar", "g"):
            render_shrines_log(state, engine)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("landmarks", "landmark", "panoramas", "panorama", "survey", "l"):
            render_landmarks_log(state, engine)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("history", "hist"):
            render_history(state)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("u", "undo"):
            if len(state_history) > 1:
                state_history.pop()
                state = state_history[-1]
                obs = engine.observe(state)
                page = 0
                print(f"\n[✓] Turn undone. Reverted to Turn {state.turn_count}.")
            else:
                print("\n[!] Already at initial state; cannot undo further.")
            continue
        elif choice == "export":
            export_payload = {
                "preset": preset,
                "turn_count": state.turn_count,
                "history": list(state.history),
                "fingerprint": state.fingerprint(),
            }
            print("\n[Deterministic Replay Payload]:")
            print(json.dumps(export_payload, indent=2))
            input("\nPress Enter to return to action screen...")
            continue
        elif choice == "n":
            total_pages = max(1, (len(obs.legal_actions) + page_size - 1) // page_size)
            if page + 1 < total_pages:
                page += 1
            else:
                print("Already on last page.")
            continue
        elif choice == "p":
            if page > 0:
                page -= 1
            else:
                print("Already on first page.")
            continue
        elif choice.startswith("page ") or choice.startswith("goto "):
            parts = choice.split()
            if len(parts) == 2 and parts[1].isdigit():
                target_page = int(parts[1]) - 1
                total_pages = max(1, (len(obs.legal_actions) + page_size - 1) // page_size)
                if 0 <= target_page < total_pages:
                    page = target_page
                else:
                    print(f"Page must be between 1 and {total_pages}.")
            else:
                print("Usage: page <number> or goto <number>")
            continue

        if not choice.isdigit():
            # Check if user entered action id directly
            matches = [a for a in obs.legal_actions if a["id"] == choice]
            if matches:
                selected_action_id = matches[0]["id"]
            else:
                print(f"Invalid input '{choice}'. Enter a number from the action list, or 'sheet' / 'quest' / 'u'.")
                continue
        else:
            num = int(choice)
            if 1 <= num <= len(obs.legal_actions):
                selected_action_id = obs.legal_actions[num - 1]["id"]
            else:
                print(f"Choice {num} out of bounds (1..{len(obs.legal_actions)}).")
                continue

        state, obs = engine.step(state, selected_action_id)
        if obs.success:
            state_history.append(state)
        page = 0  # Reset page on state transition

        if obs.is_terminal:
            final_quest = engine.get_quest_progress(state)
            render_ui(obs, page=page, page_size=page_size, state=state, quest_info=final_quest)
            print(f"\n*** OUTCOME REACHED: {obs.outcome or 'JOURNEY CONCLUDED'} ***\n")
            break


if __name__ == "__main__":
    main()
