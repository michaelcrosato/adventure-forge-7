"""Tactical Combat Stances & Systemic Exploits (Milestone 16).

Provides deterministic tactical stances that dynamically expand the player's
affordance space according to 7-axis character attributes, skills, and traits:
- Aggressive Stance (Brutal Strike): high martial force, obstacle buckling.
- Guarded Stance (Brace Impact): damage mitigation, composure restoration.
- Elusive Stance (Feint Maneuver): stealth evasion, phantom footwork.
- Focused Stance (Spot Weakness): perceptive deduction, posture analysis.
"""
from dataclasses import dataclass
from typing import Dict, Any, List
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.conditions import evaluate_condition


@dataclass(frozen=True)
class TacticalStance:
    """Specification of a selectable tactical stance."""
    id: str
    name: str
    shift_action_id: str
    shift_label: str
    marker: str
    category: str
    prerequisite: Dict[str, Any]
    shift_effects: List[Dict[str, Any]]
    shift_result_text: str
    exploit_action_id: str
    exploit_label: str
    exploit_category: str
    exploit_effects: List[Dict[str, Any]]
    exploit_result_text: str
    stamina_cost: int = 0
    exploit_stamina_cost: int = 1

    def is_available(self, character: CharacterSheet, world_flags: Dict[str, Any]) -> bool:
        """Check if character meets the stance prerequisite."""
        return evaluate_condition(self.prerequisite, character, world_flags)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "shift_action_id": self.shift_action_id,
            "shift_label": self.shift_label,
            "marker": self.marker,
            "category": self.category,
            "shift_result_text": self.shift_result_text,
            "exploit_action_id": self.exploit_action_id,
            "exploit_label": self.exploit_label,
            "exploit_category": self.exploit_category,
            "exploit_result_text": self.exploit_result_text,
            "stamina_cost": self.stamina_cost,
            "exploit_stamina_cost": self.exploit_stamina_cost,
        }


ALL_STANCE_MARKERS = [
    "stance_aggressive",
    "stance_defensive",
    "stance_elusive",
    "stance_focused",
]

TACTICAL_STANCES: Dict[str, TacticalStance] = {
    "aggressive": TacticalStance(
        id="aggressive",
        name="Aggressive Stance",
        shift_action_id="stance_aggressive",
        shift_label="Take Aggressive Stance",
        marker="stance_aggressive",
        category="tactical",
        prerequisite={
            "any_of": [
                {"min_attribute": {"attribute": "strength", "value": 12}},
                {"min_skill": {"skill": "brawling", "value": 3}},
                {"has_trait": "iron_gutted"},
                {"has_flaw": "reckless"},
            ]
        },
        shift_effects=[
            {"add_marker": "stance_aggressive"},
            {"remove_marker": "stance_defensive"},
            {"remove_marker": "stance_elusive"},
            {"remove_marker": "stance_focused"},
            {"set_flag": {"flag": "active_stance", "value": "aggressive"}},
            {"log_event": "You shifted into an aggressive stance."},
        ],
        shift_result_text="You lower your center of gravity. Raw martial momentum surges through your muscles.",
        exploit_action_id="tactical_brutal_strike",
        exploit_label="Brutal Strike",
        exploit_category="combat",
        exploit_effects=[
            {"set_flag": {"flag": "tactical_strike_executed", "value": True}},
            {"log_event": "You struck with crushing force."},
        ],
        exploit_result_text="You drive forward with tremendous force. The heavy blow crushes through enemy defenses.",
        stamina_cost=0,
        exploit_stamina_cost=1,
    ),
    "defensive": TacticalStance(
        id="defensive",
        name="Guarded Stance",
        shift_action_id="stance_defensive",
        shift_label="Take Guarded Stance",
        marker="stance_defensive",
        category="tactical",
        prerequisite={
            "any_of": [
                {"min_attribute": {"attribute": "endurance", "value": 12}},
                {"min_skill": {"skill": "athletics", "value": 3}},
                {"has_flaw": "oath_bound"},
                {"has_trait": "oath_bound"},
                {"has_trait": "iron_gutted"},
            ]
        },
        shift_effects=[
            {"add_marker": "stance_defensive"},
            {"remove_marker": "stance_aggressive"},
            {"remove_marker": "stance_elusive"},
            {"remove_marker": "stance_focused"},
            {"set_flag": {"flag": "active_stance", "value": "defensive"}},
            {"log_event": "You raised your guard in a defensive stance."},
        ],
        shift_result_text="You raise your guard. Solid footing braces you against incoming hazards and blows.",
        exploit_action_id="tactical_brace_impact",
        exploit_label="Brace Impact",
        exploit_category="combat",
        exploit_effects=[
            {"modify_health": 1},
            {"set_flag": {"flag": "tactical_brace_executed", "value": True}},
            {"log_event": "You braced your stance and restored your composure."},
        ],
        exploit_result_text="You absorb the kinetic shock through your heels. Your composure remains unbroken.",
        stamina_cost=0,
        exploit_stamina_cost=1,
    ),
    "elusive": TacticalStance(
        id="elusive",
        name="Elusive Stance",
        shift_action_id="stance_elusive",
        shift_label="Take Elusive Stance",
        marker="stance_elusive",
        category="tactical",
        prerequisite={
            "any_of": [
                {"min_attribute": {"attribute": "agility", "value": 12}},
                {"min_skill": {"skill": "stealth", "value": 3}},
                {"has_trait": "nimble"},
                {"has_trait": "night_eyed"},
                {"has_trait": "streetwise"},
            ]
        },
        shift_effects=[
            {"add_marker": "stance_elusive"},
            {"remove_marker": "stance_aggressive"},
            {"remove_marker": "stance_defensive"},
            {"remove_marker": "stance_focused"},
            {"set_flag": {"flag": "active_stance", "value": "elusive"}},
            {"log_event": "You slipped into an elusive, light-footed stance."},
        ],
        shift_result_text="You shift weight to your toes. You move swift and silent across stone.",
        exploit_action_id="tactical_feint",
        exploit_label="Feint Maneuver",
        exploit_category="combat",
        exploit_effects=[
            {"set_flag": {"flag": "tactical_feint_executed", "value": True}},
            {"log_event": "You executed a swift feint maneuver."},
        ],
        exploit_result_text="You fake a sudden step. Observers track the phantom step and lose your true path.",
        stamina_cost=0,
        exploit_stamina_cost=1,
    ),
    "focused": TacticalStance(
        id="focused",
        name="Focused Stance",
        shift_action_id="stance_focused",
        shift_label="Take Focused Stance",
        marker="stance_focused",
        category="tactical",
        prerequisite={
            "any_of": [
                {"min_skill": {"skill": "cunning", "value": 3}},
                {"min_skill": {"skill": "rhetoric", "value": 3}},
                {"has_trait": "keen_eyed"},
                {"has_trait": "skeptical"},
            ]
        },
        shift_effects=[
            {"add_marker": "stance_focused"},
            {"remove_marker": "stance_aggressive"},
            {"remove_marker": "stance_defensive"},
            {"remove_marker": "stance_elusive"},
            {"set_flag": {"flag": "active_stance", "value": "focused"}},
            {"log_event": "You focused your senses on subtle tactical cues."},
        ],
        shift_result_text="Your breathing slows. Every subtle shift in airflow and footsteps sharpens in your mind.",
        exploit_action_id="tactical_spot_weakness",
        exploit_label="Spot Weakness",
        exploit_category="interaction",
        exploit_effects=[
            {"set_flag": {"flag": "tactical_weakness_spotted", "value": True}},
            {"log_event": "You spotted a tactical flaw in enemy posture."},
        ],
        exploit_result_text="You observe subtle gaps in posture. A clean path of tactical opportunity presents itself.",
        stamina_cost=0,
        exploit_stamina_cost=0,
    ),
}


def get_tactical_stances() -> Dict[str, TacticalStance]:
    """Return all configured tactical stances."""
    return dict(TACTICAL_STANCES)
