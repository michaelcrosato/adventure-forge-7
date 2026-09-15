"""Milestone 31: Continental Runeforges, Ancient Crucible Anvils & Master Artificer System.

Provides 6 Canonical Ancient Runeforges situated at regional armories and crossroads,
7-axis metalworking affordances yielding ancient runes and metallurgical mastery,
dynamic field rune tempering, crucible quenching renewals, and Continental Forgemaster rank progression.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class Runeforge:
    """A continental ancient runeforge with dedicated armory scene, runic anvil, and crucible."""
    id: str
    name: str
    province: str
    forge_scene: str
    icon: str
    rune_name: str
    domain: str
    description: str
    inscribe_action_id: str
    inscribe_action_label: str       # Exactly 1 to 3 words
    inscribe_result_text: str
    rune_marker: str
    mastery_marker: str
    temper_action_id: str
    temper_action_label: str        # Exactly 1 to 3 words
    temper_result_text: str
    quench_action_id: str
    quench_action_label: str        # Exactly 1 to 3 words
    quench_result_text: str
    required_tool: str
    alternate_attribute: str
    alternate_attr_val: int
    alternate_trait: str

    def to_dict(
        self,
        is_inscribed: bool = False,
        has_rune: bool = False,
        is_tempered: bool = False,
        has_mastery: bool = False,
    ) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "forge_scene": self.forge_scene,
            "icon": self.icon,
            "rune_name": self.rune_name,
            "domain": self.domain,
            "description": self.description,
            "inscribe_action_id": self.inscribe_action_id,
            "inscribe_action_label": self.inscribe_action_label,
            "rune_marker": self.rune_marker,
            "mastery_marker": self.mastery_marker,
            "temper_action_id": self.temper_action_id,
            "temper_action_label": self.temper_action_label,
            "quench_action_id": self.quench_action_id,
            "quench_action_label": self.quench_action_label,
            "required_tool": self.required_tool,
            "alternate_attribute": self.alternate_attribute,
            "alternate_attr_val": self.alternate_attr_val,
            "alternate_trait": self.alternate_trait,
            "is_inscribed": is_inscribed,
            "has_rune": has_rune,
            "is_tempered": is_tempered,
            "has_mastery": has_mastery,
        }


# 6 Canonical Continental Runeforges
ANCIENT_RUNEFORGES: Dict[str, Runeforge] = {
    "forge_frost_iron": Runeforge(
        id="forge_frost_iron",
        name="Glacial Frost Anvil",
        province="The Reach",
        forge_scene="reach_high_pass_armory",
        icon="❄️",
        rune_name="Glacial Frost Rune",
        domain="High Peak Cold-Forging & Titan Plates",
        description="High smelting furnaces warm the cavernous mountain workshop. Bright sparks illuminate the glacial granite floor.",
        inscribe_action_id="forge_inscribe_frost_iron",
        inscribe_action_label="Inscribe Frost Anvil",
        inscribe_result_text="You temper cold-hammered steel upon the glacial anvil. Freezing mountain winds harden your tempered resolve.",
        rune_marker="marker_rune_frost_iron",
        mastery_marker="marker_forge_mastery_reach",
        temper_action_id="forge_temper_frost_iron",
        temper_action_label="Temper Frost Rune",
        temper_result_text="You quench the glacial rune in frozen mountain snowmelt. Alpine clarity sharpens your fighting edge.",
        quench_action_id="forge_quench_frost_iron",
        quench_action_label="Quench Frost Crucible",
        quench_result_text="You submerge the glowing blade into mountain oil. Rising icy vapor renews your travel resolve.",
        required_tool="smith_hammer",
        alternate_attribute="strength",
        alternate_attr_val=14,
        alternate_trait="blacksmith",
    ),
    "forge_sol_brass": Runeforge(
        id="forge_sol_brass",
        name="Solar Crucible Anvil",
        province="The Scorchwaste",
        forge_scene="scorchwaste_dune_ridge_armory",
        icon="🔥",
        rune_name="Sunfire Solar Rune",
        domain="Desert Hearth-Smelting & Sunfire Mail",
        description="Bronze braziers illuminate the desert foundry. Arid thermal heat fills the sandstone chamber.",
        inscribe_action_id="forge_inscribe_sol_brass",
        inscribe_action_label="Inscribe Solar Anvil",
        inscribe_result_text="You strike glowing desert brass upon the ancient anvil. Radiant hearth flames harden your defensive resolve.",
        rune_marker="marker_rune_sol_brass",
        mastery_marker="marker_forge_mastery_scorchwaste",
        temper_action_id="forge_temper_sol_brass",
        temper_action_label="Temper Solar Rune",
        temper_result_text="You heat the solar rune in the glowing embers. Desert warmth restores your physical endurance.",
        quench_action_id="forge_quench_sol_brass",
        quench_action_label="Quench Solar Crucible",
        quench_result_text="You immerse the heated bronze into spiced furnace oil. Radiant aromatic sparks renew your travel resolve.",
        required_tool="furnace_tongs",
        alternate_attribute="agility",
        alternate_attr_val=14,
        alternate_trait="fire_tender",
    ),
    "forge_tide_bronze": Runeforge(
        id="forge_tide_bronze",
        name="Abyssal Tide Anvil",
        province="The Sunken Hollows",
        forge_scene="sunken_hollows_glow_grotto_armory",
        icon="🫧",
        rune_name="Abyssal Tide Rune",
        domain="Hydrostatic Pressure-Forging & Tidal Cuirass",
        description="Oceanic currents drift past the submerged basalt forge. Steady mineral drops echo over the anvil.",
        inscribe_action_id="forge_inscribe_tide_bronze",
        inscribe_action_label="Inscribe Tide Anvil",
        inscribe_result_text="You hammer deep marine bronze under dripping stone. Cool ocean pressure hardens your protective resolve.",
        rune_marker="marker_rune_tide_bronze",
        mastery_marker="marker_forge_mastery_sunken",
        temper_action_id="forge_temper_tide_bronze",
        temper_action_label="Temper Tide Rune",
        temper_result_text="You align the tidal bronze runic engravings. Submerged grotto quiet steadies your breathing.",
        quench_action_id="forge_quench_tide_bronze",
        quench_action_label="Quench Tide Crucible",
        quench_result_text="You immerse the treated bronze in mineral brine. Salty oceanic vapor renews your travel resolve.",
        required_tool="cold_chisel",
        alternate_attribute="endurance",
        alternate_attr_val=14,
        alternate_trait="water_breather",
    ),
    "forge_palatine_steel": Runeforge(
        id="forge_palatine_steel",
        name="Palatine Ducal Anvil",
        province="The High Court",
        forge_scene="high_court_knight_barracks_armory",
        icon="⚖️",
        rune_name="Palatine Ducal Rune",
        domain="Regal Damascening & Noble Parrying Blades",
        description="Polished marble columns flank the private ducal foundry. Magnificent weapon racks line the grand hall.",
        inscribe_action_id="forge_inscribe_palatine_steel",
        inscribe_action_label="Inscribe Court Anvil",
        inscribe_result_text="You fold high-carbon court steel upon the polished anvil. Regal martial discipline sharpens your edge.",
        rune_marker="marker_rune_palatine_steel",
        mastery_marker="marker_forge_mastery_high_court",
        temper_action_id="forge_temper_palatine_steel",
        temper_action_label="Temper Court Rune",
        temper_result_text="You inspect the damascened palace runes under lantern light. High court elegance steadies your nerves.",
        quench_action_id="forge_quench_palatine_steel",
        quench_action_label="Quench Court Crucible",
        quench_result_text="You bathe the gleaming rapier in lavender oil. Subtle floral aromas renew your travel resolve.",
        required_tool="jeweler_pliers",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="noble_bearing",
    ),
    "forge_bell_iron": Runeforge(
        id="forge_bell_iron",
        name="Harbor Bell Foundry",
        province="The Lowlands",
        forge_scene="lowlands_oakhaven_port_armory",
        icon="⚓",
        rune_name="Harbor Bell Rune",
        domain="Saline Quenching & Heavy Dockyard Cleavers",
        description="Heavy maritime mist blankets the waterfront armory. The pungent scent of hot iron fills the bay.",
        inscribe_action_id="forge_inscribe_bell_iron",
        inscribe_action_label="Inscribe Harbor Anvil",
        inscribe_result_text="You hammer heavy river iron on the salt-stained block. Harbor shipyard resolve strengthens your grip.",
        rune_marker="marker_rune_bell_iron",
        mastery_marker="marker_forge_mastery_lowlands",
        temper_action_id="forge_temper_bell_iron",
        temper_action_label="Temper Harbor Rune",
        temper_result_text="You scrape maritime salt crust from the harbor rune. Industrial dockyard resolve restores your traveling pace.",
        quench_action_id="forge_quench_bell_iron",
        quench_action_label="Quench Harbor Crucible",
        quench_result_text="You plunge the dark iron into river brack. Rushing maritime spray renews your travel resolve.",
        required_tool="iron_file",
        alternate_attribute="agility",
        alternate_attr_val=14,
        alternate_trait="streetwise",
    ),
    "forge_crossroads_grand": Runeforge(
        id="forge_crossroads_grand",
        name="Grand Sovereign Foundry",
        province="Central Crossroads",
        forge_scene="bazaar_center",
        icon="👑",
        rune_name="Grand Sovereign Rune",
        domain="Continental Metallurgy & Master Relic Alloys",
        description="Bazaar banners hang above the grand central foundry. Caravan travelers barter for forged wares.",
        inscribe_action_id="forge_inscribe_crossroads_grand",
        inscribe_action_label="Inscribe Sovereign Anvil",
        inscribe_result_text="You strike the master crossroads anvil with precision. Grand continental unity guides your hand.",
        rune_marker="marker_rune_crossroads_grand",
        mastery_marker="marker_forge_mastery_crossroads",
        temper_action_id="forge_temper_crossroads_grand",
        temper_action_label="Temper Sovereign Rune",
        temper_result_text="You study the five provincial rune marks with care. Caravan trade unity restores your fighting spirit.",
        quench_action_id="forge_quench_crossroads_grand",
        quench_action_label="Quench Sovereign Crucible",
        quench_result_text="You polish the finished masterwork blade with care. Rich bazaar incense renews your travel resolve.",
        required_tool="smith_hammer",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="artificer",
    ),
}

# Artificer rank progression tiers
ARTIFICER_RANKS: List[Dict[str, Any]] = [
    {
        "count": 0,
        "title": "Apprentice Striker",
        "desc": "You hold no forged runes or inscribed masterworks. Continental anvils remain dormant in your travels.",
    },
    {
        "count": 1,
        "title": "Journeyman Smith",
        "desc": "You have struck your first ancient provincial anvil. Metalworking experience guides your hammer.",
    },
    {
        "count": 2,
        "title": "Anvil Craftsman",
        "desc": "Two provincial anvils bear your masterwork marks. Complex smithing formulas appear clear to your eyes.",
    },
    {
        "count": 3,
        "title": "Master Artificer",
        "desc": "Three continental runeforges have been inscribed with skill. Tough armor materials yield easily to your craft.",
    },
    {
        "count": 4,
        "title": "Guild Metallurgist",
        "desc": "Four provincial anvils are mastered with great care. Your forging reputation commands high respect.",
    },
    {
        "count": 5,
        "title": "Grand Anvilmaster",
        "desc": "All five provincial runeforges are mastered with care. You command complete smithing knowledge across the realm.",
    },
    {
        "count": 6,
        "title": "Continental Forgemaster",
        "desc": "All continental runeforges are conquered with skill. You hold supreme smithing mastery across the land.",
    },
]


def get_artificer_rank(inscribed_count: int) -> Dict[str, str]:
    """Determine Artificer rank title and description from inscribed runeforge count."""
    best = ARTIFICER_RANKS[0]
    for tier in ARTIFICER_RANKS:
        if inscribed_count >= tier["count"]:
            best = tier
    return {"title": str(best["title"]), "desc": str(best["desc"])}


def evaluate_forge_progress(
    flags: Dict[str, Any],
    inventory: List[str],
    markers: List[str],
    current_scene: str = ""
) -> Dict[str, Any]:
    """Deterministic evaluation of runeforges, artificer rank, and active runes."""
    marker_set = {str(m).lower() for m in markers}
    inscribed_count = 0
    active_runes_count = 0
    active_masteries_count = 0
    forge_list = []
    current_scene_forge = None

    for f in ANCIENT_RUNEFORGES.values():
        is_inscribed = bool(flags.get(f"forge_inscribed_{f.id}", False))
        has_rune = f.rune_marker.lower() in marker_set
        is_tempered = bool(flags.get(f"forge_tempered_{f.id}", False))
        has_mastery = f.mastery_marker.lower() in marker_set

        if is_inscribed:
            inscribed_count += 1
        if has_rune:
            active_runes_count += 1
        if has_mastery:
            active_masteries_count += 1

        if current_scene == f.forge_scene:
            current_scene_forge = f.id

        forge_list.append(
            f.to_dict(
                is_inscribed=is_inscribed,
                has_rune=has_rune,
                is_tempered=is_tempered,
                has_mastery=has_mastery,
            )
        )

    rank_info = get_artificer_rank(inscribed_count)
    progress_pct = round((inscribed_count / max(1, len(ANCIENT_RUNEFORGES))) * 100, 1)

    return {
        "forges": forge_list,
        "inscribed_count": inscribed_count,
        "total_forges": len(ANCIENT_RUNEFORGES),
        "active_runes_count": active_runes_count,
        "active_masteries_count": active_masteries_count,
        "artificer_rank": rank_info["title"],
        "rank_desc": rank_info["desc"],
        "progress_pct": progress_pct,
        "current_scene_forge": current_scene_forge,
    }


def get_forge_progress(state: Any) -> Dict[str, Any]:
    """Compute deterministic forge progress and artificer rank from GameState."""
    flags = state.world_flags if hasattr(state, "world_flags") else getattr(state, "flags", {})
    char = getattr(state, "character", None)
    inv = getattr(char, "inventory", []) if char else []
    markers = getattr(char, "markers", []) if char else []
    current_scene = getattr(state, "current_scene", "")
    return evaluate_forge_progress(flags, inv, markers, current_scene)


def get_forge_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic runeforge inscription, rune tempering, and crucible quenching affordances."""
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

    # Generic smithing tools that satisfy hardware requirements
    forge_tools = {
        "smith_hammer",
        "item_hammer",
        "hammer",
        "tools",
        "tinkering_tools",
        "crafting_supplies",
        "cold_chisel",
        "furnace_tongs",
        "iron_file",
        "jeweler_pliers",
    }
    has_any_forge_tool = any(t in inv_list for t in forge_tools) or any(
        any(k in item for k in ["hammer", "chisel", "tongs", "pliers", "file", "tinkering", "crafting"])
        for item in inv_list
    )

    # 1. Armory Runeforge Inscriptions and Crucible Quenchings
    for f in ANCIENT_RUNEFORGES.values():
        if scene_id == f.forge_scene:
            is_inscribed = bool(world_flags.get(f"forge_inscribed_{f.id}", False))
            is_tempered = bool(world_flags.get(f"forge_tempered_{f.id}", False))

            if not is_inscribed:
                # 7-axis qualification:
                # 1. Has specific tool or generic smith tool
                # 2. Has relevant traits (blacksmith, artificer, craftsman, etc.)
                # 3. Has high attribute (strength >= 14, wits >= 14, or alternate_attr)
                # 4. Has relevant skills (cunning, athletics, lore >= 2)
                # 5. Has physical stamina (stamina >= 2)
                has_tool = (f.required_tool.lower() in inv_list) or has_any_forge_tool
                has_trait = (f.alternate_trait.lower() in traits_list) or any(
                    t in traits_list
                    for t in [
                        "blacksmith",
                        "artificer",
                        "craftsman",
                        "metalworker",
                        "strong",
                        "focused",
                        "nimble",
                    ]
                )
                attr_val = character.get_attribute(f.alternate_attribute)
                has_attr = (attr_val >= f.alternate_attr_val) or (
                    character.get_attribute("strength") >= 14
                    or character.get_attribute("wits") >= 14
                )
                has_skill = (
                    skills_dict.get("cunning", 0) >= 2
                    or skills_dict.get("athletics", 0) >= 2
                    or skills_dict.get("lore", 0) >= 2
                )
                has_stam = getattr(character, "stamina", 0) >= 2

                if has_tool or has_trait or has_attr or has_skill or has_stam:
                    affordances.append(
                        Action(
                            id=f.inscribe_action_id,
                            label=f.inscribe_action_label,
                            category="exploration",
                            effects=[
                                {"set_flag": {"flag": f"forge_inscribed_{f.id}", "value": True}},
                                {"add_marker": f.rune_marker},
                                {"add_marker": f.mastery_marker},
                                {"modify_stamina": 3},
                                {"log_event": f.inscribe_result_text},
                            ],
                            result_text=f.inscribe_result_text,
                            risk="low",
                            stamina_cost=0,
                        )
                    )
            elif is_tempered:
                # Can quench and refine masterwork at forge scene
                affordances.append(
                    Action(
                        id=f.quench_action_id,
                        label=f.quench_action_label,
                        category="exploration",
                        effects=[
                            {"set_flag": {"flag": f"forge_tempered_{f.id}", "value": False}},
                            {"modify_stamina": 2},
                            {"log_event": f.quench_result_text},
                        ],
                        result_text=f.quench_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    # 2. Field Rune Tempering anywhere in the continental world
    for f in ANCIENT_RUNEFORGES.values():
        if f.rune_marker.lower() in marker_list:
            is_tempered = bool(world_flags.get(f"forge_tempered_{f.id}", False))
            if not is_tempered:
                affordances.append(
                    Action(
                        id=f.temper_action_id,
                        label=f.temper_action_label,
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": f"forge_tempered_{f.id}", "value": True}},
                            {"add_marker": f"marker_tempered_{f.id}"},
                            {"modify_stamina": 3},
                            {"log_event": f.temper_result_text},
                        ],
                        result_text=f.temper_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    return affordances
