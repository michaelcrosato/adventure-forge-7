"""Milestone 30: Continental Dungeon Vaults, Arcane Keystones & Ancient Crypt Raids System.

Provides 6 Canonical Legendary Vaults situated at deep regional crypt vaults and crossroads,
7-axis lock breach affordances yielding ancient keystones and subterranean delve mastery,
dynamic field keystone attunement, reliquary realignment renewals, and Grandmaster Delver rank progression.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class AncientVault:
    """A continental deep vault with dedicated crypt scene, arcane keystone, and reliquary."""
    id: str
    name: str
    province: str
    vault_scene: str
    icon: str
    keystone_name: str
    domain: str
    description: str
    breach_action_id: str
    breach_action_label: str       # Exactly 1 to 3 words
    breach_result_text: str
    keystone_marker: str
    mastery_marker: str
    attune_action_id: str
    attune_action_label: str       # Exactly 1 to 3 words
    attune_result_text: str
    realign_action_id: str
    realign_action_label: str      # Exactly 1 to 3 words
    realign_result_text: str
    required_tool: str
    alternate_attribute: str
    alternate_attr_val: int
    alternate_trait: str

    def to_dict(
        self,
        is_unlocked: bool = False,
        has_keystone: bool = False,
        is_attuned: bool = False,
        has_mastery: bool = False,
    ) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "vault_scene": self.vault_scene,
            "icon": self.icon,
            "keystone_name": self.keystone_name,
            "domain": self.domain,
            "description": self.description,
            "breach_action_id": self.breach_action_id,
            "breach_action_label": self.breach_action_label,
            "keystone_marker": self.keystone_marker,
            "mastery_marker": self.mastery_marker,
            "attune_action_id": self.attune_action_id,
            "attune_action_label": self.attune_action_label,
            "realign_action_id": self.realign_action_id,
            "realign_action_label": self.realign_action_label,
            "required_tool": self.required_tool,
            "alternate_attribute": self.alternate_attribute,
            "alternate_attr_val": self.alternate_attr_val,
            "alternate_trait": self.alternate_trait,
            "is_unlocked": is_unlocked,
            "has_keystone": has_keystone,
            "is_attuned": is_attuned,
            "has_mastery": has_mastery,
        }


ANCIENT_VAULTS: Dict[str, AncientVault] = {
    "vault_frost_titan": AncientVault(
        id="vault_frost_titan",
        name="Frost Titan Glacial Vault",
        province="The Reach",
        vault_scene="reach_frost_cavern_vault",
        icon="🧊",
        keystone_name="Glacial Frost Keystone",
        domain="Glacial Crags & Frozen Reliquaries",
        description="Glacial arches support the mountain vault ceiling. Freezing northern breezes chill the reinforced iron portal.",
        breach_action_id="vault_breach_frost_titan",
        breach_action_label="Breach Frost Vault",
        breach_result_text="You bypass the frozen tumblers with mechanical skill. The heavy granite portal swings smoothly open.",
        keystone_marker="marker_keystone_frost_titan",
        mastery_marker="marker_delve_mastery_reach",
        attune_action_id="vault_attune_frost_titan",
        attune_action_label="Attune Frost Keystone",
        attune_result_text="You focus your mind upon the cold keystone. Enduring mountain stability strengthens your steps.",
        realign_action_id="vault_realign_frost_titan",
        realign_action_label="Realign Frost Reliquary",
        realign_result_text="You align the granite lockbox tumblers. Cold mountain resolve steadies your weary hands.",
        required_tool="lockpick",
        alternate_attribute="strength",
        alternate_attr_val=14,
        alternate_trait="iron_gutted",
    ),
    "vault_sol_serpent": AncientVault(
        id="vault_sol_serpent",
        name="Sunfire Serpent Tomb Vault",
        province="The Scorchwaste",
        vault_scene="scorchwaste_sun_shrine_vault",
        icon="🔥",
        keystone_name="Solar Serpent Keystone",
        domain="Desert Crypts & Bronze Reliquaries",
        description="Carved sandstone columns support the ancient desert crypt. Intense subterranean heat fills the stone chamber.",
        breach_action_id="vault_breach_sol_serpent",
        breach_action_label="Breach Sun Vault",
        breach_result_text="You manipulate the brass tumblers with mechanical precision. The massive bronze vault gate swings wide.",
        keystone_marker="marker_keystone_sol_serpent",
        mastery_marker="marker_delve_mastery_scorchwaste",
        attune_action_id="vault_attune_sol_serpent",
        attune_action_label="Attune Sun Keystone",
        attune_result_text="You channel warm energy from the sun keystone. Radiant desert warmth restores your fighting spirit.",
        realign_action_id="vault_realign_sol_serpent",
        realign_action_label="Realign Sun Reliquary",
        realign_result_text="You reset the bronze locking pins in order. Desert patience renews your physical stamina.",
        required_tool="skeleton_key",
        alternate_attribute="agility",
        alternate_attr_val=14,
        alternate_trait="nimble",
    ),
    "vault_abyssal_temple": AncientVault(
        id="vault_abyssal_temple",
        name="Abyssal Drowned Temple Vault",
        province="The Sunken Hollows",
        vault_scene="sunken_hollows_drowned_temple_vault",
        icon="🫧",
        keystone_name="Abyssal Drowned Keystone",
        domain="Flooded Grottos & Tidal Reliquaries",
        description="Submerged basalt columns support the flooded crypt ceiling. Cold oceanic currents flow past the iron portal.",
        breach_action_id="vault_breach_abyssal_temple",
        breach_action_label="Breach Abyssal Vault",
        breach_result_text="You bypass the aquatic lock mechanisms with surgical care. The heavy waterlogged gate creaks open.",
        keystone_marker="marker_keystone_abyssal_temple",
        mastery_marker="marker_delve_mastery_sunken",
        attune_action_id="vault_attune_abyssal_temple",
        attune_action_label="Attune Abyssal Keystone",
        attune_result_text="You hold the damp aquatic keystone aloft. Deep tidal currents strengthen your inner resolve.",
        realign_action_id="vault_realign_abyssal_temple",
        realign_action_label="Realign Abyssal Reliquary",
        realign_result_text="You align the submerged brass latch mechanisms with precision. Deep tidal calm restores your breathing.",
        required_tool="crowbar",
        alternate_attribute="endurance",
        alternate_attr_val=14,
        alternate_trait="water_breather",
    ),
    "vault_silver_palatine": AncientVault(
        id="vault_silver_palatine",
        name="Palatine Ducal Treasury Vault",
        province="The High Court",
        vault_scene="high_court_silver_vault_vault",
        icon="🪙",
        keystone_name="Palatine Silver Keystone",
        domain="Imperial Treasuries & Gilded Reliquaries",
        description="Polished marble pillars support the imperial treasury vault. Gilded heraldic crests gleam along the wall.",
        breach_action_id="vault_breach_silver_palatine",
        breach_action_label="Breach Palatine Vault",
        breach_result_text="You pick the imperial lock with surgical skill. The grand treasury door swings inward silently.",
        keystone_marker="marker_keystone_silver_palatine",
        mastery_marker="marker_delve_mastery_high_court",
        attune_action_id="vault_attune_silver_palatine",
        attune_action_label="Attune Palatine Keystone",
        attune_result_text="You examine the polished silver keystone with care. Noble courtly poise steadies your inner resolve.",
        realign_action_id="vault_realign_silver_palatine",
        realign_action_label="Realign Palatine Reliquary",
        realign_result_text="You reset the palace locking bolts with care. Noble discipline restores your courtly stamina.",
        required_tool="lockpick",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="skeptical",
    ),
    "vault_bell_catacomb": AncientVault(
        id="vault_bell_catacomb",
        name="Harbor Bell Catacomb Vault",
        province="The Lowlands",
        vault_scene="lowlands_bell_tower_vault",
        icon="⚓",
        keystone_name="Harbor Bell Keystone",
        domain="Canal Catacombs & Bronze Lockboxes",
        description="Heavy wooden beams support the subterranean river vault. Damp fog drifts through iron ceiling grates.",
        breach_action_id="vault_breach_bell_catacomb",
        breach_action_label="Breach Harbor Vault",
        breach_result_text="You manipulate the corroded tumblers with delicate skill. The heavy harbor vault door opens wide.",
        keystone_marker="marker_keystone_bell_catacomb",
        mastery_marker="marker_delve_mastery_lowlands",
        attune_action_id="vault_attune_bell_catacomb",
        attune_action_label="Attune Harbor Keystone",
        attune_result_text="You examine the salt-stained bronze keystone with care. Coastal harbor resolve steadies your travel pace.",
        realign_action_id="vault_realign_bell_catacomb",
        realign_action_label="Realign Harbor Reliquary",
        realign_result_text="You lubricate the heavy dockyard locking bolts. Salty sea air renews your travel resolve.",
        required_tool="iron_crank",
        alternate_attribute="agility",
        alternate_attr_val=14,
        alternate_trait="streetwise",
    ),
    "vault_crossroads_crypt": AncientVault(
        id="vault_crossroads_crypt",
        name="Grand Sovereign Under-Vault",
        province="Central Crossroads",
        vault_scene="bazaar_center",
        icon="👑",
        keystone_name="Grand Sovereign Keystone",
        domain="Continental Foundations & Imperial Reliquaries",
        description="Five massive archways support the central stone vault. Caravan trade banners hang along the passage.",
        breach_action_id="vault_breach_crossroads_crypt",
        breach_action_label="Breach Crossroads Vault",
        breach_result_text="You solve the intricate crossroads lock mechanism. The ancient sovereign vault door glides open.",
        keystone_marker="marker_keystone_crossroads_crypt",
        mastery_marker="marker_delve_mastery_crossroads",
        attune_action_id="vault_attune_crossroads_crypt",
        attune_action_label="Attune Sovereign Keystone",
        attune_result_text="You harmonize with the grand sovereign keystone. Continental trade roads guide your travel resolve.",
        realign_action_id="vault_realign_crossroads_crypt",
        realign_action_label="Realign Sovereign Reliquary",
        realign_result_text="You align the master crossroads locking pins. Grand market harmony restores your focused resolve.",
        required_tool="lockpick",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="nimble",
    ),
}

# Delver rank progression tiers
DELVER_RANKS: List[Dict[str, Any]] = [
    {
        "count": 0,
        "title": "Unproven Delver",
        "desc": "You hold no ancient keystones or breached vaults. Continental dungeons remain completely locked in your journey.",
    },
    {
        "count": 1,
        "title": "Crypt Breacher",
        "desc": "You have breached your first ancient provincial vault. Subterranean travel experience guides your journey.",
    },
    {
        "count": 2,
        "title": "Tomb Raider",
        "desc": "Two legendary provincial crypts have yielded their keystones. Ancient locking mechanisms appear clear in your mind.",
    },
    {
        "count": 3,
        "title": "Vault Specialist",
        "desc": "Three continental vaults have been breached with skill. Dangerous dungeon hazards no longer impede your progress.",
    },
    {
        "count": 4,
        "title": "Master Infiltrator",
        "desc": "Four ancient provincial vaults are unlocked with care. Your dungeon mastery commands great respect.",
    },
    {
        "count": 5,
        "title": "Lord of Five Vaults",
        "desc": "All five provincial vaults are unlocked with care. You command complete subterranean knowledge across the realm.",
    },
    {
        "count": 6,
        "title": "Grandmaster of Crypts",
        "desc": "All continental vaults and crossroads under-vaults are breached. You hold complete dungeon mastery across the land.",
    },
]


def get_delver_rank(unlocked_count: int) -> Dict[str, str]:
    """Determine Delver rank title and description from unlocked vault count."""
    best = DELVER_RANKS[0]
    for tier in DELVER_RANKS:
        if unlocked_count >= tier["count"]:
            best = tier
    return {"title": str(best["title"]), "desc": str(best["desc"])}


def evaluate_vaults_progress(
    flags: Dict[str, Any],
    inventory: List[str],
    markers: List[str],
    current_scene: str = ""
) -> Dict[str, Any]:
    """Deterministic evaluation of dungeon vaults, delver rank, and active keystones."""
    marker_set = {str(m).lower() for m in markers}
    unlocked_count = 0
    active_keystones_count = 0
    active_masteries_count = 0
    vault_list = []
    current_scene_vault = None

    for v in ANCIENT_VAULTS.values():
        is_unlocked = bool(flags.get(f"vault_unlocked_{v.id}", False)) or bool(flags.get(f"vault_breached_{v.id}", False))
        has_keystone = v.keystone_marker.lower() in marker_set
        is_attuned = bool(flags.get(f"vault_attuned_{v.id}", False))
        has_mastery = v.mastery_marker.lower() in marker_set

        if is_unlocked:
            unlocked_count += 1
        if has_keystone:
            active_keystones_count += 1
        if has_mastery:
            active_masteries_count += 1

        if current_scene == v.vault_scene:
            current_scene_vault = v.id

        vault_list.append(
            v.to_dict(
                is_unlocked=is_unlocked,
                has_keystone=has_keystone,
                is_attuned=is_attuned,
                has_mastery=has_mastery,
            )
        )

    rank_info = get_delver_rank(unlocked_count)
    progress_pct = round((unlocked_count / max(1, len(ANCIENT_VAULTS))) * 100, 1)

    return {
        "vaults": vault_list,
        "unlocked_count": unlocked_count,
        "breached_count": unlocked_count,
        "total_vaults": len(ANCIENT_VAULTS),
        "active_keystones_count": active_keystones_count,
        "active_masteries_count": active_masteries_count,
        "delver_rank": rank_info["title"],
        "rank_desc": rank_info["desc"],
        "progress_pct": progress_pct,
        "current_scene_vault": current_scene_vault,
    }


def get_vaults_progress(state: Any) -> Dict[str, Any]:
    """Compute deterministic vault progress and delver rank from GameState."""
    flags = state.world_flags if hasattr(state, "world_flags") else getattr(state, "flags", {})
    char = getattr(state, "character", None)
    inv = getattr(char, "inventory", []) if char else []
    markers = getattr(char, "markers", []) if char else []
    current_scene = getattr(state, "current_scene", "")
    return evaluate_vaults_progress(flags, inv, markers, current_scene)


def get_vault_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic vault breach, keystone attunement, and reliquary realignment affordances."""
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

    # Generic lock bypass tools that satisfy hardware requirements
    breach_tools = {
        "lockpick",
        "lockpicks",
        "lockpick_set",
        "item_lockpicks",
        "skeleton_key",
        "crowbar",
        "iron_crank",
        "iron_spike",
        "tinkering_tools",
    }
    has_any_breach_tool = any(t in inv_list for t in breach_tools) or any(
        any(k in item for k in ["lockpick", "skeleton_key", "crowbar", "crank", "tinkering"])
        for item in inv_list
    )

    # 1. Crypt Vault Breaches and Reliquary Realignments
    for v in ANCIENT_VAULTS.values():
        if scene_id == v.vault_scene:
            is_unlocked = bool(world_flags.get(f"vault_unlocked_{v.id}", False)) or bool(
                world_flags.get(f"vault_breached_{v.id}", False)
            )
            is_attuned = bool(world_flags.get(f"vault_attuned_{v.id}", False))

            if not is_unlocked:
                # 7-axis qualification:
                # 1. Has specific tool or generic breach tool
                # 2. Has relevant traits
                # 3. Has high attribute (>= 14)
                # 4. Has relevant skills (cunning, stealth, athletics >= 2)
                # 5. Has physical stamina (stamina >= 2)
                has_tool = (v.required_tool.lower() in inv_list) or has_any_breach_tool
                has_trait = (v.alternate_trait.lower() in traits_list) or any(
                    t in traits_list
                    for t in [
                        "locksmith",
                        "dungeon_diver",
                        "nimble",
                        "streetwise",
                        "infiltrator",
                        "water_breather",
                        "iron_gutted",
                    ]
                )
                attr_val = character.get_attribute(v.alternate_attribute)
                has_attr = (attr_val >= v.alternate_attr_val) or (character.get_attribute("wits") >= 14)
                has_skill = (
                    skills_dict.get("cunning", 0) >= 2
                    or skills_dict.get("stealth", 0) >= 2
                    or skills_dict.get("athletics", 0) >= 2
                )
                has_stam = getattr(character, "stamina", 0) >= 2

                if has_tool or has_trait or has_attr or has_skill or has_stam:
                    affordances.append(
                        Action(
                            id=v.breach_action_id,
                            label=v.breach_action_label,
                            category="exploration",
                            effects=[
                                {"set_flag": {"flag": f"vault_unlocked_{v.id}", "value": True}},
                                {"add_marker": v.keystone_marker},
                                {"add_marker": v.mastery_marker},
                                {"modify_stamina": 3},
                                {"log_event": v.breach_result_text},
                            ],
                            result_text=v.breach_result_text,
                            risk="low",
                            stamina_cost=0,
                        )
                    )
            elif is_attuned:
                # Can realign and secure reliquary at vault scene
                affordances.append(
                    Action(
                        id=v.realign_action_id,
                        label=v.realign_action_label,
                        category="exploration",
                        effects=[
                            {"set_flag": {"flag": f"vault_attuned_{v.id}", "value": False}},
                            {"modify_stamina": 2},
                            {"log_event": v.realign_result_text},
                        ],
                        result_text=v.realign_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    # 2. Field Keystone Attunement anywhere in the continental world
    for v in ANCIENT_VAULTS.values():
        if v.keystone_marker.lower() in marker_list:
            is_attuned = bool(world_flags.get(f"vault_attuned_{v.id}", False))
            if not is_attuned:
                affordances.append(
                    Action(
                        id=v.attune_action_id,
                        label=v.attune_action_label,
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": f"vault_attuned_{v.id}", "value": True}},
                            {"add_marker": f"marker_attuned_{v.id}"},
                            {"modify_stamina": 3},
                            {"log_event": v.attune_result_text},
                        ],
                        result_text=v.attune_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    return affordances
