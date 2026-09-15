"""Milestone 25: Continental Bestiary & Apex Trophy Hunting System.

Provides 10 Continental Apex Beasts (2 per province across 5 provinces):
1. The Reach:
   - Frost-Claw Manticore at reach_wind_hollow_sanctum
   - Iron-Spire Crag Wyrm at reach_iron_spire_sanctum
2. The Scorchwaste:
   - Dune Sand-Leviathan at scorchwaste_dune_ridge_vault
   - Ashen Glass-Stalker at scorchwaste_skiff_graveyard_vault
3. The Lowlands:
   - Mire-Maw Behemoth at lowlands_canal_sluice_cellar
   - Blackwater Gloom-Viper at lowlands_smuggler_cove_chamber
4. The High Court:
   - Gilded Crest-Chimera at high_court_high_spire_sanctum
   - Palace Shadow-Panther at high_court_knight_barracks_cellar
5. The Sunken Hollows:
   - Abyssal Trench-Kraken at sunken_hollows_abyssal_river_sanctum
   - Bioluminescent Grotto-Titan at sunken_hollows_fungal_forest_vault

Implements anatomical study, apex hunting encounters, trophy harvesting,
Menagerie trophy mounting at Central Bazaar, and Hunter Rank progression.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class ApexBeast:
    """An apex legendary creature dwelling in provincial wilderness."""
    id: str
    name: str
    title: str
    province: str
    lair_scene: str
    description: str
    weakness: str
    study_action_id: str
    study_action_label: str   # Exactly 1 to 3 words
    study_result_text: str
    hunt_action_id: str
    hunt_action_label: str    # Exactly 1 to 3 words
    hunt_result_text: str
    trophy_id: str
    trophy_name: str
    short_trophy_name: str
    trophy_perk: str
    hunt_stamina_cost: int = 8
    studied_stamina_cost: int = 4

    def to_dict(
        self,
        is_studied: bool = False,
        is_hunted: bool = False,
        is_mounted: bool = False,
        has_trophy: bool = False,
    ) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "province": self.province,
            "lair_scene": self.lair_scene,
            "description": self.description,
            "weakness": self.weakness,
            "study_action_id": self.study_action_id,
            "study_action_label": self.study_action_label,
            "hunt_action_id": self.hunt_action_id,
            "hunt_action_label": self.hunt_action_label,
            "trophy_id": self.trophy_id,
            "trophy_name": self.trophy_name,
            "short_trophy_name": self.short_trophy_name,
            "trophy_perk": self.trophy_perk,
            "is_studied": is_studied,
            "is_hunted": is_hunted,
            "is_mounted": is_mounted,
            "has_trophy": has_trophy,
        }


# --- 10 Continental Apex Beasts (2 per Province) ---

APEX_BEASTS: Dict[str, ApexBeast] = {
    # 1. The Reach
    "frost_claw_manticore": ApexBeast(
        id="frost_claw_manticore",
        name="Frost-Claw Manticore",
        title="Scourge of the Wind Hollow",
        province="The Reach",
        lair_scene="reach_wind_hollow_sanctum",
        description="A barbed manticore perches upon the windward crag. Frost cakes its iron quills.",
        weakness="Blunt impacts fracture its hollow wing joints.",
        study_action_id="bestiary_study_frost_claw",
        study_action_label="Study Frost-Claw",
        study_result_text="You note its heavy tail swings slowly. Quick thrusts to the ribcage will pierce its lungs.",
        hunt_action_id="bestiary_hunt_frost_claw",
        hunt_action_label="Hunt Frost-Claw",
        hunt_result_text="You dodge its venom quill and strike true. The manticore falls across the frozen crag.",
        trophy_id="trophy_frost_claw_talon",
        trophy_name="Frost-Claw Talon",
        short_trophy_name="Talon",
        trophy_perk="Resists arctic gales and steep crag falls.",
    ),
    "iron_crag_wyrm": ApexBeast(
        id="iron_crag_wyrm",
        name="Iron-Spire Crag Wyrm",
        title="Burrower of the Granite Peaks",
        province="The Reach",
        lair_scene="reach_iron_spire_sanctum",
        description="A giant armored wyrm coils around the stone pillar. Heavy granite plates shield its spine.",
        weakness="Sonic vibrations crack its ventral plates.",
        study_action_id="bestiary_study_crag_wyrm",
        study_action_label="Study Crag Wyrm",
        study_result_text="You track its tremor rhythm across the rock. The creature goes blind when striking from stone.",
        hunt_action_id="bestiary_hunt_crag_wyrm",
        hunt_action_label="Hunt Crag Wyrm",
        hunt_result_text="You lure the wyrm into solid granite. Your blade cleaves its soft underbelly.",
        trophy_id="trophy_crag_wyrm_scale",
        trophy_name="Crag Wyrm Scale",
        short_trophy_name="Scale",
        trophy_perk="Grants heavy armor poise and shock absorption.",
    ),

    # 2. The Scorchwaste
    "dune_sand_leviathan": ApexBeast(
        id="dune_sand_leviathan",
        name="Dune Sand-Leviathan",
        title="Terror of the Razor Ridge",
        province="The Scorchwaste",
        lair_scene="scorchwaste_dune_ridge_vault",
        description="A massive sand serpent breaches from the dunes. Burning silt sprays from its ribbed throat.",
        weakness="Water quench shocks its superheated scales.",
        study_action_id="bestiary_study_dune_leviathan",
        study_action_label="Study Dune Leviathan",
        study_result_text="You watch it emerge to breathe hot air. Its soft throat sac opens during each roar.",
        hunt_action_id="bestiary_hunt_dune_leviathan",
        hunt_action_label="Hunt Dune Leviathan",
        hunt_result_text="You plunge your spear down its throat. The leviathan thrashes and collapses into the sand.",
        trophy_id="trophy_sand_leviathan_plate",
        trophy_name="Sand Leviathan Plate",
        short_trophy_name="Plate",
        trophy_perk="Insulates against burning heat and sand friction.",
    ),
    "ashen_glass_stalker": ApexBeast(
        id="ashen_glass_stalker",
        name="Ashen Glass-Stalker",
        title="Scythe-Fiend of the Skiff Wreck",
        province="The Scorchwaste",
        lair_scene="scorchwaste_skiff_graveyard_vault",
        description="A predatory insectoid crouches beneath shattered timber. Twin obsidian scythes click in the heat.",
        weakness="Reflected glare blinds its compound eyes.",
        study_action_id="bestiary_study_glass_stalker",
        study_action_label="Study Glass-Stalker",
        study_result_text="You observe its swift reflex arcs. It hesitates whenever dust clouds obscure its sight.",
        hunt_action_id="bestiary_hunt_glass_stalker",
        hunt_action_label="Hunt Glass-Stalker",
        hunt_result_text="You shatter its leading scythe with a heavy blow. Your second strike severs its neck.",
        trophy_id="trophy_glass_stalker_scythe",
        trophy_name="Glass Stalker Scythe",
        short_trophy_name="Scythe",
        trophy_perk="Sharpens critical weapon strikes and quick dodges.",
    ),

    # 3. The Lowlands
    "mire_maw_behemoth": ApexBeast(
        id="mire_maw_behemoth",
        name="Mire-Maw Behemoth",
        title="Dredger of the Canal Sluice",
        province="The Lowlands",
        lair_scene="lowlands_canal_sluice_cellar",
        description="A swamp drake churns muddy canal water. Moss covers its tooth-lined jaws.",
        weakness="Fire sparks ignite marsh gas in its maw.",
        study_action_id="bestiary_study_mire_maw",
        study_action_label="Study Mire-Maw",
        study_result_text="You watch bubbles rise before it attacks. Its hide softens after diving into deep slime.",
        hunt_action_id="bestiary_hunt_mire_maw",
        hunt_action_label="Hunt Mire-Maw",
        hunt_result_text="You trap its massive jaws with an iron bar. Your dagger drives into its eye socket.",
        trophy_id="trophy_mire_behemoth_tusk",
        trophy_name="Mire Behemoth Tusk",
        short_trophy_name="Tusk",
        trophy_perk="Repels swamp rot and improves muddy footing.",
    ),
    "blackwater_gloom_viper": ApexBeast(
        id="blackwater_gloom_viper",
        name="Blackwater Gloom-Viper",
        title="Fang of the Smuggler Cove",
        province="The Lowlands",
        lair_scene="lowlands_smuggler_cove_chamber",
        description="A hooded sea serpent slithers through brackish pools. Thick green venom drips from hollow fangs.",
        weakness="Cold brine cools down its burning venom.",
        study_action_id="bestiary_study_gloom_viper",
        study_action_label="Study Gloom-Viper",
        study_result_text="You study its strike pattern across the water. It recoils whenever stone strikes sparks.",
        hunt_action_id="bestiary_hunt_gloom_viper",
        hunt_action_label="Hunt Gloom-Viper",
        hunt_result_text="You pin its flared hood against the damp stone. A clean cut decapitates the viper.",
        trophy_id="trophy_gloom_viper_gland",
        trophy_name="Gloom Viper Gland",
        short_trophy_name="Gland",
        trophy_perk="Wards against lethal toxins and venom strikes.",
    ),

    # 4. The High Court
    "gilded_crest_chimera": ApexBeast(
        id="gilded_crest_chimera",
        name="Gilded Crest-Chimera",
        title="Monarch of the High Spire",
        province="The High Court",
        lair_scene="high_court_high_spire_sanctum",
        description="A majestic chimera stalks the marble balcony. Golden feathers crown its leonine shoulders.",
        weakness="High piercing strikes break its wing span.",
        study_action_id="bestiary_study_gilded_chimera",
        study_action_label="Study Gilded Chimera",
        study_result_text="You examine its proud defensive stance. It favors its left flank after banking in flight.",
        hunt_action_id="bestiary_hunt_gilded_chimera",
        hunt_action_label="Hunt Gilded Chimera",
        hunt_result_text="You exploit its blind turn with a swift lunging thrust. The beast crashes onto marble tiles.",
        trophy_id="trophy_gilded_chimera_crest",
        trophy_name="Gilded Chimera Crest",
        short_trophy_name="Crest",
        trophy_perk="Inspires deep respect and steady court poise.",
    ),
    "palace_shadow_panther": ApexBeast(
        id="palace_shadow_panther",
        name="Palace Shadow-Panther",
        title="Prowler of the Knight Cellar",
        province="The High Court",
        lair_scene="high_court_knight_barracks_cellar",
        description="A sleek black feline glides through cold archways. Violet eyes track every subtle movement.",
        weakness="Lantern flares ruin its dark adaptation.",
        study_action_id="bestiary_study_shadow_panther",
        study_action_label="Study Shadow-Panther",
        study_result_text="You note its silent paw placements on stone. It prepares to pounce when ears twitch.",
        hunt_action_id="bestiary_hunt_shadow_panther",
        hunt_action_label="Hunt Shadow-Panther",
        hunt_result_text="You anticipate its pounce and counter with steel. The panther falls in the cellar dust.",
        trophy_id="trophy_shadow_panther_pelt",
        trophy_name="Shadow Panther Pelt",
        short_trophy_name="Pelt",
        trophy_perk="Silences footsteps and enhances stealth ambushes.",
    ),

    # 5. The Sunken Hollows
    "abyssal_trench_kraken": ApexBeast(
        id="abyssal_trench_kraken",
        name="Abyssal Trench-Kraken",
        title="Sovereign of the Under-River",
        province="The Sunken Hollows",
        lair_scene="sunken_hollows_abyssal_river_sanctum",
        description="Giant tentacles churn the rushing subterranean rapids. Cold suction rings grip the wet rocks.",
        weakness="Cutting its air vents drains its swimming speed.",
        study_action_id="bestiary_study_trench_kraken",
        study_action_label="Study Trench-Kraken",
        study_result_text="You track siphon pulses along its central mantle. It blinks before expelling dark cloud ink.",
        hunt_action_id="bestiary_hunt_trench_kraken",
        hunt_action_label="Hunt Trench-Kraken",
        hunt_result_text="You sever the grasping arms and puncture its mantle. The kraken drifts down into dark rapids.",
        trophy_id="trophy_trench_kraken_beak",
        trophy_name="Trench Kraken Beak",
        short_trophy_name="Beak",
        trophy_perk="Expands deep breath capacity and swim speed.",
    ),
    "bioluminescent_grotto_titan": ApexBeast(
        id="bioluminescent_grotto_titan",
        name="Bioluminescent Grotto-Titan",
        title="Crusher of the Fungal Vault",
        province="The Sunken Hollows",
        lair_scene="sunken_hollows_fungal_forest_vault",
        description="A giant armored crustacean rests among glowing fungi. Phosphor shines on its heavy shell.",
        weakness="Acid dissolves its joint cartilage.",
        study_action_id="bestiary_study_grotto_titan",
        study_action_label="Study Grotto-Titan",
        study_result_text="You analyze its slow pincer rotation. Its underbelly glows brightest right before a smash.",
        hunt_action_id="bestiary_hunt_grotto_titan",
        hunt_action_label="Hunt Grotto-Titan",
        hunt_result_text="You dodge under the heavy claw and drive inward. The glowing titan collapses into broken spores.",
        trophy_id="trophy_grotto_titan_core",
        trophy_name="Grotto Titan Core",
        short_trophy_name="Core",
        trophy_perk="Emits safe subterranean light and spore warding.",
    ),
}

LAIR_TO_BEAST: Dict[str, ApexBeast] = {
    b.lair_scene: b for b in APEX_BEASTS.values()
}


def evaluate_bestiary_progress(
    world_flags: Dict[str, Any],
    inventory: Any = None
) -> Dict[str, Any]:
    """Calculate hunted trophies, studied weaknesses, and continental hunter rank."""
    inv_set = set()
    if isinstance(inventory, (list, tuple, set)):
        inv_set = {str(i).lower() for i in inventory}
    elif isinstance(inventory, dict):
        inv_set = {str(k).lower() for k in inventory.keys()}

    hunted_ids = [bid for bid in APEX_BEASTS if world_flags.get(f"bestiary_hunted_{bid}")]
    studied_ids = [bid for bid in APEX_BEASTS if world_flags.get(f"bestiary_studied_{bid}")]
    mounted_ids = [bid for bid in APEX_BEASTS if world_flags.get(f"bestiary_mounted_{bid}")]

    hunted_count = len(hunted_ids)
    studied_count = len(studied_ids)
    mounted_count = len(mounted_ids)

    if hunted_count >= 10:
        rank_title = "👑 Continental Apex Slayer"
    elif hunted_count >= 5:
        rank_title = "⚔️ Grandmaster Hunter"
    elif hunted_count >= 3:
        rank_title = "🏹 Apex Hunter"
    elif hunted_count >= 1:
        rank_title = "🎯 Provincial Tracker"
    else:
        rank_title = "Novice Trapper"

    return {
        "hunted_count": hunted_count,
        "studied_count": studied_count,
        "mounted_count": mounted_count,
        "total_beasts": len(APEX_BEASTS),
        "rank_title": rank_title,
        "is_tracker": hunted_count >= 1,
        "is_apex_hunter": hunted_count >= 3,
        "is_grandmaster": hunted_count >= 5,
        "is_slayer": hunted_count >= 10,
        "beasts": {
            bid: b.to_dict(
                is_studied=(bid in studied_ids),
                is_hunted=(bid in hunted_ids),
                is_mounted=(bid in mounted_ids),
                has_trophy=(b.trophy_id.lower() in inv_set),
            )
            for bid, b in APEX_BEASTS.items()
        },
    }


def get_bestiary_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic bestiary affordances (Study, Hunt, Mount, Inspect)."""
    from adventure_forge.core.actions import Action
    actions: List[Action] = []

    # 1. Lair Confrontation Affordances
    beast = LAIR_TO_BEAST.get(scene_id)
    if beast:
        is_hunted = bool(world_flags.get(f"bestiary_hunted_{beast.id}"))
        is_studied = bool(world_flags.get(f"bestiary_studied_{beast.id}"))

        if not is_hunted:
            # 1a. Study Weakness
            if not is_studied:
                actions.append(Action(
                    id=beast.study_action_id,
                    label=beast.study_action_label,
                    category="bestiary",
                    effects=[
                        {"set_flag": {"flag": f"bestiary_studied_{beast.id}", "value": True}},
                        {"log_event": f"Discovered weakness of {beast.name}: {beast.weakness}"},
                    ],
                    result_text=beast.study_result_text,
                    risk="low",
                    stamina_cost=1,
                ))

            # 1b. Apex Hunt
            cost = beast.studied_stamina_cost if is_studied else beast.hunt_stamina_cost
            actions.append(Action(
                id=beast.hunt_action_id,
                label=beast.hunt_action_label,
                category="bestiary",
                effects=[
                    {"set_flag": {"flag": f"bestiary_hunted_{beast.id}", "value": True}},
                    {"add_item": beast.trophy_id},
                    {"log_event": f"Defeated {beast.name} and harvested {beast.trophy_name}."},
                ],
                result_text=beast.hunt_result_text,
                risk="high",
                stamina_cost=cost,
            ))

    # 2. Central Bazaar Trophy Hall & Menagerie (bazaar_center)
    if scene_id == "bazaar_center":
        # Check inventory defensively
        inv_set = set()
        if isinstance(character.inventory, (list, tuple, set)):
            inv_set = {str(i).lower() for i in character.inventory}
        elif isinstance(character.inventory, dict):
            inv_set = {str(k).lower() for k in character.inventory.keys()}

        # Affordances to mount unmounted trophies in inventory
        for bid, b in APEX_BEASTS.items():
            if b.trophy_id.lower() in inv_set and not world_flags.get(f"bestiary_mounted_{bid}"):
                actions.append(Action(
                    id=f"bestiary_mount_{bid}",
                    label=f"Mount {b.short_trophy_name}",
                    category="bestiary",
                    effects=[
                        {"remove_item": b.trophy_id},
                        {"set_flag": {"flag": f"bestiary_mounted_{bid}", "value": True}},
                        {"log_event": f"Mounted {b.trophy_name} in the Central Menagerie."},
                    ],
                    result_text="The curator mounts the trophy on stone. Crowds nod with quiet respect.",
                    risk="low",
                    stamina_cost=0,
                ))

        # Inspect Menagerie
        actions.append(Action(
            id="bestiary_inspect_menagerie",
            label="Inspect Menagerie",
            category="bestiary",
            effects=[
                {"log_event": "You toured the preserved apex specimens in the Grand Menagerie."},
            ],
            result_text="Carved stone displays preserved apex beasts. Guards watch the mounted specimens.",
            risk="low",
            stamina_cost=0,
        ))

    return actions
