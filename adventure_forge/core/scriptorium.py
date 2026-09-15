"""Continental Scriptoriums, Illuminator Desks & Master Calligrapher System (Milestone 34).

Defines 6 canonical ancient scriptoriums situated at regional quarters complexes
and crossroads. Supports 7-axis qualification (tools, traits, attributes, skills, stamina)
for transcribing illuminated manuscripts (+3 stamina, regional mastery marker), field recitation
anywhere in the continental world (+3 stamina, recited marker), and desk ink renewal (+2 stamina).
"""
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass(frozen=True)
class ContinentalScriptorium:
    """Specification for a canonical continental scriptorium desk."""
    id: str
    name: str
    province: str
    quarters_scene: str
    icon: str
    manuscript_name: str
    domain: str
    description: str
    inscribe_action_id: str
    inscribe_action_label: str
    inscribe_result_text: str
    manuscript_marker: str
    mastery_marker: str
    recite_action_id: str
    recite_action_label: str
    recite_result_text: str
    renew_action_id: str
    renew_action_label: str
    renew_result_text: str
    required_tool: str = "quill_and_ink"
    alternate_attribute: str = "wits"
    alternate_attr_val: int = 14
    alternate_trait: str = "scholar"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "quarters_scene": self.quarters_scene,
            "icon": self.icon,
            "manuscript_name": self.manuscript_name,
            "domain": self.domain,
            "description": self.description,
            "inscribe_action_id": self.inscribe_action_id,
            "inscribe_action_label": self.inscribe_action_label,
            "inscribe_result_text": self.inscribe_result_text,
            "manuscript_marker": self.manuscript_marker,
            "mastery_marker": self.mastery_marker,
            "recite_action_id": self.recite_action_id,
            "recite_action_label": self.recite_action_label,
            "recite_result_text": self.recite_result_text,
            "renew_action_id": self.renew_action_id,
            "renew_action_label": self.renew_action_label,
            "renew_result_text": self.renew_result_text,
            "required_tool": self.required_tool,
            "alternate_attribute": self.alternate_attribute,
            "alternate_attr_val": self.alternate_attr_val,
            "alternate_trait": self.alternate_trait,
        }


CANONICAL_SCRIPTORIUMS: Dict[str, ContinentalScriptorium] = {
    "scribe_glacial_chronicle": ContinentalScriptorium(
        id="scribe_glacial_chronicle",
        name="Glacial Chronicle Desk",
        province="The Reach",
        quarters_scene="reach_high_pass_quarters",
        icon="🏔️",
        manuscript_name="Frostbound Annals of Khoros",
        domain="Highland Clan Treaties & Glacial Defense Treatises",
        description="A heavy oak drafting desk stands upon a granite foundation. Shelves of provincial calfskin parchment await your pen.",
        inscribe_action_id="scribe_inscribe_glacial_chronicle",
        inscribe_action_label="Inscribe Glacial Annals",
        inscribe_result_text="You copy ancient alpine oaths upon calfskin parchment. Mountain resolve steadies your writing hand.",
        manuscript_marker="marker_manuscript_glacial_chronicle",
        mastery_marker="marker_scribe_mastery_reach",
        recite_action_id="scribe_recite_glacial_chronicle",
        recite_action_label="Recite Frost Annals",
        recite_result_text="You read aloud the oath of high pass sentinels. Highland fortitude strengthens your travel stamina.",
        renew_action_id="scribe_renew_glacial_chronicle",
        renew_action_label="Grind Granite Ink",
        renew_result_text="You mix thick spruce resin into black calligraphy ink. Cold mountain composure renews your resolve.",
        required_tool="quill_and_ink",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="scholar",
    ),
    "scribe_sunfire_papyrus": ContinentalScriptorium(
        id="scribe_sunfire_papyrus",
        name="Sunfire Papyrus Scriptorium",
        province="The Scorchwaste",
        quarters_scene="scorchwaste_dune_ridge_quarters",
        icon="☀️",
        manuscript_name="Solar Covenant of the Sands",
        domain="Caravan Oasis Charters & Desert Water Treaties",
        description="Polished cedar tables hold rolls of papyrus paper. Jars of red cinnabar pigment stand arranged neatly.",
        inscribe_action_id="scribe_inscribe_sunfire_papyrus",
        inscribe_action_label="Inscribe Solar Covenant",
        inscribe_result_text="You inscribe dry desert covenants with crimson mineral ink. Harsh sun wisdom guides your careful hand.",
        manuscript_marker="marker_manuscript_sunfire_papyrus",
        mastery_marker="marker_scribe_mastery_scorchwaste",
        recite_action_id="scribe_recite_sunfire_papyrus",
        recite_action_label="Recite Desert Covenant",
        recite_result_text="You read aloud the water compact of the dunes. Desert tenacity bolsters your walking endurance.",
        renew_action_id="scribe_renew_sunfire_papyrus",
        renew_action_label="Grind Ochre Ink",
        renew_result_text="You grind crimson mineral rocks into fine colored dust. Rich pigments renew your travel resolve.",
        required_tool="quill_and_ink",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="navigator",
    ),
    "scribe_abyssal_vellum": ContinentalScriptorium(
        id="scribe_abyssal_vellum",
        name="Abyssal Vellum Scriptorium",
        province="The Sunken Hollows",
        quarters_scene="sunken_hollows_glow_grotto_quarters",
        icon="💧",
        manuscript_name="Tidal Vellum of Thalassa",
        domain="Subterranean Current Logs & Diver Safe Conducts",
        description="A slate drafting desk stands upon a submerged cavern foundation. Shelves of provincial vellum await your pen.",
        inscribe_action_id="scribe_inscribe_abyssal_vellum",
        inscribe_action_label="Inscribe Tidal Vellum",
        inscribe_result_text="You scribe deep water depths on water-resistant vellum rolls. Silent cavern composure steadies your hand.",
        manuscript_marker="marker_manuscript_abyssal_vellum",
        mastery_marker="marker_scribe_mastery_sunken",
        recite_action_id="scribe_recite_abyssal_vellum",
        recite_action_label="Recite Tidal Vellum",
        recite_result_text="You recite quiet verses of underground ocean currents. Cavern peace steadies your breathing rhythm.",
        renew_action_id="scribe_renew_abyssal_vellum",
        renew_action_label="Grind Squid Ink",
        renew_result_text="You mix glowing shell powder into dark squid ink. Bioluminescent pigments renew your travel resolve.",
        required_tool="quill_and_ink",
        alternate_attribute="wits",
        alternate_attr_val=14,
        alternate_trait="scholar",
    ),
    "scribe_palatine_codex": ContinentalScriptorium(
        id="scribe_palatine_codex",
        name="Palatine Imperial Scriptoria",
        province="The High Court",
        quarters_scene="high_court_royal_archive_quarters",
        icon="⚜️",
        manuscript_name="Golden Decree of Veras",
        domain="Imperial Lineage Scrolls & High Chancellor Charters",
        description="Gilded walnut drafting desks stand upon polished stone pedestals. Rolls of provincial imperial gold leaf await your pen.",
        inscribe_action_id="scribe_inscribe_palatine_codex",
        inscribe_action_label="Inscribe Imperial Decree",
        inscribe_result_text="You apply gold leaf letters across royal court scrolls. Imperial decorum elevates your written speech.",
        manuscript_marker="marker_manuscript_palatine_codex",
        mastery_marker="marker_scribe_mastery_high_court",
        recite_action_id="scribe_recite_palatine_codex",
        recite_action_label="Recite Royal Decree",
        recite_result_text="You recite court decrees with polished vocal poise. Noble authority commands your inner focus.",
        renew_action_id="scribe_renew_palatine_codex",
        renew_action_label="Grind Gold Leaf",
        renew_result_text="You polish the delicate tips of fine raven quill pens. Gilded imperial calligraphy renews your marching resolve.",
        required_tool="quill_and_ink",
        alternate_attribute="presence",
        alternate_attr_val=14,
        alternate_trait="noble",
    ),
    "scribe_tidebell_ledger": ContinentalScriptorium(
        id="scribe_tidebell_ledger",
        name="Lowlands Notary Bureau",
        province="The Lowlands",
        quarters_scene="lowlands_brewery_vault_quarters",
        icon="🔔",
        manuscript_name="Canal Guild Mercantile Concordat",
        domain="River Guild Charters & Smuggler Immunity Pacts",
        description="Stout oak desks stand upon stone warehouse pedestals. Heavy merchant ledgers wait beside red sealing wax.",
        inscribe_action_id="scribe_inscribe_tidebell_ledger",
        inscribe_action_label="Inscribe Guild Concordat",
        inscribe_result_text="You draft municipal river charters with lampblack ink. Shrewd merchant prudence guides your written craft.",
        manuscript_marker="marker_manuscript_tidebell_ledger",
        mastery_marker="marker_scribe_mastery_lowlands",
        recite_action_id="scribe_recite_tidebell_ledger",
        recite_action_label="Recite Guild Concordat",
        recite_result_text="You read aloud formal terms of the river concordat. Shrewd merchant discipline sharpens your senses.",
        renew_action_id="scribe_renew_tidebell_ledger",
        renew_action_label="Grind Lampblack Ink",
        renew_result_text="You scrape dried wax residues from brass notary seal dies. Polished mercantile stamps renew your marching resolve.",
        required_tool="quill_and_ink",
        alternate_attribute="cunning",
        alternate_attr_val=14,
        alternate_trait="merchant",
    ),
    "scribe_crossroads_grand": ContinentalScriptorium(
        id="scribe_crossroads_grand",
        name="Grand Sovereign Scriptorium",
        province="Central Crossroads",
        quarters_scene="bazaar_center",
        icon="👑",
        manuscript_name="Continental Concordat of Sovereign Realms",
        domain="Five-Province Peace Treaty & Master Cartographic Deed",
        description="A marble writing rotunda crowns the bazaar library. Five provincial banners hang over calfskin rolls.",
        inscribe_action_id="scribe_inscribe_crossroads_grand",
        inscribe_action_label="Inscribe Sovereign Concordat",
        inscribe_result_text="You write sovereign peace treaties across five borders. Continental accord steadies your hand.",
        manuscript_marker="marker_manuscript_crossroads_grand",
        mastery_marker="marker_scribe_mastery_crossroads",
        recite_action_id="scribe_recite_crossroads_grand",
        recite_action_label="Recite Grand Concordat",
        recite_result_text="You recite the sovereign treaty of the five realms. Continental harmony restores your marching strength.",
        renew_action_id="scribe_renew_crossroads_grand",
        renew_action_label="Grind Mineral Ink",
        renew_result_text="You scrape calfskin parchment with coarse pumice stone. Pristine provincial vellum sheets renew your travel resolve.",
        required_tool="quill_and_ink",
        alternate_attribute="presence",
        alternate_attr_val=14,
        alternate_trait="diplomat",
    ),
}

CALLIGRAPHER_RANKS: List[Dict[str, Any]] = [
    {
        "count": 0,
        "title": "Novice Copyist",
        "desc": "You hold no inscribed treaty scrolls or manuscripts. Continental scriptoriums remain idle in your journey.",
    },
    {
        "count": 1,
        "title": "Apprentice Scribe",
        "desc": "You have inscribed your first provincial treaty scroll. Basic scribal discipline guides your writing hand.",
    },
    {
        "count": 2,
        "title": "Illuminator Craftsman",
        "desc": "Two provincial manuscripts record your deeds. Intricate script sharpens your clear vision.",
    },
    {
        "count": 3,
        "title": "Master Calligrapher",
        "desc": "Three continental scrolls have been drafted with care. Sophisticated legal agreements yield to your quill.",
    },
    {
        "count": 4,
        "title": "Charter Chancellor",
        "desc": "Four provincial charters are inscribed with fine skill. Your illuminated manuscripts earn high renown.",
    },
    {
        "count": 5,
        "title": "High Archivist",
        "desc": "All five provincial charters are completed with skill. Complete historical lore guides your steady hand.",
    },
    {
        "count": 6,
        "title": "Continental Grandmaster Scribe",
        "desc": "All continental manuscripts are inscribed with great care. Supreme scribal craft marks your journey.",
    },
]


def get_calligrapher_rank(inscribed_count: int) -> Dict[str, str]:
    """Determine Calligrapher rank title and description from inscribed manuscript count."""
    best = CALLIGRAPHER_RANKS[0]
    for tier in CALLIGRAPHER_RANKS:
        if inscribed_count >= tier["count"]:
            best = tier
        else:
            break
    return {"title": str(best["title"]), "desc": str(best["desc"])}


def evaluate_scriptorium_progress(
    world_flags: Dict[str, Any],
    inventory: List[str],
    markers: List[str],
) -> Dict[str, Any]:
    """Pure evaluation of scriptorium progress and calligrapher status."""
    inscribed_ids: List[str] = []
    active_manuscript_markers: List[str] = []
    active_masteries: List[str] = []
    recited_ids: List[str] = []

    m_set = {m.lower() for m in markers}

    for s_id, s in CANONICAL_SCRIPTORIUMS.items():
        flag_inscribed = bool(world_flags.get(f"scribe_inscribed_{s_id}", False))
        if flag_inscribed or (s.manuscript_marker.lower() in m_set):
            inscribed_ids.append(s_id)
        if s.manuscript_marker.lower() in m_set:
            active_manuscript_markers.append(s.manuscript_marker)
        if s.mastery_marker.lower() in m_set:
            active_masteries.append(s.mastery_marker)
        if bool(world_flags.get(f"scribe_recited_{s_id}", False)):
            recited_ids.append(s_id)

    inscribed_count = len(inscribed_ids)
    total_scriptoriums = len(CANONICAL_SCRIPTORIUMS)
    progress_pct = round((inscribed_count / total_scriptoriums) * 100.0, 1) if total_scriptoriums > 0 else 0.0

    rank_info = get_calligrapher_rank(inscribed_count)

    scriptorium_status: List[Dict[str, Any]] = []
    for s_id, s in CANONICAL_SCRIPTORIUMS.items():
        is_inscribed = s_id in inscribed_ids
        is_recited = s_id in recited_ids
        has_manuscript = s.manuscript_marker.lower() in m_set
        has_mastery = s.mastery_marker.lower() in m_set

        scriptorium_status.append({
            "id": s_id,
            "name": s.name,
            "province": s.province,
            "quarters_scene": s.quarters_scene,
            "icon": s.icon,
            "manuscript_name": s.manuscript_name,
            "domain": s.domain,
            "description": s.description,
            "is_inscribed": is_inscribed,
            "is_recited": is_recited,
            "has_manuscript": has_manuscript,
            "has_mastery": has_mastery,
            "inscribe_action_id": s.inscribe_action_id,
            "inscribe_action_label": s.inscribe_action_label,
            "recite_action_id": s.recite_action_id,
            "recite_action_label": s.recite_action_label,
            "renew_action_id": s.renew_action_id,
            "renew_action_label": s.renew_action_label,
        })

    return {
        "inscribed_count": inscribed_count,
        "total_scriptoriums": total_scriptoriums,
        "progress_pct": progress_pct,
        "calligrapher_rank": rank_info["title"],
        "calligrapher_desc": rank_info["desc"],
        "inscribed_scriptoriums": inscribed_ids,
        "active_manuscript_count": len(active_manuscript_markers),
        "active_masteries_count": len(active_masteries),
        "recited_scriptoriums": recited_ids,
        "scriptoriums": scriptorium_status,
    }


def get_scriptorium_progress(state: Any) -> Dict[str, Any]:
    """Helper extracting scriptorium progress directly from a GameState object."""
    if not hasattr(state, "world_flags") or not hasattr(state, "character"):
        return evaluate_scriptorium_progress({}, [], [])

    inv = list(getattr(state.character, "inventory", []))
    markers = list(getattr(state.character, "markers", []))
    return evaluate_scriptorium_progress(state.world_flags, inv, markers)


def get_scriptorium_affordances_for_scene(
    scene_id: str,
    character: Any,
    world_flags: Dict[str, Any],
) -> List[Any]:
    """Dynamically synthesize scriptorium affordances for the given scene and character."""
    from adventure_forge.content.schema import Action

    affordances: List[Action] = []
    inv_list = [str(i).lower() for i in getattr(character, "inventory", [])]
    traits_list = [str(t).lower() for t in getattr(character, "traits", [])]
    marker_list = [str(m).lower() for m in getattr(character, "markers", [])]
    skills_dict = getattr(character, "skills", {})

    has_any_calligraphy_tool = any(
        tool in inv_list
        for tool in [
            "quill_and_ink",
            "parchment_roll",
            "inkpot",
            "scribe_quill",
            "wax_seal_stamp",
            "calligraphy_pen",
            "illuminator_brush",
        ]
    )

    # 1. Quarters Scene: Inscribe Manuscript or Renew Ink & Polish Dies
    for s in CANONICAL_SCRIPTORIUMS.values():
        if s.quarters_scene == scene_id:
            flag_inscribed = bool(world_flags.get(f"scribe_inscribed_{s.id}", False))
            is_recited = bool(world_flags.get(f"scribe_recited_{s.id}", False))

            if not flag_inscribed:
                # 7-axis qualification:
                # 1. Has specific tool or generic calligraphy tool
                # 2. Has relevant traits (scholar, scribe, calligrapher, historian, noble, diplomat, merchant, etc.)
                # 3. Has high attribute (wits >= 14, cunning >= 14, presence >= 14, or alternate_attr)
                # 4. Has relevant skills (lore, cunning, diplomacy >= 2)
                # 5. Has physical stamina (stamina >= 2)
                has_tool = (s.required_tool.lower() in inv_list) or has_any_calligraphy_tool
                has_trait = (s.alternate_trait.lower() in traits_list) or any(
                    t in traits_list
                    for t in [
                        "scholar",
                        "scribe",
                        "calligrapher",
                        "historian",
                        "noble",
                        "diplomat",
                        "merchant",
                        "astronomer",
                        "focused",
                        "wise",
                        "cautious",
                    ]
                )
                attr_val = character.get_attribute(s.alternate_attribute)
                has_attr = (attr_val >= s.alternate_attr_val) or (
                    character.get_attribute("wits") >= 14
                    or character.get_attribute("cunning") >= 14
                    or character.get_attribute("presence") >= 14
                )
                has_skill = (
                    skills_dict.get("lore", 0) >= 2
                    or skills_dict.get("cunning", 0) >= 2
                    or skills_dict.get("diplomacy", 0) >= 2
                )
                has_stam = getattr(character, "stamina", 0) >= 2

                if has_tool or has_trait or has_attr or has_skill or has_stam:
                    affordances.append(
                        Action(
                            id=s.inscribe_action_id,
                            label=s.inscribe_action_label,
                            category="exploration",
                            effects=[
                                {"set_flag": {"flag": f"scribe_inscribed_{s.id}", "value": True}},
                                {"add_marker": s.manuscript_marker},
                                {"add_marker": s.mastery_marker},
                                {"modify_stamina": 3},
                                {"log_event": s.inscribe_result_text},
                            ],
                            result_text=s.inscribe_result_text,
                            risk="low",
                            stamina_cost=0,
                        )
                    )
            elif is_recited:
                # Can renew ink and clean wax seal stamps at quarters scene
                affordances.append(
                    Action(
                        id=s.renew_action_id,
                        label=s.renew_action_label,
                        category="exploration",
                        effects=[
                            {"set_flag": {"flag": f"scribe_recited_{s.id}", "value": False}},
                            {"modify_stamina": 2},
                            {"log_event": s.renew_result_text},
                        ],
                        result_text=s.renew_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    # 2. Field Recitation anywhere across the continental world
    for s in CANONICAL_SCRIPTORIUMS.values():
        if s.manuscript_marker.lower() in marker_list:
            is_recited = bool(world_flags.get(f"scribe_recited_{s.id}", False))
            if not is_recited:
                affordances.append(
                    Action(
                        id=s.recite_action_id,
                        label=s.recite_action_label,
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": f"scribe_recited_{s.id}", "value": True}},
                            {"add_marker": f"marker_recited_{s.id}"},
                            {"modify_stamina": 3},
                            {"log_event": s.recite_result_text},
                        ],
                        result_text=s.recite_result_text,
                        risk="low",
                        stamina_cost=0,
                    )
                )

    return affordances
