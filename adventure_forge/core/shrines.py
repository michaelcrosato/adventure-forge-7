"""Milestone 28: Continental Ancient Shrines, Relic Offerings & Divine Celestial Blessings System.

Provides 6 Ancient Shrines situated at regional sanctums and crossroads,
7-axis devotion offerings yielding divine Titan Blessings, dynamic field invocations,
sanctum attunement renewals, and Continental Hierarch / Avatar of the Five Titans rank progression.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class AncientShrine:
    """An ancient continental shrine with dedicated sanctum, patron deity, and divine blessing."""
    id: str
    name: str
    deity: str
    province: str
    sanctum_scene: str
    icon: str
    domain: str
    description: str
    consecrate_action_id: str
    consecrate_action_label: str   # Exactly 1 to 3 words
    consecrate_result_text: str
    blessing_marker: str
    blessing_name: str
    blessing_desc: str
    invoke_action_id: str
    invoke_action_label: str       # Exactly 1 to 3 words
    invoke_result_text: str
    aura_marker: str
    renew_action_id: str
    renew_action_label: str        # Exactly 1 to 3 words
    renew_result_text: str
    offering_item: str
    alternate_attribute: str
    alternate_attr_val: int
    alternate_trait: str

    def to_dict(
        self,
        is_consecrated: bool = False,
        has_blessing: bool = False,
        is_invoked: bool = False,
        is_aura_active: bool = False,
    ) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "deity": self.deity,
            "province": self.province,
            "sanctum_scene": self.sanctum_scene,
            "icon": self.icon,
            "domain": self.domain,
            "description": self.description,
            "consecrate_action_id": self.consecrate_action_id,
            "consecrate_action_label": self.consecrate_action_label,
            "blessing_marker": self.blessing_marker,
            "blessing_name": self.blessing_name,
            "blessing_desc": self.blessing_desc,
            "invoke_action_id": self.invoke_action_id,
            "invoke_action_label": self.invoke_action_label,
            "aura_marker": self.aura_marker,
            "renew_action_id": self.renew_action_id,
            "renew_action_label": self.renew_action_label,
            "offering_item": self.offering_item,
            "alternate_attribute": self.alternate_attribute,
            "alternate_attr_val": self.alternate_attr_val,
            "alternate_trait": self.alternate_trait,
            "is_consecrated": is_consecrated,
            "has_blessing": has_blessing,
            "is_invoked": is_invoked,
            "is_aura_active": is_aura_active,
        }


ANCIENT_SHRINES: Dict[str, AncientShrine] = {
    "shrine_khoros": AncientShrine(
        id="shrine_khoros",
        name="Shrine of Khoros",
        deity="Khoros the Mountain Titan",
        province="The Reach",
        sanctum_scene="reach_frost_cavern_sanctum",
        icon="⛰️",
        domain="Crags, Granite Will & Mountain Strength",
        description="Granite monoliths crown this frost cavern altar. Mountain winds echo through the frozen stone chamber.",
        consecrate_action_id="shrine_consecrate_khoros",
        consecrate_action_label="Consecrate Khoros Altar",
        consecrate_result_text="You offer your tribute upon the stone altar. Mountain resolve steadies your weary body.",
        blessing_marker="marker_blessing_khoros",
        blessing_name="Blessing of Khoros",
        blessing_desc="Enduring mountain resilience granting vitality and unyielding stability.",
        invoke_action_id="shrine_invoke_khoros",
        invoke_action_label="Invoke Khoros",
        invoke_result_text="You invoke the mountain blessing of Khoros. Sturdy stone fortitude restores your vigor.",
        aura_marker="marker_aura_khoros",
        renew_action_id="shrine_renew_khoros",
        renew_action_label="Renew Khoros",
        renew_result_text="You rest hands upon the frost altar. Unyielding mountain resilience recharges your spirit.",
        offering_item="ice_lotus",
        alternate_attribute="strength",
        alternate_attr_val=14,
        alternate_trait="iron_gutted",
    ),
    "shrine_sol_ankh": AncientShrine(
        id="shrine_sol_ankh",
        name="Altar of Sol-Ankh",
        deity="Sol-Ankh the Sun Serpent",
        province="The Scorchwaste",
        sanctum_scene="scorchwaste_sun_shrine_sanctum",
        icon="☀️",
        domain="Sunfire, Heat Tolerance & Purifying Light",
        description="Carved sandstone pillars encircle the desert altar. Solar braziers radiate dry heat across the floor.",
        consecrate_action_id="shrine_consecrate_sol_ankh",
        consecrate_action_label="Consecrate Sun Altar",
        consecrate_result_text="You set your desert offering on the bronze altar. Warm solar radiance banishes your exhaustion.",
        blessing_marker="marker_blessing_sol_ankh",
        blessing_name="Blessing of Sol-Ankh",
        blessing_desc="Purifying solar flame granting heat tolerance and fiery fighting spirit.",
        invoke_action_id="shrine_invoke_sol_ankh",
        invoke_action_label="Invoke Sol-Ankh",
        invoke_result_text="You invoke the radiant power of Sol-Ankh. Cleansing desert heat purges deep fatigue and restores combat focus.",
        aura_marker="marker_aura_sol_ankh",
        renew_action_id="shrine_renew_sol_ankh",
        renew_action_label="Renew Sol-Ankh",
        renew_result_text="You place your hands upon the serpent altar. Restorative solar fire recharges your blessing.",
        offering_item="trade_sunfire_spice",
        alternate_attribute="endurance",
        alternate_attr_val=14,
        alternate_trait="heat_adapted",
    ),
    "shrine_thalassa": AncientShrine(
        id="shrine_thalassa",
        name="Altar of Thalassa",
        deity="Thalassa the Abyssal Leviathan",
        province="The Sunken Hollows",
        sanctum_scene="sunken_hollows_drowned_temple_sanctum",
        icon="🌊",
        domain="Depths, Hydrostatic Calm & Tidal Vigor",
        description="Black obsidian columns rise from the calm cavern pool. Clear underground waters lap against the leviathan dais.",
        consecrate_action_id="shrine_consecrate_thalassa",
        consecrate_action_label="Consecrate Deep Altar",
        consecrate_result_text="You dip your hands into the sacred tidal pool. Deep oceanic serenity restores quiet focus to your mind.",
        blessing_marker="marker_blessing_thalassa",
        blessing_name="Blessing of Thalassa",
        blessing_desc="Deep aquatic serenity granting diving endurance and abyssal calmness.",
        invoke_action_id="shrine_invoke_thalassa",
        invoke_action_label="Invoke Thalassa",
        invoke_result_text="You invoke the deep calm of Thalassa. Cool restorative water soothes your lungs and restores endurance.",
        aura_marker="marker_aura_thalassa",
        renew_action_id="shrine_renew_thalassa",
        renew_action_label="Renew Thalassa",
        renew_result_text="You dip your fingers into the sacred cavern pool. Deep tidal serenity recharges your watery blessing.",
        offering_item="abyssal_pearl",
        alternate_attribute="agility",
        alternate_attr_val=14,
        alternate_trait="diver_lungs",
    ),
    "shrine_aurelius": AncientShrine(
        id="shrine_aurelius",
        name="Altar of Aurelius",
        deity="Aurelius the Sovereign Justiciar",
        province="The High Court",
        sanctum_scene="high_court_grand_basilica_sanctum",
        icon="👑",
        domain="Justice, Imperial Grace & Royal Sovereignty",
        description="Tall stone pillars support the high basilica ceiling. Soft light shines upon the royal altar.",
        consecrate_action_id="shrine_consecrate_aurelius",
        consecrate_action_label="Consecrate Royal Altar",
        consecrate_result_text="You kneel in respect before the basilica altar. Sovereign favor grants steady poise to your command.",
        blessing_marker="marker_blessing_aurelius",
        blessing_name="Blessing of Aurelius",
        blessing_desc="Imperial sovereign dignity granting diplomatic presence and regal composure.",
        invoke_action_id="shrine_invoke_aurelius",
        invoke_action_label="Invoke Aurelius",
        invoke_result_text="You invoke the royal grace of Aurelius. Calm command presence restores your confidence.",
        aura_marker="marker_aura_aurelius",
        renew_action_id="shrine_renew_aurelius",
        renew_action_label="Renew Aurelius",
        renew_result_text="You bow before the white cathedral altar. Sovereign favor recharges your royal blessing.",
        offering_item="trade_silk_bolt",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="silver_tongued",
    ),
    "shrine_mara": AncientShrine(
        id="shrine_mara",
        name="Altar of Mara",
        deity="Mara the Mist Maiden",
        province="The Lowlands",
        sanctum_scene="lowlands_bell_tower_sanctum",
        icon="🌫️",
        domain="Tides, Canal Mists & Evasive Fortune",
        description="Weathered granite stones form this coastal mist altar. Salty harbor breezes sweep past the ancient bell tower sanctuary.",
        consecrate_action_id="shrine_consecrate_mara",
        consecrate_action_label="Consecrate Mist Altar",
        consecrate_result_text="You place a silver token upon the harbor altar. Evasive fortune shields your quiet movements.",
        blessing_marker="marker_blessing_mara",
        blessing_name="Blessing of Mara",
        blessing_desc="Evasive mist veil granting stealthy swiftness and canal navigation fortune.",
        invoke_action_id="shrine_invoke_mara",
        invoke_action_label="Invoke Mara",
        invoke_result_text="You invoke the elusive blessing of Mara. Shifting canal vapors mask your footprints and restore quickness.",
        aura_marker="marker_aura_mara",
        renew_action_id="shrine_renew_mara",
        renew_action_label="Renew Mara",
        renew_result_text="You cast salt upon the weathered harbor altar. Evasive mist fortune recharges your stealthy blessing.",
        offering_item="trade_bog_whiskey",
        alternate_attribute="agility",
        alternate_attr_val=14,
        alternate_trait="shadow_cloaked",
    ),
    "shrine_wayfarer": AncientShrine(
        id="shrine_wayfarer",
        name="Shrine of the Five Winds",
        deity="Pantheon of the Five Winds",
        province="Central Crossroads",
        sanctum_scene="bazaar_center",
        icon="✨",
        domain="Pilgrimage, Safe Roads & Continental Unity",
        description="A circular stone dais rests at the center of the crossroads. Colorful prayer flags flutter in the brisk marketplace air.",
        consecrate_action_id="shrine_consecrate_wayfarer",
        consecrate_action_label="Consecrate Winds Altar",
        consecrate_result_text="You dedicate your long continental journey at the central stone. The Five Winds grant enduring travel stamina.",
        blessing_marker="marker_blessing_wayfarer",
        blessing_name="Blessing of the Five Winds",
        blessing_desc="Continental traveling grace granting sustained march endurance and road speed.",
        invoke_action_id="shrine_invoke_wayfarer",
        invoke_action_label="Invoke Five Winds",
        invoke_result_text="You invoke the ancient blessing of the Five Winds. A steady continental breeze restores your stamina.",
        aura_marker="marker_aura_wayfarer",
        renew_action_id="shrine_renew_wayfarer",
        renew_action_label="Renew Five Winds",
        renew_result_text="You touch the central crossroads dais. Swift travelers favor recharges your continental blessing.",
        offering_item="lockpick",
        alternate_attribute="agility",
        alternate_attr_val=12,
        alternate_trait="tireless_trekker",
    ),
}


PILGRIM_RANKS: List[Dict[str, Any]] = [
    {"count": 0, "title": "Unanointed Wanderer", "desc": "You have not yet consecrated any ancient provincial shrines."},
    {"count": 1, "title": "Shrine Pilgrim", "desc": "You have consecrated 1 ancient shrine and earned a divine blessing."},
    {"count": 2, "title": "Consecrated Devotee", "desc": "You have consecrated 2 ancient shrines across the realm."},
    {"count": 3, "title": "Temple Hierophant", "desc": "You have consecrated 3 ancient shrines and mastered sacred rites."},
    {"count": 4, "title": "Provincial Exarch", "desc": "You have consecrated 4 ancient shrines across the continent."},
    {"count": 5, "title": "Continental Hierarch", "desc": "You have consecrated 5 provincial shrines to the elemental titans."},
    {"count": 6, "title": "Avatar of the Five Titans", "desc": "You have consecrated all 6 shrines and united the continental pantheon."},
]


def get_pilgrim_rank(consecrated_count: int) -> Dict[str, Any]:
    """Return the pilgrim rank tier matching consecrated shrines count."""
    best = PILGRIM_RANKS[0]
    for tier in PILGRIM_RANKS:
        if consecrated_count >= tier["count"]:
            best = tier
    return best


def evaluate_shrines_progress(
    world_flags: Dict[str, Any],
    inventory: Any,
    markers: Any,
    current_scene: str = ""
) -> Dict[str, Any]:
    """Compute deterministic shrine progress, active blessings, and pilgrim rank from components."""
    marker_set = set()
    if isinstance(markers, (list, tuple, set)):
        marker_set = {str(m).lower() for m in markers}

    shrine_list = []
    consecrated_count = 0
    active_blessings_count = 0
    active_auras_count = 0
    current_scene_shrine = None

    for shrine in ANCIENT_SHRINES.values():
        is_consecrated = bool(world_flags.get(f"shrine_consecrated_{shrine.id}", False))
        has_blessing = shrine.blessing_marker.lower() in marker_set
        is_invoked = bool(world_flags.get(f"blessing_invoked_{shrine.id}", False))
        is_aura_active = (shrine.aura_marker.lower() in marker_set) and is_invoked

        if is_consecrated:
            consecrated_count += 1
        if has_blessing:
            active_blessings_count += 1
        if is_aura_active:
            active_auras_count += 1
        if current_scene == shrine.sanctum_scene:
            current_scene_shrine = shrine.id

        shrine_list.append(
            shrine.to_dict(
                is_consecrated=is_consecrated,
                has_blessing=has_blessing,
                is_invoked=is_invoked,
                is_aura_active=is_aura_active,
            )
        )

    rank_info = get_pilgrim_rank(consecrated_count)
    progress_pct = round((consecrated_count / max(1, len(ANCIENT_SHRINES))) * 100, 1)

    return {
        "shrines": shrine_list,
        "consecrated_count": consecrated_count,
        "total_shrines": len(ANCIENT_SHRINES),
        "active_blessings_count": active_blessings_count,
        "active_auras_count": active_auras_count,
        "pilgrim_rank": rank_info["title"],
        "rank_desc": rank_info["desc"],
        "progress_pct": progress_pct,
        "current_scene_shrine": current_scene_shrine,
    }


def get_shrines_progress(state: Any) -> Dict[str, Any]:
    """Compute deterministic shrine progress, active blessings, and pilgrim rank from GameState."""
    flags = state.world_flags if hasattr(state, "world_flags") else getattr(state, "flags", {})
    char = getattr(state, "character", None)
    inv = getattr(char, "inventory", []) if char else []
    markers = getattr(char, "markers", []) if char else []
    current_scene = getattr(state, "current_scene", "")
    return evaluate_shrines_progress(flags, inv, markers, current_scene)


def get_shrine_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic shrine consecration, blessing renewal, and field invocation affordances."""
    from adventure_forge.content.schema import Action

    affordances: List[Action] = []
    inv_list: List[str] = []
    marker_list: List[str] = []
    if hasattr(character, "inventory"):
        inv_list = [str(k).lower() for k in character.inventory]
    if hasattr(character, "markers"):
        marker_list = [str(k).lower() for k in character.markers]

    # 1. Sanctum Consecrations and Renewals
    for shrine in ANCIENT_SHRINES.values():
        if scene_id == shrine.sanctum_scene:
            is_consecrated = bool(world_flags.get(f"shrine_consecrated_{shrine.id}", False))
            is_invoked = bool(world_flags.get(f"blessing_invoked_{shrine.id}", False))

            if not is_consecrated:
                # 7-axis qualification: item tribute OR attribute OR trait OR stamina >= 2
                has_item = shrine.offering_item.lower() in inv_list
                has_trait = shrine.alternate_trait.lower() in [t.lower() for t in getattr(character, "traits", [])]
                attr_val = character.get_attribute(shrine.alternate_attribute)
                has_attr = attr_val >= shrine.alternate_attr_val
                has_stam = getattr(character, "stamina", 0) >= 2

                if has_item or has_trait or has_attr or has_stam:
                    affordances.append(
                        Action(
                            id=shrine.consecrate_action_id,
                            label=shrine.consecrate_action_label,
                            category="social",
                            effects=[
                                {"set_flag": {"flag": f"shrine_consecrated_{shrine.id}", "value": True}},
                                {"add_marker": shrine.blessing_marker},
                                {"modify_stamina": 3},
                                {"log_event": shrine.consecrate_result_text},
                            ],
                            result_text=shrine.consecrate_result_text,
                            risk="low",
                            stamina_cost=0,
                        )
                    )
            elif is_invoked:
                # Can renew blessing at the sanctum
                affordances.append(
                    Action(
                        id=shrine.renew_action_id,
                        label=shrine.renew_action_label,
                        category="social",
                        effects=[
                            {"set_flag": {"flag": f"blessing_invoked_{shrine.id}", "value": False}},
                            {"modify_stamina": 2},
                            {"log_event": shrine.renew_result_text},
                        ],
                        result_text=shrine.renew_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    # 2. Field Invocations anywhere in the continental world
    for shrine in ANCIENT_SHRINES.values():
        if shrine.blessing_marker.lower() in marker_list:
            is_invoked = bool(world_flags.get(f"blessing_invoked_{shrine.id}", False))
            if not is_invoked:
                affordances.append(
                    Action(
                        id=shrine.invoke_action_id,
                        label=shrine.invoke_action_label,
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": f"blessing_invoked_{shrine.id}", "value": True}},
                            {"add_marker": shrine.aura_marker},
                            {"modify_stamina": 4},
                            {"log_event": shrine.invoke_result_text},
                        ],
                        result_text=shrine.invoke_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    return affordances
