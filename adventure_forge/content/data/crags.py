"""Region 1: The Iron Crags.

Unique Mechanic: Verticality, Climbing Gear, and Ledge Hazards.
"""
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action


def build_iron_crags_region() -> RegionManifest:
    scenes = {}

    # Scene 1: Approach at Base
    scenes["crags_base"] = SceneNode(
        id="crags_base",
        title="Iron Crags Base",
        region="iron_crags",
        description="Cold wind whips down the shale slope. Sheer rock rises into the mist.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"background_is": "pit_fighter"},
                text="Loose rock offers firm footing for heavy boots."
            ),
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your dark vision catches iron pitons driven into the cliff."
            ),
        ],
        entities=[
            {
                "id": "cliff_face",
                "name": "Cliff Face",
                "tags": ["climbable"],
                "climb_destination": "crags_ridge"
            },
            {
                "id": "iron_chest",
                "name": "Iron Chest",
                "tags": ["lockable"],
                "initial_state": "locked"
            }
        ],
        base_actions=[
            Action(
                id="search_scree",
                label="Search scree",
                category="interaction",
                effects=[
                    {"add_item": "climbing_rope"},
                    {"log_event": "You found discarded climbing rope under the shale."}
                ],
                condition={"lacks_flag": "found_crags_rope"},
                result_text="Your hands unearth coiled hemp rope.",
                risk="low"
            ),
            Action(
                id="hail_watchman",
                label="Hail watchman",
                category="social",
                condition={"min_reputation": {"faction": "iron_guard", "value": 0}},
                effects=[
                    {"log_event": "The watchman nods and lowers a ladder."}
                ],
                target_scene="crags_ridge",
                result_text="The guard recognizes your colors and drops a wooden ladder.",
                risk="low"
            ),
            Action(
                id="walk_to_warrens",
                label="Head to Warrens",
                category="movement",
                target_scene="warrens_gate",
                result_text="You take the switchback trail down toward the low city.",
                risk="low"
            )
        ]
    )

    # Scene 2: High Ridge
    scenes["crags_ridge"] = SceneNode(
        id="crags_ridge",
        title="The High Ridge",
        region="iron_crags",
        description="A narrow stone ledge overlooks the valley below. Iron chains rattle against granite.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "nimble"},
                text="The fierce wind does not shake your balance."
            )
        ],
        entities=[
            {
                "id": "cable_car",
                "name": "Cable Car",
                "tags": ["transport"],
                "initial_state": "intact"
            },
            {
                "id": "signal_bell",
                "name": "Signal Bell",
                "tags": ["metallic", "interactable"]
            }
        ],
        base_actions=[
            Action(
                id="ring_warning_bell",
                label="Ring signal bell",
                category="interaction",
                effects=[
                    {"log_event": "You struck the iron bell to alert the watch."}
                ],
                result_text="A deep chime echoes down the mountain canyons.",
                risk="low"
            ),
            Action(
                id="climb_down_base",
                label="Climb down",
                category="movement",
                target_scene="crags_base",
                result_text="You descend carefully back to the canyon floor.",
                risk="medium"
            ),
            Action(
                id="ride_cable_car",
                label="Ride cable car",
                category="systemic",
                target_scene="crags_peak",
                condition={"has_item": "iron_crank"},
                effects=[
                    {"log_event": "You cranked the cable car across the chasm."}
                ],
                result_text="Gears grind as the cage carries you across the abyss.",
                risk="high"
            ),
            Action(
                id="cross_rope_bridge",
                label="Cross bridge",
                category="movement",
                target_scene="crags_peak",
                stamina_cost=1,
                result_text="You step across swaying planks over the gorge.",
                risk="medium"
            )
        ]
    )

    # Scene 3: Eagle Peak (Terminal Outcome)
    scenes["crags_peak"] = SceneNode(
        id="crags_peak",
        title="Eagle Peak Fortress",
        region="iron_crags",
        description="The ancient mountain stronghold stands unbroken. Signal fires burn along the parapet.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_attribute": {"attribute": "strength", "value": 14}},
                text="You feel right at home among the heavy stone ramparts."
            )
        ],
        entities=[
            {
                "id": "beacon_brazier",
                "name": "Beacon Brazier",
                "tags": ["flammable", "interactable"]
            },
            {
                "id": "lookout_perch",
                "name": "Lookout Perch",
                "tags": ["climbable"]
            }
        ],
        base_actions=[
            Action(
                id="claim_crags_beacon",
                label="Light beacon",
                category="interaction",
                effects=[
                    {"set_flag": {"flag": "crags_beacon_lit", "value": True}},
                    {"modify_reputation": {"faction": "iron_guard", "value": 10}},
                    {"log_event": "The mountain beacon blazes into the night."}
                ],
                result_text="You thrust a torch into pitch. Flames roar into the sky.",
                risk="low"
            ),
            Action(
                id="survey_valley",
                label="Survey valley below",
                category="interaction",
                effects=[
                    {"set_flag": {"flag": "crags_valley_mapped", "value": True}},
                    {"log_event": "You surveyed the sprawling lowlands from the peak."}
                ],
                result_text="Clear skies reveal the entire continent stretched below.",
                risk="low"
            ),
            Action(
                id="return_ridge",
                label="Return to ridge",
                category="movement",
                target_scene="crags_ridge",
                result_text="You retrace your steps toward the lower ridge.",
                risk="low"
            )
        ],
        is_terminal=False
    )

    return RegionManifest(
        id="iron_crags",
        name="The Iron Crags",
        mechanic_name="Verticality & Climbing Hazards",
        mechanic_description="Vertical climbing routes, rope requirements, and wind balance checks.",
        scenes=scenes
    )
