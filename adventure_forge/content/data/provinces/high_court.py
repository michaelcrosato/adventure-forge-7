"""Province: The High Crown of Veras.
Unique Mechanic: Legal Evidence & Court Intrigues.
"""
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action

def build_high_court_province() -> RegionManifest:
    scenes = {}

    # Province Hub
    scenes["high_court_hub"] = SceneNode(
        id="high_court_hub",
        title="The High Crown of Veras - Central Hub",
        region="high_court",
        description="White marble colonnades rise above manicured plazas. Armored knights stand at attention.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_attribute": {"attribute": "strength", "value": 12}},
                text="Your military posture draws respectful nods from travelers."
            ),
        ],
        base_actions=[
            Action(id="high_court_hub_scout", label="Scout hub", category="interaction", result_text="You survey the bustling provincial crossroads."),
            Action(id="high_court_hub_rest", label="Rest at inn", category="interaction", effects=[{"modify_stamina": 5}], result_text="You rest and regain stamina."),
            Action(id="high_court_to_bazaar", label="Go to Bazaar", category="movement", target_scene="bazaar_center", result_text="You travel along the highway to the Grand Bazaar."),
        ]
    )

    # POI: The Grand Basilica (10 nodes)
    scenes["high_court_grand_basilica_gate"] = SceneNode(
        id="high_court_grand_basilica_gate",
        title="The Grand Basilica - Outer Gate",
        region="high_court",
        description="Iron bars secure the heavy timber entrance. Sunlight streams through tall arched clerestories.",
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
            Action(id="high_court_grand_basilica_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="high_court_grand_basilica_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="high_court_grand_basilica_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_gate_to_next", label="Press forward", category="movement", target_scene="high_court_grand_basilica_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_grand_basilica_courtyard"] = SceneNode(
        id="high_court_grand_basilica_courtyard",
        title="The Grand Basilica - Main Courtyard",
        region="high_court",
        description="Cobblestones show heavy cart wheel wear. Sunlight streams through tall arched clerestories.",
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
            Action(id="high_court_grand_basilica_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="high_court_grand_basilica_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="high_court_grand_basilica_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_grand_basilica_gate", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_grand_basilica_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_grand_basilica_quarters"] = SceneNode(
        id="high_court_grand_basilica_quarters",
        title="The Grand Basilica - Living Quarters",
        region="high_court",
        description="Rows of wooden bunks line the walls. Sunlight streams through tall arched clerestories.",
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
            Action(id="high_court_grand_basilica_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="high_court_grand_basilica_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="high_court_grand_basilica_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_grand_basilica_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_grand_basilica_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_grand_basilica_armory"] = SceneNode(
        id="high_court_grand_basilica_armory",
        title="The Grand Basilica - Supply Depot",
        region="high_court",
        description="Crates of rations and tools stand stacked. Sunlight streams through tall arched clerestories.",
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
            Action(id="high_court_grand_basilica_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="high_court_grand_basilica_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="high_court_grand_basilica_armory_to_prev", label="Return back", category="movement", target_scene="high_court_grand_basilica_quarters", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_armory_to_next", label="Press forward", category="movement", target_scene="high_court_grand_basilica_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_grand_basilica_cellar"] = SceneNode(
        id="high_court_grand_basilica_cellar",
        title="The Grand Basilica - Lower Cellar",
        region="high_court",
        description="Damp air smells of cool earth and storage. Sunlight streams through tall arched clerestories.",
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
            Action(id="high_court_grand_basilica_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="high_court_grand_basilica_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="high_court_grand_basilica_cellar_to_prev", label="Return back", category="movement", target_scene="high_court_grand_basilica_armory", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_cellar_to_next", label="Press forward", category="movement", target_scene="high_court_grand_basilica_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_grand_basilica_passage"] = SceneNode(
        id="high_court_grand_basilica_passage",
        title="The Grand Basilica - Stone Corridor",
        region="high_court",
        description="Wall sconces hold flickering tallow candles. Sunlight streams through tall arched clerestories.",
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
            Action(id="high_court_grand_basilica_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="high_court_grand_basilica_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="high_court_grand_basilica_passage_to_prev", label="Return back", category="movement", target_scene="high_court_grand_basilica_cellar", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_passage_to_next", label="Press forward", category="movement", target_scene="high_court_grand_basilica_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_grand_basilica_chamber"] = SceneNode(
        id="high_court_grand_basilica_chamber",
        title="The Grand Basilica - Inner Chamber",
        region="high_court",
        description="A sturdy oak desk holds ledgers and maps. Sunlight streams through tall arched clerestories.",
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
            Action(id="high_court_grand_basilica_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="high_court_grand_basilica_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="high_court_grand_basilica_chamber_to_prev", label="Return back", category="movement", target_scene="high_court_grand_basilica_passage", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_chamber_to_next", label="Press forward", category="movement", target_scene="high_court_grand_basilica_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_grand_basilica_overlook"] = SceneNode(
        id="high_court_grand_basilica_overlook",
        title="The Grand Basilica - High Overlook",
        region="high_court",
        description="A stone ledge provides a clear view. Sunlight streams through tall arched clerestories.",
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
            Action(id="high_court_grand_basilica_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="high_court_grand_basilica_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="high_court_grand_basilica_overlook_to_prev", label="Return back", category="movement", target_scene="high_court_grand_basilica_chamber", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_overlook_to_next", label="Press forward", category="movement", target_scene="high_court_grand_basilica_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_grand_basilica_sanctum"] = SceneNode(
        id="high_court_grand_basilica_sanctum",
        title="The Grand Basilica - Inner Sanctum",
        region="high_court",
        description="A stone altar stands in quiet reverence. Sunlight streams through tall arched clerestories.",
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
            Action(id="high_court_grand_basilica_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="high_court_grand_basilica_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="high_court_grand_basilica_sanctum_to_prev", label="Return back", category="movement", target_scene="high_court_grand_basilica_overlook", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_sanctum_to_next", label="Press forward", category="movement", target_scene="high_court_grand_basilica_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_grand_basilica_vault"] = SceneNode(
        id="high_court_grand_basilica_vault",
        title="The Grand Basilica - Deep Vault",
        region="high_court",
        description="Iron-banded chests sit in deep shadows. Sunlight streams through tall arched clerestories.",
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
            Action(id="high_court_grand_basilica_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="high_court_grand_basilica_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="high_court_grand_basilica_vault_to_prev", label="Return back", category="movement", target_scene="high_court_grand_basilica_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_grand_basilica", label="Visit Grand Basilica", category="movement", target_scene="high_court_grand_basilica_gate", result_text="You travel to The Grand Basilica.")
    )

    # POI: Hall of Justiciars (10 nodes)
    scenes["high_court_justiciar_hall_gate"] = SceneNode(
        id="high_court_justiciar_hall_gate",
        title="Hall of Justiciars - Outer Gate",
        region="high_court",
        description="Iron bars secure the heavy timber entrance. Bailiffs carry sealed legal briefs between courts.",
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
            Action(id="high_court_justiciar_hall_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="high_court_justiciar_hall_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="high_court_justiciar_hall_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_gate_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_justiciar_hall_courtyard"] = SceneNode(
        id="high_court_justiciar_hall_courtyard",
        title="Hall of Justiciars - Main Courtyard",
        region="high_court",
        description="Cobblestones show heavy cart wheel wear. Bailiffs carry sealed legal briefs between courts.",
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
            Action(id="high_court_justiciar_hall_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="high_court_justiciar_hall_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="high_court_justiciar_hall_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_gate", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_justiciar_hall_quarters"] = SceneNode(
        id="high_court_justiciar_hall_quarters",
        title="Hall of Justiciars - Living Quarters",
        region="high_court",
        description="Rows of wooden bunks line the walls. Bailiffs carry sealed legal briefs between courts.",
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
            Action(id="high_court_justiciar_hall_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="high_court_justiciar_hall_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="high_court_justiciar_hall_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_justiciar_hall_armory"] = SceneNode(
        id="high_court_justiciar_hall_armory",
        title="Hall of Justiciars - Supply Depot",
        region="high_court",
        description="Crates of rations and tools stand stacked. Bailiffs carry sealed legal briefs between courts.",
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
            Action(id="high_court_justiciar_hall_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="high_court_justiciar_hall_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="high_court_justiciar_hall_armory_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_quarters", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_armory_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_justiciar_hall_cellar"] = SceneNode(
        id="high_court_justiciar_hall_cellar",
        title="Hall of Justiciars - Lower Cellar",
        region="high_court",
        description="Damp air smells of cool earth and storage. Bailiffs carry sealed legal briefs between courts.",
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
            Action(id="high_court_justiciar_hall_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="high_court_justiciar_hall_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="high_court_justiciar_hall_cellar_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_armory", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_cellar_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_justiciar_hall_passage"] = SceneNode(
        id="high_court_justiciar_hall_passage",
        title="Hall of Justiciars - Stone Corridor",
        region="high_court",
        description="Wall sconces hold flickering tallow candles. Bailiffs carry sealed legal briefs between courts.",
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
            Action(id="high_court_justiciar_hall_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="high_court_justiciar_hall_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="high_court_justiciar_hall_passage_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_cellar", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_passage_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_justiciar_hall_chamber"] = SceneNode(
        id="high_court_justiciar_hall_chamber",
        title="Hall of Justiciars - Inner Chamber",
        region="high_court",
        description="A sturdy oak desk holds ledgers and maps. Bailiffs carry sealed legal briefs between courts.",
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
            Action(id="high_court_justiciar_hall_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="high_court_justiciar_hall_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="high_court_justiciar_hall_chamber_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_passage", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_chamber_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_justiciar_hall_overlook"] = SceneNode(
        id="high_court_justiciar_hall_overlook",
        title="Hall of Justiciars - High Overlook",
        region="high_court",
        description="A stone ledge provides a clear view. Bailiffs carry sealed legal briefs between courts.",
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
            Action(id="high_court_justiciar_hall_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="high_court_justiciar_hall_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="high_court_justiciar_hall_overlook_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_chamber", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_overlook_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_justiciar_hall_sanctum"] = SceneNode(
        id="high_court_justiciar_hall_sanctum",
        title="Hall of Justiciars - Inner Sanctum",
        region="high_court",
        description="A stone altar stands in quiet reverence. Bailiffs carry sealed legal briefs between courts.",
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
            Action(id="high_court_justiciar_hall_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="high_court_justiciar_hall_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="high_court_justiciar_hall_sanctum_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_overlook", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_sanctum_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_justiciar_hall_vault"] = SceneNode(
        id="high_court_justiciar_hall_vault",
        title="Hall of Justiciars - Deep Vault",
        region="high_court",
        description="Iron-banded chests sit in deep shadows. Bailiffs carry sealed legal briefs between courts.",
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
            Action(id="high_court_justiciar_hall_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="high_court_justiciar_hall_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="high_court_justiciar_hall_vault_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_justiciar_hall", label="Visit Justiciar Hall", category="movement", target_scene="high_court_justiciar_hall_gate", result_text="You travel to Hall of Justiciars.")
    )

    # POI: The Royal Archives (10 nodes)
    scenes["high_court_royal_archive_gate"] = SceneNode(
        id="high_court_royal_archive_gate",
        title="The Royal Archives - Outer Gate",
        region="high_court",
        description="Iron bars secure the heavy timber entrance. Cedar book stacks reach the vaulted ceiling.",
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
            Action(id="high_court_royal_archive_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="high_court_royal_archive_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="high_court_royal_archive_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_royal_archive_gate_to_next", label="Press forward", category="movement", target_scene="high_court_royal_archive_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_royal_archive_courtyard"] = SceneNode(
        id="high_court_royal_archive_courtyard",
        title="The Royal Archives - Main Courtyard",
        region="high_court",
        description="Cobblestones show heavy cart wheel wear. Cedar book stacks reach the vaulted ceiling.",
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
            Action(id="high_court_royal_archive_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="high_court_royal_archive_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="high_court_royal_archive_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_royal_archive_gate", result_text="You retrace your steps."),
            Action(id="high_court_royal_archive_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_royal_archive_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_royal_archive_quarters"] = SceneNode(
        id="high_court_royal_archive_quarters",
        title="The Royal Archives - Living Quarters",
        region="high_court",
        description="Rows of wooden bunks line the walls. Cedar book stacks reach the vaulted ceiling.",
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
            Action(id="high_court_royal_archive_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="high_court_royal_archive_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="high_court_royal_archive_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_royal_archive_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_royal_archive_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_royal_archive_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_royal_archive_armory"] = SceneNode(
        id="high_court_royal_archive_armory",
        title="The Royal Archives - Supply Depot",
        region="high_court",
        description="Crates of rations and tools stand stacked. Cedar book stacks reach the vaulted ceiling.",
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
            Action(id="high_court_royal_archive_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="high_court_royal_archive_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="high_court_royal_archive_armory_to_prev", label="Return back", category="movement", target_scene="high_court_royal_archive_quarters", result_text="You retrace your steps."),
            Action(id="high_court_royal_archive_armory_to_next", label="Press forward", category="movement", target_scene="high_court_royal_archive_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_royal_archive_cellar"] = SceneNode(
        id="high_court_royal_archive_cellar",
        title="The Royal Archives - Lower Cellar",
        region="high_court",
        description="Damp air smells of cool earth and storage. Cedar book stacks reach the vaulted ceiling.",
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
            Action(id="high_court_royal_archive_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="high_court_royal_archive_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="high_court_royal_archive_cellar_to_prev", label="Return back", category="movement", target_scene="high_court_royal_archive_armory", result_text="You retrace your steps."),
            Action(id="high_court_royal_archive_cellar_to_next", label="Press forward", category="movement", target_scene="high_court_royal_archive_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_royal_archive_passage"] = SceneNode(
        id="high_court_royal_archive_passage",
        title="The Royal Archives - Stone Corridor",
        region="high_court",
        description="Wall sconces hold flickering tallow candles. Cedar book stacks reach the vaulted ceiling.",
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
            Action(id="high_court_royal_archive_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="high_court_royal_archive_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="high_court_royal_archive_passage_to_prev", label="Return back", category="movement", target_scene="high_court_royal_archive_cellar", result_text="You retrace your steps."),
            Action(id="high_court_royal_archive_passage_to_next", label="Press forward", category="movement", target_scene="high_court_royal_archive_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_royal_archive_chamber"] = SceneNode(
        id="high_court_royal_archive_chamber",
        title="The Royal Archives - Inner Chamber",
        region="high_court",
        description="A sturdy oak desk holds ledgers and maps. Cedar book stacks reach the vaulted ceiling.",
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
            Action(id="high_court_royal_archive_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="high_court_royal_archive_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="high_court_royal_archive_chamber_to_prev", label="Return back", category="movement", target_scene="high_court_royal_archive_passage", result_text="You retrace your steps."),
            Action(id="high_court_royal_archive_chamber_to_next", label="Press forward", category="movement", target_scene="high_court_royal_archive_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_royal_archive_overlook"] = SceneNode(
        id="high_court_royal_archive_overlook",
        title="The Royal Archives - High Overlook",
        region="high_court",
        description="A stone ledge provides a clear view. Cedar book stacks reach the vaulted ceiling.",
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
            Action(id="high_court_royal_archive_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="high_court_royal_archive_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="high_court_royal_archive_overlook_to_prev", label="Return back", category="movement", target_scene="high_court_royal_archive_chamber", result_text="You retrace your steps."),
            Action(id="high_court_royal_archive_overlook_to_next", label="Press forward", category="movement", target_scene="high_court_royal_archive_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_royal_archive_sanctum"] = SceneNode(
        id="high_court_royal_archive_sanctum",
        title="The Royal Archives - Inner Sanctum",
        region="high_court",
        description="A stone altar stands in quiet reverence. Cedar book stacks reach the vaulted ceiling.",
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
            Action(id="high_court_royal_archive_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="high_court_royal_archive_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="high_court_royal_archive_sanctum_to_prev", label="Return back", category="movement", target_scene="high_court_royal_archive_overlook", result_text="You retrace your steps."),
            Action(id="high_court_royal_archive_sanctum_to_next", label="Press forward", category="movement", target_scene="high_court_royal_archive_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_royal_archive_vault"] = SceneNode(
        id="high_court_royal_archive_vault",
        title="The Royal Archives - Deep Vault",
        region="high_court",
        description="Iron-banded chests sit in deep shadows. Cedar book stacks reach the vaulted ceiling.",
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
            Action(id="high_court_royal_archive_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="high_court_royal_archive_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="high_court_royal_archive_vault_to_prev", label="Return back", category="movement", target_scene="high_court_royal_archive_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_royal_archive_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_royal_archive", label="Visit Royal Archive", category="movement", target_scene="high_court_royal_archive_gate", result_text="You travel to The Royal Archives.")
    )

    # POI: Chancellor Garden (10 nodes)
    scenes["high_court_chancellor_court_gate"] = SceneNode(
        id="high_court_chancellor_court_gate",
        title="Chancellor Garden - Outer Gate",
        region="high_court",
        description="Iron bars secure the heavy timber entrance. Stone fountains bubble among trimmed rose hedges.",
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
            Action(id="high_court_chancellor_court_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="high_court_chancellor_court_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="high_court_chancellor_court_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_chancellor_court_gate_to_next", label="Press forward", category="movement", target_scene="high_court_chancellor_court_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_chancellor_court_courtyard"] = SceneNode(
        id="high_court_chancellor_court_courtyard",
        title="Chancellor Garden - Main Courtyard",
        region="high_court",
        description="Cobblestones show heavy cart wheel wear. Stone fountains bubble among trimmed rose hedges.",
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
            Action(id="high_court_chancellor_court_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="high_court_chancellor_court_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="high_court_chancellor_court_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_chancellor_court_gate", result_text="You retrace your steps."),
            Action(id="high_court_chancellor_court_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_chancellor_court_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_chancellor_court_quarters"] = SceneNode(
        id="high_court_chancellor_court_quarters",
        title="Chancellor Garden - Living Quarters",
        region="high_court",
        description="Rows of wooden bunks line the walls. Stone fountains bubble among trimmed rose hedges.",
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
            Action(id="high_court_chancellor_court_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="high_court_chancellor_court_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="high_court_chancellor_court_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_chancellor_court_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_chancellor_court_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_chancellor_court_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_chancellor_court_armory"] = SceneNode(
        id="high_court_chancellor_court_armory",
        title="Chancellor Garden - Supply Depot",
        region="high_court",
        description="Crates of rations and tools stand stacked. Stone fountains bubble among trimmed rose hedges.",
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
            Action(id="high_court_chancellor_court_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="high_court_chancellor_court_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="high_court_chancellor_court_armory_to_prev", label="Return back", category="movement", target_scene="high_court_chancellor_court_quarters", result_text="You retrace your steps."),
            Action(id="high_court_chancellor_court_armory_to_next", label="Press forward", category="movement", target_scene="high_court_chancellor_court_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_chancellor_court_cellar"] = SceneNode(
        id="high_court_chancellor_court_cellar",
        title="Chancellor Garden - Lower Cellar",
        region="high_court",
        description="Damp air smells of cool earth and storage. Stone fountains bubble among trimmed rose hedges.",
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
            Action(id="high_court_chancellor_court_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="high_court_chancellor_court_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="high_court_chancellor_court_cellar_to_prev", label="Return back", category="movement", target_scene="high_court_chancellor_court_armory", result_text="You retrace your steps."),
            Action(id="high_court_chancellor_court_cellar_to_next", label="Press forward", category="movement", target_scene="high_court_chancellor_court_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_chancellor_court_passage"] = SceneNode(
        id="high_court_chancellor_court_passage",
        title="Chancellor Garden - Stone Corridor",
        region="high_court",
        description="Wall sconces hold flickering tallow candles. Stone fountains bubble among trimmed rose hedges.",
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
            Action(id="high_court_chancellor_court_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="high_court_chancellor_court_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="high_court_chancellor_court_passage_to_prev", label="Return back", category="movement", target_scene="high_court_chancellor_court_cellar", result_text="You retrace your steps."),
            Action(id="high_court_chancellor_court_passage_to_next", label="Press forward", category="movement", target_scene="high_court_chancellor_court_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_chancellor_court_chamber"] = SceneNode(
        id="high_court_chancellor_court_chamber",
        title="Chancellor Garden - Inner Chamber",
        region="high_court",
        description="A sturdy oak desk holds ledgers and maps. Stone fountains bubble among trimmed rose hedges.",
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
            Action(id="high_court_chancellor_court_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="high_court_chancellor_court_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="high_court_chancellor_court_chamber_to_prev", label="Return back", category="movement", target_scene="high_court_chancellor_court_passage", result_text="You retrace your steps."),
            Action(id="high_court_chancellor_court_chamber_to_next", label="Press forward", category="movement", target_scene="high_court_chancellor_court_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_chancellor_court_overlook"] = SceneNode(
        id="high_court_chancellor_court_overlook",
        title="Chancellor Garden - High Overlook",
        region="high_court",
        description="A stone ledge provides a clear view. Stone fountains bubble among trimmed rose hedges.",
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
            Action(id="high_court_chancellor_court_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="high_court_chancellor_court_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="high_court_chancellor_court_overlook_to_prev", label="Return back", category="movement", target_scene="high_court_chancellor_court_chamber", result_text="You retrace your steps."),
            Action(id="high_court_chancellor_court_overlook_to_next", label="Press forward", category="movement", target_scene="high_court_chancellor_court_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_chancellor_court_sanctum"] = SceneNode(
        id="high_court_chancellor_court_sanctum",
        title="Chancellor Garden - Inner Sanctum",
        region="high_court",
        description="A stone altar stands in quiet reverence. Stone fountains bubble among trimmed rose hedges.",
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
            Action(id="high_court_chancellor_court_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="high_court_chancellor_court_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="high_court_chancellor_court_sanctum_to_prev", label="Return back", category="movement", target_scene="high_court_chancellor_court_overlook", result_text="You retrace your steps."),
            Action(id="high_court_chancellor_court_sanctum_to_next", label="Press forward", category="movement", target_scene="high_court_chancellor_court_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_chancellor_court_vault"] = SceneNode(
        id="high_court_chancellor_court_vault",
        title="Chancellor Garden - Deep Vault",
        region="high_court",
        description="Iron-banded chests sit in deep shadows. Stone fountains bubble among trimmed rose hedges.",
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
            Action(id="high_court_chancellor_court_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="high_court_chancellor_court_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="high_court_chancellor_court_vault_to_prev", label="Return back", category="movement", target_scene="high_court_chancellor_court_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_chancellor_court_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_chancellor_court", label="Visit Chancellor G", category="movement", target_scene="high_court_chancellor_court_gate", result_text="You travel to Chancellor Garden.")
    )

    # POI: Knight-Palatine Armory (10 nodes)
    scenes["high_court_knight_barracks_gate"] = SceneNode(
        id="high_court_knight_barracks_gate",
        title="Knight-Palatine Armory - Outer Gate",
        region="high_court",
        description="Iron bars secure the heavy timber entrance. Polished breastplates hang in neat rows.",
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
            Action(id="high_court_knight_barracks_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="high_court_knight_barracks_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="high_court_knight_barracks_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_knight_barracks_gate_to_next", label="Press forward", category="movement", target_scene="high_court_knight_barracks_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_knight_barracks_courtyard"] = SceneNode(
        id="high_court_knight_barracks_courtyard",
        title="Knight-Palatine Armory - Main Courtyard",
        region="high_court",
        description="Cobblestones show heavy cart wheel wear. Polished breastplates hang in neat rows.",
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
            Action(id="high_court_knight_barracks_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="high_court_knight_barracks_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="high_court_knight_barracks_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_knight_barracks_gate", result_text="You retrace your steps."),
            Action(id="high_court_knight_barracks_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_knight_barracks_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_knight_barracks_quarters"] = SceneNode(
        id="high_court_knight_barracks_quarters",
        title="Knight-Palatine Armory - Living Quarters",
        region="high_court",
        description="Rows of wooden bunks line the walls. Polished breastplates hang in neat rows.",
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
            Action(id="high_court_knight_barracks_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="high_court_knight_barracks_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="high_court_knight_barracks_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_knight_barracks_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_knight_barracks_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_knight_barracks_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_knight_barracks_armory"] = SceneNode(
        id="high_court_knight_barracks_armory",
        title="Knight-Palatine Armory - Supply Depot",
        region="high_court",
        description="Crates of rations and tools stand stacked. Polished breastplates hang in neat rows.",
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
            Action(id="high_court_knight_barracks_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="high_court_knight_barracks_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="high_court_knight_barracks_armory_to_prev", label="Return back", category="movement", target_scene="high_court_knight_barracks_quarters", result_text="You retrace your steps."),
            Action(id="high_court_knight_barracks_armory_to_next", label="Press forward", category="movement", target_scene="high_court_knight_barracks_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_knight_barracks_cellar"] = SceneNode(
        id="high_court_knight_barracks_cellar",
        title="Knight-Palatine Armory - Lower Cellar",
        region="high_court",
        description="Damp air smells of cool earth and storage. Polished breastplates hang in neat rows.",
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
            Action(id="high_court_knight_barracks_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="high_court_knight_barracks_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="high_court_knight_barracks_cellar_to_prev", label="Return back", category="movement", target_scene="high_court_knight_barracks_armory", result_text="You retrace your steps."),
            Action(id="high_court_knight_barracks_cellar_to_next", label="Press forward", category="movement", target_scene="high_court_knight_barracks_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_knight_barracks_passage"] = SceneNode(
        id="high_court_knight_barracks_passage",
        title="Knight-Palatine Armory - Stone Corridor",
        region="high_court",
        description="Wall sconces hold flickering tallow candles. Polished breastplates hang in neat rows.",
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
            Action(id="high_court_knight_barracks_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="high_court_knight_barracks_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="high_court_knight_barracks_passage_to_prev", label="Return back", category="movement", target_scene="high_court_knight_barracks_cellar", result_text="You retrace your steps."),
            Action(id="high_court_knight_barracks_passage_to_next", label="Press forward", category="movement", target_scene="high_court_knight_barracks_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_knight_barracks_chamber"] = SceneNode(
        id="high_court_knight_barracks_chamber",
        title="Knight-Palatine Armory - Inner Chamber",
        region="high_court",
        description="A sturdy oak desk holds ledgers and maps. Polished breastplates hang in neat rows.",
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
            Action(id="high_court_knight_barracks_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="high_court_knight_barracks_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="high_court_knight_barracks_chamber_to_prev", label="Return back", category="movement", target_scene="high_court_knight_barracks_passage", result_text="You retrace your steps."),
            Action(id="high_court_knight_barracks_chamber_to_next", label="Press forward", category="movement", target_scene="high_court_knight_barracks_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_knight_barracks_overlook"] = SceneNode(
        id="high_court_knight_barracks_overlook",
        title="Knight-Palatine Armory - High Overlook",
        region="high_court",
        description="A stone ledge provides a clear view. Polished breastplates hang in neat rows.",
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
            Action(id="high_court_knight_barracks_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="high_court_knight_barracks_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="high_court_knight_barracks_overlook_to_prev", label="Return back", category="movement", target_scene="high_court_knight_barracks_chamber", result_text="You retrace your steps."),
            Action(id="high_court_knight_barracks_overlook_to_next", label="Press forward", category="movement", target_scene="high_court_knight_barracks_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_knight_barracks_sanctum"] = SceneNode(
        id="high_court_knight_barracks_sanctum",
        title="Knight-Palatine Armory - Inner Sanctum",
        region="high_court",
        description="A stone altar stands in quiet reverence. Polished breastplates hang in neat rows.",
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
            Action(id="high_court_knight_barracks_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="high_court_knight_barracks_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="high_court_knight_barracks_sanctum_to_prev", label="Return back", category="movement", target_scene="high_court_knight_barracks_overlook", result_text="You retrace your steps."),
            Action(id="high_court_knight_barracks_sanctum_to_next", label="Press forward", category="movement", target_scene="high_court_knight_barracks_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_knight_barracks_vault"] = SceneNode(
        id="high_court_knight_barracks_vault",
        title="Knight-Palatine Armory - Deep Vault",
        region="high_court",
        description="Iron-banded chests sit in deep shadows. Polished breastplates hang in neat rows.",
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
            Action(id="high_court_knight_barracks_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="high_court_knight_barracks_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="high_court_knight_barracks_vault_to_prev", label="Return back", category="movement", target_scene="high_court_knight_barracks_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_knight_barracks_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_knight_barracks", label="Visit Knight-Palat", category="movement", target_scene="high_court_knight_barracks_gate", result_text="You travel to Knight-Palatine Armory.")
    )

    # POI: Catacombs of Kings (10 nodes)
    scenes["high_court_catacomb_kings_gate"] = SceneNode(
        id="high_court_catacomb_kings_gate",
        title="Catacombs of Kings - Outer Gate",
        region="high_court",
        description="Iron bars secure the heavy timber entrance. Marble sarcophagi rest inside cool alcoves.",
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
            Action(id="high_court_catacomb_kings_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="high_court_catacomb_kings_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="high_court_catacomb_kings_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_catacomb_kings_gate_to_next", label="Press forward", category="movement", target_scene="high_court_catacomb_kings_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_catacomb_kings_courtyard"] = SceneNode(
        id="high_court_catacomb_kings_courtyard",
        title="Catacombs of Kings - Main Courtyard",
        region="high_court",
        description="Cobblestones show heavy cart wheel wear. Marble sarcophagi rest inside cool alcoves.",
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
            Action(id="high_court_catacomb_kings_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="high_court_catacomb_kings_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="high_court_catacomb_kings_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_catacomb_kings_gate", result_text="You retrace your steps."),
            Action(id="high_court_catacomb_kings_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_catacomb_kings_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_catacomb_kings_quarters"] = SceneNode(
        id="high_court_catacomb_kings_quarters",
        title="Catacombs of Kings - Living Quarters",
        region="high_court",
        description="Rows of wooden bunks line the walls. Marble sarcophagi rest inside cool alcoves.",
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
            Action(id="high_court_catacomb_kings_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="high_court_catacomb_kings_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="high_court_catacomb_kings_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_catacomb_kings_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_catacomb_kings_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_catacomb_kings_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_catacomb_kings_armory"] = SceneNode(
        id="high_court_catacomb_kings_armory",
        title="Catacombs of Kings - Supply Depot",
        region="high_court",
        description="Crates of rations and tools stand stacked. Marble sarcophagi rest inside cool alcoves.",
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
            Action(id="high_court_catacomb_kings_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="high_court_catacomb_kings_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="high_court_catacomb_kings_armory_to_prev", label="Return back", category="movement", target_scene="high_court_catacomb_kings_quarters", result_text="You retrace your steps."),
            Action(id="high_court_catacomb_kings_armory_to_next", label="Press forward", category="movement", target_scene="high_court_catacomb_kings_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_catacomb_kings_cellar"] = SceneNode(
        id="high_court_catacomb_kings_cellar",
        title="Catacombs of Kings - Lower Cellar",
        region="high_court",
        description="Damp air smells of cool earth and storage. Marble sarcophagi rest inside cool alcoves.",
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
            Action(id="high_court_catacomb_kings_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="high_court_catacomb_kings_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="high_court_catacomb_kings_cellar_to_prev", label="Return back", category="movement", target_scene="high_court_catacomb_kings_armory", result_text="You retrace your steps."),
            Action(id="high_court_catacomb_kings_cellar_to_next", label="Press forward", category="movement", target_scene="high_court_catacomb_kings_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_catacomb_kings_passage"] = SceneNode(
        id="high_court_catacomb_kings_passage",
        title="Catacombs of Kings - Stone Corridor",
        region="high_court",
        description="Wall sconces hold flickering tallow candles. Marble sarcophagi rest inside cool alcoves.",
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
            Action(id="high_court_catacomb_kings_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="high_court_catacomb_kings_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="high_court_catacomb_kings_passage_to_prev", label="Return back", category="movement", target_scene="high_court_catacomb_kings_cellar", result_text="You retrace your steps."),
            Action(id="high_court_catacomb_kings_passage_to_next", label="Press forward", category="movement", target_scene="high_court_catacomb_kings_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_catacomb_kings_chamber"] = SceneNode(
        id="high_court_catacomb_kings_chamber",
        title="Catacombs of Kings - Inner Chamber",
        region="high_court",
        description="A sturdy oak desk holds ledgers and maps. Marble sarcophagi rest inside cool alcoves.",
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
            Action(id="high_court_catacomb_kings_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="high_court_catacomb_kings_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="high_court_catacomb_kings_chamber_to_prev", label="Return back", category="movement", target_scene="high_court_catacomb_kings_passage", result_text="You retrace your steps."),
            Action(id="high_court_catacomb_kings_chamber_to_next", label="Press forward", category="movement", target_scene="high_court_catacomb_kings_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_catacomb_kings_overlook"] = SceneNode(
        id="high_court_catacomb_kings_overlook",
        title="Catacombs of Kings - High Overlook",
        region="high_court",
        description="A stone ledge provides a clear view. Marble sarcophagi rest inside cool alcoves.",
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
            Action(id="high_court_catacomb_kings_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="high_court_catacomb_kings_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="high_court_catacomb_kings_overlook_to_prev", label="Return back", category="movement", target_scene="high_court_catacomb_kings_chamber", result_text="You retrace your steps."),
            Action(id="high_court_catacomb_kings_overlook_to_next", label="Press forward", category="movement", target_scene="high_court_catacomb_kings_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_catacomb_kings_sanctum"] = SceneNode(
        id="high_court_catacomb_kings_sanctum",
        title="Catacombs of Kings - Inner Sanctum",
        region="high_court",
        description="A stone altar stands in quiet reverence. Marble sarcophagi rest inside cool alcoves.",
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
            Action(id="high_court_catacomb_kings_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="high_court_catacomb_kings_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="high_court_catacomb_kings_sanctum_to_prev", label="Return back", category="movement", target_scene="high_court_catacomb_kings_overlook", result_text="You retrace your steps."),
            Action(id="high_court_catacomb_kings_sanctum_to_next", label="Press forward", category="movement", target_scene="high_court_catacomb_kings_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_catacomb_kings_vault"] = SceneNode(
        id="high_court_catacomb_kings_vault",
        title="Catacombs of Kings - Deep Vault",
        region="high_court",
        description="Iron-banded chests sit in deep shadows. Marble sarcophagi rest inside cool alcoves.",
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
            Action(id="high_court_catacomb_kings_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="high_court_catacomb_kings_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="high_court_catacomb_kings_vault_to_prev", label="Return back", category="movement", target_scene="high_court_catacomb_kings_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_catacomb_kings_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_catacomb_kings", label="Visit Catacombs of", category="movement", target_scene="high_court_catacomb_kings_gate", result_text="You travel to Catacombs of Kings.")
    )

    # POI: White Spire Parapet (10 nodes)
    scenes["high_court_high_spire_gate"] = SceneNode(
        id="high_court_high_spire_gate",
        title="White Spire Parapet - Outer Gate",
        region="high_court",
        description="Iron bars secure the heavy timber entrance. Wind flutters heraldic pennants across the walls.",
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
            Action(id="high_court_high_spire_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="high_court_high_spire_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="high_court_high_spire_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_high_spire_gate_to_next", label="Press forward", category="movement", target_scene="high_court_high_spire_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_high_spire_courtyard"] = SceneNode(
        id="high_court_high_spire_courtyard",
        title="White Spire Parapet - Main Courtyard",
        region="high_court",
        description="Cobblestones show heavy cart wheel wear. Wind flutters heraldic pennants across the walls.",
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
            Action(id="high_court_high_spire_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="high_court_high_spire_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="high_court_high_spire_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_high_spire_gate", result_text="You retrace your steps."),
            Action(id="high_court_high_spire_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_high_spire_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_high_spire_quarters"] = SceneNode(
        id="high_court_high_spire_quarters",
        title="White Spire Parapet - Living Quarters",
        region="high_court",
        description="Rows of wooden bunks line the walls. Wind flutters heraldic pennants across the walls.",
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
            Action(id="high_court_high_spire_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="high_court_high_spire_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="high_court_high_spire_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_high_spire_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_high_spire_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_high_spire_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_high_spire_armory"] = SceneNode(
        id="high_court_high_spire_armory",
        title="White Spire Parapet - Supply Depot",
        region="high_court",
        description="Crates of rations and tools stand stacked. Wind flutters heraldic pennants across the walls.",
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
            Action(id="high_court_high_spire_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="high_court_high_spire_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="high_court_high_spire_armory_to_prev", label="Return back", category="movement", target_scene="high_court_high_spire_quarters", result_text="You retrace your steps."),
            Action(id="high_court_high_spire_armory_to_next", label="Press forward", category="movement", target_scene="high_court_high_spire_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_high_spire_cellar"] = SceneNode(
        id="high_court_high_spire_cellar",
        title="White Spire Parapet - Lower Cellar",
        region="high_court",
        description="Damp air smells of cool earth and storage. Wind flutters heraldic pennants across the walls.",
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
            Action(id="high_court_high_spire_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="high_court_high_spire_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="high_court_high_spire_cellar_to_prev", label="Return back", category="movement", target_scene="high_court_high_spire_armory", result_text="You retrace your steps."),
            Action(id="high_court_high_spire_cellar_to_next", label="Press forward", category="movement", target_scene="high_court_high_spire_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_high_spire_passage"] = SceneNode(
        id="high_court_high_spire_passage",
        title="White Spire Parapet - Stone Corridor",
        region="high_court",
        description="Wall sconces hold flickering tallow candles. Wind flutters heraldic pennants across the walls.",
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
            Action(id="high_court_high_spire_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="high_court_high_spire_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="high_court_high_spire_passage_to_prev", label="Return back", category="movement", target_scene="high_court_high_spire_cellar", result_text="You retrace your steps."),
            Action(id="high_court_high_spire_passage_to_next", label="Press forward", category="movement", target_scene="high_court_high_spire_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_high_spire_chamber"] = SceneNode(
        id="high_court_high_spire_chamber",
        title="White Spire Parapet - Inner Chamber",
        region="high_court",
        description="A sturdy oak desk holds ledgers and maps. Wind flutters heraldic pennants across the walls.",
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
            Action(id="high_court_high_spire_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="high_court_high_spire_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="high_court_high_spire_chamber_to_prev", label="Return back", category="movement", target_scene="high_court_high_spire_passage", result_text="You retrace your steps."),
            Action(id="high_court_high_spire_chamber_to_next", label="Press forward", category="movement", target_scene="high_court_high_spire_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_high_spire_overlook"] = SceneNode(
        id="high_court_high_spire_overlook",
        title="White Spire Parapet - High Overlook",
        region="high_court",
        description="A stone ledge provides a clear view. Wind flutters heraldic pennants across the walls.",
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
            Action(id="high_court_high_spire_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="high_court_high_spire_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="high_court_high_spire_overlook_to_prev", label="Return back", category="movement", target_scene="high_court_high_spire_chamber", result_text="You retrace your steps."),
            Action(id="high_court_high_spire_overlook_to_next", label="Press forward", category="movement", target_scene="high_court_high_spire_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_high_spire_sanctum"] = SceneNode(
        id="high_court_high_spire_sanctum",
        title="White Spire Parapet - Inner Sanctum",
        region="high_court",
        description="A stone altar stands in quiet reverence. Wind flutters heraldic pennants across the walls.",
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
            Action(id="high_court_high_spire_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="high_court_high_spire_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="high_court_high_spire_sanctum_to_prev", label="Return back", category="movement", target_scene="high_court_high_spire_overlook", result_text="You retrace your steps."),
            Action(id="high_court_high_spire_sanctum_to_next", label="Press forward", category="movement", target_scene="high_court_high_spire_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_high_spire_vault"] = SceneNode(
        id="high_court_high_spire_vault",
        title="White Spire Parapet - Deep Vault",
        region="high_court",
        description="Iron-banded chests sit in deep shadows. Wind flutters heraldic pennants across the walls.",
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
            Action(id="high_court_high_spire_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="high_court_high_spire_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="high_court_high_spire_vault_to_prev", label="Return back", category="movement", target_scene="high_court_high_spire_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_high_spire_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_high_spire", label="Visit White Spire", category="movement", target_scene="high_court_high_spire_gate", result_text="You travel to White Spire Parapet.")
    )

    # POI: Herald Office (10 nodes)
    scenes["high_court_herald_chamber_gate"] = SceneNode(
        id="high_court_herald_chamber_gate",
        title="Herald Office - Outer Gate",
        region="high_court",
        description="Iron bars secure the heavy timber entrance. Wax seals sit ready on the carved oak table.",
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
            Action(id="high_court_herald_chamber_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="high_court_herald_chamber_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="high_court_herald_chamber_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_gate_to_next", label="Press forward", category="movement", target_scene="high_court_herald_chamber_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_herald_chamber_courtyard"] = SceneNode(
        id="high_court_herald_chamber_courtyard",
        title="Herald Office - Main Courtyard",
        region="high_court",
        description="Cobblestones show heavy cart wheel wear. Wax seals sit ready on the carved oak table.",
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
            Action(id="high_court_herald_chamber_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="high_court_herald_chamber_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="high_court_herald_chamber_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_herald_chamber_gate", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_herald_chamber_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_herald_chamber_quarters"] = SceneNode(
        id="high_court_herald_chamber_quarters",
        title="Herald Office - Living Quarters",
        region="high_court",
        description="Rows of wooden bunks line the walls. Wax seals sit ready on the carved oak table.",
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
            Action(id="high_court_herald_chamber_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="high_court_herald_chamber_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="high_court_herald_chamber_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_herald_chamber_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_herald_chamber_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_herald_chamber_armory"] = SceneNode(
        id="high_court_herald_chamber_armory",
        title="Herald Office - Supply Depot",
        region="high_court",
        description="Crates of rations and tools stand stacked. Wax seals sit ready on the carved oak table.",
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
            Action(id="high_court_herald_chamber_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="high_court_herald_chamber_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="high_court_herald_chamber_armory_to_prev", label="Return back", category="movement", target_scene="high_court_herald_chamber_quarters", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_armory_to_next", label="Press forward", category="movement", target_scene="high_court_herald_chamber_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_herald_chamber_cellar"] = SceneNode(
        id="high_court_herald_chamber_cellar",
        title="Herald Office - Lower Cellar",
        region="high_court",
        description="Damp air smells of cool earth and storage. Wax seals sit ready on the carved oak table.",
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
            Action(id="high_court_herald_chamber_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="high_court_herald_chamber_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="high_court_herald_chamber_cellar_to_prev", label="Return back", category="movement", target_scene="high_court_herald_chamber_armory", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_cellar_to_next", label="Press forward", category="movement", target_scene="high_court_herald_chamber_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_herald_chamber_passage"] = SceneNode(
        id="high_court_herald_chamber_passage",
        title="Herald Office - Stone Corridor",
        region="high_court",
        description="Wall sconces hold flickering tallow candles. Wax seals sit ready on the carved oak table.",
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
            Action(id="high_court_herald_chamber_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="high_court_herald_chamber_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="high_court_herald_chamber_passage_to_prev", label="Return back", category="movement", target_scene="high_court_herald_chamber_cellar", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_passage_to_next", label="Press forward", category="movement", target_scene="high_court_herald_chamber_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_herald_chamber_chamber"] = SceneNode(
        id="high_court_herald_chamber_chamber",
        title="Herald Office - Inner Chamber",
        region="high_court",
        description="A sturdy oak desk holds ledgers and maps. Wax seals sit ready on the carved oak table.",
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
            Action(id="high_court_herald_chamber_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="high_court_herald_chamber_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="high_court_herald_chamber_chamber_to_prev", label="Return back", category="movement", target_scene="high_court_herald_chamber_passage", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_chamber_to_next", label="Press forward", category="movement", target_scene="high_court_herald_chamber_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_herald_chamber_overlook"] = SceneNode(
        id="high_court_herald_chamber_overlook",
        title="Herald Office - High Overlook",
        region="high_court",
        description="A stone ledge provides a clear view. Wax seals sit ready on the carved oak table.",
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
            Action(id="high_court_herald_chamber_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="high_court_herald_chamber_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="high_court_herald_chamber_overlook_to_prev", label="Return back", category="movement", target_scene="high_court_herald_chamber_chamber", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_overlook_to_next", label="Press forward", category="movement", target_scene="high_court_herald_chamber_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_herald_chamber_sanctum"] = SceneNode(
        id="high_court_herald_chamber_sanctum",
        title="Herald Office - Inner Sanctum",
        region="high_court",
        description="A stone altar stands in quiet reverence. Wax seals sit ready on the carved oak table.",
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
            Action(id="high_court_herald_chamber_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="high_court_herald_chamber_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="high_court_herald_chamber_sanctum_to_prev", label="Return back", category="movement", target_scene="high_court_herald_chamber_overlook", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_sanctum_to_next", label="Press forward", category="movement", target_scene="high_court_herald_chamber_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_herald_chamber_vault"] = SceneNode(
        id="high_court_herald_chamber_vault",
        title="Herald Office - Deep Vault",
        region="high_court",
        description="Iron-banded chests sit in deep shadows. Wax seals sit ready on the carved oak table.",
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
            Action(id="high_court_herald_chamber_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="high_court_herald_chamber_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="high_court_herald_chamber_vault_to_prev", label="Return back", category="movement", target_scene="high_court_herald_chamber_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_herald_chamber", label="Visit Herald Offic", category="movement", target_scene="high_court_herald_chamber_gate", result_text="You travel to Herald Office.")
    )

    # POI: Ambassador Salon (10 nodes)
    scenes["high_court_diplomat_lounge_gate"] = SceneNode(
        id="high_court_diplomat_lounge_gate",
        title="Ambassador Salon - Outer Gate",
        region="high_court",
        description="Iron bars secure the heavy timber entrance. Soft chairs sit in the quiet meeting room.",
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
            Action(id="high_court_diplomat_lounge_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="high_court_diplomat_lounge_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="high_court_diplomat_lounge_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_gate_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_diplomat_lounge_courtyard"] = SceneNode(
        id="high_court_diplomat_lounge_courtyard",
        title="Ambassador Salon - Main Courtyard",
        region="high_court",
        description="Cobblestones show heavy cart wheel wear. Soft chairs sit in the quiet meeting room.",
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
            Action(id="high_court_diplomat_lounge_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="high_court_diplomat_lounge_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="high_court_diplomat_lounge_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_gate", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_diplomat_lounge_quarters"] = SceneNode(
        id="high_court_diplomat_lounge_quarters",
        title="Ambassador Salon - Living Quarters",
        region="high_court",
        description="Rows of wooden bunks line the walls. Soft chairs sit in the quiet meeting room.",
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
            Action(id="high_court_diplomat_lounge_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="high_court_diplomat_lounge_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="high_court_diplomat_lounge_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_diplomat_lounge_armory"] = SceneNode(
        id="high_court_diplomat_lounge_armory",
        title="Ambassador Salon - Supply Depot",
        region="high_court",
        description="Crates of rations and tools stand stacked. Soft chairs sit in the quiet meeting room.",
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
            Action(id="high_court_diplomat_lounge_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="high_court_diplomat_lounge_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="high_court_diplomat_lounge_armory_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_quarters", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_armory_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_diplomat_lounge_cellar"] = SceneNode(
        id="high_court_diplomat_lounge_cellar",
        title="Ambassador Salon - Lower Cellar",
        region="high_court",
        description="Damp air smells of cool earth and storage. Soft chairs sit in the quiet meeting room.",
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
            Action(id="high_court_diplomat_lounge_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="high_court_diplomat_lounge_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="high_court_diplomat_lounge_cellar_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_armory", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_cellar_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_diplomat_lounge_passage"] = SceneNode(
        id="high_court_diplomat_lounge_passage",
        title="Ambassador Salon - Stone Corridor",
        region="high_court",
        description="Wall sconces hold flickering tallow candles. Soft chairs sit in the quiet meeting room.",
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
            Action(id="high_court_diplomat_lounge_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="high_court_diplomat_lounge_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="high_court_diplomat_lounge_passage_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_cellar", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_passage_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_diplomat_lounge_chamber"] = SceneNode(
        id="high_court_diplomat_lounge_chamber",
        title="Ambassador Salon - Inner Chamber",
        region="high_court",
        description="A sturdy oak desk holds ledgers and maps. Soft chairs sit in the quiet meeting room.",
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
            Action(id="high_court_diplomat_lounge_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="high_court_diplomat_lounge_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="high_court_diplomat_lounge_chamber_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_passage", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_chamber_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_diplomat_lounge_overlook"] = SceneNode(
        id="high_court_diplomat_lounge_overlook",
        title="Ambassador Salon - High Overlook",
        region="high_court",
        description="A stone ledge provides a clear view. Soft chairs sit in the quiet meeting room.",
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
            Action(id="high_court_diplomat_lounge_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="high_court_diplomat_lounge_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="high_court_diplomat_lounge_overlook_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_chamber", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_overlook_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_diplomat_lounge_sanctum"] = SceneNode(
        id="high_court_diplomat_lounge_sanctum",
        title="Ambassador Salon - Inner Sanctum",
        region="high_court",
        description="A stone altar stands in quiet reverence. Soft chairs sit in the quiet meeting room.",
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
            Action(id="high_court_diplomat_lounge_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="high_court_diplomat_lounge_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="high_court_diplomat_lounge_sanctum_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_overlook", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_sanctum_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_diplomat_lounge_vault"] = SceneNode(
        id="high_court_diplomat_lounge_vault",
        title="Ambassador Salon - Deep Vault",
        region="high_court",
        description="Iron-banded chests sit in deep shadows. Soft chairs sit in the quiet meeting room.",
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
            Action(id="high_court_diplomat_lounge_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="high_court_diplomat_lounge_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="high_court_diplomat_lounge_vault_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_diplomat_lounge", label="Visit Ambassador S", category="movement", target_scene="high_court_diplomat_lounge_gate", result_text="You travel to Ambassador Salon.")
    )

    # POI: Ducal Silver Vault (10 nodes)
    scenes["high_court_silver_vault_gate"] = SceneNode(
        id="high_court_silver_vault_gate",
        title="Ducal Silver Vault - Outer Gate",
        region="high_court",
        description="Iron bars secure the heavy timber entrance. Heavy steel vault doors require three bronze keys.",
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
            Action(id="high_court_silver_vault_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect gate."),
            Action(id="high_court_silver_vault_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to check locks."),
            Action(id="high_court_silver_vault_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_silver_vault_gate_to_next", label="Press forward", category="movement", target_scene="high_court_silver_vault_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_silver_vault_courtyard"] = SceneNode(
        id="high_court_silver_vault_courtyard",
        title="Ducal Silver Vault - Main Courtyard",
        region="high_court",
        description="Cobblestones show heavy cart wheel wear. Heavy steel vault doors require three bronze keys.",
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
            Action(id="high_court_silver_vault_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search yard."),
            Action(id="high_court_silver_vault_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey area."),
            Action(id="high_court_silver_vault_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_silver_vault_gate", result_text="You retrace your steps."),
            Action(id="high_court_silver_vault_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_silver_vault_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_silver_vault_quarters"] = SceneNode(
        id="high_court_silver_vault_quarters",
        title="Ducal Silver Vault - Living Quarters",
        region="high_court",
        description="Rows of wooden bunks line the walls. Heavy steel vault doors require three bronze keys.",
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
            Action(id="high_court_silver_vault_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search bunks."),
            Action(id="high_court_silver_vault_quarters_act_1", label="Rest briefly", category="interaction", result_text="You proceed to rest briefly."),
            Action(id="high_court_silver_vault_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_silver_vault_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_silver_vault_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_silver_vault_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_silver_vault_armory"] = SceneNode(
        id="high_court_silver_vault_armory",
        title="Ducal Silver Vault - Supply Depot",
        region="high_court",
        description="Crates of rations and tools stand stacked. Heavy steel vault doors require three bronze keys.",
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
            Action(id="high_court_silver_vault_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inspect supplies."),
            Action(id="high_court_silver_vault_armory_act_1", label="Take provisions", category="interaction", result_text="You proceed to take provisions."),
            Action(id="high_court_silver_vault_armory_to_prev", label="Return back", category="movement", target_scene="high_court_silver_vault_quarters", result_text="You retrace your steps."),
            Action(id="high_court_silver_vault_armory_to_next", label="Press forward", category="movement", target_scene="high_court_silver_vault_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_silver_vault_cellar"] = SceneNode(
        id="high_court_silver_vault_cellar",
        title="Ducal Silver Vault - Lower Cellar",
        region="high_court",
        description="Damp air smells of cool earth and storage. Heavy steel vault doors require three bronze keys.",
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
            Action(id="high_court_silver_vault_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully check barrels."),
            Action(id="high_court_silver_vault_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to search crates."),
            Action(id="high_court_silver_vault_cellar_to_prev", label="Return back", category="movement", target_scene="high_court_silver_vault_armory", result_text="You retrace your steps."),
            Action(id="high_court_silver_vault_cellar_to_next", label="Press forward", category="movement", target_scene="high_court_silver_vault_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_silver_vault_passage"] = SceneNode(
        id="high_court_silver_vault_passage",
        title="Ducal Silver Vault - Stone Corridor",
        region="high_court",
        description="Wall sconces hold flickering tallow candles. Heavy steel vault doors require three bronze keys.",
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
            Action(id="high_court_silver_vault_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check walls."),
            Action(id="high_court_silver_vault_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to search floor."),
            Action(id="high_court_silver_vault_passage_to_prev", label="Return back", category="movement", target_scene="high_court_silver_vault_cellar", result_text="You retrace your steps."),
            Action(id="high_court_silver_vault_passage_to_next", label="Press forward", category="movement", target_scene="high_court_silver_vault_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_silver_vault_chamber"] = SceneNode(
        id="high_court_silver_vault_chamber",
        title="Ducal Silver Vault - Inner Chamber",
        region="high_court",
        description="A sturdy oak desk holds ledgers and maps. Heavy steel vault doors require three bronze keys.",
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
            Action(id="high_court_silver_vault_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully examine desk."),
            Action(id="high_court_silver_vault_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to read ledger."),
            Action(id="high_court_silver_vault_chamber_to_prev", label="Return back", category="movement", target_scene="high_court_silver_vault_passage", result_text="You retrace your steps."),
            Action(id="high_court_silver_vault_chamber_to_next", label="Press forward", category="movement", target_scene="high_court_silver_vault_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_silver_vault_overlook"] = SceneNode(
        id="high_court_silver_vault_overlook",
        title="Ducal Silver Vault - High Overlook",
        region="high_court",
        description="A stone ledge provides a clear view. Heavy steel vault doors require three bronze keys.",
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
            Action(id="high_court_silver_vault_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scout terrain."),
            Action(id="high_court_silver_vault_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to watch horizon."),
            Action(id="high_court_silver_vault_overlook_to_prev", label="Return back", category="movement", target_scene="high_court_silver_vault_chamber", result_text="You retrace your steps."),
            Action(id="high_court_silver_vault_overlook_to_next", label="Press forward", category="movement", target_scene="high_court_silver_vault_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_silver_vault_sanctum"] = SceneNode(
        id="high_court_silver_vault_sanctum",
        title="Ducal Silver Vault - Inner Sanctum",
        region="high_court",
        description="A stone altar stands in quiet reverence. Heavy steel vault doors require three bronze keys.",
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
            Action(id="high_court_silver_vault_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully examine altar."),
            Action(id="high_court_silver_vault_sanctum_act_1", label="Offer prayer", category="interaction", result_text="You proceed to offer prayer."),
            Action(id="high_court_silver_vault_sanctum_to_prev", label="Return back", category="movement", target_scene="high_court_silver_vault_overlook", result_text="You retrace your steps."),
            Action(id="high_court_silver_vault_sanctum_to_next", label="Press forward", category="movement", target_scene="high_court_silver_vault_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["high_court_silver_vault_vault"] = SceneNode(
        id="high_court_silver_vault_vault",
        title="Ducal Silver Vault - Deep Vault",
        region="high_court",
        description="Iron-banded chests sit in deep shadows. Heavy steel vault doors require three bronze keys.",
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
            Action(id="high_court_silver_vault_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully inspect chests."),
            Action(id="high_court_silver_vault_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search shadows."),
            Action(id="high_court_silver_vault_vault_to_prev", label="Return back", category="movement", target_scene="high_court_silver_vault_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_silver_vault_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_silver_vault", label="Visit Ducal Silver", category="movement", target_scene="high_court_silver_vault_gate", result_text="You travel to Ducal Silver Vault.")
    )

    return RegionManifest(
        id="high_court",
        name="The High Crown of Veras",
        mechanic_name="Legal Evidence & Court Intrigues",
        mechanic_description="Comprehensive open-world region with 10 deep POIs.",
        scenes=scenes
    )