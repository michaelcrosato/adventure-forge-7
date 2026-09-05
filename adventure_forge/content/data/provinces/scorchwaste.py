"""Province: The Scorchwaste.
Unique Mechanic: Ambient Heat & Hydration Survival.
"""
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action

def build_scorchwaste_province() -> RegionManifest:
    scenes = {}

    # Province Hub
    scenes["scorchwaste_hub"] = SceneNode(
        id="scorchwaste_hub",
        title="The Scorchwaste - Central Hub",
        region="scorchwaste",
        description="Red sandstone cliffs frame the desert gateway. Caravan camels drink at the stone trough.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_attribute": {"attribute": "strength", "value": 12}},
                text="Your military posture draws respectful nods from travelers."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_hub_scout", label="Scout hub", category="interaction", result_text="You survey the bustling provincial crossroads."),
            Action(id="scorchwaste_hub_rest", label="Rest at inn", category="interaction", effects=[{"modify_stamina": 5}], result_text="You rest and regain stamina."),
            Action(id="scorchwaste_hub_board", label="Check notice board", category="interaction", effects=[{"set_flag": {"flag": "scorchwaste_notices_read", "value": True}}, {"log_event": "You read the municipal notice board."}], result_text="You read the pinned municipal notices."),
            Action(id="scorch_baron_end_liberate", label="Free the water", category="interaction", condition={"flag_is": {"flag": "scorch_cistern_diverted", "value": True}, "lacks_flag": "scorch_baron_resolved"}, effects=[{"set_flag": {"flag": "scorch_baron_resolved", "value": True}}, {"set_flag": {"flag": "scorch_water_liberated", "value": True}}, {"modify_reputation": {"faction": "desert_nomads", "value": 30}}, {"log_event": "You broke the monopoly and freed the wells."}], result_text="Nomads cheer as cool water flows freely across the dunes."),
            Action(id="scorch_baron_end_treaty", label="Sign water pact", category="interaction", condition={"flag_is": {"flag": "scorch_cistern_diverted", "value": True}, "lacks_flag": "scorch_baron_resolved"}, effects=[{"set_flag": {"flag": "scorch_baron_resolved", "value": True}}, {"set_flag": {"flag": "scorch_water_negotiated", "value": True}}, {"modify_reputation": {"faction": "oasis_merchants", "value": 20}}, {"log_event": "You brokered a fair water agreement."}], result_text="The baron yields to regulated prices for desert travelers."),
            Action(id="scorch_baron_end_claim", label="Claim the wells", category="interaction", condition={"flag_is": {"flag": "scorch_cistern_diverted", "value": True}, "lacks_flag": "scorch_baron_resolved"}, effects=[{"set_flag": {"flag": "scorch_baron_resolved", "value": True}}, {"set_flag": {"flag": "scorch_water_claimed", "value": True}}, {"log_event": "You seized the deep wells as the new water baron."}], result_text="You claim the deep water keys and rule the oasis."),
            Action(id="scorch_war_end_free_water", label="Free The Waters", category="social", condition={"all_of": [{"flag_is": {"flag": "scorch_crisis_resolved", "value": True}}, {"lacks_flag": "scorch_war_resolved"}]}, effects=[{"set_flag": {"flag": "scorch_war_resolved", "value": True}}, {"set_flag": {"flag": "scorch_ending_free_water", "value": True}}, {"modify_reputation": {"faction": "desert_nomads", "value": 30}}, {"modify_reputation": {"faction": "salt_raiders", "value": -25}}, {"log_event": "You broke the Salt Cartel monopoly and freed the desert aquifer."}], result_text="Cool aquifer water rushes through open sluices into nomad cisterns."),
            Action(id="scorch_war_end_monopoly", label="Enforce Cartel Monopoly", category="social", condition={"all_of": [{"flag_is": {"flag": "scorch_crisis_resolved", "value": True}}, {"lacks_flag": "scorch_war_resolved"}]}, effects=[{"set_flag": {"flag": "scorch_war_resolved", "value": True}}, {"set_flag": {"flag": "scorch_ending_cartel_monopoly", "value": True}}, {"modify_reputation": {"faction": "salt_raiders", "value": 30}}, {"modify_reputation": {"faction": "desert_nomads", "value": -25}}, {"log_event": "You enforced the Salt Cartel monopoly over the desert wells."}], result_text="Armed cartel guards bar the wells and extract heavy tithes."),
            Action(id="scorch_war_end_concordat", label="Ratify Dune Concordat", category="social", condition={"all_of": [{"flag_is": {"flag": "scorch_crisis_resolved", "value": True}}, {"lacks_flag": "scorch_war_resolved"}]}, effects=[{"set_flag": {"flag": "scorch_war_resolved", "value": True}}, {"set_flag": {"flag": "scorch_ending_concordat", "value": True}}, {"modify_reputation": {"faction": "desert_nomads", "value": 15}}, {"modify_reputation": {"faction": "salt_raiders", "value": 15}}, {"modify_reputation": {"faction": "caravaneers", "value": 20}}, {"log_event": "You brokered a fair desalination treaty between all clans."}], result_text="Nomad elders and caravan masters sign the shared water concordat."),
            Action(id="scorch_war_end_autocrat", label="Claim Aquifer Keys", category="trait_exploit", condition={"all_of": [{"flag_is": {"flag": "scorch_crisis_resolved", "value": True}}, {"lacks_flag": "scorch_war_resolved"}]}, effects=[{"set_flag": {"flag": "scorch_war_resolved", "value": True}}, {"set_flag": {"flag": "scorch_ending_autocrat", "value": True}}, {"modify_reputation": {"faction": "desert_nomads", "value": -10}}, {"modify_reputation": {"faction": "salt_raiders", "value": -10}}, {"log_event": "You seized sole control of the desert aquifer keys."}], result_text="You turn the grand bronze wheel and claim dominion over the dunes."),
            Action(id="scorchwaste_to_bazaar", label="Go to Bazaar", category="movement", target_scene="bazaar_center", result_text="You travel along the highway to the Grand Bazaar."),
        ]
    )

    # POI: The Ashen Gate (10 nodes)
    scenes["scorchwaste_ashen_gate_gate"] = SceneNode(
        id="scorchwaste_ashen_gate_gate",
        title="The Ashen Gate - Outer Gate",
        region="scorchwaste",
        description="Iron bars secure the heavy timber entrance. Carved stone monoliths guard the sun-bleached pass.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_ashen_gate_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_ashen_gate_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="scorchwaste_ashen_gate_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="scorchwaste_ashen_gate_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_ashen_gate_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="scorchwaste_ashen_gate_gate_to_prev", label="Return back", category="movement", target_scene="scorchwaste_hub", result_text="You retrace your steps."),
            Action(id="scorchwaste_ashen_gate_gate_to_next", label="Press forward", category="movement", target_scene="scorchwaste_ashen_gate_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_ashen_gate_courtyard"] = SceneNode(
        id="scorchwaste_ashen_gate_courtyard",
        title="The Ashen Gate - Main Courtyard",
        region="scorchwaste",
        description="Cobblestones show heavy cart wheel wear. Carved stone monoliths guard the sun-bleached pass.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_ashen_gate_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_ashen_gate_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="scorchwaste_ashen_gate_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="scorchwaste_ashen_gate_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_ashen_gate_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="scorchwaste_ashen_gate_courtyard_to_prev", label="Return back", category="movement", target_scene="scorchwaste_ashen_gate_gate", result_text="You retrace your steps."),
            Action(id="scorchwaste_ashen_gate_courtyard_to_next", label="Press forward", category="movement", target_scene="scorchwaste_ashen_gate_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_ashen_gate_quarters"] = SceneNode(
        id="scorchwaste_ashen_gate_quarters",
        title="The Ashen Gate - Living Quarters",
        region="scorchwaste",
        description="Rows of wooden bunks line the walls. Carved stone monoliths guard the sun-bleached pass.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_ashen_gate_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="scorchwaste_ashen_gate_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="scorchwaste_ashen_gate_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_ashen_gate_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="scorchwaste_ashen_gate_quarters_to_prev", label="Return back", category="movement", target_scene="scorchwaste_ashen_gate_courtyard", result_text="You retrace your steps."),
            Action(id="scorchwaste_ashen_gate_quarters_to_next", label="Press forward", category="movement", target_scene="scorchwaste_ashen_gate_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_ashen_gate_armory"] = SceneNode(
        id="scorchwaste_ashen_gate_armory",
        title="The Ashen Gate - Supply Depot",
        region="scorchwaste",
        description="Crates of rations and tools stand stacked. Carved stone monoliths guard the sun-bleached pass.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_ashen_gate_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_ashen_gate_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="scorchwaste_ashen_gate_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="scorchwaste_ashen_gate_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_ashen_gate_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="scorchwaste_ashen_gate_armory_to_prev", label="Return back", category="movement", target_scene="scorchwaste_ashen_gate_quarters", result_text="You retrace your steps."),
            Action(id="scorchwaste_ashen_gate_armory_to_next", label="Press forward", category="movement", target_scene="scorchwaste_ashen_gate_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_ashen_gate_cellar"] = SceneNode(
        id="scorchwaste_ashen_gate_cellar",
        title="The Ashen Gate - Lower Cellar",
        region="scorchwaste",
        description="Damp air smells of cool earth and storage. Carved stone monoliths guard the sun-bleached pass.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_ashen_gate_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="scorchwaste_ashen_gate_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="scorchwaste_ashen_gate_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_ashen_gate_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="scorchwaste_ashen_gate_cellar_to_prev", label="Return back", category="movement", target_scene="scorchwaste_ashen_gate_armory", result_text="You retrace your steps."),
            Action(id="scorchwaste_ashen_gate_cellar_to_next", label="Press forward", category="movement", target_scene="scorchwaste_ashen_gate_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_ashen_gate_passage"] = SceneNode(
        id="scorchwaste_ashen_gate_passage",
        title="The Ashen Gate - Stone Corridor",
        region="scorchwaste",
        description="Wall sconces hold flickering tallow candles. Carved stone monoliths guard the sun-bleached pass.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_ashen_gate_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_ashen_gate_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="scorchwaste_ashen_gate_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="scorchwaste_ashen_gate_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_ashen_gate_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="scorchwaste_ashen_gate_passage_to_prev", label="Return back", category="movement", target_scene="scorchwaste_ashen_gate_cellar", result_text="You retrace your steps."),
            Action(id="scorchwaste_ashen_gate_passage_to_next", label="Press forward", category="movement", target_scene="scorchwaste_ashen_gate_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_ashen_gate_chamber"] = SceneNode(
        id="scorchwaste_ashen_gate_chamber",
        title="The Ashen Gate - Inner Chamber",
        region="scorchwaste",
        description="A sturdy oak desk holds ledgers and maps. Carved stone monoliths guard the sun-bleached pass.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_ashen_gate_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="scorchwaste_ashen_gate_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="scorchwaste_ashen_gate_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_ashen_gate_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="scorchwaste_ashen_gate_chamber_to_prev", label="Return back", category="movement", target_scene="scorchwaste_ashen_gate_passage", result_text="You retrace your steps."),
            Action(id="scorchwaste_ashen_gate_chamber_to_next", label="Press forward", category="movement", target_scene="scorchwaste_ashen_gate_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_ashen_gate_overlook"] = SceneNode(
        id="scorchwaste_ashen_gate_overlook",
        title="The Ashen Gate - High Overlook",
        region="scorchwaste",
        description="A stone ledge provides a clear view. Carved stone monoliths guard the sun-bleached pass.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_ashen_gate_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="scorchwaste_ashen_gate_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="scorchwaste_ashen_gate_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_ashen_gate_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="scorchwaste_ashen_gate_overlook_to_prev", label="Return back", category="movement", target_scene="scorchwaste_ashen_gate_chamber", result_text="You retrace your steps."),
            Action(id="scorchwaste_ashen_gate_overlook_to_next", label="Press forward", category="movement", target_scene="scorchwaste_ashen_gate_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_ashen_gate_sanctum"] = SceneNode(
        id="scorchwaste_ashen_gate_sanctum",
        title="The Ashen Gate - Inner Sanctum",
        region="scorchwaste",
        description="A stone altar stands in quiet reverence. Carved stone monoliths guard the sun-bleached pass.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_ashen_gate_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="scorchwaste_ashen_gate_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="scorchwaste_ashen_gate_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_ashen_gate_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="scorchwaste_ashen_gate_sanctum_to_prev", label="Return back", category="movement", target_scene="scorchwaste_ashen_gate_overlook", result_text="You retrace your steps."),
            Action(id="scorchwaste_ashen_gate_sanctum_to_next", label="Press forward", category="movement", target_scene="scorchwaste_ashen_gate_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_ashen_gate_vault"] = SceneNode(
        id="scorchwaste_ashen_gate_vault",
        title="The Ashen Gate - Deep Vault",
        region="scorchwaste",
        description="Iron-banded chests sit in deep shadows. Carved stone monoliths guard the sun-bleached pass.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_ashen_gate_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_ashen_gate_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="scorchwaste_ashen_gate_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="scorchwaste_ashen_gate_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_ashen_gate_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="scorchwaste_ashen_gate_vault_to_prev", label="Return back", category="movement", target_scene="scorchwaste_ashen_gate_sanctum", result_text="You retrace your steps."),
            Action(id="scorchwaste_ashen_gate_vault_to_hub", label="Return to Hub", category="movement", target_scene="scorchwaste_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["scorchwaste_hub"].base_actions.append(
        Action(id="scorchwaste_hub_to_ashen_gate", label="Visit Ashen Gate", category="movement", target_scene="scorchwaste_ashen_gate_gate", result_text="You travel to The Ashen Gate.")
    )

    # POI: Nomad Tent Camp (10 nodes)
    scenes["scorchwaste_mirage_camp_gate"] = SceneNode(
        id="scorchwaste_mirage_camp_gate",
        title="Nomad Tent Camp - Outer Gate",
        region="scorchwaste",
        description="Iron bars secure the heavy timber entrance. Woven wool awnings cast deep crimson shade.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_mirage_camp_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_mirage_camp_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="scorchwaste_mirage_camp_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="scorchwaste_mirage_camp_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_mirage_camp_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="scorchwaste_mirage_camp_gate_to_prev", label="Return back", category="movement", target_scene="scorchwaste_hub", result_text="You retrace your steps."),
            Action(id="scorchwaste_mirage_camp_gate_to_next", label="Press forward", category="movement", target_scene="scorchwaste_mirage_camp_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_mirage_camp_courtyard"] = SceneNode(
        id="scorchwaste_mirage_camp_courtyard",
        title="Nomad Tent Camp - Main Courtyard",
        region="scorchwaste",
        description="Cobblestones show heavy cart wheel wear. Woven wool awnings cast deep crimson shade.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_mirage_camp_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_mirage_camp_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="scorchwaste_mirage_camp_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="scorchwaste_mirage_camp_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_mirage_camp_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="scorchwaste_mirage_camp_courtyard_to_prev", label="Return back", category="movement", target_scene="scorchwaste_mirage_camp_gate", result_text="You retrace your steps."),
            Action(id="scorchwaste_mirage_camp_courtyard_to_next", label="Press forward", category="movement", target_scene="scorchwaste_mirage_camp_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_mirage_camp_quarters"] = SceneNode(
        id="scorchwaste_mirage_camp_quarters",
        title="Nomad Tent Camp - Living Quarters",
        region="scorchwaste",
        description="Rows of wooden bunks line the walls. Woven wool awnings cast deep crimson shade.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_mirage_camp_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="scorchwaste_mirage_camp_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="scorchwaste_mirage_camp_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_mirage_camp_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="scorchwaste_mirage_camp_quarters_to_prev", label="Return back", category="movement", target_scene="scorchwaste_mirage_camp_courtyard", result_text="You retrace your steps."),
            Action(id="scorchwaste_mirage_camp_quarters_to_next", label="Press forward", category="movement", target_scene="scorchwaste_mirage_camp_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_mirage_camp_armory"] = SceneNode(
        id="scorchwaste_mirage_camp_armory",
        title="Nomad Tent Camp - Supply Depot",
        region="scorchwaste",
        description="Crates of rations and tools stand stacked. Woven wool awnings cast deep crimson shade.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_mirage_camp_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_mirage_camp_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="scorchwaste_mirage_camp_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="scorchwaste_mirage_camp_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_mirage_camp_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="scorchwaste_mirage_camp_armory_to_prev", label="Return back", category="movement", target_scene="scorchwaste_mirage_camp_quarters", result_text="You retrace your steps."),
            Action(id="scorchwaste_mirage_camp_armory_to_next", label="Press forward", category="movement", target_scene="scorchwaste_mirage_camp_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_mirage_camp_cellar"] = SceneNode(
        id="scorchwaste_mirage_camp_cellar",
        title="Nomad Tent Camp - Lower Cellar",
        region="scorchwaste",
        description="Damp air smells of cool earth and storage. Woven wool awnings cast deep crimson shade.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_mirage_camp_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="scorchwaste_mirage_camp_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="scorchwaste_mirage_camp_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_mirage_camp_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="scorchwaste_mirage_camp_cellar_to_prev", label="Return back", category="movement", target_scene="scorchwaste_mirage_camp_armory", result_text="You retrace your steps."),
            Action(id="scorchwaste_mirage_camp_cellar_to_next", label="Press forward", category="movement", target_scene="scorchwaste_mirage_camp_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_mirage_camp_passage"] = SceneNode(
        id="scorchwaste_mirage_camp_passage",
        title="Nomad Tent Camp - Stone Corridor",
        region="scorchwaste",
        description="Wall sconces hold flickering tallow candles. Woven wool awnings cast deep crimson shade.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_mirage_camp_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_mirage_camp_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="scorchwaste_mirage_camp_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="scorchwaste_mirage_camp_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_mirage_camp_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="scorchwaste_mirage_camp_passage_to_prev", label="Return back", category="movement", target_scene="scorchwaste_mirage_camp_cellar", result_text="You retrace your steps."),
            Action(id="scorchwaste_mirage_camp_passage_to_next", label="Press forward", category="movement", target_scene="scorchwaste_mirage_camp_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_mirage_camp_chamber"] = SceneNode(
        id="scorchwaste_mirage_camp_chamber",
        title="Nomad Tent Camp - Inner Chamber",
        region="scorchwaste",
        description="A sturdy oak desk holds ledgers and maps. Woven wool awnings cast deep crimson shade.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_mirage_camp_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="scorchwaste_mirage_camp_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="scorchwaste_mirage_camp_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_mirage_camp_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="scorchwaste_mirage_camp_chamber_to_prev", label="Return back", category="movement", target_scene="scorchwaste_mirage_camp_passage", result_text="You retrace your steps."),
            Action(id="scorchwaste_mirage_camp_chamber_to_next", label="Press forward", category="movement", target_scene="scorchwaste_mirage_camp_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_mirage_camp_overlook"] = SceneNode(
        id="scorchwaste_mirage_camp_overlook",
        title="Nomad Tent Camp - High Overlook",
        region="scorchwaste",
        description="A stone ledge provides a clear view. Woven wool awnings cast deep crimson shade.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_mirage_camp_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="scorchwaste_mirage_camp_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="scorchwaste_mirage_camp_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_mirage_camp_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="scorchwaste_mirage_camp_overlook_to_prev", label="Return back", category="movement", target_scene="scorchwaste_mirage_camp_chamber", result_text="You retrace your steps."),
            Action(id="scorchwaste_mirage_camp_overlook_to_next", label="Press forward", category="movement", target_scene="scorchwaste_mirage_camp_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_mirage_camp_sanctum"] = SceneNode(
        id="scorchwaste_mirage_camp_sanctum",
        title="Nomad Tent Camp - Inner Sanctum",
        region="scorchwaste",
        description="A stone altar stands in quiet reverence. Woven wool awnings cast deep crimson shade.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_mirage_camp_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="scorchwaste_mirage_camp_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="scorchwaste_mirage_camp_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_mirage_camp_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="scorchwaste_mirage_camp_sanctum_to_prev", label="Return back", category="movement", target_scene="scorchwaste_mirage_camp_overlook", result_text="You retrace your steps."),
            Action(id="scorchwaste_mirage_camp_sanctum_to_next", label="Press forward", category="movement", target_scene="scorchwaste_mirage_camp_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_mirage_camp_vault"] = SceneNode(
        id="scorchwaste_mirage_camp_vault",
        title="Nomad Tent Camp - Deep Vault",
        region="scorchwaste",
        description="Iron-banded chests sit in deep shadows. Woven wool awnings cast deep crimson shade.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_mirage_camp_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_mirage_camp_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="scorchwaste_mirage_camp_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="scorchwaste_mirage_camp_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_mirage_camp_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="scorchwaste_mirage_camp_vault_to_prev", label="Return back", category="movement", target_scene="scorchwaste_mirage_camp_sanctum", result_text="You retrace your steps."),
            Action(id="scorchwaste_mirage_camp_vault_to_hub", label="Return to Hub", category="movement", target_scene="scorchwaste_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["scorchwaste_hub"].base_actions.append(
        Action(id="scorchwaste_hub_to_mirage_camp", label="Visit Nomad Camp", category="movement", target_scene="scorchwaste_mirage_camp_gate", result_text="You travel to Nomad Tent Camp.")
    )

    # POI: Sandswept Crypt (10 nodes)
    # Encounter 5 - Stage 1: Assessment / Approach
    scenes["scorchwaste_buried_tomb_gate"] = SceneNode(
        id="scorchwaste_buried_tomb_gate",
        title="Sandswept Crypt - Sunken Lintel",
        region="scorchwaste",
        description="Searing desert wind blows red sand over carved stone steps. Intense heat ripples rise from the dunes. A half-buried bronze temple door glints.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "heat_hardened"},
                text="Your weathered skin resists the baking sun."
            ),
            DynamicDescription(
                condition={"ancestry_is": "ashenborn"},
                text="The desert sun fills your limbs with steady warmth."
            ),
        ],
        entities=[
            {"id": "scorch_tomb_sanddrift", "name": "Sand Drift", "tags": ["climbable"], "initial_state": "intact"},
            {"id": "scorch_tomb_bronze_door", "name": "Bronze Door", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="scorch_tomb_drink_water", label="Drink from canteen", category="interaction", condition={"has_item": "water_skin"}, effects=[{"modify_stamina": 3}], result_text="Cool water revives your parched throat."),
            Action(id="scorch_tomb_clear_sand", label="Clear red sand", category="interaction", stamina_cost=1, effects=[{"set_flag": {"flag": "tomb_steps_cleared", "value": True}}, {"log_event": "You shoveled heavy red sand off the doorway."}], result_text="You clear the buried stone threshold."),
            Action(id="scorch_tomb_force_door", label="Pry bronze door", category="item_affordance", condition={"has_item": "crowbar"}, target_scene="scorchwaste_buried_tomb_courtyard", result_text="The heavy bronze door screeches open over sand."),
            Action(id="scorchwaste_buried_tomb_gate_to_prev", label="Return back", category="movement", target_scene="scorchwaste_hub", result_text="You retrace your steps."),
            Action(id="scorchwaste_buried_tomb_gate_to_next", label="Press forward", category="movement", target_scene="scorchwaste_buried_tomb_courtyard", result_text="You press on to the next area."),
        ]
    )

    # Encounter 5 - Stage 2: Engagement / Climax
    scenes["scorchwaste_buried_tomb_courtyard"] = SceneNode(
        id="scorchwaste_buried_tomb_courtyard",
        title="Sandswept Crypt - Solar Mirror Hall",
        region="scorchwaste",
        description="Sunlight beams down an overhead shaft onto polished bronze mirrors. Stifling heat fills the stone chamber. A sealed stone vault blocks the way.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="You trace mirror reflection lines carved into the dust."
            ),
        ],
        entities=[
            {"id": "scorch_tomb_solar_mirror", "name": "Bronze Mirror", "tags": ["lockable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="scorch_tomb_align_mirrors", label="Align bronze mirrors", category="trait_exploit", condition={"min_skill": {"skill": "cunning", "value": 3}}, effects=[{"set_flag": {"flag": "solar_lock_solved", "value": True}}, {"log_event": "You aligned the solar mirrors and disengaged the stone lock."}], target_scene="scorchwaste_buried_tomb_quarters", result_text="The focused beam of sunlight trips the counterweight."),
            Action(id="scorch_tomb_endure_heat", label="Endure baking heat", category="systemic", condition={"min_attribute": {"attribute": "endurance", "value": 13}}, target_scene="scorchwaste_buried_tomb_quarters", result_text="You push through the sweltering chamber without slowing down."),
            Action(id="scorchwaste_buried_tomb_courtyard_to_prev", label="Return back", category="movement", target_scene="scorchwaste_buried_tomb_gate", result_text="You retrace your steps."),
            Action(id="scorchwaste_buried_tomb_courtyard_to_next", label="Press forward", category="movement", target_scene="scorchwaste_buried_tomb_quarters", result_text="You press on to the next area."),
        ]
    )

    # Encounter 5 - Stage 3: Resolution / Consequences
    scenes["scorchwaste_buried_tomb_quarters"] = SceneNode(
        id="scorchwaste_buried_tomb_quarters",
        title="Sandswept Crypt - Spring Vault",
        region="scorchwaste",
        description="Cool underground air chills your sweat. A pristine pool of desert water bubbles within a stone font. An ornate solar amulet rests on a carved dais.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"flag_is": {"flag": "solar_amulet_taken", "value": True}},
                text="The stone dais stands empty beside the bubbling spring."
            ),
        ],
        entities=[
            {"id": "scorch_tomb_spring_font", "name": "Stone Font", "tags": ["flammable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="scorch_tomb_take_amulet", label="Take solar amulet", category="interaction", condition={"lacks_flag": "solar_amulet_taken"}, effects=[{"add_item": "solar_amulet"}, {"set_flag": {"flag": "solar_amulet_taken", "value": True}}, {"modify_health": 5}, {"log_event": "You retrieved the ancient solar amulet."}], result_text="The gold amulet gleams in your hand."),
            Action(id="scorch_tomb_refill_skins", label="Fill water skins", category="interaction", effects=[{"modify_stamina": 5}, {"log_event": "You replenished your fresh water supply."}], result_text="You drink deeply from the cool underground spring."),
            Action(id="scorchwaste_buried_tomb_quarters_to_prev", label="Return back", category="movement", target_scene="scorchwaste_buried_tomb_courtyard", result_text="You retrace your steps."),
            Action(id="scorchwaste_buried_tomb_quarters_to_next", label="Press forward", category="movement", target_scene="scorchwaste_buried_tomb_armory", result_text="You press on to the supply depot."),
        ]
    )

    scenes["scorchwaste_buried_tomb_armory"] = SceneNode(
        id="scorchwaste_buried_tomb_armory",
        title="Sandswept Crypt - Supply Depot",
        region="scorchwaste",
        description="Crates of rations and tools stand stacked. Wind blows red sand across carved obsidian doors.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_buried_tomb_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_buried_tomb_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="scorchwaste_buried_tomb_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="scorchwaste_buried_tomb_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_buried_tomb_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="scorchwaste_buried_tomb_armory_to_prev", label="Return back", category="movement", target_scene="scorchwaste_buried_tomb_quarters", result_text="You retrace your steps."),
            Action(id="scorchwaste_buried_tomb_armory_to_next", label="Press forward", category="movement", target_scene="scorchwaste_buried_tomb_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_buried_tomb_cellar"] = SceneNode(
        id="scorchwaste_buried_tomb_cellar",
        title="Sandswept Crypt - Lower Cellar",
        region="scorchwaste",
        description="Damp air smells of cool earth and storage. Wind blows red sand across carved obsidian doors.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_buried_tomb_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="scorchwaste_buried_tomb_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="scorchwaste_buried_tomb_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_buried_tomb_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="scorchwaste_buried_tomb_cellar_to_prev", label="Return back", category="movement", target_scene="scorchwaste_buried_tomb_armory", result_text="You retrace your steps."),
            Action(id="scorchwaste_buried_tomb_cellar_to_next", label="Press forward", category="movement", target_scene="scorchwaste_buried_tomb_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_buried_tomb_passage"] = SceneNode(
        id="scorchwaste_buried_tomb_passage",
        title="Sandswept Crypt - Stone Corridor",
        region="scorchwaste",
        description="Wall sconces hold flickering tallow candles. Wind blows red sand across carved obsidian doors.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_buried_tomb_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_buried_tomb_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="scorchwaste_buried_tomb_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="scorchwaste_buried_tomb_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_buried_tomb_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="scorchwaste_buried_tomb_passage_to_prev", label="Return back", category="movement", target_scene="scorchwaste_buried_tomb_cellar", result_text="You retrace your steps."),
            Action(id="scorchwaste_buried_tomb_passage_to_next", label="Press forward", category="movement", target_scene="scorchwaste_buried_tomb_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_buried_tomb_chamber"] = SceneNode(
        id="scorchwaste_buried_tomb_chamber",
        title="Sandswept Crypt - Inner Chamber",
        region="scorchwaste",
        description="A sturdy oak desk holds ledgers and maps. Wind blows red sand across carved obsidian doors.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_buried_tomb_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="scorchwaste_buried_tomb_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="scorchwaste_buried_tomb_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_buried_tomb_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="scorchwaste_buried_tomb_chamber_to_prev", label="Return back", category="movement", target_scene="scorchwaste_buried_tomb_passage", result_text="You retrace your steps."),
            Action(id="scorchwaste_buried_tomb_chamber_to_next", label="Press forward", category="movement", target_scene="scorchwaste_buried_tomb_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_buried_tomb_overlook"] = SceneNode(
        id="scorchwaste_buried_tomb_overlook",
        title="Sandswept Crypt - High Overlook",
        region="scorchwaste",
        description="A stone ledge provides a clear view. Wind blows red sand across carved obsidian doors.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_buried_tomb_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="scorchwaste_buried_tomb_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="scorchwaste_buried_tomb_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_buried_tomb_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="scorchwaste_buried_tomb_overlook_to_prev", label="Return back", category="movement", target_scene="scorchwaste_buried_tomb_chamber", result_text="You retrace your steps."),
            Action(id="scorchwaste_buried_tomb_overlook_to_next", label="Press forward", category="movement", target_scene="scorchwaste_buried_tomb_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_buried_tomb_sanctum"] = SceneNode(
        id="scorchwaste_buried_tomb_sanctum",
        title="Sandswept Crypt - Inner Sanctum",
        region="scorchwaste",
        description="A stone altar stands in quiet reverence. Wind blows red sand across carved obsidian doors.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_buried_tomb_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="scorchwaste_buried_tomb_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="scorchwaste_buried_tomb_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_buried_tomb_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="scorchwaste_buried_tomb_sanctum_to_prev", label="Return back", category="movement", target_scene="scorchwaste_buried_tomb_overlook", result_text="You retrace your steps."),
            Action(id="scorchwaste_buried_tomb_sanctum_to_next", label="Press forward", category="movement", target_scene="scorchwaste_buried_tomb_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_buried_tomb_vault"] = SceneNode(
        id="scorchwaste_buried_tomb_vault",
        title="Sandswept Crypt - Deep Vault",
        region="scorchwaste",
        description="Iron-banded chests sit in deep shadows. Wind blows red sand across carved obsidian doors.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_buried_tomb_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_buried_tomb_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="scorchwaste_buried_tomb_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="scorchwaste_buried_tomb_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_buried_tomb_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="scorchwaste_buried_tomb_vault_to_prev", label="Return back", category="movement", target_scene="scorchwaste_buried_tomb_sanctum", result_text="You retrace your steps."),
            Action(id="scorchwaste_buried_tomb_vault_to_hub", label="Return to Hub", category="movement", target_scene="scorchwaste_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["scorchwaste_hub"].base_actions.append(
        Action(id="scorchwaste_hub_to_buried_tomb", label="Visit Sandswept Cr", category="movement", target_scene="scorchwaste_buried_tomb_gate", result_text="You travel to Sandswept Crypt.")
    )

    # POI: Obsidian Basin (10 nodes)
    scenes["scorchwaste_crater_mine_gate"] = SceneNode(
        id="scorchwaste_crater_mine_gate",
        title="Obsidian Basin - Outer Gate",
        region="scorchwaste",
        description="Iron bars secure the heavy timber entrance. Volcanic glass sparkles under the desert sun.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_crater_mine_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_crater_mine_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="scorchwaste_crater_mine_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="scorchwaste_crater_mine_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_crater_mine_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="scorchwaste_crater_mine_gate_to_prev", label="Return back", category="movement", target_scene="scorchwaste_hub", result_text="You retrace your steps."),
            Action(id="scorchwaste_crater_mine_gate_to_next", label="Press forward", category="movement", target_scene="scorchwaste_crater_mine_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_crater_mine_courtyard"] = SceneNode(
        id="scorchwaste_crater_mine_courtyard",
        title="Obsidian Basin - Main Courtyard",
        region="scorchwaste",
        description="Cobblestones show heavy cart wheel wear. Volcanic glass sparkles under the desert sun.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_crater_mine_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_crater_mine_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="scorchwaste_crater_mine_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="scorchwaste_crater_mine_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_crater_mine_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="scorchwaste_crater_mine_courtyard_to_prev", label="Return back", category="movement", target_scene="scorchwaste_crater_mine_gate", result_text="You retrace your steps."),
            Action(id="scorchwaste_crater_mine_courtyard_to_next", label="Press forward", category="movement", target_scene="scorchwaste_crater_mine_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_crater_mine_quarters"] = SceneNode(
        id="scorchwaste_crater_mine_quarters",
        title="Obsidian Basin - Living Quarters",
        region="scorchwaste",
        description="Rows of wooden bunks line the walls. Volcanic glass sparkles under the desert sun.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_crater_mine_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="scorchwaste_crater_mine_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="scorchwaste_crater_mine_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_crater_mine_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="scorchwaste_crater_mine_quarters_to_prev", label="Return back", category="movement", target_scene="scorchwaste_crater_mine_courtyard", result_text="You retrace your steps."),
            Action(id="scorchwaste_crater_mine_quarters_to_next", label="Press forward", category="movement", target_scene="scorchwaste_crater_mine_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_crater_mine_armory"] = SceneNode(
        id="scorchwaste_crater_mine_armory",
        title="Obsidian Basin - Supply Depot",
        region="scorchwaste",
        description="Crates of rations and tools stand stacked. Volcanic glass sparkles under the desert sun.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_crater_mine_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_crater_mine_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="scorchwaste_crater_mine_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="scorchwaste_crater_mine_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_crater_mine_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="scorchwaste_crater_mine_armory_to_prev", label="Return back", category="movement", target_scene="scorchwaste_crater_mine_quarters", result_text="You retrace your steps."),
            Action(id="scorchwaste_crater_mine_armory_to_next", label="Press forward", category="movement", target_scene="scorchwaste_crater_mine_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_crater_mine_cellar"] = SceneNode(
        id="scorchwaste_crater_mine_cellar",
        title="Obsidian Basin - Lower Cellar",
        region="scorchwaste",
        description="Damp air smells of cool earth and storage. Volcanic glass sparkles under the desert sun.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_crater_mine_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="scorchwaste_crater_mine_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="scorchwaste_crater_mine_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_crater_mine_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="scorchwaste_crater_mine_cellar_to_prev", label="Return back", category="movement", target_scene="scorchwaste_crater_mine_armory", result_text="You retrace your steps."),
            Action(id="scorchwaste_crater_mine_cellar_to_next", label="Press forward", category="movement", target_scene="scorchwaste_crater_mine_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_crater_mine_passage"] = SceneNode(
        id="scorchwaste_crater_mine_passage",
        title="Obsidian Basin - Stone Corridor",
        region="scorchwaste",
        description="Wall sconces hold flickering tallow candles. Volcanic glass sparkles under the desert sun.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_crater_mine_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_crater_mine_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="scorchwaste_crater_mine_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="scorchwaste_crater_mine_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_crater_mine_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="scorchwaste_crater_mine_passage_to_prev", label="Return back", category="movement", target_scene="scorchwaste_crater_mine_cellar", result_text="You retrace your steps."),
            Action(id="scorchwaste_crater_mine_passage_to_next", label="Press forward", category="movement", target_scene="scorchwaste_crater_mine_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_crater_mine_chamber"] = SceneNode(
        id="scorchwaste_crater_mine_chamber",
        title="Obsidian Basin - Inner Chamber",
        region="scorchwaste",
        description="A sturdy oak desk holds ledgers and maps. Volcanic glass sparkles under the desert sun.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_crater_mine_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="scorchwaste_crater_mine_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="scorchwaste_crater_mine_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_crater_mine_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="scorchwaste_crater_mine_chamber_to_prev", label="Return back", category="movement", target_scene="scorchwaste_crater_mine_passage", result_text="You retrace your steps."),
            Action(id="scorchwaste_crater_mine_chamber_to_next", label="Press forward", category="movement", target_scene="scorchwaste_crater_mine_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_crater_mine_overlook"] = SceneNode(
        id="scorchwaste_crater_mine_overlook",
        title="Obsidian Basin - High Overlook",
        region="scorchwaste",
        description="A stone ledge provides a clear view. Volcanic glass sparkles under the desert sun.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_crater_mine_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="scorchwaste_crater_mine_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="scorchwaste_crater_mine_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_crater_mine_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="scorchwaste_crater_mine_overlook_to_prev", label="Return back", category="movement", target_scene="scorchwaste_crater_mine_chamber", result_text="You retrace your steps."),
            Action(id="scorchwaste_crater_mine_overlook_to_next", label="Press forward", category="movement", target_scene="scorchwaste_crater_mine_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_crater_mine_sanctum"] = SceneNode(
        id="scorchwaste_crater_mine_sanctum",
        title="Obsidian Basin - Inner Sanctum",
        region="scorchwaste",
        description="A stone altar stands in quiet reverence. Volcanic glass sparkles under the desert sun.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_crater_mine_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="scorchwaste_crater_mine_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="scorchwaste_crater_mine_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_crater_mine_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="scorchwaste_crater_mine_sanctum_to_prev", label="Return back", category="movement", target_scene="scorchwaste_crater_mine_overlook", result_text="You retrace your steps."),
            Action(id="scorchwaste_crater_mine_sanctum_to_next", label="Press forward", category="movement", target_scene="scorchwaste_crater_mine_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_crater_mine_vault"] = SceneNode(
        id="scorchwaste_crater_mine_vault",
        title="Obsidian Basin - Deep Vault",
        region="scorchwaste",
        description="Iron-banded chests sit in deep shadows. Volcanic glass sparkles under the desert sun.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_crater_mine_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_crater_mine_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="scorchwaste_crater_mine_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="scorchwaste_crater_mine_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_crater_mine_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="scorchwaste_crater_mine_vault_to_prev", label="Return back", category="movement", target_scene="scorchwaste_crater_mine_sanctum", result_text="You retrace your steps."),
            Action(id="scorchwaste_crater_mine_vault_to_hub", label="Return to Hub", category="movement", target_scene="scorchwaste_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["scorchwaste_hub"].base_actions.append(
        Action(id="scorchwaste_hub_to_crater_mine", label="Visit Obsidian Bas", category="movement", target_scene="scorchwaste_crater_mine_gate", result_text="You travel to Obsidian Basin.")
    )

    # POI: White Salt Flats (10 nodes)
    # Encounter 6 - Stage 1: Assessment / Approach
    scenes["scorchwaste_salt_pan_gate"] = SceneNode(
        id="scorchwaste_salt_pan_gate",
        title="White Salt Flats - Shimmering Verge",
        region="scorchwaste",
        description="A blinding white plain of salt crust stretches toward the horizon. Searing heat creates trembling mirages. A stranded pack caravan calls for assistance.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "skeptical"},
                text="You pierce through the mirage to pinpoint the true caravan."
            ),
        ],
        entities=[
            {"id": "scorch_salt_pillar", "name": "Salt Pillar", "tags": ["climbable"], "climb_destination": "scorchwaste_salt_pan_courtyard"},
            {"id": "scorch_salt_dried_brush", "name": "Dried Brush", "tags": ["flammable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="scorch_salt_scan_flats", label="Scan the flats", category="interaction", result_text="You shield your eyes and study the salt formations."),
            Action(id="scorch_salt_tread_carefully", label="Tread fragile salt", category="trait_exploit", condition={"has_trait": "nimble"}, target_scene="scorchwaste_salt_pan_courtyard", result_text="You step lightly across brittle crust without cracking it."),
            Action(id="scorchwaste_salt_pan_gate_to_prev", label="Return back", category="movement", target_scene="scorchwaste_hub", result_text="You retrace your steps."),
            Action(id="scorchwaste_salt_pan_gate_to_next", label="Press forward", category="movement", target_scene="scorchwaste_salt_pan_courtyard", result_text="You press on to the next area."),
        ]
    )

    # Encounter 6 - Stage 2: Engagement / Climax
    scenes["scorchwaste_salt_pan_courtyard"] = SceneNode(
        id="scorchwaste_salt_pan_courtyard",
        title="White Salt Flats - Caustic Brine Pit",
        region="scorchwaste",
        description="A fractured salt crust exposes a deep pit of caustic grey brine. A trapped desert merchant clings to a sinking pack saddle.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_attribute": {"attribute": "strength", "value": 14}},
                text="Your powerful build can hoist the merchant out alone."
            ),
        ],
        entities=[
            {"id": "scorch_salt_brine_pit_anchor", "name": "Salt Ridge", "tags": ["lockable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="scorch_salt_throw_rope", label="Throw climbing rope", category="item_affordance", condition={"has_item": "climbing_rope"}, effects=[{"set_flag": {"flag": "merchant_rescued", "value": True}}, {"log_event": "You pulled the merchant from the caustic brine."}], target_scene="scorchwaste_salt_pan_quarters", result_text="The merchant grips the rope and scrambles to solid ground."),
            Action(id="scorch_salt_haul_merchant", label="Haul by hand", category="systemic", condition={"min_attribute": {"attribute": "strength", "value": 14}}, stamina_cost=2, effects=[{"set_flag": {"flag": "merchant_rescued", "value": True}}, {"log_event": "You dragged the heavy merchant from the brine."}], target_scene="scorchwaste_salt_pan_quarters", result_text="You haul the shouting merchant onto the firm salt ledge."),
            Action(id="scorchwaste_salt_pan_courtyard_to_prev", label="Return back", category="movement", target_scene="scorchwaste_salt_pan_gate", result_text="You retrace your steps."),
            Action(id="scorchwaste_salt_pan_courtyard_to_next", label="Press forward", category="movement", target_scene="scorchwaste_salt_pan_quarters", result_text="You press on to the next area."),
        ]
    )

    # Encounter 6 - Stage 3: Resolution / Consequences
    scenes["scorchwaste_salt_pan_quarters"] = SceneNode(
        id="scorchwaste_salt_pan_quarters",
        title="White Salt Flats - Solid Camp",
        region="scorchwaste",
        description="A dry sandstone hummock rises above the salt plain. The rescued merchant washes bitter brine from his face. Pack crates sit safe upon the stone.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"flag_is": {"flag": "merchant_rescued", "value": True}},
                text="The grateful merchant opens a cedar crate of trade crystals."
            ),
        ],
        entities=[
            {"id": "scorch_salt_merchant_crate", "name": "Trade Crate", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="scorch_salt_reward", label="Accept salt crystals", category="social", condition={"flag_is": {"flag": "merchant_rescued", "value": True}, "lacks_flag": "salt_reward_taken"}, effects=[{"add_item": "refined_salt_crystals"}, {"set_flag": {"flag": "salt_reward_taken", "value": True}}, {"modify_reputation": {"faction": "caravaneers", "value": 20}}, {"log_event": "You received refined salt crystals from the merchant."}], result_text="The merchant gifts you rare crystalline salt."),
            Action(id="scorch_salt_rest_camp", label="Rest under awning", category="interaction", effects=[{"modify_stamina": 3}], result_text="You rest beneath the canvas awning."),
            Action(id="scorchwaste_salt_pan_quarters_to_prev", label="Return back", category="movement", target_scene="scorchwaste_salt_pan_courtyard", result_text="You retrace your steps."),
            Action(id="scorchwaste_salt_pan_quarters_to_next", label="Press forward", category="movement", target_scene="scorchwaste_salt_pan_armory", result_text="You press on to the supply depot."),
        ]
    )

    scenes["scorchwaste_salt_pan_armory"] = SceneNode(
        id="scorchwaste_salt_pan_armory",
        title="White Salt Flats - Supply Depot",
        region="scorchwaste",
        description="Crates of rations and tools stand stacked. Blinding white crust stretches to the horizon.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_salt_pan_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_salt_pan_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="scorchwaste_salt_pan_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="scorchwaste_salt_pan_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_salt_pan_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="scorchwaste_salt_pan_armory_to_prev", label="Return back", category="movement", target_scene="scorchwaste_salt_pan_quarters", result_text="You retrace your steps."),
            Action(id="scorchwaste_salt_pan_armory_to_next", label="Press forward", category="movement", target_scene="scorchwaste_salt_pan_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_salt_pan_cellar"] = SceneNode(
        id="scorchwaste_salt_pan_cellar",
        title="White Salt Flats - Lower Cellar",
        region="scorchwaste",
        description="Damp air smells of cool earth and storage. Blinding white crust stretches to the horizon.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_salt_pan_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="scorchwaste_salt_pan_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="scorchwaste_salt_pan_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_salt_pan_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="scorchwaste_salt_pan_cellar_to_prev", label="Return back", category="movement", target_scene="scorchwaste_salt_pan_armory", result_text="You retrace your steps."),
            Action(id="scorchwaste_salt_pan_cellar_to_next", label="Press forward", category="movement", target_scene="scorchwaste_salt_pan_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_salt_pan_passage"] = SceneNode(
        id="scorchwaste_salt_pan_passage",
        title="White Salt Flats - Stone Corridor",
        region="scorchwaste",
        description="Wall sconces hold flickering tallow candles. Blinding white crust stretches to the horizon.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_salt_pan_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_salt_pan_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="scorchwaste_salt_pan_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="scorchwaste_salt_pan_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_salt_pan_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="scorchwaste_salt_pan_passage_to_prev", label="Return back", category="movement", target_scene="scorchwaste_salt_pan_cellar", result_text="You retrace your steps."),
            Action(id="scorchwaste_salt_pan_passage_to_next", label="Press forward", category="movement", target_scene="scorchwaste_salt_pan_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_salt_pan_chamber"] = SceneNode(
        id="scorchwaste_salt_pan_chamber",
        title="White Salt Flats - Inner Chamber",
        region="scorchwaste",
        description="A sturdy oak desk holds ledgers and maps. Blinding white crust stretches to the horizon.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_salt_pan_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="scorchwaste_salt_pan_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="scorchwaste_salt_pan_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_salt_pan_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="scorchwaste_salt_pan_chamber_to_prev", label="Return back", category="movement", target_scene="scorchwaste_salt_pan_passage", result_text="You retrace your steps."),
            Action(id="scorchwaste_salt_pan_chamber_to_next", label="Press forward", category="movement", target_scene="scorchwaste_salt_pan_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_salt_pan_overlook"] = SceneNode(
        id="scorchwaste_salt_pan_overlook",
        title="White Salt Flats - High Overlook",
        region="scorchwaste",
        description="A stone ledge provides a clear view. Blinding white crust stretches to the horizon.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_salt_pan_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="scorchwaste_salt_pan_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="scorchwaste_salt_pan_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_salt_pan_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="scorchwaste_salt_pan_overlook_to_prev", label="Return back", category="movement", target_scene="scorchwaste_salt_pan_chamber", result_text="You retrace your steps."),
            Action(id="scorchwaste_salt_pan_overlook_to_next", label="Press forward", category="movement", target_scene="scorchwaste_salt_pan_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_salt_pan_sanctum"] = SceneNode(
        id="scorchwaste_salt_pan_sanctum",
        title="White Salt Flats - Inner Sanctum",
        region="scorchwaste",
        description="A stone altar stands in quiet reverence. Blinding white crust stretches to the horizon.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_salt_pan_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="scorchwaste_salt_pan_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="scorchwaste_salt_pan_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_salt_pan_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="scorchwaste_salt_pan_sanctum_to_prev", label="Return back", category="movement", target_scene="scorchwaste_salt_pan_overlook", result_text="You retrace your steps."),
            Action(id="scorchwaste_salt_pan_sanctum_to_next", label="Press forward", category="movement", target_scene="scorchwaste_salt_pan_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_salt_pan_vault"] = SceneNode(
        id="scorchwaste_salt_pan_vault",
        title="White Salt Flats - Deep Vault",
        region="scorchwaste",
        description="Iron-banded chests sit in deep shadows. Blinding white crust stretches to the horizon.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_salt_pan_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_salt_pan_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="scorchwaste_salt_pan_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="scorchwaste_salt_pan_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_salt_pan_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="scorch_inspect_aqueduct", label="Inspect water pipe", category="interaction", condition={"lacks_flag": "scorch_aqueduct_inspected"}, effects=[{"set_flag": {"flag": "scorch_aqueduct_inspected", "value": True}}, {"log_event": "You mapped the baron siphon aqueducts."}], result_text="You trace the rusted iron pipes feeding the private tanks."),
            Action(id="scorchwaste_salt_pan_vault_to_prev", label="Return back", category="movement", target_scene="scorchwaste_salt_pan_sanctum", result_text="You retrace your steps."),
            Action(id="scorchwaste_salt_pan_vault_to_hub", label="Return to Hub", category="movement", target_scene="scorchwaste_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["scorchwaste_hub"].base_actions.append(
        Action(id="scorchwaste_hub_to_salt_pan", label="Visit Salt Flats", category="movement", target_scene="scorchwaste_salt_pan_gate", result_text="You travel to White Salt Flats.")
    )

    # POI: Solar Altar (10 nodes)
    scenes["scorchwaste_sun_shrine_gate"] = SceneNode(
        id="scorchwaste_sun_shrine_gate",
        title="Solar Altar - Outer Gate",
        region="scorchwaste",
        description="Iron bars secure the heavy timber entrance. A golden disk reflects blinding desert light.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_sun_shrine_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_sun_shrine_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="scorchwaste_sun_shrine_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="scorchwaste_sun_shrine_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_sun_shrine_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="scorchwaste_sun_shrine_gate_to_prev", label="Return back", category="movement", target_scene="scorchwaste_hub", result_text="You retrace your steps."),
            Action(id="scorchwaste_sun_shrine_gate_to_next", label="Press forward", category="movement", target_scene="scorchwaste_sun_shrine_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_sun_shrine_courtyard"] = SceneNode(
        id="scorchwaste_sun_shrine_courtyard",
        title="Solar Altar - Main Courtyard",
        region="scorchwaste",
        description="Cobblestones show heavy cart wheel wear. A golden disk reflects blinding desert light.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_sun_shrine_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_sun_shrine_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="scorchwaste_sun_shrine_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="scorchwaste_sun_shrine_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_sun_shrine_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="scorchwaste_sun_shrine_courtyard_to_prev", label="Return back", category="movement", target_scene="scorchwaste_sun_shrine_gate", result_text="You retrace your steps."),
            Action(id="scorchwaste_sun_shrine_courtyard_to_next", label="Press forward", category="movement", target_scene="scorchwaste_sun_shrine_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_sun_shrine_quarters"] = SceneNode(
        id="scorchwaste_sun_shrine_quarters",
        title="Solar Altar - Living Quarters",
        region="scorchwaste",
        description="Rows of wooden bunks line the walls. A golden disk reflects blinding desert light.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_sun_shrine_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="scorchwaste_sun_shrine_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="scorchwaste_sun_shrine_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_sun_shrine_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="scorchwaste_sun_shrine_quarters_to_prev", label="Return back", category="movement", target_scene="scorchwaste_sun_shrine_courtyard", result_text="You retrace your steps."),
            Action(id="scorchwaste_sun_shrine_quarters_to_next", label="Press forward", category="movement", target_scene="scorchwaste_sun_shrine_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_sun_shrine_armory"] = SceneNode(
        id="scorchwaste_sun_shrine_armory",
        title="Solar Altar - Supply Depot",
        region="scorchwaste",
        description="Crates of rations and tools stand stacked. A golden disk reflects blinding desert light.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_sun_shrine_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_sun_shrine_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="scorchwaste_sun_shrine_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="scorchwaste_sun_shrine_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_sun_shrine_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="scorchwaste_sun_shrine_armory_to_prev", label="Return back", category="movement", target_scene="scorchwaste_sun_shrine_quarters", result_text="You retrace your steps."),
            Action(id="scorchwaste_sun_shrine_armory_to_next", label="Press forward", category="movement", target_scene="scorchwaste_sun_shrine_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_sun_shrine_cellar"] = SceneNode(
        id="scorchwaste_sun_shrine_cellar",
        title="Solar Altar - Lower Cellar",
        region="scorchwaste",
        description="Damp air smells of cool earth and storage. A golden disk reflects blinding desert light.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_sun_shrine_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="scorchwaste_sun_shrine_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="scorchwaste_sun_shrine_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_sun_shrine_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="scorchwaste_sun_shrine_cellar_to_prev", label="Return back", category="movement", target_scene="scorchwaste_sun_shrine_armory", result_text="You retrace your steps."),
            Action(id="scorchwaste_sun_shrine_cellar_to_next", label="Press forward", category="movement", target_scene="scorchwaste_sun_shrine_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_sun_shrine_passage"] = SceneNode(
        id="scorchwaste_sun_shrine_passage",
        title="Solar Altar - Stone Corridor",
        region="scorchwaste",
        description="Wall sconces hold flickering tallow candles. A golden disk reflects blinding desert light.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_sun_shrine_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_sun_shrine_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="scorchwaste_sun_shrine_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="scorchwaste_sun_shrine_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_sun_shrine_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="scorchwaste_sun_shrine_passage_to_prev", label="Return back", category="movement", target_scene="scorchwaste_sun_shrine_cellar", result_text="You retrace your steps."),
            Action(id="scorchwaste_sun_shrine_passage_to_next", label="Press forward", category="movement", target_scene="scorchwaste_sun_shrine_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_sun_shrine_chamber"] = SceneNode(
        id="scorchwaste_sun_shrine_chamber",
        title="Solar Altar - Inner Chamber",
        region="scorchwaste",
        description="A sturdy oak desk holds ledgers and maps. A golden disk reflects blinding desert light.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_sun_shrine_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="scorchwaste_sun_shrine_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="scorchwaste_sun_shrine_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_sun_shrine_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="scorchwaste_sun_shrine_chamber_to_prev", label="Return back", category="movement", target_scene="scorchwaste_sun_shrine_passage", result_text="You retrace your steps."),
            Action(id="scorchwaste_sun_shrine_chamber_to_next", label="Press forward", category="movement", target_scene="scorchwaste_sun_shrine_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_sun_shrine_overlook"] = SceneNode(
        id="scorchwaste_sun_shrine_overlook",
        title="Solar Altar - High Overlook",
        region="scorchwaste",
        description="A stone ledge provides a clear view. A golden disk reflects blinding desert light.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_sun_shrine_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="scorchwaste_sun_shrine_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="scorchwaste_sun_shrine_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_sun_shrine_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="scorchwaste_sun_shrine_overlook_to_prev", label="Return back", category="movement", target_scene="scorchwaste_sun_shrine_chamber", result_text="You retrace your steps."),
            Action(id="scorchwaste_sun_shrine_overlook_to_next", label="Press forward", category="movement", target_scene="scorchwaste_sun_shrine_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_sun_shrine_sanctum"] = SceneNode(
        id="scorchwaste_sun_shrine_sanctum",
        title="Solar Altar - Inner Sanctum",
        region="scorchwaste",
        description="A stone altar stands in quiet reverence. A golden disk reflects blinding desert light.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_sun_shrine_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="scorchwaste_sun_shrine_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="scorchwaste_sun_shrine_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_sun_shrine_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="scorchwaste_sun_shrine_sanctum_to_prev", label="Return back", category="movement", target_scene="scorchwaste_sun_shrine_overlook", result_text="You retrace your steps."),
            Action(id="scorchwaste_sun_shrine_sanctum_to_next", label="Press forward", category="movement", target_scene="scorchwaste_sun_shrine_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_sun_shrine_vault"] = SceneNode(
        id="scorchwaste_sun_shrine_vault",
        title="Solar Altar - Deep Vault",
        region="scorchwaste",
        description="Iron-banded chests sit in deep shadows. A golden disk reflects blinding desert light.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_sun_shrine_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_sun_shrine_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="scorchwaste_sun_shrine_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="scorchwaste_sun_shrine_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_sun_shrine_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="scorchwaste_sun_shrine_vault_to_prev", label="Return back", category="movement", target_scene="scorchwaste_sun_shrine_sanctum", result_text="You retrace your steps."),
            Action(id="scorchwaste_sun_shrine_vault_to_hub", label="Return to Hub", category="movement", target_scene="scorchwaste_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["scorchwaste_hub"].base_actions.append(
        Action(id="scorchwaste_hub_to_sun_shrine", label="Visit Solar Altar", category="movement", target_scene="scorchwaste_sun_shrine_gate", result_text="You travel to Solar Altar.")
    )

    # POI: Hidden Spring Oasis (10 nodes)
    # Encounter 15 - Stage 1: Assessment / Approach
    scenes["scorchwaste_canyon_oasis_gate"] = SceneNode(
        id="scorchwaste_canyon_oasis_gate",
        title="Hidden Spring Oasis - Canyon Mouth",
        region="scorchwaste",
        description="Sunlight scorches the red sandstone canyon. Palm fronds cast cool shadows over a green spring basin. Two desert sentries eye each other across the pool.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "heat_hardened"},
                text="Your heat hardened skin shrugs off the blistering midday glare."
            ),
        ],
        entities=[
            {"id": "scorch_oasis_spring_basin", "name": "Spring Basin", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="scorch_oasis_scout_spring", label="Inspect canyon oasis", category="interaction", result_text="You scan the green oasis water and watch the tense guards."),
            Action(id="scorch_oasis_rest_shade", label="Rest in shade", category="interaction", effects=[{"modify_stamina": 4}], result_text="You rest beneath the cool date palms and shake off the heat."),
            Action(id="scorch_oasis_drink_canteen", label="Drink from canteen", category="item_affordance", condition={"has_item": "water_skin"}, effects=[{"modify_stamina": 2}, {"modify_health": 2}], result_text="You take a deep drink from your waterskin, feeling refreshed."),
            Action(id="scorch_trade_lowlands_contraband", label="Trade Contraband", category="social", condition={"has_marker": "syndicate_contact"}, effects=[{"add_item": "nomad_water_flask"}, {"set_flag": {"flag": "scorch_contraband_traded", "value": True}}, {"modify_reputation": {"faction": "shadow_syndicate", "value": 15}}, {"log_event": "You traded Lowlands contraband for rare desert supplies."}], result_text="A hooded runner accepts your stolen seal and hands over fresh supplies."),
            Action(id="scorchwaste_canyon_oasis_gate_to_prev", label="Return back", category="movement", target_scene="scorchwaste_hub", result_text="You retrace your steps."),
            Action(id="scorchwaste_canyon_oasis_gate_to_next", label="Press forward", category="movement", target_scene="scorchwaste_canyon_oasis_courtyard", result_text="You press on to the next area."),
        ]
    )

    # Encounter 15 - Stage 2: Engagement / Climax
    scenes["scorchwaste_canyon_oasis_courtyard"] = SceneNode(
        id="scorchwaste_canyon_oasis_courtyard",
        title="Hidden Spring Oasis - Contested Pool",
        region="scorchwaste",
        description="Red algae clouds the shallow stone pool. Armed nomad elders argue over contested water rights. A fallen palm trunk blocks the upper feeder sluice.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "nimble"},
                text="You step lightly across the hot gravel near the spring."
            ),
        ],
        entities=[
            {"id": "scorch_oasis_sluice", "name": "Feeder Sluice", "tags": ["flammable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="scorch_oasis_inspect_pool", label="Inspect spring basin", category="interaction", result_text="You examine the stagnant red pool and the jammed intake sluice."),
            Action(id="scorch_oasis_purify_spring", label="Purify spring water", category="trait_exploit", condition={"min_skill": {"skill": "cunning", "value": 3}}, effects=[{"set_flag": {"flag": "oasis_water_purified", "value": True}}, {"log_event": "You neutralized the red algae with mineral salts."}], target_scene="scorchwaste_canyon_oasis_quarters", result_text="You dissolve mineral salts into the pool, clearing the toxic algae."),
            Action(id="scorch_oasis_parley_clans", label="Parley with elders", category="social", condition={"min_skill": {"skill": "rhetoric", "value": 4}}, effects=[{"set_flag": {"flag": "oasis_clans_allied", "value": True}}, {"log_event": "You brokered a water treaty between the clans."}], target_scene="scorchwaste_canyon_oasis_quarters", result_text="Your reasoned words convince both sides to share the spring."),
            Action(id="scorch_oasis_drag_trunk", label="Drag palm trunk", category="systemic", condition={"min_attribute": {"attribute": "strength", "value": 15}}, effects=[{"set_flag": {"flag": "oasis_sluice_cleared", "value": True}}, {"log_event": "You dragged the fallen palm trunk from the sluice."}], target_scene="scorchwaste_canyon_oasis_quarters", result_text="You heave the heavy palm trunk free, letting fresh water rush in."),
            Action(id="scorch_war_pledge_wardens", label="Pledge To Nomads", category="social", condition={"all_of": [{"flag_is": {"flag": "scorch_pipeline_surveyed", "value": True}}, {"lacks_flag": "scorch_faction_chosen"}]}, effects=[{"set_flag": {"flag": "scorch_faction_chosen", "value": True}}, {"set_flag": {"flag": "scorch_allied_nomads", "value": True}}, {"modify_reputation": {"faction": "desert_nomads", "value": 15}}, {"modify_reputation": {"faction": "salt_raiders", "value": -10}}, {"log_event": "You allied with the Dune Nomads to defend the wells."}], result_text="The nomad elder presses a carved wooden water token into your hand."),
            Action(id="scorch_war_parley_cartel", label="Accept Cartel Contract", category="social", condition={"all_of": [{"flag_is": {"flag": "scorch_pipeline_surveyed", "value": True}}, {"lacks_flag": "scorch_faction_chosen"}]}, effects=[{"set_flag": {"flag": "scorch_faction_chosen", "value": True}}, {"set_flag": {"flag": "scorch_allied_cartel", "value": True}}, {"modify_reputation": {"faction": "salt_raiders", "value": 15}}, {"modify_reputation": {"faction": "desert_nomads", "value": -10}}, {"log_event": "You took a paid mercenary contract from the Salt Cartel."}], result_text="The cartel factor hands you a heavy pouch of silver coins."),
            Action(id="scorch_war_extort_both", label="Play Both Sides", category="trait_exploit", condition={"all_of": [{"flag_is": {"flag": "scorch_pipeline_surveyed", "value": True}}, {"lacks_flag": "scorch_faction_chosen"}, {"min_skill": {"skill": "cunning", "value": 3}}]}, effects=[{"set_flag": {"flag": "scorch_faction_chosen", "value": True}}, {"set_flag": {"flag": "scorch_played_both", "value": True}}, {"modify_reputation": {"faction": "caravaneers", "value": 15}}, {"log_event": "You played both desert factions against each other for profit."}], result_text="You pocket guarantees from both factions while concealing your true loyalties."),
            Action(id="scorchwaste_canyon_oasis_courtyard_to_prev", label="Return back", category="movement", target_scene="scorchwaste_canyon_oasis_gate", result_text="You retrace your steps."),
            Action(id="scorchwaste_canyon_oasis_courtyard_to_next", label="Press forward", category="movement", target_scene="scorchwaste_canyon_oasis_quarters", result_text="You press on to the next area."),
        ]
    )

    # Encounter 15 - Stage 3: Resolution / Consequences
    scenes["scorchwaste_canyon_oasis_quarters"] = SceneNode(
        id="scorchwaste_canyon_oasis_quarters",
        title="Hidden Spring Oasis - Elders Shelter",
        region="scorchwaste",
        description="Cool spring water trickles into a clean rock basin. Palm woven mats offer rest from the desert heat. Clay water jugs stand along the sandstone wall.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"flag_is": {"flag": "oasis_water_purified", "value": True}},
                text="Nomad elders nod in gratitude as clean water fills the pool."
            ),
            DynamicDescription(
                condition={"flag_is": {"flag": "oasis_clans_allied", "value": True}},
                text="A fragile desert peace holds after your successful parley."
            ),
        ],
        entities=[
            {"id": "scorch_oasis_jugs", "name": "Water Jugs", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="scorch_oasis_receive_offering", label="Receive elder gift", category="interaction", condition={"all_of": [{"any_of": [{"flag_is": {"flag": "oasis_water_purified", "value": True}}, {"flag_is": {"flag": "oasis_clans_allied", "value": True}}, {"flag_is": {"flag": "oasis_sluice_cleared", "value": True}}]}, {"lacks_flag": "oasis_offering_taken"}]}, effects=[{"add_item": "purified_oasis_vial"}, {"set_flag": {"flag": "oasis_offering_taken", "value": True}}, {"modify_reputation": {"faction": "caravaneers", "value": 25}}, {"add_marker": "desert_healer"}, {"log_event": "You received the purified oasis vial from the elders."}], result_text="The elders present you with a glass vial of sacred spring water."),
            Action(id="scorch_oasis_rest_cistern", label="Rest near cistern", category="interaction", effects=[{"modify_stamina": 3}], result_text="You rest on palm mats beside the cool spring water."),
            Action(id="scorchwaste_canyon_oasis_quarters_act_2", label="Inspect water jugs", category="interaction", effects=[{"set_flag": {"flag": "scorchwaste_canyon_oasis_quarters_footlocker_searched", "value": True}}, {"log_event": "You inspected the clay jugs."}], result_text="You check the sealed clay water amphorae."),
            Action(id="scorchwaste_canyon_oasis_quarters_to_prev", label="Return back", category="movement", target_scene="scorchwaste_canyon_oasis_courtyard", result_text="You retrace your steps."),
            Action(id="scorchwaste_canyon_oasis_quarters_to_next", label="Press forward", category="movement", target_scene="scorchwaste_canyon_oasis_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_canyon_oasis_armory"] = SceneNode(
        id="scorchwaste_canyon_oasis_armory",
        title="Hidden Spring Oasis - Supply Depot",
        region="scorchwaste",
        description="Crates of rations and tools stand stacked. Date palms shelter a deep pool of fresh water.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_canyon_oasis_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_canyon_oasis_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="scorchwaste_canyon_oasis_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="scorchwaste_canyon_oasis_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_canyon_oasis_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="scorchwaste_canyon_oasis_armory_to_prev", label="Return back", category="movement", target_scene="scorchwaste_canyon_oasis_quarters", result_text="You retrace your steps."),
            Action(id="scorchwaste_canyon_oasis_armory_to_next", label="Press forward", category="movement", target_scene="scorchwaste_canyon_oasis_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_canyon_oasis_cellar"] = SceneNode(
        id="scorchwaste_canyon_oasis_cellar",
        title="Hidden Spring Oasis - Lower Cellar",
        region="scorchwaste",
        description="Damp air smells of cool earth and storage. Date palms shelter a deep pool of fresh water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_canyon_oasis_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="scorchwaste_canyon_oasis_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="scorchwaste_canyon_oasis_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_canyon_oasis_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="scorchwaste_canyon_oasis_cellar_to_prev", label="Return back", category="movement", target_scene="scorchwaste_canyon_oasis_armory", result_text="You retrace your steps."),
            Action(id="scorchwaste_canyon_oasis_cellar_to_next", label="Press forward", category="movement", target_scene="scorchwaste_canyon_oasis_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_canyon_oasis_passage"] = SceneNode(
        id="scorchwaste_canyon_oasis_passage",
        title="Hidden Spring Oasis - Stone Corridor",
        region="scorchwaste",
        description="Wall sconces hold flickering tallow candles. Date palms shelter a deep pool of fresh water.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_canyon_oasis_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_canyon_oasis_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="scorchwaste_canyon_oasis_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="scorchwaste_canyon_oasis_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_canyon_oasis_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="scorchwaste_canyon_oasis_passage_to_prev", label="Return back", category="movement", target_scene="scorchwaste_canyon_oasis_cellar", result_text="You retrace your steps."),
            Action(id="scorchwaste_canyon_oasis_passage_to_next", label="Press forward", category="movement", target_scene="scorchwaste_canyon_oasis_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_canyon_oasis_chamber"] = SceneNode(
        id="scorchwaste_canyon_oasis_chamber",
        title="Hidden Spring Oasis - Inner Chamber",
        region="scorchwaste",
        description="A sturdy oak desk holds ledgers and maps. Date palms shelter a deep pool of fresh water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_canyon_oasis_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="scorchwaste_canyon_oasis_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="scorchwaste_canyon_oasis_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_canyon_oasis_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="scorchwaste_canyon_oasis_chamber_to_prev", label="Return back", category="movement", target_scene="scorchwaste_canyon_oasis_passage", result_text="You retrace your steps."),
            Action(id="scorchwaste_canyon_oasis_chamber_to_next", label="Press forward", category="movement", target_scene="scorchwaste_canyon_oasis_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_canyon_oasis_overlook"] = SceneNode(
        id="scorchwaste_canyon_oasis_overlook",
        title="Hidden Spring Oasis - High Overlook",
        region="scorchwaste",
        description="A stone ledge provides a clear view. Date palms shelter a deep pool of fresh water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_canyon_oasis_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="scorchwaste_canyon_oasis_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="scorchwaste_canyon_oasis_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_canyon_oasis_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="scorchwaste_canyon_oasis_overlook_to_prev", label="Return back", category="movement", target_scene="scorchwaste_canyon_oasis_chamber", result_text="You retrace your steps."),
            Action(id="scorchwaste_canyon_oasis_overlook_to_next", label="Press forward", category="movement", target_scene="scorchwaste_canyon_oasis_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_canyon_oasis_sanctum"] = SceneNode(
        id="scorchwaste_canyon_oasis_sanctum",
        title="Hidden Spring Oasis - Inner Sanctum",
        region="scorchwaste",
        description="A stone altar stands in quiet reverence. Date palms shelter a deep pool of fresh water.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_canyon_oasis_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="scorchwaste_canyon_oasis_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="scorchwaste_canyon_oasis_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_canyon_oasis_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="scorchwaste_canyon_oasis_sanctum_to_prev", label="Return back", category="movement", target_scene="scorchwaste_canyon_oasis_overlook", result_text="You retrace your steps."),
            Action(id="scorchwaste_canyon_oasis_sanctum_to_next", label="Press forward", category="movement", target_scene="scorchwaste_canyon_oasis_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_canyon_oasis_vault"] = SceneNode(
        id="scorchwaste_canyon_oasis_vault",
        title="Hidden Spring Oasis - Deep Vault",
        region="scorchwaste",
        description="Iron-banded chests sit in deep shadows. Date palms shelter a deep pool of fresh water.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_canyon_oasis_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_canyon_oasis_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="scorchwaste_canyon_oasis_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="scorchwaste_canyon_oasis_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_canyon_oasis_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="scorch_divert_cistern", label="Sabotage water valve", category="interaction", condition={"flag_is": {"flag": "scorch_aqueduct_inspected", "value": True}, "lacks_flag": "scorch_cistern_diverted"}, effects=[{"set_flag": {"flag": "scorch_cistern_diverted", "value": True}}, {"log_event": "You jammed open the oasis reservoir flow."}], result_text="Water surges through open pipes into public basins."),
            Action(id="scorchwaste_canyon_oasis_vault_to_prev", label="Return back", category="movement", target_scene="scorchwaste_canyon_oasis_sanctum", result_text="You retrace your steps."),
            Action(id="scorchwaste_canyon_oasis_vault_to_hub", label="Return to Hub", category="movement", target_scene="scorchwaste_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["scorchwaste_hub"].base_actions.append(
        Action(id="scorchwaste_hub_to_canyon_oasis", label="Visit Hidden Sprin", category="movement", target_scene="scorchwaste_canyon_oasis_gate", result_text="You travel to Hidden Spring Oasis.")
    )

    # POI: Sand Skiff Wreck (10 nodes)
    scenes["scorchwaste_skiff_graveyard_gate"] = SceneNode(
        id="scorchwaste_skiff_graveyard_gate",
        title="Sand Skiff Wreck - Outer Gate",
        region="scorchwaste",
        description="Iron bars secure the heavy timber entrance. Bleached wooden hulls lie half-buried in sand.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_skiff_graveyard_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_skiff_graveyard_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="scorchwaste_skiff_graveyard_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="scorchwaste_skiff_graveyard_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_skiff_graveyard_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="scorchwaste_skiff_graveyard_gate_to_prev", label="Return back", category="movement", target_scene="scorchwaste_hub", result_text="You retrace your steps."),
            Action(id="scorchwaste_skiff_graveyard_gate_to_next", label="Press forward", category="movement", target_scene="scorchwaste_skiff_graveyard_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_skiff_graveyard_courtyard"] = SceneNode(
        id="scorchwaste_skiff_graveyard_courtyard",
        title="Sand Skiff Wreck - Main Courtyard",
        region="scorchwaste",
        description="Cobblestones show heavy cart wheel wear. Bleached wooden hulls lie half-buried in sand.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_skiff_graveyard_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_skiff_graveyard_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="scorchwaste_skiff_graveyard_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="scorchwaste_skiff_graveyard_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_skiff_graveyard_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="scorchwaste_skiff_graveyard_courtyard_to_prev", label="Return back", category="movement", target_scene="scorchwaste_skiff_graveyard_gate", result_text="You retrace your steps."),
            Action(id="scorchwaste_skiff_graveyard_courtyard_to_next", label="Press forward", category="movement", target_scene="scorchwaste_skiff_graveyard_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_skiff_graveyard_quarters"] = SceneNode(
        id="scorchwaste_skiff_graveyard_quarters",
        title="Sand Skiff Wreck - Living Quarters",
        region="scorchwaste",
        description="Rows of wooden bunks line the walls. Bleached wooden hulls lie half-buried in sand.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_skiff_graveyard_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="scorchwaste_skiff_graveyard_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="scorchwaste_skiff_graveyard_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_skiff_graveyard_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="scorchwaste_skiff_graveyard_quarters_to_prev", label="Return back", category="movement", target_scene="scorchwaste_skiff_graveyard_courtyard", result_text="You retrace your steps."),
            Action(id="scorchwaste_skiff_graveyard_quarters_to_next", label="Press forward", category="movement", target_scene="scorchwaste_skiff_graveyard_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_skiff_graveyard_armory"] = SceneNode(
        id="scorchwaste_skiff_graveyard_armory",
        title="Sand Skiff Wreck - Supply Depot",
        region="scorchwaste",
        description="Crates of rations and tools stand stacked. Bleached wooden hulls lie half-buried in sand.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_skiff_graveyard_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_skiff_graveyard_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="scorchwaste_skiff_graveyard_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="scorchwaste_skiff_graveyard_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_skiff_graveyard_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="scorchwaste_skiff_graveyard_armory_to_prev", label="Return back", category="movement", target_scene="scorchwaste_skiff_graveyard_quarters", result_text="You retrace your steps."),
            Action(id="scorchwaste_skiff_graveyard_armory_to_next", label="Press forward", category="movement", target_scene="scorchwaste_skiff_graveyard_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_skiff_graveyard_cellar"] = SceneNode(
        id="scorchwaste_skiff_graveyard_cellar",
        title="Sand Skiff Wreck - Lower Cellar",
        region="scorchwaste",
        description="Damp air smells of cool earth and storage. Bleached wooden hulls lie half-buried in sand.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_skiff_graveyard_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="scorchwaste_skiff_graveyard_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="scorchwaste_skiff_graveyard_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_skiff_graveyard_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="scorchwaste_skiff_graveyard_cellar_to_prev", label="Return back", category="movement", target_scene="scorchwaste_skiff_graveyard_armory", result_text="You retrace your steps."),
            Action(id="scorchwaste_skiff_graveyard_cellar_to_next", label="Press forward", category="movement", target_scene="scorchwaste_skiff_graveyard_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_skiff_graveyard_passage"] = SceneNode(
        id="scorchwaste_skiff_graveyard_passage",
        title="Sand Skiff Wreck - Stone Corridor",
        region="scorchwaste",
        description="Wall sconces hold flickering tallow candles. Bleached wooden hulls lie half-buried in sand.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_skiff_graveyard_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_skiff_graveyard_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="scorchwaste_skiff_graveyard_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="scorchwaste_skiff_graveyard_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_skiff_graveyard_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="scorchwaste_skiff_graveyard_passage_to_prev", label="Return back", category="movement", target_scene="scorchwaste_skiff_graveyard_cellar", result_text="You retrace your steps."),
            Action(id="scorchwaste_skiff_graveyard_passage_to_next", label="Press forward", category="movement", target_scene="scorchwaste_skiff_graveyard_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_skiff_graveyard_chamber"] = SceneNode(
        id="scorchwaste_skiff_graveyard_chamber",
        title="Sand Skiff Wreck - Inner Chamber",
        region="scorchwaste",
        description="A sturdy oak desk holds ledgers and maps. Bleached wooden hulls lie half-buried in sand.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_skiff_graveyard_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="scorchwaste_skiff_graveyard_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="scorchwaste_skiff_graveyard_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_skiff_graveyard_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="scorchwaste_skiff_graveyard_chamber_to_prev", label="Return back", category="movement", target_scene="scorchwaste_skiff_graveyard_passage", result_text="You retrace your steps."),
            Action(id="scorchwaste_skiff_graveyard_chamber_to_next", label="Press forward", category="movement", target_scene="scorchwaste_skiff_graveyard_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_skiff_graveyard_overlook"] = SceneNode(
        id="scorchwaste_skiff_graveyard_overlook",
        title="Sand Skiff Wreck - High Overlook",
        region="scorchwaste",
        description="A stone ledge provides a clear view. Bleached wooden hulls lie half-buried in sand.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_skiff_graveyard_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="scorchwaste_skiff_graveyard_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="scorchwaste_skiff_graveyard_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_skiff_graveyard_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="scorchwaste_skiff_graveyard_overlook_to_prev", label="Return back", category="movement", target_scene="scorchwaste_skiff_graveyard_chamber", result_text="You retrace your steps."),
            Action(id="scorchwaste_skiff_graveyard_overlook_to_next", label="Press forward", category="movement", target_scene="scorchwaste_skiff_graveyard_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_skiff_graveyard_sanctum"] = SceneNode(
        id="scorchwaste_skiff_graveyard_sanctum",
        title="Sand Skiff Wreck - Inner Sanctum",
        region="scorchwaste",
        description="A stone altar stands in quiet reverence. Bleached wooden hulls lie half-buried in sand.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_skiff_graveyard_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="scorchwaste_skiff_graveyard_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="scorchwaste_skiff_graveyard_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_skiff_graveyard_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="scorchwaste_skiff_graveyard_sanctum_to_prev", label="Return back", category="movement", target_scene="scorchwaste_skiff_graveyard_overlook", result_text="You retrace your steps."),
            Action(id="scorchwaste_skiff_graveyard_sanctum_to_next", label="Press forward", category="movement", target_scene="scorchwaste_skiff_graveyard_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_skiff_graveyard_vault"] = SceneNode(
        id="scorchwaste_skiff_graveyard_vault",
        title="Sand Skiff Wreck - Deep Vault",
        region="scorchwaste",
        description="Iron-banded chests sit in deep shadows. Bleached wooden hulls lie half-buried in sand.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_skiff_graveyard_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_skiff_graveyard_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="scorchwaste_skiff_graveyard_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="scorchwaste_skiff_graveyard_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_skiff_graveyard_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="scorchwaste_skiff_graveyard_vault_to_prev", label="Return back", category="movement", target_scene="scorchwaste_skiff_graveyard_sanctum", result_text="You retrace your steps."),
            Action(id="scorchwaste_skiff_graveyard_vault_to_hub", label="Return to Hub", category="movement", target_scene="scorchwaste_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["scorchwaste_hub"].base_actions.append(
        Action(id="scorchwaste_hub_to_skiff_graveyard", label="Visit Sand Skiff", category="movement", target_scene="scorchwaste_skiff_graveyard_gate", result_text="You travel to Sand Skiff Wreck.")
    )

    # POI: Razor Dune Ridge (10 nodes)
    scenes["scorchwaste_dune_ridge_gate"] = SceneNode(
        id="scorchwaste_dune_ridge_gate",
        title="Razor Dune Ridge - Outer Gate",
        region="scorchwaste",
        description="Iron bars secure the heavy timber entrance. Shifting sand dunes ripple under hot desert wind.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_dune_ridge_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_dune_ridge_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="scorchwaste_dune_ridge_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="scorchwaste_dune_ridge_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_dune_ridge_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="scorch_war_survey_pipeline", label="Survey Water Pipeline", category="interaction", condition={"lacks_flag": "scorch_pipeline_surveyed"}, effects=[{"set_flag": {"flag": "scorch_pipeline_surveyed", "value": True}}, {"log_event": "You surveyed the cracked desert pipeline."}], result_text="You inspect the rusted brass pipes running under the dunes."),
            Action(id="scorch_war_track_cartel", label="Track Salt Raiders", category="trait_exploit", condition={"all_of": [{"lacks_flag": "scorch_pipeline_surveyed"}, {"any_of": [{"has_trait": "night_eyed"}, {"min_skill": {"skill": "cunning", "value": 2}}]}]}, effects=[{"set_flag": {"flag": "scorch_pipeline_surveyed", "value": True}}, {"log_event": "You tracked cartel raider tracks along the pipeline."}], result_text="You trace boot prints and skiff tracks toward the canyon."),
            Action(id="scorchwaste_dune_ridge_gate_to_prev", label="Return back", category="movement", target_scene="scorchwaste_hub", result_text="You retrace your steps."),
            Action(id="scorchwaste_dune_ridge_gate_to_next", label="Press forward", category="movement", target_scene="scorchwaste_dune_ridge_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_dune_ridge_courtyard"] = SceneNode(
        id="scorchwaste_dune_ridge_courtyard",
        title="Razor Dune Ridge - Main Courtyard",
        region="scorchwaste",
        description="Cobblestones show heavy cart wheel wear. Shifting sand dunes ripple under hot desert wind.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_dune_ridge_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_dune_ridge_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="scorchwaste_dune_ridge_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="scorchwaste_dune_ridge_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_dune_ridge_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="scorchwaste_dune_ridge_courtyard_to_prev", label="Return back", category="movement", target_scene="scorchwaste_dune_ridge_gate", result_text="You retrace your steps."),
            Action(id="scorchwaste_dune_ridge_courtyard_to_next", label="Press forward", category="movement", target_scene="scorchwaste_dune_ridge_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_dune_ridge_quarters"] = SceneNode(
        id="scorchwaste_dune_ridge_quarters",
        title="Razor Dune Ridge - Living Quarters",
        region="scorchwaste",
        description="Rows of wooden bunks line the walls. Shifting sand dunes ripple under hot desert wind.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_dune_ridge_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="scorchwaste_dune_ridge_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="scorchwaste_dune_ridge_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_dune_ridge_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
            Action(id="scorchwaste_dune_ridge_quarters_to_prev", label="Return back", category="movement", target_scene="scorchwaste_dune_ridge_courtyard", result_text="You retrace your steps."),
            Action(id="scorchwaste_dune_ridge_quarters_to_next", label="Press forward", category="movement", target_scene="scorchwaste_dune_ridge_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_dune_ridge_armory"] = SceneNode(
        id="scorchwaste_dune_ridge_armory",
        title="Razor Dune Ridge - Supply Depot",
        region="scorchwaste",
        description="Crates of rations and tools stand stacked. Shifting sand dunes ripple under hot desert wind.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_dune_ridge_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_dune_ridge_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="scorchwaste_dune_ridge_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="scorchwaste_dune_ridge_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_dune_ridge_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="scorchwaste_dune_ridge_armory_to_prev", label="Return back", category="movement", target_scene="scorchwaste_dune_ridge_quarters", result_text="You retrace your steps."),
            Action(id="scorchwaste_dune_ridge_armory_to_next", label="Press forward", category="movement", target_scene="scorchwaste_dune_ridge_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_dune_ridge_cellar"] = SceneNode(
        id="scorchwaste_dune_ridge_cellar",
        title="Razor Dune Ridge - Lower Cellar",
        region="scorchwaste",
        description="Damp air smells of cool earth and storage. Shifting sand dunes ripple under hot desert wind.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_dune_ridge_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="scorchwaste_dune_ridge_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="scorchwaste_dune_ridge_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_dune_ridge_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="scorchwaste_dune_ridge_cellar_to_prev", label="Return back", category="movement", target_scene="scorchwaste_dune_ridge_armory", result_text="You retrace your steps."),
            Action(id="scorchwaste_dune_ridge_cellar_to_next", label="Press forward", category="movement", target_scene="scorchwaste_dune_ridge_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_dune_ridge_passage"] = SceneNode(
        id="scorchwaste_dune_ridge_passage",
        title="Razor Dune Ridge - Stone Corridor",
        region="scorchwaste",
        description="Wall sconces hold flickering tallow candles. Shifting sand dunes ripple under hot desert wind.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_dune_ridge_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_dune_ridge_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="scorchwaste_dune_ridge_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="scorchwaste_dune_ridge_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_dune_ridge_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="scorchwaste_dune_ridge_passage_to_prev", label="Return back", category="movement", target_scene="scorchwaste_dune_ridge_cellar", result_text="You retrace your steps."),
            Action(id="scorchwaste_dune_ridge_passage_to_next", label="Press forward", category="movement", target_scene="scorchwaste_dune_ridge_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_dune_ridge_chamber"] = SceneNode(
        id="scorchwaste_dune_ridge_chamber",
        title="Razor Dune Ridge - Inner Chamber",
        region="scorchwaste",
        description="A sturdy oak desk holds ledgers and maps. Shifting sand dunes ripple under hot desert wind.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_dune_ridge_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="scorchwaste_dune_ridge_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="scorchwaste_dune_ridge_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_dune_ridge_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="scorchwaste_dune_ridge_chamber_to_prev", label="Return back", category="movement", target_scene="scorchwaste_dune_ridge_passage", result_text="You retrace your steps."),
            Action(id="scorchwaste_dune_ridge_chamber_to_next", label="Press forward", category="movement", target_scene="scorchwaste_dune_ridge_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_dune_ridge_overlook"] = SceneNode(
        id="scorchwaste_dune_ridge_overlook",
        title="Razor Dune Ridge - High Overlook",
        region="scorchwaste",
        description="A stone ledge provides a clear view. Shifting sand dunes ripple under hot desert wind.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_dune_ridge_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="scorchwaste_dune_ridge_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="scorchwaste_dune_ridge_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_dune_ridge_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="scorchwaste_dune_ridge_overlook_to_prev", label="Return back", category="movement", target_scene="scorchwaste_dune_ridge_chamber", result_text="You retrace your steps."),
            Action(id="scorchwaste_dune_ridge_overlook_to_next", label="Press forward", category="movement", target_scene="scorchwaste_dune_ridge_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_dune_ridge_sanctum"] = SceneNode(
        id="scorchwaste_dune_ridge_sanctum",
        title="Razor Dune Ridge - Inner Sanctum",
        region="scorchwaste",
        description="A stone altar stands in quiet reverence. Shifting sand dunes ripple under hot desert wind.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_dune_ridge_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="scorchwaste_dune_ridge_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="scorchwaste_dune_ridge_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_dune_ridge_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="scorchwaste_dune_ridge_sanctum_to_prev", label="Return back", category="movement", target_scene="scorchwaste_dune_ridge_overlook", result_text="You retrace your steps."),
            Action(id="scorchwaste_dune_ridge_sanctum_to_next", label="Press forward", category="movement", target_scene="scorchwaste_dune_ridge_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_dune_ridge_vault"] = SceneNode(
        id="scorchwaste_dune_ridge_vault",
        title="Razor Dune Ridge - Deep Vault",
        region="scorchwaste",
        description="Iron-banded chests sit in deep shadows. Shifting sand dunes ripple under hot desert wind.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_dune_ridge_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_dune_ridge_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="scorchwaste_dune_ridge_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="scorchwaste_dune_ridge_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_dune_ridge_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="scorchwaste_dune_ridge_vault_to_prev", label="Return back", category="movement", target_scene="scorchwaste_dune_ridge_sanctum", result_text="You retrace your steps."),
            Action(id="scorchwaste_dune_ridge_vault_to_hub", label="Return to Hub", category="movement", target_scene="scorchwaste_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["scorchwaste_hub"].base_actions.append(
        Action(id="scorchwaste_hub_to_dune_ridge", label="Visit Dune Ridge", category="movement", target_scene="scorchwaste_dune_ridge_gate", result_text="You travel to Razor Dune Ridge.")
    )

    # POI: Nomad Deep Well (10 nodes)
    scenes["scorchwaste_nomad_well_gate"] = SceneNode(
        id="scorchwaste_nomad_well_gate",
        title="Nomad Deep Well - Outer Wellhead",
        region="scorchwaste",
        description="Windblown dunes encircle a stone wellhead. Heavy iron chains hang slack down the dark shaft. Sand skiff ruts scar the outer dune ridge.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your sharp vision picks out fresh raider tracks in the sand."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You spot tactical high ground atop the nearby dune crest."
            ),
        ],
        entities=[
            {"id": "scorch_well_head", "name": "Stone Wellhead", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="scorch_well_scout_dunes", label="Inspect desert well", category="interaction", result_text="You scan the desert wellhead and examine the slack hoist chains."),
            Action(id="scorch_well_survey_tracks", label="Survey sand tracks", category="trait_exploit", condition={"any_of": [{"has_trait": "night_eyed"}, {"min_skill": {"skill": "cunning", "value": 2}}]}, effects=[{"set_flag": {"flag": "nomad_tracks_surveyed", "value": True}}, {"log_event": "You discovered fresh desert raider tracks."}], target_scene="scorchwaste_nomad_well_courtyard", result_text="You trace skiff runner ruts leading toward the courtyard."),
            Action(id="scorch_well_rig_harness", label="Rig descent harness", category="item_affordance", condition={"has_item": "climbing_rope"}, effects=[{"set_flag": {"flag": "well_rope_rigged", "value": True}}, {"log_event": "You rigged a rope harness to the wellhead."}], target_scene="scorchwaste_nomad_well_courtyard", result_text="You secure a climbing rope harness around the stone rim."),
            Action(id="scorch_present_guild_charter", label="Present Guild Charter", category="social", condition={"has_marker": "river_bailiff"}, effects=[{"modify_reputation": {"faction": "caravaneers", "value": 20}}, {"set_flag": {"flag": "scorch_guild_charter_presented", "value": True}}, {"log_event": "You presented Lowlands River Guild authority to desert merchants."}], result_text="The caravan master recognizes the High River seal and offers steep discounts."),
            Action(id="scorchwaste_nomad_well_gate_to_prev", label="Return back", category="movement", target_scene="scorchwaste_hub", result_text="You retrace your steps."),
            Action(id="scorchwaste_nomad_well_gate_to_next", label="Press forward", category="movement", target_scene="scorchwaste_nomad_well_courtyard", result_text="You press on to the next area."),
        ]
    )

    # Encounter 16 - Stage 2: Engagement / Climax
    scenes["scorchwaste_nomad_well_courtyard"] = SceneNode(
        id="scorchwaste_nomad_well_courtyard",
        title="Nomad Deep Well - Hoist Platform",
        region="scorchwaste",
        description="A seized brass windlass drum sits jammed with gravel. Desert raiders watch the well from behind high sandbanks. Heat shimmers across the parched stone.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_attribute": {"attribute": "endurance", "value": 14}},
                text="You brace against the dry wind without losing footing."
            ),
        ],
        entities=[
            {"id": "scorch_well_windlass", "name": "Brass Windlass", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="scorch_well_inspect_drum", label="Examine cable drum", category="interaction", result_text="You inspect the gravel-choked gears of the bronze windlass drum."),
            Action(id="scorch_well_repair_windlass", label="Repair well windlass", category="systemic", condition={"any_of": [{"min_attribute": {"attribute": "strength", "value": 14}}, {"has_item": "crowbar"}]}, effects=[{"set_flag": {"flag": "nomad_well_repaired", "value": True}}, {"log_event": "You cleared the jammed gears and repaired the windlass."}], target_scene="scorchwaste_nomad_well_quarters", result_text="You free the seized drum, cranking groundwater to the surface."),
            Action(id="scorch_well_repel_raiders", label="Repel sand raiders", category="trait_exploit", condition={"any_of": [{"min_skill": {"skill": "stealth", "value": 3}}, {"min_attribute": {"attribute": "strength", "value": 15}}]}, effects=[{"set_flag": {"flag": "well_raiders_repelled", "value": True}}, {"log_event": "You repelled the desert raider scouts."}], target_scene="scorchwaste_nomad_well_quarters", result_text="You drive off the raider scouts before they can rush the well."),
            Action(id="scorchwaste_nomad_well_courtyard_to_prev", label="Return back", category="movement", target_scene="scorchwaste_nomad_well_gate", result_text="You retrace your steps."),
            Action(id="scorchwaste_nomad_well_courtyard_to_next", label="Press forward", category="movement", target_scene="scorchwaste_nomad_well_quarters", result_text="You press on to the next area."),
        ]
    )

    # Encounter 16 - Stage 3: Resolution / Consequences
    scenes["scorchwaste_nomad_well_quarters"] = SceneNode(
        id="scorchwaste_nomad_well_quarters",
        title="Nomad Deep Well - Cistern Vault",
        region="scorchwaste",
        description="Damp sand cools the cistern floor beneath the well. Droplets collect on ancient carved sandstone blocks. A leather tool roll lies half buried in the silt.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"flag_is": {"flag": "nomad_well_repaired", "value": True}},
                text="Clear water sloshes inside the hoisted leather well bucket."
            ),
        ],
        entities=[
            {"id": "scorch_well_cistern", "name": "Deep Cistern", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="scorch_well_claim_relic", label="Claim nomad relic", category="interaction", condition={"all_of": [{"any_of": [{"flag_is": {"flag": "nomad_well_repaired", "value": True}}, {"flag_is": {"flag": "well_raiders_repelled", "value": True}}]}, {"lacks_flag": "well_relic_claimed"}]}, effects=[{"add_item": "desert_star_compass"}, {"add_item": "nomad_water_flask"}, {"set_flag": {"flag": "well_relic_claimed", "value": True}}, {"modify_reputation": {"faction": "caravaneers", "value": 20}}, {"log_event": "You unearthed the ancient nomad star compass."}], result_text="You dig out a bronze star compass and an oiled nomad flask from the silt."),
            Action(id="scorch_war_purge_brine_pump", label="Purge Brine Pump", category="systemic", condition={"all_of": [{"flag_is": {"flag": "scorch_faction_chosen", "value": True}}, {"lacks_flag": "scorch_crisis_resolved"}, {"any_of": [{"min_attribute": {"attribute": "strength", "value": 14}}, {"has_item": "crowbar"}]}]}, effects=[{"set_flag": {"flag": "scorch_crisis_resolved", "value": True}}, {"modify_reputation": {"faction": "desert_nomads", "value": 20}}, {"log_event": "You cleared the jammed brine pump with brute force."}], result_text="You pry loose the calcified pump piston. Fresh water surges upward."),
            Action(id="scorch_war_dissolve_scale", label="Dissolve Mineral Scale", category="trait_exploit", condition={"all_of": [{"flag_is": {"flag": "scorch_faction_chosen", "value": True}}, {"lacks_flag": "scorch_crisis_resolved"}, {"min_skill": {"skill": "cunning", "value": 3}}]}, effects=[{"set_flag": {"flag": "scorch_crisis_resolved", "value": True}}, {"modify_reputation": {"faction": "caravaneers", "value": 20}}, {"log_event": "You dissolved mineral deposits in the well intake valves."}], result_text="You pour acid salts into the intake. Crusted scale hisses and dissolves."),
            Action(id="scorch_war_seal_pipeline_pitch", label="Seal Pipe Leaks", category="item_affordance", condition={"all_of": [{"flag_is": {"flag": "scorch_faction_chosen", "value": True}}, {"lacks_flag": "scorch_crisis_resolved"}, {"has_item": "torch"}]}, effects=[{"set_flag": {"flag": "scorch_crisis_resolved", "value": True}}, {"modify_reputation": {"faction": "desert_nomads", "value": 15}}, {"log_event": "You melted desert pitch to seal cracked pipeline seams."}], result_text="You melt pitch over the cracked seams. The hiss of escaping vapor ceases."),
            Action(id="scorch_war_weaponize_brine", label="Divert Brine Flow", category="trait_exploit", condition={"all_of": [{"flag_is": {"flag": "scorch_faction_chosen", "value": True}}, {"lacks_flag": "scorch_crisis_resolved"}, {"min_skill": {"skill": "stealth", "value": 3}}]}, effects=[{"set_flag": {"flag": "scorch_crisis_resolved", "value": True}}, {"modify_reputation": {"faction": "salt_raiders", "value": 20}}, {"log_event": "You diverted caustic brine into rival water tanks."}], result_text="You reroute the toxic brine bypass into the competitor holding basins."),
            Action(id="scorch_well_rest_cistern", label="Rest near basin", category="interaction", effects=[{"modify_stamina": 3}], result_text="The cool cistern air restores your energy."),
            Action(id="scorchwaste_nomad_well_quarters_act_2", label="Inspect salt jars", category="interaction", effects=[{"set_flag": {"flag": "scorchwaste_nomad_well_quarters_footlocker_searched", "value": True}}, {"log_event": "You searched the cistern niche."}], result_text="You check the sealed clay salt jars."),
            Action(id="scorchwaste_nomad_well_quarters_to_prev", label="Return back", category="movement", target_scene="scorchwaste_nomad_well_courtyard", result_text="You retrace your steps."),
            Action(id="scorchwaste_nomad_well_quarters_to_next", label="Press forward", category="movement", target_scene="scorchwaste_nomad_well_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_nomad_well_armory"] = SceneNode(
        id="scorchwaste_nomad_well_armory",
        title="Nomad Deep Well - Supply Depot",
        region="scorchwaste",
        description="Crates of rations and tools stand stacked. A bronze bucket hangs on a hemp rope.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_nomad_well_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_nomad_well_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="scorchwaste_nomad_well_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="scorchwaste_nomad_well_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_nomad_well_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="scorchwaste_nomad_well_armory_to_prev", label="Return back", category="movement", target_scene="scorchwaste_nomad_well_quarters", result_text="You retrace your steps."),
            Action(id="scorchwaste_nomad_well_armory_to_next", label="Press forward", category="movement", target_scene="scorchwaste_nomad_well_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_nomad_well_cellar"] = SceneNode(
        id="scorchwaste_nomad_well_cellar",
        title="Nomad Deep Well - Lower Cellar",
        region="scorchwaste",
        description="Damp air smells of cool earth and storage. A bronze bucket hangs on a hemp rope.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_nomad_well_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="scorchwaste_nomad_well_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="scorchwaste_nomad_well_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_nomad_well_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="scorchwaste_nomad_well_cellar_to_prev", label="Return back", category="movement", target_scene="scorchwaste_nomad_well_armory", result_text="You retrace your steps."),
            Action(id="scorchwaste_nomad_well_cellar_to_next", label="Press forward", category="movement", target_scene="scorchwaste_nomad_well_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_nomad_well_passage"] = SceneNode(
        id="scorchwaste_nomad_well_passage",
        title="Nomad Deep Well - Stone Corridor",
        region="scorchwaste",
        description="Wall sconces hold flickering tallow candles. A bronze bucket hangs on a hemp rope.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_nomad_well_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="scorchwaste_nomad_well_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="scorchwaste_nomad_well_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="scorchwaste_nomad_well_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_nomad_well_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="scorchwaste_nomad_well_passage_to_prev", label="Return back", category="movement", target_scene="scorchwaste_nomad_well_cellar", result_text="You retrace your steps."),
            Action(id="scorchwaste_nomad_well_passage_to_next", label="Press forward", category="movement", target_scene="scorchwaste_nomad_well_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_nomad_well_chamber"] = SceneNode(
        id="scorchwaste_nomad_well_chamber",
        title="Nomad Deep Well - Inner Chamber",
        region="scorchwaste",
        description="A sturdy oak desk holds ledgers and maps. A bronze bucket hangs on a hemp rope.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_nomad_well_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="scorchwaste_nomad_well_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="scorchwaste_nomad_well_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_nomad_well_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="scorchwaste_nomad_well_chamber_to_prev", label="Return back", category="movement", target_scene="scorchwaste_nomad_well_passage", result_text="You retrace your steps."),
            Action(id="scorchwaste_nomad_well_chamber_to_next", label="Press forward", category="movement", target_scene="scorchwaste_nomad_well_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_nomad_well_overlook"] = SceneNode(
        id="scorchwaste_nomad_well_overlook",
        title="Nomad Deep Well - High Overlook",
        region="scorchwaste",
        description="A stone ledge provides a clear view. A bronze bucket hangs on a hemp rope.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_nomad_well_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="scorchwaste_nomad_well_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="scorchwaste_nomad_well_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_nomad_well_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="scorchwaste_nomad_well_overlook_to_prev", label="Return back", category="movement", target_scene="scorchwaste_nomad_well_chamber", result_text="You retrace your steps."),
            Action(id="scorchwaste_nomad_well_overlook_to_next", label="Press forward", category="movement", target_scene="scorchwaste_nomad_well_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_nomad_well_sanctum"] = SceneNode(
        id="scorchwaste_nomad_well_sanctum",
        title="Nomad Deep Well - Inner Sanctum",
        region="scorchwaste",
        description="A stone altar stands in quiet reverence. A bronze bucket hangs on a hemp rope.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="scorchwaste_nomad_well_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="scorchwaste_nomad_well_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="scorchwaste_nomad_well_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_nomad_well_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="scorchwaste_nomad_well_sanctum_to_prev", label="Return back", category="movement", target_scene="scorchwaste_nomad_well_overlook", result_text="You retrace your steps."),
            Action(id="scorchwaste_nomad_well_sanctum_to_next", label="Press forward", category="movement", target_scene="scorchwaste_nomad_well_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["scorchwaste_nomad_well_vault"] = SceneNode(
        id="scorchwaste_nomad_well_vault",
        title="Nomad Deep Well - Deep Vault",
        region="scorchwaste",
        description="Iron-banded chests sit in deep shadows. A bronze bucket hangs on a hemp rope.",
        dynamic_descriptions=[
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
            {'id': 'scorchwaste_nomad_well_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="scorchwaste_nomad_well_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="scorchwaste_nomad_well_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="scorchwaste_nomad_well_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'scorchwaste_nomad_well_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="scorchwaste_nomad_well_vault_to_prev", label="Return back", category="movement", target_scene="scorchwaste_nomad_well_sanctum", result_text="You retrace your steps."),
            Action(id="scorchwaste_nomad_well_vault_to_hub", label="Return to Hub", category="movement", target_scene="scorchwaste_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["scorchwaste_hub"].base_actions.append(
        Action(id="scorchwaste_hub_to_nomad_well", label="Visit Nomad Well", category="movement", target_scene="scorchwaste_nomad_well_gate", result_text="You travel to Nomad Deep Well.")
    )

    return RegionManifest(
        id="scorchwaste",
        name="The Scorchwaste",
        mechanic_name="Ambient Heat & Hydration Survival",
        mechanic_description="Comprehensive open-world region with 10 deep POIs.",
        scenes=scenes
    )