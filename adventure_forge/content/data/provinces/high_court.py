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
            Action(id="high_court_hub_board", label="Check notice board", category="interaction", effects=[{"set_flag": {"flag": "high_court_notices_read", "value": True}}, {"log_event": "You read the municipal notice board."}], result_text="You read the pinned municipal notices."),
            Action(id="court_decree_end_reform", label="Vote for reform", category="interaction", condition={"flag_is": {"flag": "court_nobles_swayed", "value": True}, "lacks_flag": "court_decree_resolved"}, effects=[{"set_flag": {"flag": "court_decree_resolved", "value": True}}, {"set_flag": {"flag": "court_decree_reformed", "value": True}}, {"modify_reputation": {"faction": "commoners", "value": 25}}, {"log_event": "You passed sweeping constitutional reforms."}], result_text="The magistrate stamps the reform charter with imperial wax."),
            Action(id="court_decree_end_martial", label="Vote martial rule", category="interaction", condition={"flag_is": {"flag": "court_nobles_swayed", "value": True}, "lacks_flag": "court_decree_resolved"}, effects=[{"set_flag": {"flag": "court_decree_resolved", "value": True}}, {"set_flag": {"flag": "court_decree_martialed", "value": True}}, {"modify_reputation": {"faction": "justiciars", "value": 25}}, {"log_event": "You passed the martial security decree."}], result_text="High Justiciars salute as martial orders take effect."),
            Action(id="court_decree_end_veto", label="Tear the decree", category="interaction", condition={"flag_is": {"flag": "court_nobles_swayed", "value": True}, "lacks_flag": "court_decree_resolved"}, effects=[{"set_flag": {"flag": "court_decree_resolved", "value": True}}, {"set_flag": {"flag": "court_decree_vetoed", "value": True}}, {"log_event": "You tore up the royal edict before the judges."}], result_text="Uproar fills the hall as the council dissolves in deadlock."),
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
        entities=[
            {'id': 'high_court_grand_basilica_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_grand_basilica_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="high_court_grand_basilica_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="high_court_grand_basilica_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'high_court_grand_basilica_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'high_court_grand_basilica_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_grand_basilica_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="high_court_grand_basilica_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="high_court_grand_basilica_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'high_court_grand_basilica_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="high_court_grand_basilica_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="high_court_grand_basilica_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="high_court_grand_basilica_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'high_court_grand_basilica_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'high_court_grand_basilica_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_grand_basilica_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="high_court_grand_basilica_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="high_court_grand_basilica_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'high_court_grand_basilica_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="high_court_grand_basilica_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="high_court_grand_basilica_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="high_court_grand_basilica_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'high_court_grand_basilica_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'high_court_grand_basilica_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_grand_basilica_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="high_court_grand_basilica_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="high_court_grand_basilica_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'high_court_grand_basilica_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="high_court_grand_basilica_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="high_court_grand_basilica_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="high_court_grand_basilica_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'high_court_grand_basilica_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="high_court_grand_basilica_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="high_court_grand_basilica_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="high_court_grand_basilica_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'high_court_grand_basilica_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="high_court_grand_basilica_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="high_court_grand_basilica_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="high_court_grand_basilica_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'high_court_grand_basilica_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'high_court_grand_basilica_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_grand_basilica_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="high_court_grand_basilica_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="high_court_grand_basilica_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'high_court_grand_basilica_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="high_court_grand_basilica_vault_to_prev", label="Return back", category="movement", target_scene="high_court_grand_basilica_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_grand_basilica_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_grand_basilica", label="Visit Grand Basilica", category="movement", target_scene="high_court_grand_basilica_gate", result_text="You travel to The Grand Basilica.")
    )

    # POI: Hall of Justiciars (10 nodes)
    # Encounter 7 - Stage 1: Assessment / Approach
    scenes["high_court_justiciar_hall_gate"] = SceneNode(
        id="high_court_justiciar_hall_gate",
        title="Hall of Justiciars - Bailiff Court",
        region="high_court",
        description="Polished white marble arches rise above solemn clerks. Armed palatines in polished steel stand guard before the high courtroom doors.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"background_is": "noble_exile"},
                text="The court bailiff recognizes the signet of your noble house."
            ),
            DynamicDescription(
                condition={"has_trait": "skeptical"},
                text="You spot the prosecutor concealing altered court depositions."
            ),
        ],
        entities=[
            {"id": "high_court_grille", "name": "Court Grille", "tags": ["lockable"], "initial_state": "locked"},
            {"id": "high_court_scribes_desk", "name": "Scribes Desk", "tags": ["flammable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="high_justiciar_read_docket", label="Inspect court docket", category="interaction", result_text="You scan the list of pending treason trials."),
            Action(id="high_justiciar_present_writ", label="Present sealed writ", category="item_affordance", condition={"has_item": "legal_dossier"}, target_scene="high_court_justiciar_hall_courtyard", result_text="The head bailiff examines the wax seal and bows you in."),
            Action(id="high_justiciar_plead_standing", label="Demand legal standing", category="social", condition={"min_skill": {"skill": "rhetoric", "value": 3}}, target_scene="high_court_justiciar_hall_courtyard", result_text="Your commanding legal rhetoric compels the guards to open the doors."),
            Action(id="high_court_justiciar_hall_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_gate_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_courtyard", result_text="You press on to the next area."),
        ]
    )

    # Encounter 7 - Stage 2: Engagement / Climax
    scenes["high_court_justiciar_hall_courtyard"] = SceneNode(
        id="high_court_justiciar_hall_courtyard",
        title="Hall of Justiciars - The Tribunal Bar",
        region="high_court",
        description="Three masked judges sit on a high cedar bench. A harsh clerk reads charges against a merchant.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_skill": {"skill": "rhetoric", "value": 4}},
                text="You identify fatal logical contradictions in the prosecutor plea."
            ),
        ],
        entities=[
            {"id": "high_court_evidence_chest", "name": "Evidence Chest", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="high_justiciar_object_plea", label="Object to evidence", category="social", condition={"min_skill": {"skill": "rhetoric", "value": 4}}, effects=[{"set_flag": {"flag": "court_verdict_won", "value": True}}, {"modify_reputation": {"faction": "justiciars", "value": 20}}, {"log_event": "You dismantled the false accusations before the magisters."}], target_scene="high_court_justiciar_hall_quarters", result_text="The chief magister silences the prosecutor with a sharp rap of his gavel."),
            Action(id="high_justiciar_bribe_magister", label="Expose forged papers", category="trait_exploit", condition={"min_skill": {"skill": "cunning", "value": 3}}, effects=[{"set_flag": {"flag": "court_verdict_won", "value": True}}, {"log_event": "You revealed the forged watermarks on the state evidence."}], target_scene="high_court_justiciar_hall_quarters", result_text="The magisters dismiss the indictment and praise your vigilance."),
            Action(id="high_court_justiciar_hall_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_gate", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_quarters", result_text="You press on to the next area."),
        ]
    )

    # Encounter 7 - Stage 3: Resolution / Consequences
    scenes["high_court_justiciar_hall_quarters"] = SceneNode(
        id="high_court_justiciar_hall_quarters",
        title="Hall of Justiciars - Arch-Justiciar Bench",
        region="high_court",
        description="Guards lead the silent clerk away. Sunlight shines on stone scales above the judge bench.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"flag_is": {"flag": "court_verdict_won", "value": True}},
                text="The chief magister signs an authoritative judicial pardon."
            ),
        ],
        entities=[
            {"id": "high_court_bench_dais", "name": "Magister Bench", "tags": ["flammable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="high_justiciar_take_seal", label="Take judicial seal", category="interaction", condition={"flag_is": {"flag": "court_verdict_won", "value": True}, "lacks_flag": "court_seal_taken"}, effects=[{"add_item": "arch_justiciar_seal"}, {"set_flag": {"flag": "court_seal_taken", "value": True}}, {"add_marker": "court_advocate"}, {"log_event": "You received the official Arch-Justiciar seal of advocacy."}], result_text="The chief clerk stamps your warrant of exoneration."),
            Action(id="high_justiciar_review_statutes", label="Study legal statutes", category="interaction", result_text="You browse the ancient leather volumes of imperial law."),
            Action(id="high_court_justiciar_hall_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_justiciar_hall_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_justiciar_hall_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_justiciar_hall_armory", result_text="You press on to the supply depot."),
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
        entities=[
            {'id': 'high_court_justiciar_hall_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_justiciar_hall_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="high_court_justiciar_hall_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="high_court_justiciar_hall_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'high_court_justiciar_hall_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="high_court_justiciar_hall_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="high_court_justiciar_hall_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="high_court_justiciar_hall_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'high_court_justiciar_hall_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'high_court_justiciar_hall_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_justiciar_hall_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="high_court_justiciar_hall_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="high_court_justiciar_hall_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'high_court_justiciar_hall_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="high_court_justiciar_hall_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="high_court_justiciar_hall_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="high_court_justiciar_hall_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'high_court_justiciar_hall_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="high_court_justiciar_hall_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="high_court_justiciar_hall_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="high_court_justiciar_hall_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'high_court_justiciar_hall_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="high_court_justiciar_hall_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="high_court_justiciar_hall_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="high_court_justiciar_hall_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'high_court_justiciar_hall_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'high_court_justiciar_hall_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_justiciar_hall_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="high_court_justiciar_hall_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="high_court_justiciar_hall_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'high_court_justiciar_hall_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        entities=[
            {'id': 'high_court_royal_archive_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_royal_archive_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="high_court_royal_archive_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="high_court_royal_archive_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'high_court_royal_archive_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'high_court_royal_archive_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_royal_archive_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="high_court_royal_archive_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="high_court_royal_archive_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'high_court_royal_archive_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="high_court_royal_archive_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="high_court_royal_archive_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="high_court_royal_archive_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'high_court_royal_archive_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'high_court_royal_archive_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_royal_archive_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="high_court_royal_archive_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="high_court_royal_archive_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'high_court_royal_archive_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="high_court_royal_archive_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="high_court_royal_archive_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="high_court_royal_archive_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'high_court_royal_archive_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'high_court_royal_archive_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_royal_archive_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="high_court_royal_archive_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="high_court_royal_archive_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'high_court_royal_archive_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="high_court_royal_archive_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="high_court_royal_archive_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="high_court_royal_archive_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'high_court_royal_archive_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="high_court_royal_archive_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="high_court_royal_archive_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="high_court_royal_archive_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'high_court_royal_archive_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="high_court_royal_archive_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="high_court_royal_archive_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="high_court_royal_archive_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'high_court_royal_archive_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'high_court_royal_archive_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_royal_archive_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="high_court_royal_archive_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="high_court_royal_archive_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'high_court_royal_archive_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="court_intercept_edict", label="Read secret edict", category="interaction", condition={"lacks_flag": "court_decree_intercepted"}, effects=[{"set_flag": {"flag": "court_decree_intercepted", "value": True}}, {"log_event": "You studied the draft of the imperial decree."}], result_text="You read the sealed parchment outlining emergency levies."),
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
        entities=[
            {'id': 'high_court_chancellor_court_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_chancellor_court_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="high_court_chancellor_court_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="high_court_chancellor_court_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'high_court_chancellor_court_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'high_court_chancellor_court_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_chancellor_court_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="high_court_chancellor_court_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="high_court_chancellor_court_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'high_court_chancellor_court_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="high_court_chancellor_court_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="high_court_chancellor_court_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="high_court_chancellor_court_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'high_court_chancellor_court_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'high_court_chancellor_court_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_chancellor_court_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="high_court_chancellor_court_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="high_court_chancellor_court_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'high_court_chancellor_court_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="high_court_chancellor_court_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="high_court_chancellor_court_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="high_court_chancellor_court_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'high_court_chancellor_court_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'high_court_chancellor_court_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_chancellor_court_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="high_court_chancellor_court_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="high_court_chancellor_court_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'high_court_chancellor_court_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="high_court_chancellor_court_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="high_court_chancellor_court_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="high_court_chancellor_court_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'high_court_chancellor_court_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="high_court_chancellor_court_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="high_court_chancellor_court_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="high_court_chancellor_court_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'high_court_chancellor_court_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="high_court_chancellor_court_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="high_court_chancellor_court_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="high_court_chancellor_court_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'high_court_chancellor_court_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'high_court_chancellor_court_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_chancellor_court_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="high_court_chancellor_court_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="high_court_chancellor_court_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'high_court_chancellor_court_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        entities=[
            {'id': 'high_court_knight_barracks_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_knight_barracks_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="high_court_knight_barracks_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="high_court_knight_barracks_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'high_court_knight_barracks_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'high_court_knight_barracks_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_knight_barracks_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="high_court_knight_barracks_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="high_court_knight_barracks_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'high_court_knight_barracks_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="high_court_knight_barracks_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="high_court_knight_barracks_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="high_court_knight_barracks_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'high_court_knight_barracks_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'high_court_knight_barracks_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_knight_barracks_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="high_court_knight_barracks_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="high_court_knight_barracks_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'high_court_knight_barracks_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="high_court_knight_barracks_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="high_court_knight_barracks_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="high_court_knight_barracks_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'high_court_knight_barracks_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'high_court_knight_barracks_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_knight_barracks_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="high_court_knight_barracks_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="high_court_knight_barracks_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'high_court_knight_barracks_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="high_court_knight_barracks_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="high_court_knight_barracks_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="high_court_knight_barracks_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'high_court_knight_barracks_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="high_court_knight_barracks_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="high_court_knight_barracks_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="high_court_knight_barracks_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'high_court_knight_barracks_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="high_court_knight_barracks_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="high_court_knight_barracks_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="high_court_knight_barracks_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'high_court_knight_barracks_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'high_court_knight_barracks_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_knight_barracks_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="high_court_knight_barracks_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="high_court_knight_barracks_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'high_court_knight_barracks_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        entities=[
            {'id': 'high_court_catacomb_kings_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_catacomb_kings_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="high_court_catacomb_kings_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="high_court_catacomb_kings_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'high_court_catacomb_kings_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'high_court_catacomb_kings_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_catacomb_kings_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="high_court_catacomb_kings_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="high_court_catacomb_kings_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'high_court_catacomb_kings_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="high_court_catacomb_kings_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="high_court_catacomb_kings_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="high_court_catacomb_kings_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'high_court_catacomb_kings_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'high_court_catacomb_kings_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_catacomb_kings_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="high_court_catacomb_kings_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="high_court_catacomb_kings_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'high_court_catacomb_kings_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="high_court_catacomb_kings_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="high_court_catacomb_kings_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="high_court_catacomb_kings_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'high_court_catacomb_kings_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'high_court_catacomb_kings_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_catacomb_kings_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="high_court_catacomb_kings_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="high_court_catacomb_kings_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'high_court_catacomb_kings_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="high_court_catacomb_kings_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="high_court_catacomb_kings_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="high_court_catacomb_kings_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'high_court_catacomb_kings_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="high_court_catacomb_kings_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="high_court_catacomb_kings_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="high_court_catacomb_kings_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'high_court_catacomb_kings_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="high_court_catacomb_kings_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="high_court_catacomb_kings_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="high_court_catacomb_kings_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'high_court_catacomb_kings_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'high_court_catacomb_kings_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_catacomb_kings_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="high_court_catacomb_kings_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="high_court_catacomb_kings_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'high_court_catacomb_kings_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        entities=[
            {'id': 'high_court_high_spire_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_high_spire_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="high_court_high_spire_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="high_court_high_spire_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'high_court_high_spire_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'high_court_high_spire_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_high_spire_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="high_court_high_spire_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="high_court_high_spire_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'high_court_high_spire_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="high_court_high_spire_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="high_court_high_spire_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="high_court_high_spire_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'high_court_high_spire_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'high_court_high_spire_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_high_spire_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="high_court_high_spire_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="high_court_high_spire_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'high_court_high_spire_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="high_court_high_spire_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="high_court_high_spire_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="high_court_high_spire_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'high_court_high_spire_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'high_court_high_spire_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_high_spire_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="high_court_high_spire_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="high_court_high_spire_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'high_court_high_spire_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="high_court_high_spire_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="high_court_high_spire_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="high_court_high_spire_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'high_court_high_spire_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="high_court_high_spire_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="high_court_high_spire_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="high_court_high_spire_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'high_court_high_spire_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="high_court_high_spire_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="high_court_high_spire_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="high_court_high_spire_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'high_court_high_spire_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'high_court_high_spire_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_high_spire_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="high_court_high_spire_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="high_court_high_spire_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'high_court_high_spire_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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
        entities=[
            {'id': 'high_court_herald_chamber_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_herald_chamber_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="high_court_herald_chamber_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="high_court_herald_chamber_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'high_court_herald_chamber_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'high_court_herald_chamber_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_herald_chamber_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="high_court_herald_chamber_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="high_court_herald_chamber_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'high_court_herald_chamber_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="high_court_herald_chamber_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="high_court_herald_chamber_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="high_court_herald_chamber_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'high_court_herald_chamber_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'high_court_herald_chamber_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_herald_chamber_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="high_court_herald_chamber_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="high_court_herald_chamber_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'high_court_herald_chamber_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="high_court_herald_chamber_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="high_court_herald_chamber_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="high_court_herald_chamber_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'high_court_herald_chamber_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'high_court_herald_chamber_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_herald_chamber_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="high_court_herald_chamber_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="high_court_herald_chamber_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'high_court_herald_chamber_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="high_court_herald_chamber_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="high_court_herald_chamber_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="high_court_herald_chamber_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'high_court_herald_chamber_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="high_court_herald_chamber_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="high_court_herald_chamber_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="high_court_herald_chamber_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'high_court_herald_chamber_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="high_court_herald_chamber_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="high_court_herald_chamber_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="high_court_herald_chamber_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'high_court_herald_chamber_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'high_court_herald_chamber_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_herald_chamber_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="high_court_herald_chamber_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="high_court_herald_chamber_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'high_court_herald_chamber_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="high_court_herald_chamber_vault_to_prev", label="Return back", category="movement", target_scene="high_court_herald_chamber_sanctum", result_text="You retrace your steps."),
            Action(id="high_court_herald_chamber_vault_to_hub", label="Return to Hub", category="movement", target_scene="high_court_hub", result_text="You return victorious to the hub."),
        ]
    )

    scenes["high_court_hub"].base_actions.append(
        Action(id="high_court_hub_to_herald_chamber", label="Visit Herald Offic", category="movement", target_scene="high_court_herald_chamber_gate", result_text="You travel to Herald Office.")
    )

    # POI: Ambassador Salon (10 nodes)
    # Encounter 8 - Stage 1: Assessment / Approach
    scenes["high_court_diplomat_lounge_gate"] = SceneNode(
        id="high_court_diplomat_lounge_gate",
        title="Ambassador Salon - Velvet Colonnade",
        region="high_court",
        description="Soft lute music floats through velvet curtains. Highborn guests sip plum wine in opulent gilded alcoves. Foreign Envoy Laurent holds court.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"background_is": "noble_exile"},
                text="Courtiers whisper your ancestral name with hushed curiosity."
            ),
        ],
        entities=[
            {"id": "high_court_salon_secretaire", "name": "Inlaid Secretaire", "tags": ["lockable"], "initial_state": "locked"},
            {"id": "high_court_silk_tapestry", "name": "Silk Drapery", "tags": ["flammable"], "initial_state": "intact"},
        ],
        base_actions=[
            Action(id="high_salon_mingle_guests", label="Mingle with guests", category="interaction", result_text="You chat casually with titled dignitaries."),
            Action(id="high_salon_offer_toast", label="Offer court toast", category="social", condition={"min_skill": {"skill": "rhetoric", "value": 3}}, target_scene="high_court_diplomat_lounge_courtyard", result_text="Your refined manners catch the eye of Envoy Laurent."),
            Action(id="high_salon_slip_balcony", label="Step to balcony", category="trait_exploit", condition={"min_skill": {"skill": "stealth", "value": 3}}, target_scene="high_court_diplomat_lounge_courtyard", result_text="You step past the heavy drapery onto the private terrace."),
            Action(id="high_court_diplomat_lounge_gate_to_prev", label="Return back", category="movement", target_scene="high_court_hub", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_gate_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_courtyard", result_text="You press on to the next area."),
        ]
    )

    # Encounter 8 - Stage 2: Engagement / Climax
    scenes["high_court_diplomat_lounge_courtyard"] = SceneNode(
        id="high_court_diplomat_lounge_courtyard",
        title="Ambassador Salon - Secluded Balcony",
        region="high_court",
        description="Night air chills the marble terrace. Envoy Laurent leans against the balustrade, swirling wine in a crystal goblet.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"has_trait": "skeptical"},
                text="You notice Laurent bodyguard hidden in the terrace shadows."
            ),
        ],
        entities=[
            {"id": "high_court_terrace_balustrade", "name": "Stone Balustrade", "tags": ["climbable"], "climb_destination": "high_court_diplomat_lounge_quarters"},
        ],
        base_actions=[
            Action(id="high_salon_parley_laurent", label="Probe Laurent motive", category="social", condition={"min_skill": {"skill": "cunning", "value": 3}}, effects=[{"set_flag": {"flag": "envoy_deal_made", "value": True}}, {"modify_reputation": {"faction": "royal_court", "value": 20}}, {"log_event": "You negotiated a clandestine pact with Envoy Laurent."}], target_scene="high_court_diplomat_lounge_quarters", result_text="Laurent smiles and reveals his diplomatic cipher key."),
            Action(id="high_salon_blackmail_envoy", label="Blackmail the envoy", category="trait_exploit", condition={"min_skill": {"skill": "rhetoric", "value": 4}}, effects=[{"set_flag": {"flag": "envoy_deal_made", "value": True}}, {"log_event": "You blackmailed Laurent into compliance."}], target_scene="high_court_diplomat_lounge_quarters", result_text="Laurent pales and capitulates to your demands."),
            Action(id="high_court_diplomat_lounge_courtyard_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_gate", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_courtyard_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_quarters", result_text="You press on to the next area."),
        ]
    )

    # Encounter 8 - Stage 3: Resolution / Consequences
    scenes["high_court_diplomat_lounge_quarters"] = SceneNode(
        id="high_court_diplomat_lounge_quarters",
        title="Ambassador Salon - Private Cabinet",
        region="high_court",
        description="A quiet wood study looks over dark gardens. Red wax seals sit beside a book on the oak desk.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"flag_is": {"flag": "envoy_deal_made", "value": True}},
                text="The envoy diplomatic cipher sits unguarded upon the desk."
            ),
        ],
        entities=[
            {"id": "high_court_mahogany_desk", "name": "Mahogany Desk", "tags": ["lockable"], "initial_state": "locked"},
        ],
        base_actions=[
            Action(id="high_salon_take_cipher", label="Take cipher key", category="interaction", condition={"flag_is": {"flag": "envoy_deal_made", "value": True}, "lacks_flag": "cipher_key_taken"}, effects=[{"add_item": "royal_cipher_key"}, {"set_flag": {"flag": "cipher_key_taken", "value": True}}, {"log_event": "You acquired the royal diplomatic cipher key."}], result_text="You pocket the carved ivory cipher key."),
            Action(id="high_salon_inspect_gardens", label="Gaze over gardens", category="interaction", result_text="You look over manicured hedge mazes beneath the stars."),
            Action(id="high_court_diplomat_lounge_quarters_to_prev", label="Return back", category="movement", target_scene="high_court_diplomat_lounge_courtyard", result_text="You retrace your steps."),
            Action(id="high_court_diplomat_lounge_quarters_to_next", label="Press forward", category="movement", target_scene="high_court_diplomat_lounge_armory", result_text="You press on to the supply depot."),
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
        entities=[
            {'id': 'high_court_diplomat_lounge_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_diplomat_lounge_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="high_court_diplomat_lounge_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="high_court_diplomat_lounge_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'high_court_diplomat_lounge_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="high_court_diplomat_lounge_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="high_court_diplomat_lounge_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="high_court_diplomat_lounge_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'high_court_diplomat_lounge_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'high_court_diplomat_lounge_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_diplomat_lounge_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="high_court_diplomat_lounge_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="high_court_diplomat_lounge_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'high_court_diplomat_lounge_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="high_court_diplomat_lounge_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="high_court_diplomat_lounge_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="high_court_diplomat_lounge_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'high_court_diplomat_lounge_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="high_court_diplomat_lounge_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="high_court_diplomat_lounge_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="high_court_diplomat_lounge_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'high_court_diplomat_lounge_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="high_court_diplomat_lounge_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="high_court_diplomat_lounge_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="high_court_diplomat_lounge_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'high_court_diplomat_lounge_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'high_court_diplomat_lounge_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_diplomat_lounge_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="high_court_diplomat_lounge_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="high_court_diplomat_lounge_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'high_court_diplomat_lounge_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
            Action(id="court_sway_nobles", label="Lobby the envoys", category="interaction", condition={"flag_is": {"flag": "court_decree_intercepted", "value": True}, "lacks_flag": "court_nobles_swayed"}, effects=[{"set_flag": {"flag": "court_nobles_swayed", "value": True}}, {"log_event": "You persuaded foreign ambassadors to back your vote."}], result_text="The visiting dignitaries pledge their votes to your faction."),
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
        entities=[
            {'id': 'high_court_silver_vault_gate_grate', 'name': 'Iron Grate', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_silver_vault_gate_act_0", label="Inspect gate", category="interaction", result_text="You carefully inspect the heavy entrance."),
            Action(id="high_court_silver_vault_gate_act_1", label="Check locks", category="interaction", result_text="You proceed to inspect the lock mechanism."),
            Action(id="high_court_silver_vault_gate_act_2", label="Inspect hinges", category="interaction", effects=[{'set_flag': {'flag': 'high_court_silver_vault_gate_hinges_checked', 'value': True}}, {'log_event': 'You checked the iron hinges.'}], result_text="You inspect the reinforced iron hinges."),
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
        entities=[
            {'id': 'high_court_silver_vault_courtyard_hay_cart', 'name': 'Hay Cart', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_silver_vault_courtyard_act_0", label="Search yard", category="interaction", result_text="You carefully search the courtyard perimeter."),
            Action(id="high_court_silver_vault_courtyard_act_1", label="Survey area", category="interaction", result_text="You proceed to survey the open ground."),
            Action(id="high_court_silver_vault_courtyard_act_2", label="Inspect cart", category="interaction", effects=[{'set_flag': {'flag': 'high_court_silver_vault_courtyard_cart_checked', 'value': True}}, {'log_event': 'You checked the supply cart.'}], result_text="You search the weathered wagon bed."),
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
            Action(id="high_court_silver_vault_quarters_act_0", label="Search bunks", category="interaction", result_text="You carefully search beneath the rough bunks."),
            Action(id="high_court_silver_vault_quarters_act_1", label="Rest briefly", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to catch your breath."),
            Action(id="high_court_silver_vault_quarters_act_2", label="Search footlocker", category="interaction", effects=[{'set_flag': {'flag': 'high_court_silver_vault_quarters_footlocker_searched', 'value': True}}, {'log_event': 'You searched the barracks footlocker.'}], result_text="You search through a wooden footlocker."),
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
        entities=[
            {'id': 'high_court_silver_vault_armory_supply_chest', 'name': 'Supply Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_silver_vault_armory_act_0", label="Inspect supplies", category="interaction", result_text="You carefully inventory the stacked rations."),
            Action(id="high_court_silver_vault_armory_act_1", label="Take provisions", category="interaction", effects=[{'modify_stamina': 2}, {'log_event': 'You gathered emergency trail rations.'}], result_text="You proceed to gather field rations."),
            Action(id="high_court_silver_vault_armory_act_2", label="Inspect weapon rack", category="interaction", effects=[{'set_flag': {'flag': 'high_court_silver_vault_armory_weapons_checked', 'value': True}}, {'log_event': 'You inspected the weapon racks.'}], result_text="You inspect the blunted training blades."),
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
            Action(id="high_court_silver_vault_cellar_act_0", label="Check barrels", category="interaction", result_text="You carefully inspect the wooden casks."),
            Action(id="high_court_silver_vault_cellar_act_1", label="Search crates", category="interaction", result_text="You proceed to pry open packing crates."),
            Action(id="high_court_silver_vault_cellar_act_2", label="Inspect cask", category="interaction", effects=[{'set_flag': {'flag': 'high_court_silver_vault_cellar_cask_checked', 'value': True}}, {'log_event': 'You inspected the storage barrels.'}], result_text="You inspect the aged storage barrels."),
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
        entities=[
            {'id': 'high_court_silver_vault_passage_brazier', 'name': 'Wall Brazier', 'tags': ['flammable'], 'initial_state': 'intact'},
        ],
        base_actions=[
            Action(id="high_court_silver_vault_passage_act_0", label="Check walls", category="interaction", result_text="You carefully check masonry for hidden seams."),
            Action(id="high_court_silver_vault_passage_act_1", label="Search floor", category="interaction", result_text="You proceed to look for tripwires on the flagstones."),
            Action(id="high_court_silver_vault_passage_act_2", label="Inspect sconce", category="interaction", effects=[{'set_flag': {'flag': 'high_court_silver_vault_passage_sconce_adjusted', 'value': True}}, {'log_event': 'You adjusted the wall sconce.'}], result_text="You adjust the flickering tallow torch."),
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
            Action(id="high_court_silver_vault_chamber_act_0", label="Examine desk", category="interaction", result_text="You carefully inspect the carved desk drawers."),
            Action(id="high_court_silver_vault_chamber_act_1", label="Read ledger", category="interaction", result_text="You proceed to scan recent accounting entries."),
            Action(id="high_court_silver_vault_chamber_act_2", label="Study road map", category="interaction", effects=[{'set_flag': {'flag': 'high_court_silver_vault_chamber_map_studied', 'value': True}}, {'log_event': 'You studied the regional map.'}], result_text="You examine the regional road map."),
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
            Action(id="high_court_silver_vault_overlook_act_0", label="Scout terrain", category="interaction", result_text="You carefully scan terrain features below."),
            Action(id="high_court_silver_vault_overlook_act_1", label="Watch horizon", category="interaction", result_text="You proceed to monitor distant movement."),
            Action(id="high_court_silver_vault_overlook_act_2", label="Study approach road", category="interaction", effects=[{'set_flag': {'flag': 'high_court_silver_vault_overlook_road_scouted', 'value': True}}, {'log_event': 'You scouted the approach road.'}], result_text="You study the winding approach road."),
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
            Action(id="high_court_silver_vault_sanctum_act_0", label="Examine altar", category="interaction", result_text="You carefully inspect religious engravings."),
            Action(id="high_court_silver_vault_sanctum_act_1", label="Offer prayer", category="interaction", effects=[{'modify_stamina': 1}], result_text="You proceed to speak a silent devotion."),
            Action(id="high_court_silver_vault_sanctum_act_2", label="Light candle", category="interaction", effects=[{'set_flag': {'flag': 'high_court_silver_vault_sanctum_candle_lit', 'value': True}}, {'log_event': 'A quiet moment of calm restores focus.'}], result_text="You light a small clay votive candle."),
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
        entities=[
            {'id': 'high_court_silver_vault_vault_iron_chest', 'name': 'Iron Chest', 'tags': ['lockable'], 'initial_state': 'locked'},
        ],
        base_actions=[
            Action(id="high_court_silver_vault_vault_act_0", label="Inspect chests", category="interaction", result_text="You carefully examine the iron chest bands."),
            Action(id="high_court_silver_vault_vault_act_1", label="Search shadows", category="interaction", result_text="You proceed to search deep corner recesses."),
            Action(id="high_court_silver_vault_vault_act_2", label="Examine lock", category="interaction", effects=[{'set_flag': {'flag': 'high_court_silver_vault_vault_lock_examined', 'value': True}}, {'log_event': 'You inspected the vault lock.'}], result_text="You inspect the heavy brass lock tumbler."),
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