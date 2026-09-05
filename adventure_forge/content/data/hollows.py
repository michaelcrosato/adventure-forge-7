"""Region 5: The Sunken Hollows.

Unique Mechanic: Water Buoyancy, Diving Depth, and Torch Preservation.
"""
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action


def build_sunken_hollows_region() -> RegionManifest:
    scenes = {}

    # Scene 1: Grotto Entrance
    scenes["hollows_grotto"] = SceneNode(
        id="hollows_grotto",
        title="Sunken Grotto Entrance",
        region="sunken_hollows",
        description="Dark subterranean water laps against mossy stone steps. Phosphorescent fungi cast green light.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"ancestry_is": "deep_dweller"},
                text="The scent of underground minerals and deep water feels welcoming."
            ),
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="You track underwater tunnel arches through the clear water."
            )
        ],
        entities=[
            {
                "id": "diving_bell",
                "name": "Diving Bell",
                "tags": ["transport", "submersible"],
                "initial_state": "intact"
            }
        ],
        base_actions=[
            Action(
                id="dive_into_pool",
                label="Dive underwater",
                category="movement",
                condition={
                    "any_of": [
                        {"min_attribute": {"attribute": "endurance", "value": 12}},
                        {"min_attribute": {"attribute": "agility", "value": 12}},
                        {"has_trait": "water_breather"},
                        {"has_trait": "nimble"}
                    ]
                },
                target_scene="hollows_temple",
                stamina_cost=2,
                result_text="You hold your breath and plunge into the freezing subterranean river.",
                risk="high"
            ),
            Action(
                id="salvage_diving_gear",
                label="Search grotto shore",
                category="interaction",
                condition={"lacks_flag": "salvaged_grotto_seal"},
                effects=[
                    {"add_item": "waterproof_seal"},
                    {"set_flag": {"flag": "salvaged_grotto_seal", "value": True}},
                    {"log_event": "You found a tin of waterproof pitch along the shore."}
                ],
                result_text="Your fingers pry a sealed tin of wax pitch from wet gravel.",
                risk="low"
            ),
            Action(
                id="board_diving_bell",
                label="Enter diving bell",
                category="systemic",
                condition={"has_item": "waterproof_seal"},
                target_scene="hollows_temple",
                result_text="The bronze bell slowly submerges beneath the foam.",
                risk="low"
            ),
            Action(
                id="ascend_to_bazaar",
                label="Climb to Bazaar",
                category="movement",
                target_scene="bazaar_center",
                result_text="You climb the spiral stair back toward the upper city.",
                risk="low"
            )
        ]
    )

    # Scene 2: Sunken Temple
    scenes["hollows_temple"] = SceneNode(
        id="hollows_temple",
        title="The Sunken Temple",
        region="sunken_hollows",
        description="Air trapped beneath stone domes allows shallow breathing. Carved obsidian altars gleam.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "water_breather"},
                text="Your gills effortlessly draw oxygen from the subterranean currents."
            )
        ],
        entities=[],
        base_actions=[
            Action(
                id="take_sunken_relic",
                label="Take altar relic",
                category="interaction",
                effects=[
                    {"add_item": "sunken_pearl"},
                    {"set_flag": {"flag": "sunken_relic_secured", "value": True}},
                    {"log_event": "You retrieved the glowing pearl from the obsidian shrine."}
                ],
                condition={"lacks_flag": "sunken_relic_secured"},
                result_text="Your hand closes around the smooth, luminous pearl.",
                risk="medium"
            ),
            Action(
                id="swim_to_surface",
                label="Swim to surface",
                category="movement",
                target_scene="hollows_grotto",
                result_text="You kick upward and break through into the open cavern air.",
                risk="low"
            )
        ]
    )

    return RegionManifest(
        id="sunken_hollows",
        name="The Sunken Hollows",
        mechanic_name="Water Buoyancy & Cavern Diving",
        mechanic_description="Underwater breath management, diving bells, and buoyancy physics.",
        scenes=scenes
    )
