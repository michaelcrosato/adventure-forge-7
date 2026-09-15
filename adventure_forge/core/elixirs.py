"""Milestone 32: Continental Alchemical Laboratories, Distillation Alembics & Grand Master Apothecary System.

Provides 6 Canonical Ancient Alembic Laboratories situated in regional cellars and crossroads,
7-axis apothecary affordances yielding ancient elixirs and pharmacological mastery,
dynamic field elixir imbibing, laboratory alembic refill renewals, and Continental Arch-Apothecary rank progression.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class AlembicLab:
    """A continental ancient alchemical laboratory with dedicated cellar scene, distillation alembic, and retort."""
    id: str
    name: str
    province: str
    lab_scene: str
    icon: str
    elixir_name: str
    domain: str
    description: str
    distill_action_id: str
    distill_action_label: str       # Exactly 1 to 3 words
    distill_result_text: str
    elixir_marker: str
    mastery_marker: str
    imbibe_action_id: str
    imbibe_action_label: str        # Exactly 1 to 3 words
    imbibe_result_text: str
    refill_action_id: str
    refill_action_label: str        # Exactly 1 to 3 words
    refill_result_text: str
    required_tool: str
    alternate_attribute: str
    alternate_attr_val: int
    alternate_trait: str

    def to_dict(
        self,
        is_distilled: bool = False,
        has_elixir: bool = False,
        is_imbibed: bool = False,
        has_mastery: bool = False,
    ) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "lab_scene": self.lab_scene,
            "icon": self.icon,
            "elixir_name": self.elixir_name,
            "domain": self.domain,
            "description": self.description,
            "distill_action_id": self.distill_action_id,
            "distill_action_label": self.distill_action_label,
            "elixir_marker": self.elixir_marker,
            "mastery_marker": self.mastery_marker,
            "imbibe_action_id": self.imbibe_action_id,
            "imbibe_action_label": self.imbibe_action_label,
            "refill_action_id": self.refill_action_id,
            "refill_action_label": self.refill_action_label,
            "required_tool": self.required_tool,
            "alternate_attribute": self.alternate_attribute,
            "alternate_attr_val": self.alternate_attr_val,
            "alternate_trait": self.alternate_trait,
            "is_distilled": is_distilled,
            "has_elixir": has_elixir,
            "is_imbibed": is_imbibed,
            "has_mastery": has_mastery,
        }


# 6 Canonical Continental Alchemical Laboratories
ANCIENT_ALEMBICS: Dict[str, AlembicLab] = {
    "alembic_frostbane": AlembicLab(
        id="alembic_frostbane",
        name="Glacial Distillation Alembic",
        province="The Reach",
        lab_scene="reach_high_pass_cellar",
        icon="❄️",
        elixir_name="Frostbane Phial",
        domain="Alpine Cryo-Distillation & Frostbite Salves",
        description="Glacial drafts chill the stone laboratory. Cold condensation coats the long copper coil.",
        distill_action_id="elixir_distill_frostbane",
        distill_action_label="Distill Frostbane Phial",
        distill_result_text="You extract pure alpine essence into the crystal phial. Cool glacial vapors fortify your breathing.",
        elixir_marker="marker_elixir_frostbane",
        mastery_marker="marker_elixir_mastery_reach",
        imbibe_action_id="elixir_imbibe_frostbane",
        imbibe_action_label="Imbibe Frostbane Phial",
        imbibe_result_text="You drink the cold winter elixir with steady discipline. Alpine clarity sharpens your senses.",
        refill_action_id="elixir_refill_frostbane",
        refill_action_label="Refill Frost Alembic",
        refill_result_text="You replenish the glacial condenser with mountain ice. Fresh herbal extracts renew your travel resolve.",
        required_tool="alembic_vial",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="herbalist",
    ),
    "alembic_sunfire": AlembicLab(
        id="alembic_sunfire",
        name="Solar Essence Alembic",
        province="The Scorchwaste",
        lab_scene="scorchwaste_dune_ridge_cellar",
        icon="🔥",
        elixir_name="Sunfire Draught",
        domain="Desert Solar Distillation & Sunstroke Tonics",
        description="Warm desert sand covers the distillation bench. Rising heat warms the copper retort.",
        distill_action_id="elixir_distill_sunfire",
        distill_action_label="Distill Sunfire Draught",
        distill_result_text="You distill solar resins over burning charcoal coals. Warm aromatic vapor calms your pulse.",
        elixir_marker="marker_elixir_sunfire",
        mastery_marker="marker_elixir_mastery_scorchwaste",
        imbibe_action_id="elixir_imbibe_sunfire",
        imbibe_action_label="Imbibe Sunfire Draught",
        imbibe_result_text="You swallow the spicy golden draught with care. Heat tolerance fortifies your endurance.",
        refill_action_id="elixir_refill_sunfire",
        refill_action_label="Refill Solar Alembic",
        refill_result_text="You pack crushed desert sage into the retort. Warm aromatic steam renews your travel resolve.",
        required_tool="alembic_vial",
        alternate_attribute="endurance",
        alternate_attr_val=14,
        alternate_trait="desert_born",
    ),
    "alembic_deepglow": AlembicLab(
        id="alembic_deepglow",
        name="Bioluminescent Tidal Alembic",
        province="The Sunken Hollows",
        lab_scene="sunken_hollows_glow_grotto_cellar",
        icon="💧",
        elixir_name="Deepglow Tincture",
        domain="Abyssal Extraction & Deep-Pressure Tonics",
        description="Glowing algae illuminates the damp cavern still. Saltwater droplets drip from the copper spout.",
        distill_action_id="elixir_distill_deepglow",
        distill_action_label="Distill Deepglow Tincture",
        distill_result_text="You filter glowing abyssal algae through tidal charcoal. Glowing blue liquid fills your vial.",
        elixir_marker="marker_elixir_deepglow",
        mastery_marker="marker_elixir_mastery_sunken",
        imbibe_action_id="elixir_imbibe_deepglow",
        imbibe_action_label="Imbibe Deepglow Tincture",
        imbibe_result_text="You drink the glowing azure tincture with calm focus. Abyssal stamina restores your limbs.",
        refill_action_id="elixir_refill_deepglow",
        refill_action_label="Refill Tidal Alembic",
        refill_result_text="You pour fresh brine into the tidal retort. Ocean minerals renew your travel resolve.",
        required_tool="alembic_vial",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="diver",
    ),
    "alembic_courtier": AlembicLab(
        id="alembic_courtier",
        name="Palatine Ducal Apothecary",
        province="The High Court",
        lab_scene="high_court_royal_archive_cellar",
        icon="⚜️",
        elixir_name="Courtier Cordial",
        domain="Court Poison Antidotes & Polished Cordials",
        description="Polished brass instruments line marble tables. Labeled apothecary jars fill the cellar shelves.",
        distill_action_id="elixir_distill_courtier",
        distill_action_label="Distill Courtier Cordial",
        distill_result_text="You blend refined floral cordials in silver basins. Subtle aromatics mask deadly court poisons.",
        elixir_marker="marker_elixir_courtier",
        mastery_marker="marker_elixir_mastery_high_court",
        imbibe_action_id="elixir_imbibe_courtier",
        imbibe_action_label="Imbibe Courtier Cordial",
        imbibe_result_text="You sip the delicate floral cordial with grace. Poison resistance shields your system.",
        refill_action_id="elixir_refill_courtier",
        refill_action_label="Refill Ducal Alembic",
        refill_result_text="You add floral spirits to the silver retort. Sweet rosewater steam renews your travel resolve.",
        required_tool="alembic_vial",
        alternate_attribute="presence",
        alternate_attr_val=14,
        alternate_trait="diplomat",
    ),
    "alembic_marshmoss": AlembicLab(
        id="alembic_marshmoss",
        name="Saltmarsh Distillation Still",
        province="The Lowlands",
        lab_scene="lowlands_brewery_vault_cellar",
        icon="🌿",
        elixir_name="Marshmoss Panacea",
        domain="Fen Herb Fermentation & Plague Wardens",
        description="Wooden fermentation barrels line the stone cellar. Pungent peat vapors drift from bubbling copper vats.",
        distill_action_id="elixir_distill_marshmoss",
        distill_action_label="Distill Marshmoss Panacea",
        distill_result_text="You boil medicinal marshmoss into dark soothing syrup. Pungent steam wards away swamp sickness.",
        elixir_marker="marker_elixir_marshmoss",
        mastery_marker="marker_elixir_mastery_lowlands",
        imbibe_action_id="elixir_imbibe_marshmoss",
        imbibe_action_label="Imbibe Marshmoss Panacea",
        imbibe_result_text="You drink the thick bitter syrup with steady resolve. Swamplands immunity protects your blood.",
        refill_action_id="elixir_refill_marshmoss",
        refill_action_label="Refill Saltmarsh Still",
        refill_result_text="You feed dried peat under the copper alembic vat. Earthy woodsmoke renews your travel resolve.",
        required_tool="alembic_vial",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="apothecary",
    ),
    "alembic_crossroads_grand": AlembicLab(
        id="alembic_crossroads_grand",
        name="Grand Sovereign Pharmacopeia",
        province="Central Crossroads",
        lab_scene="bazaar_center",
        icon="👑",
        elixir_name="Sovereign Panacea",
        domain="Continental Pharmacopeia & Master Elixirs",
        description="Silk awnings shelter rows of glass apothecary jars. Spiced continental roots simmer in brass kettles.",
        distill_action_id="elixir_distill_crossroads_grand",
        distill_action_label="Distill Sovereign Panacea",
        distill_result_text="You blend five provincial extracts with care. Master continental balance restores your strength.",
        elixir_marker="marker_elixir_crossroads_grand",
        mastery_marker="marker_elixir_mastery_crossroads",
        imbibe_action_id="elixir_imbibe_crossroads_grand",
        imbibe_action_label="Imbibe Sovereign Panacea",
        imbibe_result_text="You swallow the master panacea with calm resolve. Five provincial blessings restore your body.",
        refill_action_id="elixir_refill_crossroads_grand",
        refill_action_label="Refill Sovereign Still",
        refill_result_text="You steep caravan spices in the copper kettle. Rich aromatic vapor renews your travel resolve.",
        required_tool="alembic_vial",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="artificer",
    ),
}

# Apothecary rank progression tiers
APOTHECARY_RANKS: List[Dict[str, Any]] = [
    {
        "count": 0,
        "title": "Novice Herbalist",
        "desc": "You hold no brewed elixirs or distilled salves. Continental alembics remain dormant in your travels.",
    },
    {
        "count": 1,
        "title": "Journeyman Brewer",
        "desc": "You have distilled your first ancient elixir. Basic apothecary knowledge guides your vials.",
    },
    {
        "count": 2,
        "title": "Tincture Craftsman",
        "desc": "Two provincial alembics yield their precious draughts. Complex herbal formulas appear clear to your eyes.",
    },
    {
        "count": 3,
        "title": "Master Alchemist",
        "desc": "Three continental alembics have been distilled with care. Tough botanical extracts yield to your craft.",
    },
    {
        "count": 4,
        "title": "Guild Toxicologist",
        "desc": "Four provincial alembics are mastered with great care. Your potion brewing craft commands high respect.",
    },
    {
        "count": 5,
        "title": "Grand Pharmacist",
        "desc": "All five provincial alembics are mastered with care. Complete botanical knowledge guides your hand.",
    },
    {
        "count": 6,
        "title": "Continental Arch-Apothecary",
        "desc": "All continental alembics are conquered with skill. Supreme potion mastery guides your craft.",
    },
]


def get_apothecary_rank(distilled_count: int) -> Dict[str, str]:
    """Determine Apothecary rank title and description from distilled alembic count."""
    best = APOTHECARY_RANKS[0]
    for tier in APOTHECARY_RANKS:
        if distilled_count >= tier["count"]:
            best = tier
    return {"title": str(best["title"]), "desc": str(best["desc"])}


def evaluate_elixirs_progress(
    flags: Dict[str, Any],
    inventory: List[str],
    markers: List[str],
    current_scene: str = ""
) -> Dict[str, Any]:
    """Deterministic evaluation of alchemical laboratories, apothecary rank, and active elixirs."""
    marker_set = {str(m).lower() for m in markers}
    distilled_count = 0
    active_elixirs_count = 0
    active_masteries_count = 0
    lab_list = []
    current_scene_lab = None

    for lab in ANCIENT_ALEMBICS.values():
        is_distilled = bool(flags.get(f"elixir_distilled_{lab.id}", False))
        has_elixir = lab.elixir_marker.lower() in marker_set
        is_imbibed = bool(flags.get(f"elixir_imbibed_{lab.id}", False))
        has_mastery = lab.mastery_marker.lower() in marker_set

        if is_distilled:
            distilled_count += 1
        if has_elixir:
            active_elixirs_count += 1
        if has_mastery:
            active_masteries_count += 1

        if current_scene == lab.lab_scene:
            current_scene_lab = lab.id

        lab_list.append(
            lab.to_dict(
                is_distilled=is_distilled,
                has_elixir=has_elixir,
                is_imbibed=is_imbibed,
                has_mastery=has_mastery,
            )
        )

    rank_info = get_apothecary_rank(distilled_count)
    progress_pct = round((distilled_count / max(1, len(ANCIENT_ALEMBICS))) * 100, 1)

    return {
        "labs": lab_list,
        "distilled_count": distilled_count,
        "total_labs": len(ANCIENT_ALEMBICS),
        "active_elixirs_count": active_elixirs_count,
        "active_masteries_count": active_masteries_count,
        "apothecary_rank": rank_info["title"],
        "rank_desc": rank_info["desc"],
        "progress_pct": progress_pct,
        "current_scene_lab": current_scene_lab,
    }


def get_elixirs_progress(state: Any) -> Dict[str, Any]:
    """Compute deterministic elixirs progress and apothecary rank from GameState."""
    flags = state.world_flags if hasattr(state, "world_flags") else getattr(state, "flags", {})
    char = getattr(state, "character", None)
    inv = getattr(char, "inventory", []) if char else []
    markers = getattr(char, "markers", []) if char else []
    current_scene = getattr(state, "current_scene", "")
    return evaluate_elixirs_progress(flags, inv, markers, current_scene)


def get_elixir_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic elixir distillation, field imbibing, and alembic refill affordances."""
    from adventure_forge.content.schema import Action

    affordances: List[Action] = []
    inv_list: List[str] = []
    marker_list: List[str] = []
    traits_list: List[str] = []
    skills_dict: Dict[str, int] = {}

    if hasattr(character, "inventory"):
        inv_list = [str(k).lower() for k in character.inventory]
    if hasattr(character, "markers"):
        marker_list = [str(k).lower() for k in character.markers]
    if hasattr(character, "traits"):
        traits_list = [str(t).lower() for t in character.traits]
    if hasattr(character, "skills"):
        skills_dict = {str(s).lower(): int(v) for s, v in character.skills.items()}

    # Generic apothecary tools that satisfy glassware requirements
    apothecary_tools = {
        "alembic_vial",
        "potion_vial",
        "item_vial",
        "glass_vial",
        "vial",
        "crystal_phial",
        "herbalist_kit",
        "alchemical_tools",
        "mortar_and_pestle",
        "apothecary_kit",
    }
    has_any_apothecary_tool = any(t in inv_list for t in apothecary_tools) or any(
        any(k in item for k in ["vial", "phial", "flask", "bottle", "alembic", "herbal", "apothecary", "mortar", "alchem"])
        for item in inv_list
    )

    # 1. Laboratory Alembic Distillations and Refills
    for lab in ANCIENT_ALEMBICS.values():
        if scene_id == lab.lab_scene:
            is_distilled = bool(world_flags.get(f"elixir_distilled_{lab.id}", False))
            is_imbibed = bool(world_flags.get(f"elixir_imbibed_{lab.id}", False))

            if not is_distilled:
                # 7-axis qualification:
                # 1. Has specific tool or generic apothecary glassware
                # 2. Has relevant traits (herbalist, apothecary, alchemist, botanist, etc.)
                # 3. Has high attribute (wits >= 14, cunning >= 14, or alternate_attr)
                # 4. Has relevant skills (cunning, lore, survival >= 2)
                # 5. Has physical stamina (stamina >= 2)
                has_tool = (lab.required_tool.lower() in inv_list) or has_any_apothecary_tool
                has_trait = (lab.alternate_trait.lower() in traits_list) or any(
                    t in traits_list
                    for t in [
                        "herbalist",
                        "apothecary",
                        "alchemist",
                        "botanist",
                        "focused",
                        "nimble",
                        "cautious",
                    ]
                )
                attr_val = character.get_attribute(lab.alternate_attribute)
                has_attr = (attr_val >= lab.alternate_attr_val) or (
                    character.get_attribute("wits") >= 14
                    or character.get_attribute("cunning") >= 14
                )
                has_skill = (
                    skills_dict.get("cunning", 0) >= 2
                    or skills_dict.get("lore", 0) >= 2
                    or skills_dict.get("survival", 0) >= 2
                )
                has_stam = getattr(character, "stamina", 0) >= 2

                if has_tool or has_trait or has_attr or has_skill or has_stam:
                    affordances.append(
                        Action(
                            id=lab.distill_action_id,
                            label=lab.distill_action_label,
                            category="exploration",
                            effects=[
                                {"set_flag": {"flag": f"elixir_distilled_{lab.id}", "value": True}},
                                {"add_marker": lab.elixir_marker},
                                {"add_marker": lab.mastery_marker},
                                {"modify_stamina": 3},
                                {"log_event": lab.distill_result_text},
                            ],
                            result_text=lab.distill_result_text,
                            risk="low",
                            stamina_cost=0,
                        )
                    )
            elif is_imbibed:
                # Can refill and replenish alembic condenser at lab scene
                affordances.append(
                    Action(
                        id=lab.refill_action_id,
                        label=lab.refill_action_label,
                        category="exploration",
                        effects=[
                            {"set_flag": {"flag": f"elixir_imbibed_{lab.id}", "value": False}},
                            {"modify_stamina": 2},
                            {"log_event": lab.refill_result_text},
                        ],
                        result_text=lab.refill_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    # 2. Field Elixir Imbibing anywhere in the continental world
    for lab in ANCIENT_ALEMBICS.values():
        if lab.elixir_marker.lower() in marker_list:
            is_imbibed = bool(world_flags.get(f"elixir_imbibed_{lab.id}", False))
            if not is_imbibed:
                affordances.append(
                    Action(
                        id=lab.imbibe_action_id,
                        label=lab.imbibe_action_label,
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": f"elixir_imbibed_{lab.id}", "value": True}},
                            {"add_marker": f"marker_imbibed_{lab.id}"},
                            {"modify_stamina": 3},
                            {"log_event": lab.imbibe_result_text},
                        ],
                        result_text=lab.imbibe_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    return affordances
