"""Region 6: The Grand Bazaar (Unbounded Choice Stress Scene).

Implements G6 / SYS-05 requirement:
Supports 100+ distinct legal actions in a single scene without crash, truncation, or slowdown.
"""
from typing import List
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action


def build_stress_market_region() -> RegionManifest:
    scenes = {}

    stress_actions: List[Action] = []

    # 1. Major region transitions
    stress_actions.append(Action(
        id="travel_to_warrens",
        label="Go to Warrens",
        category="movement",
        target_scene="warrens_alley",
        result_text="You slip down the cobblestones into the low alleys.",
        risk="low"
    ))
    stress_actions.append(Action(
        id="travel_to_crags",
        label="Climb to Crags",
        category="movement",
        target_scene="crags_base",
        result_text="You head toward the looming mountain trail.",
        risk="low"
    ))
    stress_actions.append(Action(
        id="travel_to_scorchwaste",
        label="Trek to Dunes",
        category="movement",
        target_scene="scorch_dunes",
        result_text="You pass through the sun gate into the open sands.",
        risk="medium"
    ))
    stress_actions.append(Action(
        id="travel_to_court",
        label="Enter High Court",
        category="movement",
        target_scene="court_antechamber",
        result_text="You walk up the marble staircase of the justice hall.",
        risk="low"
    ))
    stress_actions.append(Action(
        id="travel_to_hollows",
        label="Descend to Grotto",
        category="movement",
        target_scene="hollows_grotto",
        result_text="You take the wet steps down to the underground grotto.",
        risk="low"
    ))

    # 2. 30 Distinct Merchant Stalls
    merchants = [
        ("spices", "Inspect spice cart"),
        ("silk", "Inspect silk bales"),
        ("iron", "Inspect iron tools"),
        ("pottery", "Inspect clay jars"),
        ("gems", "Inspect cut gems"),
        ("parchment", "Inspect rare inks"),
        ("leather", "Inspect raw hides"),
        ("herbs", "Inspect dried herbs"),
        ("brass", "Inspect brass lamps"),
        ("weapons", "Inspect steel daggers"),
        ("armor", "Inspect chain mail"),
        ("carpets", "Inspect wool rugs"),
        ("bread", "Inspect fresh loaves"),
        ("fruit", "Inspect sweet dates"),
        ("wine", "Inspect vintage flasks"),
        ("relics", "Inspect copper icons"),
        ("timber", "Inspect cedar planks"),
        ("dyes", "Inspect crimson powders"),
        ("oils", "Inspect lamp oils"),
        ("glass", "Inspect colored vials"),
        ("poultices", "Inspect herbal salves"),
        ("furs", "Inspect wolf pelts"),
        ("tallow", "Inspect wax tapers"),
        ("salt", "Inspect rock salt"),
        ("pitch", "Inspect pitch buckets"),
        ("cordage", "Inspect braided cords"),
        ("flint", "Inspect strike stones"),
        ("tinkering", "Inspect clock gears"),
        ("tomes", "Inspect bound ledgers"),
        ("charms", "Inspect bone charms"),
    ]
    for m_id, m_label in merchants:
        stress_actions.append(Action(
            id=f"inspect_{m_id}",
            label=m_label,
            category="interaction",
            result_text=f"You inspect the merchant's selection of {m_id}.",
            risk="low"
        ))
        stress_actions.append(Action(
            id=f"barter_{m_id}",
            label=f"Barter for {m_id}",
            category="social",
            effects=[
                {"log_event": f"You negotiated prices at the {m_id} merchant."}
            ],
            result_text=f"The vendor haggles over current {m_id} rates.",
            risk="low"
        ))

    # 3. 25 NPC Inquiries and Street Rumors
    rumor_sources = [
        "caravan_guard", "beggar_boy", "foreign_diplomat", "temple_acolyte",
        "dock_porter", "city_watchman", "shadow_fence", "nomad_scout",
        "drunken_sailor", "bazaar_herald", "scribe_apprentice", "weaver_elder",
        "smuggler_courier", "magistrate_clerk", "armorer_journeyman", "water_carrier",
        "traveling_bard", "alchemist_drudge", "stable_master", "toll_collector",
        "guild_treasurer", "innkeeper_wife", "street_preacher", "retired_gladiator",
        "dune_raider"
    ]
    for r_id in rumor_sources:
        stress_actions.append(Action(
            id=f"question_{r_id}",
            label=f"Question {r_id.split('_')[0]}",
            category="social",
            effects=[
                {"log_event": f"You gathered street intelligence from {r_id}."}
            ],
            result_text="The local shares quiet rumors of unrest.",
            risk="low"
        ))

    # 4. 20 Public Infrastructure Affordances
    infra = [
        ("public_fountain", "Drink from fountain"),
        ("stone_monument", "Read marble monument"),
        ("bounty_board", "Examine public bounties"),
        ("watch_tower", "Survey watch tower"),
        ("bell_gantry", "Inspect alarm bell"),
        ("drainage_sluice", "Check sewer grate"),
        ("caravan_scale", "Test public scale"),
        ("auction_block", "Watch auction block"),
        ("guild_seal", "Touch guild seal"),
        ("lamp_post", "Check brass lamp"),
        ("hay_stack", "Search hay stack"),
        ("sun_dial", "Check sun dial"),
        ("courier_pigeon", "Examine messenger bird"),
        ("guard_barricade", "Inspect iron spikes"),
        ("city_map_slate", "Study district map"),
        ("well_crane", "Inspect well crank"),
        ("tax_pillar", "Read tax decree"),
        ("refuse_bin", "Search discard heap"),
        ("water_trough", "Inspect horse trough"),
        ("flagstone_drain", "Probe loose flagstone"),
    ]
    for i_id, i_label in infra:
        stress_actions.append(Action(
            id=f"interact_{i_id}",
            label=i_label,
            category="interaction",
            result_text=f"You inspect the {i_id.replace('_', ' ')}.",
            risk="low"
        ))

    # Grand Bazaar Center Scene
    scenes["bazaar_center"] = SceneNode(
        id="bazaar_center",
        title="The Grand Bazaar Plaza",
        region="stress_market",
        description="Merchants shout beneath colorful canopies. Spices, brass, and livestock crowd the bustling square.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "streetwise"},
                text="You note the undercover watchmen blending into the crowd."
            ),
            DynamicDescription(
                condition={"background_is": "cutpurse"},
                text="Heavy coin purses hang unguarded from wealthy belts."
            )
        ],
        entities=[],
        base_actions=stress_actions
    )

    return RegionManifest(
        id="stress_market",
        name="The Grand Bazaar",
        mechanic_name="Unbounded Commercial Affordance",
        mechanic_description="Stress tests engine affordance synthesis with over 100 simultaneous legal actions.",
        scenes=scenes
    )
