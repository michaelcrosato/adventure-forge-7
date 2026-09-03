"""Continental Quest Engine & Branching Narrative DAGs.

Implements Baldur's Gate 3 systemic depth:
- Cross-province persistent consequences.
- Multi-approach resolutions (Force, Cunning, Diplomacy, Trait Exploits).
- Faction standing shifts that dynamically reshape NPC greetings and shop prices.
- Multiple mutually exclusive campaign endings.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from adventure_forge.core.conditions import evaluate_condition
from adventure_forge.core.character import CharacterSheet


@dataclass
class QuestStage:
    id: str
    title: str
    province: str
    description: str
    required_flags: Dict[str, Any]
    completion_flags: Dict[str, Any]
    reputation_rewards: Dict[str, int]
    approaches: List[str]  # e.g. ["force", "stealth", "diplomacy", "trait"]


@dataclass
class QuestLine:
    id: str
    name: str
    synopsis: str
    stages: List[QuestStage]
    endings: Dict[str, str]

    def evaluate_progress(self, character: CharacterSheet, world_flags: Dict[str, Any]) -> Dict[str, Any]:
        completed_stages = []
        active_stage = None

        for stage in self.stages:
            is_complete = all(world_flags.get(k) == v for k, v in stage.completion_flags.items())
            if is_complete:
                completed_stages.append(stage.id)
            elif active_stage is None:
                prereqs_met = all(world_flags.get(k) == v for k, v in stage.required_flags.items())
                if prereqs_met:
                    active_stage = stage.id

        return {
            "quest_id": self.id,
            "completed_stages": completed_stages,
            "active_stage": active_stage,
            "is_finished": len(completed_stages) == len(self.stages),
        }


def get_continental_main_quest() -> QuestLine:
    """Returns the grand 5-province main campaign: The Five Seals of Sovereignty."""
    return QuestLine(
        id="five_seals_campaign",
        name="The Five Seals of Sovereignty",
        synopsis="Unite or exploit the five regional powers to claim the Unbounded Throne.",
        stages=[
            QuestStage(
                id="stage_crags_beacon",
                title="Ignite the Highland Beacon",
                province="reach",
                description="Secure the fortress at Eagle Peak and light the signal fire.",
                required_flags={},
                completion_flags={"crags_beacon_lit": True},
                reputation_rewards={"iron_guard": 10},
                approaches=["force", "stealth", "climbing"]
            ),
            QuestStage(
                id="stage_warrens_ledger",
                title="Recover the Shadow Ledger",
                province="lowlands",
                description="Retrieve the contraband ledger from the underground fence.",
                required_flags={"crags_beacon_lit": True},
                completion_flags={"has_watch_badge": True},
                reputation_rewards={"city_watch": 10, "smugglers": -5},
                approaches=["cunning", "bribe", "social_disguise"]
            ),
            QuestStage(
                id="stage_scorch_compass",
                title="Acquire the Solar Compass",
                province="scorchwaste",
                description="Brave the dunes and secure the brass sun compass from nomads.",
                required_flags={"has_watch_badge": True},
                completion_flags={"scorch_compass_secured": True},
                reputation_rewards={"desert_nomads": 15},
                approaches=["trade", "survival_crafting", "heat_endurance"]
            ),
            QuestStage(
                id="stage_court_verdict",
                title="Win the Tribunal Verdict",
                province="high_court",
                description="Argue your exoneration before the High Magistrate.",
                required_flags={"scorch_compass_secured": True},
                completion_flags={"court_verdict_won": True},
                reputation_rewards={"justiciars": 15},
                approaches=["rhetoric", "legal_writ", "aristocratic_influence"]
            ),
            QuestStage(
                id="stage_abyssal_pearl",
                title="Retrieve the Sunken Pearl",
                province="sunken_hollows",
                description="Dive into the flooded obsidian temple and extract the heart relic.",
                required_flags={"court_verdict_won": True},
                completion_flags={"sunken_relic_secured": True},
                reputation_rewards={"deep_clans": 20},
                approaches=["diving_bell", "breath_holding", "subterranean_lore"]
            )
        ],
        endings={
            "justiciar_order": "You delivered all five seals to the High Justiciars, establishing strict martial law.",
            "shadow_syndicate": "You bartered the five seals to the Smuggler Syndicate, turning the continent into a free-trade black market.",
            "unbounded_ruler": "You kept all five relics for yourself, taking the Unbounded Throne by absolute sovereignty."
        }
    )
