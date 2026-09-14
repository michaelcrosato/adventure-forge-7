"""Continental Chartered Transit & Regional Caravan Network (Milestone 20).

Provides pure, deterministic fast-travel connections linking the Central Bazaar
to each of the five provincial entry points:
- The Reach: Highland Cable Lift (Central Bazaar <-> Dunwall Fort Gate)
- The Lowlands: Canal River Barge (Central Bazaar <-> Oakhaven Port Gate)
- The Scorchwaste: Desert Silt-Skiff (Central Bazaar <-> Ashen Gate)
- The High Court: Imperial High Carriage (Central Bazaar <-> Grand Basilica Gate)
- The Sunken Hollows: Submersible Siphon Ferry (Central Bazaar <-> Glow Grotto Gate)

All routes enforce 7-axis reactivity (currency, traits, backgrounds, attributes, or gear),
consume stamina, update world route flags, and award the Continental Wayfarer mastery.
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.conditions import evaluate_condition


@dataclass(frozen=True)
class TransitRoute:
    """A deterministic chartered transit connection between continental hubs."""
    id: str
    name: str
    origin_scene: str
    destination_scene: str
    destination_province: str
    action_id: str
    action_label: str  # Exactly 1 to 3 words
    stamina_cost: int
    condition: Dict[str, Any]
    result_text: str  # 1-2 sentences, <= 18 words/sent
    route_flag: str
    category: str = "movement"

    def is_available(self, character: CharacterSheet, world_flags: Dict[str, Any]) -> bool:
        """Check if character can board this transit connection."""
        if character.stamina < self.stamina_cost:
            return False
        return evaluate_condition(self.condition, character, world_flags)

    def build_effects(self, world_flags: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Construct effects: route recording, mastery check, and scene transition."""
        effects: List[Dict[str, Any]] = [
            {"set_flag": {"flag": self.route_flag, "value": True}},
            {"log_event": f"Traveled via {self.name} to {self.destination_province}."},
        ]

        # Check for Continental Wayfarer milestone (all 5 provincial routes traveled)
        all_routes = ["route_reach", "route_lowlands", "route_scorchwaste", "route_high_court", "route_sunken_hollows"]
        completed = sum(1 for r in all_routes if world_flags.get(r, False) or r == self.route_flag)

        if completed >= 5 and not world_flags.get("continental_wayfarer_unlocked", False):
            effects.append({"set_flag": {"flag": "continental_wayfarer_unlocked", "value": True}})
            effects.append({"add_marker": "continental_wayfarer"})
            effects.append({"log_event": "Continental Mastery Achieved: Continental Wayfarer!"})

        return effects

    def to_dict(self, traveled: bool = False) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "origin_scene": self.origin_scene,
            "destination_scene": self.destination_scene,
            "destination_province": self.destination_province,
            "action_id": self.action_id,
            "action_label": self.action_label,
            "stamina_cost": self.stamina_cost,
            "traveled": traveled,
            "route_flag": self.route_flag,
        }


CHARTERED_ROUTES: List[TransitRoute] = [
    # --- The Reach (Highland Cable Lift) ---
    TransitRoute(
        id="bazaar_to_reach",
        name="Highland Cable Lift",
        origin_scene="bazaar_center",
        destination_scene="reach_dunwall_fort_gate",
        destination_province="The Reach",
        action_id="transit_cable_to_reach",
        action_label="Board Cable Lift",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_item": "silver_coin"},
                {"has_item": "climbing_rope"},
                {"has_trait": "Mountain Scout"},
                {"has_trait": "nimble"},
                {"background_is": "Reachman"},
                {"background_is": "highland_scout"},
                {"has_marker": "scout_cloak"},
                {"min_attribute": {"attribute": "might", "value": 4}},
                {"min_skill": {"skill": "athletics", "value": 3}},
            ]
        },
        result_text="The heavy cable groans as the iron car climbs the cliff. Cold winds buffet the carriage.",
        route_flag="route_reach",
    ),
    TransitRoute(
        id="reach_to_bazaar",
        name="Highland Cable Lift",
        origin_scene="reach_dunwall_fort_gate",
        destination_scene="bazaar_center",
        destination_province="Central Crossroads",
        action_id="transit_cable_to_bazaar",
        action_label="Descend Cable Lift",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_item": "silver_coin"},
                {"has_item": "climbing_rope"},
                {"has_trait": "Mountain Scout"},
                {"has_trait": "nimble"},
                {"background_is": "Reachman"},
                {"background_is": "highland_scout"},
                {"has_marker": "scout_cloak"},
                {"min_attribute": {"attribute": "might", "value": 4}},
                {"min_skill": {"skill": "athletics", "value": 3}},
            ]
        },
        result_text="The iron car descends swiftly along the high steel cable. The bustling bazaar spreads below.",
        route_flag="route_reach",
    ),

    # --- The Lowlands (Canal River Barge) ---
    TransitRoute(
        id="bazaar_to_lowlands",
        name="Canal River Barge",
        origin_scene="bazaar_center",
        destination_scene="lowlands_oakhaven_port_gate",
        destination_province="The Lowlands",
        action_id="transit_barge_to_lowlands",
        action_label="Board River Barge",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_item": "silver_coin"},
                {"has_item": "tallow"},
                {"has_trait": "Street Drifter"},
                {"has_marker": "thief_signet"},
                {"background_is": "cutpurse"},
                {"ancestry_is": "Lowlander"},
                {"has_trait": "Shadow Walker"},
            ]
        },
        result_text="The barge slips smoothly down the canal. Murky water laps against the wooden hull.",
        route_flag="route_lowlands",
    ),
    TransitRoute(
        id="lowlands_to_bazaar",
        name="Canal River Barge",
        origin_scene="lowlands_oakhaven_port_gate",
        destination_scene="bazaar_center",
        destination_province="Central Crossroads",
        action_id="transit_barge_to_bazaar",
        action_label="Upstream River Barge",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_item": "silver_coin"},
                {"has_item": "tallow"},
                {"has_trait": "Street Drifter"},
                {"has_marker": "thief_signet"},
                {"background_is": "cutpurse"},
                {"ancestry_is": "Lowlander"},
                {"has_trait": "Shadow Walker"},
            ]
        },
        result_text="Draft beasts haul the river barge upstream. Stalls and stone arches rise into view.",
        route_flag="route_lowlands",
    ),

    # --- The Scorchwaste (Desert Silt-Skiff) ---
    TransitRoute(
        id="bazaar_to_scorchwaste",
        name="Desert Silt-Skiff",
        origin_scene="bazaar_center",
        destination_scene="scorchwaste_ashen_gate_gate",
        destination_province="The Scorchwaste",
        action_id="transit_skiff_to_scorchwaste",
        action_label="Board Silt Skiff",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_item": "silver_coin"},
                {"has_item": "desert_cowl"},
                {"has_trait": "Dune Strider"},
                {"background_is": "dune_strider"},
                {"ancestry_is": "Nomad"},
                {"has_marker": "nomad_sash"},
                {"has_trait": "heat_tolerant"},
                {"has_trait": "Sun Hardened"},
                {"has_item": "water_skin"},
            ]
        },
        result_text="Cloth sails catch the hot desert draft. The wooden skiff glides across red sand.",
        route_flag="route_scorchwaste",
    ),
    TransitRoute(
        id="scorchwaste_to_bazaar",
        name="Desert Silt-Skiff",
        origin_scene="scorchwaste_ashen_gate_gate",
        destination_scene="bazaar_center",
        destination_province="Central Crossroads",
        action_id="transit_skiff_to_bazaar",
        action_label="Skiff To Bazaar",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_item": "silver_coin"},
                {"has_item": "desert_cowl"},
                {"has_trait": "Dune Strider"},
                {"background_is": "dune_strider"},
                {"ancestry_is": "Nomad"},
                {"has_marker": "nomad_sash"},
                {"has_trait": "heat_tolerant"},
                {"has_trait": "Sun Hardened"},
                {"has_item": "water_skin"},
            ]
        },
        result_text="The skiff glides north away from the dunes. Cool cross-winds herald the crossroads.",
        route_flag="route_scorchwaste",
    ),

    # --- The High Court (Imperial High Carriage) ---
    TransitRoute(
        id="bazaar_to_high_court",
        name="Imperial High Carriage",
        origin_scene="bazaar_center",
        destination_scene="high_court_grand_basilica_gate",
        destination_province="The High Court",
        action_id="transit_carriage_to_court",
        action_label="Board High Carriage",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_item": "silver_coin"},
                {"has_trait": "High Decorum"},
                {"background_is": "noble_exile"},
                {"background_is": "Noble Exile"},
                {"ancestry_is": "High-Kin"},
                {"has_marker": "court_signet"},
                {"has_marker": "noble_favor"},
                {"min_skill": {"skill": "rhetoric", "value": 3}},
            ]
        },
        result_text="The cushioned carriage rumbles over paved stone. Gilded gates swing open ahead.",
        route_flag="route_high_court",
    ),
    TransitRoute(
        id="high_court_to_bazaar",
        name="Imperial High Carriage",
        origin_scene="high_court_grand_basilica_gate",
        destination_scene="bazaar_center",
        destination_province="Central Crossroads",
        action_id="transit_carriage_to_bazaar",
        action_label="Carriage To Bazaar",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_item": "silver_coin"},
                {"has_trait": "High Decorum"},
                {"background_is": "noble_exile"},
                {"background_is": "Noble Exile"},
                {"ancestry_is": "High-Kin"},
                {"has_marker": "court_signet"},
                {"has_marker": "noble_favor"},
                {"min_skill": {"skill": "rhetoric", "value": 3}},
            ]
        },
        result_text="The carriage rolls past sentry checkpoints. The noisy bazaar welcomes travelers.",
        route_flag="route_high_court",
    ),

    # --- The Sunken Hollows (Submersible Siphon Ferry) ---
    TransitRoute(
        id="bazaar_to_sunken_hollows",
        name="Submersible Siphon Ferry",
        origin_scene="bazaar_center",
        destination_scene="sunken_hollows_glow_grotto_gate",
        destination_province="The Sunken Hollows",
        action_id="transit_ferry_to_hollows",
        action_label="Board Siphon Ferry",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_item": "silver_coin"},
                {"has_item": "pitch_seal"},
                {"has_trait": "Abyssal Diver"},
                {"has_trait": "water_breather"},
                {"background_is": "abyssal_diver"},
                {"ancestry_is": "Deep-Dweller"},
                {"has_marker": "abyssal_tattoos"},
                {"has_trait": "Water Born"},
                {"has_item": "filter_mask"},
            ]
        },
        result_text="Water rises around the reinforced brass cabin. The pressurized vessel plunges deep into darkness.",
        route_flag="route_sunken_hollows",
    ),
    TransitRoute(
        id="sunken_hollows_to_bazaar",
        name="Submersible Siphon Ferry",
        origin_scene="sunken_hollows_glow_grotto_gate",
        destination_scene="bazaar_center",
        destination_province="Central Crossroads",
        action_id="transit_ferry_to_bazaar",
        action_label="Ferry To Bazaar",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_item": "silver_coin"},
                {"has_item": "pitch_seal"},
                {"has_trait": "Abyssal Diver"},
                {"has_trait": "water_breather"},
                {"background_is": "abyssal_diver"},
                {"ancestry_is": "Deep-Dweller"},
                {"has_marker": "abyssal_tattoos"},
                {"has_trait": "Water Born"},
                {"has_item": "filter_mask"},
            ]
        },
        result_text="Pumping valves hiss as air fills the ballast tanks. The ferry surfaces into the light.",
        route_flag="route_sunken_hollows",
    ),
]

# Fast lookup mappings
SCENE_TO_TRANSIT: Dict[str, List[TransitRoute]] = {}
ACTION_TO_TRANSIT: Dict[str, TransitRoute] = {}

for _route in CHARTERED_ROUTES:
    SCENE_TO_TRANSIT.setdefault(_route.origin_scene, []).append(_route)
    ACTION_TO_TRANSIT[_route.action_id] = _route


def get_transit_routes_for_scene(scene_id: str) -> List[TransitRoute]:
    """Retrieve all chartered transit routes originating from a given scene."""
    return list(SCENE_TO_TRANSIT.get(scene_id, []))


def get_transit_route_by_action(action_id: str) -> Optional[TransitRoute]:
    """Retrieve the transit route associated with an action id."""
    return ACTION_TO_TRANSIT.get(action_id)


def evaluate_transit_progress(world_flags: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate continental transit network coverage and wayfarer milestone."""
    distinct_routes = [
        {"key": "route_reach", "name": "Highland Cable Lift", "province": "The Reach"},
        {"key": "route_lowlands", "name": "Canal River Barge", "province": "The Lowlands"},
        {"key": "route_scorchwaste", "name": "Desert Silt-Skiff", "province": "The Scorchwaste"},
        {"key": "route_high_court", "name": "Imperial High Carriage", "province": "The High Court"},
        {"key": "route_sunken_hollows", "name": "Submersible Siphon Ferry", "province": "The Sunken Hollows"},
    ]

    traveled_count = sum(1 for r in distinct_routes if world_flags.get(r["key"], False))
    wayfarer = traveled_count >= 5 or bool(world_flags.get("continental_wayfarer_unlocked", False))

    return {
        "total_provinces": 5,
        "traveled_count": traveled_count,
        "wayfarer_unlocked": wayfarer,
        "routes": [
            {
                "name": r["name"],
                "province": r["province"],
                "traveled": bool(world_flags.get(r["key"], False)),
            }
            for r in distinct_routes
        ],
    }
