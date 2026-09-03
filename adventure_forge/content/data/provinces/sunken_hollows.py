"""Province: The Sunken Abyss.
Unique Mechanic: Water Buoyancy & Underwater Diving.
"""
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action

def build_sunken_hollows_province() -> RegionManifest:
    scenes = {}

    # Province Hub
    scenes["sunken_hollows_hub"] = SceneNode(
        id="sunken_hollows_hub",
        title="The Sunken Abyss - Central Hub",
        region="sunken_hollows",
        description="Green moss lights the underground cavern lake. Cold water drips from dark stone points.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_attribute": {"attribute": "strength", "value": 12}},
                text="Your military posture draws respectful nods from travelers."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_hub_scout", label="Scout hub", category="interaction", result_text="You survey the bustling provincial crossroads."),
            Action(id="sunken_hollows_hub_rest", label="Rest at inn", category="interaction", effects=[{"modify_stamina": 5}], result_text="You rest and regain stamina."),
            Action(id="sunken_hollows_to_bazaar", label="Go to Bazaar", category="movement", target_scene="bazaar_center", result_text="You travel along the highway to the Grand Bazaar."),
        ]
    )

    # POI: Glowstone Grotto (10 nodes)
    scenes["sunken_hollows_glow_grotto_gate"] = SceneNode(
        id="sunken_hollows_glow_grotto_gate",
        title="Glowstone Grotto - Outer Gate",
        region="sunken_hollows",
        description="Iron bars secure the heavy timber entrance. Green moss covers the wet stone rocks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="sunken_hollows_glow_grotto_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="sunken_hollows_glow_grotto_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_glow_grotto_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_glow_grotto_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_glow_grotto_courtyard"] = SceneNode(
        id="sunken_hollows_glow_grotto_courtyard",
        title="Glowstone Grotto - Main Courtyard",
        region="sunken_hollows",
        description="Cobblestones show heavy cart wheel wear. Green moss covers the wet stone rocks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="sunken_hollows_glow_grotto_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="sunken_hollows_glow_grotto_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_glow_grotto_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_glow_grotto_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_glow_grotto_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_glow_grotto_quarters"] = SceneNode(
        id="sunken_hollows_glow_grotto_quarters",
        title="Glowstone Grotto - Living Quarters",
        region="sunken_hollows",
        description="Rows of wooden bunks line the walls. Green moss covers the wet stone rocks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="sunken_hollows_glow_grotto_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="sunken_hollows_glow_grotto_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_glow_grotto_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_glow_grotto_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_glow_grotto_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_glow_grotto_armory"] = SceneNode(
        id="sunken_hollows_glow_grotto_armory",
        title="Glowstone Grotto - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. Green moss covers the wet stone rocks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="sunken_hollows_glow_grotto_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="sunken_hollows_glow_grotto_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_glow_grotto_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_glow_grotto_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_glow_grotto_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_glow_grotto_cellar"] = SceneNode(
        id="sunken_hollows_glow_grotto_cellar",
        title="Glowstone Grotto - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. Green moss covers the wet stone rocks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="sunken_hollows_glow_grotto_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="sunken_hollows_glow_grotto_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_glow_grotto_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_glow_grotto_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_glow_grotto_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_glow_grotto_passage"] = SceneNode(
        id="sunken_hollows_glow_grotto_passage",
        title="Glowstone Grotto - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. Green moss covers the wet stone rocks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="sunken_hollows_glow_grotto_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="sunken_hollows_glow_grotto_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_glow_grotto_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_glow_grotto_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_glow_grotto_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_glow_grotto_chamber"] = SceneNode(
        id="sunken_hollows_glow_grotto_chamber",
        title="Glowstone Grotto - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. Green moss covers the wet stone rocks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="sunken_hollows_glow_grotto_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="sunken_hollows_glow_grotto_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_glow_grotto_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_glow_grotto_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_glow_grotto_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_glow_grotto_overlook"] = SceneNode(
        id="sunken_hollows_glow_grotto_overlook",
        title="Glowstone Grotto - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. Green moss covers the wet stone rocks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="sunken_hollows_glow_grotto_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="sunken_hollows_glow_grotto_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_glow_grotto_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_glow_grotto_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_glow_grotto_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_glow_grotto_sanctum"] = SceneNode(
        id="sunken_hollows_glow_grotto_sanctum",
        title="Glowstone Grotto - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. Green moss covers the wet stone rocks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="sunken_hollows_glow_grotto_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="sunken_hollows_glow_grotto_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_glow_grotto_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_glow_grotto_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_glow_grotto_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_glow_grotto_vault"] = SceneNode(
        id="sunken_hollows_glow_grotto_vault",
        title="Glowstone Grotto - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. Green moss covers the wet stone rocks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="sunken_hollows_glow_grotto_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="sunken_hollows_glow_grotto_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_glow_grotto_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_glow_grotto_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_glow_grotto", label="Visit Glowstone Gr", category="movement", target_scene="sunken_hollows_glow_grotto_gate", result_text="You travel to Glowstone Grotto.")
    )

    # POI: Subterranean River (10 nodes)
    scenes["sunken_hollows_abyssal_river_gate"] = SceneNode(
        id="sunken_hollows_abyssal_river_gate",
        title="Subterranean River - Outer Gate",
        region="sunken_hollows",
        description="Iron bars secure the heavy timber entrance. Black water rushes through smooth cavern arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="sunken_hollows_abyssal_river_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="sunken_hollows_abyssal_river_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_abyssal_river_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_abyssal_river_courtyard"] = SceneNode(
        id="sunken_hollows_abyssal_river_courtyard",
        title="Subterranean River - Main Courtyard",
        region="sunken_hollows",
        description="Cobblestones show heavy cart wheel wear. Black water rushes through smooth cavern arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="sunken_hollows_abyssal_river_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="sunken_hollows_abyssal_river_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_abyssal_river_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_abyssal_river_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_abyssal_river_quarters"] = SceneNode(
        id="sunken_hollows_abyssal_river_quarters",
        title="Subterranean River - Living Quarters",
        region="sunken_hollows",
        description="Rows of wooden bunks line the walls. Black water rushes through smooth cavern arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="sunken_hollows_abyssal_river_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="sunken_hollows_abyssal_river_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_abyssal_river_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_abyssal_river_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_abyssal_river_armory"] = SceneNode(
        id="sunken_hollows_abyssal_river_armory",
        title="Subterranean River - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. Black water rushes through smooth cavern arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="sunken_hollows_abyssal_river_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="sunken_hollows_abyssal_river_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_abyssal_river_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_abyssal_river_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_abyssal_river_cellar"] = SceneNode(
        id="sunken_hollows_abyssal_river_cellar",
        title="Subterranean River - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. Black water rushes through smooth cavern arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="sunken_hollows_abyssal_river_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="sunken_hollows_abyssal_river_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_abyssal_river_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_abyssal_river_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_abyssal_river_passage"] = SceneNode(
        id="sunken_hollows_abyssal_river_passage",
        title="Subterranean River - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. Black water rushes through smooth cavern arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="sunken_hollows_abyssal_river_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="sunken_hollows_abyssal_river_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_abyssal_river_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_abyssal_river_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_abyssal_river_chamber"] = SceneNode(
        id="sunken_hollows_abyssal_river_chamber",
        title="Subterranean River - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. Black water rushes through smooth cavern arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="sunken_hollows_abyssal_river_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="sunken_hollows_abyssal_river_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_abyssal_river_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_abyssal_river_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_abyssal_river_overlook"] = SceneNode(
        id="sunken_hollows_abyssal_river_overlook",
        title="Subterranean River - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. Black water rushes through smooth cavern arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="sunken_hollows_abyssal_river_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="sunken_hollows_abyssal_river_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_abyssal_river_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_abyssal_river_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_abyssal_river_sanctum"] = SceneNode(
        id="sunken_hollows_abyssal_river_sanctum",
        title="Subterranean River - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. Black water rushes through smooth cavern arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="sunken_hollows_abyssal_river_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="sunken_hollows_abyssal_river_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_abyssal_river_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_abyssal_river_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_abyssal_river_vault"] = SceneNode(
        id="sunken_hollows_abyssal_river_vault",
        title="Subterranean River - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. Black water rushes through smooth cavern arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="sunken_hollows_abyssal_river_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="sunken_hollows_abyssal_river_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_abyssal_river_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_abyssal_river", label="Visit Subterranean", category="movement", target_scene="sunken_hollows_abyssal_river_gate", result_text="You travel to Subterranean River.")
    )

    # POI: Drowned Shrine (10 nodes)
    scenes["sunken_hollows_drowned_temple_gate"] = SceneNode(
        id="sunken_hollows_drowned_temple_gate",
        title="Drowned Shrine - Outer Gate",
        region="sunken_hollows",
        description="Iron bars secure the heavy timber entrance. Submerged stone pillars rise through clear water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="sunken_hollows_drowned_temple_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="sunken_hollows_drowned_temple_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_drowned_temple_courtyard"] = SceneNode(
        id="sunken_hollows_drowned_temple_courtyard",
        title="Drowned Shrine - Main Courtyard",
        region="sunken_hollows",
        description="Cobblestones show heavy cart wheel wear. Submerged stone pillars rise through clear water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="sunken_hollows_drowned_temple_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="sunken_hollows_drowned_temple_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_drowned_temple_quarters"] = SceneNode(
        id="sunken_hollows_drowned_temple_quarters",
        title="Drowned Shrine - Living Quarters",
        region="sunken_hollows",
        description="Rows of wooden bunks line the walls. Submerged stone pillars rise through clear water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="sunken_hollows_drowned_temple_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="sunken_hollows_drowned_temple_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_drowned_temple_armory"] = SceneNode(
        id="sunken_hollows_drowned_temple_armory",
        title="Drowned Shrine - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. Submerged stone pillars rise through clear water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="sunken_hollows_drowned_temple_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="sunken_hollows_drowned_temple_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_drowned_temple_cellar"] = SceneNode(
        id="sunken_hollows_drowned_temple_cellar",
        title="Drowned Shrine - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. Submerged stone pillars rise through clear water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="sunken_hollows_drowned_temple_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="sunken_hollows_drowned_temple_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_drowned_temple_passage"] = SceneNode(
        id="sunken_hollows_drowned_temple_passage",
        title="Drowned Shrine - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. Submerged stone pillars rise through clear water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="sunken_hollows_drowned_temple_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="sunken_hollows_drowned_temple_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_drowned_temple_chamber"] = SceneNode(
        id="sunken_hollows_drowned_temple_chamber",
        title="Drowned Shrine - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. Submerged stone pillars rise through clear water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="sunken_hollows_drowned_temple_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="sunken_hollows_drowned_temple_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_drowned_temple_overlook"] = SceneNode(
        id="sunken_hollows_drowned_temple_overlook",
        title="Drowned Shrine - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. Submerged stone pillars rise through clear water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="sunken_hollows_drowned_temple_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="sunken_hollows_drowned_temple_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_drowned_temple_sanctum"] = SceneNode(
        id="sunken_hollows_drowned_temple_sanctum",
        title="Drowned Shrine - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. Submerged stone pillars rise through clear water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="sunken_hollows_drowned_temple_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="sunken_hollows_drowned_temple_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_drowned_temple_vault"] = SceneNode(
        id="sunken_hollows_drowned_temple_vault",
        title="Drowned Shrine - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. Submerged stone pillars rise through clear water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="sunken_hollows_drowned_temple_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="sunken_hollows_drowned_temple_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_drowned_temple", label="Visit Drowned Shri", category="movement", target_scene="sunken_hollows_drowned_temple_gate", result_text="You travel to Drowned Shrine.")
    )

    # POI: Crystal Trench (10 nodes)
    scenes["sunken_hollows_coral_chasm_gate"] = SceneNode(
        id="sunken_hollows_coral_chasm_gate",
        title="Crystal Trench - Outer Gate",
        region="sunken_hollows",
        description="Iron bars secure the heavy timber entrance. Glowing coral reefs thrive in subterranean warmth.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="sunken_hollows_coral_chasm_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="sunken_hollows_coral_chasm_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_courtyard"] = SceneNode(
        id="sunken_hollows_coral_chasm_courtyard",
        title="Crystal Trench - Main Courtyard",
        region="sunken_hollows",
        description="Cobblestones show heavy cart wheel wear. Glowing coral reefs thrive in subterranean warmth.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="sunken_hollows_coral_chasm_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="sunken_hollows_coral_chasm_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_quarters"] = SceneNode(
        id="sunken_hollows_coral_chasm_quarters",
        title="Crystal Trench - Living Quarters",
        region="sunken_hollows",
        description="Rows of wooden bunks line the walls. Glowing coral reefs thrive in subterranean warmth.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="sunken_hollows_coral_chasm_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="sunken_hollows_coral_chasm_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_armory"] = SceneNode(
        id="sunken_hollows_coral_chasm_armory",
        title="Crystal Trench - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. Glowing coral reefs thrive in subterranean warmth.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="sunken_hollows_coral_chasm_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="sunken_hollows_coral_chasm_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_cellar"] = SceneNode(
        id="sunken_hollows_coral_chasm_cellar",
        title="Crystal Trench - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. Glowing coral reefs thrive in subterranean warmth.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="sunken_hollows_coral_chasm_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="sunken_hollows_coral_chasm_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_passage"] = SceneNode(
        id="sunken_hollows_coral_chasm_passage",
        title="Crystal Trench - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. Glowing coral reefs thrive in subterranean warmth.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="sunken_hollows_coral_chasm_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="sunken_hollows_coral_chasm_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_chamber"] = SceneNode(
        id="sunken_hollows_coral_chasm_chamber",
        title="Crystal Trench - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. Glowing coral reefs thrive in subterranean warmth.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="sunken_hollows_coral_chasm_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="sunken_hollows_coral_chasm_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_overlook"] = SceneNode(
        id="sunken_hollows_coral_chasm_overlook",
        title="Crystal Trench - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. Glowing coral reefs thrive in subterranean warmth.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="sunken_hollows_coral_chasm_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="sunken_hollows_coral_chasm_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_sanctum"] = SceneNode(
        id="sunken_hollows_coral_chasm_sanctum",
        title="Crystal Trench - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. Glowing coral reefs thrive in subterranean warmth.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="sunken_hollows_coral_chasm_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="sunken_hollows_coral_chasm_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_vault"] = SceneNode(
        id="sunken_hollows_coral_chasm_vault",
        title="Crystal Trench - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. Glowing coral reefs thrive in subterranean warmth.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="sunken_hollows_coral_chasm_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="sunken_hollows_coral_chasm_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_coral_chasm", label="Visit Crystal Tren", category="movement", target_scene="sunken_hollows_coral_chasm_gate", result_text="You travel to Crystal Trench.")
    )

    # POI: The Flooded Siphon (10 nodes)
    scenes["sunken_hollows_deep_siphon_gate"] = SceneNode(
        id="sunken_hollows_deep_siphon_gate",
        title="The Flooded Siphon - Outer Gate",
        region="sunken_hollows",
        description="Iron bars secure the heavy timber entrance. Air pockets linger beneath stone cavern domes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="sunken_hollows_deep_siphon_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="sunken_hollows_deep_siphon_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_deep_siphon_courtyard"] = SceneNode(
        id="sunken_hollows_deep_siphon_courtyard",
        title="The Flooded Siphon - Main Courtyard",
        region="sunken_hollows",
        description="Cobblestones show heavy cart wheel wear. Air pockets linger beneath stone cavern domes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="sunken_hollows_deep_siphon_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="sunken_hollows_deep_siphon_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_deep_siphon_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_deep_siphon_quarters"] = SceneNode(
        id="sunken_hollows_deep_siphon_quarters",
        title="The Flooded Siphon - Living Quarters",
        region="sunken_hollows",
        description="Rows of wooden bunks line the walls. Air pockets linger beneath stone cavern domes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="sunken_hollows_deep_siphon_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="sunken_hollows_deep_siphon_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_deep_siphon_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_deep_siphon_armory"] = SceneNode(
        id="sunken_hollows_deep_siphon_armory",
        title="The Flooded Siphon - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. Air pockets linger beneath stone cavern domes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="sunken_hollows_deep_siphon_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="sunken_hollows_deep_siphon_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_deep_siphon_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_deep_siphon_cellar"] = SceneNode(
        id="sunken_hollows_deep_siphon_cellar",
        title="The Flooded Siphon - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. Air pockets linger beneath stone cavern domes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="sunken_hollows_deep_siphon_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="sunken_hollows_deep_siphon_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_deep_siphon_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_deep_siphon_passage"] = SceneNode(
        id="sunken_hollows_deep_siphon_passage",
        title="The Flooded Siphon - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. Air pockets linger beneath stone cavern domes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="sunken_hollows_deep_siphon_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="sunken_hollows_deep_siphon_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_deep_siphon_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_deep_siphon_chamber"] = SceneNode(
        id="sunken_hollows_deep_siphon_chamber",
        title="The Flooded Siphon - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. Air pockets linger beneath stone cavern domes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="sunken_hollows_deep_siphon_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="sunken_hollows_deep_siphon_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_deep_siphon_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_deep_siphon_overlook"] = SceneNode(
        id="sunken_hollows_deep_siphon_overlook",
        title="The Flooded Siphon - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. Air pockets linger beneath stone cavern domes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="sunken_hollows_deep_siphon_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="sunken_hollows_deep_siphon_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_deep_siphon_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_deep_siphon_sanctum"] = SceneNode(
        id="sunken_hollows_deep_siphon_sanctum",
        title="The Flooded Siphon - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. Air pockets linger beneath stone cavern domes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="sunken_hollows_deep_siphon_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="sunken_hollows_deep_siphon_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_deep_siphon_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_deep_siphon_vault"] = SceneNode(
        id="sunken_hollows_deep_siphon_vault",
        title="The Flooded Siphon - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. Air pockets linger beneath stone cavern domes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="sunken_hollows_deep_siphon_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="sunken_hollows_deep_siphon_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_deep_siphon_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_deep_siphon", label="Visit The Flooded", category="movement", target_scene="sunken_hollows_deep_siphon_gate", result_text="You travel to The Flooded Siphon.")
    )

    # POI: Abyssal Pearl Vault (10 nodes)
    scenes["sunken_hollows_vault_depths_gate"] = SceneNode(
        id="sunken_hollows_vault_depths_gate",
        title="Abyssal Pearl Vault - Outer Gate",
        region="sunken_hollows",
        description="Iron bars secure the heavy timber entrance. Giant oyster beds cling to carved steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="sunken_hollows_vault_depths_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="sunken_hollows_vault_depths_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_vault_depths_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_vault_depths_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_vault_depths_courtyard"] = SceneNode(
        id="sunken_hollows_vault_depths_courtyard",
        title="Abyssal Pearl Vault - Main Courtyard",
        region="sunken_hollows",
        description="Cobblestones show heavy cart wheel wear. Giant oyster beds cling to carved steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="sunken_hollows_vault_depths_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="sunken_hollows_vault_depths_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_vault_depths_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_vault_depths_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_vault_depths_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_vault_depths_quarters"] = SceneNode(
        id="sunken_hollows_vault_depths_quarters",
        title="Abyssal Pearl Vault - Living Quarters",
        region="sunken_hollows",
        description="Rows of wooden bunks line the walls. Giant oyster beds cling to carved steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="sunken_hollows_vault_depths_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="sunken_hollows_vault_depths_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_vault_depths_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_vault_depths_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_vault_depths_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_vault_depths_armory"] = SceneNode(
        id="sunken_hollows_vault_depths_armory",
        title="Abyssal Pearl Vault - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. Giant oyster beds cling to carved steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="sunken_hollows_vault_depths_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="sunken_hollows_vault_depths_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_vault_depths_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_vault_depths_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_vault_depths_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_vault_depths_cellar"] = SceneNode(
        id="sunken_hollows_vault_depths_cellar",
        title="Abyssal Pearl Vault - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. Giant oyster beds cling to carved steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="sunken_hollows_vault_depths_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="sunken_hollows_vault_depths_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_vault_depths_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_vault_depths_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_vault_depths_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_vault_depths_passage"] = SceneNode(
        id="sunken_hollows_vault_depths_passage",
        title="Abyssal Pearl Vault - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. Giant oyster beds cling to carved steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="sunken_hollows_vault_depths_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="sunken_hollows_vault_depths_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_vault_depths_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_vault_depths_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_vault_depths_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_vault_depths_chamber"] = SceneNode(
        id="sunken_hollows_vault_depths_chamber",
        title="Abyssal Pearl Vault - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. Giant oyster beds cling to carved steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="sunken_hollows_vault_depths_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="sunken_hollows_vault_depths_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_vault_depths_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_vault_depths_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_vault_depths_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_vault_depths_overlook"] = SceneNode(
        id="sunken_hollows_vault_depths_overlook",
        title="Abyssal Pearl Vault - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. Giant oyster beds cling to carved steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="sunken_hollows_vault_depths_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="sunken_hollows_vault_depths_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_vault_depths_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_vault_depths_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_vault_depths_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_vault_depths_sanctum"] = SceneNode(
        id="sunken_hollows_vault_depths_sanctum",
        title="Abyssal Pearl Vault - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. Giant oyster beds cling to carved steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="sunken_hollows_vault_depths_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="sunken_hollows_vault_depths_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_vault_depths_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_vault_depths_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_vault_depths_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_vault_depths_vault"] = SceneNode(
        id="sunken_hollows_vault_depths_vault",
        title="Abyssal Pearl Vault - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. Giant oyster beds cling to carved steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="sunken_hollows_vault_depths_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="sunken_hollows_vault_depths_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_vault_depths_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_vault_depths_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_vault_depths", label="Visit Abyssal Pear", category="movement", target_scene="sunken_hollows_vault_depths_gate", result_text="You travel to Abyssal Pearl Vault.")
    )

    # POI: Giant Fungal Grove (10 nodes)
    scenes["sunken_hollows_fungal_forest_gate"] = SceneNode(
        id="sunken_hollows_fungal_forest_gate",
        title="Giant Fungal Grove - Outer Gate",
        region="sunken_hollows",
        description="Iron bars secure the heavy timber entrance. Luminescent cap stalks tower over damp paths.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="sunken_hollows_fungal_forest_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="sunken_hollows_fungal_forest_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_fungal_forest_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_fungal_forest_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_fungal_forest_courtyard"] = SceneNode(
        id="sunken_hollows_fungal_forest_courtyard",
        title="Giant Fungal Grove - Main Courtyard",
        region="sunken_hollows",
        description="Cobblestones show heavy cart wheel wear. Luminescent cap stalks tower over damp paths.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="sunken_hollows_fungal_forest_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="sunken_hollows_fungal_forest_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_fungal_forest_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_fungal_forest_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_fungal_forest_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_fungal_forest_quarters"] = SceneNode(
        id="sunken_hollows_fungal_forest_quarters",
        title="Giant Fungal Grove - Living Quarters",
        region="sunken_hollows",
        description="Rows of wooden bunks line the walls. Luminescent cap stalks tower over damp paths.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="sunken_hollows_fungal_forest_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="sunken_hollows_fungal_forest_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_fungal_forest_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_fungal_forest_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_fungal_forest_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_fungal_forest_armory"] = SceneNode(
        id="sunken_hollows_fungal_forest_armory",
        title="Giant Fungal Grove - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. Luminescent cap stalks tower over damp paths.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="sunken_hollows_fungal_forest_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="sunken_hollows_fungal_forest_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_fungal_forest_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_fungal_forest_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_fungal_forest_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_fungal_forest_cellar"] = SceneNode(
        id="sunken_hollows_fungal_forest_cellar",
        title="Giant Fungal Grove - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. Luminescent cap stalks tower over damp paths.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="sunken_hollows_fungal_forest_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="sunken_hollows_fungal_forest_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_fungal_forest_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_fungal_forest_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_fungal_forest_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_fungal_forest_passage"] = SceneNode(
        id="sunken_hollows_fungal_forest_passage",
        title="Giant Fungal Grove - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. Luminescent cap stalks tower over damp paths.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="sunken_hollows_fungal_forest_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="sunken_hollows_fungal_forest_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_fungal_forest_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_fungal_forest_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_fungal_forest_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_fungal_forest_chamber"] = SceneNode(
        id="sunken_hollows_fungal_forest_chamber",
        title="Giant Fungal Grove - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. Luminescent cap stalks tower over damp paths.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="sunken_hollows_fungal_forest_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="sunken_hollows_fungal_forest_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_fungal_forest_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_fungal_forest_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_fungal_forest_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_fungal_forest_overlook"] = SceneNode(
        id="sunken_hollows_fungal_forest_overlook",
        title="Giant Fungal Grove - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. Luminescent cap stalks tower over damp paths.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="sunken_hollows_fungal_forest_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="sunken_hollows_fungal_forest_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_fungal_forest_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_fungal_forest_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_fungal_forest_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_fungal_forest_sanctum"] = SceneNode(
        id="sunken_hollows_fungal_forest_sanctum",
        title="Giant Fungal Grove - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. Luminescent cap stalks tower over damp paths.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="sunken_hollows_fungal_forest_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="sunken_hollows_fungal_forest_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_fungal_forest_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_fungal_forest_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_fungal_forest_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_fungal_forest_vault"] = SceneNode(
        id="sunken_hollows_fungal_forest_vault",
        title="Giant Fungal Grove - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. Luminescent cap stalks tower over damp paths.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="sunken_hollows_fungal_forest_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="sunken_hollows_fungal_forest_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_fungal_forest_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_fungal_forest_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_fungal_forest", label="Visit Giant Fungal", category="movement", target_scene="sunken_hollows_fungal_forest_gate", result_text="You travel to Giant Fungal Grove.")
    )

    # POI: Underground Wharf (10 nodes)
    scenes["sunken_hollows_sub_wharf_gate"] = SceneNode(
        id="sunken_hollows_sub_wharf_gate",
        title="Underground Wharf - Outer Gate",
        region="sunken_hollows",
        description="Iron bars secure the heavy timber entrance. Flat-bottom barges moor at mossy stone docks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="sunken_hollows_sub_wharf_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="sunken_hollows_sub_wharf_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_sub_wharf_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_sub_wharf_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_sub_wharf_courtyard"] = SceneNode(
        id="sunken_hollows_sub_wharf_courtyard",
        title="Underground Wharf - Main Courtyard",
        region="sunken_hollows",
        description="Cobblestones show heavy cart wheel wear. Flat-bottom barges moor at mossy stone docks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="sunken_hollows_sub_wharf_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="sunken_hollows_sub_wharf_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_sub_wharf_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_sub_wharf_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_sub_wharf_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_sub_wharf_quarters"] = SceneNode(
        id="sunken_hollows_sub_wharf_quarters",
        title="Underground Wharf - Living Quarters",
        region="sunken_hollows",
        description="Rows of wooden bunks line the walls. Flat-bottom barges moor at mossy stone docks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="sunken_hollows_sub_wharf_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="sunken_hollows_sub_wharf_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_sub_wharf_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_sub_wharf_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_sub_wharf_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_sub_wharf_armory"] = SceneNode(
        id="sunken_hollows_sub_wharf_armory",
        title="Underground Wharf - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. Flat-bottom barges moor at mossy stone docks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="sunken_hollows_sub_wharf_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="sunken_hollows_sub_wharf_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_sub_wharf_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_sub_wharf_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_sub_wharf_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_sub_wharf_cellar"] = SceneNode(
        id="sunken_hollows_sub_wharf_cellar",
        title="Underground Wharf - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. Flat-bottom barges moor at mossy stone docks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="sunken_hollows_sub_wharf_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="sunken_hollows_sub_wharf_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_sub_wharf_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_sub_wharf_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_sub_wharf_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_sub_wharf_passage"] = SceneNode(
        id="sunken_hollows_sub_wharf_passage",
        title="Underground Wharf - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. Flat-bottom barges moor at mossy stone docks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="sunken_hollows_sub_wharf_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="sunken_hollows_sub_wharf_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_sub_wharf_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_sub_wharf_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_sub_wharf_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_sub_wharf_chamber"] = SceneNode(
        id="sunken_hollows_sub_wharf_chamber",
        title="Underground Wharf - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. Flat-bottom barges moor at mossy stone docks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="sunken_hollows_sub_wharf_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="sunken_hollows_sub_wharf_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_sub_wharf_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_sub_wharf_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_sub_wharf_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_sub_wharf_overlook"] = SceneNode(
        id="sunken_hollows_sub_wharf_overlook",
        title="Underground Wharf - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. Flat-bottom barges moor at mossy stone docks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="sunken_hollows_sub_wharf_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="sunken_hollows_sub_wharf_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_sub_wharf_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_sub_wharf_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_sub_wharf_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_sub_wharf_sanctum"] = SceneNode(
        id="sunken_hollows_sub_wharf_sanctum",
        title="Underground Wharf - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. Flat-bottom barges moor at mossy stone docks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="sunken_hollows_sub_wharf_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="sunken_hollows_sub_wharf_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_sub_wharf_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_sub_wharf_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_sub_wharf_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_sub_wharf_vault"] = SceneNode(
        id="sunken_hollows_sub_wharf_vault",
        title="Underground Wharf - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. Flat-bottom barges moor at mossy stone docks.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="sunken_hollows_sub_wharf_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="sunken_hollows_sub_wharf_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_sub_wharf_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_sub_wharf_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_sub_wharf", label="Visit Underground", category="movement", target_scene="sunken_hollows_sub_wharf_gate", result_text="You travel to Underground Wharf.")
    )

    # POI: Steam Geyser Basin (10 nodes)
    scenes["sunken_hollows_geyser_basin_gate"] = SceneNode(
        id="sunken_hollows_geyser_basin_gate",
        title="Steam Geyser Basin - Outer Gate",
        region="sunken_hollows",
        description="Iron bars secure the heavy timber entrance. Warm mist rises from mineral-rich geothermal vents.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="sunken_hollows_geyser_basin_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="sunken_hollows_geyser_basin_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_geyser_basin_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_geyser_basin_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_geyser_basin_courtyard"] = SceneNode(
        id="sunken_hollows_geyser_basin_courtyard",
        title="Steam Geyser Basin - Main Courtyard",
        region="sunken_hollows",
        description="Cobblestones show heavy cart wheel wear. Warm mist rises from mineral-rich geothermal vents.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="sunken_hollows_geyser_basin_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="sunken_hollows_geyser_basin_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_geyser_basin_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_geyser_basin_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_geyser_basin_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_geyser_basin_quarters"] = SceneNode(
        id="sunken_hollows_geyser_basin_quarters",
        title="Steam Geyser Basin - Living Quarters",
        region="sunken_hollows",
        description="Rows of wooden bunks line the walls. Warm mist rises from mineral-rich geothermal vents.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="sunken_hollows_geyser_basin_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="sunken_hollows_geyser_basin_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_geyser_basin_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_geyser_basin_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_geyser_basin_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_geyser_basin_armory"] = SceneNode(
        id="sunken_hollows_geyser_basin_armory",
        title="Steam Geyser Basin - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. Warm mist rises from mineral-rich geothermal vents.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="sunken_hollows_geyser_basin_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="sunken_hollows_geyser_basin_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_geyser_basin_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_geyser_basin_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_geyser_basin_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_geyser_basin_cellar"] = SceneNode(
        id="sunken_hollows_geyser_basin_cellar",
        title="Steam Geyser Basin - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. Warm mist rises from mineral-rich geothermal vents.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="sunken_hollows_geyser_basin_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="sunken_hollows_geyser_basin_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_geyser_basin_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_geyser_basin_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_geyser_basin_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_geyser_basin_passage"] = SceneNode(
        id="sunken_hollows_geyser_basin_passage",
        title="Steam Geyser Basin - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. Warm mist rises from mineral-rich geothermal vents.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="sunken_hollows_geyser_basin_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="sunken_hollows_geyser_basin_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_geyser_basin_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_geyser_basin_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_geyser_basin_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_geyser_basin_chamber"] = SceneNode(
        id="sunken_hollows_geyser_basin_chamber",
        title="Steam Geyser Basin - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. Warm mist rises from mineral-rich geothermal vents.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="sunken_hollows_geyser_basin_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="sunken_hollows_geyser_basin_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_geyser_basin_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_geyser_basin_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_geyser_basin_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_geyser_basin_overlook"] = SceneNode(
        id="sunken_hollows_geyser_basin_overlook",
        title="Steam Geyser Basin - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. Warm mist rises from mineral-rich geothermal vents.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="sunken_hollows_geyser_basin_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="sunken_hollows_geyser_basin_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_geyser_basin_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_geyser_basin_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_geyser_basin_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_geyser_basin_sanctum"] = SceneNode(
        id="sunken_hollows_geyser_basin_sanctum",
        title="Steam Geyser Basin - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. Warm mist rises from mineral-rich geothermal vents.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="sunken_hollows_geyser_basin_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="sunken_hollows_geyser_basin_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_geyser_basin_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_geyser_basin_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_geyser_basin_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_geyser_basin_vault"] = SceneNode(
        id="sunken_hollows_geyser_basin_vault",
        title="Steam Geyser Basin - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. Warm mist rises from mineral-rich geothermal vents.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="sunken_hollows_geyser_basin_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="sunken_hollows_geyser_basin_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_geyser_basin_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_geyser_basin_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_geyser_basin", label="Visit Steam Geyser", category="movement", target_scene="sunken_hollows_geyser_basin_gate", result_text="You travel to Steam Geyser Basin.")
    )

    # POI: The Echoing Dome (10 nodes)
    scenes["sunken_hollows_echoing_dome_gate"] = SceneNode(
        id="sunken_hollows_echoing_dome_gate",
        title="The Echoing Dome - Outer Gate",
        region="sunken_hollows",
        description="Iron bars secure the heavy timber entrance. The huge dark caves carry quiet whispers for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="sunken_hollows_echoing_dome_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="sunken_hollows_echoing_dome_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_courtyard"] = SceneNode(
        id="sunken_hollows_echoing_dome_courtyard",
        title="The Echoing Dome - Main Courtyard",
        region="sunken_hollows",
        description="Cobblestones show heavy cart wheel wear. The huge dark caves carry quiet whispers for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="sunken_hollows_echoing_dome_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="sunken_hollows_echoing_dome_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_quarters"] = SceneNode(
        id="sunken_hollows_echoing_dome_quarters",
        title="The Echoing Dome - Living Quarters",
        region="sunken_hollows",
        description="Rows of wooden bunks line the walls. The huge dark caves carry quiet whispers for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="sunken_hollows_echoing_dome_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="sunken_hollows_echoing_dome_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_armory"] = SceneNode(
        id="sunken_hollows_echoing_dome_armory",
        title="The Echoing Dome - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. The huge dark caves carry quiet whispers for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="sunken_hollows_echoing_dome_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="sunken_hollows_echoing_dome_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_cellar"] = SceneNode(
        id="sunken_hollows_echoing_dome_cellar",
        title="The Echoing Dome - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. The huge dark caves carry quiet whispers for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="sunken_hollows_echoing_dome_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="sunken_hollows_echoing_dome_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_passage"] = SceneNode(
        id="sunken_hollows_echoing_dome_passage",
        title="The Echoing Dome - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. The huge dark caves carry quiet whispers for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="sunken_hollows_echoing_dome_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="sunken_hollows_echoing_dome_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_chamber"] = SceneNode(
        id="sunken_hollows_echoing_dome_chamber",
        title="The Echoing Dome - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. The huge dark caves carry quiet whispers for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="sunken_hollows_echoing_dome_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="sunken_hollows_echoing_dome_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_overlook"] = SceneNode(
        id="sunken_hollows_echoing_dome_overlook",
        title="The Echoing Dome - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. The huge dark caves carry quiet whispers for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="sunken_hollows_echoing_dome_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="sunken_hollows_echoing_dome_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_sanctum"] = SceneNode(
        id="sunken_hollows_echoing_dome_sanctum",
        title="The Echoing Dome - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. The huge dark caves carry quiet whispers for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="sunken_hollows_echoing_dome_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="sunken_hollows_echoing_dome_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_vault"] = SceneNode(
        id="sunken_hollows_echoing_dome_vault",
        title="The Echoing Dome - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. The huge dark caves carry quiet whispers for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="sunken_hollows_echoing_dome_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="sunken_hollows_echoing_dome_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_echoing_dome", label="Visit The Echoing", category="movement", target_scene="sunken_hollows_echoing_dome_gate", result_text="You travel to The Echoing Dome.")
    )

    return RegionManifest(
        id="sunken_hollows",
        name="The Sunken Abyss",
        mechanic_name="Water Buoyancy & Underwater Diving",
        mechanic_description="Comprehensive open-world region with 10 deep POIs.",
        scenes=scenes
    )