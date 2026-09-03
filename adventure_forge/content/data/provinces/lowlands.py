"""Province: The Lowlands.
Unique Mechanic: Social Stealth & Disguise.
"""
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action

def build_lowlands_province() -> RegionManifest:
    scenes = {}

    # Province Hub
    scenes["lowlands_hub"] = SceneNode(
        id="lowlands_hub",
        title="The Lowlands - Central Hub",
        region="lowlands",
        description="Barge horns echo along the river canal. City guards question passing dock workers.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_attribute": {"attribute": "strength", "value": 12}},
                text="Your military posture draws respectful nods from travelers."
            ),
        ],
        base_actions=[
            Action(id="lowlands_hub_scout", label="Scout hub", category="interaction", result_text="You survey the bustling provincial crossroads."),
            Action(id="lowlands_hub_rest", label="Rest at inn", category="interaction", effects=[{"modify_stamina": 5}], result_text="You rest and regain stamina."),
            Action(id="lowlands_to_bazaar", label="Go to Bazaar", category="movement", target_scene="bazaar_center", result_text="You travel along the highway to the Grand Bazaar."),
        ]
    )

    # POI: Port Oakhaven Docks (10 nodes)
    scenes["lowlands_oakhaven_port_gate"] = SceneNode(
        id="lowlands_oakhaven_port_gate",
        title="Port Oakhaven Docks - Outer Gate",
        region="lowlands",
        description="Iron bars secure the heavy timber entrance. Salt spray coats the wooden pier pilings.",
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
            Action(id="lowlands_oakhaven_port_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="lowlands_oakhaven_port_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="lowlands_oakhaven_port_gate_to_prev", label="Return back", category="movement", target_scene="lowlands_hub", result_text="You retrace your steps."),
            Action(id="lowlands_oakhaven_port_gate_to_next", label="Press forward", category="movement", target_scene="lowlands_oakhaven_port_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_oakhaven_port_courtyard"] = SceneNode(
        id="lowlands_oakhaven_port_courtyard",
        title="Port Oakhaven Docks - Main Courtyard",
        region="lowlands",
        description="Cobblestones show heavy cart wheel wear. Salt spray coats the wooden pier pilings.",
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
            Action(id="lowlands_oakhaven_port_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="lowlands_oakhaven_port_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="lowlands_oakhaven_port_courtyard_to_prev", label="Return back", category="movement", target_scene="lowlands_oakhaven_port_gate", result_text="You retrace your steps."),
            Action(id="lowlands_oakhaven_port_courtyard_to_next", label="Press forward", category="movement", target_scene="lowlands_oakhaven_port_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_oakhaven_port_quarters"] = SceneNode(
        id="lowlands_oakhaven_port_quarters",
        title="Port Oakhaven Docks - Living Quarters",
        region="lowlands",
        description="Rows of wooden bunks line the walls. Salt spray coats the wooden pier pilings.",
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
            Action(id="lowlands_oakhaven_port_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="lowlands_oakhaven_port_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="lowlands_oakhaven_port_quarters_to_prev", label="Return back", category="movement", target_scene="lowlands_oakhaven_port_courtyard", result_text="You retrace your steps."),
            Action(id="lowlands_oakhaven_port_quarters_to_next", label="Press forward", category="movement", target_scene="lowlands_oakhaven_port_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_oakhaven_port_armory"] = SceneNode(
        id="lowlands_oakhaven_port_armory",
        title="Port Oakhaven Docks - Supply Depot",
        region="lowlands",
        description="Crates of rations and tools stand stacked. Salt spray coats the wooden pier pilings.",
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
            Action(id="lowlands_oakhaven_port_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="lowlands_oakhaven_port_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="lowlands_oakhaven_port_armory_to_prev", label="Return back", category="movement", target_scene="lowlands_oakhaven_port_quarters", result_text="You retrace your steps."),
            Action(id="lowlands_oakhaven_port_armory_to_next", label="Press forward", category="movement", target_scene="lowlands_oakhaven_port_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_oakhaven_port_cellar"] = SceneNode(
        id="lowlands_oakhaven_port_cellar",
        title="Port Oakhaven Docks - Lower Cellar",
        region="lowlands",
        description="Damp air smells of cool earth and storage. Salt spray coats the wooden pier pilings.",
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
            Action(id="lowlands_oakhaven_port_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="lowlands_oakhaven_port_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="lowlands_oakhaven_port_cellar_to_prev", label="Return back", category="movement", target_scene="lowlands_oakhaven_port_armory", result_text="You retrace your steps."),
            Action(id="lowlands_oakhaven_port_cellar_to_next", label="Press forward", category="movement", target_scene="lowlands_oakhaven_port_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_oakhaven_port_passage"] = SceneNode(
        id="lowlands_oakhaven_port_passage",
        title="Port Oakhaven Docks - Stone Corridor",
        region="lowlands",
        description="Wall sconces hold flickering tallow candles. Salt spray coats the wooden pier pilings.",
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
            Action(id="lowlands_oakhaven_port_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="lowlands_oakhaven_port_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="lowlands_oakhaven_port_passage_to_prev", label="Return back", category="movement", target_scene="lowlands_oakhaven_port_cellar", result_text="You retrace your steps."),
            Action(id="lowlands_oakhaven_port_passage_to_next", label="Press forward", category="movement", target_scene="lowlands_oakhaven_port_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_oakhaven_port_chamber"] = SceneNode(
        id="lowlands_oakhaven_port_chamber",
        title="Port Oakhaven Docks - Inner Chamber",
        region="lowlands",
        description="A sturdy oak desk holds ledgers and maps. Salt spray coats the wooden pier pilings.",
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
            Action(id="lowlands_oakhaven_port_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="lowlands_oakhaven_port_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="lowlands_oakhaven_port_chamber_to_prev", label="Return back", category="movement", target_scene="lowlands_oakhaven_port_passage", result_text="You retrace your steps."),
            Action(id="lowlands_oakhaven_port_chamber_to_next", label="Press forward", category="movement", target_scene="lowlands_oakhaven_port_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_oakhaven_port_overlook"] = SceneNode(
        id="lowlands_oakhaven_port_overlook",
        title="Port Oakhaven Docks - High Overlook",
        region="lowlands",
        description="A stone ledge provides a clear view. Salt spray coats the wooden pier pilings.",
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
            Action(id="lowlands_oakhaven_port_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="lowlands_oakhaven_port_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="lowlands_oakhaven_port_overlook_to_prev", label="Return back", category="movement", target_scene="lowlands_oakhaven_port_chamber", result_text="You retrace your steps."),
            Action(id="lowlands_oakhaven_port_overlook_to_next", label="Press forward", category="movement", target_scene="lowlands_oakhaven_port_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_oakhaven_port_sanctum"] = SceneNode(
        id="lowlands_oakhaven_port_sanctum",
        title="Port Oakhaven Docks - Inner Sanctum",
        region="lowlands",
        description="A stone altar stands in quiet reverence. Salt spray coats the wooden pier pilings.",
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
            Action(id="lowlands_oakhaven_port_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="lowlands_oakhaven_port_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="lowlands_oakhaven_port_sanctum_to_prev", label="Return back", category="movement", target_scene="lowlands_oakhaven_port_overlook", result_text="You retrace your steps."),
            Action(id="lowlands_oakhaven_port_sanctum_to_next", label="Press forward", category="movement", target_scene="lowlands_oakhaven_port_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_oakhaven_port_vault"] = SceneNode(
        id="lowlands_oakhaven_port_vault",
        title="Port Oakhaven Docks - Deep Vault",
        region="lowlands",
        description="Iron-banded chests sit in deep shadows. Salt spray coats the wooden pier pilings.",
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
            Action(id="lowlands_oakhaven_port_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="lowlands_oakhaven_port_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="lowlands_oakhaven_port_vault_to_prev", label="Return back", category="movement", target_scene="lowlands_oakhaven_port_sanctum", result_text="You retrace your steps."),
            Action(id="lowlands_oakhaven_port_vault_to_hub", label="Return to Hub", category="movement", target_scene="lowlands_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["lowlands_hub"].base_actions.append(
        Action(id="lowlands_hub_to_oakhaven_port", label="Visit Port Oakhave", category="movement", target_scene="lowlands_oakhaven_port_gate", result_text="You travel to Port Oakhaven Docks.")
    )

    # POI: Shadow Cellar (10 nodes)
    scenes["lowlands_thieves_hall_gate"] = SceneNode(
        id="lowlands_thieves_hall_gate",
        title="Shadow Cellar - Outer Gate",
        region="lowlands",
        description="Iron bars secure the heavy timber entrance. Masked smugglers barter contraband under dim lamps.",
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
            Action(id="lowlands_thieves_hall_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="lowlands_thieves_hall_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="lowlands_thieves_hall_gate_to_prev", label="Return back", category="movement", target_scene="lowlands_hub", result_text="You retrace your steps."),
            Action(id="lowlands_thieves_hall_gate_to_next", label="Press forward", category="movement", target_scene="lowlands_thieves_hall_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_thieves_hall_courtyard"] = SceneNode(
        id="lowlands_thieves_hall_courtyard",
        title="Shadow Cellar - Main Courtyard",
        region="lowlands",
        description="Cobblestones show heavy cart wheel wear. Masked smugglers barter contraband under dim lamps.",
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
            Action(id="lowlands_thieves_hall_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="lowlands_thieves_hall_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="lowlands_thieves_hall_courtyard_to_prev", label="Return back", category="movement", target_scene="lowlands_thieves_hall_gate", result_text="You retrace your steps."),
            Action(id="lowlands_thieves_hall_courtyard_to_next", label="Press forward", category="movement", target_scene="lowlands_thieves_hall_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_thieves_hall_quarters"] = SceneNode(
        id="lowlands_thieves_hall_quarters",
        title="Shadow Cellar - Living Quarters",
        region="lowlands",
        description="Rows of wooden bunks line the walls. Masked smugglers barter contraband under dim lamps.",
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
            Action(id="lowlands_thieves_hall_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="lowlands_thieves_hall_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="lowlands_thieves_hall_quarters_to_prev", label="Return back", category="movement", target_scene="lowlands_thieves_hall_courtyard", result_text="You retrace your steps."),
            Action(id="lowlands_thieves_hall_quarters_to_next", label="Press forward", category="movement", target_scene="lowlands_thieves_hall_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_thieves_hall_armory"] = SceneNode(
        id="lowlands_thieves_hall_armory",
        title="Shadow Cellar - Supply Depot",
        region="lowlands",
        description="Crates of rations and tools stand stacked. Masked smugglers barter contraband under dim lamps.",
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
            Action(id="lowlands_thieves_hall_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="lowlands_thieves_hall_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="lowlands_thieves_hall_armory_to_prev", label="Return back", category="movement", target_scene="lowlands_thieves_hall_quarters", result_text="You retrace your steps."),
            Action(id="lowlands_thieves_hall_armory_to_next", label="Press forward", category="movement", target_scene="lowlands_thieves_hall_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_thieves_hall_cellar"] = SceneNode(
        id="lowlands_thieves_hall_cellar",
        title="Shadow Cellar - Lower Cellar",
        region="lowlands",
        description="Damp air smells of cool earth and storage. Masked smugglers barter contraband under dim lamps.",
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
            Action(id="lowlands_thieves_hall_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="lowlands_thieves_hall_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="lowlands_thieves_hall_cellar_to_prev", label="Return back", category="movement", target_scene="lowlands_thieves_hall_armory", result_text="You retrace your steps."),
            Action(id="lowlands_thieves_hall_cellar_to_next", label="Press forward", category="movement", target_scene="lowlands_thieves_hall_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_thieves_hall_passage"] = SceneNode(
        id="lowlands_thieves_hall_passage",
        title="Shadow Cellar - Stone Corridor",
        region="lowlands",
        description="Wall sconces hold flickering tallow candles. Masked smugglers barter contraband under dim lamps.",
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
            Action(id="lowlands_thieves_hall_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="lowlands_thieves_hall_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="lowlands_thieves_hall_passage_to_prev", label="Return back", category="movement", target_scene="lowlands_thieves_hall_cellar", result_text="You retrace your steps."),
            Action(id="lowlands_thieves_hall_passage_to_next", label="Press forward", category="movement", target_scene="lowlands_thieves_hall_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_thieves_hall_chamber"] = SceneNode(
        id="lowlands_thieves_hall_chamber",
        title="Shadow Cellar - Inner Chamber",
        region="lowlands",
        description="A sturdy oak desk holds ledgers and maps. Masked smugglers barter contraband under dim lamps.",
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
            Action(id="lowlands_thieves_hall_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="lowlands_thieves_hall_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="lowlands_thieves_hall_chamber_to_prev", label="Return back", category="movement", target_scene="lowlands_thieves_hall_passage", result_text="You retrace your steps."),
            Action(id="lowlands_thieves_hall_chamber_to_next", label="Press forward", category="movement", target_scene="lowlands_thieves_hall_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_thieves_hall_overlook"] = SceneNode(
        id="lowlands_thieves_hall_overlook",
        title="Shadow Cellar - High Overlook",
        region="lowlands",
        description="A stone ledge provides a clear view. Masked smugglers barter contraband under dim lamps.",
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
            Action(id="lowlands_thieves_hall_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="lowlands_thieves_hall_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="lowlands_thieves_hall_overlook_to_prev", label="Return back", category="movement", target_scene="lowlands_thieves_hall_chamber", result_text="You retrace your steps."),
            Action(id="lowlands_thieves_hall_overlook_to_next", label="Press forward", category="movement", target_scene="lowlands_thieves_hall_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_thieves_hall_sanctum"] = SceneNode(
        id="lowlands_thieves_hall_sanctum",
        title="Shadow Cellar - Inner Sanctum",
        region="lowlands",
        description="A stone altar stands in quiet reverence. Masked smugglers barter contraband under dim lamps.",
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
            Action(id="lowlands_thieves_hall_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="lowlands_thieves_hall_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="lowlands_thieves_hall_sanctum_to_prev", label="Return back", category="movement", target_scene="lowlands_thieves_hall_overlook", result_text="You retrace your steps."),
            Action(id="lowlands_thieves_hall_sanctum_to_next", label="Press forward", category="movement", target_scene="lowlands_thieves_hall_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_thieves_hall_vault"] = SceneNode(
        id="lowlands_thieves_hall_vault",
        title="Shadow Cellar - Deep Vault",
        region="lowlands",
        description="Iron-banded chests sit in deep shadows. Masked smugglers barter contraband under dim lamps.",
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
            Action(id="lowlands_thieves_hall_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="lowlands_thieves_hall_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="lowlands_thieves_hall_vault_to_prev", label="Return back", category="movement", target_scene="lowlands_thieves_hall_sanctum", result_text="You retrace your steps."),
            Action(id="lowlands_thieves_hall_vault_to_hub", label="Return to Hub", category="movement", target_scene="lowlands_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["lowlands_hub"].base_actions.append(
        Action(id="lowlands_hub_to_thieves_hall", label="Visit Shadow Cella", category="movement", target_scene="lowlands_thieves_hall_gate", result_text="You travel to Shadow Cellar.")
    )

    # POI: Great Canal Sluice (10 nodes)
    scenes["lowlands_canal_sluice_gate"] = SceneNode(
        id="lowlands_canal_sluice_gate",
        title="Great Canal Sluice - Outer Gate",
        region="lowlands",
        description="Iron bars secure the heavy timber entrance. Heavy water wheels turn inside brick housings.",
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
            Action(id="lowlands_canal_sluice_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="lowlands_canal_sluice_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="lowlands_canal_sluice_gate_to_prev", label="Return back", category="movement", target_scene="lowlands_hub", result_text="You retrace your steps."),
            Action(id="lowlands_canal_sluice_gate_to_next", label="Press forward", category="movement", target_scene="lowlands_canal_sluice_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_canal_sluice_courtyard"] = SceneNode(
        id="lowlands_canal_sluice_courtyard",
        title="Great Canal Sluice - Main Courtyard",
        region="lowlands",
        description="Cobblestones show heavy cart wheel wear. Heavy water wheels turn inside brick housings.",
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
            Action(id="lowlands_canal_sluice_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="lowlands_canal_sluice_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="lowlands_canal_sluice_courtyard_to_prev", label="Return back", category="movement", target_scene="lowlands_canal_sluice_gate", result_text="You retrace your steps."),
            Action(id="lowlands_canal_sluice_courtyard_to_next", label="Press forward", category="movement", target_scene="lowlands_canal_sluice_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_canal_sluice_quarters"] = SceneNode(
        id="lowlands_canal_sluice_quarters",
        title="Great Canal Sluice - Living Quarters",
        region="lowlands",
        description="Rows of wooden bunks line the walls. Heavy water wheels turn inside brick housings.",
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
            Action(id="lowlands_canal_sluice_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="lowlands_canal_sluice_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="lowlands_canal_sluice_quarters_to_prev", label="Return back", category="movement", target_scene="lowlands_canal_sluice_courtyard", result_text="You retrace your steps."),
            Action(id="lowlands_canal_sluice_quarters_to_next", label="Press forward", category="movement", target_scene="lowlands_canal_sluice_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_canal_sluice_armory"] = SceneNode(
        id="lowlands_canal_sluice_armory",
        title="Great Canal Sluice - Supply Depot",
        region="lowlands",
        description="Crates of rations and tools stand stacked. Heavy water wheels turn inside brick housings.",
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
            Action(id="lowlands_canal_sluice_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="lowlands_canal_sluice_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="lowlands_canal_sluice_armory_to_prev", label="Return back", category="movement", target_scene="lowlands_canal_sluice_quarters", result_text="You retrace your steps."),
            Action(id="lowlands_canal_sluice_armory_to_next", label="Press forward", category="movement", target_scene="lowlands_canal_sluice_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_canal_sluice_cellar"] = SceneNode(
        id="lowlands_canal_sluice_cellar",
        title="Great Canal Sluice - Lower Cellar",
        region="lowlands",
        description="Damp air smells of cool earth and storage. Heavy water wheels turn inside brick housings.",
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
            Action(id="lowlands_canal_sluice_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="lowlands_canal_sluice_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="lowlands_canal_sluice_cellar_to_prev", label="Return back", category="movement", target_scene="lowlands_canal_sluice_armory", result_text="You retrace your steps."),
            Action(id="lowlands_canal_sluice_cellar_to_next", label="Press forward", category="movement", target_scene="lowlands_canal_sluice_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_canal_sluice_passage"] = SceneNode(
        id="lowlands_canal_sluice_passage",
        title="Great Canal Sluice - Stone Corridor",
        region="lowlands",
        description="Wall sconces hold flickering tallow candles. Heavy water wheels turn inside brick housings.",
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
            Action(id="lowlands_canal_sluice_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="lowlands_canal_sluice_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="lowlands_canal_sluice_passage_to_prev", label="Return back", category="movement", target_scene="lowlands_canal_sluice_cellar", result_text="You retrace your steps."),
            Action(id="lowlands_canal_sluice_passage_to_next", label="Press forward", category="movement", target_scene="lowlands_canal_sluice_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_canal_sluice_chamber"] = SceneNode(
        id="lowlands_canal_sluice_chamber",
        title="Great Canal Sluice - Inner Chamber",
        region="lowlands",
        description="A sturdy oak desk holds ledgers and maps. Heavy water wheels turn inside brick housings.",
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
            Action(id="lowlands_canal_sluice_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="lowlands_canal_sluice_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="lowlands_canal_sluice_chamber_to_prev", label="Return back", category="movement", target_scene="lowlands_canal_sluice_passage", result_text="You retrace your steps."),
            Action(id="lowlands_canal_sluice_chamber_to_next", label="Press forward", category="movement", target_scene="lowlands_canal_sluice_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_canal_sluice_overlook"] = SceneNode(
        id="lowlands_canal_sluice_overlook",
        title="Great Canal Sluice - High Overlook",
        region="lowlands",
        description="A stone ledge provides a clear view. Heavy water wheels turn inside brick housings.",
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
            Action(id="lowlands_canal_sluice_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="lowlands_canal_sluice_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="lowlands_canal_sluice_overlook_to_prev", label="Return back", category="movement", target_scene="lowlands_canal_sluice_chamber", result_text="You retrace your steps."),
            Action(id="lowlands_canal_sluice_overlook_to_next", label="Press forward", category="movement", target_scene="lowlands_canal_sluice_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_canal_sluice_sanctum"] = SceneNode(
        id="lowlands_canal_sluice_sanctum",
        title="Great Canal Sluice - Inner Sanctum",
        region="lowlands",
        description="A stone altar stands in quiet reverence. Heavy water wheels turn inside brick housings.",
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
            Action(id="lowlands_canal_sluice_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="lowlands_canal_sluice_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="lowlands_canal_sluice_sanctum_to_prev", label="Return back", category="movement", target_scene="lowlands_canal_sluice_overlook", result_text="You retrace your steps."),
            Action(id="lowlands_canal_sluice_sanctum_to_next", label="Press forward", category="movement", target_scene="lowlands_canal_sluice_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_canal_sluice_vault"] = SceneNode(
        id="lowlands_canal_sluice_vault",
        title="Great Canal Sluice - Deep Vault",
        region="lowlands",
        description="Iron-banded chests sit in deep shadows. Heavy water wheels turn inside brick housings.",
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
            Action(id="lowlands_canal_sluice_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="lowlands_canal_sluice_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="lowlands_canal_sluice_vault_to_prev", label="Return back", category="movement", target_scene="lowlands_canal_sluice_sanctum", result_text="You retrace your steps."),
            Action(id="lowlands_canal_sluice_vault_to_hub", label="Return to Hub", category="movement", target_scene="lowlands_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["lowlands_hub"].base_actions.append(
        Action(id="lowlands_hub_to_canal_sluice", label="Visit Great Canal", category="movement", target_scene="lowlands_canal_sluice_gate", result_text="You travel to Great Canal Sluice.")
    )

    # POI: Anchor & Chain Inn (10 nodes)
    scenes["lowlands_dock_tavern_gate"] = SceneNode(
        id="lowlands_dock_tavern_gate",
        title="Anchor & Chain Inn - Outer Gate",
        region="lowlands",
        description="Iron bars secure the heavy timber entrance. Drunken sailors sing around wooden bench tables.",
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
            Action(id="lowlands_dock_tavern_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="lowlands_dock_tavern_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="lowlands_dock_tavern_gate_to_prev", label="Return back", category="movement", target_scene="lowlands_hub", result_text="You retrace your steps."),
            Action(id="lowlands_dock_tavern_gate_to_next", label="Press forward", category="movement", target_scene="lowlands_dock_tavern_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_dock_tavern_courtyard"] = SceneNode(
        id="lowlands_dock_tavern_courtyard",
        title="Anchor & Chain Inn - Main Courtyard",
        region="lowlands",
        description="Cobblestones show heavy cart wheel wear. Drunken sailors sing around wooden bench tables.",
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
            Action(id="lowlands_dock_tavern_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="lowlands_dock_tavern_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="lowlands_dock_tavern_courtyard_to_prev", label="Return back", category="movement", target_scene="lowlands_dock_tavern_gate", result_text="You retrace your steps."),
            Action(id="lowlands_dock_tavern_courtyard_to_next", label="Press forward", category="movement", target_scene="lowlands_dock_tavern_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_dock_tavern_quarters"] = SceneNode(
        id="lowlands_dock_tavern_quarters",
        title="Anchor & Chain Inn - Living Quarters",
        region="lowlands",
        description="Rows of wooden bunks line the walls. Drunken sailors sing around wooden bench tables.",
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
            Action(id="lowlands_dock_tavern_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="lowlands_dock_tavern_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="lowlands_dock_tavern_quarters_to_prev", label="Return back", category="movement", target_scene="lowlands_dock_tavern_courtyard", result_text="You retrace your steps."),
            Action(id="lowlands_dock_tavern_quarters_to_next", label="Press forward", category="movement", target_scene="lowlands_dock_tavern_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_dock_tavern_armory"] = SceneNode(
        id="lowlands_dock_tavern_armory",
        title="Anchor & Chain Inn - Supply Depot",
        region="lowlands",
        description="Crates of rations and tools stand stacked. Drunken sailors sing around wooden bench tables.",
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
            Action(id="lowlands_dock_tavern_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="lowlands_dock_tavern_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="lowlands_dock_tavern_armory_to_prev", label="Return back", category="movement", target_scene="lowlands_dock_tavern_quarters", result_text="You retrace your steps."),
            Action(id="lowlands_dock_tavern_armory_to_next", label="Press forward", category="movement", target_scene="lowlands_dock_tavern_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_dock_tavern_cellar"] = SceneNode(
        id="lowlands_dock_tavern_cellar",
        title="Anchor & Chain Inn - Lower Cellar",
        region="lowlands",
        description="Damp air smells of cool earth and storage. Drunken sailors sing around wooden bench tables.",
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
            Action(id="lowlands_dock_tavern_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="lowlands_dock_tavern_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="lowlands_dock_tavern_cellar_to_prev", label="Return back", category="movement", target_scene="lowlands_dock_tavern_armory", result_text="You retrace your steps."),
            Action(id="lowlands_dock_tavern_cellar_to_next", label="Press forward", category="movement", target_scene="lowlands_dock_tavern_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_dock_tavern_passage"] = SceneNode(
        id="lowlands_dock_tavern_passage",
        title="Anchor & Chain Inn - Stone Corridor",
        region="lowlands",
        description="Wall sconces hold flickering tallow candles. Drunken sailors sing around wooden bench tables.",
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
            Action(id="lowlands_dock_tavern_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="lowlands_dock_tavern_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="lowlands_dock_tavern_passage_to_prev", label="Return back", category="movement", target_scene="lowlands_dock_tavern_cellar", result_text="You retrace your steps."),
            Action(id="lowlands_dock_tavern_passage_to_next", label="Press forward", category="movement", target_scene="lowlands_dock_tavern_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_dock_tavern_chamber"] = SceneNode(
        id="lowlands_dock_tavern_chamber",
        title="Anchor & Chain Inn - Inner Chamber",
        region="lowlands",
        description="A sturdy oak desk holds ledgers and maps. Drunken sailors sing around wooden bench tables.",
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
            Action(id="lowlands_dock_tavern_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="lowlands_dock_tavern_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="lowlands_dock_tavern_chamber_to_prev", label="Return back", category="movement", target_scene="lowlands_dock_tavern_passage", result_text="You retrace your steps."),
            Action(id="lowlands_dock_tavern_chamber_to_next", label="Press forward", category="movement", target_scene="lowlands_dock_tavern_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_dock_tavern_overlook"] = SceneNode(
        id="lowlands_dock_tavern_overlook",
        title="Anchor & Chain Inn - High Overlook",
        region="lowlands",
        description="A stone ledge provides a clear view. Drunken sailors sing around wooden bench tables.",
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
            Action(id="lowlands_dock_tavern_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="lowlands_dock_tavern_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="lowlands_dock_tavern_overlook_to_prev", label="Return back", category="movement", target_scene="lowlands_dock_tavern_chamber", result_text="You retrace your steps."),
            Action(id="lowlands_dock_tavern_overlook_to_next", label="Press forward", category="movement", target_scene="lowlands_dock_tavern_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_dock_tavern_sanctum"] = SceneNode(
        id="lowlands_dock_tavern_sanctum",
        title="Anchor & Chain Inn - Inner Sanctum",
        region="lowlands",
        description="A stone altar stands in quiet reverence. Drunken sailors sing around wooden bench tables.",
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
            Action(id="lowlands_dock_tavern_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="lowlands_dock_tavern_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="lowlands_dock_tavern_sanctum_to_prev", label="Return back", category="movement", target_scene="lowlands_dock_tavern_overlook", result_text="You retrace your steps."),
            Action(id="lowlands_dock_tavern_sanctum_to_next", label="Press forward", category="movement", target_scene="lowlands_dock_tavern_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_dock_tavern_vault"] = SceneNode(
        id="lowlands_dock_tavern_vault",
        title="Anchor & Chain Inn - Deep Vault",
        region="lowlands",
        description="Iron-banded chests sit in deep shadows. Drunken sailors sing around wooden bench tables.",
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
            Action(id="lowlands_dock_tavern_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="lowlands_dock_tavern_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="lowlands_dock_tavern_vault_to_prev", label="Return back", category="movement", target_scene="lowlands_dock_tavern_sanctum", result_text="You retrace your steps."),
            Action(id="lowlands_dock_tavern_vault_to_hub", label="Return to Hub", category="movement", target_scene="lowlands_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["lowlands_hub"].base_actions.append(
        Action(id="lowlands_hub_to_dock_tavern", label="Visit Anchor & Cha", category="movement", target_scene="lowlands_dock_tavern_gate", result_text="You travel to Anchor & Chain Inn.")
    )

    # POI: Weavers District (10 nodes)
    scenes["lowlands_cloth_market_gate"] = SceneNode(
        id="lowlands_cloth_market_gate",
        title="Weavers District - Outer Gate",
        region="lowlands",
        description="Iron bars secure the heavy timber entrance. Dyed linens hang drying across the alleyways.",
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
            Action(id="lowlands_cloth_market_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="lowlands_cloth_market_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="lowlands_cloth_market_gate_to_prev", label="Return back", category="movement", target_scene="lowlands_hub", result_text="You retrace your steps."),
            Action(id="lowlands_cloth_market_gate_to_next", label="Press forward", category="movement", target_scene="lowlands_cloth_market_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_cloth_market_courtyard"] = SceneNode(
        id="lowlands_cloth_market_courtyard",
        title="Weavers District - Main Courtyard",
        region="lowlands",
        description="Cobblestones show heavy cart wheel wear. Dyed linens hang drying across the alleyways.",
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
            Action(id="lowlands_cloth_market_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="lowlands_cloth_market_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="lowlands_cloth_market_courtyard_to_prev", label="Return back", category="movement", target_scene="lowlands_cloth_market_gate", result_text="You retrace your steps."),
            Action(id="lowlands_cloth_market_courtyard_to_next", label="Press forward", category="movement", target_scene="lowlands_cloth_market_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_cloth_market_quarters"] = SceneNode(
        id="lowlands_cloth_market_quarters",
        title="Weavers District - Living Quarters",
        region="lowlands",
        description="Rows of wooden bunks line the walls. Dyed linens hang drying across the alleyways.",
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
            Action(id="lowlands_cloth_market_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="lowlands_cloth_market_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="lowlands_cloth_market_quarters_to_prev", label="Return back", category="movement", target_scene="lowlands_cloth_market_courtyard", result_text="You retrace your steps."),
            Action(id="lowlands_cloth_market_quarters_to_next", label="Press forward", category="movement", target_scene="lowlands_cloth_market_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_cloth_market_armory"] = SceneNode(
        id="lowlands_cloth_market_armory",
        title="Weavers District - Supply Depot",
        region="lowlands",
        description="Crates of rations and tools stand stacked. Dyed linens hang drying across the alleyways.",
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
            Action(id="lowlands_cloth_market_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="lowlands_cloth_market_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="lowlands_cloth_market_armory_to_prev", label="Return back", category="movement", target_scene="lowlands_cloth_market_quarters", result_text="You retrace your steps."),
            Action(id="lowlands_cloth_market_armory_to_next", label="Press forward", category="movement", target_scene="lowlands_cloth_market_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_cloth_market_cellar"] = SceneNode(
        id="lowlands_cloth_market_cellar",
        title="Weavers District - Lower Cellar",
        region="lowlands",
        description="Damp air smells of cool earth and storage. Dyed linens hang drying across the alleyways.",
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
            Action(id="lowlands_cloth_market_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="lowlands_cloth_market_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="lowlands_cloth_market_cellar_to_prev", label="Return back", category="movement", target_scene="lowlands_cloth_market_armory", result_text="You retrace your steps."),
            Action(id="lowlands_cloth_market_cellar_to_next", label="Press forward", category="movement", target_scene="lowlands_cloth_market_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_cloth_market_passage"] = SceneNode(
        id="lowlands_cloth_market_passage",
        title="Weavers District - Stone Corridor",
        region="lowlands",
        description="Wall sconces hold flickering tallow candles. Dyed linens hang drying across the alleyways.",
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
            Action(id="lowlands_cloth_market_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="lowlands_cloth_market_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="lowlands_cloth_market_passage_to_prev", label="Return back", category="movement", target_scene="lowlands_cloth_market_cellar", result_text="You retrace your steps."),
            Action(id="lowlands_cloth_market_passage_to_next", label="Press forward", category="movement", target_scene="lowlands_cloth_market_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_cloth_market_chamber"] = SceneNode(
        id="lowlands_cloth_market_chamber",
        title="Weavers District - Inner Chamber",
        region="lowlands",
        description="A sturdy oak desk holds ledgers and maps. Dyed linens hang drying across the alleyways.",
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
            Action(id="lowlands_cloth_market_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="lowlands_cloth_market_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="lowlands_cloth_market_chamber_to_prev", label="Return back", category="movement", target_scene="lowlands_cloth_market_passage", result_text="You retrace your steps."),
            Action(id="lowlands_cloth_market_chamber_to_next", label="Press forward", category="movement", target_scene="lowlands_cloth_market_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_cloth_market_overlook"] = SceneNode(
        id="lowlands_cloth_market_overlook",
        title="Weavers District - High Overlook",
        region="lowlands",
        description="A stone ledge provides a clear view. Dyed linens hang drying across the alleyways.",
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
            Action(id="lowlands_cloth_market_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="lowlands_cloth_market_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="lowlands_cloth_market_overlook_to_prev", label="Return back", category="movement", target_scene="lowlands_cloth_market_chamber", result_text="You retrace your steps."),
            Action(id="lowlands_cloth_market_overlook_to_next", label="Press forward", category="movement", target_scene="lowlands_cloth_market_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_cloth_market_sanctum"] = SceneNode(
        id="lowlands_cloth_market_sanctum",
        title="Weavers District - Inner Sanctum",
        region="lowlands",
        description="A stone altar stands in quiet reverence. Dyed linens hang drying across the alleyways.",
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
            Action(id="lowlands_cloth_market_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="lowlands_cloth_market_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="lowlands_cloth_market_sanctum_to_prev", label="Return back", category="movement", target_scene="lowlands_cloth_market_overlook", result_text="You retrace your steps."),
            Action(id="lowlands_cloth_market_sanctum_to_next", label="Press forward", category="movement", target_scene="lowlands_cloth_market_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_cloth_market_vault"] = SceneNode(
        id="lowlands_cloth_market_vault",
        title="Weavers District - Deep Vault",
        region="lowlands",
        description="Iron-banded chests sit in deep shadows. Dyed linens hang drying across the alleyways.",
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
            Action(id="lowlands_cloth_market_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="lowlands_cloth_market_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="lowlands_cloth_market_vault_to_prev", label="Return back", category="movement", target_scene="lowlands_cloth_market_sanctum", result_text="You retrace your steps."),
            Action(id="lowlands_cloth_market_vault_to_hub", label="Return to Hub", category="movement", target_scene="lowlands_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["lowlands_hub"].base_actions.append(
        Action(id="lowlands_hub_to_cloth_market", label="Visit Weavers Dist", category="movement", target_scene="lowlands_cloth_market_gate", result_text="You travel to Weavers District.")
    )

    # POI: Sunken Smuggler Cove (10 nodes)
    scenes["lowlands_smuggler_cove_gate"] = SceneNode(
        id="lowlands_smuggler_cove_gate",
        title="Sunken Smuggler Cove - Outer Gate",
        region="lowlands",
        description="Iron bars secure the heavy timber entrance. Rowboats moor inside sea caverns at low tide.",
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
            Action(id="lowlands_smuggler_cove_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="lowlands_smuggler_cove_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="lowlands_smuggler_cove_gate_to_prev", label="Return back", category="movement", target_scene="lowlands_hub", result_text="You retrace your steps."),
            Action(id="lowlands_smuggler_cove_gate_to_next", label="Press forward", category="movement", target_scene="lowlands_smuggler_cove_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_smuggler_cove_courtyard"] = SceneNode(
        id="lowlands_smuggler_cove_courtyard",
        title="Sunken Smuggler Cove - Main Courtyard",
        region="lowlands",
        description="Cobblestones show heavy cart wheel wear. Rowboats moor inside sea caverns at low tide.",
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
            Action(id="lowlands_smuggler_cove_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="lowlands_smuggler_cove_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="lowlands_smuggler_cove_courtyard_to_prev", label="Return back", category="movement", target_scene="lowlands_smuggler_cove_gate", result_text="You retrace your steps."),
            Action(id="lowlands_smuggler_cove_courtyard_to_next", label="Press forward", category="movement", target_scene="lowlands_smuggler_cove_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_smuggler_cove_quarters"] = SceneNode(
        id="lowlands_smuggler_cove_quarters",
        title="Sunken Smuggler Cove - Living Quarters",
        region="lowlands",
        description="Rows of wooden bunks line the walls. Rowboats moor inside sea caverns at low tide.",
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
            Action(id="lowlands_smuggler_cove_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="lowlands_smuggler_cove_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="lowlands_smuggler_cove_quarters_to_prev", label="Return back", category="movement", target_scene="lowlands_smuggler_cove_courtyard", result_text="You retrace your steps."),
            Action(id="lowlands_smuggler_cove_quarters_to_next", label="Press forward", category="movement", target_scene="lowlands_smuggler_cove_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_smuggler_cove_armory"] = SceneNode(
        id="lowlands_smuggler_cove_armory",
        title="Sunken Smuggler Cove - Supply Depot",
        region="lowlands",
        description="Crates of rations and tools stand stacked. Rowboats moor inside sea caverns at low tide.",
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
            Action(id="lowlands_smuggler_cove_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="lowlands_smuggler_cove_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="lowlands_smuggler_cove_armory_to_prev", label="Return back", category="movement", target_scene="lowlands_smuggler_cove_quarters", result_text="You retrace your steps."),
            Action(id="lowlands_smuggler_cove_armory_to_next", label="Press forward", category="movement", target_scene="lowlands_smuggler_cove_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_smuggler_cove_cellar"] = SceneNode(
        id="lowlands_smuggler_cove_cellar",
        title="Sunken Smuggler Cove - Lower Cellar",
        region="lowlands",
        description="Damp air smells of cool earth and storage. Rowboats moor inside sea caverns at low tide.",
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
            Action(id="lowlands_smuggler_cove_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="lowlands_smuggler_cove_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="lowlands_smuggler_cove_cellar_to_prev", label="Return back", category="movement", target_scene="lowlands_smuggler_cove_armory", result_text="You retrace your steps."),
            Action(id="lowlands_smuggler_cove_cellar_to_next", label="Press forward", category="movement", target_scene="lowlands_smuggler_cove_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_smuggler_cove_passage"] = SceneNode(
        id="lowlands_smuggler_cove_passage",
        title="Sunken Smuggler Cove - Stone Corridor",
        region="lowlands",
        description="Wall sconces hold flickering tallow candles. Rowboats moor inside sea caverns at low tide.",
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
            Action(id="lowlands_smuggler_cove_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="lowlands_smuggler_cove_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="lowlands_smuggler_cove_passage_to_prev", label="Return back", category="movement", target_scene="lowlands_smuggler_cove_cellar", result_text="You retrace your steps."),
            Action(id="lowlands_smuggler_cove_passage_to_next", label="Press forward", category="movement", target_scene="lowlands_smuggler_cove_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_smuggler_cove_chamber"] = SceneNode(
        id="lowlands_smuggler_cove_chamber",
        title="Sunken Smuggler Cove - Inner Chamber",
        region="lowlands",
        description="A sturdy oak desk holds ledgers and maps. Rowboats moor inside sea caverns at low tide.",
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
            Action(id="lowlands_smuggler_cove_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="lowlands_smuggler_cove_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="lowlands_smuggler_cove_chamber_to_prev", label="Return back", category="movement", target_scene="lowlands_smuggler_cove_passage", result_text="You retrace your steps."),
            Action(id="lowlands_smuggler_cove_chamber_to_next", label="Press forward", category="movement", target_scene="lowlands_smuggler_cove_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_smuggler_cove_overlook"] = SceneNode(
        id="lowlands_smuggler_cove_overlook",
        title="Sunken Smuggler Cove - High Overlook",
        region="lowlands",
        description="A stone ledge provides a clear view. Rowboats moor inside sea caverns at low tide.",
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
            Action(id="lowlands_smuggler_cove_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="lowlands_smuggler_cove_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="lowlands_smuggler_cove_overlook_to_prev", label="Return back", category="movement", target_scene="lowlands_smuggler_cove_chamber", result_text="You retrace your steps."),
            Action(id="lowlands_smuggler_cove_overlook_to_next", label="Press forward", category="movement", target_scene="lowlands_smuggler_cove_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_smuggler_cove_sanctum"] = SceneNode(
        id="lowlands_smuggler_cove_sanctum",
        title="Sunken Smuggler Cove - Inner Sanctum",
        region="lowlands",
        description="A stone altar stands in quiet reverence. Rowboats moor inside sea caverns at low tide.",
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
            Action(id="lowlands_smuggler_cove_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="lowlands_smuggler_cove_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="lowlands_smuggler_cove_sanctum_to_prev", label="Return back", category="movement", target_scene="lowlands_smuggler_cove_overlook", result_text="You retrace your steps."),
            Action(id="lowlands_smuggler_cove_sanctum_to_next", label="Press forward", category="movement", target_scene="lowlands_smuggler_cove_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_smuggler_cove_vault"] = SceneNode(
        id="lowlands_smuggler_cove_vault",
        title="Sunken Smuggler Cove - Deep Vault",
        region="lowlands",
        description="Iron-banded chests sit in deep shadows. Rowboats moor inside sea caverns at low tide.",
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
            Action(id="lowlands_smuggler_cove_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="lowlands_smuggler_cove_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="lowlands_smuggler_cove_vault_to_prev", label="Return back", category="movement", target_scene="lowlands_smuggler_cove_sanctum", result_text="You retrace your steps."),
            Action(id="lowlands_smuggler_cove_vault_to_hub", label="Return to Hub", category="movement", target_scene="lowlands_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["lowlands_hub"].base_actions.append(
        Action(id="lowlands_hub_to_smuggler_cove", label="Visit Sunken Smugg", category="movement", target_scene="lowlands_smuggler_cove_gate", result_text="You travel to Sunken Smuggler Cove.")
    )

    # POI: Old Brewery Vault (10 nodes)
    scenes["lowlands_brewery_vault_gate"] = SceneNode(
        id="lowlands_brewery_vault_gate",
        title="Old Brewery Vault - Outer Gate",
        region="lowlands",
        description="Iron bars secure the heavy timber entrance. Copper vats bubble with dark fermented barley.",
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
            Action(id="lowlands_brewery_vault_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="lowlands_brewery_vault_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="lowlands_brewery_vault_gate_to_prev", label="Return back", category="movement", target_scene="lowlands_hub", result_text="You retrace your steps."),
            Action(id="lowlands_brewery_vault_gate_to_next", label="Press forward", category="movement", target_scene="lowlands_brewery_vault_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_brewery_vault_courtyard"] = SceneNode(
        id="lowlands_brewery_vault_courtyard",
        title="Old Brewery Vault - Main Courtyard",
        region="lowlands",
        description="Cobblestones show heavy cart wheel wear. Copper vats bubble with dark fermented barley.",
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
            Action(id="lowlands_brewery_vault_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="lowlands_brewery_vault_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="lowlands_brewery_vault_courtyard_to_prev", label="Return back", category="movement", target_scene="lowlands_brewery_vault_gate", result_text="You retrace your steps."),
            Action(id="lowlands_brewery_vault_courtyard_to_next", label="Press forward", category="movement", target_scene="lowlands_brewery_vault_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_brewery_vault_quarters"] = SceneNode(
        id="lowlands_brewery_vault_quarters",
        title="Old Brewery Vault - Living Quarters",
        region="lowlands",
        description="Rows of wooden bunks line the walls. Copper vats bubble with dark fermented barley.",
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
            Action(id="lowlands_brewery_vault_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="lowlands_brewery_vault_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="lowlands_brewery_vault_quarters_to_prev", label="Return back", category="movement", target_scene="lowlands_brewery_vault_courtyard", result_text="You retrace your steps."),
            Action(id="lowlands_brewery_vault_quarters_to_next", label="Press forward", category="movement", target_scene="lowlands_brewery_vault_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_brewery_vault_armory"] = SceneNode(
        id="lowlands_brewery_vault_armory",
        title="Old Brewery Vault - Supply Depot",
        region="lowlands",
        description="Crates of rations and tools stand stacked. Copper vats bubble with dark fermented barley.",
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
            Action(id="lowlands_brewery_vault_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="lowlands_brewery_vault_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="lowlands_brewery_vault_armory_to_prev", label="Return back", category="movement", target_scene="lowlands_brewery_vault_quarters", result_text="You retrace your steps."),
            Action(id="lowlands_brewery_vault_armory_to_next", label="Press forward", category="movement", target_scene="lowlands_brewery_vault_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_brewery_vault_cellar"] = SceneNode(
        id="lowlands_brewery_vault_cellar",
        title="Old Brewery Vault - Lower Cellar",
        region="lowlands",
        description="Damp air smells of cool earth and storage. Copper vats bubble with dark fermented barley.",
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
            Action(id="lowlands_brewery_vault_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="lowlands_brewery_vault_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="lowlands_brewery_vault_cellar_to_prev", label="Return back", category="movement", target_scene="lowlands_brewery_vault_armory", result_text="You retrace your steps."),
            Action(id="lowlands_brewery_vault_cellar_to_next", label="Press forward", category="movement", target_scene="lowlands_brewery_vault_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_brewery_vault_passage"] = SceneNode(
        id="lowlands_brewery_vault_passage",
        title="Old Brewery Vault - Stone Corridor",
        region="lowlands",
        description="Wall sconces hold flickering tallow candles. Copper vats bubble with dark fermented barley.",
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
            Action(id="lowlands_brewery_vault_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="lowlands_brewery_vault_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="lowlands_brewery_vault_passage_to_prev", label="Return back", category="movement", target_scene="lowlands_brewery_vault_cellar", result_text="You retrace your steps."),
            Action(id="lowlands_brewery_vault_passage_to_next", label="Press forward", category="movement", target_scene="lowlands_brewery_vault_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_brewery_vault_chamber"] = SceneNode(
        id="lowlands_brewery_vault_chamber",
        title="Old Brewery Vault - Inner Chamber",
        region="lowlands",
        description="A sturdy oak desk holds ledgers and maps. Copper vats bubble with dark fermented barley.",
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
            Action(id="lowlands_brewery_vault_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="lowlands_brewery_vault_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="lowlands_brewery_vault_chamber_to_prev", label="Return back", category="movement", target_scene="lowlands_brewery_vault_passage", result_text="You retrace your steps."),
            Action(id="lowlands_brewery_vault_chamber_to_next", label="Press forward", category="movement", target_scene="lowlands_brewery_vault_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_brewery_vault_overlook"] = SceneNode(
        id="lowlands_brewery_vault_overlook",
        title="Old Brewery Vault - High Overlook",
        region="lowlands",
        description="A stone ledge provides a clear view. Copper vats bubble with dark fermented barley.",
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
            Action(id="lowlands_brewery_vault_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="lowlands_brewery_vault_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="lowlands_brewery_vault_overlook_to_prev", label="Return back", category="movement", target_scene="lowlands_brewery_vault_chamber", result_text="You retrace your steps."),
            Action(id="lowlands_brewery_vault_overlook_to_next", label="Press forward", category="movement", target_scene="lowlands_brewery_vault_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_brewery_vault_sanctum"] = SceneNode(
        id="lowlands_brewery_vault_sanctum",
        title="Old Brewery Vault - Inner Sanctum",
        region="lowlands",
        description="A stone altar stands in quiet reverence. Copper vats bubble with dark fermented barley.",
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
            Action(id="lowlands_brewery_vault_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="lowlands_brewery_vault_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="lowlands_brewery_vault_sanctum_to_prev", label="Return back", category="movement", target_scene="lowlands_brewery_vault_overlook", result_text="You retrace your steps."),
            Action(id="lowlands_brewery_vault_sanctum_to_next", label="Press forward", category="movement", target_scene="lowlands_brewery_vault_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_brewery_vault_vault"] = SceneNode(
        id="lowlands_brewery_vault_vault",
        title="Old Brewery Vault - Deep Vault",
        region="lowlands",
        description="Iron-banded chests sit in deep shadows. Copper vats bubble with dark fermented barley.",
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
            Action(id="lowlands_brewery_vault_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="lowlands_brewery_vault_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="lowlands_brewery_vault_vault_to_prev", label="Return back", category="movement", target_scene="lowlands_brewery_vault_sanctum", result_text="You retrace your steps."),
            Action(id="lowlands_brewery_vault_vault_to_hub", label="Return to Hub", category="movement", target_scene="lowlands_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["lowlands_hub"].base_actions.append(
        Action(id="lowlands_hub_to_brewery_vault", label="Visit Old Brewery", category="movement", target_scene="lowlands_brewery_vault_gate", result_text="You travel to Old Brewery Vault.")
    )

    # POI: Harbor Bell Tower (10 nodes)
    scenes["lowlands_bell_tower_gate"] = SceneNode(
        id="lowlands_bell_tower_gate",
        title="Harbor Bell Tower - Outer Gate",
        region="lowlands",
        description="Iron bars secure the heavy timber entrance. The massive iron bell warns ships of fog.",
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
            Action(id="lowlands_bell_tower_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="lowlands_bell_tower_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="lowlands_bell_tower_gate_to_prev", label="Return back", category="movement", target_scene="lowlands_hub", result_text="You retrace your steps."),
            Action(id="lowlands_bell_tower_gate_to_next", label="Press forward", category="movement", target_scene="lowlands_bell_tower_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_bell_tower_courtyard"] = SceneNode(
        id="lowlands_bell_tower_courtyard",
        title="Harbor Bell Tower - Main Courtyard",
        region="lowlands",
        description="Cobblestones show heavy cart wheel wear. The massive iron bell warns ships of fog.",
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
            Action(id="lowlands_bell_tower_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="lowlands_bell_tower_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="lowlands_bell_tower_courtyard_to_prev", label="Return back", category="movement", target_scene="lowlands_bell_tower_gate", result_text="You retrace your steps."),
            Action(id="lowlands_bell_tower_courtyard_to_next", label="Press forward", category="movement", target_scene="lowlands_bell_tower_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_bell_tower_quarters"] = SceneNode(
        id="lowlands_bell_tower_quarters",
        title="Harbor Bell Tower - Living Quarters",
        region="lowlands",
        description="Rows of wooden bunks line the walls. The massive iron bell warns ships of fog.",
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
            Action(id="lowlands_bell_tower_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="lowlands_bell_tower_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="lowlands_bell_tower_quarters_to_prev", label="Return back", category="movement", target_scene="lowlands_bell_tower_courtyard", result_text="You retrace your steps."),
            Action(id="lowlands_bell_tower_quarters_to_next", label="Press forward", category="movement", target_scene="lowlands_bell_tower_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_bell_tower_armory"] = SceneNode(
        id="lowlands_bell_tower_armory",
        title="Harbor Bell Tower - Supply Depot",
        region="lowlands",
        description="Crates of rations and tools stand stacked. The massive iron bell warns ships of fog.",
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
            Action(id="lowlands_bell_tower_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="lowlands_bell_tower_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="lowlands_bell_tower_armory_to_prev", label="Return back", category="movement", target_scene="lowlands_bell_tower_quarters", result_text="You retrace your steps."),
            Action(id="lowlands_bell_tower_armory_to_next", label="Press forward", category="movement", target_scene="lowlands_bell_tower_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_bell_tower_cellar"] = SceneNode(
        id="lowlands_bell_tower_cellar",
        title="Harbor Bell Tower - Lower Cellar",
        region="lowlands",
        description="Damp air smells of cool earth and storage. The massive iron bell warns ships of fog.",
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
            Action(id="lowlands_bell_tower_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="lowlands_bell_tower_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="lowlands_bell_tower_cellar_to_prev", label="Return back", category="movement", target_scene="lowlands_bell_tower_armory", result_text="You retrace your steps."),
            Action(id="lowlands_bell_tower_cellar_to_next", label="Press forward", category="movement", target_scene="lowlands_bell_tower_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_bell_tower_passage"] = SceneNode(
        id="lowlands_bell_tower_passage",
        title="Harbor Bell Tower - Stone Corridor",
        region="lowlands",
        description="Wall sconces hold flickering tallow candles. The massive iron bell warns ships of fog.",
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
            Action(id="lowlands_bell_tower_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="lowlands_bell_tower_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="lowlands_bell_tower_passage_to_prev", label="Return back", category="movement", target_scene="lowlands_bell_tower_cellar", result_text="You retrace your steps."),
            Action(id="lowlands_bell_tower_passage_to_next", label="Press forward", category="movement", target_scene="lowlands_bell_tower_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_bell_tower_chamber"] = SceneNode(
        id="lowlands_bell_tower_chamber",
        title="Harbor Bell Tower - Inner Chamber",
        region="lowlands",
        description="A sturdy oak desk holds ledgers and maps. The massive iron bell warns ships of fog.",
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
            Action(id="lowlands_bell_tower_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="lowlands_bell_tower_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="lowlands_bell_tower_chamber_to_prev", label="Return back", category="movement", target_scene="lowlands_bell_tower_passage", result_text="You retrace your steps."),
            Action(id="lowlands_bell_tower_chamber_to_next", label="Press forward", category="movement", target_scene="lowlands_bell_tower_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_bell_tower_overlook"] = SceneNode(
        id="lowlands_bell_tower_overlook",
        title="Harbor Bell Tower - High Overlook",
        region="lowlands",
        description="A stone ledge provides a clear view. The massive iron bell warns ships of fog.",
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
            Action(id="lowlands_bell_tower_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="lowlands_bell_tower_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="lowlands_bell_tower_overlook_to_prev", label="Return back", category="movement", target_scene="lowlands_bell_tower_chamber", result_text="You retrace your steps."),
            Action(id="lowlands_bell_tower_overlook_to_next", label="Press forward", category="movement", target_scene="lowlands_bell_tower_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_bell_tower_sanctum"] = SceneNode(
        id="lowlands_bell_tower_sanctum",
        title="Harbor Bell Tower - Inner Sanctum",
        region="lowlands",
        description="A stone altar stands in quiet reverence. The massive iron bell warns ships of fog.",
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
            Action(id="lowlands_bell_tower_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="lowlands_bell_tower_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="lowlands_bell_tower_sanctum_to_prev", label="Return back", category="movement", target_scene="lowlands_bell_tower_overlook", result_text="You retrace your steps."),
            Action(id="lowlands_bell_tower_sanctum_to_next", label="Press forward", category="movement", target_scene="lowlands_bell_tower_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_bell_tower_vault"] = SceneNode(
        id="lowlands_bell_tower_vault",
        title="Harbor Bell Tower - Deep Vault",
        region="lowlands",
        description="Iron-banded chests sit in deep shadows. The massive iron bell warns ships of fog.",
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
            Action(id="lowlands_bell_tower_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="lowlands_bell_tower_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="lowlands_bell_tower_vault_to_prev", label="Return back", category="movement", target_scene="lowlands_bell_tower_sanctum", result_text="You retrace your steps."),
            Action(id="lowlands_bell_tower_vault_to_hub", label="Return to Hub", category="movement", target_scene="lowlands_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["lowlands_hub"].base_actions.append(
        Action(id="lowlands_hub_to_bell_tower", label="Visit Harbor Bell", category="movement", target_scene="lowlands_bell_tower_gate", result_text="You travel to Harbor Bell Tower.")
    )

    # POI: River Customs Gate (10 nodes)
    scenes["lowlands_customs_house_gate"] = SceneNode(
        id="lowlands_customs_house_gate",
        title="River Customs Gate - Outer Gate",
        region="lowlands",
        description="Iron bars secure the heavy timber entrance. Clerks stamp cargo manifests behind iron bars.",
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
            Action(id="lowlands_customs_house_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="lowlands_customs_house_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="lowlands_customs_house_gate_to_prev", label="Return back", category="movement", target_scene="lowlands_hub", result_text="You retrace your steps."),
            Action(id="lowlands_customs_house_gate_to_next", label="Press forward", category="movement", target_scene="lowlands_customs_house_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_customs_house_courtyard"] = SceneNode(
        id="lowlands_customs_house_courtyard",
        title="River Customs Gate - Main Courtyard",
        region="lowlands",
        description="Cobblestones show heavy cart wheel wear. Clerks stamp cargo manifests behind iron bars.",
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
            Action(id="lowlands_customs_house_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="lowlands_customs_house_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="lowlands_customs_house_courtyard_to_prev", label="Return back", category="movement", target_scene="lowlands_customs_house_gate", result_text="You retrace your steps."),
            Action(id="lowlands_customs_house_courtyard_to_next", label="Press forward", category="movement", target_scene="lowlands_customs_house_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_customs_house_quarters"] = SceneNode(
        id="lowlands_customs_house_quarters",
        title="River Customs Gate - Living Quarters",
        region="lowlands",
        description="Rows of wooden bunks line the walls. Clerks stamp cargo manifests behind iron bars.",
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
            Action(id="lowlands_customs_house_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="lowlands_customs_house_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="lowlands_customs_house_quarters_to_prev", label="Return back", category="movement", target_scene="lowlands_customs_house_courtyard", result_text="You retrace your steps."),
            Action(id="lowlands_customs_house_quarters_to_next", label="Press forward", category="movement", target_scene="lowlands_customs_house_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_customs_house_armory"] = SceneNode(
        id="lowlands_customs_house_armory",
        title="River Customs Gate - Supply Depot",
        region="lowlands",
        description="Crates of rations and tools stand stacked. Clerks stamp cargo manifests behind iron bars.",
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
            Action(id="lowlands_customs_house_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="lowlands_customs_house_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="lowlands_customs_house_armory_to_prev", label="Return back", category="movement", target_scene="lowlands_customs_house_quarters", result_text="You retrace your steps."),
            Action(id="lowlands_customs_house_armory_to_next", label="Press forward", category="movement", target_scene="lowlands_customs_house_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_customs_house_cellar"] = SceneNode(
        id="lowlands_customs_house_cellar",
        title="River Customs Gate - Lower Cellar",
        region="lowlands",
        description="Damp air smells of cool earth and storage. Clerks stamp cargo manifests behind iron bars.",
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
            Action(id="lowlands_customs_house_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="lowlands_customs_house_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="lowlands_customs_house_cellar_to_prev", label="Return back", category="movement", target_scene="lowlands_customs_house_armory", result_text="You retrace your steps."),
            Action(id="lowlands_customs_house_cellar_to_next", label="Press forward", category="movement", target_scene="lowlands_customs_house_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_customs_house_passage"] = SceneNode(
        id="lowlands_customs_house_passage",
        title="River Customs Gate - Stone Corridor",
        region="lowlands",
        description="Wall sconces hold flickering tallow candles. Clerks stamp cargo manifests behind iron bars.",
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
            Action(id="lowlands_customs_house_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="lowlands_customs_house_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="lowlands_customs_house_passage_to_prev", label="Return back", category="movement", target_scene="lowlands_customs_house_cellar", result_text="You retrace your steps."),
            Action(id="lowlands_customs_house_passage_to_next", label="Press forward", category="movement", target_scene="lowlands_customs_house_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_customs_house_chamber"] = SceneNode(
        id="lowlands_customs_house_chamber",
        title="River Customs Gate - Inner Chamber",
        region="lowlands",
        description="A sturdy oak desk holds ledgers and maps. Clerks stamp cargo manifests behind iron bars.",
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
            Action(id="lowlands_customs_house_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="lowlands_customs_house_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="lowlands_customs_house_chamber_to_prev", label="Return back", category="movement", target_scene="lowlands_customs_house_passage", result_text="You retrace your steps."),
            Action(id="lowlands_customs_house_chamber_to_next", label="Press forward", category="movement", target_scene="lowlands_customs_house_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_customs_house_overlook"] = SceneNode(
        id="lowlands_customs_house_overlook",
        title="River Customs Gate - High Overlook",
        region="lowlands",
        description="A stone ledge provides a clear view. Clerks stamp cargo manifests behind iron bars.",
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
            Action(id="lowlands_customs_house_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="lowlands_customs_house_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="lowlands_customs_house_overlook_to_prev", label="Return back", category="movement", target_scene="lowlands_customs_house_chamber", result_text="You retrace your steps."),
            Action(id="lowlands_customs_house_overlook_to_next", label="Press forward", category="movement", target_scene="lowlands_customs_house_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_customs_house_sanctum"] = SceneNode(
        id="lowlands_customs_house_sanctum",
        title="River Customs Gate - Inner Sanctum",
        region="lowlands",
        description="A stone altar stands in quiet reverence. Clerks stamp cargo manifests behind iron bars.",
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
            Action(id="lowlands_customs_house_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="lowlands_customs_house_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="lowlands_customs_house_sanctum_to_prev", label="Return back", category="movement", target_scene="lowlands_customs_house_overlook", result_text="You retrace your steps."),
            Action(id="lowlands_customs_house_sanctum_to_next", label="Press forward", category="movement", target_scene="lowlands_customs_house_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_customs_house_vault"] = SceneNode(
        id="lowlands_customs_house_vault",
        title="River Customs Gate - Deep Vault",
        region="lowlands",
        description="Iron-banded chests sit in deep shadows. Clerks stamp cargo manifests behind iron bars.",
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
            Action(id="lowlands_customs_house_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="lowlands_customs_house_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="lowlands_customs_house_vault_to_prev", label="Return back", category="movement", target_scene="lowlands_customs_house_sanctum", result_text="You retrace your steps."),
            Action(id="lowlands_customs_house_vault_to_hub", label="Return to Hub", category="movement", target_scene="lowlands_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["lowlands_hub"].base_actions.append(
        Action(id="lowlands_hub_to_customs_house", label="Visit River Custom", category="movement", target_scene="lowlands_customs_house_gate", result_text="You travel to River Customs Gate.")
    )

    # POI: Potters Quay (10 nodes)
    scenes["lowlands_potters_quay_gate"] = SceneNode(
        id="lowlands_potters_quay_gate",
        title="Potters Quay - Outer Gate",
        region="lowlands",
        description="Iron bars secure the heavy timber entrance. Clay jars line the muddy riverbank landing.",
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
            Action(id="lowlands_potters_quay_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="lowlands_potters_quay_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="lowlands_potters_quay_gate_to_prev", label="Return back", category="movement", target_scene="lowlands_hub", result_text="You retrace your steps."),
            Action(id="lowlands_potters_quay_gate_to_next", label="Press forward", category="movement", target_scene="lowlands_potters_quay_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_potters_quay_courtyard"] = SceneNode(
        id="lowlands_potters_quay_courtyard",
        title="Potters Quay - Main Courtyard",
        region="lowlands",
        description="Cobblestones show heavy cart wheel wear. Clay jars line the muddy riverbank landing.",
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
            Action(id="lowlands_potters_quay_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="lowlands_potters_quay_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="lowlands_potters_quay_courtyard_to_prev", label="Return back", category="movement", target_scene="lowlands_potters_quay_gate", result_text="You retrace your steps."),
            Action(id="lowlands_potters_quay_courtyard_to_next", label="Press forward", category="movement", target_scene="lowlands_potters_quay_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_potters_quay_quarters"] = SceneNode(
        id="lowlands_potters_quay_quarters",
        title="Potters Quay - Living Quarters",
        region="lowlands",
        description="Rows of wooden bunks line the walls. Clay jars line the muddy riverbank landing.",
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
            Action(id="lowlands_potters_quay_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="lowlands_potters_quay_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="lowlands_potters_quay_quarters_to_prev", label="Return back", category="movement", target_scene="lowlands_potters_quay_courtyard", result_text="You retrace your steps."),
            Action(id="lowlands_potters_quay_quarters_to_next", label="Press forward", category="movement", target_scene="lowlands_potters_quay_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_potters_quay_armory"] = SceneNode(
        id="lowlands_potters_quay_armory",
        title="Potters Quay - Supply Depot",
        region="lowlands",
        description="Crates of rations and tools stand stacked. Clay jars line the muddy riverbank landing.",
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
            Action(id="lowlands_potters_quay_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="lowlands_potters_quay_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="lowlands_potters_quay_armory_to_prev", label="Return back", category="movement", target_scene="lowlands_potters_quay_quarters", result_text="You retrace your steps."),
            Action(id="lowlands_potters_quay_armory_to_next", label="Press forward", category="movement", target_scene="lowlands_potters_quay_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_potters_quay_cellar"] = SceneNode(
        id="lowlands_potters_quay_cellar",
        title="Potters Quay - Lower Cellar",
        region="lowlands",
        description="Damp air smells of cool earth and storage. Clay jars line the muddy riverbank landing.",
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
            Action(id="lowlands_potters_quay_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="lowlands_potters_quay_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="lowlands_potters_quay_cellar_to_prev", label="Return back", category="movement", target_scene="lowlands_potters_quay_armory", result_text="You retrace your steps."),
            Action(id="lowlands_potters_quay_cellar_to_next", label="Press forward", category="movement", target_scene="lowlands_potters_quay_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_potters_quay_passage"] = SceneNode(
        id="lowlands_potters_quay_passage",
        title="Potters Quay - Stone Corridor",
        region="lowlands",
        description="Wall sconces hold flickering tallow candles. Clay jars line the muddy riverbank landing.",
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
            Action(id="lowlands_potters_quay_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="lowlands_potters_quay_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="lowlands_potters_quay_passage_to_prev", label="Return back", category="movement", target_scene="lowlands_potters_quay_cellar", result_text="You retrace your steps."),
            Action(id="lowlands_potters_quay_passage_to_next", label="Press forward", category="movement", target_scene="lowlands_potters_quay_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_potters_quay_chamber"] = SceneNode(
        id="lowlands_potters_quay_chamber",
        title="Potters Quay - Inner Chamber",
        region="lowlands",
        description="A sturdy oak desk holds ledgers and maps. Clay jars line the muddy riverbank landing.",
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
            Action(id="lowlands_potters_quay_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="lowlands_potters_quay_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="lowlands_potters_quay_chamber_to_prev", label="Return back", category="movement", target_scene="lowlands_potters_quay_passage", result_text="You retrace your steps."),
            Action(id="lowlands_potters_quay_chamber_to_next", label="Press forward", category="movement", target_scene="lowlands_potters_quay_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_potters_quay_overlook"] = SceneNode(
        id="lowlands_potters_quay_overlook",
        title="Potters Quay - High Overlook",
        region="lowlands",
        description="A stone ledge provides a clear view. Clay jars line the muddy riverbank landing.",
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
            Action(id="lowlands_potters_quay_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="lowlands_potters_quay_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="lowlands_potters_quay_overlook_to_prev", label="Return back", category="movement", target_scene="lowlands_potters_quay_chamber", result_text="You retrace your steps."),
            Action(id="lowlands_potters_quay_overlook_to_next", label="Press forward", category="movement", target_scene="lowlands_potters_quay_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_potters_quay_sanctum"] = SceneNode(
        id="lowlands_potters_quay_sanctum",
        title="Potters Quay - Inner Sanctum",
        region="lowlands",
        description="A stone altar stands in quiet reverence. Clay jars line the muddy riverbank landing.",
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
            Action(id="lowlands_potters_quay_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="lowlands_potters_quay_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="lowlands_potters_quay_sanctum_to_prev", label="Return back", category="movement", target_scene="lowlands_potters_quay_overlook", result_text="You retrace your steps."),
            Action(id="lowlands_potters_quay_sanctum_to_next", label="Press forward", category="movement", target_scene="lowlands_potters_quay_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["lowlands_potters_quay_vault"] = SceneNode(
        id="lowlands_potters_quay_vault",
        title="Potters Quay - Deep Vault",
        region="lowlands",
        description="Iron-banded chests sit in deep shadows. Clay jars line the muddy riverbank landing.",
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
            Action(id="lowlands_potters_quay_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="lowlands_potters_quay_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="lowlands_potters_quay_vault_to_prev", label="Return back", category="movement", target_scene="lowlands_potters_quay_sanctum", result_text="You retrace your steps."),
            Action(id="lowlands_potters_quay_vault_to_hub", label="Return to Hub", category="movement", target_scene="lowlands_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["lowlands_hub"].base_actions.append(
        Action(id="lowlands_hub_to_potters_quay", label="Visit Potters Quay", category="movement", target_scene="lowlands_potters_quay_gate", result_text="You travel to Potters Quay.")
    )

    return RegionManifest(
        id="lowlands",
        name="The Lowlands",
        mechanic_name="Social Stealth & Disguise",
        mechanic_description="Comprehensive open-world region with 10 deep POIs.",
        scenes=scenes
    )