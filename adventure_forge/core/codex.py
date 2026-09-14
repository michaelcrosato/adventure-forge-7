"""Provincial Ancient Lore Codex & Relic Inscription Engine (Milestone 19).

Provides pure, deterministic ancient lore deciphering across the 5 provinces:
- The Reach: The First Oath, Gryphon Riders, Frost Forge Mastery.
- The Lowlands: Under-City Tallies, Canal Genesis, The Tide Covenant.
- The Scorchwaste: The Solar Liturgy, The Cinder Kings, The Hidden Aquifers.
- The High Court: The First Decree, The Basilica Bells, The Dynasty Sepulcher.
- The Sunken Hollows: The Abyssal Psalms, Coral Symbiosis, The Drowned Armada.

Deciphering relics triggers 7-axis reactivity, consumes stamina, updates world flags,
awards narrative codex lore, and unlocks provincial lore masteries.
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.conditions import evaluate_condition


@dataclass(frozen=True)
class CodexEntry:
    """An authoritative collectible lore inscription within the world graph."""
    id: str
    title: str
    province: str
    province_key: str
    category: str
    scene_id: str
    action_id: str
    action_label: str  # Exactly 1 to 3 words
    stamina_cost: int
    condition: Dict[str, Any]
    discovery_text: str  # 1-2 sentences, <= 18 words/sent
    lore_text: str  # 1-2 sentences, <= 18 words/sent
    reward_flag: str
    granted_marker: Optional[str] = None

    def is_available(self, character: CharacterSheet, world_flags: Dict[str, Any]) -> bool:
        """Check if this entry can be deciphered by the character."""
        # Already discovered
        if world_flags.get(self.reward_flag, False):
            return False
        # Stamina check
        if character.stamina < self.stamina_cost:
            return False
        # Condition check
        return evaluate_condition(self.condition, character, world_flags)

    def build_effects(self, world_flags: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Construct the deterministic state mutation effects for deciphering this entry."""
        effects: List[Dict[str, Any]] = [
            {"set_flag": {"flag": self.reward_flag, "value": True}},
        ]
        if self.granted_marker:
            effects.append({"add_marker": self.granted_marker})

        # Check for provincial mastery (unlocking 3 entries in the province)
        current_in_province = sum(
            1 for e in CODEX_ENTRIES.values()
            if e.province_key == self.province_key and (world_flags.get(e.reward_flag, False) or e.id == self.id)
        )
        mastery_flag = f"{self.province_key}_mastery_unlocked"
        if current_in_province >= 3 and not world_flags.get(mastery_flag, False):
            mastery_info = PROVINCIAL_MASTERIES.get(self.province_key)
            if mastery_info:
                effects.append({"set_flag": {"flag": mastery_flag, "value": True}})
                effects.append({"add_marker": mastery_info["marker"]})
                effects.append({"log_event": f"Provincial Lore Mastery Achieved: {mastery_info['title']}!"})

        return effects

    def to_dict(self, unlocked: bool = False) -> Dict[str, Any]:
        """Serialize codex entry for API and UI presentation."""
        return {
            "id": self.id,
            "title": self.title,
            "province": self.province,
            "province_key": self.province_key,
            "category": self.category,
            "scene_id": self.scene_id,
            "action_id": self.action_id,
            "action_label": self.action_label,
            "stamina_cost": self.stamina_cost,
            "reward_flag": self.reward_flag,
            "unlocked": unlocked,
            "lore_text": self.lore_text if unlocked else None,
            "discovery_text": self.discovery_text if unlocked else None,
            "granted_marker": self.granted_marker,
        }


PROVINCIAL_MASTERIES: Dict[str, Dict[str, str]] = {
    "reach": {
        "title": "Reach Archivist",
        "marker": "reach_archivist",
        "description": "Mastery of ancient highland pacts and mountain lore.",
    },
    "lowlands": {
        "title": "Lowlands Chronicler",
        "marker": "lowlands_chronicler",
        "description": "Mastery of canal ciphers and harbor history.",
    },
    "scorchwaste": {
        "title": "Dune Antiquarian",
        "marker": "scorch_antiquarian",
        "description": "Mastery of solar dynasties and desert hydrology.",
    },
    "high_court": {
        "title": "Court Historian",
        "marker": "court_historian",
        "description": "Mastery of sovereign decrees and noble bloodlines.",
    },
    "sunken_hollows": {
        "title": "Abyssal Scholar",
        "marker": "abyssal_scholar",
        "description": "Mastery of sunken psalms and deep trench ecology.",
    },
}


CODEX_ENTRIES: Dict[str, CodexEntry] = {
    # --- The Reach ---
    "codex_reach_first_oath": CodexEntry(
        id="codex_reach_first_oath",
        title="The First Oath",
        province="The Reach",
        province_key="reach",
        category="History",
        scene_id="reach_secret_shrine",
        action_id="codex_study_first_oath",
        action_label="Study First Oath",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Mountain Scout"},
                {"has_trait": "Keen Mind"},
                {"background_is": "Reachman"},
                {"min_attribute": {"attribute": "intellect", "value": 3}},
                {"has_item": "torch"},
                {"has_item": "climbing_rope"},
            ]
        },
        discovery_text="You trace the ancient granite runes. Chiseled lines reveal the mountain pact.",
        lore_text="The high clans bound their blood to the stone. No king shall rule the aeries.",
        reward_flag="codex_reach_first_oath",
        granted_marker="lore_reach_first_oath",
    ),
    "codex_reach_gryphon_riders": CodexEntry(
        id="codex_reach_gryphon_riders",
        title="The Gryphon Riders",
        province="The Reach",
        province_key="reach",
        category="Factions",
        scene_id="reach_watch_ruin_sanctum",
        action_id="codex_examine_gryphon_perch",
        action_label="Examine Gryphon Perch",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Mountain Scout"},
                {"min_attribute": {"attribute": "agility", "value": 3}},
                {"min_skill": {"skill": "athletics", "value": 2}},
                {"has_item": "climbing_rope"},
                {"has_item": "torch"},
            ]
        },
        discovery_text="Faded carvings show armored scouts mounted upon raptors. Iron talons clutch the ridge.",
        lore_text="Winged scouts guarded the high pass. They monitored the lower valleys from the clouds.",
        reward_flag="codex_reach_gryphon_riders",
        granted_marker="lore_reach_gryphon_riders",
    ),
    "codex_reach_frost_forging": CodexEntry(
        id="codex_reach_frost_forging",
        title="Frost Forge Mastery",
        province="The Reach",
        province_key="reach",
        category="Arcana",
        scene_id="reach_frost_cavern_sanctum",
        action_id="codex_decipher_frost_stele",
        action_label="Decipher Frost Stele",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Cold Hardy"},
                {"has_trait": "Craftsman"},
                {"min_attribute": {"attribute": "might", "value": 3}},
                {"has_item": "fire_striker"},
                {"has_item": "torch"},
            ]
        },
        discovery_text="Frozen glyphs shimmer inside the cavern wall. Glacial ice preserves the smith tallies.",
        lore_text="Highland smiths quenched hot steel in glacial runoff. The resulting blades never notched or broke.",
        reward_flag="codex_reach_frost_forging",
        granted_marker="lore_reach_frost_forging",
    ),

    # --- The Lowlands ---
    "codex_lowlands_under_tallies": CodexEntry(
        id="codex_lowlands_under_tallies",
        title="Under-City Tallies",
        province="The Lowlands",
        province_key="lowlands",
        category="Factions",
        scene_id="lowlands_thieves_hall_sanctum",
        action_id="codex_read_guild_tallies",
        action_label="Read Guild Tallies",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Agile Fingers"},
                {"has_trait": "Shadow Walker"},
                {"background_is": "Street Drifter"},
                {"has_marker": "thief_guild_friend"},
                {"has_item": "lockpick"},
                {"min_skill": {"skill": "stealth", "value": 2}},
            ]
        },
        discovery_text="Notched slate marks the old cutpurse dues. Scratched ciphers detail hidden escape grates.",
        lore_text="The shadow guild collected harbor tribute. No cargo entered the docks without a mark.",
        reward_flag="codex_lowlands_under_tallies",
        granted_marker="lore_lowlands_under_tallies",
    ),
    "codex_lowlands_sluice_genesis": CodexEntry(
        id="codex_lowlands_sluice_genesis",
        title="The Canal Genesis",
        province="The Lowlands",
        province_key="lowlands",
        category="History",
        scene_id="lowlands_canal_sluice_sanctum",
        action_id="codex_inspect_sluice_masonry",
        action_label="Inspect Sluice Masonry",
        stamina_cost=1,
        condition={
            "any_of": [
                {"min_attribute": {"attribute": "might", "value": 3}},
                {"min_attribute": {"attribute": "intellect", "value": 3}},
                {"has_item": "crowbar"},
                {"has_item": "torch"},
                {"has_trait": "Craftsman"},
            ]
        },
        discovery_text="Weathered brass plaques document the canal digging. Early dredgers drained the salt marshes.",
        lore_text="Ten thousand laborers carved the drainage channels. Their effort created the thriving port trade.",
        reward_flag="codex_lowlands_sluice_genesis",
        granted_marker="lore_lowlands_sluice_genesis",
    ),
    "codex_lowlands_black_covenant": CodexEntry(
        id="codex_lowlands_black_covenant",
        title="The Tide Covenant",
        province="The Lowlands",
        province_key="lowlands",
        category="Arcana",
        scene_id="lowlands_smuggler_cove_sanctum",
        action_id="codex_decipher_smuggler_rune",
        action_label="Decipher Smuggler Rune",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Keen Senses"},
                {"has_trait": "Shadow Walker"},
                {"has_item": "torch"},
                {"has_item": "filter_mask"},
                {"min_skill": {"skill": "stealth", "value": 2}},
            ]
        },
        discovery_text="Luminescent pitch marks the tidal cavern. Hidden symbols warn of customs patrol routes.",
        lore_text="Smugglers timed their runs with the spring moons. Low tide revealed secret water passages.",
        reward_flag="codex_lowlands_black_covenant",
        granted_marker="lore_lowlands_black_covenant",
    ),

    # --- The Scorchwaste ---
    "codex_scorch_sun_hymn": CodexEntry(
        id="codex_scorch_sun_hymn",
        title="The Solar Liturgy",
        province="The Scorchwaste",
        province_key="scorchwaste",
        category="Dynasty",
        scene_id="scorchwaste_sun_shrine_sanctum",
        action_id="codex_decipher_sun_tablet",
        action_label="Decipher Sun Tablet",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Dune Strider"},
                {"has_trait": "Sun Hardened"},
                {"has_item": "desert_cowl"},
                {"min_attribute": {"attribute": "intellect", "value": 3}},
                {"min_skill": {"skill": "survival", "value": 2}},
            ]
        },
        discovery_text="Gold foil glints beneath red desert dust. Chiseled solar discs mark the equinox.",
        lore_text="Sun priests chanted at high noon. They believed solar heat purged pestilence and sin.",
        reward_flag="codex_scorch_sun_hymn",
        granted_marker="lore_scorch_sun_hymn",
    ),
    "codex_scorch_cinder_dynasty": CodexEntry(
        id="codex_scorch_cinder_dynasty",
        title="The Cinder Kings",
        province="The Scorchwaste",
        province_key="scorchwaste",
        category="History",
        scene_id="scorchwaste_buried_tomb_sanctum",
        action_id="codex_examine_royal_tomb",
        action_label="Examine Royal Tomb",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Dune Strider"},
                {"has_item": "torch"},
                {"has_item": "filter_mask"},
                {"min_attribute": {"attribute": "intellect", "value": 3}},
                {"min_skill": {"skill": "athletics", "value": 2}},
            ]
        },
        discovery_text="Basalt reliefs depict monarchs crowned in bronze. Sandstone urns guard dynastic ashes.",
        lore_text="The Cinder Kings ruled the southern basin before drought. Their palaces now sleep under silt.",
        reward_flag="codex_scorch_cinder_dynasty",
        granted_marker="lore_scorch_cinder_dynasty",
    ),
    "codex_scorch_aquifer_charts": CodexEntry(
        id="codex_scorch_aquifer_charts",
        title="The Hidden Aquifers",
        province="The Scorchwaste",
        province_key="scorchwaste",
        category="Ecology",
        scene_id="scorchwaste_nomad_well_vault",
        action_id="codex_transcribe_well_map",
        action_label="Transcribe Well Map",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Dune Strider"},
                {"has_trait": "Keen Senses"},
                {"has_item": "water_canteen"},
                {"min_attribute": {"attribute": "perception", "value": 3}},
                {"min_skill": {"skill": "survival", "value": 2}},
            ]
        },
        discovery_text="A sandstone disc maps underground wells. Carved ripples indicate deep fresh water.",
        lore_text="Nomads tracked water currents beneath the hardpan. A single deep bore supported thirty tribes.",
        reward_flag="codex_scorch_aquifer_charts",
        granted_marker="lore_scorch_aquifer_charts",
    ),

    # --- The High Court ---
    "codex_court_first_decree": CodexEntry(
        id="codex_court_first_decree",
        title="The First Decree",
        province="The High Court",
        province_key="high_court",
        category="Dynasty",
        scene_id="high_court_royal_archive_sanctum",
        action_id="codex_inspect_royal_parchment",
        action_label="Inspect Royal Parchment",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "High Decorum"},
                {"background_is": "Noble Exile"},
                {"has_marker": "court_signet"},
                {"has_marker": "noble_favor"},
                {"min_attribute": {"attribute": "intellect", "value": 3}},
                {"min_skill": {"skill": "rhetoric", "value": 2}},
            ]
        },
        discovery_text="An old vellum roll rests in glass. The first king signed the sovereign accord.",
        lore_text="The sovereign united the five warring provinces. Each lord swore fealty upon the High Throne.",
        reward_flag="codex_court_first_decree",
        granted_marker="lore_court_first_decree",
    ),
    "codex_court_golden_chimes": CodexEntry(
        id="codex_court_golden_chimes",
        title="The Basilica Bells",
        province="The High Court",
        province_key="high_court",
        category="Arcana",
        scene_id="high_court_grand_basilica_sanctum",
        action_id="codex_study_cathedral_inscription",
        action_label="Study Cathedral Inscription",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "High Decorum"},
                {"has_trait": "Keen Mind"},
                {"min_attribute": {"attribute": "perception", "value": 3}},
                {"min_skill": {"skill": "rhetoric", "value": 2}},
                {"has_item": "torch"},
            ]
        },
        discovery_text="Gilded engravings encircle the sanctuary plinth. Resonant bronze runes detail sacred harmonic law.",
        lore_text="Cathedral chimes signaled court assemblies. The bells rang to announce legal verdicts.",
        reward_flag="codex_court_golden_chimes",
        granted_marker="lore_court_golden_chimes",
    ),
    "codex_court_bloodline_vault": CodexEntry(
        id="codex_court_bloodline_vault",
        title="The Dynasty Sepulcher",
        province="The High Court",
        province_key="high_court",
        category="History",
        scene_id="high_court_catacomb_kings_sanctum",
        action_id="codex_read_royal_epitaph",
        action_label="Read Royal Epitaph",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "High Decorum"},
                {"background_is": "Noble Exile"},
                {"has_item": "torch"},
                {"has_item": "filter_mask"},
                {"min_attribute": {"attribute": "intellect", "value": 3}},
            ]
        },
        discovery_text="Marble sarcophagi line the solemn crypt. Engraved lineages trace seven noble houses.",
        lore_text="High-court bloodlines guarded their lineage with poison and arranged marriages. Ambition shaped the realm.",
        reward_flag="codex_court_bloodline_vault",
        granted_marker="lore_court_bloodline_vault",
    ),

    # --- The Sunken Hollows ---
    "codex_hollows_abyssal_psalms": CodexEntry(
        id="codex_hollows_abyssal_psalms",
        title="The Abyssal Psalms",
        province="The Sunken Hollows",
        province_key="sunken_hollows",
        category="Arcana",
        scene_id="sunken_hollows_drowned_temple_sanctum",
        action_id="codex_decipher_drowned_stele",
        action_label="Decipher Drowned Stele",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Abyssal Diver"},
                {"has_trait": "Water Born"},
                {"has_item": "pitch_seal"},
                {"has_item": "torch"},
                {"min_attribute": {"attribute": "perception", "value": 3}},
            ]
        },
        discovery_text="Pale algae coats the wet stone slab. Cold tide waters illuminate carved sea runes.",
        lore_text="Ancient acolytes prayed to the deep tide. They sought salvation beneath the crushing waves.",
        reward_flag="codex_hollows_abyssal_psalms",
        granted_marker="lore_hollows_abyssal_psalms",
    ),
    "codex_hollows_coral_symbiosis": CodexEntry(
        id="codex_hollows_coral_symbiosis",
        title="Coral Symbiosis",
        province="The Sunken Hollows",
        province_key="sunken_hollows",
        category="Ecology",
        scene_id="sunken_hollows_coral_chasm_sanctum",
        action_id="codex_examine_living_reef",
        action_label="Examine Living Reef",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Abyssal Diver"},
                {"has_trait": "Keen Senses"},
                {"has_item": "filter_mask"},
                {"min_attribute": {"attribute": "perception", "value": 3}},
                {"min_skill": {"skill": "survival", "value": 2}},
            ]
        },
        discovery_text="Stone coral branches form ancient signs. Glowing sea bulbs pulse in quiet sequence.",
        lore_text="Living coral filtered poison from the trench water. Deep dwellers harvested the glowing resin.",
        reward_flag="codex_hollows_coral_symbiosis",
        granted_marker="lore_hollows_coral_symbiosis",
    ),
    "codex_hollows_sunken_fleet": CodexEntry(
        id="codex_hollows_sunken_fleet",
        title="The Drowned Armada",
        province="The Sunken Hollows",
        province_key="sunken_hollows",
        category="History",
        scene_id="sunken_hollows_vault_depths_sanctum",
        action_id="codex_inspect_ship_carvings",
        action_label="Inspect Ship Carvings",
        stamina_cost=1,
        condition={
            "any_of": [
                {"has_trait": "Abyssal Diver"},
                {"min_attribute": {"attribute": "might", "value": 3}},
                {"has_item": "crowbar"},
                {"has_item": "pitch_seal"},
                {"has_item": "torch"},
            ]
        },
        discovery_text="Waterlogged timber displays fleet heraldry. Rotted hulls mark the final naval stand.",
        lore_text="An entire war fleet sank during the great cataclysm. Their iron hulls now form underwater reefs.",
        reward_flag="codex_hollows_sunken_fleet",
        granted_marker="lore_hollows_sunken_fleet",
    ),
}

# Fast lookup mappings
SCENE_TO_CODEX: Dict[str, List[CodexEntry]] = {}
ACTION_TO_CODEX: Dict[str, CodexEntry] = {}

for _entry in CODEX_ENTRIES.values():
    SCENE_TO_CODEX.setdefault(_entry.scene_id, []).append(_entry)
    ACTION_TO_CODEX[_entry.action_id] = _entry


def get_codex_entries_for_scene(scene_id: str) -> List[CodexEntry]:
    """Retrieve all codex entries situated at a given scene."""
    return list(SCENE_TO_CODEX.get(scene_id, []))


def get_codex_entry_by_action(action_id: str) -> Optional[CodexEntry]:
    """Retrieve the codex entry associated with an action id."""
    return ACTION_TO_CODEX.get(action_id)


def evaluate_codex_progress(world_flags: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate codex discovery status and provincial masteries across all entries."""
    discovered = []
    province_counts: Dict[str, int] = {k: 0 for k in PROVINCIAL_MASTERIES}
    masteries_unlocked = []

    for entry in CODEX_ENTRIES.values():
        is_unlocked = bool(world_flags.get(entry.reward_flag, False))
        if is_unlocked:
            discovered.append(entry.id)
            province_counts[entry.province_key] = province_counts.get(entry.province_key, 0) + 1

    for p_key, m_info in PROVINCIAL_MASTERIES.items():
        if world_flags.get(f"{p_key}_mastery_unlocked", False) or province_counts.get(p_key, 0) >= 3:
            masteries_unlocked.append({
                "province_key": p_key,
                "title": m_info["title"],
                "marker": m_info["marker"],
                "description": m_info["description"],
            })

    province_progress = {}
    for p_key, m_info in PROVINCIAL_MASTERIES.items():
        disc = province_counts.get(p_key, 0)
        province_progress[p_key] = {
            "title": m_info["title"],
            "discovered": disc,
            "total": 3,
            "mastery_unlocked": disc >= 3 or bool(world_flags.get(f"{p_key}_mastery_unlocked", False)),
        }

    return {
        "total_entries": len(CODEX_ENTRIES),
        "discovered_count": len(discovered),
        "discovered_ids": discovered,
        "masteries_unlocked": masteries_unlocked,
        "province_progress": province_progress,
        "entries": [
            entry.to_dict(unlocked=bool(world_flags.get(entry.reward_flag, False)))
            for entry in CODEX_ENTRIES.values()
        ],
    }
