"""Continental Quest Engine & Branching Narrative DAGs.

Implements Baldur's Gate 3 systemic depth:
- Cross-province persistent consequences.
- Multi-approach resolutions (Force, Cunning, Diplomacy, Trait Exploits).
- Faction standing shifts that dynamically reshape NPC greetings and shop prices.
- Multiple mutually exclusive campaign endings.
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "province": self.province,
            "description": self.description,
            "reputation_rewards": dict(self.reputation_rewards),
            "approaches": list(self.approaches),
        }


@dataclass
class QuestLine:
    id: str
    name: str
    synopsis: str
    stages: List[QuestStage]
    endings: Dict[str, str]
    ending_conditions: Optional[Dict[str, Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "synopsis": self.synopsis,
            "stages": [s.to_dict() for s in self.stages],
            "endings": dict(self.endings),
        }

    def resolve_ending(self, world_flags: Dict[str, Any]) -> Optional[str]:
        """Determine which ending is active based on world flags."""
        if self.ending_conditions:
            for end_id, cond in self.ending_conditions.items():
                if all(world_flags.get(k) == v for k, v in cond.items()):
                    return end_id
        for ending_key in self.endings:
            if world_flags.get(f"{self.id}_{ending_key}") is True or world_flags.get(ending_key) is True:
                return ending_key
            if world_flags.get(f"{self.id}_ending") == ending_key or world_flags.get("quest_ending") == ending_key:
                return ending_key
        return None

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

        ending = self.resolve_ending(world_flags)
        is_finished = len(completed_stages) == len(self.stages)

        return {
            "quest_id": self.id,
            "completed_stages": completed_stages,
            "active_stage": active_stage,
            "is_finished": is_finished,
            "ending": ending,
            "active_ending": ending,
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
                description="Take the secret ledger from the underground fence.",
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
                description="Argue your case before the high judge.",
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
            "justiciar_order": "You gave the five seals to the High Justiciars to set strict martial law.",
            "shadow_syndicate": "You sold the five seals to the Smuggler Syndicate to free trade across the realm.",
            "unbounded_ruler": "You kept all five relics to take the Unbounded Throne by your own hand."
        },
        ending_conditions={
            "justiciar_order": {"continental_ending_justiciar": True},
            "shadow_syndicate": {"continental_ending_smuggler": True},
            "unbounded_ruler": {"continental_ending_ruler": True},
        }
    )


# ---------------------------------------------------------------------------
# Cycle 2: Provincial Subquest Chains
# ---------------------------------------------------------------------------


def subquest_reach_smuggler_caches() -> QuestLine:
    """The Reach: Smuggler Caches subquest chain."""
    return QuestLine(
        id="subquest_reach_smuggler_caches",
        name="The Reach Smuggler Caches",
        synopsis="Find hidden mountain loot before the Iron Guard sweeps the high cliffs.",
        stages=[
            QuestStage(
                id="reach_cache_stage_scout",
                title="Locate Quarry Cache",
                province="reach",
                description="Track mountain smuggler marks near the deep stone quarry.",
                required_flags={},
                completion_flags={"reach_quarry_cache_found": True},
                reputation_rewards={"smugglers": 5},
                approaches=["climbing", "tracking", "stealth"]
            ),
            QuestStage(
                id="reach_cache_stage_recover",
                title="Recover Bluff Contraband",
                province="reach",
                description="Retrieve the hidden weapons crate from the high wind bluff.",
                required_flags={"reach_quarry_cache_found": True},
                completion_flags={"reach_bluff_cache_recovered": True},
                reputation_rewards={"smugglers": 10},
                approaches=["force", "agility", "cunning"]
            ),
            QuestStage(
                id="reach_cache_stage_deliver",
                title="Resolve Contraband Fate",
                province="reach",
                description="Deliver the mountain loot or trade it for fast coin.",
                required_flags={"reach_bluff_cache_recovered": True},
                completion_flags={"reach_caches_resolved": True},
                reputation_rewards={"smugglers": 15, "iron_guard": 10},
                approaches=["diplomacy", "trade", "loyalty"]
            )
        ],
        endings={
            "smuggler_syndicate": "You gave the arms to the mountain crew and won their trust.",
            "iron_guard_turnin": "You gave the loot to the Iron Guard garrison for gold.",
            "black_market_hoard": "You hid the mountain arms away for your own trade."
        },
        ending_conditions={
            "smuggler_syndicate": {"reach_cache_smuggler_ending": True},
            "iron_guard_turnin": {"reach_cache_guard_ending": True},
            "black_market_hoard": {"reach_cache_hoard_ending": True},
        }
    )


def subquest_lowlands_shadow_broker() -> QuestLine:
    """The Lowlands: Shadow Broker subquest chain."""
    return QuestLine(
        id="subquest_lowlands_shadow_broker",
        name="The Lowlands Shadow Broker",
        synopsis="Track down the secret broker who runs the river crime ring.",
        stages=[
            QuestStage(
                id="lowlands_broker_stage_contact",
                title="Find the Dock Informant",
                province="lowlands",
                description="Meet the dock runner in the harbor district to buy fresh rumors.",
                required_flags={},
                completion_flags={"lowlands_informant_contacted": True},
                reputation_rewards={"shadow_syndicate": 5},
                approaches=["bribe", "cunning", "stealth"]
            ),
            QuestStage(
                id="lowlands_broker_stage_decode",
                title="Decode Harbor Cipher",
                province="lowlands",
                description="Steal the secret cargo book from the river customs office.",
                required_flags={"lowlands_informant_contacted": True},
                completion_flags={"lowlands_cipher_decoded": True},
                reputation_rewards={"shadow_syndicate": 10},
                approaches=["infiltration", "forgery", "lockpicking"]
            ),
            QuestStage(
                id="lowlands_broker_stage_confront",
                title="Confront the Broker",
                province="lowlands",
                description="Corner the Shadow Broker in the sunken cellar to pick a side.",
                required_flags={"lowlands_cipher_decoded": True},
                completion_flags={"lowlands_broker_resolved": True},
                reputation_rewards={"shadow_syndicate": 15, "city_watch": 15},
                approaches=["extortion", "alliance", "arrest"]
            )
        ],
        endings={
            "broker_alliance": "You joined the Shadow Broker to run harbor trade together.",
            "broker_exposed": "You handed the Shadow Broker to the City Watch for trial.",
            "broker_usurped": "You took down the Shadow Broker and seized the ring yourself."
        },
        ending_conditions={
            "broker_alliance": {"lowlands_broker_allied": True},
            "broker_exposed": {"lowlands_broker_exposed": True},
            "broker_usurped": {"lowlands_broker_usurped": True},
        }
    )


def subquest_scorchwaste_water_baron() -> QuestLine:
    """The Scorchwaste: Oasis Water Baron subquest chain."""
    return QuestLine(
        id="subquest_scorchwaste_water_baron",
        name="The Scorchwaste Oasis Water Baron",
        synopsis="Break the iron grip of the cruel water boss over the oasis wells.",
        stages=[
            QuestStage(
                id="scorch_baron_stage_scout",
                title="Inspect Salt Aqueduct",
                province="scorchwaste",
                description="Survey the locked water gates across the white salt flats.",
                required_flags={},
                completion_flags={"scorch_aqueduct_inspected": True},
                reputation_rewards={"desert_nomads": 5},
                approaches=["survival", "scouting", "engineering"]
            ),
            QuestStage(
                id="scorch_baron_stage_sabotage",
                title="Divert Oasis Cistern",
                province="scorchwaste",
                description="Shut down the pressure pump at the hidden spring oasis.",
                required_flags={"scorch_aqueduct_inspected": True},
                completion_flags={"scorch_cistern_diverted": True},
                reputation_rewards={"desert_nomads": 10},
                approaches=["stealth", "mechanics", "force"]
            ),
            QuestStage(
                id="scorch_baron_stage_reckoning",
                title="Depose the Baron",
                province="scorchwaste",
                description="Face the water boss at the deep well to settle desert rule.",
                required_flags={"scorch_cistern_diverted": True},
                completion_flags={"scorch_baron_resolved": True},
                reputation_rewards={"desert_nomads": 20, "oasis_merchants": 15},
                approaches=["duel", "negotiation", "monopoly"]
            )
        ],
        endings={
            "free_water": "You freed the deep wells to give fresh water to every nomad.",
            "merchant_treaty": "You made a fair trade deal between the water boss and caravans.",
            "new_baron": "You took the oasis wells and made the desert answer to you."
        },
        ending_conditions={
            "free_water": {"scorch_water_liberated": True},
            "merchant_treaty": {"scorch_water_negotiated": True},
            "new_baron": {"scorch_water_claimed": True},
        }
    )


def subquest_court_decrees() -> QuestLine:
    """The High Court: Decrees subquest chain."""
    return QuestLine(
        id="subquest_court_decrees",
        name="High Court Decrees",
        synopsis="Play court politics to rewrite the high decrees of the realm.",
        stages=[
            QuestStage(
                id="court_decree_stage_petition",
                title="Intercept Royal Edict",
                province="high_court",
                description="Read the secret law inside the Royal Archives before it is signed.",
                required_flags={},
                completion_flags={"court_decree_intercepted": True},
                reputation_rewards={"justiciars": 5},
                approaches=["scholarship", "bribery", "subterfuge"]
            ),
            QuestStage(
                id="court_decree_stage_influence",
                title="Sway Court Nobility",
                province="high_court",
                description="Win support from rival lords inside the envoy salon.",
                required_flags={"court_decree_intercepted": True},
                completion_flags={"court_nobles_swayed": True},
                reputation_rewards={"high_nobility": 10},
                approaches=["etiquette", "blackmail", "eloquence"]
            ),
            QuestStage(
                id="court_decree_stage_promulgate",
                title="Seal Imperial Edict",
                province="high_court",
                description="Cast your vote before the high bench to seal the provincial law.",
                required_flags={"court_nobles_swayed": True},
                completion_flags={"court_decree_resolved": True},
                reputation_rewards={"justiciars": 15, "high_nobility": 15},
                approaches=["legal_argument", "regal_command", "bribery"]
            )
        ],
        endings={
            "decree_reform": "You passed new laws that stripped corrupt lords of land and titles.",
            "decree_martial": "You backed strict martial rule with heavy guard posts everywhere.",
            "decree_veto": "You killed the decree to throw the high council into pure chaos."
        },
        ending_conditions={
            "decree_reform": {"court_decree_reformed": True},
            "decree_martial": {"court_decree_martialed": True},
            "decree_veto": {"court_decree_vetoed": True},
        }
    )


def subquest_hollows_abyssal_keystones() -> QuestLine:
    """The Sunken Hollows: Abyssal Keystones subquest chain."""
    return QuestLine(
        id="subquest_hollows_abyssal_keystones",
        name="Sunken Hollows Abyssal Keystones",
        synopsis="Find the sunken keystones to open the ancient gate under the lake.",
        stages=[
            QuestStage(
                id="hollows_keystone_stage_grotto",
                title="Retrieve Grotto Keystone",
                province="sunken_hollows",
                description="Pry the glowing stone key from the deep cave shrine.",
                required_flags={},
                completion_flags={"hollows_grotto_keystone_found": True},
                reputation_rewards={"deep_clans": 5},
                approaches=["mining", "arcana", "athletics"]
            ),
            QuestStage(
                id="hollows_keystone_stage_trench",
                title="Dredge Trench Keystone",
                province="sunken_hollows",
                description="Dig up the second key from deep mud in the crystal trench.",
                required_flags={"hollows_grotto_keystone_found": True},
                completion_flags={"hollows_trench_keystone_found": True},
                reputation_rewards={"deep_clans": 10},
                approaches=["dredging", "diving", "strength"]
            ),
            QuestStage(
                id="hollows_keystone_stage_gate",
                title="Unlock Primordial Gate",
                province="sunken_hollows",
                description="Place the keystones into the sunken vault gate to test its power.",
                required_flags={"hollows_trench_keystone_found": True},
                completion_flags={"hollows_gate_resolved": True},
                reputation_rewards={"deep_clans": 20},
                approaches=["ancient_lore", "ritual_binding", "seal_destruction"]
            )
        ],
        endings={
            "gate_unsealed": "You opened the deep gate and let old magic flood the caves.",
            "gate_warded": "You locked the deep gate forever under heavy warding stones.",
            "power_absorbed": "You took the raw power from the stones into your own soul."
        },
        ending_conditions={
            "gate_unsealed": {"hollows_gate_unsealed": True},
            "gate_warded": {"hollows_gate_warded": True},
            "power_absorbed": {"hollows_power_absorbed": True},
        }
    )


def quest_reach_faction_intrigue() -> QuestLine:
    """The Reach: Sky-Pact of the Crags faction intrigue arc."""
    return QuestLine(
        id="quest_reach_faction_intrigue",
        name="The Sky-Pact of the Crags",
        synopsis="Mediate the clash between Cliff Clans and Storm Wardens over the Spire Grid.",
        stages=[
            QuestStage(
                id="reach_intrigue_stage_discovery",
                title="Severed Mountain Circuit",
                province="reach",
                description="Inspect severed cables or ground the surge wire to trace the sabotage.",
                required_flags={},
                completion_flags={"reach_discovery_completed": True},
                reputation_rewards={"cliff_clans": 5, "storm_wardens": 5},
                approaches=["perception", "social", "item_affordance"],
            ),
            QuestStage(
                id="reach_intrigue_stage_escalation",
                title="The Quarry Blockade",
                province="reach",
                description="Break the quarry blockade by force, stealth, or negotiated truce.",
                required_flags={"reach_discovery_completed": True},
                completion_flags={"reach_escalation_completed": True},
                reputation_rewards={"cliff_clans": 10, "storm_wardens": 10},
                approaches=["athletics", "stealth", "rhetoric"],
            ),
            QuestStage(
                id="reach_intrigue_stage_dilemma",
                title="The Apex Overload",
                province="reach",
                description="Stop the battery overload before blue lightning strikes the peaks.",
                required_flags={"reach_escalation_completed": True},
                completion_flags={"reach_dilemma_resolved": True},
                reputation_rewards={"storm_wardens": 15, "cliff_clans": 15},
                approaches=["discharge", "short_circuit", "harmonize"],
            ),
            QuestStage(
                id="reach_intrigue_stage_resolution",
                title="Pact of the Peaks",
                province="reach",
                description="Proclaim the final summit pact at the central mountain hub.",
                required_flags={"reach_dilemma_resolved": True},
                completion_flags={"reach_intrigue_resolved": True},
                reputation_rewards={"storm_wardens": 25, "cliff_clans": 25},
                approaches=["dominance", "liberation", "harmony"],
            ),
        ],
        endings={
            "storm_warden_dominance": "You gave full power to the Storm Wardens to shield the high pass.",
            "cliff_clan_liberation": "You cut the power grid and freed the Cliff Clans from monastic rule.",
            "ascetic_harmony": "You vented the storm charge into alpine steam vents to unite both factions.",
        },
        ending_conditions={
            "storm_warden_dominance": {"reach_ending_warden": True},
            "cliff_clan_liberation": {"reach_ending_clan": True},
            "ascetic_harmony": {"reach_ending_harmony": True},
        },
    )


def quest_high_court_faction_intrigue() -> QuestLine:
    """The High Court: Tripartite Throne faction intrigue arc."""
    return QuestLine(
        id="quest_high_court_faction_intrigue",
        name="The Tripartite Throne",
        synopsis="Navigate the deadly throne crisis among Crown, Duke, and Guild factions.",
        stages=[
            QuestStage(
                id="court_intrigue_stage_discovery",
                title="Shadows in the Archives",
                province="high_court",
                description="Uncover scraped records in the archives or stop trade couriers.",
                required_flags={},
                completion_flags={"court_discovery_completed": True},
                reputation_rewards={"crown_royalists": 5, "dukes_conclave": 5, "guild_emissaries": 5},
                approaches=["lockpicking", "cunning", "stealth", "rhetoric"],
            ),
            QuestStage(
                id="court_intrigue_stage_escalation",
                title="The Silver Embargo",
                province="high_court",
                description="Infiltrate the ducal silver vault, sway palatine knights, or buy grain.",
                required_flags={"court_discovery_completed": True},
                completion_flags={"court_escalation_completed": True},
                reputation_rewards={"crown_royalists": 10, "dukes_conclave": 10, "guild_emissaries": 10},
                approaches=["infiltration", "rhetoric", "commerce"],
            ),
            QuestStage(
                id="court_intrigue_stage_dilemma",
                title="The Tribunal Convocation",
                province="high_court",
                description="Present key evidence before the high court bench.",
                required_flags={"court_escalation_completed": True},
                completion_flags={"court_dilemma_resolved": True},
                reputation_rewards={"crown_royalists": 15, "dukes_conclave": 15, "guild_emissaries": 15},
                approaches=["crown", "duke", "guild", "regency"],
            ),
            QuestStage(
                id="court_intrigue_stage_resolution",
                title="Proclamation of Veras",
                province="high_court",
                description="Read the royal decree from the high palace balcony.",
                required_flags={"court_dilemma_resolved": True},
                completion_flags={"court_intrigue_resolved": True},
                reputation_rewards={"crown_royalists": 25, "dukes_conclave": 25, "guild_emissaries": 25},
                approaches=["martial", "autonomy", "commerce", "regency"],
            ),
        ],
        endings={
            "court_royalist_ascendancy": "You restored imperial law under the firm rule of the High Justiciar.",
            "court_ducal_confederacy": "You gave noble autonomy to Duke Cassian and ended central taxes.",
            "court_guild_plutocracy": "You approved the trade pact to let merchant syndicates govern.",
            "court_unbounded_protector": "You cast out all three factions to govern the capital as Lord Regent.",
        },
        ending_conditions={
            "court_royalist_ascendancy": {"court_ending_royalist": True},
            "court_ducal_confederacy": {"court_ending_ducal": True},
            "court_guild_plutocracy": {"court_ending_guild": True},
            "court_unbounded_protector": {"court_ending_regent": True},
        },
    )


def subquest_scorchwaste_water_wars() -> QuestLine:
    """The Scorchwaste: Water Wars faction intrigue arc."""
    return QuestLine(
        id="subquest_scorchwaste_water_wars",
        name="The Scorchwaste Water Wars",
        synopsis="Intervene in the clash between Dune Nomads and the Salt Raider Cartel.",
        stages=[
            QuestStage(
                id="scorch_war_stage_exploration",
                title="Survey the Dune Ridge",
                province="scorchwaste",
                description="Brave hot desert winds to find the contested water pipe.",
                required_flags={},
                completion_flags={"scorch_pipeline_surveyed": True},
                reputation_rewards={"desert_nomads": 5},
                approaches=["survival", "scouting", "heat_endurance"],
            ),
            QuestStage(
                id="scorch_war_stage_alignment",
                title="The Oasis Parley",
                province="scorchwaste",
                description="Pledge to the water wardens or take a contract from the salt cartel.",
                required_flags={"scorch_pipeline_surveyed": True},
                completion_flags={"scorch_faction_chosen": True},
                reputation_rewards={"desert_nomads": 15, "salt_raiders": 15},
                approaches=["diplomacy", "extortion", "infiltration"],
            ),
            QuestStage(
                id="scorch_war_stage_crisis",
                title="Purge the Aquifer",
                province="scorchwaste",
                description="Clear caustic salt scale from the deep well pump.",
                required_flags={"scorch_faction_chosen": True},
                completion_flags={"scorch_crisis_resolved": True},
                reputation_rewards={"desert_nomads": 20, "caravaneers": 15},
                approaches=["force", "chemistry", "sabotage"],
            ),
            QuestStage(
                id="scorch_war_stage_resolution",
                title="Dominion of the Dunes",
                province="scorchwaste",
                description="Settle the rule of the desert aquifer at the central hub.",
                required_flags={"scorch_crisis_resolved": True},
                completion_flags={"scorch_war_resolved": True},
                reputation_rewards={"desert_nomads": 25, "salt_raiders": 25},
                approaches=["treaty", "monopoly", "sovereignty"],
            ),
        ],
        endings={
            "free_waters": "You broke the cartel blockade and returned pure water to all nomad tribes.",
            "cartel_monopoly": "You enforced the Salt Cartel monopoly over the desert wells for gold.",
            "desalination_concordat": "You made a fair treaty between caravans and nomad tribes.",
            "desert_autocrat": "You seized sole control of the deep aquifer keys to rule the dunes.",
        },
        ending_conditions={
            "free_waters": {"scorch_ending_free_water": True},
            "cartel_monopoly": {"scorch_ending_cartel_monopoly": True},
            "desalination_concordat": {"scorch_ending_concordat": True},
            "desert_autocrat": {"scorch_ending_autocrat": True},
        },
    )


def subquest_hollows_abyssal_schism() -> QuestLine:
    """The Sunken Hollows: Abyssal Schism faction intrigue arc."""
    return QuestLine(
        id="subquest_hollows_abyssal_schism",
        name="The Sunken Hollows Abyssal Schism",
        synopsis="Guide the struggle between deep scholars and salvage divers.",
        stages=[
            QuestStage(
                id="hollows_schism_stage_exploration",
                title="The Dark Plunge",
                province="sunken_hollows",
                description="Dive subterranean rapids to reach the lower sunken halls.",
                required_flags={},
                completion_flags={"hollows_rapids_navigated": True},
                reputation_rewards={"deep_clans": 5},
                approaches=["diving", "athletics", "buoyancy"],
            ),
            QuestStage(
                id="hollows_schism_stage_alignment",
                title="The Wharf Concordat",
                province="sunken_hollows",
                description="Align with Scholar Vance or hire Master Orlov salvage crew.",
                required_flags={"hollows_rapids_navigated": True},
                completion_flags={"hollows_faction_chosen": True},
                reputation_rewards={"deep_clans": 15, "trench_divers": 15},
                approaches=["scholarship", "bribery", "labor_union"],
            ),
            QuestStage(
                id="hollows_schism_stage_crisis",
                title="The Siphon Rupture",
                province="sunken_hollows",
                description="Stop rising water and severed air hoses inside the deep siphon.",
                required_flags={"hollows_faction_chosen": True},
                completion_flags={"hollows_crisis_resolved": True},
                reputation_rewards={"deep_clans": 20, "trench_divers": 20},
                approaches=["engineering", "diving_gear", "acoustic_tuning"],
            ),
            QuestStage(
                id="hollows_schism_stage_resolution",
                title="Fate of Abyssal Vault",
                province="sunken_hollows",
                description="Decide the fate of the primordial vault gates at the central hub.",
                required_flags={"hollows_crisis_resolved": True},
                completion_flags={"hollows_schism_resolved": True},
                reputation_rewards={"deep_clans": 25, "trench_divers": 25},
                approaches=["warding", "dredging", "awakening"],
            ),
        ],
        endings={
            "archive_sanctuary": "You warded the sunken temples to safeguard ancient history.",
            "cartel_dredge": "You helped the Brine Cartel claim the deep vaults for salvage.",
            "diver_commune": "You led working divers to form a free union commune.",
            "deluge_unsealed": "You broke the ancient seals and let primeval tides flood the caves.",
        },
        ending_conditions={
            "archive_sanctuary": {"hollows_ending_archive_sanctuary": True},
            "cartel_dredge": {"hollows_ending_cartel_dredge": True},
            "diver_commune": {"hollows_ending_diver_commune": True},
            "deluge_unsealed": {"hollows_ending_deluge_unsealed": True},
        },
    )


def subquest_lowlands_river_intrigue() -> QuestLine:
    """The Lowlands: River Sluice War faction intrigue arc."""
    return QuestLine(
        id="subquest_lowlands_river_intrigue",
        name="The Lowlands Sluice War",
        synopsis="Take a side in the canal war between shadow smugglers and river guild bailiffs.",
        stages=[
            QuestStage(
                id="lowlands_intrigue_stage_manifest",
                title="Intercept Customs Book",
                province="lowlands",
                description="Steal the customs book from the river gate before bailiffs lock the vault.",
                required_flags={},
                completion_flags={"lowlands_manifest_decided": True},
                reputation_rewards={"shadow_syndicate": 10, "river_guild": 10},
                approaches=["stealth", "rhetoric", "forgery"],
            ),
            QuestStage(
                id="lowlands_intrigue_stage_sluice",
                title="Control Canal Sluice",
                province="lowlands",
                description="Control the great canal sluice to dictate river barge traffic through the city.",
                required_flags={"lowlands_manifest_decided": True},
                completion_flags={"lowlands_sluice_decided": True},
                reputation_rewards={"shadow_syndicate": 15, "river_guild": 15},
                approaches=["mechanics", "force", "bribery"],
            ),
            QuestStage(
                id="lowlands_intrigue_stage_showdown",
                title="Harbor Bell Showdown",
                province="lowlands",
                description="Decide the fate of the harbor at the bell tower showdown.",
                required_flags={"lowlands_sluice_decided": True},
                completion_flags={"lowlands_river_intrigue_resolved": True},
                reputation_rewards={"shadow_syndicate": 25, "river_guild": 25},
                approaches=["signaling", "alarm", "diplomacy"],
            ),
        ],
        endings={
            "syndicate_ascendant": "You helped the smugglers seize the canal. Black market trade rules the harbor.",
            "river_guild_monopoly": "You helped the bailiffs lock the river. The guild enforces strict river tolls.",
            "clandestine_compact": "You brokered peace between both factions. Profit flows to you from both sides.",
        },
        ending_conditions={
            "syndicate_ascendant": {"lowlands_intrigue_syndicate_win": True},
            "river_guild_monopoly": {"lowlands_intrigue_guild_win": True},
            "clandestine_compact": {"lowlands_intrigue_compact_win": True},
        },
    )


def get_faction_intrigue_quests() -> Dict[str, QuestLine]:
    """Returns the Milestone 13 5-province faction intrigue questlines."""
    return {
        "quest_reach_faction_intrigue": quest_reach_faction_intrigue(),
        "quest_high_court_faction_intrigue": quest_high_court_faction_intrigue(),
        "subquest_scorchwaste_water_wars": subquest_scorchwaste_water_wars(),
        "subquest_hollows_abyssal_schism": subquest_hollows_abyssal_schism(),
        "subquest_lowlands_river_intrigue": subquest_lowlands_river_intrigue(),
    }


def get_provincial_subquests(include_intrigue: bool = False) -> Dict[str, QuestLine]:
    """Returns provincial subquests. Defaults to baseline subquests for backward compatibility."""
    quests = {
        "subquest_reach_smuggler_caches": subquest_reach_smuggler_caches(),
        "subquest_lowlands_shadow_broker": subquest_lowlands_shadow_broker(),
        "subquest_scorchwaste_water_baron": subquest_scorchwaste_water_baron(),
        "subquest_court_decrees": subquest_court_decrees(),
        "subquest_hollows_abyssal_keystones": subquest_hollows_abyssal_keystones(),
    }
    if include_intrigue:
        quests.update(get_faction_intrigue_quests())
    return quests


def get_provincial_subquest(quest_id: str) -> Optional[QuestLine]:
    """Retrieve a specific provincial subquest by its id or province keyword."""
    subquests = get_provincial_subquests(include_intrigue=True)
    if quest_id in subquests:
        return subquests[quest_id]
    for q in subquests.values():
        if q.id == quest_id:
            return q
        if q.stages and quest_id == q.stages[0].province:
            return q
    return None


def get_all_quests(include_intrigue: bool = False) -> List[QuestLine]:
    """Return all shipped quests."""
    return [get_continental_main_quest()] + list(get_provincial_subquests(include_intrigue=include_intrigue).values())


def evaluate_all_subquests(
    character: CharacterSheet, world_flags: Dict[str, Any], include_intrigue: bool = False
) -> Dict[str, Any]:
    """Evaluate progress across provincial subquest lines."""
    return {
        qid: quest.evaluate_progress(character, world_flags)
        for qid, quest in get_provincial_subquests(include_intrigue=include_intrigue).items()
    }


def evaluate_all_quests(
    character: CharacterSheet, world_flags: Dict[str, Any], include_intrigue: bool = False
) -> Dict[str, Any]:
    """Evaluate continental main quest and all provincial subquests."""
    main_prog = get_continental_main_quest().evaluate_progress(character, world_flags)
    sub_progs = evaluate_all_subquests(character, world_flags, include_intrigue=include_intrigue)
    res: Dict[str, Any] = {
        "main_quest": main_prog,
        "subquests": sub_progs,
    }
    res[get_continental_main_quest().id] = main_prog
    for qid, sprog in sub_progs.items():
        res[qid] = sprog
    return res


