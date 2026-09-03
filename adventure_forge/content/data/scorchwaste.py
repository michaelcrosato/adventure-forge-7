"""Region 3: The Scorchwaste.

Unique Mechanic: Ambient Heat, Hydration, Survival Crafting, and Shade Tracking.
"""
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action


def build_scorchwaste_region() -> RegionManifest:
    scenes = {}

    # Scene 1: Dunes Perimeter
    scenes["scorch_dunes"] = SceneNode(
        id="scorch_dunes",
        title="The Sun-Bleached Dunes",
        region="scorchwaste",
        description="Heat ripples rise from red sand. Dry wind stings your eyes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"ancestry_is": "ashenborn"},
                text="The searing sun warms your blood without sapping your strength."
            ),
            DynamicDescription(
                condition={"has_trait": "desert_born"},
                text="You recognize the subterranean water reed clusters ahead."
            )
        ],
        entities=[
            {
                "id": "crashed_skiff",
                "name": "Crashed Skiff",
                "tags": ["scavengeable", "flammable"],
                "initial_state": "intact"
            }
        ],
        base_actions=[
            Action(
                id="drink_canteen",
                label="Drink canteen",
                category="interaction",
                condition={"has_item": "water_skin"},
                effects=[
                    {"modify_stamina": 3},
                    {"log_event": "You drank cool water and restored stamina."}
                ],
                result_text="Clear water soothes your parched throat.",
                risk="low"
            ),
            Action(
                id="dig_sand_well",
                label="Dig for water",
                category="systemic",
                effects=[
                    {"add_item": "water_skin"},
                    {"log_event": "You dug down to damp sand and filled a skin."}
                ],
                stamina_cost=1,
                result_text="Moist soil yields a steady trickle of fresh water.",
                risk="low"
            ),
            Action(
                id="march_to_oasis",
                label="Trek to Oasis",
                category="movement",
                target_scene="scorch_oasis",
                stamina_cost=1,
                result_text="You press through shifting sand toward distant date palms.",
                risk="medium"
            ),
            Action(
                id="retreat_to_bazaar",
                label="Back to Bazaar",
                category="movement",
                target_scene="bazaar_center",
                result_text="You turn back toward the bustling city gates.",
                risk="low"
            )
        ]
    )

    # Scene 2: The Palm Oasis
    scenes["scorch_oasis"] = SceneNode(
        id="scorch_oasis",
        title="Oasis of Still Waters",
        region="scorchwaste",
        description="Tall palms cast deep green shadows over a clear pool. Bedouin nomads watch silently.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "iron_gutted"},
                text="You can drink from stagnant desert pools without sickness."
            )
        ],
        entities=[],
        base_actions=[
            Action(
                id="rest_in_shade",
                label="Rest in shade",
                category="interaction",
                effects=[
                    {"modify_health": 5},
                    {"modify_stamina": 5},
                    {"log_event": "You rested under the palms and recovered vitality."}
                ],
                result_text="The cool breeze under the fronds revives your senses.",
                risk="low"
            ),
            Action(
                id="trade_with_nomads",
                label="Trade with nomads",
                category="social",
                condition={"has_item": "silver_coin"},
                effects=[
                    {"remove_item": "silver_coin"},
                    {"add_item": "desert_compass"},
                    {"log_event": "Nomads traded a brass desert compass for silver."}
                ],
                result_text="The elder offers a reliable sun compass.",
                risk="low"
            ),
            Action(
                id="travel_to_dunes",
                label="Return to dunes",
                category="movement",
                target_scene="scorch_dunes",
                result_text="You step back out into the blistering heat.",
                risk="low"
            )
        ]
    )

    return RegionManifest(
        id="scorchwaste",
        name="The Scorchwaste",
        mechanic_name="Ambient Heat & Hydration Survival",
        mechanic_description="Heat stamina drain, water skin management, and oasis shade recovery.",
        scenes=scenes
    )
