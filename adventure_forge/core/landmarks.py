"""Milestone 29: Continental Survey Landmarks, Lookout Panoramas & Master Cartographer System.

Provides 6 Canonical Apex Landmarks situated at regional overlook summits and crossroads,
7-axis survey affordances yielding regional terrain mastery and topographical charts,
dynamic field chart study, overlook triangulation renewals, and Grand Royal Cartographer rank progression.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class SurveyLandmark:
    """A continental apex landmark with dedicated overlook summit, regional domain, and survey chart."""
    id: str
    name: str
    province: str
    overlook_scene: str
    icon: str
    domain: str
    description: str
    survey_action_id: str
    survey_action_label: str       # Exactly 1 to 3 words
    survey_result_text: str
    survey_marker: str
    mastery_marker: str
    study_action_id: str
    study_action_label: str        # Exactly 1 to 3 words
    study_result_text: str
    triangulate_action_id: str
    triangulate_action_label: str  # Exactly 1 to 3 words
    triangulate_result_text: str
    required_tool: str
    alternate_attribute: str
    alternate_attr_val: int
    alternate_trait: str

    def to_dict(
        self,
        is_surveyed: bool = False,
        has_chart: bool = False,
        is_studied: bool = False,
        has_mastery: bool = False,
    ) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "overlook_scene": self.overlook_scene,
            "icon": self.icon,
            "domain": self.domain,
            "description": self.description,
            "survey_action_id": self.survey_action_id,
            "survey_action_label": self.survey_action_label,
            "survey_marker": self.survey_marker,
            "mastery_marker": self.mastery_marker,
            "study_action_id": self.study_action_id,
            "study_action_label": self.study_action_label,
            "triangulate_action_id": self.triangulate_action_id,
            "triangulate_action_label": self.triangulate_action_label,
            "required_tool": self.required_tool,
            "alternate_attribute": self.alternate_attribute,
            "alternate_attr_val": self.alternate_attr_val,
            "alternate_trait": self.alternate_trait,
            "is_surveyed": is_surveyed,
            "has_chart": has_chart,
            "is_studied": is_studied,
            "has_mastery": has_mastery,
        }


SURVEY_LANDMARKS: Dict[str, SurveyLandmark] = {
    "landmark_reach_pass": SurveyLandmark(
        id="landmark_reach_pass",
        name="Eagle Wing Pass Apex",
        province="The Reach",
        overlook_scene="reach_high_pass_overlook",
        icon="🏔️",
        domain="Mountain Passes & Jagged Crags",
        description="High granite ledges overlook rugged mountain canyons. Bitter northern gales buffet the frozen ramparts.",
        survey_action_id="landmark_survey_reach_pass",
        survey_action_label="Survey Reach Apex",
        survey_result_text="You survey steep granite ledges through your spyglass. Cold northern breezes assist your precise observations.",
        survey_marker="marker_survey_reach_pass",
        mastery_marker="marker_mastery_reach",
        study_action_id="landmark_study_reach_pass",
        study_action_label="Study Reach Chart",
        study_result_text="You review the mountain chart with care. Dangerous high passes appear manageable in your memory.",
        triangulate_action_id="landmark_triangulate_reach_pass",
        triangulate_action_label="Triangulate Reach",
        triangulate_result_text="You align your brass compass with distant icy ridges. Fresh surveying observations restore your alpine resolve.",
        required_tool="item_spyglass",
        alternate_attribute="agility",
        alternate_attr_val=14,
        alternate_trait="pathfinder",
    ),
    "landmark_scorchwaste_dune": SurveyLandmark(
        id="landmark_scorchwaste_dune",
        name="Razor Dune Ridge Panorama",
        province="The Scorchwaste",
        overlook_scene="scorchwaste_dune_ridge_overlook",
        icon="🏜️",
        domain="Sandswept Wastes & Shifting Dunes",
        description="Sun-baked stone cliffs overlook shifting sandy plateaus. Dry desert winds sweep across the hot basin floor.",
        survey_action_id="landmark_survey_scorchwaste_dune",
        survey_action_label="Survey Dune Ridge",
        survey_result_text="You survey the shifting desert dunes through your instrument. Arid travel paths appear clearly upon your chart.",
        survey_marker="marker_survey_scorchwaste_dune",
        mastery_marker="marker_mastery_scorchwaste",
        study_action_id="landmark_study_scorchwaste_dune",
        study_action_label="Study Dune Chart",
        study_result_text="You review the desert cartography with care. Perilous sandswept tracks appear clear in your memory.",
        triangulate_action_id="landmark_triangulate_scorchwaste_dune",
        triangulate_action_label="Triangulate Dunes",
        triangulate_result_text="You align the compass with desert spires. Clear navigational lines steady your travel resolve.",
        required_tool="continental_compass",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="far_sighted",
    ),
    "landmark_sunken_shrine": SurveyLandmark(
        id="landmark_sunken_shrine",
        name="Drowned Shrine Vista",
        province="The Sunken Hollows",
        overlook_scene="sunken_hollows_drowned_temple_overlook",
        icon="🌊",
        domain="Abyssal Caves & Submerged Ruins",
        description="High limestone shelves overlook submerged stone columns. Deep oceanic currents flow through the quiet grotto.",
        survey_action_id="landmark_survey_sunken_shrine",
        survey_action_label="Survey Drowned Vista",
        survey_result_text="You record the tidal contours of sunken temple ruins. Clear underwater passages emerge upon your marine chart.",
        survey_marker="marker_survey_sunken_shrine",
        mastery_marker="marker_mastery_sunken_hollows",
        study_action_id="landmark_study_sunken_shrine",
        study_action_label="Study Abyssal Chart",
        study_result_text="You consult the charted tidal routes. Submerged cavern passages feel familiar and manageable.",
        triangulate_action_id="landmark_triangulate_sunken_shrine",
        triangulate_action_label="Triangulate Grotto",
        triangulate_result_text="You inspect glowing coral spires across the water. Clear maritime sightings renew your deep resolve.",
        required_tool="parchment_map",
        alternate_attribute="intellect",
        alternate_attr_val=14,
        alternate_trait="scout",
    ),
    "landmark_high_court_spire": SurveyLandmark(
        id="landmark_high_court_spire",
        name="White Spire Parapet Zenith",
        province="The High Court",
        overlook_scene="high_court_high_spire_overlook",
        icon="🏰",
        domain="Palatine Spikes & Royal Plazas",
        description="Carved white parapets overlook ducal palace courtyards. Imperial banners snap in the crisp royal breeze.",
        survey_action_id="landmark_survey_high_court_spire",
        survey_action_label="Survey White Spire",
        survey_result_text="You map the palace bastions and manicured lanes. Noble patrol gates are documented with precision.",
        survey_marker="marker_survey_high_court_spire",
        mastery_marker="marker_mastery_high_court",
        study_action_id="landmark_study_high_court_spire",
        study_action_label="Study Spire Chart",
        study_result_text="You inspect the royal city survey with care. Secret palace corridors are recorded with precision.",
        triangulate_action_id="landmark_triangulate_high_court_spire",
        triangulate_action_label="Triangulate Spire",
        triangulate_result_text="You sight palace parapets against the high sky. Fresh courtly observations steady your pulse.",
        required_tool="item_spyglass",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="surveyor",
    ),
    "landmark_lowlands_bell": SurveyLandmark(
        id="landmark_lowlands_bell",
        name="Harbor Bell Tower Crow's Nest",
        province="The Lowlands",
        overlook_scene="lowlands_bell_tower_overlook",
        icon="🔔",
        domain="Canal Networks & Foggy Harbors",
        description="Wooden lookout platforms overlook river docks. Heavy bronze bells remain silent in morning mist.",
        survey_action_id="landmark_survey_lowlands_bell",
        survey_action_label="Survey Harbor Tower",
        survey_result_text="You sketch coastal docks and winding waterways. Foggy river channels are recorded with nautical care.",
        survey_marker="marker_survey_lowlands_bell",
        mastery_marker="marker_mastery_lowlands",
        study_action_id="landmark_study_lowlands_bell",
        study_action_label="Study Harbor Chart",
        study_result_text="You review the coastal river survey. Lowland marsh roads and foggy inlets become crystal clear.",
        triangulate_action_id="landmark_triangulate_lowlands_bell",
        triangulate_action_label="Triangulate Harbor",
        triangulate_result_text="You align your compass with the outer sea buoy. Accurate harbor bearings steady your mind.",
        required_tool="continental_compass",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="eagle_eyed",
    ),
    "landmark_crossroads_watch": SurveyLandmark(
        id="landmark_crossroads_watch",
        name="Grand Crossroads Watchpost",
        province="Central Crossroads",
        overlook_scene="bazaar_center",
        icon="🧭",
        domain="Continental Arteries & Caravan Termini",
        description="The high watchpost overlooks the central plaza. Five continental roads meet beside busy market stalls.",
        survey_action_id="landmark_survey_crossroads_watch",
        survey_action_label="Survey Crossroads Apex",
        survey_result_text="You record the meeting of five roads. Continental trade routes connect in logical order.",
        survey_marker="marker_survey_crossroads_watch",
        mastery_marker="marker_mastery_crossroads",
        study_action_id="landmark_study_crossroads_watch",
        study_action_label="Study Crossroads Chart",
        study_result_text="You inspect the crossroads trail chart. All five provincial highways connect in logical order.",
        triangulate_action_id="landmark_triangulate_crossroads_watch",
        triangulate_action_label="Triangulate Crossroads",
        triangulate_result_text="You check bearings toward all five provincial gates. Perfect crossroads alignment steadies your journey.",
        required_tool="parchment_map",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="pathfinder",
    ),
}

# Cartographer rank progression tiers
CARTOGRAPHER_RANKS: List[Dict[str, Any]] = [
    {
        "count": 0,
        "title": "Uncharted Drifter",
        "desc": "You hold no surveyed landmarks or charts. Continental trails remain completely uncharted in your journey.",
    },
    {
        "count": 1,
        "title": "Regional Scout",
        "desc": "You have mapped your first continental overlook. Regional terrain patterns become clear in your mind.",
    },
    {
        "count": 2,
        "title": "Topographer",
        "desc": "Two apex landmarks are charted with care. Your understanding of continental trails expands with each survey.",
    },
    {
        "count": 3,
        "title": "Continental Cartographer",
        "desc": "Three regional panoramas are surveyed. Your travel routes across the provinces are secure and reliable.",
    },
    {
        "count": 4,
        "title": "Grand Surveyor",
        "desc": "Four provincial heights are mapped with care. Your detailed charts guide traveling caravans along dangerous provincial roads.",
    },
    {
        "count": 5,
        "title": "Master of Five Panoramas",
        "desc": "All five provincial apex landmarks are surveyed. You hold complete regional terrain knowledge across the realm.",
    },
    {
        "count": 6,
        "title": "Grand Royal Cartographer",
        "desc": "All continental landmarks are charted with care. Your royal maps record every horizon across the land.",
    },
]


def get_cartographer_rank(surveyed_count: int) -> Dict[str, str]:
    """Determine Cartographer rank title and description from surveyed landmark count."""
    best = CARTOGRAPHER_RANKS[0]
    for tier in CARTOGRAPHER_RANKS:
        if surveyed_count >= tier["count"]:
            best = tier
    return {"title": str(best["title"]), "desc": str(best["desc"])}


def evaluate_landmarks_progress(
    flags: Dict[str, Any],
    inventory: List[str],
    markers: List[str],
    current_scene: str = ""
) -> Dict[str, Any]:
    """Deterministic evaluation of survey landmarks, cartographer rank, and active charts."""
    marker_set = {str(m).lower() for m in markers}
    surveyed_count = 0
    active_charts_count = 0
    active_masteries_count = 0
    landmark_list = []
    current_scene_landmark = None

    for lm in SURVEY_LANDMARKS.values():
        is_surveyed = bool(flags.get(f"landmark_surveyed_{lm.id}", False))
        has_chart = lm.survey_marker.lower() in marker_set
        is_studied = bool(flags.get(f"landmark_studied_{lm.id}", False))
        has_mastery = lm.mastery_marker.lower() in marker_set

        if is_surveyed:
            surveyed_count += 1
        if has_chart:
            active_charts_count += 1
        if has_mastery:
            active_masteries_count += 1

        if current_scene == lm.overlook_scene:
            current_scene_landmark = lm.id

        landmark_list.append(
            lm.to_dict(
                is_surveyed=is_surveyed,
                has_chart=has_chart,
                is_studied=is_studied,
                has_mastery=has_mastery,
            )
        )

    rank_info = get_cartographer_rank(surveyed_count)
    progress_pct = round((surveyed_count / max(1, len(SURVEY_LANDMARKS))) * 100, 1)

    return {
        "landmarks": landmark_list,
        "surveyed_count": surveyed_count,
        "total_landmarks": len(SURVEY_LANDMARKS),
        "active_charts_count": active_charts_count,
        "active_masteries_count": active_masteries_count,
        "cartographer_rank": rank_info["title"],
        "rank_desc": rank_info["desc"],
        "progress_pct": progress_pct,
        "current_scene_landmark": current_scene_landmark,
    }


def get_landmarks_progress(state: Any) -> Dict[str, Any]:
    """Compute deterministic landmark progress and cartographer rank from GameState."""
    flags = state.world_flags if hasattr(state, "world_flags") else getattr(state, "flags", {})
    char = getattr(state, "character", None)
    inv = getattr(char, "inventory", []) if char else []
    markers = getattr(char, "markers", []) if char else []
    current_scene = getattr(state, "current_scene", "")
    return evaluate_landmarks_progress(flags, inv, markers, current_scene)


def get_landmark_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic landmark survey, field chart study, and overlook triangulation affordances."""
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

    # Generic surveying tools that satisfy instrument requirements
    survey_instruments = {"item_spyglass", "spyglass", "continental_compass", "compass", "parchment_map", "map", "survey_tools"}
    has_any_instrument = any(inst in inv_list for inst in survey_instruments)

    # 1. Overlook Summit Surveys and Triangulation Renewals
    for lm in SURVEY_LANDMARKS.values():
        if scene_id == lm.overlook_scene:
            is_surveyed = bool(world_flags.get(f"landmark_surveyed_{lm.id}", False))
            is_studied = bool(world_flags.get(f"landmark_studied_{lm.id}", False))

            if not is_surveyed:
                # 7-axis qualification:
                # 1. Has specific or generic tool
                # 2. Has trait (pathfinder, scout, surveyor, eagle_eyed, far_sighted)
                # 3. Has high attribute (>= 14)
                # 4. Has relevant skill (cunning, lore, perception >= 2)
                # 5. Has stamina >= 2
                has_tool = (lm.required_tool.lower() in inv_list) or has_any_instrument
                has_trait = (lm.alternate_trait.lower() in traits_list) or any(
                    t in traits_list for t in ["pathfinder", "scout", "surveyor", "eagle_eyed", "far_sighted"]
                )
                attr_val = character.get_attribute(lm.alternate_attribute)
                has_attr = attr_val >= lm.alternate_attr_val
                has_skill = (
                    skills_dict.get("cunning", 0) >= 2
                    or skills_dict.get("lore", 0) >= 2
                    or skills_dict.get("perception", 0) >= 2
                )
                has_stam = getattr(character, "stamina", 0) >= 2

                if has_tool or has_trait or has_attr or has_skill or has_stam:
                    affordances.append(
                        Action(
                            id=lm.survey_action_id,
                            label=lm.survey_action_label,
                            category="exploration",
                            effects=[
                                {"set_flag": {"flag": f"landmark_surveyed_{lm.id}", "value": True}},
                                {"add_marker": lm.survey_marker},
                                {"add_marker": lm.mastery_marker},
                                {"modify_stamina": 3},
                                {"log_event": lm.survey_result_text},
                            ],
                            result_text=lm.survey_result_text,
                            risk="low",
                            stamina_cost=0,
                        )
                    )
            elif is_studied:
                # Can re-triangulate and renew at the overlook
                affordances.append(
                    Action(
                        id=lm.triangulate_action_id,
                        label=lm.triangulate_action_label,
                        category="exploration",
                        effects=[
                            {"set_flag": {"flag": f"landmark_studied_{lm.id}", "value": False}},
                            {"modify_stamina": 2},
                            {"log_event": lm.triangulate_result_text},
                        ],
                        result_text=lm.triangulate_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    # 2. Field Chart Study anywhere in the continental world
    for lm in SURVEY_LANDMARKS.values():
        if lm.survey_marker.lower() in marker_list:
            is_studied = bool(world_flags.get(f"landmark_studied_{lm.id}", False))
            if not is_studied:
                affordances.append(
                    Action(
                        id=lm.study_action_id,
                        label=lm.study_action_label,
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": f"landmark_studied_{lm.id}", "value": True}},
                            {"add_marker": f"marker_studied_{lm.id}"},
                            {"modify_stamina": 3},
                            {"log_event": lm.study_result_text},
                        ],
                        result_text=lm.study_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    return affordances
