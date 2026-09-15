"""Milestone 33: Continental Celestial Orreries, Astrolabe Spheres & Master Stargazer System.

Provides 6 Canonical Ancient Astrolabe Chambers situated in regional spires, domes, and crossroads,
7-axis astrological affordances yielding celestial lenses and astrometric mastery,
dynamic field constellation attunement, chamber recalibration renewals, and Grand Royal Stargazer rank progression.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class CelestialOrrery:
    """A continental ancient astrolabe chamber with celestial armillary sphere, crystal lens, and star dials."""
    id: str
    name: str
    province: str
    chamber_scene: str
    icon: str
    lens_name: str
    domain: str
    description: str
    align_action_id: str
    align_action_label: str       # Exactly 1 to 3 words
    align_result_text: str
    lens_marker: str
    mastery_marker: str
    attune_action_id: str
    attune_action_label: str      # Exactly 1 to 3 words
    attune_result_text: str
    recalibrate_action_id: str
    recalibrate_action_label: str  # Exactly 1 to 3 words
    recalibrate_result_text: str
    required_tool: str
    alternate_attribute: str
    alternate_attr_val: int
    alternate_trait: str

    def to_dict(
        self,
        is_aligned: bool = False,
        has_lens: bool = False,
        is_attuned: bool = False,
        has_mastery: bool = False,
    ) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "chamber_scene": self.chamber_scene,
            "icon": self.icon,
            "lens_name": self.lens_name,
            "domain": self.domain,
            "description": self.description,
            "align_action_id": self.align_action_id,
            "align_action_label": self.align_action_label,
            "lens_marker": self.lens_marker,
            "mastery_marker": self.mastery_marker,
            "attune_action_id": self.attune_action_id,
            "attune_action_label": self.attune_action_label,
            "recalibrate_action_id": self.recalibrate_action_id,
            "recalibrate_action_label": self.recalibrate_action_label,
            "required_tool": self.required_tool,
            "alternate_attribute": self.alternate_attribute,
            "alternate_attr_val": self.alternate_attr_val,
            "alternate_trait": self.alternate_trait,
            "is_aligned": is_aligned,
            "has_lens": has_lens,
            "is_attuned": is_attuned,
            "has_mastery": has_mastery,
        }


# 6 Canonical Continental Celestial Orreries
ANCIENT_ORRERIES: Dict[str, CelestialOrrery] = {
    "orrery_frost_zenith": CelestialOrrery(
        id="orrery_frost_zenith",
        name="Glacial Astrolabe Chamber",
        province="The Reach",
        chamber_scene="reach_iron_spire_chamber",
        icon="❄️",
        lens_name="Titan Crown Lens",
        domain="High Peak Celestial Navigation & Blizzard Tracking",
        description="Brass rings swivel within the lofty mountain chamber. Clear starlight reflects across polished crystal lenses.",
        align_action_id="orrery_align_frost_zenith",
        align_action_label="Align Glacial Astrolabe",
        align_result_text="You rotate the heavy brass astrolabe toward northern stars. Crisp alpine clarity guides your compass.",
        lens_marker="marker_lens_frost_zenith",
        mastery_marker="marker_orrery_mastery_reach",
        attune_action_id="orrery_attune_frost_zenith",
        attune_action_label="Attune Frost Constellation",
        attune_result_text="You observe the northern crown through the crystal lens. Glacial celestial clarity sharpens your focus.",
        recalibrate_action_id="orrery_recalibrate_frost_zenith",
        recalibrate_action_label="Recalibrate Mountain Lens",
        recalibrate_result_text="You polish the frozen lens with chamois leather. Pure alpine starlight renews your travel resolve.",
        required_tool="brass_astrolabe",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="stargazer",
    ),
    "orrery_sol_zenith": CelestialOrrery(
        id="orrery_sol_zenith",
        name="Solar Zenith Astrolabe",
        province="The Scorchwaste",
        chamber_scene="scorchwaste_sun_shrine_chamber",
        icon="🔥",
        lens_name="Solar Disk Lens",
        domain="Desert Solar Zenith & Sandstorm Trajectories",
        description="Golden sun discs rotate upon sandstone pillars. Focused solar rays illuminate carved star charts.",
        align_action_id="orrery_align_sol_zenith",
        align_action_label="Align Solar Astrolabe",
        align_result_text="You align the golden disc with brilliant desert sunbeams. Radiant warmth steadies your marching endurance.",
        lens_marker="marker_lens_sol_zenith",
        mastery_marker="marker_orrery_mastery_scorchwaste",
        attune_action_id="orrery_attune_sol_zenith",
        attune_action_label="Attune Solar Constellation",
        attune_result_text="You channel solar warmth from the golden lens. Desert vigor shields your physical endurance.",
        recalibrate_action_id="orrery_recalibrate_sol_zenith",
        recalibrate_action_label="Recalibrate Solar Disc",
        recalibrate_result_text="You balance the golden solar disc on oiled pivots. Golden reflected sunlight renews your travel resolve.",
        required_tool="brass_astrolabe",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="navigator",
    ),
    "orrery_abyssal_prism": CelestialOrrery(
        id="orrery_abyssal_prism",
        name="Abyssal Prism Astrolabe",
        province="The Sunken Hollows",
        chamber_scene="sunken_hollows_echoing_dome_chamber",
        icon="💧",
        lens_name="Tidal Pearl Lens",
        domain="Subterranean Tide Currents & Hydrostatic Cycles",
        description="Deep cave mirrors catch glowing crystal light. Rotating water wheels spin calibrated lunar dials.",
        align_action_id="orrery_align_abyssal_prism",
        align_action_label="Align Abyssal Astrolabe",
        align_result_text="You turn the lunar dials against rushing cave waters. Deep water balance stabilizes your body.",
        lens_marker="marker_lens_abyssal_prism",
        mastery_marker="marker_orrery_mastery_sunken",
        attune_action_id="orrery_attune_abyssal_prism",
        attune_action_label="Attune Tidal Constellation",
        attune_result_text="You study the azure light refracted by the pearl. Subterranean oceanic calm steadies your breathing.",
        recalibrate_action_id="orrery_recalibrate_abyssal_prism",
        recalibrate_action_label="Recalibrate Tidal Prism",
        recalibrate_result_text="You clear mineral salts from the crystal prism. Rushing tidal waters renew your travel resolve.",
        required_tool="brass_astrolabe",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="scholar",
    ),
    "orrery_palatine_dome": CelestialOrrery(
        id="orrery_palatine_dome",
        name="Palatine Star Chamber",
        province="The High Court",
        chamber_scene="high_court_high_spire_chamber",
        icon="⚜️",
        lens_name="Imperial Scepter Lens",
        domain="Noble Natal Charts & Sovereign Planetary Alignments",
        description="Gilded armillary spheres rotate beneath the high vaulted ceiling. Velvet drapes frame bronze telescope sights.",
        align_action_id="orrery_align_palatine_dome",
        align_action_label="Align Palatine Astrolabe",
        align_result_text="You set the gilded rings to the imperial ascendant. Princely confidence commands your mind.",
        lens_marker="marker_lens_palatine_dome",
        mastery_marker="marker_orrery_mastery_high_court",
        attune_action_id="orrery_attune_palatine_dome",
        attune_action_label="Attune Imperial Constellation",
        attune_result_text="You align the royal star with precision. Imperial prestige elevates your poise.",
        recalibrate_action_id="orrery_recalibrate_palatine_dome",
        recalibrate_action_label="Recalibrate Star Sphere",
        recalibrate_result_text="You dust velvet bearings along the armillary rim. Gleaming gold luster renews your travel resolve.",
        required_tool="brass_astrolabe",
        alternate_attribute="presence",
        alternate_attr_val=14,
        alternate_trait="noble",
    ),
    "orrery_tidebell_meridian": CelestialOrrery(
        id="orrery_tidebell_meridian",
        name="Tidebell Meridian Chamber",
        province="The Lowlands",
        chamber_scene="lowlands_bell_tower_chamber",
        icon="🌿",
        lens_name="Compass Rose Lens",
        domain="Harbor Navigation & Coastal Horizon Astrometry",
        description="Heavy brass pendulum weights swing within the stone tower. Marine navigation charts hang beside iron gears.",
        align_action_id="orrery_align_tidebell_meridian",
        align_action_label="Align Meridian Astrolabe",
        align_result_text="You adjust the pendulum clock to coastal harbor tide. Rhythmic coastal winds steady your footing.",
        lens_marker="marker_lens_tidebell_meridian",
        mastery_marker="marker_orrery_mastery_lowlands",
        attune_action_id="orrery_attune_tidebell_meridian",
        attune_action_label="Attune Meridian Constellation",
        attune_result_text="You study the southern cross on nautical charts. Maritime instincts guide your coastal footsteps.",
        recalibrate_action_id="orrery_recalibrate_tidebell_meridian",
        recalibrate_action_label="Recalibrate Clock Weights",
        recalibrate_result_text="You oil the iron pendulum pivots with tallow. Rhythmic ticking renews your travel resolve.",
        required_tool="brass_astrolabe",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="sailor",
    ),
    "orrery_crossroads_grand": CelestialOrrery(
        id="orrery_crossroads_grand",
        name="Grand Sovereign Orrery",
        province="Central Crossroads",
        chamber_scene="bazaar_center",
        icon="👑",
        lens_name="Sovereign Zodiac Sphere",
        domain="Continental Planetary Synthesis & Grand Zodiac Alignment",
        description="A grand celestial armillary sphere crowns the courtyard. Polished brass planets trace great bronze orbits.",
        align_action_id="orrery_align_crossroads_grand",
        align_action_label="Align Sovereign Orrery",
        align_result_text="You turn the master wheel across five regional orbits. Continental harmony guides your path.",
        lens_marker="marker_lens_crossroads_grand",
        mastery_marker="marker_orrery_mastery_crossroads",
        attune_action_id="orrery_attune_crossroads_grand",
        attune_action_label="Attune Sovereign Zodiac",
        attune_result_text="You harmonize the central zodiac sphere with care. Continental harmony restores your strength.",
        recalibrate_action_id="orrery_recalibrate_crossroads_grand",
        recalibrate_action_label="Recalibrate Grand Orrery",
        recalibrate_result_text="You clean five planetary markers with soft chamois cloth. Smooth brass rotation renews your travel resolve.",
        required_tool="brass_astrolabe",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="artificer",
    ),
}

# Stargazer rank progression tiers
STARGAZER_RANKS: List[Dict[str, Any]] = [
    {
        "count": 0,
        "title": "Novice Gazer",
        "desc": "You hold no aligned orreries or star charts. Continental astrolabes remain dormant in your travels.",
    },
    {
        "count": 1,
        "title": "Apprentice Astrologer",
        "desc": "You have aligned your first provincial astrolabe. Basic star knowledge guides your compass.",
    },
    {
        "count": 2,
        "title": "Constellation Seeker",
        "desc": "Two provincial orreries track your celestial journeys. Shifting star paths appear clear to your eyes.",
    },
    {
        "count": 3,
        "title": "Astromancer",
        "desc": "Three continental astrolabes have been aligned with care. Intricate planetary charts yield to your gaze.",
    },
    {
        "count": 4,
        "title": "Master Stargazer",
        "desc": "Four provincial orreries are aligned with great skill. Your star navigation commands high respect.",
    },
    {
        "count": 5,
        "title": "High Astrologian",
        "desc": "All five provincial orreries are mastered with care. Complete planetary knowledge guides your hand.",
    },
    {
        "count": 6,
        "title": "Grand Royal Stargazer",
        "desc": "All continental orreries are aligned with skill. Supreme star mastery guides your craft.",
    },
]


def get_stargazer_rank(aligned_count: int) -> Dict[str, str]:
    """Determine Stargazer rank title and description from aligned orrery count."""
    best = STARGAZER_RANKS[0]
    for tier in STARGAZER_RANKS:
        if aligned_count >= tier["count"]:
            best = tier
    return {"title": str(best["title"]), "desc": str(best["desc"])}


def evaluate_orrery_progress(
    flags: Dict[str, Any],
    inventory: List[str],
    markers: List[str],
    current_scene: str = ""
) -> Dict[str, Any]:
    """Deterministic evaluation of celestial orreries, stargazer rank, and active lenses."""
    marker_set = {str(m).lower() for m in markers}
    aligned_count = 0
    active_lenses_count = 0
    active_masteries_count = 0
    orrery_list = []
    current_scene_orrery = None

    for o in ANCIENT_ORRERIES.values():
        is_aligned = bool(flags.get(f"orrery_aligned_{o.id}", False))
        has_lens = o.lens_marker.lower() in marker_set
        is_attuned = bool(flags.get(f"orrery_attuned_{o.id}", False))
        has_mastery = o.mastery_marker.lower() in marker_set

        if is_aligned:
            aligned_count += 1
        if has_lens:
            active_lenses_count += 1
        if has_mastery:
            active_masteries_count += 1

        if current_scene == o.chamber_scene:
            current_scene_orrery = o.id

        orrery_list.append(
            o.to_dict(
                is_aligned=is_aligned,
                has_lens=has_lens,
                is_attuned=is_attuned,
                has_mastery=has_mastery,
            )
        )

    rank_info = get_stargazer_rank(aligned_count)
    progress_pct = round((aligned_count / max(1, len(ANCIENT_ORRERIES))) * 100, 1)

    return {
        "orreries": orrery_list,
        "aligned_count": aligned_count,
        "total_orreries": len(ANCIENT_ORRERIES),
        "active_lenses_count": active_lenses_count,
        "active_masteries_count": active_masteries_count,
        "stargazer_rank": rank_info["title"],
        "rank_desc": rank_info["desc"],
        "progress_pct": progress_pct,
        "current_scene_orrery": current_scene_orrery,
    }


def get_orrery_progress(state: Any) -> Dict[str, Any]:
    """Compute deterministic orrery progress and stargazer rank from GameState."""
    flags = state.world_flags if hasattr(state, "world_flags") else getattr(state, "flags", {})
    char = getattr(state, "character", None)
    inv = getattr(char, "inventory", []) if char else []
    markers = getattr(char, "markers", []) if char else []
    current_scene = getattr(state, "current_scene", "")
    return evaluate_orrery_progress(flags, inv, markers, current_scene)


def get_orrery_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic astrolabe alignment, field constellation attunement, and chamber recalibration affordances."""
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

    # Generic astronomical instruments that satisfy optical requirements
    astronomical_tools = {
        "brass_astrolabe",
        "astrolabe",
        "item_astrolabe",
        "celestial_lens",
        "telescope",
        "sextant",
        "star_chart",
        "spyglass",
        "surveyor_lens",
        "crystal_prism",
    }
    has_any_astronomical_tool = any(t in inv_list for t in astronomical_tools) or any(
        any(k in item for k in ["astrolabe", "lens", "telescope", "sextant", "spyglass", "prism", "stargazer", "optics"])
        for item in inv_list
    )

    # 1. Chamber Astrolabe Alignment and Recalibration
    for o in ANCIENT_ORRERIES.values():
        if scene_id == o.chamber_scene:
            is_aligned = bool(world_flags.get(f"orrery_aligned_{o.id}", False))
            is_attuned = bool(world_flags.get(f"orrery_attuned_{o.id}", False))

            if not is_aligned:
                # 7-axis qualification:
                # 1. Has specific tool or generic astronomical tool
                # 2. Has relevant traits (stargazer, astrologer, navigator, scholar, etc.)
                # 3. Has high attribute (wits >= 14, cunning >= 14, presence >= 14, or alternate_attr)
                # 4. Has relevant skills (lore, cunning, athletics >= 2)
                # 5. Has physical stamina (stamina >= 2)
                has_tool = (o.required_tool.lower() in inv_list) or has_any_astronomical_tool
                has_trait = (o.alternate_trait.lower() in traits_list) or any(
                    t in traits_list
                    for t in [
                        "stargazer",
                        "astronomer",
                        "astrologer",
                        "navigator",
                        "scholar",
                        "artificer",
                        "noble",
                        "sailor",
                        "focused",
                        "wise",
                        "cautious",
                    ]
                )
                attr_val = character.get_attribute(o.alternate_attribute)
                has_attr = (attr_val >= o.alternate_attr_val) or (
                    character.get_attribute("wits") >= 14
                    or character.get_attribute("cunning") >= 14
                    or character.get_attribute("presence") >= 14
                )
                has_skill = (
                    skills_dict.get("lore", 0) >= 2
                    or skills_dict.get("cunning", 0) >= 2
                    or skills_dict.get("athletics", 0) >= 2
                )
                has_stam = getattr(character, "stamina", 0) >= 2

                if has_tool or has_trait or has_attr or has_skill or has_stam:
                    affordances.append(
                        Action(
                            id=o.align_action_id,
                            label=o.align_action_label,
                            category="exploration",
                            effects=[
                                {"set_flag": {"flag": f"orrery_aligned_{o.id}", "value": True}},
                                {"add_marker": o.lens_marker},
                                {"add_marker": o.mastery_marker},
                                {"modify_stamina": 3},
                                {"log_event": o.align_result_text},
                            ],
                            result_text=o.align_result_text,
                            risk="low",
                            stamina_cost=0,
                        )
                    )
            elif is_attuned:
                # Can recalibrate and polish armillary sphere bearings at chamber scene
                affordances.append(
                    Action(
                        id=o.recalibrate_action_id,
                        label=o.recalibrate_action_label,
                        category="exploration",
                        effects=[
                            {"set_flag": {"flag": f"orrery_attuned_{o.id}", "value": False}},
                            {"modify_stamina": 2},
                            {"log_event": o.recalibrate_result_text},
                        ],
                        result_text=o.recalibrate_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    # 2. Field Constellation Attunement anywhere in the continental world
    for o in ANCIENT_ORRERIES.values():
        if o.lens_marker.lower() in marker_list:
            is_attuned = bool(world_flags.get(f"orrery_attuned_{o.id}", False))
            if not is_attuned:
                affordances.append(
                    Action(
                        id=o.attune_action_id,
                        label=o.attune_action_label,
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": f"orrery_attuned_{o.id}", "value": True}},
                            {"add_marker": f"marker_attuned_{o.id}"},
                            {"modify_stamina": 3},
                            {"log_event": o.attune_result_text},
                        ],
                        result_text=o.attune_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    return affordances
