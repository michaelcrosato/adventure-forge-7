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
            Action(id="sunken_hollows_hub_board", label="Check notice board", category="interaction", effects=[{"set_flag": {"flag": "sunken_hollows_notices_read", "value": True}}, {"log_event": "You read the municipal notice board."}], result_text="You read the pinned municipal notices."),
            Action(id="hollows_gate_end_unseal", label="Open deep gate", category="interaction", condition={"flag_is": {"flag": "hollows_trench_keystone_found", "value": True}, "lacks_flag": "hollows_gate_resolved"}, effects=[{"set_flag": {"flag": "hollows_gate_resolved", "value": True}}, {"set_flag": {"flag": "hollows_gate_unsealed", "value": True}}, {"modify_reputation": {"faction": "deep_clans", "value": 30}}, {"log_event": "You unsealed the primordial abyss."}], result_text="The stone gate grinds open and cold currents swirl through."),
            Action(id="hollows_gate_end_ward", label="Ward the gate", category="interaction", condition={"flag_is": {"flag": "hollows_trench_keystone_found", "value": True}, "lacks_flag": "hollows_gate_resolved"}, effects=[{"set_flag": {"flag": "hollows_gate_resolved", "value": True}}, {"set_flag": {"flag": "hollows_gate_warded", "value": True}}, {"log_event": "You placed warding runes to seal the gate forever."}], result_text="Golden wards flare to life and lock the portal shut."),
            Action(id="hollows_gate_end_absorb", label="Drain key power", category="interaction", condition={"flag_is": {"flag": "hollows_trench_keystone_found", "value": True}, "lacks_flag": "hollows_gate_resolved"}, effects=[{"set_flag": {"flag": "hollows_gate_resolved", "value": True}}, {"set_flag": {"flag": "hollows_power_absorbed", "value": True}}, {"log_event": "You channeled the ancient keystone magic into yourself."}], result_text="Raw cold power surges into your veins from the stones."),
            Action(id="hollows_end_archive_sanctuary", label="Ward Sunken Archive", category="social", condition={"all_of": [{"flag_is": {"flag": "hollows_crisis_resolved", "value": True}}, {"lacks_flag": "hollows_schism_resolved"}]}, effects=[{"set_flag": {"flag": "hollows_schism_resolved", "value": True}}, {"set_flag": {"flag": "hollows_ending_archive_sanctuary", "value": True}}, {"modify_reputation": {"faction": "deep_clans", "value": 30}}, {"modify_reputation": {"faction": "trench_divers", "value": -20}}, {"log_event": "You warded the sunken temples to safeguard ancient history."}], result_text="Ancient stone runes flare with blue light, sealing the archives against plunder."),
            Action(id="hollows_end_cartel_dredge", label="Authorize Dredging", category="social", condition={"all_of": [{"flag_is": {"flag": "hollows_crisis_resolved", "value": True}}, {"lacks_flag": "hollows_schism_resolved"}]}, effects=[{"set_flag": {"flag": "hollows_schism_resolved", "value": True}}, {"set_flag": {"flag": "hollows_ending_cartel_dredge", "value": True}}, {"modify_reputation": {"faction": "trench_divers", "value": 30}}, {"modify_reputation": {"faction": "deep_clans", "value": -25}}, {"log_event": "You authorized the Brine Cartel to dredge the ancient vaults."}], result_text="Iron dredges drag heavy chains through the drowned ruins, hoisting relics to surface barges."),
            Action(id="hollows_end_diver_commune", label="Establish Diver Commune", category="social", condition={"all_of": [{"flag_is": {"flag": "hollows_crisis_resolved", "value": True}}, {"lacks_flag": "hollows_schism_resolved"}]}, effects=[{"set_flag": {"flag": "hollows_schism_resolved", "value": True}}, {"set_flag": {"flag": "hollows_ending_diver_commune", "value": True}}, {"modify_reputation": {"faction": "trench_divers", "value": 25}}, {"modify_reputation": {"faction": "deep_clans", "value": 15}}, {"log_event": "You established an independent salvage collective for deep divers."}], result_text="Diver crews cheer as you burn the monopoly charter and declare the wharf free."),
            Action(id="hollows_end_deluge_unsealed", label="Unseal Primeval Deluge", category="trait_exploit", condition={"all_of": [{"flag_is": {"flag": "hollows_crisis_resolved", "value": True}}, {"lacks_flag": "hollows_schism_resolved"}]}, effects=[{"set_flag": {"flag": "hollows_schism_resolved", "value": True}}, {"set_flag": {"flag": "hollows_ending_deluge_unsealed", "value": True}}, {"modify_reputation": {"faction": "deep_clans", "value": -15}}, {"modify_reputation": {"faction": "trench_divers", "value": -15}}, {"log_event": "You broke the ancient sea ward and unleashed primeval tides."}], result_text="Tremendous torrents crash through shattered floodgates. Cold abyssal waters reclaim the caverns."),
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
        entities=[
            {'id': 'sunken_hollows_glow_grotto_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="sunken_hollows_glow_grotto_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="sunken_hollows_glow_grotto_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_glow_grotto_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'sunken_hollows_glow_grotto_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="sunken_hollows_glow_grotto_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="sunken_hollows_glow_grotto_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_glow_grotto_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="sunken_hollows_glow_grotto_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="sunken_hollows_glow_grotto_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="sunken_hollows_glow_grotto_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_glow_grotto_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'sunken_hollows_glow_grotto_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="sunken_hollows_glow_grotto_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="sunken_hollows_glow_grotto_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_glow_grotto_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="sunken_hollows_glow_grotto_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="sunken_hollows_glow_grotto_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="sunken_hollows_glow_grotto_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_glow_grotto_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'sunken_hollows_glow_grotto_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="sunken_hollows_glow_grotto_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="sunken_hollows_glow_grotto_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_glow_grotto_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="sunken_hollows_glow_grotto_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="sunken_hollows_glow_grotto_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="sunken_hollows_glow_grotto_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_glow_grotto_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="sunken_hollows_glow_grotto_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="sunken_hollows_glow_grotto_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="sunken_hollows_glow_grotto_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_glow_grotto_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="sunken_hollows_glow_grotto_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="sunken_hollows_glow_grotto_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="sunken_hollows_glow_grotto_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_glow_grotto_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'sunken_hollows_glow_grotto_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_glow_grotto_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="sunken_hollows_glow_grotto_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="sunken_hollows_glow_grotto_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_glow_grotto_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="hollows_pry_grotto_keystone", label="Pry glowing key", category="interaction", condition={"lacks_flag": "hollows_grotto_keystone_found"}, effects=[{"set_flag": {"flag": "hollows_grotto_keystone_found", "value": True}}, {"add_item": "grotto_keystone"}, {"log_event": "You pried the first abyssal keystone from the rock."}], result_text="The obsidian stone pulses with cold blue light in your hand."),
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
        entities=[
            {'id': 'sunken_hollows_abyssal_river_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="sunken_hollows_abyssal_river_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="sunken_hollows_abyssal_river_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_abyssal_river_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
            Action(id="hollows_schism_scout_currents", label="Scout Currents", category="interaction", condition={"lacks_flag": "hollows_rapids_navigated"}, effects=[{"set_flag": {"flag": "hollows_rapids_navigated", "value": True}}, {"log_event": "You mapped safe submerged currents through the chasm."}], result_text="You track glowing ripples to chart a safe dive path."),
            Action(id="hollows_schism_dive_rapids", label="Dive River Rapids", category="trait_exploit", condition={"all_of": [{"lacks_flag": "hollows_rapids_navigated"}, {"any_of": [{"has_trait": "amphibious"}, {"min_skill": {"skill": "athletics", "value": 3}}]}]}, effects=[{"set_flag": {"flag": "hollows_rapids_navigated", "value": True}}, {"log_event": "You braved the freezing rapids and plunged into the lower caves."}], result_text="You plunge into churning black water and emerge safely downstream."),
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
        entities=[
            {'id': 'sunken_hollows_abyssal_river_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="sunken_hollows_abyssal_river_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="sunken_hollows_abyssal_river_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_abyssal_river_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="sunken_hollows_abyssal_river_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="sunken_hollows_abyssal_river_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="sunken_hollows_abyssal_river_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_abyssal_river_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'sunken_hollows_abyssal_river_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="sunken_hollows_abyssal_river_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="sunken_hollows_abyssal_river_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_abyssal_river_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="sunken_hollows_abyssal_river_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="sunken_hollows_abyssal_river_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="sunken_hollows_abyssal_river_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_abyssal_river_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'sunken_hollows_abyssal_river_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="sunken_hollows_abyssal_river_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="sunken_hollows_abyssal_river_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_abyssal_river_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="sunken_hollows_abyssal_river_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="sunken_hollows_abyssal_river_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="sunken_hollows_abyssal_river_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_abyssal_river_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="sunken_hollows_abyssal_river_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="sunken_hollows_abyssal_river_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="sunken_hollows_abyssal_river_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_abyssal_river_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="sunken_hollows_abyssal_river_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="sunken_hollows_abyssal_river_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="sunken_hollows_abyssal_river_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_abyssal_river_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'sunken_hollows_abyssal_river_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_abyssal_river_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="sunken_hollows_abyssal_river_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="sunken_hollows_abyssal_river_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_abyssal_river_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="sunken_hollows_abyssal_river_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_abyssal_river_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_abyssal_river_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_abyssal_river", label="Visit Subterranean", category="movement", target_scene="sunken_hollows_abyssal_river_gate", result_text="You travel to Subterranean River.")
    )

    # POI: Drowned Shrine (10 nodes)
    # Encounter 10 - Stage 1: Assessment / Approach
    scenes["sunken_hollows_drowned_temple_gate"] = SceneNode(
        id="sunken_hollows_drowned_temple_gate",
        title="Drowned Shrine - Flooded Portico",
        region="sunken_hollows",
        description="Submerged black obsidian pillars rise through calm cavern water. Luminous blue cave fish glide past carved gargoyles. A submerged shrine nave opens below.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your vision pierces the deep water to spot the central altar."
            ),
        ],
        entities=[
            {"id": "sunken_temple_bronze_crane", "name": "Bell Crane", "tags": ["lockable"], "initial_state": "locked"},
            {"id": "sunken_temple_kelp_cluster", "name": "Water Kelp", "tags": ["flammable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="hollows_shrine_inspect_pillars", label="Inspect shrine nave", category="interaction", result_text="You study the ancient stone reliefs submerged in water."),
            Action(id="hollows_shrine_rig_rope", label="Rig descent rope", category="item_affordance", condition={"has_item": "climbing_rope"}, effects=[{"set_flag": {"flag": "shrine_rope_rigged", "value": True}}, {"log_event": "You secured a descent guideline to the submerged altar."}], result_text="The braided rope guides the way to the altar floor."),
            Action(id="hollows_shrine_dive_nave", label="Dive to altar", category="movement", target_scene="sunken_hollows_drowned_temple_courtyard", stamina_cost=1, result_text="You glide down between the dark obsidian colonnades."),
            Action(id="sunken_hollows_drowned_temple_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_courtyard", result_text="You press on to the next area."),
        ]
    )

    # Encounter 10 - Stage 2: Engagement / Climax
    scenes["sunken_hollows_drowned_temple_courtyard"] = SceneNode(
        id="sunken_hollows_drowned_temple_courtyard",
        title="Drowned Shrine - Submerged Altar",
        region="sunken_hollows",
        description="A carved obsidian altar rests on the flooded flagstone floor. A glowing pearl floats inside an iron cage. Predatory cave lampreys circle the ceiling arches.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "water_breather"},
                text="You swim motionlessly in the deep water without disturbing the fish."
            ),
        ],
        entities=[
            {"id": "sunken_temple_altar_cage", "name": "Iron Cage", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="hollows_shrine_pick_cage", label="Pick altar cage", category="item_affordance", condition={"has_item": "lockpick"}, effects=[{"set_flag": {"flag": "altar_cage_opened", "value": True}}, {"log_event": "You picked open the submerged altar lock."}], target_scene="sunken_hollows_drowned_temple_quarters", result_text="The lock tumblers yield cleanly beneath the water."),
            Action(id="hollows_shrine_pry_cage", label="Pry iron cage", category="systemic", condition={"has_item": "crowbar"}, stamina_cost=2, effects=[{"set_flag": {"flag": "altar_cage_opened", "value": True}}, {"log_event": "You forced open the cage bars with raw leverage."}], target_scene="sunken_hollows_drowned_temple_quarters", result_text="The iron bars bend and release the glowing pearl."),
            Action(id="sunken_hollows_drowned_temple_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_quarters", result_text="You press on to the next area."),
        ]
    )

    # Encounter 10 - Stage 3: Resolution / Consequences
    scenes["sunken_hollows_drowned_temple_quarters"] = SceneNode(
        id="sunken_hollows_drowned_temple_quarters",
        title="Drowned Shrine - High Air Belfry",
        region="sunken_hollows",
        description="You kick up into an ancient stone belfry trapped with breathable air. Water drips continuously from the bells. The retrieved abyssal pearl pulses with blue light.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"flag_is": {"flag": "altar_cage_opened", "value": True}},
                text="The radiant pearl illuminates the ancient bell chamber."
            ),
        ],
        entities=[
            {"id": "sunken_temple_belfry_bell", "name": "Temple Bell", "tags": ["flammable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="hollows_shrine_take_pearl", label="Take abyssal pearl", category="interaction", condition={"lacks_flag": "abyssal_pearl_taken"}, effects=[{"add_item": "abyssal_pearl"}, {"set_flag": {"flag": "abyssal_pearl_taken", "value": True}}, {"modify_reputation": {"faction": "hollow_dwellers", "value": 25}}, {"add_marker": "pearl_bearer"}, {"log_event": "You claimed the sacred abyssal pearl."}], result_text="The smooth pearl warms your hand with gentle power."),
            Action(id="hollows_shrine_ring_bell", label="Strike temple bell", category="interaction", effects=[{"log_event": "The deep chime echoes across the underground sea."}], result_text="A deep resonant tone reverberates through the water."),
            Action(id="sunken_hollows_drowned_temple_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_drowned_temple_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_drowned_temple_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_drowned_temple_armory", result_text="You press on to the supply depot."),
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
        entities=[
            {'id': 'sunken_hollows_drowned_temple_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="sunken_hollows_drowned_temple_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="sunken_hollows_drowned_temple_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_drowned_temple_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="sunken_hollows_drowned_temple_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="sunken_hollows_drowned_temple_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="sunken_hollows_drowned_temple_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_drowned_temple_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'sunken_hollows_drowned_temple_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="sunken_hollows_drowned_temple_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="sunken_hollows_drowned_temple_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_drowned_temple_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="sunken_hollows_drowned_temple_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="sunken_hollows_drowned_temple_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="sunken_hollows_drowned_temple_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_drowned_temple_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="sunken_hollows_drowned_temple_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="sunken_hollows_drowned_temple_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="sunken_hollows_drowned_temple_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_drowned_temple_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="sunken_hollows_drowned_temple_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="sunken_hollows_drowned_temple_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="sunken_hollows_drowned_temple_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_drowned_temple_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'sunken_hollows_drowned_temple_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_drowned_temple_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="sunken_hollows_drowned_temple_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="sunken_hollows_drowned_temple_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_drowned_temple_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        title="Crystal Trench - Outer Chasm",
        region="sunken_hollows",
        description="Bioluminescent coral clings to the sheer chasm precipice. Cold seawater surges through deep fissures below. Dark abyssal currents pull at loose gravel.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "water_breather"},
                text="Your gills adapt smoothly to the icy hydrostatic pressure."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'hollows_coral_chasm_gate_pulley', 'name': 'Descent Winch', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="hollows_coral_scout_trench", label="Survey deep chasm", category="interaction", result_text="You study the sheer drop and locate anchoring points in the basalt shelf."),
            Action(id="hollows_coral_anchor_winch", label="Rig descent winch", category="item_affordance", condition={"has_item": "climbing_rope"}, effects=[{'set_flag': {'flag': 'trench_descent_rigged', 'value': True}}, {'log_event': 'You rigged a weighted descent rope.'}], target_scene="sunken_hollows_coral_chasm_courtyard", result_text="You anchor a weighted descent line over the chasm lip and rappel downward."),
            Action(id="hollows_coral_plunge_abyss", label="Plunge into abyss", category="trait_exploit", condition={"any_of": [{"has_trait": "water_breather"}, {"min_attribute": {"attribute": "endurance", "value": 14}}]}, target_scene="sunken_hollows_coral_chasm_courtyard", result_text="You leap directly into the icy underwater abyss and sink smoothly downward."),
            Action(id="hollows_trade_black_pearls", label="Trade Black Pearls", category="social", condition={"has_marker": "syndicate_contact"}, effects=[{"add_item": "diving_helm"}, {"set_flag": {"flag": "hollows_black_pearls_traded", "value": True}}, {"modify_reputation": {"faction": "shadow_syndicate", "value": 15}}, {"log_event": "You traded illicit deep-sea black pearls through syndicate fences."}], result_text="A shadowy diver swaps an armored diving helmet for your smuggler tokens."),
            Action(id="sunken_hollows_coral_chasm_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_courtyard"] = SceneNode(
        id="sunken_hollows_coral_chasm_courtyard",
        title="Crystal Trench - Pressure Sluice",
        region="sunken_hollows",
        description="Submerged hydraulic sluice gates shudder under immense ocean pressure. Serrated thickets of violet razor coral encircle the catwalk. Trapped geyser steam vents along the seabed floor.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "nimble"},
                text="You dodge sharp polyps swaying in the cold water."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'hollows_coral_chasm_valve_mechanism', 'name': 'Bronze Sluice', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="hollows_coral_inspect_sluice", label="Inspect pressure valve", category="interaction", result_text="You inspect the corroded bronze wheel controlling the hydraulic drain."),
            Action(id="hollows_coral_crank_valve", label="Crank pressure valve", category="systemic", condition={"any_of": [{"has_item": "crowbar"}, {"min_attribute": {"attribute": "strength", "value": 15}}]}, effects=[{'set_flag': {'flag': 'chasm_valve_opened', 'value': True}}, {'log_event': 'You cracked open the rusted pressure valve.'}], target_scene="sunken_hollows_coral_chasm_quarters", result_text="You strain against the rusted valve wheel until boiling steam vents outward."),
            Action(id="hollows_coral_dodge_tendrils", label="Dodge razor spines", category="trait_exploit", condition={"has_trait": "nimble"}, effects=[{'log_event': 'You weaved nimbly through razor coral spines.'}], target_scene="sunken_hollows_coral_chasm_quarters", result_text="You twist deftly between vibrating razor spines and drop safely down."),
            Action(id="sunken_hollows_coral_chasm_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_coral_chasm_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_coral_chasm_quarters"] = SceneNode(
        id="sunken_hollows_coral_chasm_quarters",
        title="Crystal Trench - Abyssal Shelf",
        region="sunken_hollows",
        description="Drained obsidian shelves glisten under radiant mineral glow. Subterranean thermal vents warm the exposed crystal seabed. Exhaust steam escapes through heavy relief valves.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"flag_is": {"flag": "chasm_valve_opened", "value": True}},
                text="The drained seabed reveals vibrant crystal clusters nestled in the basalt."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'hollows_coral_chasm_quarters_crystal_bed', 'name': 'Crystal Bed', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="hollows_coral_harvest_prism", label="Harvest seabed prism", category="interaction", condition={"all_of": [{"flag_is": {"flag": "chasm_valve_opened", "value": True}}, {"lacks_flag": "abyssal_prism_harvested"}]}, effects=[{'add_item': 'abyssal_prism_core'}, {'add_item': 'deep_trench_helm'}, {'set_flag': {'flag': 'abyssal_prism_harvested', 'value': True}}, {'modify_reputation': {'faction': 'hollow_dwellers', 'value': 25}}, {'log_event': 'You harvested the abyssal prism core.'}], result_text="You pry the glowing abyssal prism core and salvage an ancient diving helm."),
            Action(id="hollows_coral_rest_shelf", label="Rest on shelf", category="interaction", effects=[{'modify_stamina': 3}], result_text="You rest on the warm volcanic stone and replenish your breath."),
            Action(id="sunken_hollows_coral_chasm_quarters_act_2", label="Search coral shelf", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_coral_chasm_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the coral shelf.'}], result_text="You sift through mineral crusts along the exposed seabed."),
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
        entities=[
            {'id': 'sunken_hollows_coral_chasm_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="sunken_hollows_coral_chasm_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="sunken_hollows_coral_chasm_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_coral_chasm_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="sunken_hollows_coral_chasm_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="sunken_hollows_coral_chasm_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="sunken_hollows_coral_chasm_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_coral_chasm_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'sunken_hollows_coral_chasm_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="sunken_hollows_coral_chasm_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="sunken_hollows_coral_chasm_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_coral_chasm_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="sunken_hollows_coral_chasm_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="sunken_hollows_coral_chasm_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="sunken_hollows_coral_chasm_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_coral_chasm_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="sunken_hollows_coral_chasm_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="sunken_hollows_coral_chasm_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="sunken_hollows_coral_chasm_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_coral_chasm_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="sunken_hollows_coral_chasm_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="sunken_hollows_coral_chasm_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="sunken_hollows_coral_chasm_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_coral_chasm_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'sunken_hollows_coral_chasm_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_coral_chasm_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="sunken_hollows_coral_chasm_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="sunken_hollows_coral_chasm_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_coral_chasm_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="hollows_dredge_trench_keystone", label="Dredge silt key", category="interaction", condition={"flag_is": {"flag": "hollows_grotto_keystone_found", "value": True}, "lacks_flag": "hollows_trench_keystone_found"}, effects=[{"set_flag": {"flag": "hollows_trench_keystone_found", "value": True}}, {"add_item": "trench_keystone"}, {"log_event": "You dredged the second keystone from the mud."}], result_text="You pull a mud-covered runic wedge from the deep silt."),
            Action(id="sunken_hollows_coral_chasm_vault_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_coral_chasm_sanctum", result_text="You retrace your steps."),
            Action(id="sunken_hollows_coral_chasm_vault_to_hub", label="Return to Hub", category="movement", target_scene="sunken_hollows_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["sunken_hollows_hub"].base_actions.append(
        Action(id="sunken_hollows_hub_to_coral_chasm", label="Visit Crystal Tren", category="movement", target_scene="sunken_hollows_coral_chasm_gate", result_text="You travel to Crystal Trench.")
    )

    # POI: The Flooded Siphon (10 nodes)
    # Encounter 9 - Stage 1: Assessment / Approach
    scenes["sunken_hollows_deep_siphon_gate"] = SceneNode(
        id="sunken_hollows_deep_siphon_gate",
        title="The Flooded Siphon - Cave Shore",
        region="sunken_hollows",
        description="Dark subterranean water laps against slick limestone shelves. Glowing green moss illuminates a flooded tunnel entrance. Rising bubbles hint at caverns beyond.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "water_breather"},
                text="Your gills pulse as they sample the oxygenated currents."
            ),
            DynamicDescription(
                condition={"ancestry_is": "deep_dweller"},
                text="The scent of mineral water and cool stone is familiar."
            ),
        ],
        entities=[
            {"id": "sunken_limestone_shelf", "name": "Limestone Shelf", "tags": ["climbable"], "climb_destination": "sunken_hollows_deep_siphon_courtyard"},
            {"id": "sunken_driftwood_pile", "name": "Cave Driftwood", "tags": ["flammable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="hollows_siphon_survey_depth", label="Survey water depth", category="interaction", result_text="You test the depth with a staff. The channel drops sharply."),
            Action(id="hollows_siphon_seal_gear", label="Apply waterproof seal", category="item_affordance", condition={"has_item": "waterproof_seal"}, effects=[{"set_flag": {"flag": "gear_waterproofed", "value": True}}, {"log_event": "You treated your pack with waterproof sealant."}], result_text="Your equipment is secure against immersion."),
            Action(id="hollows_siphon_dive_pool", label="Plunge into siphon", category="movement", target_scene="sunken_hollows_deep_siphon_courtyard", stamina_cost=2, result_text="You take a deep breath and dive into the freezing underground river."),
            Action(id="hollows_claim_salvage_rig", label="Claim Salvage Rig", category="social", condition={"has_marker": "river_bailiff"}, effects=[{"modify_reputation": {"faction": "trench_divers", "value": 20}}, {"set_flag": {"flag": "hollows_salvage_rig_claimed", "value": True}}, {"log_event": "You leveraged River Guild bailiff authority to claim salvage rig rights."}], result_text="The harbor master honors the River Guild warrant and grants rig access."),
            Action(id="sunken_hollows_deep_siphon_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_courtyard", result_text="You press on to the next area."),
        ]
    )

    # Encounter 9 - Stage 2: Engagement / Climax
    scenes["sunken_hollows_deep_siphon_courtyard"] = SceneNode(
        id="sunken_hollows_deep_siphon_courtyard",
        title="The Flooded Siphon - Choked Conduit",
        region="sunken_hollows",
        description="Frigid water exerts crushing pressure in the narrow stone siphon. A silt collapse partially chokes the tunnel. Lungs burn as air dwindles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "water_breather"},
                text="You breathe effortlessly in the submerged darkness."
            ),
        ],
        entities=[
            {"id": "sunken_choked_boulder", "name": "Choked Boulder", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="hollows_siphon_push_boulder", label="Heave choked stone", category="systemic", condition={"min_attribute": {"attribute": "strength", "value": 13}}, effects=[{"set_flag": {"flag": "siphon_cleared", "value": True}}, {"log_event": "You dislodged the boulder and opened the airway."}], target_scene="sunken_hollows_deep_siphon_quarters", result_text="You roll the heavy rock free and surge upward through the gap."),
            Action(id="hollows_siphon_endure_breath", label="Hold breath hard", category="trait_exploit", condition={"min_attribute": {"attribute": "endurance", "value": 14}}, effects=[{"set_flag": {"flag": "siphon_cleared", "value": True}}], target_scene="sunken_hollows_deep_siphon_quarters", result_text="You suppress the burning panic and kick through the silt."),
            Action(id="hollows_siphon_pry_crowbar", label="Pry stone loose", category="item_affordance", condition={"has_item": "crowbar"}, effects=[{"set_flag": {"flag": "siphon_cleared", "value": True}}], target_scene="sunken_hollows_deep_siphon_quarters", result_text="The iron crowbar levers the blockage out of the channel."),
            Action(id="sunken_hollows_deep_siphon_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_deep_siphon_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_deep_siphon_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_deep_siphon_quarters", result_text="You press on to the next area."),
        ]
    )

    # Encounter 9 - Stage 3: Resolution / Consequences
    scenes["sunken_hollows_deep_siphon_quarters"] = SceneNode(
        id="sunken_hollows_deep_siphon_quarters",
        title="The Flooded Siphon - Trapped Air Dome",
        region="sunken_hollows",
        description="You break the surface and cough fresh air into an ancient dry cavern dome. Bioluminescent crystal stalactites glow along the vault. A chitin shell rests upon dry sand.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"flag_is": {"flag": "siphon_cleared", "value": True}},
                text="The air pocket remains stable and dry above the submerged current."
            ),
        ],
        entities=[
            {"id": "sunken_chitin_relic", "name": "Chitin Relic", "tags": ["lockable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="hollows_siphon_take_shield", label="Take chitin shield", category="interaction", condition={"lacks_flag": "chitin_shield_taken"}, effects=[{"add_item": "chitin_shield"}, {"set_flag": {"flag": "chitin_shield_taken", "value": True}}, {"modify_health": 4}, {"log_event": "You claimed the lightweight chitin shield."}], result_text="You strap the iridescent chitin shield to your arm."),
            Action(id="hollows_schism_crank_pressure_valve", label="Crank Pressure Valve", category="systemic", condition={"all_of": [{"flag_is": {"flag": "hollows_faction_chosen", "value": True}}, {"lacks_flag": "hollows_crisis_resolved"}, {"any_of": [{"min_attribute": {"attribute": "strength", "value": 14}}, {"has_item": "crowbar"}]}]}, effects=[{"set_flag": {"flag": "hollows_crisis_resolved", "value": True}}, {"modify_reputation": {"faction": "deep_clans", "value": 20}}, {"log_event": "You heaved the rusted pressure valve shut, stopping the cave flood."}], result_text="You throw your weight against the iron wheel. The roaring siphon slows to a trickle."),
            Action(id="hollows_schism_seal_air_line", label="Patch Diving Hose", category="trait_exploit", condition={"all_of": [{"flag_is": {"flag": "hollows_faction_chosen", "value": True}}, {"lacks_flag": "hollows_crisis_resolved"}, {"min_skill": {"skill": "cunning", "value": 3}}]}, effects=[{"set_flag": {"flag": "hollows_crisis_resolved", "value": True}}, {"modify_reputation": {"faction": "trench_divers", "value": 20}}, {"log_event": "You repaired the severed rubber air line under high hydrostatic pressure."}], result_text="You wrap tarred canvas around the severed hose, restoring breathing air."),
            Action(id="hollows_schism_tune_acoustic_bell", label="Ring Acoustic Resonator", category="item_affordance", condition={"all_of": [{"flag_is": {"flag": "hollows_faction_chosen", "value": True}}, {"lacks_flag": "hollows_crisis_resolved"}, {"has_item": "tuning_fork"}]}, effects=[{"set_flag": {"flag": "hollows_crisis_resolved", "value": True}}, {"modify_reputation": {"faction": "deep_clans", "value": 15}}, {"log_event": "You struck the bronze acoustic bell to disperse water pressure waves."}], result_text="The brass chime vibrates underwater, settling the turbulent pressure surge."),
            Action(id="hollows_schism_dredge_ruins", label="Dredge Submerged Ruins", category="trait_exploit", condition={"all_of": [{"flag_is": {"flag": "hollows_faction_chosen", "value": True}}, {"lacks_flag": "hollows_crisis_resolved"}, {"min_skill": {"skill": "athletics", "value": 3}}]}, effects=[{"set_flag": {"flag": "hollows_crisis_resolved", "value": True}}, {"modify_reputation": {"faction": "trench_divers", "value": 20}}, {"log_event": "You dived into the flooding ruins to recover drowned salvage gear."}], result_text="You haul heavy diving equipment out of the rising deep waters."),
            Action(id="hollows_siphon_rest_sand", label="Rest on sand", category="interaction", effects=[{"modify_stamina": 5}], result_text="You stretch out on the warm subterranean sand."),
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
        entities=[
            {'id': 'sunken_hollows_deep_siphon_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="sunken_hollows_deep_siphon_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="sunken_hollows_deep_siphon_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_deep_siphon_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="sunken_hollows_deep_siphon_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="sunken_hollows_deep_siphon_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="sunken_hollows_deep_siphon_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_deep_siphon_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'sunken_hollows_deep_siphon_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="sunken_hollows_deep_siphon_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="sunken_hollows_deep_siphon_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_deep_siphon_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="sunken_hollows_deep_siphon_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="sunken_hollows_deep_siphon_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="sunken_hollows_deep_siphon_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_deep_siphon_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="sunken_hollows_deep_siphon_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="sunken_hollows_deep_siphon_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="sunken_hollows_deep_siphon_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_deep_siphon_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="sunken_hollows_deep_siphon_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="sunken_hollows_deep_siphon_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="sunken_hollows_deep_siphon_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_deep_siphon_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'sunken_hollows_deep_siphon_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_deep_siphon_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="sunken_hollows_deep_siphon_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="sunken_hollows_deep_siphon_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_deep_siphon_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        entities=[
            {'id': 'sunken_hollows_vault_depths_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="sunken_hollows_vault_depths_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="sunken_hollows_vault_depths_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_vault_depths_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'sunken_hollows_vault_depths_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="sunken_hollows_vault_depths_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="sunken_hollows_vault_depths_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_vault_depths_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="sunken_hollows_vault_depths_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="sunken_hollows_vault_depths_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="sunken_hollows_vault_depths_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_vault_depths_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'sunken_hollows_vault_depths_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="sunken_hollows_vault_depths_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="sunken_hollows_vault_depths_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_vault_depths_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="sunken_hollows_vault_depths_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="sunken_hollows_vault_depths_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="sunken_hollows_vault_depths_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_vault_depths_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'sunken_hollows_vault_depths_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="sunken_hollows_vault_depths_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="sunken_hollows_vault_depths_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_vault_depths_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="sunken_hollows_vault_depths_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="sunken_hollows_vault_depths_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="sunken_hollows_vault_depths_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_vault_depths_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="sunken_hollows_vault_depths_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="sunken_hollows_vault_depths_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="sunken_hollows_vault_depths_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_vault_depths_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="sunken_hollows_vault_depths_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="sunken_hollows_vault_depths_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="sunken_hollows_vault_depths_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_vault_depths_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'sunken_hollows_vault_depths_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_vault_depths_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="sunken_hollows_vault_depths_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="sunken_hollows_vault_depths_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_vault_depths_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        entities=[
            {'id': 'sunken_hollows_fungal_forest_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="sunken_hollows_fungal_forest_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="sunken_hollows_fungal_forest_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_fungal_forest_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'sunken_hollows_fungal_forest_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="sunken_hollows_fungal_forest_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="sunken_hollows_fungal_forest_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_fungal_forest_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="sunken_hollows_fungal_forest_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="sunken_hollows_fungal_forest_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="sunken_hollows_fungal_forest_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_fungal_forest_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'sunken_hollows_fungal_forest_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="sunken_hollows_fungal_forest_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="sunken_hollows_fungal_forest_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_fungal_forest_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="sunken_hollows_fungal_forest_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="sunken_hollows_fungal_forest_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="sunken_hollows_fungal_forest_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_fungal_forest_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'sunken_hollows_fungal_forest_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="sunken_hollows_fungal_forest_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="sunken_hollows_fungal_forest_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_fungal_forest_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="sunken_hollows_fungal_forest_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="sunken_hollows_fungal_forest_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="sunken_hollows_fungal_forest_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_fungal_forest_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="sunken_hollows_fungal_forest_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="sunken_hollows_fungal_forest_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="sunken_hollows_fungal_forest_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_fungal_forest_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="sunken_hollows_fungal_forest_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="sunken_hollows_fungal_forest_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="sunken_hollows_fungal_forest_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_fungal_forest_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'sunken_hollows_fungal_forest_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_fungal_forest_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="sunken_hollows_fungal_forest_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="sunken_hollows_fungal_forest_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_fungal_forest_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        entities=[
            {'id': 'sunken_hollows_sub_wharf_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="sunken_hollows_sub_wharf_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="sunken_hollows_sub_wharf_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_sub_wharf_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'sunken_hollows_sub_wharf_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="sunken_hollows_sub_wharf_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="sunken_hollows_sub_wharf_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_sub_wharf_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
            Action(id="hollows_schism_pledge_scholars", label="Pledge To Scholars", category="social", condition={"all_of": [{"flag_is": {"flag": "hollows_rapids_navigated", "value": True}}, {"lacks_flag": "hollows_faction_chosen"}]}, effects=[{"set_flag": {"flag": "hollows_faction_chosen", "value": True}}, {"set_flag": {"flag": "hollows_allied_scholars", "value": True}}, {"modify_reputation": {"faction": "deep_clans", "value": 15}}, {"modify_reputation": {"faction": "trench_divers", "value": -10}}, {"log_event": "You pledged your blade to the Scholar Antiquarians."}], result_text="Scholar Vance gives you an inscribed slate catalog of primeval runes."),
            Action(id="hollows_schism_contract_cartel", label="Sign Cartel Contract", category="social", condition={"all_of": [{"flag_is": {"flag": "hollows_rapids_navigated", "value": True}}, {"lacks_flag": "hollows_faction_chosen"}]}, effects=[{"set_flag": {"flag": "hollows_faction_chosen", "value": True}}, {"set_flag": {"flag": "hollows_allied_cartel", "value": True}}, {"modify_reputation": {"faction": "trench_divers", "value": 15}}, {"modify_reputation": {"faction": "deep_clans", "value": -10}}, {"log_event": "You signed a salvage contract with the Brine Cartel."}], result_text="Master Orlov claps your shoulder and hands you a diver wage advance."),
            Action(id="hollows_schism_unionize_divers", label="Unionize Trench Divers", category="social", condition={"all_of": [{"flag_is": {"flag": "hollows_rapids_navigated", "value": True}}, {"lacks_flag": "hollows_faction_chosen"}, {"min_skill": {"skill": "rhetoric", "value": 3}}]}, effects=[{"set_flag": {"flag": "hollows_faction_chosen", "value": True}}, {"set_flag": {"flag": "hollows_allied_union", "value": True}}, {"modify_reputation": {"faction": "trench_divers", "value": 20}}, {"modify_reputation": {"faction": "deep_clans", "value": 5}}, {"log_event": "You organized an independent salvage strike on the wharf."}], result_text="The gathered divers strike their lead boots together in solidarity."),
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
            Action(id="sunken_hollows_sub_wharf_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="sunken_hollows_sub_wharf_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="sunken_hollows_sub_wharf_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_sub_wharf_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'sunken_hollows_sub_wharf_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="sunken_hollows_sub_wharf_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="sunken_hollows_sub_wharf_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_sub_wharf_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="sunken_hollows_sub_wharf_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="sunken_hollows_sub_wharf_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="sunken_hollows_sub_wharf_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_sub_wharf_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'sunken_hollows_sub_wharf_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="sunken_hollows_sub_wharf_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="sunken_hollows_sub_wharf_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_sub_wharf_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="sunken_hollows_sub_wharf_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="sunken_hollows_sub_wharf_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="sunken_hollows_sub_wharf_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_sub_wharf_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="sunken_hollows_sub_wharf_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="sunken_hollows_sub_wharf_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="sunken_hollows_sub_wharf_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_sub_wharf_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="sunken_hollows_sub_wharf_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="sunken_hollows_sub_wharf_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="sunken_hollows_sub_wharf_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_sub_wharf_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'sunken_hollows_sub_wharf_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_sub_wharf_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="sunken_hollows_sub_wharf_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="sunken_hollows_sub_wharf_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_sub_wharf_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        entities=[
            {'id': 'sunken_hollows_geyser_basin_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="sunken_hollows_geyser_basin_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="sunken_hollows_geyser_basin_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_geyser_basin_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'sunken_hollows_geyser_basin_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="sunken_hollows_geyser_basin_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="sunken_hollows_geyser_basin_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_geyser_basin_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="sunken_hollows_geyser_basin_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="sunken_hollows_geyser_basin_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="sunken_hollows_geyser_basin_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_geyser_basin_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'sunken_hollows_geyser_basin_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="sunken_hollows_geyser_basin_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="sunken_hollows_geyser_basin_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_geyser_basin_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="sunken_hollows_geyser_basin_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="sunken_hollows_geyser_basin_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="sunken_hollows_geyser_basin_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_geyser_basin_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'sunken_hollows_geyser_basin_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="sunken_hollows_geyser_basin_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="sunken_hollows_geyser_basin_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_geyser_basin_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="sunken_hollows_geyser_basin_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="sunken_hollows_geyser_basin_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="sunken_hollows_geyser_basin_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_geyser_basin_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="sunken_hollows_geyser_basin_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="sunken_hollows_geyser_basin_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="sunken_hollows_geyser_basin_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_geyser_basin_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="sunken_hollows_geyser_basin_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="sunken_hollows_geyser_basin_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="sunken_hollows_geyser_basin_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_geyser_basin_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'sunken_hollows_geyser_basin_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_geyser_basin_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="sunken_hollows_geyser_basin_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="sunken_hollows_geyser_basin_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_geyser_basin_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        title="The Echoing Dome - Outer Arch",
        region="sunken_hollows",
        description="Cold cavern winds hum through the stone archway. Towering dome vaults magnify footsteps into booming echoes.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_attribute": {"attribute": "endurance", "value": 14}},
                text="Your sturdy endurance helps you resist loud ringing."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'sunken_hollows_echoing_dome_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="hollows_dome_scout_entrance", label="Survey echoing dome", category="interaction", result_text="You inspect the towering stone vault and track acoustic reverberations."),
            Action(id="hollows_dome_strike_tuning_fork", label="Strike tuning fork", category="interaction", result_text="You strike a bronze pitch fork against the arch to locate resonant frequency nodes."),
            Action(id="hollows_dome_brace_ears", label="Brace against harmonics", category="systemic", condition={"min_attribute": {"attribute": "endurance", "value": 14}}, effects=[{'modify_stamina': 2}, {'log_event': 'You braced against ultrasonic harmonics.'}], result_text="You steel your resolve and steady your breathing against concussive acoustic waves."),
            Action(id="sunken_hollows_echoing_dome_gate_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_hub", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_gate_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_courtyard", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_courtyard"] = SceneNode(
        id="sunken_hollows_echoing_dome_courtyard",
        title="The Echoing Dome - Bell Chamber",
        region="sunken_hollows",
        description="Massive bronze bells hang suspended above dark reflecting pools. Sound waves vibrate through subterranean basalt arches. Droplets strike stone with ringing clarity.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "water_breather"},
                text="You spot calm underwater currents below the quiet pool."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        entities=[
            {'id': 'sunken_hollows_echoing_dome_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="hollows_dome_inspect_bells", label="Inspect bronze bells", category="interaction", result_text="You study the suspended acoustic bells and locate the fallen central chime."),
            Action(id="hollows_dome_tune_bells", label="Tune resonator bells", category="trait_exploit", condition={"any_of": [{"min_skill": {"skill": "cunning", "value": 3}}, {"has_item": "crowbar"}]}, effects=[{'set_flag': {'flag': 'dome_bells_tuned', 'value': True}}, {'log_event': 'You aligned the acoustic resonator bells.'}], target_scene="sunken_hollows_echoing_dome_quarters", result_text="You adjust the heavy bronze bells until they ring in perfect harmony."),
            Action(id="hollows_dome_dive_pool", label="Dive resonance pool", category="trait_exploit", condition={"has_trait": "water_breather"}, effects=[{'set_flag': {'flag': 'dome_pool_damped', 'value': True}}, {'log_event': 'You released the submerged acoustic damper.'}], target_scene="sunken_hollows_echoing_dome_quarters", result_text="You dive into the icy pool and release the jammed stone dampening block."),
            Action(id="sunken_hollows_echoing_dome_courtyard_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_gate", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_courtyard_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_quarters", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_quarters"] = SceneNode(
        id="sunken_hollows_echoing_dome_quarters",
        title="The Echoing Dome - Harmonic Sanctuary",
        region="sunken_hollows",
        description="Obsidian pillars stand around a circular stone dais. Gentle vibrations pulse through the quiet cavern sanctuary. Clear water laps against carved black steps.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"flag_is": {"flag": "dome_bells_tuned", "value": True}},
                text="The tuned bronze bells keep a gentle soothing chime."
            ),
            DynamicDescription(
                condition={"flag_is": {"flag": "dome_pool_damped", "value": True}},
                text="The sunken stone damper quiets loud cavern echoes."
            ),
        ],
        entities=[
            {'id': 'sunken_hollows_echoing_dome_quarters_dais', 'name': 'Resonance Dais', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="hollows_dome_claim_chime", label="Claim harmonic chime", category="interaction", condition={"all_of": [{"any_of": [{"flag_is": {"flag": "dome_bells_tuned", "value": True}}, {"flag_is": {"flag": "dome_pool_damped", "value": True}}]}, {"lacks_flag": "harmonic_chime_taken"}]}, effects=[{'add_item': 'harmonic_obsidian_bell'}, {'set_flag': {'flag': 'harmonic_chime_taken', 'value': True}}, {'modify_reputation': {'faction': 'hollow_dwellers', 'value': 20}}, {'add_marker': 'echo_master'}, {'log_event': 'You claimed the harmonic obsidian bell.'}], result_text="You retrieve the humming harmonic obsidian bell from the center dais."),
            Action(id="hollows_dome_rest_dais", label="Rest on dais", category="interaction", effects=[{'modify_stamina': 3}], result_text="You rest on the acoustic dais as soothing harmonics ease your fatigue."),
            Action(id="sunken_hollows_echoing_dome_quarters_act_2", label="Search stone alcove", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_echoing_dome_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the stone alcove.'}], result_text="You search an acoustic niche carved into the obsidian wall."),
            Action(id="sunken_hollows_echoing_dome_quarters_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_courtyard", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_quarters_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_armory", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_armory"] = SceneNode(
        id="sunken_hollows_echoing_dome_armory",
        title="The Echoing Dome - Supply Depot",
        region="sunken_hollows",
        description="Crates of rations and tools stand stacked. The huge dark caves carry quiet echoes for miles.",
        dynamic_descriptions=[
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
            {'id': 'sunken_hollows_echoing_dome_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="sunken_hollows_echoing_dome_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="sunken_hollows_echoing_dome_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_echoing_dome_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
            Action(id="sunken_hollows_echoing_dome_armory_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_quarters", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_armory_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_cellar", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_cellar"] = SceneNode(
        id="sunken_hollows_echoing_dome_cellar",
        title="The Echoing Dome - Lower Cellar",
        region="sunken_hollows",
        description="Damp air smells of cool earth and storage. The huge dark caves carry quiet echoes for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="sunken_hollows_echoing_dome_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="sunken_hollows_echoing_dome_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_echoing_dome_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
            Action(id="sunken_hollows_echoing_dome_cellar_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_armory", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_cellar_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_passage", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_passage"] = SceneNode(
        id="sunken_hollows_echoing_dome_passage",
        title="The Echoing Dome - Stone Corridor",
        region="sunken_hollows",
        description="Wall sconces hold flickering tallow candles. The huge dark caves carry quiet echoes for miles.",
        dynamic_descriptions=[
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
            {'id': 'sunken_hollows_echoing_dome_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="sunken_hollows_echoing_dome_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="sunken_hollows_echoing_dome_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_echoing_dome_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
            Action(id="sunken_hollows_echoing_dome_passage_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_cellar", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_passage_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_chamber", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_chamber"] = SceneNode(
        id="sunken_hollows_echoing_dome_chamber",
        title="The Echoing Dome - Inner Chamber",
        region="sunken_hollows",
        description="A sturdy oak desk holds ledgers and maps. The huge dark caves carry quiet echoes for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="sunken_hollows_echoing_dome_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="sunken_hollows_echoing_dome_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_echoing_dome_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
            Action(id="sunken_hollows_echoing_dome_chamber_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_passage", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_chamber_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_overlook", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_overlook"] = SceneNode(
        id="sunken_hollows_echoing_dome_overlook",
        title="The Echoing Dome - High Overlook",
        region="sunken_hollows",
        description="A stone ledge provides a clear view. The huge dark caves carry quiet echoes for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="sunken_hollows_echoing_dome_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="sunken_hollows_echoing_dome_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_echoing_dome_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
            Action(id="sunken_hollows_echoing_dome_overlook_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_chamber", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_overlook_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_sanctum", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_sanctum"] = SceneNode(
        id="sunken_hollows_echoing_dome_sanctum",
        title="The Echoing Dome - Inner Sanctum",
        region="sunken_hollows",
        description="A stone altar stands in quiet reverence. The huge dark caves carry quiet echoes for miles.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "night_eyed"},
                text="Your keen eyes track motion in the dark."
            ),
            DynamicDescription(
                condition={"min_skill": {"skill": "cunning", "value": 2}},
                text="You note tactical cover and exit routes."
            ),
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="sunken_hollows_echoing_dome_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="sunken_hollows_echoing_dome_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_echoing_dome_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
            Action(id="sunken_hollows_echoing_dome_sanctum_to_prev", label="Return back", category="movement", target_scene="sunken_hollows_echoing_dome_overlook", result_text="You retrace your steps."),
            Action(id="sunken_hollows_echoing_dome_sanctum_to_next", label="Press forward", category="movement", target_scene="sunken_hollows_echoing_dome_vault", result_text="You press on to the next area."),
        ]
    )

    scenes["sunken_hollows_echoing_dome_vault"] = SceneNode(
        id="sunken_hollows_echoing_dome_vault",
        title="The Echoing Dome - Deep Vault",
        region="sunken_hollows",
        description="Iron-banded chests sit in deep shadows. The huge dark caves carry quiet echoes for miles.",
        dynamic_descriptions=[
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
            {'id': 'sunken_hollows_echoing_dome_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="sunken_hollows_echoing_dome_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="sunken_hollows_echoing_dome_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="sunken_hollows_echoing_dome_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'sunken_hollows_echoing_dome_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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