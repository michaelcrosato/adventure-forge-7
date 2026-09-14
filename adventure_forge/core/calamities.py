"""Continental Dynamic Event & World Calamity System (Milestone 18).

Provides pure, deterministic provincial incursion events across the 5 provinces:
- The Reach: Crag Tremor (rockfalls, tumbling scree; mitigable by rope anchor or bracing).
- The Sunken Hollows: Siphon Surge (high-pressure water flood; mitigable by bulkhead seal or air equalization).
- The Scorchwaste: Glass Tempest (superheated sand scouring; mitigable by cowl draping or canteen burial).
- The High Court: Inquisitor Lockdown (martial sentry cordons; mitigable by crest display or noble decorum).
- The Lowlands: Sluice Breach (canal runoff flooding; mitigable by winch levering or grate traversal).
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.conditions import evaluate_condition


@dataclass(frozen=True)
class CalamityMitigation:
    """A deterministic player affordance to mitigate a regional calamity."""
    id: str
    action_id: str
    label: str  # Exactly 1 to 3 words
    category: str
    condition: Dict[str, Any]
    effects: List[Dict[str, Any]]
    result_text: str  # 1-2 short sentences, <= 18 words/sent
    stamina_cost: int = 0
    risk: str = "medium"

    def is_legal(self, character: CharacterSheet, world_flags: Dict[str, Any]) -> bool:
        if character.stamina < self.stamina_cost:
            return False
        return evaluate_condition(self.condition, character, world_flags)


@dataclass(frozen=True)
class WorldCalamity:
    """Specification of a provincial incursion and systemic calamity."""
    id: str
    name: str
    province: str
    region_prefixes: Tuple[str, ...]
    description: str  # 1-2 short sentences, <= 18 words/sent
    hazard_flag: str
    cleared_flag: str
    mitigations: Tuple[CalamityMitigation, ...]
    turn_mod: int = 8
    active_offsets: Tuple[int, ...] = (3, 4)

    def is_active(self, turn_count: int, region_id: str, world_flags: Dict[str, Any]) -> bool:
        """Evaluate if the calamity is actively threatening the current scene."""
        # Cleared in current cycle
        if world_flags.get(self.cleared_flag, False):
            return False

        # Explicitly triggered via world flags
        if world_flags.get(f"{self.id}_active", False) or world_flags.get(self.hazard_flag, False):
            return True

        # Check regional matching
        clean_reg = region_id.lower().strip()
        matches_region = any(
            clean_reg.startswith(prefix) or prefix in clean_reg
            for prefix in self.region_prefixes
        )
        if not matches_region:
            return False

        # If calamities are disabled in flags, skip
        if world_flags.get("calamities_disabled", False):
            return False

        # Cyclical activation (deterministic turn cycle)
        return (turn_count % self.turn_mod) in self.active_offsets

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "description": self.description,
            "hazard_flag": self.hazard_flag,
            "cleared_flag": self.cleared_flag,
        }


WORLD_CALAMITIES: Dict[str, WorldCalamity] = {
    "reach_tremor": WorldCalamity(
        id="reach_tremor",
        name="Crag Tremor",
        province="The Reach",
        region_prefixes=("reach", "crag", "province_reach"),
        description="A deep tremor rumbles through the granite crags. Loose rocks clatter down the cliff.",
        hazard_flag="hazard_reach_tremor",
        cleared_flag="reach_tremor_cleared",
        mitigations=(
            CalamityMitigation(
                id="reach_anchor",
                action_id="calamity_reach_anchor",
                label="Anchor Line",
                category="systemic",
                condition={
                    "any_of": [
                        {"has_item": "climbing_rope"},
                        {"min_attribute": {"attribute": "agility", "value": 12}},
                        {"has_trait": "nimble"},
                    ]
                },
                effects=[
                    {"set_flag": {"flag": "reach_tremor_cleared", "value": True}},
                    {"set_flag": {"flag": "hazard_reach_tremor", "value": False}},
                    {"add_item": "scrap_metal"},
                    {"log_event": "You anchored your climbing line against the crag tremor."},
                ],
                result_text="You drive a steel piton into solid rock and secure your line against the falling stone.",
                stamina_cost=1,
            ),
            CalamityMitigation(
                id="reach_brace",
                action_id="calamity_reach_brace",
                label="Brace Shudder",
                category="systemic",
                condition={
                    "any_of": [
                        {"min_attribute": {"attribute": "strength", "value": 12}},
                        {"min_attribute": {"attribute": "endurance", "value": 12}},
                    ]
                },
                effects=[
                    {"set_flag": {"flag": "reach_tremor_cleared", "value": True}},
                    {"set_flag": {"flag": "hazard_reach_tremor", "value": False}},
                    {"log_event": "You braced your footing against the crag tremor."},
                ],
                result_text="You plant your boots against the rock face and absorb the tremor through your knees.",
                stamina_cost=1,
            ),
        ),
    ),
    "hollows_surge": WorldCalamity(
        id="hollows_surge",
        name="Siphon Surge",
        province="The Sunken Hollows",
        region_prefixes=("sunken", "hollows", "province_sunken_hollows"),
        description="Cold water surges violently through the siphon conduit. Frothing foam rises along the stone walls.",
        hazard_flag="hazard_hollows_surge",
        cleared_flag="hollows_surge_cleared",
        mitigations=(
            CalamityMitigation(
                id="hollows_seal",
                action_id="calamity_hollows_seal",
                label="Seal Bulkhead",
                category="systemic",
                condition={
                    "any_of": [
                        {"has_item": "waterproof_seal"},
                        {"has_item": "crowbar"},
                        {"min_attribute": {"attribute": "strength", "value": 12}},
                    ]
                },
                effects=[
                    {"set_flag": {"flag": "hollows_surge_cleared", "value": True}},
                    {"set_flag": {"flag": "hazard_hollows_surge", "value": False}},
                    {"add_item": "algae_sample"},
                    {"log_event": "You sealed the bulkhead against the water surge."},
                ],
                result_text="You clamp the heavy hatch shut with pitch and seal against the hydrostatic surge.",
                stamina_cost=1,
            ),
            CalamityMitigation(
                id="hollows_equalize",
                action_id="calamity_hollows_equalize",
                label="Equalize Air",
                category="systemic",
                condition={
                    "any_of": [
                        {"has_trait": "water_breather"},
                        {"min_attribute": {"attribute": "endurance", "value": 12}},
                    ]
                },
                effects=[
                    {"set_flag": {"flag": "hollows_surge_cleared", "value": True}},
                    {"set_flag": {"flag": "hazard_hollows_surge", "value": False}},
                    {"log_event": "You equalized air pressure against the deep surge."},
                ],
                result_text="You slow your breathing and let your chest equalize against the rising water pressure.",
                stamina_cost=0,
            ),
        ),
    ),
    "scorch_tempest": WorldCalamity(
        id="scorch_tempest",
        name="Glass Tempest",
        province="The Scorchwaste",
        region_prefixes=("scorch", "desert", "sand", "province_scorchwaste"),
        description="A blinding glass tempest sweeps across the salt flats. Superheated sand scours the dunes.",
        hazard_flag="hazard_scorch_tempest",
        cleared_flag="scorch_tempest_cleared",
        mitigations=(
            CalamityMitigation(
                id="scorch_cowl",
                action_id="calamity_scorch_cowl",
                label="Drape Cowl",
                category="systemic",
                condition={
                    "any_of": [
                        {"has_item": "cloak"},
                        {"has_trait": "heat_tolerant"},
                    ]
                },
                effects=[
                    {"set_flag": {"flag": "scorch_tempest_cleared", "value": True}},
                    {"set_flag": {"flag": "hazard_scorch_tempest", "value": False}},
                    {"add_item": "salt_crust"},
                    {"log_event": "You draped your cowl against the glass tempest."},
                ],
                result_text="You wrap your woven cowl tight across your face to shield against burning sand.",
                stamina_cost=0,
            ),
            CalamityMitigation(
                id="scorch_canteen",
                action_id="calamity_scorch_canteen",
                label="Bury Canteen",
                category="systemic",
                condition={
                    "any_of": [
                        {"has_item": "water_skin"},
                        {"has_item": "waterskin"},
                    ]
                },
                effects=[
                    {"set_flag": {"flag": "scorch_tempest_cleared", "value": True}},
                    {"set_flag": {"flag": "hazard_scorch_tempest", "value": False}},
                    {"log_event": "You buried your canteen to preserve clean water."},
                ],
                result_text="You bury the canteen in cool sand beneath your boots to conserve drinking water.",
                stamina_cost=0,
            ),
        ),
    ),
    "court_lockdown": WorldCalamity(
        id="court_lockdown",
        name="Inquisitor Lockdown",
        province="The High Court",
        region_prefixes=("court", "high_court", "province_high_court"),
        description="The grand hall bells ring a sudden martial alarm. Heavily armored justiciars bar every arched exit.",
        hazard_flag="hazard_court_lockdown",
        cleared_flag="court_lockdown_cleared",
        mitigations=(
            CalamityMitigation(
                id="court_signet",
                action_id="calamity_court_signet",
                label="Display Signet",
                category="social",
                condition={
                    "any_of": [
                        {"has_item": "watch_crest"},
                        {"has_marker": "watch_crest"},
                        {"has_item": "legal_dossier"},
                    ]
                },
                effects=[
                    {"set_flag": {"flag": "court_lockdown_cleared", "value": True}},
                    {"set_flag": {"flag": "hazard_court_lockdown", "value": False}},
                    {"log_event": "You flashed your legal crest to pass the guard cordon."},
                ],
                result_text="You present the legal crest with cool authority. The justiciars step aside with formal salutes.",
                stamina_cost=0,
            ),
            CalamityMitigation(
                id="court_decorum",
                action_id="calamity_court_decorum",
                label="Feign Decorum",
                category="social",
                condition={
                    "any_of": [
                        {"min_skill": {"skill": "rhetoric", "value": 3}},
                        {"has_trait": "skeptical"},
                    ]
                },
                effects=[
                    {"set_flag": {"flag": "court_lockdown_cleared", "value": True}},
                    {"set_flag": {"flag": "hazard_court_lockdown", "value": False}},
                    {"log_event": "You spoke with calm noble decorum to disarm the watch."},
                ],
                result_text="You bow with calm noble poise. Your steady tone convinces the sentries to stand down.",
                stamina_cost=0,
            ),
        ),
    ),
    "lowlands_breach": WorldCalamity(
        id="lowlands_breach",
        name="Sluice Breach",
        province="The Lowlands",
        region_prefixes=("lowlands", "warrens", "province_lowlands"),
        description="A loud crack echoes down the canal. Murky canal runoff rushes across the stone walkway.",
        hazard_flag="hazard_lowlands_breach",
        cleared_flag="lowlands_breach_cleared",
        mitigations=(
            CalamityMitigation(
                id="lowlands_winch",
                action_id="calamity_lowlands_winch",
                label="Lever Winch",
                category="systemic",
                condition={
                    "any_of": [
                        {"has_item": "crowbar"},
                        {"min_attribute": {"attribute": "strength", "value": 12}},
                    ]
                },
                effects=[
                    {"set_flag": {"flag": "lowlands_breach_cleared", "value": True}},
                    {"set_flag": {"flag": "hazard_lowlands_breach", "value": False}},
                    {"add_item": "tallow"},
                    {"log_event": "You cranked the winch shut to halt the canal flood."},
                ],
                result_text="You throw your weight onto the iron winch to shut the heavy sluice gate.",
                stamina_cost=1,
            ),
            CalamityMitigation(
                id="lowlands_grate",
                action_id="calamity_lowlands_grate",
                label="Slip Grate",
                category="systemic",
                condition={
                    "any_of": [
                        {"has_trait": "nimble"},
                        {"has_item": "lockpick"},
                        {"min_skill": {"skill": "stealth", "value": 3}},
                    ]
                },
                effects=[
                    {"set_flag": {"flag": "lowlands_breach_cleared", "value": True}},
                    {"set_flag": {"flag": "hazard_lowlands_breach", "value": False}},
                    {"log_event": "You slipped past the rising water through an iron grate."},
                ],
                result_text="You slip through a narrow drain grate and escape the rushing water.",
                stamina_cost=0,
            ),
        ),
    ),
}


def get_active_calamity(
    turn_count: int,
    region_id: Optional[str],
    world_flags: Dict[str, Any]
) -> Optional[WorldCalamity]:
    """Identify which calamity, if any, is currently threatening the active scene."""
    if not region_id:
        return None
    for calamity in WORLD_CALAMITIES.values():
        if calamity.is_active(turn_count, region_id, world_flags):
            return calamity
    return None
