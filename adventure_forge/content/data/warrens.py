"""Region 2: The Lower Warrens.

Unique Mechanic: Social Stealth, Disguise, Faction Stances, and Curfew.
Implements counterfactual witness divergence between Outlaw and Noble sheets.
"""
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action


def build_lower_warrens_region() -> RegionManifest:
    scenes = {}

    # Scene 1: Warrens Gate (Shared counterfactual witness scene)
    scenes["warrens_gate"] = SceneNode(
        id="warrens_gate",
        title="The Warrens Iron Gate",
        region="lower_warrens",
        description="Torch smoke clings to the damp stone archway. Two city watchmen lean on halberds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"background_is": "cutpurse"},
                text="You spot the carved thieves mark hidden beside the sewer drain."
            ),
            DynamicDescription(
                condition={"background_is": "noble_exile"},
                text="The sergeant straightens up and snaps a crisp military salute."
            ),
            DynamicDescription(
                condition={"has_flaw": "marked_outlaw"},
                text="A wanted poster on the wall bears a crude sketch of your face."
            ),
        ],
        entities=[
            {
                "id": "sewer_grate",
                "name": "Sewer Grate",
                "tags": ["lockable"],
                "initial_state": "locked"
            },
            {
                "id": "wooden_cart",
                "name": "Hay Cart",
                "tags": ["flammable"],
                "initial_state": "intact"
            }
        ],
        base_actions=[
            # Action for Outlaw / Cutpurse / Smugglers
            Action(
                id="flash_thief_signet",
                label="Flash thief sign",
                category="trait_exploit",
                condition={
                    "any_of": [
                        {"background_is": "cutpurse"},
                        {"has_marker": "guild_brand"},
                        {"min_skill": {"skill": "cunning", "value": 3}}
                    ]
                },
                effects=[
                    {"modify_reputation": {"faction": "smugglers", "value": 5}},
                    {"log_event": "The gatekeeper slips open the smuggler postern."}
                ],
                target_scene="warrens_black_market",
                result_text="The beggar nods slightly and opens the shadow door.",
                risk="low"
            ),
            # Action for Noble / Watch affiliation
            Action(
                id="demand_guard_entry",
                label="Order guards aside",
                category="social",
                condition={
                    "any_of": [
                        {"background_is": "noble_exile"},
                        {"has_marker": "watch_crest"},
                        {"min_attribute": {"attribute": "intimidation", "value": 12}}
                    ]
                },
                effects=[
                    {"modify_reputation": {"faction": "city_watch", "value": 5}},
                    {"log_event": "The watchmen clear the passage without inspection."}
                ],
                target_scene="warrens_guardhouse",
                result_text="The guards snap to attention and unbar the heavy oak gate.",
                risk="low"
            ),
            # General public action
            Action(
                id="pay_gate_toll",
                label="Pay coin toll",
                category="interaction",
                condition={"has_item": "silver_coin"},
                effects=[
                    {"remove_item": "silver_coin"},
                    {"log_event": "You paid the gate sergeant a silver coin."}
                ],
                target_scene="warrens_alley",
                result_text="The guard takes your coin and steps aside.",
                risk="low"
            ),
            # Sneak past
            Action(
                id="slip_past_watch",
                label="Slip into shadow",
                category="movement",
                condition={"min_skill": {"skill": "stealth", "value": 2}},
                target_scene="warrens_alley",
                result_text="You dart between shadows while the guards look away.",
                risk="medium"
            ),
            # Travel back to Crags
            Action(
                id="climb_to_crags",
                label="Return to Crags",
                category="movement",
                target_scene="crags_base",
                result_text="You climb the rocky trail back toward the mountain base.",
                risk="low"
            )
        ]
    )

    # Scene 2: The Shadows Alley
    scenes["warrens_alley"] = SceneNode(
        id="warrens_alley",
        title="Cobblestone Alley",
        region="lower_warrens",
        description="Rain drips from sagging roofs into muddy gutters. Murmurs drift from shuttered windows.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "streetwise"},
                text="You read the chalk marks left by local fence lookouts."
            )
        ],
        entities=[],
        base_actions=[
            Action(
                id="enter_black_market",
                label="Enter cellar",
                category="movement",
                target_scene="warrens_black_market",
                result_text="You push through a bead curtain into the hidden cellar.",
                risk="low"
            ),
            Action(
                id="head_to_market",
                label="Enter Grand Bazaar",
                category="movement",
                target_scene="bazaar_center",
                result_text="You follow the smell of spices into the open market plaza.",
                risk="low"
            ),
            Action(
                id="back_to_gate",
                label="Return to gate",
                category="movement",
                target_scene="warrens_gate",
                result_text="You walk back toward the fortified gatehouse.",
                risk="low"
            )
        ]
    )

    # Scene 3: Black Market Fence (Thief/Outlaw focus)
    scenes["warrens_black_market"] = SceneNode(
        id="warrens_black_market",
        title="Underground Fence",
        region="lower_warrens",
        description="Oil lamps illuminate contraband crates. Masked traders weigh silver scales.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_flaw": "marked_outlaw"},
                text="The fence grins and offers you a seat at the high table."
            )
        ],
        entities=[],
        base_actions=[
            Action(
                id="buy_lockpicks",
                label="Buy lockpicks",
                category="interaction",
                condition={"has_item": "silver_coin"},
                effects=[
                    {"remove_item": "silver_coin"},
                    {"add_item": "lockpick"},
                    {"log_event": "You bought hardened tension lockpicks."}
                ],
                result_text="A slender set of steel picks slides into your pocket.",
                risk="low"
            ),
            Action(
                id="forge_watch_permit",
                label="Buy forged pass",
                category="interaction",
                condition={"has_item": "silver_coin", "lacks_flag": "has_watch_badge"},
                effects=[
                    {"remove_item": "silver_coin"},
                    {"set_flag": {"flag": "has_watch_badge", "value": True}},
                    {"log_event": "You bought a forged watch badge and contraband ledger."}
                ],
                result_text="The fence slides a forged bronze crest across the table.",
                risk="low"
            ),
            Action(
                id="leave_market",
                label="Leave cellar",
                category="movement",
                target_scene="warrens_alley",
                result_text="You climb the cellar steps into the alley.",
                risk="low"
            )
        ]
    )

    # Scene 4: Guardhouse (Law/Noble focus)
    scenes["warrens_guardhouse"] = SceneNode(
        id="warrens_guardhouse",
        title="District Guardhouse",
        region="lower_warrens",
        description="Weapons racks line the whitewashed stone walls. A duty ledger rests on the desk.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"background_is": "noble_exile"},
                text="The sergeant hands you the keys to the district armory."
            )
        ],
        entities=[],
        base_actions=[
            Action(
                id="take_patrol_badge",
                label="Take patrol badge",
                category="interaction",
                effects=[
                    {"add_marker": "watch_crest"},
                    {"set_flag": {"flag": "has_watch_badge", "value": True}},
                    {"log_event": "You pinned the bronze watch crest to your lapel."}
                ],
                condition={"lacks_flag": "has_watch_badge"},
                result_text="The heavy bronze badge confirms your official standing.",
                risk="low"
            ),
            Action(
                id="leave_guardhouse",
                label="Exit to alley",
                category="movement",
                target_scene="warrens_alley",
                result_text="You step out into the rain-swept district.",
                risk="low"
            )
        ]
    )

    return RegionManifest(
        id="lower_warrens",
        name="The Lower Warrens",
        mechanic_name="Social Stealth & Faction Stances",
        mechanic_description="Disguises, criminal signets, watch badges, and faction reaction matrices.",
        scenes=scenes
    )
