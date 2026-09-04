"""Province: The Reach.
Unique Mechanic: Verticality & Mountain Climbing.
"""
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action

def build_reach_province() -> RegionManifest:
    scenes = {}

    # Province Hub
    scenes["reach_hub"] = SceneNode(
        id="reach_hub",
        title="The Reach - Central Hub",
        region="reach",
        description="Granite peaks loom over the stone waystation. Mountain patrolmen inspect incoming pack mules.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_attribute": {"attribute": "strength", "value": 12}},
                text="Your military posture draws respectful nods from travelers."
            ),
        ],
        base_actions=[
            Action(id="reach_hub_scout", label="Scout hub", category="interaction", result_text="You survey the bustling provincial crossroads."),
            Action(id="reach_hub_rest", label="Rest at inn", category="interaction", effects=[{"modify_stamina": 5}], result_text="You rest and regain stamina."),
            Action(id="reach_hub_board", label="Check notice board", category="interaction", effects=[{"set_flag": {"flag": "reach_notices_read", "value": True}}, {"log_event": "You read the municipal notice board."}], result_text="You read the pinned municipal notices."),
            Action(id="reach_to_bazaar", label="Go to Bazaar", category="movement", target_scene="bazaar_center", result_text="You travel along the highway to the Grand Bazaar."),
        ]
    )

    # POI: Dunwall Fortress (10 nodes)
    scenes["reach_dunwall_fort_gate"] = SceneNode(
        id="reach_dunwall_fort_gate",
        title="Dunwall Fortress - Outer Gate",
        region="reach",
        description="Iron bars secure the heavy timber entrance. Iron battlements crown the sheer cliff face.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_dunwall_fort_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_dunwall_fort_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="reach_dunwall_fort_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="reach_dunwall_fort_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'reach_dunwall_fort_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="reach_dunwall_fort_gate_to_prev", label="Return back", category="movement", target_scene="reach_hub", result_text="You retrace your steps."),
            Action(id="reach_dunwall_fort_gate_to_next", label="Press forward", category="movement", target_scene="reach_dunwall_fort_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_dunwall_fort_courtyard"] = SceneNode(
        id="reach_dunwall_fort_courtyard",
        title="Dunwall Fortress - Main Courtyard",
        region="reach",
        description="Cobblestones show heavy cart wheel wear. Iron battlements crown the sheer cliff face.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_dunwall_fort_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_dunwall_fort_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="reach_dunwall_fort_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="reach_dunwall_fort_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'reach_dunwall_fort_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="reach_dunwall_fort_courtyard_to_prev", label="Return back", category="movement", target_scene="reach_dunwall_fort_gate", result_text="You retrace your steps."),
            Action(id="reach_dunwall_fort_courtyard_to_next", label="Press forward", category="movement", target_scene="reach_dunwall_fort_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_dunwall_fort_quarters"] = SceneNode(
        id="reach_dunwall_fort_quarters",
        title="Dunwall Fortress - Living Quarters",
        region="reach",
        description="Rows of wooden bunks line the walls. Iron battlements crown the sheer cliff face.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_dunwall_fort_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="reach_dunwall_fort_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="reach_dunwall_fort_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'reach_dunwall_fort_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="reach_dunwall_fort_quarters_to_prev", label="Return back", category="movement", target_scene="reach_dunwall_fort_courtyard", result_text="You retrace your steps."),
            Action(id="reach_dunwall_fort_quarters_to_next", label="Press forward", category="movement", target_scene="reach_dunwall_fort_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_dunwall_fort_armory"] = SceneNode(
        id="reach_dunwall_fort_armory",
        title="Dunwall Fortress - Supply Depot",
        region="reach",
        description="Crates of rations and tools stand stacked. Iron battlements crown the sheer cliff face.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_dunwall_fort_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_dunwall_fort_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="reach_dunwall_fort_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="reach_dunwall_fort_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'reach_dunwall_fort_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="reach_dunwall_fort_armory_to_prev", label="Return back", category="movement", target_scene="reach_dunwall_fort_quarters", result_text="You retrace your steps."),
            Action(id="reach_dunwall_fort_armory_to_next", label="Press forward", category="movement", target_scene="reach_dunwall_fort_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_dunwall_fort_cellar"] = SceneNode(
        id="reach_dunwall_fort_cellar",
        title="Dunwall Fortress - Lower Cellar",
        region="reach",
        description="Damp air smells of cool earth and storage. Iron battlements crown the sheer cliff face.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_dunwall_fort_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="reach_dunwall_fort_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="reach_dunwall_fort_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'reach_dunwall_fort_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="reach_dunwall_fort_cellar_to_prev", label="Return back", category="movement", target_scene="reach_dunwall_fort_armory", result_text="You retrace your steps."),
            Action(id="reach_dunwall_fort_cellar_to_next", label="Press forward", category="movement", target_scene="reach_dunwall_fort_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_dunwall_fort_passage"] = SceneNode(
        id="reach_dunwall_fort_passage",
        title="Dunwall Fortress - Stone Corridor",
        region="reach",
        description="Wall sconces hold flickering tallow candles. Iron battlements crown the sheer cliff face.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_dunwall_fort_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_dunwall_fort_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="reach_dunwall_fort_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="reach_dunwall_fort_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'reach_dunwall_fort_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="reach_dunwall_fort_passage_to_prev", label="Return back", category="movement", target_scene="reach_dunwall_fort_cellar", result_text="You retrace your steps."),
            Action(id="reach_dunwall_fort_passage_to_next", label="Press forward", category="movement", target_scene="reach_dunwall_fort_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_dunwall_fort_chamber"] = SceneNode(
        id="reach_dunwall_fort_chamber",
        title="Dunwall Fortress - Inner Chamber",
        region="reach",
        description="A sturdy oak desk holds ledgers and maps. Iron battlements crown the sheer cliff face.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_dunwall_fort_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="reach_dunwall_fort_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="reach_dunwall_fort_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'reach_dunwall_fort_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="reach_dunwall_fort_chamber_to_prev", label="Return back", category="movement", target_scene="reach_dunwall_fort_passage", result_text="You retrace your steps."),
            Action(id="reach_dunwall_fort_chamber_to_next", label="Press forward", category="movement", target_scene="reach_dunwall_fort_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_dunwall_fort_overlook"] = SceneNode(
        id="reach_dunwall_fort_overlook",
        title="Dunwall Fortress - High Overlook",
        region="reach",
        description="A stone ledge provides a clear view. Iron battlements crown the sheer cliff face.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_dunwall_fort_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="reach_dunwall_fort_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="reach_dunwall_fort_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'reach_dunwall_fort_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="reach_dunwall_fort_overlook_to_prev", label="Return back", category="movement", target_scene="reach_dunwall_fort_chamber", result_text="You retrace your steps."),
            Action(id="reach_dunwall_fort_overlook_to_next", label="Press forward", category="movement", target_scene="reach_dunwall_fort_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_dunwall_fort_sanctum"] = SceneNode(
        id="reach_dunwall_fort_sanctum",
        title="Dunwall Fortress - Inner Sanctum",
        region="reach",
        description="A stone altar stands in quiet reverence. Iron battlements crown the sheer cliff face.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_dunwall_fort_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="reach_dunwall_fort_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="reach_dunwall_fort_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'reach_dunwall_fort_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="reach_dunwall_fort_sanctum_to_prev", label="Return back", category="movement", target_scene="reach_dunwall_fort_overlook", result_text="You retrace your steps."),
            Action(id="reach_dunwall_fort_sanctum_to_next", label="Press forward", category="movement", target_scene="reach_dunwall_fort_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_dunwall_fort_vault"] = SceneNode(
        id="reach_dunwall_fort_vault",
        title="Dunwall Fortress - Deep Vault",
        region="reach",
        description="Iron-banded chests sit in deep shadows. Iron battlements crown the sheer cliff face.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_dunwall_fort_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_dunwall_fort_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="reach_dunwall_fort_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="reach_dunwall_fort_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'reach_dunwall_fort_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="reach_dunwall_fort_vault_to_prev", label="Return back", category="movement", target_scene="reach_dunwall_fort_sanctum", result_text="You retrace your steps."),
            Action(id="reach_dunwall_fort_vault_to_hub", label="Return to Hub", category="movement", target_scene="reach_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["reach_hub"].base_actions.append(
        Action(id="reach_hub_to_dunwall_fort", label="Visit Dunwall Fort", category="movement", target_scene="reach_dunwall_fort_gate", result_text="You travel to Dunwall Fortress.")
    )

    # POI: Deep Granite Quarry (10 nodes)
    scenes["reach_granite_mine_gate"] = SceneNode(
        id="reach_granite_mine_gate",
        title="Deep Granite Quarry - Outer Gate",
        region="reach",
        description="Iron bars secure the heavy timber entrance. Picks ring out against dark stone veins.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_granite_mine_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_granite_mine_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="reach_granite_mine_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="reach_granite_mine_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'reach_granite_mine_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="reach_granite_mine_gate_to_prev", label="Return back", category="movement", target_scene="reach_hub", result_text="You retrace your steps."),
            Action(id="reach_granite_mine_gate_to_next", label="Press forward", category="movement", target_scene="reach_granite_mine_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_granite_mine_courtyard"] = SceneNode(
        id="reach_granite_mine_courtyard",
        title="Deep Granite Quarry - Main Courtyard",
        region="reach",
        description="Cobblestones show heavy cart wheel wear. Picks ring out against dark stone veins.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_granite_mine_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_granite_mine_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="reach_granite_mine_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="reach_granite_mine_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'reach_granite_mine_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="reach_granite_mine_courtyard_to_prev", label="Return back", category="movement", target_scene="reach_granite_mine_gate", result_text="You retrace your steps."),
            Action(id="reach_granite_mine_courtyard_to_next", label="Press forward", category="movement", target_scene="reach_granite_mine_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_granite_mine_quarters"] = SceneNode(
        id="reach_granite_mine_quarters",
        title="Deep Granite Quarry - Living Quarters",
        region="reach",
        description="Rows of wooden bunks line the walls. Picks ring out against dark stone veins.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_granite_mine_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="reach_granite_mine_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="reach_granite_mine_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'reach_granite_mine_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="reach_granite_mine_quarters_to_prev", label="Return back", category="movement", target_scene="reach_granite_mine_courtyard", result_text="You retrace your steps."),
            Action(id="reach_granite_mine_quarters_to_next", label="Press forward", category="movement", target_scene="reach_granite_mine_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_granite_mine_armory"] = SceneNode(
        id="reach_granite_mine_armory",
        title="Deep Granite Quarry - Supply Depot",
        region="reach",
        description="Crates of rations and tools stand stacked. Picks ring out against dark stone veins.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_granite_mine_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_granite_mine_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="reach_granite_mine_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="reach_granite_mine_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'reach_granite_mine_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="reach_granite_mine_armory_to_prev", label="Return back", category="movement", target_scene="reach_granite_mine_quarters", result_text="You retrace your steps."),
            Action(id="reach_granite_mine_armory_to_next", label="Press forward", category="movement", target_scene="reach_granite_mine_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_granite_mine_cellar"] = SceneNode(
        id="reach_granite_mine_cellar",
        title="Deep Granite Quarry - Lower Cellar",
        region="reach",
        description="Damp air smells of cool earth and storage. Picks ring out against dark stone veins.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_granite_mine_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="reach_granite_mine_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="reach_granite_mine_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'reach_granite_mine_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="reach_granite_mine_cellar_to_prev", label="Return back", category="movement", target_scene="reach_granite_mine_armory", result_text="You retrace your steps."),
            Action(id="reach_granite_mine_cellar_to_next", label="Press forward", category="movement", target_scene="reach_granite_mine_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_granite_mine_passage"] = SceneNode(
        id="reach_granite_mine_passage",
        title="Deep Granite Quarry - Stone Corridor",
        region="reach",
        description="Wall sconces hold flickering tallow candles. Picks ring out against dark stone veins.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_granite_mine_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_granite_mine_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="reach_granite_mine_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="reach_granite_mine_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'reach_granite_mine_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="reach_granite_mine_passage_to_prev", label="Return back", category="movement", target_scene="reach_granite_mine_cellar", result_text="You retrace your steps."),
            Action(id="reach_granite_mine_passage_to_next", label="Press forward", category="movement", target_scene="reach_granite_mine_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_granite_mine_chamber"] = SceneNode(
        id="reach_granite_mine_chamber",
        title="Deep Granite Quarry - Inner Chamber",
        region="reach",
        description="A sturdy oak desk holds ledgers and maps. Picks ring out against dark stone veins.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_granite_mine_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="reach_granite_mine_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="reach_granite_mine_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'reach_granite_mine_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="reach_granite_mine_chamber_to_prev", label="Return back", category="movement", target_scene="reach_granite_mine_passage", result_text="You retrace your steps."),
            Action(id="reach_granite_mine_chamber_to_next", label="Press forward", category="movement", target_scene="reach_granite_mine_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_granite_mine_overlook"] = SceneNode(
        id="reach_granite_mine_overlook",
        title="Deep Granite Quarry - High Overlook",
        region="reach",
        description="A stone ledge provides a clear view. Picks ring out against dark stone veins.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_granite_mine_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="reach_granite_mine_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="reach_granite_mine_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'reach_granite_mine_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="reach_granite_mine_overlook_to_prev", label="Return back", category="movement", target_scene="reach_granite_mine_chamber", result_text="You retrace your steps."),
            Action(id="reach_granite_mine_overlook_to_next", label="Press forward", category="movement", target_scene="reach_granite_mine_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_granite_mine_sanctum"] = SceneNode(
        id="reach_granite_mine_sanctum",
        title="Deep Granite Quarry - Inner Sanctum",
        region="reach",
        description="A stone altar stands in quiet reverence. Picks ring out against dark stone veins.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_granite_mine_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="reach_granite_mine_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="reach_granite_mine_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'reach_granite_mine_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="reach_granite_mine_sanctum_to_prev", label="Return back", category="movement", target_scene="reach_granite_mine_overlook", result_text="You retrace your steps."),
            Action(id="reach_granite_mine_sanctum_to_next", label="Press forward", category="movement", target_scene="reach_granite_mine_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_granite_mine_vault"] = SceneNode(
        id="reach_granite_mine_vault",
        title="Deep Granite Quarry - Deep Vault",
        region="reach",
        description="Iron-banded chests sit in deep shadows. Picks ring out against dark stone veins.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_granite_mine_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_granite_mine_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="reach_granite_mine_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="reach_granite_mine_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'reach_granite_mine_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="reach_granite_mine_vault_to_prev", label="Return back", category="movement", target_scene="reach_granite_mine_sanctum", result_text="You retrace your steps."),
            Action(id="reach_granite_mine_vault_to_hub", label="Return to Hub", category="movement", target_scene="reach_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["reach_hub"].base_actions.append(
        Action(id="reach_hub_to_granite_mine", label="Visit Deep Granite", category="movement", target_scene="reach_granite_mine_gate", result_text="You travel to Deep Granite Quarry.")
    )

    # POI: Eagle Wing Pass (10 nodes)
    scenes["reach_high_pass_gate"] = SceneNode(
        id="reach_high_pass_gate",
        title="Eagle Wing Pass - Outer Gate",
        region="reach",
        description="Iron bars secure the heavy timber entrance. Narrow ledges wind past frozen mountain waterfalls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_high_pass_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_high_pass_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="reach_high_pass_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="reach_high_pass_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'reach_high_pass_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="reach_high_pass_gate_to_prev", label="Return back", category="movement", target_scene="reach_hub", result_text="You retrace your steps."),
            Action(id="reach_high_pass_gate_to_next", label="Press forward", category="movement", target_scene="reach_high_pass_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_high_pass_courtyard"] = SceneNode(
        id="reach_high_pass_courtyard",
        title="Eagle Wing Pass - Main Courtyard",
        region="reach",
        description="Cobblestones show heavy cart wheel wear. Narrow ledges wind past frozen mountain waterfalls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_high_pass_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_high_pass_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="reach_high_pass_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="reach_high_pass_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'reach_high_pass_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="reach_high_pass_courtyard_to_prev", label="Return back", category="movement", target_scene="reach_high_pass_gate", result_text="You retrace your steps."),
            Action(id="reach_high_pass_courtyard_to_next", label="Press forward", category="movement", target_scene="reach_high_pass_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_high_pass_quarters"] = SceneNode(
        id="reach_high_pass_quarters",
        title="Eagle Wing Pass - Living Quarters",
        region="reach",
        description="Rows of wooden bunks line the walls. Narrow ledges wind past frozen mountain waterfalls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_high_pass_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="reach_high_pass_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="reach_high_pass_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'reach_high_pass_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="reach_high_pass_quarters_to_prev", label="Return back", category="movement", target_scene="reach_high_pass_courtyard", result_text="You retrace your steps."),
            Action(id="reach_high_pass_quarters_to_next", label="Press forward", category="movement", target_scene="reach_high_pass_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_high_pass_armory"] = SceneNode(
        id="reach_high_pass_armory",
        title="Eagle Wing Pass - Supply Depot",
        region="reach",
        description="Crates of rations and tools stand stacked. Narrow ledges wind past frozen mountain waterfalls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_high_pass_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_high_pass_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="reach_high_pass_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="reach_high_pass_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'reach_high_pass_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="reach_high_pass_armory_to_prev", label="Return back", category="movement", target_scene="reach_high_pass_quarters", result_text="You retrace your steps."),
            Action(id="reach_high_pass_armory_to_next", label="Press forward", category="movement", target_scene="reach_high_pass_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_high_pass_cellar"] = SceneNode(
        id="reach_high_pass_cellar",
        title="Eagle Wing Pass - Lower Cellar",
        region="reach",
        description="Damp air smells of cool earth and storage. Narrow ledges wind past frozen mountain waterfalls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_high_pass_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="reach_high_pass_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="reach_high_pass_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'reach_high_pass_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="reach_high_pass_cellar_to_prev", label="Return back", category="movement", target_scene="reach_high_pass_armory", result_text="You retrace your steps."),
            Action(id="reach_high_pass_cellar_to_next", label="Press forward", category="movement", target_scene="reach_high_pass_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_high_pass_passage"] = SceneNode(
        id="reach_high_pass_passage",
        title="Eagle Wing Pass - Stone Corridor",
        region="reach",
        description="Wall sconces hold flickering tallow candles. Narrow ledges wind past frozen mountain waterfalls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_high_pass_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_high_pass_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="reach_high_pass_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="reach_high_pass_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'reach_high_pass_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="reach_high_pass_passage_to_prev", label="Return back", category="movement", target_scene="reach_high_pass_cellar", result_text="You retrace your steps."),
            Action(id="reach_high_pass_passage_to_next", label="Press forward", category="movement", target_scene="reach_high_pass_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_high_pass_chamber"] = SceneNode(
        id="reach_high_pass_chamber",
        title="Eagle Wing Pass - Inner Chamber",
        region="reach",
        description="A sturdy oak desk holds ledgers and maps. Narrow ledges wind past frozen mountain waterfalls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_high_pass_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="reach_high_pass_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="reach_high_pass_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'reach_high_pass_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="reach_high_pass_chamber_to_prev", label="Return back", category="movement", target_scene="reach_high_pass_passage", result_text="You retrace your steps."),
            Action(id="reach_high_pass_chamber_to_next", label="Press forward", category="movement", target_scene="reach_high_pass_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_high_pass_overlook"] = SceneNode(
        id="reach_high_pass_overlook",
        title="Eagle Wing Pass - High Overlook",
        region="reach",
        description="A stone ledge provides a clear view. Narrow ledges wind past frozen mountain waterfalls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_high_pass_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="reach_high_pass_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="reach_high_pass_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'reach_high_pass_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="reach_high_pass_overlook_to_prev", label="Return back", category="movement", target_scene="reach_high_pass_chamber", result_text="You retrace your steps."),
            Action(id="reach_high_pass_overlook_to_next", label="Press forward", category="movement", target_scene="reach_high_pass_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_high_pass_sanctum"] = SceneNode(
        id="reach_high_pass_sanctum",
        title="Eagle Wing Pass - Inner Sanctum",
        region="reach",
        description="A stone altar stands in quiet reverence. Narrow ledges wind past frozen mountain waterfalls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_high_pass_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="reach_high_pass_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="reach_high_pass_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'reach_high_pass_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="reach_high_pass_sanctum_to_prev", label="Return back", category="movement", target_scene="reach_high_pass_overlook", result_text="You retrace your steps."),
            Action(id="reach_high_pass_sanctum_to_next", label="Press forward", category="movement", target_scene="reach_high_pass_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_high_pass_vault"] = SceneNode(
        id="reach_high_pass_vault",
        title="Eagle Wing Pass - Deep Vault",
        region="reach",
        description="Iron-banded chests sit in deep shadows. Narrow ledges wind past frozen mountain waterfalls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_high_pass_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_high_pass_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="reach_high_pass_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="reach_high_pass_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'reach_high_pass_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="reach_high_pass_vault_to_prev", label="Return back", category="movement", target_scene="reach_high_pass_sanctum", result_text="You retrace your steps."),
            Action(id="reach_high_pass_vault_to_hub", label="Return to Hub", category="movement", target_scene="reach_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["reach_hub"].base_actions.append(
        Action(id="reach_hub_to_high_pass", label="Visit Eagle Pass", category="movement", target_scene="reach_high_pass_gate", result_text="You travel to Eagle Wing Pass.")
    )

    # POI: Bandit Bastion (10 nodes)
    scenes["reach_bastion_redoubt_gate"] = SceneNode(
        id="reach_bastion_redoubt_gate",
        title="Bandit Bastion - Outer Gate",
        region="reach",
        description="Iron bars secure the heavy timber entrance. Spiked palisades block the canyon entrance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_bastion_redoubt_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_bastion_redoubt_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="reach_bastion_redoubt_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="reach_bastion_redoubt_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'reach_bastion_redoubt_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="reach_bastion_redoubt_gate_to_prev", label="Return back", category="movement", target_scene="reach_hub", result_text="You retrace your steps."),
            Action(id="reach_bastion_redoubt_gate_to_next", label="Press forward", category="movement", target_scene="reach_bastion_redoubt_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_bastion_redoubt_courtyard"] = SceneNode(
        id="reach_bastion_redoubt_courtyard",
        title="Bandit Bastion - Main Courtyard",
        region="reach",
        description="Cobblestones show heavy cart wheel wear. Spiked palisades block the canyon entrance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_bastion_redoubt_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_bastion_redoubt_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="reach_bastion_redoubt_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="reach_bastion_redoubt_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'reach_bastion_redoubt_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="reach_bastion_redoubt_courtyard_to_prev", label="Return back", category="movement", target_scene="reach_bastion_redoubt_gate", result_text="You retrace your steps."),
            Action(id="reach_bastion_redoubt_courtyard_to_next", label="Press forward", category="movement", target_scene="reach_bastion_redoubt_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_bastion_redoubt_quarters"] = SceneNode(
        id="reach_bastion_redoubt_quarters",
        title="Bandit Bastion - Living Quarters",
        region="reach",
        description="Rows of wooden bunks line the walls. Spiked palisades block the canyon entrance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_bastion_redoubt_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="reach_bastion_redoubt_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="reach_bastion_redoubt_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'reach_bastion_redoubt_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="reach_bastion_redoubt_quarters_to_prev", label="Return back", category="movement", target_scene="reach_bastion_redoubt_courtyard", result_text="You retrace your steps."),
            Action(id="reach_bastion_redoubt_quarters_to_next", label="Press forward", category="movement", target_scene="reach_bastion_redoubt_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_bastion_redoubt_armory"] = SceneNode(
        id="reach_bastion_redoubt_armory",
        title="Bandit Bastion - Supply Depot",
        region="reach",
        description="Crates of rations and tools stand stacked. Spiked palisades block the canyon entrance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_bastion_redoubt_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_bastion_redoubt_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="reach_bastion_redoubt_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="reach_bastion_redoubt_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'reach_bastion_redoubt_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="reach_bastion_redoubt_armory_to_prev", label="Return back", category="movement", target_scene="reach_bastion_redoubt_quarters", result_text="You retrace your steps."),
            Action(id="reach_bastion_redoubt_armory_to_next", label="Press forward", category="movement", target_scene="reach_bastion_redoubt_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_bastion_redoubt_cellar"] = SceneNode(
        id="reach_bastion_redoubt_cellar",
        title="Bandit Bastion - Lower Cellar",
        region="reach",
        description="Damp air smells of cool earth and storage. Spiked palisades block the canyon entrance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_bastion_redoubt_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="reach_bastion_redoubt_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="reach_bastion_redoubt_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'reach_bastion_redoubt_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="reach_bastion_redoubt_cellar_to_prev", label="Return back", category="movement", target_scene="reach_bastion_redoubt_armory", result_text="You retrace your steps."),
            Action(id="reach_bastion_redoubt_cellar_to_next", label="Press forward", category="movement", target_scene="reach_bastion_redoubt_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_bastion_redoubt_passage"] = SceneNode(
        id="reach_bastion_redoubt_passage",
        title="Bandit Bastion - Stone Corridor",
        region="reach",
        description="Wall sconces hold flickering tallow candles. Spiked palisades block the canyon entrance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_bastion_redoubt_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_bastion_redoubt_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="reach_bastion_redoubt_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="reach_bastion_redoubt_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'reach_bastion_redoubt_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="reach_bastion_redoubt_passage_to_prev", label="Return back", category="movement", target_scene="reach_bastion_redoubt_cellar", result_text="You retrace your steps."),
            Action(id="reach_bastion_redoubt_passage_to_next", label="Press forward", category="movement", target_scene="reach_bastion_redoubt_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_bastion_redoubt_chamber"] = SceneNode(
        id="reach_bastion_redoubt_chamber",
        title="Bandit Bastion - Inner Chamber",
        region="reach",
        description="A sturdy oak desk holds ledgers and maps. Spiked palisades block the canyon entrance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_bastion_redoubt_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="reach_bastion_redoubt_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="reach_bastion_redoubt_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'reach_bastion_redoubt_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="reach_bastion_redoubt_chamber_to_prev", label="Return back", category="movement", target_scene="reach_bastion_redoubt_passage", result_text="You retrace your steps."),
            Action(id="reach_bastion_redoubt_chamber_to_next", label="Press forward", category="movement", target_scene="reach_bastion_redoubt_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_bastion_redoubt_overlook"] = SceneNode(
        id="reach_bastion_redoubt_overlook",
        title="Bandit Bastion - High Overlook",
        region="reach",
        description="A stone ledge provides a clear view. Spiked palisades block the canyon entrance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_bastion_redoubt_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="reach_bastion_redoubt_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="reach_bastion_redoubt_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'reach_bastion_redoubt_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="reach_bastion_redoubt_overlook_to_prev", label="Return back", category="movement", target_scene="reach_bastion_redoubt_chamber", result_text="You retrace your steps."),
            Action(id="reach_bastion_redoubt_overlook_to_next", label="Press forward", category="movement", target_scene="reach_bastion_redoubt_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_bastion_redoubt_sanctum"] = SceneNode(
        id="reach_bastion_redoubt_sanctum",
        title="Bandit Bastion - Inner Sanctum",
        region="reach",
        description="A stone altar stands in quiet reverence. Spiked palisades block the canyon entrance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_bastion_redoubt_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="reach_bastion_redoubt_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="reach_bastion_redoubt_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'reach_bastion_redoubt_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="reach_bastion_redoubt_sanctum_to_prev", label="Return back", category="movement", target_scene="reach_bastion_redoubt_overlook", result_text="You retrace your steps."),
            Action(id="reach_bastion_redoubt_sanctum_to_next", label="Press forward", category="movement", target_scene="reach_bastion_redoubt_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_bastion_redoubt_vault"] = SceneNode(
        id="reach_bastion_redoubt_vault",
        title="Bandit Bastion - Deep Vault",
        region="reach",
        description="Iron-banded chests sit in deep shadows. Spiked palisades block the canyon entrance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_bastion_redoubt_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_bastion_redoubt_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="reach_bastion_redoubt_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="reach_bastion_redoubt_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'reach_bastion_redoubt_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="reach_bastion_redoubt_vault_to_prev", label="Return back", category="movement", target_scene="reach_bastion_redoubt_sanctum", result_text="You retrace your steps."),
            Action(id="reach_bastion_redoubt_vault_to_hub", label="Return to Hub", category="movement", target_scene="reach_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["reach_hub"].base_actions.append(
        Action(id="reach_hub_to_bastion_redoubt", label="Visit Bandit Basti", category="movement", target_scene="reach_bastion_redoubt_gate", result_text="You travel to Bandit Bastion.")
    )

    # POI: Ancient Iron Spire (10 nodes)
    scenes["reach_iron_spire_gate"] = SceneNode(
        id="reach_iron_spire_gate",
        title="Ancient Iron Spire - Outer Gate",
        region="reach",
        description="Iron bars secure the heavy timber entrance. Rusted metal towers rise into the mountain clouds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_iron_spire_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_iron_spire_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="reach_iron_spire_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="reach_iron_spire_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'reach_iron_spire_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="reach_iron_spire_gate_to_prev", label="Return back", category="movement", target_scene="reach_hub", result_text="You retrace your steps."),
            Action(id="reach_iron_spire_gate_to_next", label="Press forward", category="movement", target_scene="reach_iron_spire_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_iron_spire_courtyard"] = SceneNode(
        id="reach_iron_spire_courtyard",
        title="Ancient Iron Spire - Main Courtyard",
        region="reach",
        description="Cobblestones show heavy cart wheel wear. Rusted metal towers rise into the mountain clouds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_iron_spire_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_iron_spire_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="reach_iron_spire_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="reach_iron_spire_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'reach_iron_spire_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="reach_iron_spire_courtyard_to_prev", label="Return back", category="movement", target_scene="reach_iron_spire_gate", result_text="You retrace your steps."),
            Action(id="reach_iron_spire_courtyard_to_next", label="Press forward", category="movement", target_scene="reach_iron_spire_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_iron_spire_quarters"] = SceneNode(
        id="reach_iron_spire_quarters",
        title="Ancient Iron Spire - Living Quarters",
        region="reach",
        description="Rows of wooden bunks line the walls. Rusted metal towers rise into the mountain clouds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_iron_spire_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="reach_iron_spire_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="reach_iron_spire_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'reach_iron_spire_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="reach_iron_spire_quarters_to_prev", label="Return back", category="movement", target_scene="reach_iron_spire_courtyard", result_text="You retrace your steps."),
            Action(id="reach_iron_spire_quarters_to_next", label="Press forward", category="movement", target_scene="reach_iron_spire_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_iron_spire_armory"] = SceneNode(
        id="reach_iron_spire_armory",
        title="Ancient Iron Spire - Supply Depot",
        region="reach",
        description="Crates of rations and tools stand stacked. Rusted metal towers rise into the mountain clouds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_iron_spire_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_iron_spire_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="reach_iron_spire_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="reach_iron_spire_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'reach_iron_spire_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="reach_iron_spire_armory_to_prev", label="Return back", category="movement", target_scene="reach_iron_spire_quarters", result_text="You retrace your steps."),
            Action(id="reach_iron_spire_armory_to_next", label="Press forward", category="movement", target_scene="reach_iron_spire_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_iron_spire_cellar"] = SceneNode(
        id="reach_iron_spire_cellar",
        title="Ancient Iron Spire - Lower Cellar",
        region="reach",
        description="Damp air smells of cool earth and storage. Rusted metal towers rise into the mountain clouds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_iron_spire_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="reach_iron_spire_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="reach_iron_spire_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'reach_iron_spire_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="reach_iron_spire_cellar_to_prev", label="Return back", category="movement", target_scene="reach_iron_spire_armory", result_text="You retrace your steps."),
            Action(id="reach_iron_spire_cellar_to_next", label="Press forward", category="movement", target_scene="reach_iron_spire_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_iron_spire_passage"] = SceneNode(
        id="reach_iron_spire_passage",
        title="Ancient Iron Spire - Stone Corridor",
        region="reach",
        description="Wall sconces hold flickering tallow candles. Rusted metal towers rise into the mountain clouds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_iron_spire_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_iron_spire_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="reach_iron_spire_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="reach_iron_spire_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'reach_iron_spire_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="reach_iron_spire_passage_to_prev", label="Return back", category="movement", target_scene="reach_iron_spire_cellar", result_text="You retrace your steps."),
            Action(id="reach_iron_spire_passage_to_next", label="Press forward", category="movement", target_scene="reach_iron_spire_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_iron_spire_chamber"] = SceneNode(
        id="reach_iron_spire_chamber",
        title="Ancient Iron Spire - Inner Chamber",
        region="reach",
        description="A sturdy oak desk holds ledgers and maps. Rusted metal towers rise into the mountain clouds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_iron_spire_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="reach_iron_spire_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="reach_iron_spire_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'reach_iron_spire_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="reach_iron_spire_chamber_to_prev", label="Return back", category="movement", target_scene="reach_iron_spire_passage", result_text="You retrace your steps."),
            Action(id="reach_iron_spire_chamber_to_next", label="Press forward", category="movement", target_scene="reach_iron_spire_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_iron_spire_overlook"] = SceneNode(
        id="reach_iron_spire_overlook",
        title="Ancient Iron Spire - High Overlook",
        region="reach",
        description="A stone ledge provides a clear view. Rusted metal towers rise into the mountain clouds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_iron_spire_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="reach_iron_spire_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="reach_iron_spire_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'reach_iron_spire_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="reach_iron_spire_overlook_to_prev", label="Return back", category="movement", target_scene="reach_iron_spire_chamber", result_text="You retrace your steps."),
            Action(id="reach_iron_spire_overlook_to_next", label="Press forward", category="movement", target_scene="reach_iron_spire_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_iron_spire_sanctum"] = SceneNode(
        id="reach_iron_spire_sanctum",
        title="Ancient Iron Spire - Inner Sanctum",
        region="reach",
        description="A stone altar stands in quiet reverence. Rusted metal towers rise into the mountain clouds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_iron_spire_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="reach_iron_spire_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="reach_iron_spire_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'reach_iron_spire_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="reach_iron_spire_sanctum_to_prev", label="Return back", category="movement", target_scene="reach_iron_spire_overlook", result_text="You retrace your steps."),
            Action(id="reach_iron_spire_sanctum_to_next", label="Press forward", category="movement", target_scene="reach_iron_spire_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_iron_spire_vault"] = SceneNode(
        id="reach_iron_spire_vault",
        title="Ancient Iron Spire - Deep Vault",
        region="reach",
        description="Iron-banded chests sit in deep shadows. Rusted metal towers rise into the mountain clouds.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_iron_spire_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_iron_spire_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="reach_iron_spire_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="reach_iron_spire_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'reach_iron_spire_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="reach_iron_spire_vault_to_prev", label="Return back", category="movement", target_scene="reach_iron_spire_sanctum", result_text="You retrace your steps."),
            Action(id="reach_iron_spire_vault_to_hub", label="Return to Hub", category="movement", target_scene="reach_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["reach_hub"].base_actions.append(
        Action(id="reach_hub_to_iron_spire", label="Visit Ancient Iron", category="movement", target_scene="reach_iron_spire_gate", result_text="You travel to Ancient Iron Spire.")
    )

    # POI: Windy Gorge (10 nodes)
    scenes["reach_wind_hollow_gate"] = SceneNode(
        id="reach_wind_hollow_gate",
        title="Windy Gorge - Outer Gate",
        region="reach",
        description="Iron bars secure the heavy timber entrance. Cold wind blows through the narrow stone gap.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_wind_hollow_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_wind_hollow_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="reach_wind_hollow_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="reach_wind_hollow_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'reach_wind_hollow_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="reach_wind_hollow_gate_to_prev", label="Return back", category="movement", target_scene="reach_hub", result_text="You retrace your steps."),
            Action(id="reach_wind_hollow_gate_to_next", label="Press forward", category="movement", target_scene="reach_wind_hollow_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_wind_hollow_courtyard"] = SceneNode(
        id="reach_wind_hollow_courtyard",
        title="Windy Gorge - Main Courtyard",
        region="reach",
        description="Cobblestones show heavy cart wheel wear. Cold wind blows through the narrow stone gap.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_wind_hollow_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_wind_hollow_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="reach_wind_hollow_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="reach_wind_hollow_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'reach_wind_hollow_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="reach_wind_hollow_courtyard_to_prev", label="Return back", category="movement", target_scene="reach_wind_hollow_gate", result_text="You retrace your steps."),
            Action(id="reach_wind_hollow_courtyard_to_next", label="Press forward", category="movement", target_scene="reach_wind_hollow_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_wind_hollow_quarters"] = SceneNode(
        id="reach_wind_hollow_quarters",
        title="Windy Gorge - Living Quarters",
        region="reach",
        description="Rows of wooden bunks line the walls. Cold wind blows through the narrow stone gap.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_wind_hollow_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="reach_wind_hollow_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="reach_wind_hollow_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'reach_wind_hollow_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="reach_wind_hollow_quarters_to_prev", label="Return back", category="movement", target_scene="reach_wind_hollow_courtyard", result_text="You retrace your steps."),
            Action(id="reach_wind_hollow_quarters_to_next", label="Press forward", category="movement", target_scene="reach_wind_hollow_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_wind_hollow_armory"] = SceneNode(
        id="reach_wind_hollow_armory",
        title="Windy Gorge - Supply Depot",
        region="reach",
        description="Crates of rations and tools stand stacked. Cold wind blows through the narrow stone gap.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_wind_hollow_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_wind_hollow_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="reach_wind_hollow_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="reach_wind_hollow_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'reach_wind_hollow_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="reach_wind_hollow_armory_to_prev", label="Return back", category="movement", target_scene="reach_wind_hollow_quarters", result_text="You retrace your steps."),
            Action(id="reach_wind_hollow_armory_to_next", label="Press forward", category="movement", target_scene="reach_wind_hollow_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_wind_hollow_cellar"] = SceneNode(
        id="reach_wind_hollow_cellar",
        title="Windy Gorge - Lower Cellar",
        region="reach",
        description="Damp air smells of cool earth and storage. Cold wind blows through the narrow stone gap.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_wind_hollow_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="reach_wind_hollow_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="reach_wind_hollow_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'reach_wind_hollow_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="reach_wind_hollow_cellar_to_prev", label="Return back", category="movement", target_scene="reach_wind_hollow_armory", result_text="You retrace your steps."),
            Action(id="reach_wind_hollow_cellar_to_next", label="Press forward", category="movement", target_scene="reach_wind_hollow_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_wind_hollow_passage"] = SceneNode(
        id="reach_wind_hollow_passage",
        title="Windy Gorge - Stone Corridor",
        region="reach",
        description="Wall sconces hold flickering tallow candles. Cold wind blows through the narrow stone gap.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_wind_hollow_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_wind_hollow_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="reach_wind_hollow_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="reach_wind_hollow_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'reach_wind_hollow_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="reach_wind_hollow_passage_to_prev", label="Return back", category="movement", target_scene="reach_wind_hollow_cellar", result_text="You retrace your steps."),
            Action(id="reach_wind_hollow_passage_to_next", label="Press forward", category="movement", target_scene="reach_wind_hollow_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_wind_hollow_chamber"] = SceneNode(
        id="reach_wind_hollow_chamber",
        title="Windy Gorge - Inner Chamber",
        region="reach",
        description="A sturdy oak desk holds ledgers and maps. Cold wind blows through the narrow stone gap.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_wind_hollow_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="reach_wind_hollow_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="reach_wind_hollow_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'reach_wind_hollow_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="reach_wind_hollow_chamber_to_prev", label="Return back", category="movement", target_scene="reach_wind_hollow_passage", result_text="You retrace your steps."),
            Action(id="reach_wind_hollow_chamber_to_next", label="Press forward", category="movement", target_scene="reach_wind_hollow_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_wind_hollow_overlook"] = SceneNode(
        id="reach_wind_hollow_overlook",
        title="Windy Gorge - High Overlook",
        region="reach",
        description="A stone ledge provides a clear view. Cold wind blows through the narrow stone gap.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_wind_hollow_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="reach_wind_hollow_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="reach_wind_hollow_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'reach_wind_hollow_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="reach_wind_hollow_overlook_to_prev", label="Return back", category="movement", target_scene="reach_wind_hollow_chamber", result_text="You retrace your steps."),
            Action(id="reach_wind_hollow_overlook_to_next", label="Press forward", category="movement", target_scene="reach_wind_hollow_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_wind_hollow_sanctum"] = SceneNode(
        id="reach_wind_hollow_sanctum",
        title="Windy Gorge - Inner Sanctum",
        region="reach",
        description="A stone altar stands in quiet reverence. Cold wind blows through the narrow stone gap.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_wind_hollow_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="reach_wind_hollow_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="reach_wind_hollow_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'reach_wind_hollow_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="reach_wind_hollow_sanctum_to_prev", label="Return back", category="movement", target_scene="reach_wind_hollow_overlook", result_text="You retrace your steps."),
            Action(id="reach_wind_hollow_sanctum_to_next", label="Press forward", category="movement", target_scene="reach_wind_hollow_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_wind_hollow_vault"] = SceneNode(
        id="reach_wind_hollow_vault",
        title="Windy Gorge - Deep Vault",
        region="reach",
        description="Iron-banded chests sit in deep shadows. Cold wind blows through the narrow stone gap.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_wind_hollow_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_wind_hollow_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="reach_wind_hollow_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="reach_wind_hollow_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'reach_wind_hollow_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="reach_wind_hollow_vault_to_prev", label="Return back", category="movement", target_scene="reach_wind_hollow_sanctum", result_text="You retrace your steps."),
            Action(id="reach_wind_hollow_vault_to_hub", label="Return to Hub", category="movement", target_scene="reach_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["reach_hub"].base_actions.append(
        Action(id="reach_hub_to_wind_hollow", label="Visit Windy Gorge", category="movement", target_scene="reach_wind_hollow_gate", result_text="You travel to Windy Gorge.")
    )

    # POI: Highland Timber Camp (10 nodes)
    scenes["reach_timber_camp_gate"] = SceneNode(
        id="reach_timber_camp_gate",
        title="Highland Timber Camp - Outer Gate",
        region="reach",
        description="Iron bars secure the heavy timber entrance. Fresh pine logs lie stacked along the trail.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_timber_camp_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_timber_camp_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="reach_timber_camp_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="reach_timber_camp_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'reach_timber_camp_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="reach_timber_camp_gate_to_prev", label="Return back", category="movement", target_scene="reach_hub", result_text="You retrace your steps."),
            Action(id="reach_timber_camp_gate_to_next", label="Press forward", category="movement", target_scene="reach_timber_camp_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_timber_camp_courtyard"] = SceneNode(
        id="reach_timber_camp_courtyard",
        title="Highland Timber Camp - Main Courtyard",
        region="reach",
        description="Cobblestones show heavy cart wheel wear. Fresh pine logs lie stacked along the trail.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_timber_camp_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_timber_camp_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="reach_timber_camp_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="reach_timber_camp_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'reach_timber_camp_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="reach_timber_camp_courtyard_to_prev", label="Return back", category="movement", target_scene="reach_timber_camp_gate", result_text="You retrace your steps."),
            Action(id="reach_timber_camp_courtyard_to_next", label="Press forward", category="movement", target_scene="reach_timber_camp_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_timber_camp_quarters"] = SceneNode(
        id="reach_timber_camp_quarters",
        title="Highland Timber Camp - Living Quarters",
        region="reach",
        description="Rows of wooden bunks line the walls. Fresh pine logs lie stacked along the trail.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_timber_camp_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="reach_timber_camp_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="reach_timber_camp_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'reach_timber_camp_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="reach_timber_camp_quarters_to_prev", label="Return back", category="movement", target_scene="reach_timber_camp_courtyard", result_text="You retrace your steps."),
            Action(id="reach_timber_camp_quarters_to_next", label="Press forward", category="movement", target_scene="reach_timber_camp_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_timber_camp_armory"] = SceneNode(
        id="reach_timber_camp_armory",
        title="Highland Timber Camp - Supply Depot",
        region="reach",
        description="Crates of rations and tools stand stacked. Fresh pine logs lie stacked along the trail.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_timber_camp_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_timber_camp_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="reach_timber_camp_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="reach_timber_camp_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'reach_timber_camp_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="reach_timber_camp_armory_to_prev", label="Return back", category="movement", target_scene="reach_timber_camp_quarters", result_text="You retrace your steps."),
            Action(id="reach_timber_camp_armory_to_next", label="Press forward", category="movement", target_scene="reach_timber_camp_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_timber_camp_cellar"] = SceneNode(
        id="reach_timber_camp_cellar",
        title="Highland Timber Camp - Lower Cellar",
        region="reach",
        description="Damp air smells of cool earth and storage. Fresh pine logs lie stacked along the trail.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_timber_camp_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="reach_timber_camp_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="reach_timber_camp_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'reach_timber_camp_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="reach_timber_camp_cellar_to_prev", label="Return back", category="movement", target_scene="reach_timber_camp_armory", result_text="You retrace your steps."),
            Action(id="reach_timber_camp_cellar_to_next", label="Press forward", category="movement", target_scene="reach_timber_camp_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_timber_camp_passage"] = SceneNode(
        id="reach_timber_camp_passage",
        title="Highland Timber Camp - Stone Corridor",
        region="reach",
        description="Wall sconces hold flickering tallow candles. Fresh pine logs lie stacked along the trail.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_timber_camp_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_timber_camp_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="reach_timber_camp_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="reach_timber_camp_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'reach_timber_camp_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="reach_timber_camp_passage_to_prev", label="Return back", category="movement", target_scene="reach_timber_camp_cellar", result_text="You retrace your steps."),
            Action(id="reach_timber_camp_passage_to_next", label="Press forward", category="movement", target_scene="reach_timber_camp_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_timber_camp_chamber"] = SceneNode(
        id="reach_timber_camp_chamber",
        title="Highland Timber Camp - Inner Chamber",
        region="reach",
        description="A sturdy oak desk holds ledgers and maps. Fresh pine logs lie stacked along the trail.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_timber_camp_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="reach_timber_camp_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="reach_timber_camp_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'reach_timber_camp_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="reach_timber_camp_chamber_to_prev", label="Return back", category="movement", target_scene="reach_timber_camp_passage", result_text="You retrace your steps."),
            Action(id="reach_timber_camp_chamber_to_next", label="Press forward", category="movement", target_scene="reach_timber_camp_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_timber_camp_overlook"] = SceneNode(
        id="reach_timber_camp_overlook",
        title="Highland Timber Camp - High Overlook",
        region="reach",
        description="A stone ledge provides a clear view. Fresh pine logs lie stacked along the trail.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_timber_camp_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="reach_timber_camp_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="reach_timber_camp_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'reach_timber_camp_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="reach_timber_camp_overlook_to_prev", label="Return back", category="movement", target_scene="reach_timber_camp_chamber", result_text="You retrace your steps."),
            Action(id="reach_timber_camp_overlook_to_next", label="Press forward", category="movement", target_scene="reach_timber_camp_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_timber_camp_sanctum"] = SceneNode(
        id="reach_timber_camp_sanctum",
        title="Highland Timber Camp - Inner Sanctum",
        region="reach",
        description="A stone altar stands in quiet reverence. Fresh pine logs lie stacked along the trail.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_timber_camp_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="reach_timber_camp_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="reach_timber_camp_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'reach_timber_camp_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="reach_timber_camp_sanctum_to_prev", label="Return back", category="movement", target_scene="reach_timber_camp_overlook", result_text="You retrace your steps."),
            Action(id="reach_timber_camp_sanctum_to_next", label="Press forward", category="movement", target_scene="reach_timber_camp_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_timber_camp_vault"] = SceneNode(
        id="reach_timber_camp_vault",
        title="Highland Timber Camp - Deep Vault",
        region="reach",
        description="Iron-banded chests sit in deep shadows. Fresh pine logs lie stacked along the trail.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_timber_camp_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_timber_camp_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="reach_timber_camp_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="reach_timber_camp_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'reach_timber_camp_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="reach_timber_camp_vault_to_prev", label="Return back", category="movement", target_scene="reach_timber_camp_sanctum", result_text="You retrace your steps."),
            Action(id="reach_timber_camp_vault_to_hub", label="Return to Hub", category="movement", target_scene="reach_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["reach_hub"].base_actions.append(
        Action(id="reach_hub_to_timber_camp", label="Visit Highland Tim", category="movement", target_scene="reach_timber_camp_gate", result_text="You travel to Highland Timber Camp.")
    )

    # POI: Glacial Cavern (10 nodes)
    scenes["reach_frost_cavern_gate"] = SceneNode(
        id="reach_frost_cavern_gate",
        title="Glacial Cavern - Outer Gate",
        region="reach",
        description="Iron bars secure the heavy timber entrance. Blue ice walls echo with dripping water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_frost_cavern_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_frost_cavern_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="reach_frost_cavern_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="reach_frost_cavern_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'reach_frost_cavern_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="reach_frost_cavern_gate_to_prev", label="Return back", category="movement", target_scene="reach_hub", result_text="You retrace your steps."),
            Action(id="reach_frost_cavern_gate_to_next", label="Press forward", category="movement", target_scene="reach_frost_cavern_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_frost_cavern_courtyard"] = SceneNode(
        id="reach_frost_cavern_courtyard",
        title="Glacial Cavern - Main Courtyard",
        region="reach",
        description="Cobblestones show heavy cart wheel wear. Blue ice walls echo with dripping water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_frost_cavern_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_frost_cavern_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="reach_frost_cavern_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="reach_frost_cavern_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'reach_frost_cavern_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="reach_frost_cavern_courtyard_to_prev", label="Return back", category="movement", target_scene="reach_frost_cavern_gate", result_text="You retrace your steps."),
            Action(id="reach_frost_cavern_courtyard_to_next", label="Press forward", category="movement", target_scene="reach_frost_cavern_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_frost_cavern_quarters"] = SceneNode(
        id="reach_frost_cavern_quarters",
        title="Glacial Cavern - Living Quarters",
        region="reach",
        description="Rows of wooden bunks line the walls. Blue ice walls echo with dripping water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_frost_cavern_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="reach_frost_cavern_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="reach_frost_cavern_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'reach_frost_cavern_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="reach_frost_cavern_quarters_to_prev", label="Return back", category="movement", target_scene="reach_frost_cavern_courtyard", result_text="You retrace your steps."),
            Action(id="reach_frost_cavern_quarters_to_next", label="Press forward", category="movement", target_scene="reach_frost_cavern_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_frost_cavern_armory"] = SceneNode(
        id="reach_frost_cavern_armory",
        title="Glacial Cavern - Supply Depot",
        region="reach",
        description="Crates of rations and tools stand stacked. Blue ice walls echo with dripping water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_frost_cavern_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_frost_cavern_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="reach_frost_cavern_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="reach_frost_cavern_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'reach_frost_cavern_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="reach_frost_cavern_armory_to_prev", label="Return back", category="movement", target_scene="reach_frost_cavern_quarters", result_text="You retrace your steps."),
            Action(id="reach_frost_cavern_armory_to_next", label="Press forward", category="movement", target_scene="reach_frost_cavern_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_frost_cavern_cellar"] = SceneNode(
        id="reach_frost_cavern_cellar",
        title="Glacial Cavern - Lower Cellar",
        region="reach",
        description="Damp air smells of cool earth and storage. Blue ice walls echo with dripping water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_frost_cavern_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="reach_frost_cavern_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="reach_frost_cavern_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'reach_frost_cavern_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="reach_frost_cavern_cellar_to_prev", label="Return back", category="movement", target_scene="reach_frost_cavern_armory", result_text="You retrace your steps."),
            Action(id="reach_frost_cavern_cellar_to_next", label="Press forward", category="movement", target_scene="reach_frost_cavern_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_frost_cavern_passage"] = SceneNode(
        id="reach_frost_cavern_passage",
        title="Glacial Cavern - Stone Corridor",
        region="reach",
        description="Wall sconces hold flickering tallow candles. Blue ice walls echo with dripping water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_frost_cavern_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_frost_cavern_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="reach_frost_cavern_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="reach_frost_cavern_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'reach_frost_cavern_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="reach_frost_cavern_passage_to_prev", label="Return back", category="movement", target_scene="reach_frost_cavern_cellar", result_text="You retrace your steps."),
            Action(id="reach_frost_cavern_passage_to_next", label="Press forward", category="movement", target_scene="reach_frost_cavern_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_frost_cavern_chamber"] = SceneNode(
        id="reach_frost_cavern_chamber",
        title="Glacial Cavern - Inner Chamber",
        region="reach",
        description="A sturdy oak desk holds ledgers and maps. Blue ice walls echo with dripping water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_frost_cavern_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="reach_frost_cavern_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="reach_frost_cavern_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'reach_frost_cavern_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="reach_frost_cavern_chamber_to_prev", label="Return back", category="movement", target_scene="reach_frost_cavern_passage", result_text="You retrace your steps."),
            Action(id="reach_frost_cavern_chamber_to_next", label="Press forward", category="movement", target_scene="reach_frost_cavern_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_frost_cavern_overlook"] = SceneNode(
        id="reach_frost_cavern_overlook",
        title="Glacial Cavern - High Overlook",
        region="reach",
        description="A stone ledge provides a clear view. Blue ice walls echo with dripping water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_frost_cavern_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="reach_frost_cavern_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="reach_frost_cavern_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'reach_frost_cavern_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="reach_frost_cavern_overlook_to_prev", label="Return back", category="movement", target_scene="reach_frost_cavern_chamber", result_text="You retrace your steps."),
            Action(id="reach_frost_cavern_overlook_to_next", label="Press forward", category="movement", target_scene="reach_frost_cavern_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_frost_cavern_sanctum"] = SceneNode(
        id="reach_frost_cavern_sanctum",
        title="Glacial Cavern - Inner Sanctum",
        region="reach",
        description="A stone altar stands in quiet reverence. Blue ice walls echo with dripping water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="A hidden crevasse glimmers faintly behind the frost-covered altar."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_frost_cavern_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="reach_frost_cavern_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="reach_frost_cavern_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'reach_frost_cavern_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="reach_frost_cavern_sanctum_to_prev", label="Return back", category="movement", target_scene="reach_frost_cavern_overlook", result_text="You retrace your steps."),
            Action(id="reach_frost_cavern_sanctum_to_next", label="Press forward", category="movement", target_scene="reach_frost_cavern_vault", result_text="You press on to the next area."),
            Action(id="reach_frost_cavern_to_secret_shrine", label="Enter hidden crevasse", category="trait_exploit", condition={"has_trait": "night_eyed"}, target_scene="reach_secret_shrine", result_text="Your dark sight guides you through the narrow ice fissure."),
        ]
    )

    scenes["reach_secret_shrine"] = SceneNode(
        id="reach_secret_shrine",
        title="Glacial Cavern - Secret Alpine Shrine",
        region="reach",
        description="Pale starlight filters through high crystalline crevasses. A carved stone icon rests on an ancient ice dais.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes pick out faint constellations etched into the ice dais."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You spot ancient mountain footholds cut into the chimney."
            ),
            DynamicDescription(
                condition={"ancestry_is": "deep-dweller"},
                text="Your subterranean blood recognizes the ancient cold stone craft."
            ),
            DynamicDescription(
                condition={"background_is": "noble_exile"},
                text="Highborn archives mentioned this forgotten redoubt of the first clans."
            ),
        ],
        base_actions=[
            Action(id="reach_secret_shrine_act_0", label="Pray at icon", category="interaction", effects=[{"modify_stamina": 3}, {"log_event": "A tranquil mountain stillness restores your focus."}], result_text="You offer a silent prayer before the frost icon."),
            Action(id="reach_secret_shrine_act_1", label="Search ice dais", category="interaction", effects=[{"add_item": "ice_lotus"}, {"log_event": "You gathered a frozen alpine blossom."}], result_text="You discover a preserved ice lotus tucked beneath the pedestal."),
            Action(id="reach_secret_shrine_act_2", label="Study frost runes", category="interaction", effects=[{"log_event": "You traced the cold geometric carvings."}], result_text="Faint chill numbs your fingertips as you touch the runes."),
            Action(id="reach_secret_shrine_to_sanctum", label="Return to sanctum", category="movement", target_scene="reach_frost_cavern_sanctum", result_text="You retrace your steps through the crevasse."),
        ]
    )

    scenes["reach_frost_cavern_vault"] = SceneNode(
        id="reach_frost_cavern_vault",
        title="Glacial Cavern - Deep Vault",
        region="reach",
        description="Iron-banded chests sit in deep shadows. Blue ice walls echo with dripping water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_frost_cavern_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_frost_cavern_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="reach_frost_cavern_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="reach_frost_cavern_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'reach_frost_cavern_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="reach_frost_cavern_vault_to_prev", label="Return back", category="movement", target_scene="reach_frost_cavern_sanctum", result_text="You retrace your steps."),
            Action(id="reach_frost_cavern_vault_to_hub", label="Return to Hub", category="movement", target_scene="reach_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["reach_hub"].base_actions.append(
        Action(id="reach_hub_to_frost_cavern", label="Visit Glacial Cave", category="movement", target_scene="reach_frost_cavern_gate", result_text="You travel to Glacial Cavern.")
    )

    # POI: Old Watchtower Ruin (10 nodes)
    scenes["reach_watch_ruin_gate"] = SceneNode(
        id="reach_watch_ruin_gate",
        title="Old Watchtower Ruin - Outer Gate",
        region="reach",
        description="Iron bars secure the heavy timber entrance. Old stone walls look over the green valley below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_watch_ruin_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_watch_ruin_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="reach_watch_ruin_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="reach_watch_ruin_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'reach_watch_ruin_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="reach_watch_ruin_gate_to_prev", label="Return back", category="movement", target_scene="reach_hub", result_text="You retrace your steps."),
            Action(id="reach_watch_ruin_gate_to_next", label="Press forward", category="movement", target_scene="reach_watch_ruin_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_watch_ruin_courtyard"] = SceneNode(
        id="reach_watch_ruin_courtyard",
        title="Old Watchtower Ruin - Main Courtyard",
        region="reach",
        description="Cobblestones show heavy cart wheel wear. Old stone walls look over the green valley below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_watch_ruin_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_watch_ruin_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="reach_watch_ruin_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="reach_watch_ruin_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'reach_watch_ruin_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="reach_watch_ruin_courtyard_to_prev", label="Return back", category="movement", target_scene="reach_watch_ruin_gate", result_text="You retrace your steps."),
            Action(id="reach_watch_ruin_courtyard_to_next", label="Press forward", category="movement", target_scene="reach_watch_ruin_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_watch_ruin_quarters"] = SceneNode(
        id="reach_watch_ruin_quarters",
        title="Old Watchtower Ruin - Living Quarters",
        region="reach",
        description="Rows of wooden bunks line the walls. Old stone walls look over the green valley below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_watch_ruin_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="reach_watch_ruin_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="reach_watch_ruin_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'reach_watch_ruin_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="reach_watch_ruin_quarters_to_prev", label="Return back", category="movement", target_scene="reach_watch_ruin_courtyard", result_text="You retrace your steps."),
            Action(id="reach_watch_ruin_quarters_to_next", label="Press forward", category="movement", target_scene="reach_watch_ruin_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_watch_ruin_armory"] = SceneNode(
        id="reach_watch_ruin_armory",
        title="Old Watchtower Ruin - Supply Depot",
        region="reach",
        description="Crates of rations and tools stand stacked. Old stone walls look over the green valley below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_watch_ruin_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_watch_ruin_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="reach_watch_ruin_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="reach_watch_ruin_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'reach_watch_ruin_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="reach_watch_ruin_armory_to_prev", label="Return back", category="movement", target_scene="reach_watch_ruin_quarters", result_text="You retrace your steps."),
            Action(id="reach_watch_ruin_armory_to_next", label="Press forward", category="movement", target_scene="reach_watch_ruin_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_watch_ruin_cellar"] = SceneNode(
        id="reach_watch_ruin_cellar",
        title="Old Watchtower Ruin - Lower Cellar",
        region="reach",
        description="Damp air smells of cool earth and storage. Old stone walls look over the green valley below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_watch_ruin_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="reach_watch_ruin_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="reach_watch_ruin_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'reach_watch_ruin_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="reach_watch_ruin_cellar_to_prev", label="Return back", category="movement", target_scene="reach_watch_ruin_armory", result_text="You retrace your steps."),
            Action(id="reach_watch_ruin_cellar_to_next", label="Press forward", category="movement", target_scene="reach_watch_ruin_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_watch_ruin_passage"] = SceneNode(
        id="reach_watch_ruin_passage",
        title="Old Watchtower Ruin - Stone Corridor",
        region="reach",
        description="Wall sconces hold flickering tallow candles. Old stone walls look over the green valley below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_watch_ruin_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_watch_ruin_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="reach_watch_ruin_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="reach_watch_ruin_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'reach_watch_ruin_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="reach_watch_ruin_passage_to_prev", label="Return back", category="movement", target_scene="reach_watch_ruin_cellar", result_text="You retrace your steps."),
            Action(id="reach_watch_ruin_passage_to_next", label="Press forward", category="movement", target_scene="reach_watch_ruin_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_watch_ruin_chamber"] = SceneNode(
        id="reach_watch_ruin_chamber",
        title="Old Watchtower Ruin - Inner Chamber",
        region="reach",
        description="A sturdy oak desk holds ledgers and maps. Old stone walls look over the green valley below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_watch_ruin_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="reach_watch_ruin_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="reach_watch_ruin_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'reach_watch_ruin_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="reach_watch_ruin_chamber_to_prev", label="Return back", category="movement", target_scene="reach_watch_ruin_passage", result_text="You retrace your steps."),
            Action(id="reach_watch_ruin_chamber_to_next", label="Press forward", category="movement", target_scene="reach_watch_ruin_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_watch_ruin_overlook"] = SceneNode(
        id="reach_watch_ruin_overlook",
        title="Old Watchtower Ruin - High Overlook",
        region="reach",
        description="A stone ledge provides a clear view. Old stone walls look over the green valley below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_watch_ruin_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="reach_watch_ruin_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="reach_watch_ruin_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'reach_watch_ruin_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="reach_watch_ruin_overlook_to_prev", label="Return back", category="movement", target_scene="reach_watch_ruin_chamber", result_text="You retrace your steps."),
            Action(id="reach_watch_ruin_overlook_to_next", label="Press forward", category="movement", target_scene="reach_watch_ruin_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_watch_ruin_sanctum"] = SceneNode(
        id="reach_watch_ruin_sanctum",
        title="Old Watchtower Ruin - Inner Sanctum",
        region="reach",
        description="A stone altar stands in quiet reverence. Old stone walls look over the green valley below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_watch_ruin_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="reach_watch_ruin_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="reach_watch_ruin_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'reach_watch_ruin_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="reach_watch_ruin_sanctum_to_prev", label="Return back", category="movement", target_scene="reach_watch_ruin_overlook", result_text="You retrace your steps."),
            Action(id="reach_watch_ruin_sanctum_to_next", label="Press forward", category="movement", target_scene="reach_watch_ruin_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_watch_ruin_vault"] = SceneNode(
        id="reach_watch_ruin_vault",
        title="Old Watchtower Ruin - Deep Vault",
        region="reach",
        description="Iron-banded chests sit in deep shadows. Old stone walls look over the green valley below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_watch_ruin_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_watch_ruin_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="reach_watch_ruin_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="reach_watch_ruin_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'reach_watch_ruin_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="reach_watch_ruin_vault_to_prev", label="Return back", category="movement", target_scene="reach_watch_ruin_sanctum", result_text="You retrace your steps."),
            Action(id="reach_watch_ruin_vault_to_hub", label="Return to Hub", category="movement", target_scene="reach_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["reach_hub"].base_actions.append(
        Action(id="reach_hub_to_watch_ruin", label="Visit Old Watchtow", category="movement", target_scene="reach_watch_ruin_gate", result_text="You travel to Old Watchtower Ruin.")
    )

    # POI: Signal Fire Bluff (10 nodes)
    scenes["reach_signal_crag_gate"] = SceneNode(
        id="reach_signal_crag_gate",
        title="Signal Fire Bluff - Outer Gate",
        region="reach",
        description="Iron bars secure the heavy timber entrance. Stacked cedar kindling sits ready for lighting.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_signal_crag_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_signal_crag_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="reach_signal_crag_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="reach_signal_crag_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'reach_signal_crag_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="reach_signal_crag_gate_to_prev", label="Return back", category="movement", target_scene="reach_hub", result_text="You retrace your steps."),
            Action(id="reach_signal_crag_gate_to_next", label="Press forward", category="movement", target_scene="reach_signal_crag_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_signal_crag_courtyard"] = SceneNode(
        id="reach_signal_crag_courtyard",
        title="Signal Fire Bluff - Main Courtyard",
        region="reach",
        description="Cobblestones show heavy cart wheel wear. Stacked cedar kindling sits ready for lighting.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_signal_crag_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_signal_crag_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="reach_signal_crag_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="reach_signal_crag_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'reach_signal_crag_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="reach_signal_crag_courtyard_to_prev", label="Return back", category="movement", target_scene="reach_signal_crag_gate", result_text="You retrace your steps."),
            Action(id="reach_signal_crag_courtyard_to_next", label="Press forward", category="movement", target_scene="reach_signal_crag_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_signal_crag_quarters"] = SceneNode(
        id="reach_signal_crag_quarters",
        title="Signal Fire Bluff - Living Quarters",
        region="reach",
        description="Rows of wooden bunks line the walls. Stacked cedar kindling sits ready for lighting.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_signal_crag_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="reach_signal_crag_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="reach_signal_crag_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'reach_signal_crag_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="reach_signal_crag_quarters_to_prev", label="Return back", category="movement", target_scene="reach_signal_crag_courtyard", result_text="You retrace your steps."),
            Action(id="reach_signal_crag_quarters_to_next", label="Press forward", category="movement", target_scene="reach_signal_crag_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_signal_crag_armory"] = SceneNode(
        id="reach_signal_crag_armory",
        title="Signal Fire Bluff - Supply Depot",
        region="reach",
        description="Crates of rations and tools stand stacked. Stacked cedar kindling sits ready for lighting.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_signal_crag_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_signal_crag_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="reach_signal_crag_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="reach_signal_crag_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'reach_signal_crag_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="reach_signal_crag_armory_to_prev", label="Return back", category="movement", target_scene="reach_signal_crag_quarters", result_text="You retrace your steps."),
            Action(id="reach_signal_crag_armory_to_next", label="Press forward", category="movement", target_scene="reach_signal_crag_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_signal_crag_cellar"] = SceneNode(
        id="reach_signal_crag_cellar",
        title="Signal Fire Bluff - Lower Cellar",
        region="reach",
        description="Damp air smells of cool earth and storage. Stacked cedar kindling sits ready for lighting.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_signal_crag_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="reach_signal_crag_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="reach_signal_crag_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'reach_signal_crag_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="reach_signal_crag_cellar_to_prev", label="Return back", category="movement", target_scene="reach_signal_crag_armory", result_text="You retrace your steps."),
            Action(id="reach_signal_crag_cellar_to_next", label="Press forward", category="movement", target_scene="reach_signal_crag_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_signal_crag_passage"] = SceneNode(
        id="reach_signal_crag_passage",
        title="Signal Fire Bluff - Stone Corridor",
        region="reach",
        description="Wall sconces hold flickering tallow candles. Stacked cedar kindling sits ready for lighting.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_signal_crag_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="reach_signal_crag_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="reach_signal_crag_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="reach_signal_crag_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'reach_signal_crag_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="reach_signal_crag_passage_to_prev", label="Return back", category="movement", target_scene="reach_signal_crag_cellar", result_text="You retrace your steps."),
            Action(id="reach_signal_crag_passage_to_next", label="Press forward", category="movement", target_scene="reach_signal_crag_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_signal_crag_chamber"] = SceneNode(
        id="reach_signal_crag_chamber",
        title="Signal Fire Bluff - Inner Chamber",
        region="reach",
        description="A sturdy oak desk holds ledgers and maps. Stacked cedar kindling sits ready for lighting.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_signal_crag_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="reach_signal_crag_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="reach_signal_crag_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'reach_signal_crag_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="reach_signal_crag_chamber_to_prev", label="Return back", category="movement", target_scene="reach_signal_crag_passage", result_text="You retrace your steps."),
            Action(id="reach_signal_crag_chamber_to_next", label="Press forward", category="movement", target_scene="reach_signal_crag_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_signal_crag_overlook"] = SceneNode(
        id="reach_signal_crag_overlook",
        title="Signal Fire Bluff - High Overlook",
        region="reach",
        description="A stone ledge provides a clear view. Stacked cedar kindling sits ready for lighting.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_signal_crag_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="reach_signal_crag_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="reach_signal_crag_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'reach_signal_crag_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="reach_signal_crag_overlook_to_prev", label="Return back", category="movement", target_scene="reach_signal_crag_chamber", result_text="You retrace your steps."),
            Action(id="reach_signal_crag_overlook_to_next", label="Press forward", category="movement", target_scene="reach_signal_crag_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_signal_crag_sanctum"] = SceneNode(
        id="reach_signal_crag_sanctum",
        title="Signal Fire Bluff - Inner Sanctum",
        region="reach",
        description="A stone altar stands in quiet reverence. Stacked cedar kindling sits ready for lighting.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="reach_signal_crag_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="reach_signal_crag_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="reach_signal_crag_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'reach_signal_crag_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="reach_signal_crag_sanctum_to_prev", label="Return back", category="movement", target_scene="reach_signal_crag_overlook", result_text="You retrace your steps."),
            Action(id="reach_signal_crag_sanctum_to_next", label="Press forward", category="movement", target_scene="reach_signal_crag_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["reach_signal_crag_vault"] = SceneNode(
        id="reach_signal_crag_vault",
        title="Signal Fire Bluff - Deep Vault",
        region="reach",
        description="Iron-banded chests sit in deep shadows. Stacked cedar kindling sits ready for lighting.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'reach_signal_crag_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="reach_signal_crag_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="reach_signal_crag_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="reach_signal_crag_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'reach_signal_crag_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="reach_signal_crag_vault_to_prev", label="Return back", category="movement", target_scene="reach_signal_crag_sanctum", result_text="You retrace your steps."),
            Action(id="reach_signal_crag_vault_to_hub", label="Return to Hub", category="movement", target_scene="reach_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["reach_hub"].base_actions.append(
        Action(id="reach_hub_to_signal_crag", label="Visit Signal Fire", category="movement", target_scene="reach_signal_crag_gate", result_text="You travel to Signal Fire Bluff.")
    )

    return RegionManifest(
        id="reach",
        name="The Reach",
        mechanic_name="Verticality & Mountain Climbing",
        mechanic_description="Comprehensive open-world region with 10 deep POIs.",
        scenes=scenes
    )