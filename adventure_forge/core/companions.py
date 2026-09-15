"""Milestone 24: Continental Companion Recruiter & Follower Synergy System.

Provides 5 provincial companions (1 per province) situated at regional garrison courtyards:
1. The Reach: Kaelen Stonebreaker (Ironborn Vanguard) at reach_dunwall_fort_courtyard
2. The Scorchwaste: Sariyah Dune-Walker (Nomad Pathfinder) at scorchwaste_ashen_gate_courtyard
3. The Lowlands: Bram the Smuggler (Riverfolk Scoundrel) at lowlands_oakhaven_port_courtyard
4. The High Court: Lady Elenore of Veras (Court Justiciar) at high_court_grand_basilica_courtyard
5. The Sunken Hollows: Tarek Deep-Delver (Grotto Siphonist) at sunken_hollows_glow_grotto_courtyard

Implements 7-axis recruitment evaluation, active party slot management,
fellowship milestone ranks, and dynamic companion affordances.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class Companion:
    """A provincial companion who can join the protagonist's warband."""
    id: str
    name: str
    title: str
    province: str
    home_scene: str
    description: str
    perk_name: str
    perk_description: str
    recruit_action_id: str
    recruit_action_label: str  # Exactly 1 to 3 words
    recruit_result_text: str
    dismiss_action_id: str
    dismiss_action_label: str  # Exactly 1 to 3 words
    dismiss_result_text: str
    talk_action_id: str
    talk_action_label: str     # Exactly 1 to 3 words
    talk_result_text: str
    activate_action_id: str
    activate_action_label: str # Exactly 1 to 3 words
    activate_result_text: str
    stamina_cost: int = 0

    def to_dict(self, is_recruited: bool = False, is_active: bool = False) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "province": self.province,
            "home_scene": self.home_scene,
            "description": self.description,
            "perk_name": self.perk_name,
            "perk_description": self.perk_description,
            "recruit_action_id": self.recruit_action_id,
            "recruit_action_label": self.recruit_action_label,
            "dismiss_action_id": self.dismiss_action_id,
            "dismiss_action_label": self.dismiss_action_label,
            "talk_action_id": self.talk_action_id,
            "talk_action_label": self.talk_action_label,
            "activate_action_id": self.activate_action_id,
            "activate_action_label": self.activate_action_label,
            "is_recruited": is_recruited,
            "is_active": is_active,
        }


# --- 5 Provincial Companions (1 per Province) ---

COMPANIONS: Dict[str, Companion] = {
    # 1. The Reach
    "kaelen": Companion(
        id="kaelen",
        name="Kaelen Stonebreaker",
        title="Ironborn Vanguard",
        province="The Reach",
        home_scene="reach_dunwall_fort_courtyard",
        description="A hulking Ironborn warrior sharpens his broadaxe near the armory rack. Scarred plates protect his chest.",
        perk_name="Highland Fortitude",
        perk_description="Reduces stamina fatigue and bolsters posture against crag tremors.",
        recruit_action_id="companion_recruit_kaelen",
        recruit_action_label="Recruit Kaelen",
        recruit_result_text="Kaelen clasps your arm with an iron grip. He slings his waraxe across heavy iron pauldrons.",
        dismiss_action_id="companion_dismiss_kaelen",
        dismiss_action_label="Dismiss Kaelen",
        dismiss_result_text="Kaelen salutes with his battle axe. He turns back toward the fortress barracks with steady strides.",
        talk_action_id="companion_talk_kaelen",
        talk_action_label="Consult Kaelen",
        talk_result_text="Kaelen scans the terrain with cold vigilance. He advises keeping your shield raised against mountain archers.",
        activate_action_id="companion_activate_kaelen",
        activate_action_label="Summon Kaelen",
        activate_result_text="Kaelen steps forward into your vanguard. His iron pauldrons clank against heavy stone armor.",
    ),

    # 2. The Scorchwaste
    "sariyah": Companion(
        id="sariyah",
        name="Sariyah Dune-Walker",
        title="Nomad Pathfinder",
        province="The Scorchwaste",
        home_scene="scorchwaste_ashen_gate_courtyard",
        description="A keen nomad scout adjusts her sand goggles against the blowing silt. A bone composite bow rests across her back.",
        perk_name="Dune Navigation",
        perk_description="Resists scorching heat and spots hidden water caches across dry wastes.",
        recruit_action_id="companion_recruit_sariyah",
        recruit_action_label="Recruit Sariyah",
        recruit_result_text="Sariyah nods with a knowing smile. She checks her water flasks and steps forward into your march.",
        dismiss_action_id="companion_dismiss_sariyah",
        dismiss_action_label="Dismiss Sariyah",
        dismiss_result_text="Sariyah fastens her desert cowl. She heads toward the nearest nomad campfire to await your summons.",
        talk_action_id="companion_talk_sariyah",
        talk_action_label="Consult Sariyah",
        talk_result_text="Sariyah tests the desert wind with raised fingers. She points out hidden footholds across the rocky ridges.",
        activate_action_id="companion_activate_sariyah",
        activate_action_label="Summon Sariyah",
        activate_result_text="Sariyah unslings her recurve bow. She takes point along the march with silent desert steps.",
    ),

    # 3. The Lowlands
    "bram": Companion(
        id="bram",
        name="Bram the Smuggler",
        title="Riverfolk Scoundrel",
        province="The Lowlands",
        home_scene="lowlands_oakhaven_port_courtyard",
        description="A wiry riverboat smuggler counts heavy brass tokens on a wooden barrel. Dual daggers hang at his belt.",
        perk_name="Black Market Fence",
        perk_description="Unlocks shadow barter discounts and bypasses city bailiff inspections.",
        recruit_action_id="companion_recruit_bram",
        recruit_action_label="Recruit Bram",
        recruit_result_text="Bram pockets his brass tokens with a quick grin. He pulls up his dark wool hood and falls into rank.",
        dismiss_action_id="companion_dismiss_bram",
        dismiss_action_label="Dismiss Bram",
        dismiss_result_text="Bram gives an informal salute. He slips into the crowded market stalls with silent footsteps.",
        talk_action_id="companion_talk_bram",
        talk_action_label="Consult Bram",
        talk_result_text="Bram shares a trade secret behind his hand. He flags local bribe rates and hidden alley exits.",
        activate_action_id="companion_activate_bram",
        activate_action_label="Summon Bram",
        activate_result_text="Bram joins your flank with a subtle grin. He loosens his daggers inside worn leather sheaths.",
    ),

    # 4. The High Court
    "elenore": Companion(
        id="elenore",
        name="Lady Elenore of Veras",
        title="Court Justiciar",
        province="The High Court",
        home_scene="high_court_grand_basilica_courtyard",
        description="An armored High Court arbiter studies imperial law codices beneath stone arches. A gilded dueling rapier rests at her side.",
        perk_name="Aristocratic Decorum",
        perk_description="Disarms noble suspicion and earns judicial favor during tribunal hearings.",
        recruit_action_id="companion_recruit_elenore",
        recruit_action_label="Recruit Elenore",
        recruit_result_text="Lady Elenore bows with court grace. She pledges her rapier and royal aid to your continental trek.",
        dismiss_action_id="companion_dismiss_elenore",
        dismiss_action_label="Dismiss Elenore",
        dismiss_result_text="Lady Elenore gives a neat court bow. She walks toward palace halls to read ancient court records.",
        talk_action_id="companion_talk_elenore",
        talk_action_label="Consult Elenore",
        talk_result_text="Lady Elenore studies court laws with calm focus. She warns against offending local judges during legal trials.",
        activate_action_id="companion_activate_elenore",
        activate_action_label="Summon Elenore",
        activate_result_text="Lady Elenore draws her gilded rapier in salute. She steps beside you with imperial poise.",
    ),

    # 5. The Sunken Hollows
    "tarek": Companion(
        id="tarek",
        name="Tarek Deep-Delver",
        title="Grotto Siphonist",
        province="The Sunken Hollows",
        home_scene="sunken_hollows_glow_grotto_courtyard",
        description="A sturdy delver engineer adjusts bronze valves along a hydrostatic siphon suit. Heavy diving wrenches cling to his harness.",
        perk_name="Submersible Engineering",
        perk_description="Reinforces pressure valves and sustains oxygen buffers inside flooded caverns.",
        recruit_action_id="companion_recruit_tarek",
        recruit_action_label="Recruit Tarek",
        recruit_result_text="Tarek tightens his brass pressure gauge. He hoists his salvage pack and pledges his diving gear to your party.",
        dismiss_action_id="companion_dismiss_tarek",
        dismiss_action_label="Dismiss Tarek",
        dismiss_result_text="Tarek nods toward the grotto staging docks. He returns to his workshop benches to service spare air pumps.",
        talk_action_id="companion_talk_tarek",
        talk_action_label="Consult Tarek",
        talk_result_text="Tarek inspects your breathing gear with experienced hands. He checks hydrostatic air lines for hairline fractures before diving.",
        activate_action_id="companion_activate_tarek",
        activate_action_label="Summon Tarek",
        activate_result_text="Tarek buckles his bronze diving helmet to his chest harness. He takes position at your side with heavy wrench in hand.",
    ),
}


def can_recruit_companion(companion_id: str, character: CharacterSheet) -> bool:
    """Evaluate 7-axis character prerequisites for companion recruitment."""
    c = COMPANIONS.get(companion_id)
    if not c:
        return False

    inv = character.inventory
    if isinstance(inv, list):
        coins = inv.count("silver_coin")
    elif isinstance(inv, dict):
        coins = int(inv.get("silver_coin", 0))
    elif isinstance(inv, (set, tuple)):
        coins = 1 if "silver_coin" in inv else 0
    else:
        coins = 0
    has_coins = coins >= 2

    if companion_id == "kaelen":
        return (
            character.attributes.get("strength", 0) >= 6
            or character.skills.get("athletics", 0) >= 3
            or character.reputation.get("ironborn", 0) >= 5
            or character.reputation.get("iron_guard", 0) >= 5
            or character.has_trait("clan_ironborn")
            or character.has_trait("iron_gutted")
            or "iron" in character.background.lower()
            or "mercenary" in character.background.lower()
            or has_coins
        )
    if companion_id == "sariyah":
        return (
            character.attributes.get("perception", 0) >= 6
            or character.skills.get("survival", 0) >= 3
            or character.reputation.get("nomads", 0) >= 5
            or character.reputation.get("desert_nomads", 0) >= 5
            or character.has_trait("survivalist")
            or character.has_trait("heat_tolerant")
            or "nomad" in character.ancestry.lower()
            or "dune" in character.background.lower()
            or has_coins
        )
    if companion_id == "bram":
        return (
            character.attributes.get("cunning", 0) >= 6
            or character.skills.get("cunning", 0) >= 3
            or character.reputation.get("syndicate", 0) >= 5
            or character.has_trait("subterfuge")
            or "cutpurse" in character.background.lower()
            or "thief" in character.background.lower()
            or "smuggler" in character.background.lower()
            or has_coins
        )
    if companion_id == "elenore":
        return (
            character.attributes.get("charm", 0) >= 6
            or character.skills.get("rhetoric", 0) >= 3
            or character.reputation.get("justiciars", 0) >= 5
            or character.reputation.get("city_watch", 0) >= 5
            or character.has_trait("aristocrat")
            or "noble" in character.background.lower()
            or "courtier" in character.background.lower()
            or has_coins
        )
    if companion_id == "tarek":
        return (
            character.attributes.get("endurance", 0) >= 6
            or character.skills.get("engineering", 0) >= 3
            or character.reputation.get("delvers", 0) >= 5
            or character.reputation.get("deep_clans", 0) >= 5
            or character.has_trait("water_breather")
            or character.has_trait("delver")
            or "diver" in character.background.lower()
            or "abyssal" in character.background.lower()
            or has_coins
        )
    return False


def evaluate_companions_progress(world_flags: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate recruited warband roster, active companion, and fellowship rank."""
    recruited_ids = []
    active_id = str(world_flags.get("active_companion", "") or "")

    for cid in COMPANIONS:
        if world_flags.get(f"companion_{cid}_recruited"):
            recruited_ids.append(cid)

    # Validate active companion is indeed recruited
    if active_id and active_id not in recruited_ids:
        active_id = ""

    recruited_count = len(recruited_ids)
    rank_title = "Lone Wanderer"
    if recruited_count >= 5:
        rank_title = "👑 Master of the Fellowship"
    elif recruited_count >= 3:
        rank_title = "⚔️ Continental Warband"
    elif recruited_count >= 1:
        rank_title = "🛡️ Provincial Partner"

    active_obj = COMPANIONS.get(active_id)
    active_name = active_obj.name if active_obj else "None"
    active_perk = active_obj.perk_name if active_obj else "None"

    return {
        "recruited_count": recruited_count,
        "total_companions": len(COMPANIONS),
        "active_companion_id": active_id,
        "active_companion_name": active_name,
        "active_companion_perk": active_perk,
        "rank_title": rank_title,
        "is_partner": recruited_count >= 1,
        "is_warband": recruited_count >= 3,
        "is_master": recruited_count >= 5,
        "companions": {
            cid: c.to_dict(
                is_recruited=(cid in recruited_ids),
                is_active=(cid == active_id),
            )
            for cid, c in COMPANIONS.items()
        },
    }


def get_companion_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic companion affordances (Recruit, Summon, Consult, Dismiss)."""
    from adventure_forge.core.actions import Action
    actions: List[Action] = []

    active_id = str(world_flags.get("active_companion", "") or "")
    active_comp = COMPANIONS.get(active_id)

    # 1. Field Interaction with Active Companion (Available anywhere)
    if active_comp:
        actions.append(Action(
            id=active_comp.talk_action_id,
            label=active_comp.talk_action_label,
            category="companion",
            effects=[
                {"log_event": f"You consulted {active_comp.name} regarding current surroundings."},
            ],
            result_text=active_comp.talk_result_text,
            risk="low",
            stamina_cost=0,
        ))
        actions.append(Action(
            id=active_comp.dismiss_action_id,
            label=active_comp.dismiss_action_label,
            category="companion",
            effects=[
                {"set_flag": {"flag": "active_companion", "value": ""}},
                {"log_event": f"{active_comp.name} returned to camp."},
            ],
            result_text=active_comp.dismiss_result_text,
            risk="low",
            stamina_cost=0,
        ))

    # 2. Local Recruitment or Switching at Companion Home Scenes
    for cid, c in COMPANIONS.items():
        if scene_id == c.home_scene:
            is_recruited = bool(world_flags.get(f"companion_{cid}_recruited"))
            if not is_recruited:
                # Check prerequisites
                if can_recruit_companion(cid, character):
                    actions.append(Action(
                        id=c.recruit_action_id,
                        label=c.recruit_action_label,
                        category="companion",
                        effects=[
                            {"set_flag": {"flag": f"companion_{cid}_recruited", "value": True}},
                            {"set_flag": {"flag": "active_companion", "value": cid}},
                            {"log_event": f"{c.name} joined your expedition."},
                        ],
                        result_text=c.recruit_result_text,
                        risk="low",
                        stamina_cost=0,
                    ))
            elif cid != active_id:
                # Recruited companion is at home, can summon them
                actions.append(Action(
                    id=c.activate_action_id,
                    label=c.activate_action_label,
                    category="companion",
                    effects=[
                        {"set_flag": {"flag": "active_companion", "value": cid}},
                        {"log_event": f"{c.name} took point as your active traveling companion."},
                    ],
                    result_text=c.activate_result_text,
                    risk="low",
                    stamina_cost=0,
                ))

    # 3. Central Bazaar Warband Master Gathering (bazaar_center)
    if scene_id == "bazaar_center":
        for cid, c in COMPANIONS.items():
            is_recruited = bool(world_flags.get(f"companion_{cid}_recruited"))
            if is_recruited and cid != active_id:
                actions.append(Action(
                    id=c.activate_action_id,
                    label=c.activate_action_label,
                    category="companion",
                    effects=[
                        {"set_flag": {"flag": "active_companion", "value": cid}},
                        {"log_event": f"{c.name} took point as your active traveling companion."},
                    ],
                    result_text=c.activate_result_text,
                    risk="low",
                    stamina_cost=0,
                ))

    return actions
