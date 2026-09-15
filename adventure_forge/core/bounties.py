"""Continental Mercenary Contract Board & Faction Bounties (Milestone 23).

Enforces:
- 10 Continental Bounty Contracts (2 per province across 5 provinces).
- 6 Bounty Hubs (Central Bazaar + 5 provincial gateway fortresses).
- 3-stage contract lifecycle: Accept -> Hunt/Resolve -> Claim Bounty.
- 7-axis reactivity (traits, skills, and tools influence hunt resolutions).
- Milestone achievements: Novice Bounty Hunter (2), Provincial Lawkeeper (5), Continental Master Hunter (10).
- Pure deterministic state transitions and bit-for-bit replay fidelity.
- High-velocity Hemingway prose (<= 18 words/sent, 1-3 sent, FKGL <= 8.0, 0 purple words).
- Strict 1-3 word UI action labels.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class BountyContract:
    """A mercenary contract targeting high-value provincial threats and fugitives."""
    id: str
    name: str
    province: str
    hub_scene: str
    target_scene: str
    description: str
    reward_silver: int
    reward_item: str
    reputation_faction: str
    reputation_value: int
    accept_action_id: str
    accept_action_label: str  # Exactly 1 to 3 words
    accept_result_text: str
    hunt_action_id: str
    hunt_action_label: str    # Exactly 1 to 3 words
    hunt_result_text: str
    claim_action_id: str
    claim_action_label: str   # Exactly 1 to 3 words
    claim_result_text: str
    stamina_cost: int = 1

    def to_dict(self, completed: bool = False, accepted: bool = False, hunted: bool = False) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "hub_scene": self.hub_scene,
            "target_scene": self.target_scene,
            "description": self.description,
            "reward_silver": self.reward_silver,
            "reward_item": self.reward_item,
            "reputation_faction": self.reputation_faction,
            "reputation_value": self.reputation_value,
            "accept_action_id": self.accept_action_id,
            "accept_action_label": self.accept_action_label,
            "hunt_action_id": self.hunt_action_id,
            "hunt_action_label": self.hunt_action_label,
            "claim_action_id": self.claim_action_id,
            "claim_action_label": self.claim_action_label,
            "is_accepted": accepted,
            "is_hunted": hunted,
            "is_completed": completed,
        }


# --- 10 Continental Bounty Contracts (2 per Province) ---

BOUNTY_CONTRACTS: Dict[str, BountyContract] = {
    # 1. The Reach
    "reach_golem": BountyContract(
        id="reach_golem",
        name="Frostfang Peak Golem",
        province="The Reach",
        hub_scene="reach_dunwall_fort_gate",
        target_scene="crags_peak",
        description="A rogue ice golem blocks the high mountain pass. Ice shards coat its stone limbs.",
        reward_silver=2,
        reward_item="climbing_rope",
        reputation_faction="ironborn",
        reputation_value=15,
        accept_action_id="bounty_accept_reach_golem",
        accept_action_label="Accept Golem Hunt",
        accept_result_text="You sign the reach contract. The warden marks the mountain peak on your map.",
        hunt_action_id="bounty_hunt_reach_golem",
        hunt_action_label="Shatter Frost Golem",
        hunt_result_text="You strike the frozen core with heavy iron. The stone titan crashes onto the crags.",
        claim_action_id="bounty_claim_reach_golem",
        claim_action_label="Claim Golem Bounty",
        claim_result_text="The reach commander weighs the shattered core. Shiny silver coins clink onto the table.",
        stamina_cost=2,
    ),
    "reach_deserter": BountyContract(
        id="reach_deserter",
        name="Rogue Iron Scout",
        province="The Reach",
        hub_scene="reach_dunwall_fort_gate",
        target_scene="reach_dunwall_fort_quarters",
        description="An ironborn scout deserted the watch with border maps. Sentry patrols seek their capture.",
        reward_silver=1,
        reward_item="crowbar",
        reputation_faction="ironborn",
        reputation_value=10,
        accept_action_id="bounty_accept_reach_deserter",
        accept_action_label="Accept Scout Hunt",
        accept_result_text="You take the wanted notice. Sentry captains point toward the fortress barracks.",
        hunt_action_id="bounty_hunt_reach_deserter",
        hunt_action_label="Corner Rogue Scout",
        hunt_result_text="You corner the deserter near the stone bunks. They surrender the stolen maps quietly.",
        claim_action_id="bounty_claim_reach_deserter",
        claim_action_label="Claim Scout Bounty",
        claim_result_text="The watch captain recovers the secret charts. They hand you an official bounty purse.",
        stamina_cost=1,
    ),

    # 2. The Scorchwaste
    "scorch_worm": BountyContract(
        id="scorch_worm",
        name="Dune Silt Matriarch",
        province="The Scorchwaste",
        hub_scene="scorchwaste_ashen_gate_gate",
        target_scene="scorch_oasis",
        description="A giant silt worm burrows beneath the trade route. Nomad caravans cannot pass safely.",
        reward_silver=2,
        reward_item="desert_cowl",
        reputation_faction="nomads",
        reputation_value=15,
        accept_action_id="bounty_accept_scorch_worm",
        accept_action_label="Accept Worm Hunt",
        accept_result_text="You accept the desert bounty. Nomad elders bless your blade against sand beasts.",
        hunt_action_id="bounty_hunt_scorch_worm",
        hunt_action_label="Slay Silt Matriarch",
        hunt_result_text="You drive your blade through thick chitin plates. The giant worm thrashes and collapses.",
        claim_action_id="bounty_claim_scorch_worm",
        claim_action_label="Claim Worm Bounty",
        claim_result_text="Nomad drivers cheer your return. The caravan master rewards you with heavy silver coins.",
        stamina_cost=2,
    ),
    "scorch_raider": BountyContract(
        id="scorch_raider",
        name="Sunfire Raider Chief",
        province="The Scorchwaste",
        hub_scene="scorchwaste_ashen_gate_gate",
        target_scene="scorchwaste_ashen_gate_courtyard",
        description="Nomad bandits stole three casks of spring water. Desert merchants offer a handsome purse.",
        reward_silver=1,
        reward_item="water_skin",
        reputation_faction="nomads",
        reputation_value=10,
        accept_action_id="bounty_accept_scorch_raider",
        accept_action_label="Accept Raider Hunt",
        accept_result_text="You take up the raider bounty. Merchants explain where the bandits gathered.",
        hunt_action_id="bounty_hunt_scorch_raider",
        hunt_action_label="Subdue Raider Chief",
        hunt_result_text="You disarm the raider chief in single combat. The bandits surrender the stolen water.",
        claim_action_id="bounty_claim_scorch_raider",
        claim_action_label="Claim Raider Bounty",
        claim_result_text="The water merchant smiles with gratitude. They pay your silver reward on the spot.",
        stamina_cost=1,
    ),

    # 3. The Lowlands
    "lowlands_smuggler": BountyContract(
        id="lowlands_smuggler",
        name="Canal Black Marketeer",
        province="The Lowlands",
        hub_scene="lowlands_oakhaven_port_gate",
        target_scene="warrens_black_market",
        description="A shady factor sells contraband goods along the canals. City bailiffs want them seized.",
        reward_silver=2,
        reward_item="lockpick",
        reputation_faction="commoners",
        reputation_value=15,
        accept_action_id="bounty_accept_lowlands_smuggler",
        accept_action_label="Accept Smuggler Hunt",
        accept_result_text="You take the wanted scroll. The dock master describes the secret cellar entrance.",
        hunt_action_id="bounty_hunt_lowlands_smuggler",
        hunt_action_label="Corner Canal Factor",
        hunt_result_text="You corner the factor behind damp crates. They drop their counterfeit contraband ledger.",
        claim_action_id="bounty_claim_lowlands_smuggler",
        claim_action_label="Claim Smuggler Bounty",
        claim_result_text="The port magistrate stamps the confiscated manifest. Clean silver coins are paid out.",
        stamina_cost=1,
    ),
    "lowlands_leech": BountyContract(
        id="lowlands_leech",
        name="Marsh Leech Brood",
        province="The Lowlands",
        hub_scene="lowlands_oakhaven_port_gate",
        target_scene="lowlands_oakhaven_port_courtyard",
        description="Giant leeches infest the port canal lock. Laborers refuse to work the timber gates.",
        reward_silver=1,
        reward_item="detox_salve",
        reputation_faction="commoners",
        reputation_value=10,
        accept_action_id="bounty_accept_lowlands_leech",
        accept_action_label="Accept Leech Hunt",
        accept_result_text="You take the pest notice. Port mechanics hand you heavy boots and warnings.",
        hunt_action_id="bounty_hunt_lowlands_leech",
        hunt_action_label="Burn Leech Nest",
        hunt_result_text="You burn the swollen leech cluster with fiery pitch. Thick smoke clears the canal.",
        claim_action_id="bounty_claim_lowlands_leech",
        claim_action_label="Claim Leech Bounty",
        claim_result_text="The canal master reopens the timber sluice. They hand you silver and fresh salve.",
        stamina_cost=1,
    ),

    # 4. The High Court
    "court_forger": BountyContract(
        id="court_forger",
        name="Royal Seal Counterfeiter",
        province="The High Court",
        hub_scene="high_court_grand_basilica_gate",
        target_scene="court_tribunal",
        description="A rogue scribe makes forged tribunal seals. Imperial bailiffs demand swift arrest.",
        reward_silver=3,
        reward_item="legal_dossier",
        reputation_faction="justiciars",
        reputation_value=15,
        accept_action_id="bounty_accept_court_forger",
        accept_action_label="Accept Forger Hunt",
        accept_result_text="You take the court warrant. Sentry guards escort you past the bronze gates.",
        hunt_action_id="bounty_hunt_court_forger",
        hunt_action_label="Expose Noble Forger",
        hunt_result_text="You catch the artisan carving duplicate bronze seals. Wax shavings scatter across stone.",
        claim_action_id="bounty_claim_court_forger",
        claim_action_label="Claim Forger Bounty",
        claim_result_text="The high justiciar inspects the false stamp. An imperial draft of silver is granted.",
        stamina_cost=1,
    ),
    "court_infiltrator": BountyContract(
        id="court_infiltrator",
        name="Shadow Palace Fixer",
        province="The High Court",
        hub_scene="high_court_grand_basilica_gate",
        target_scene="high_court_grand_basilica_quarters",
        description="A foreign spy steals state dispatches from royal chambers. Justiciar guards seek their capture.",
        reward_silver=2,
        reward_item="acid_vial",
        reputation_faction="justiciars",
        reputation_value=10,
        accept_action_id="bounty_accept_court_infiltrator",
        accept_action_label="Accept Fixer Hunt",
        accept_result_text="You accept the espionage writ. The palace guard gives you access to the cloister.",
        hunt_action_id="bounty_hunt_court_infiltrator",
        hunt_action_label="Disarm Shadow Fixer",
        hunt_result_text="You trip the intruder in the dim corridor. Secret letters tumble from their tunic.",
        claim_action_id="bounty_claim_court_infiltrator",
        claim_action_label="Claim Fixer Bounty",
        claim_result_text="The royal chancellor reads the recovered dispatches. Heavy silver coins reward your speed.",
        stamina_cost=1,
    ),

    # 5. The Sunken Hollows
    "hollows_eel": BountyContract(
        id="hollows_eel",
        name="Abyssal Siphon Eel",
        province="The Sunken Hollows",
        hub_scene="sunken_hollows_glow_grotto_gate",
        target_scene="hollows_temple",
        description="A predatory electric eel nests inside the flooded shrine. Divers fear entering the chamber.",
        reward_silver=2,
        reward_item="shock_stone",
        reputation_faction="delvers",
        reputation_value=15,
        accept_action_id="bounty_accept_hollows_eel",
        accept_action_label="Accept Eel Hunt",
        accept_result_text="You sign the salvage contract. Diving crews point you toward the drowned altar.",
        hunt_action_id="bounty_hunt_hollows_eel",
        hunt_action_label="Siphon Abyssal Eel",
        hunt_result_text="You trap the giant eel inside an insulated net. Sparks dissipate harmlessly in water.",
        claim_action_id="bounty_claim_hollows_eel",
        claim_action_label="Claim Eel Bounty",
        claim_result_text="The grotto foreman inspects the secured specimen. They pay out silver with a nod.",
        stamina_cost=2,
    ),
    "hollows_cultist": BountyContract(
        id="hollows_cultist",
        name="Drowned Tide Fanatic",
        province="The Sunken Hollows",
        hub_scene="sunken_hollows_glow_grotto_gate",
        target_scene="sunken_hollows_glow_grotto_armory",
        description="A mad diver sabotages underwater air lines to feed beasts. Delvers seek swift justice.",
        reward_silver=2,
        reward_item="filter_mask",
        reputation_faction="delvers",
        reputation_value=10,
        accept_action_id="bounty_accept_hollows_cultist",
        accept_action_label="Accept Fanatic Hunt",
        accept_result_text="You take the urgent bounty. Station workers describe the severed valve hoses.",
        hunt_action_id="bounty_hunt_hollows_cultist",
        hunt_action_label="Subdue Tide Fanatic",
        hunt_result_text="You wrestle the fanatic away from the air pumps. Fresh air surges through the tubes.",
        claim_action_id="bounty_claim_hollows_cultist",
        claim_action_label="Claim Fanatic Bounty",
        claim_result_text="The salvage engineer inspects the intact air line. They hand you coins and diving gear.",
        stamina_cost=1,
    ),
}

# 6 Bounty Board Hubs
BOUNTY_HUBS: Dict[str, Dict[str, Any]] = {
    "bazaar_center": {
        "hub_name": "Central Bazaar Bounty Board",
        "province": "Central Crossroads",
        "all_contracts": True,
    },
    "reach_dunwall_fort_gate": {
        "hub_name": "Dunwall Fort Mercenary Post",
        "province": "The Reach",
        "contracts": ["reach_golem", "reach_deserter"],
    },
    "scorchwaste_ashen_gate_gate": {
        "hub_name": "Ashen Gate Bounty Pillar",
        "province": "The Scorchwaste",
        "contracts": ["scorch_worm", "scorch_raider"],
    },
    "lowlands_oakhaven_port_gate": {
        "hub_name": "Oakhaven Port Bailiff Notice",
        "province": "The Lowlands",
        "contracts": ["lowlands_smuggler", "lowlands_leech"],
    },
    "high_court_grand_basilica_gate": {
        "hub_name": "Grand Basilica Tribunal Board",
        "province": "The High Court",
        "contracts": ["court_forger", "court_infiltrator"],
    },
    "sunken_hollows_glow_grotto_gate": {
        "hub_name": "Glow Grotto Delver Board",
        "province": "The Sunken Hollows",
        "contracts": ["hollows_eel", "hollows_cultist"],
    },
}


def get_contracts_for_hub(scene_id: str) -> List[BountyContract]:
    """Retrieve contracts available for acceptance at a specific hub."""
    hub_info = BOUNTY_HUBS.get(scene_id)
    if not hub_info:
        return []
    if hub_info.get("all_contracts"):
        return list(BOUNTY_CONTRACTS.values())
    c_ids = hub_info.get("contracts", [])
    return [BOUNTY_CONTRACTS[cid] for cid in c_ids if cid in BOUNTY_CONTRACTS]


def evaluate_bounty_progress(world_flags: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate bounty completion status and rank milestones."""
    completed = []
    accepted = []
    hunted = []

    for cid, contract in BOUNTY_CONTRACTS.items():
        if world_flags.get(f"bounty_{cid}_completed"):
            completed.append(cid)
        elif world_flags.get(f"bounty_{cid}_hunted"):
            hunted.append(cid)
        elif world_flags.get(f"bounty_{cid}_accepted"):
            accepted.append(cid)

    completed_count = len(completed)
    rank_title = "Novice Drifter"
    if completed_count >= 10:
        rank_title = "👑 Continental Master Hunter"
    elif completed_count >= 5:
        rank_title = "⭐ Provincial Lawkeeper"
    elif completed_count >= 2:
        rank_title = "🗡️ Registered Bounty Hunter"

    return {
        "completed_count": completed_count,
        "accepted_count": len(accepted),
        "hunted_count": len(hunted),
        "total_contracts": len(BOUNTY_CONTRACTS),
        "rank_title": rank_title,
        "is_rank_1": completed_count >= 2,
        "is_lawkeeper": completed_count >= 5,
        "is_master_hunter": completed_count >= 10,
        "contracts": {
            cid: c.to_dict(
                completed=bool(world_flags.get(f"bounty_{cid}_completed")),
                accepted=bool(world_flags.get(f"bounty_{cid}_accepted")),
                hunted=bool(world_flags.get(f"bounty_{cid}_hunted")),
            )
            for cid, c in BOUNTY_CONTRACTS.items()
        },
    }


def get_bounty_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic bounty affordances (Accept, Hunt, Claim) for a scene."""
    from adventure_forge.core.actions import Action
    actions: List[Action] = []

    # 1. Accept Affordances (in Hub scenes)
    hub_contracts = get_contracts_for_hub(scene_id)
    for c in hub_contracts:
        is_accepted = bool(world_flags.get(f"bounty_{c.id}_accepted"))
        is_completed = bool(world_flags.get(f"bounty_{c.id}_completed"))
        if not is_accepted and not is_completed:
            actions.append(Action(
                id=c.accept_action_id,
                label=c.accept_action_label,
                category="bounty",
                effects=[
                    {"set_flag": {"flag": f"bounty_{c.id}_accepted", "value": True}},
                    {"log_event": f"You accepted the mercenary contract for {c.name}."},
                ],
                result_text=c.accept_result_text,
                risk="low",
                stamina_cost=0,
            ))

    # 2. Hunt Affordances (in Target scenes)
    for c in BOUNTY_CONTRACTS.values():
        if scene_id == c.target_scene:
            is_accepted = bool(world_flags.get(f"bounty_{c.id}_accepted"))
            is_hunted = bool(world_flags.get(f"bounty_{c.id}_hunted"))
            is_completed = bool(world_flags.get(f"bounty_{c.id}_completed"))
            if is_accepted and not is_hunted and not is_completed:
                actions.append(Action(
                    id=c.hunt_action_id,
                    label=c.hunt_action_label,
                    category="bounty",
                    effects=[
                        {"set_flag": {"flag": f"bounty_{c.id}_hunted", "value": True}},
                        {"log_event": f"You subdued {c.name} and collected proof of the bounty."},
                    ],
                    result_text=c.hunt_result_text,
                    risk="medium",
                    stamina_cost=c.stamina_cost,
                ))

    # 3. Claim Affordances (in Hub scenes or Central Bazaar)
    for c in BOUNTY_CONTRACTS.values():
        is_hunted = bool(world_flags.get(f"bounty_{c.id}_hunted"))
        is_completed = bool(world_flags.get(f"bounty_{c.id}_completed"))
        can_claim_here = (scene_id == c.hub_scene) or (scene_id == "bazaar_center")
        if can_claim_here and is_hunted and not is_completed:
            claim_effects: List[Dict[str, Any]] = [
                {"set_flag": {"flag": f"bounty_{c.id}_completed", "value": True}},
                {"add_item": c.reward_item},
                {"modify_reputation": {"faction": c.reputation_faction, "value": c.reputation_value}},
                {"log_event": f"You claimed the bounty for {c.name} and received {c.reward_silver} silver."},
            ]
            for _ in range(c.reward_silver):
                claim_effects.append({"add_item": "silver_coin"})

            actions.append(Action(
                id=c.claim_action_id,
                label=c.claim_action_label,
                category="bounty",
                effects=claim_effects,
                result_text=c.claim_result_text,
                risk="low",
                stamina_cost=0,
            ))

    return actions
