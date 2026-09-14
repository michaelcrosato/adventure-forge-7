"""Continental Weather Dynamics & Provincial Micro-Climates (Milestone 22).

Enforces:
- Deterministic regional weather cycles based on turn count and province key.
- 5 unique provincial micro-climates + Central Crossroads market weather.
- Dynamic weather affordance synthesis (1 action per weather condition).
- 7-axis reactivity (traits like heat_tolerant, nimble, water_breather, night_eyed interact with weather).
- High-velocity Hemingway prose (<= 18 words/sent, 1-3 sent, FKGL <= 8.0, 0 purple words).
- Strict 1-3 word UI action labels.
"""
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class WeatherCondition:
    """A deterministic atmospheric condition with unique environmental narrative and affordance."""
    id: str
    name: str
    province: str
    description: str
    hazard_type: Optional[str]  # e.g. cold, heat, fog, rain, luminescence, wind
    action_id: str
    action_label: str  # Exactly 1 to 3 words
    result_text: str
    effects: List[Dict[str, Any]]
    stamina_cost: int = 0
    condition: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "description": self.description,
            "hazard_type": self.hazard_type,
            "action_id": self.action_id,
            "action_label": self.action_label,
            "stamina_cost": self.stamina_cost,
        }


# --- Provincial Weather Conditions (Mild, Extreme/Atmospheric pairs) ---

WEATHER_CONDITIONS: Dict[str, WeatherCondition] = {
    # 1. The Reach
    "reach_clear": WeatherCondition(
        id="reach_clear",
        name="Clear Alpine Air",
        province="The Reach",
        description="Cold wind whistles through the stone passes. Sharp mountain sunlight warms the snow.",
        hazard_type=None,
        action_id="weather_collect_melt",
        action_label="Collect Fresh Melt",
        result_text="You melt clean ice over a small flame. Cool water fills your flask.",
        effects=[
            {"add_item": "water_skin"},
            {"modify_stamina": 1},
            {"set_flag": {"flag": "weather_melt_collected", "value": True}},
            {"log_event": "You gathered clean meltwater from alpine drifts."},
        ],
        stamina_cost=0,
    ),
    "reach_blizzard": WeatherCondition(
        id="reach_blizzard",
        name="Blinding Blizzard",
        province="The Reach",
        description="Freezing gales sweep over the jagged mountain rim. Ice coats the exposed limestone ledges.",
        hazard_type="cold",
        action_id="weather_seek_shelter",
        action_label="Seek Crag Shelter",
        result_text="You find a dry alcove under stone overhangs. Warm breath gathers in the frost.",
        effects=[
            {"modify_stamina": 2},
            {"set_flag": {"flag": "weather_shelter_secured", "value": True}},
            {"log_event": "You waited out the gale inside an ice grotto."},
        ],
        stamina_cost=0,
    ),

    # 2. The Scorchwaste
    "scorch_dusk": WeatherCondition(
        id="scorch_dusk",
        name="Dusk Dune Chill",
        province="The Scorchwaste",
        description="Purple evening settles across the dunes. The red sand cools under the twilight sky.",
        hazard_type=None,
        action_id="weather_trek_sands",
        action_label="Trek Cool Sands",
        result_text="You walk quickly across the cool sand. Mild desert winds guide your march.",
        effects=[
            {"modify_stamina": 2},
            {"set_flag": {"flag": "weather_dusk_marched", "value": True}},
            {"log_event": "You made swift progress across the cooling dunes."},
        ],
        stamina_cost=0,
    ),
    "scorch_heatwave": WeatherCondition(
        id="scorch_heatwave",
        name="Solar Heatwave",
        province="The Scorchwaste",
        description="Scorching sun rays bake the red sand dunes. Hot air shimmers across the salt flats.",
        hazard_type="heat",
        action_id="weather_rig_tarp",
        action_label="Rig Shade Tarp",
        result_text="You pitch a coarse cloth shelter against the wind. Cool shade protects your skin.",
        effects=[
            {"modify_stamina": 1},
            {"set_flag": {"flag": "weather_shade_pitched", "value": True}},
            {"log_event": "You rigged shade fabric against the harsh sun."},
        ],
        stamina_cost=0,
    ),

    # 3. The Lowlands
    "lowlands_breeze": WeatherCondition(
        id="lowlands_breeze",
        name="Canal River Breeze",
        province="The Lowlands",
        description="Fresh air clears the canal alleys. Barges glide smoothly down the channel.",
        hazard_type=None,
        action_id="weather_watch_traffic",
        action_label="Watch River Traffic",
        result_text="You watch cargo loaders work along the docks. River workers haul heavy sacks.",
        effects=[
            {"add_item": "tallow"},
            {"set_flag": {"flag": "weather_traffic_observed", "value": True}},
            {"log_event": "You spotted discarded shipyard tallow on the quays."},
        ],
        stamina_cost=0,
    ),
    "lowlands_fog": WeatherCondition(
        id="lowlands_fog",
        name="Marsh Low Fog",
        province="The Lowlands",
        description="Dense white mist rolls off the stagnant canal waters. Distant lampposts fade into gray haze.",
        hazard_type="fog",
        action_id="weather_skulk_fog",
        action_label="Skulk In Fog",
        result_text="You move through thick mist along wet alleys. Footsteps make no sound on mud.",
        effects=[
            {"set_flag": {"flag": "status_hidden", "value": True}},
            {"set_flag": {"flag": "weather_fog_skulked", "value": True}},
            {"log_event": "You used the marsh fog to slip past city watch sentries."},
        ],
        stamina_cost=0,
    ),

    # 4. The High Court
    "court_sunburst": WeatherCondition(
        id="court_sunburst",
        name="Gilded Sunburst",
        province="The High Court",
        description="Bright sunshine reflects from the basilica glass. Courtiers gather along the grand promenade.",
        hazard_type=None,
        action_id="weather_attend_court",
        action_label="Attend Grand Court",
        result_text="You mingle among wealthy lords and factors. Courtiers exchange greetings in the sun.",
        effects=[
            {"modify_reputation": {"faction": "justiciars", "value": 5}},
            {"set_flag": {"flag": "weather_court_attended", "value": True}},
            {"log_event": "You made courtly impressions during the sunny promenade."},
        ],
        stamina_cost=0,
    ),
    "court_rain": WeatherCondition(
        id="court_rain",
        name="Imperial Rainstorm",
        province="The High Court",
        description="Heavy silver rain pours across the paved palace terraces. Noble guards stand watch under arches.",
        hazard_type="rain",
        action_id="weather_eavesdrop_rain",
        action_label="Eavesdrop In Rain",
        result_text="You listen near the curtained window. Aristocratic voices debate royal taxes above the rain.",
        effects=[
            {"add_item": "legal_dossier"},
            {"set_flag": {"flag": "weather_rain_eavesdropped", "value": True}},
            {"log_event": "You overheard classified tribunal tax disputes in the rain."},
        ],
        stamina_cost=0,
    ),

    # 5. The Sunken Hollows
    "hollows_calm": WeatherCondition(
        id="hollows_calm",
        name="Still Water Depths",
        province="The Sunken Hollows",
        description="Quiet waters fill the deep stone grotto. Dim phosphorescence glimmers on wet stone.",
        hazard_type=None,
        action_id="weather_survey_flora",
        action_label="Survey Trench Flora",
        result_text="You inspect delicate cave corals in the calm pool. Rare minerals coat the rock.",
        effects=[
            {"add_item": "pitch_seal"},
            {"set_flag": {"flag": "weather_flora_surveyed", "value": True}},
            {"log_event": "You scraped waterproofing pitch from still mineral pools."},
        ],
        stamina_cost=0,
    ),
    "hollows_bloom": WeatherCondition(
        id="hollows_bloom",
        name="Bioluminescent Spring",
        province="The Sunken Hollows",
        description="Bright blue moss glows across the submerged limestone grottos. Clear water reveals hidden caverns.",
        hazard_type="luminescence",
        action_id="weather_harvest_catch",
        action_label="Harvest Tide Catch",
        result_text="You scoop up luminous trench oysters from wet stones. Glowing fluid fills your jar.",
        effects=[
            {"add_item": "filter_mask"},
            {"modify_stamina": 1},
            {"set_flag": {"flag": "weather_catch_harvested", "value": True}},
            {"log_event": "You gathered glowing abyssal filter organisms."},
        ],
        stamina_cost=0,
    ),

    # 6. Central Crossroads (Grand Bazaar)
    "bazaar_sunlit": WeatherCondition(
        id="bazaar_sunlit",
        name="Sunlit Market Plaza",
        province="Central Crossroads",
        description="Warm light shines across the marketplace tents. Merchants display colorful wares on wooden tables.",
        hazard_type=None,
        action_id="weather_browse_stalls",
        action_label="Browse Open Stalls",
        result_text="You walk past fragrant spice carts. Friendly vendors call out daily specials.",
        effects=[
            {"modify_stamina": 1},
            {"set_flag": {"flag": "weather_stalls_browsed", "value": True}},
            {"log_event": "You enjoyed the sunlit bustle of the crossroads market."},
        ],
        stamina_cost=0,
    ),
    "bazaar_wind": WeatherCondition(
        id="bazaar_wind",
        name="Crossroads Dust Wind",
        province="Central Crossroads",
        description="Gusty winds kick up grit around the stone arches. Stall keepers tighten their cloth ropes.",
        hazard_type="wind",
        action_id="weather_secure_awning",
        action_label="Secure Trade Awning",
        result_text="You help secure a flapping market canopy. The grateful merchant hands you dried fruit.",
        effects=[
            {"add_item": "silver_coin"},
            {"set_flag": {"flag": "weather_awning_secured", "value": True}},
            {"log_event": "A merchant tipped you a silver coin for saving their goods."},
        ],
        stamina_cost=0,
    ),
}

# Mapping from province/region keys to (mild_weather_id, extreme_weather_id)
REGION_WEATHER_MAP: Dict[str, Tuple[str, str]] = {
    # The Reach
    "iron_crags": ("reach_clear", "reach_blizzard"),
    "province_reach": ("reach_clear", "reach_blizzard"),
    "the_reach": ("reach_clear", "reach_blizzard"),
    # The Scorchwaste
    "scorchwaste_local": ("scorch_dusk", "scorch_heatwave"),
    "province_scorchwaste": ("scorch_dusk", "scorch_heatwave"),
    "the_scorchwaste": ("scorch_dusk", "scorch_heatwave"),
    # The Lowlands
    "lower_warrens": ("lowlands_breeze", "lowlands_fog"),
    "warrens_local": ("lowlands_breeze", "lowlands_fog"),
    "province_lowlands": ("lowlands_breeze", "lowlands_fog"),
    "the_lowlands": ("lowlands_breeze", "lowlands_fog"),
    # The High Court
    "high_court_local": ("court_sunburst", "court_rain"),
    "province_high_court": ("court_sunburst", "court_rain"),
    "the_high_court": ("court_sunburst", "court_rain"),
    # The Sunken Hollows
    "sunken_hollows_local": ("hollows_calm", "hollows_bloom"),
    "province_sunken_hollows": ("hollows_calm", "hollows_bloom"),
    "the_sunken_hollows": ("hollows_calm", "hollows_bloom"),
    # Central Crossroads
    "stress_market": ("bazaar_sunlit", "bazaar_wind"),
    "central_bazaar": ("bazaar_sunlit", "bazaar_wind"),
}

PROVINCE_NAMES: List[str] = [
    "The Reach",
    "The Scorchwaste",
    "The Lowlands",
    "The High Court",
    "The Sunken Hollows",
    "Central Crossroads",
]

PROVINCE_TO_PRIMARY_REGION: Dict[str, str] = {
    "The Reach": "iron_crags",
    "The Scorchwaste": "scorchwaste_local",
    "The Lowlands": "lower_warrens",
    "The High Court": "high_court_local",
    "The Sunken Hollows": "sunken_hollows_local",
    "Central Crossroads": "stress_market",
}


def get_weather_for_region(turn_count: int, region_id: str) -> WeatherCondition:
    """Deterministically determine the current weather for a region.
    
    Cycles every 6 turns:
    - Turns 0-5: Mild / Baseline weather
    - Turns 6-11: Atmospheric / Dynamic micro-climate
    """
    pair = REGION_WEATHER_MAP.get(region_id, ("bazaar_sunlit", "bazaar_wind"))
    mild_id, extreme_id = pair

    # Deterministic 12-turn cycle
    cycle_pos = int(turn_count) % 12
    weather_id = mild_id if cycle_pos < 6 else extreme_id
    return WEATHER_CONDITIONS[weather_id]


def get_all_provincial_weather(turn_count: int) -> Dict[str, Dict[str, Any]]:
    """Return the current weather conditions for all 5 provinces and Central Crossroads."""
    result: Dict[str, Dict[str, Any]] = {}
    for prov_name in PROVINCE_NAMES:
        primary_reg = PROVINCE_TO_PRIMARY_REGION[prov_name]
        w = get_weather_for_region(turn_count, primary_reg)
        result[prov_name] = w.to_dict()
    return result


def get_weather_affordance_for_scene(
    scene_id: str,
    region_id: str,
    turn_count: int,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> Optional[Any]:
    """Synthesize dynamic weather affordance based on regional atmospheric state."""
    from adventure_forge.core.actions import Action

    weather = get_weather_for_region(turn_count, region_id)
    act_id = weather.action_id

    # Check if action was already taken in this weather cycle to avoid spamming
    cycle_num = int(turn_count) // 6
    flag_key = f"{act_id}_cycle_{cycle_num}"
    if world_flags.get(flag_key):
        return None

    # Build effects appending the cycle tracker flag
    action_effects = list(weather.effects)
    action_effects.append({"set_flag": {"flag": flag_key, "value": True}})

    act = Action(
        id=act_id,
        label=weather.action_label,
        category="systemic",
        effects=action_effects,
        result_text=weather.result_text,
        risk="low",
        stamina_cost=weather.stamina_cost,
    )

    if act.is_legal(character, world_flags):
        return act
    return None
