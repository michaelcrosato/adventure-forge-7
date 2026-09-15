"""Tests for Milestone 30: Continental Dungeon Vaults, Arcane Keystones & Ancient Crypt Raids System."""
import asyncio
import json
from typing import Dict, Any

from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.vaults import (
    ANCIENT_VAULTS,
    DELVER_RANKS,
    get_delver_rank,
    evaluate_vaults_progress,
    get_vault_affordances_for_scene,
)
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import ProseLinter, flesch_kincaid_grade, word_count
from app import app


def test_vaults_registry_integrity():
    """Verify all 6 canonical vaults exist, link to real crypt scenes, and have valid fields."""
    assert len(ANCIENT_VAULTS) == 6
    registry = build_world_registry()
    all_scenes = set()
    for reg in registry.values():
        all_scenes.update(reg.scenes.keys())

    for v_id, v in ANCIENT_VAULTS.items():
        assert v.id == v_id
        assert v.vault_scene in all_scenes, f"Vault scene {v.vault_scene} not found in world registry!"
        assert v.name
        assert v.province in [
            "The Reach",
            "The Scorchwaste",
            "The Sunken Hollows",
            "The High Court",
            "The Lowlands",
            "Central Crossroads",
        ]
        assert v.icon
        assert v.domain
        assert v.breach_action_id.startswith("vault_breach_")
        assert v.attune_action_id.startswith("vault_attune_")
        assert v.realign_action_id.startswith("vault_realign_")
        assert v.keystone_marker.startswith("marker_keystone_")
        assert v.mastery_marker.startswith("marker_delve_mastery_")


def test_vaults_hemingway_compliance():
    """Verify all vault descriptions, result texts, and rank descriptions satisfy Hemingway prose."""
    linter = ProseLinter(min_readability_grade=6.0, max_readability_grade=8.0)

    for v_id, v in ANCIENT_VAULTS.items():
        # Action labels <= 3 words
        for label, lbl_name in [
            (v.breach_action_label, f"{v_id}_breach_label"),
            (v.attune_action_label, f"{v_id}_attune_label"),
            (v.realign_action_label, f"{v_id}_realign_label"),
        ]:
            wc = word_count(label)
            assert 1 <= wc <= 3, f"Label {lbl_name} '{label}' has {wc} words (must be 1-3)"

        # Text bodies: FKGL in [6.0, 8.0], <= 18 words/sent, 1-3 sentences, 0 purple words
        for text, context in [
            (v.description, f"{v_id}_desc"),
            (v.breach_result_text, f"{v_id}_breach_result"),
            (v.attune_result_text, f"{v_id}_attune_result"),
            (v.realign_result_text, f"{v_id}_realign_result"),
        ]:
            errs = linter.lint_text(text, context=context, check_readability=True)
            grade = flesch_kincaid_grade(text)
            assert not errs, f"Hemingway lint errors in {context}: {errs} (grade={grade})"
            assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in {context}"

    # Rank descriptions
    for tier in DELVER_RANKS:
        errs = linter.lint_text(tier["desc"], context=f"rank_{tier['count']}", check_readability=True)
        grade = flesch_kincaid_grade(tier["desc"])
        assert not errs, f"Hemingway lint errors in rank {tier['count']}: {errs} (grade={grade})"
        assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in rank {tier['count']}"


def test_vault_breach_execution():
    """Verify breaching an ancient vault sets flags, awards keystones and delve mastery, and logs events."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="TombDelver",
        ancestry="Human",
        background="Infiltrator",
        attributes={"strength": 12, "wits": 14, "endurance": 12},
        skills={"cunning": 3, "lore": 2},
        traits=["dungeon_diver"],
        stamina=5,
        max_stamina=10,
        inventory=["item_lockpicks"],
    )

    state = GameState(
        build_id="af-build-001",
        session_id="vault-session",
        character=char,
        current_region="province_reach",
        current_scene="reach_frost_cavern_vault",
    )

    legal_acts = [a.id for a in engine.get_legal_actions(state)]
    assert "vault_breach_frost_titan" in legal_acts

    # Execute breach
    new_state, obs = engine.step(state, "vault_breach_frost_titan")
    assert obs.success
    assert new_state.world_flags.get("vault_unlocked_vault_frost_titan") is True
    assert "marker_keystone_frost_titan" in new_state.character.markers
    assert "marker_delve_mastery_reach" in new_state.character.markers
    assert new_state.character.stamina == 8  # 5 + 3

    # Check engine progress helper
    prog = engine.get_vaults_progress(new_state)
    assert prog["breached_count"] == 1
    assert prog["delver_rank"] == "Crypt Breacher"
    assert prog["active_keystones_count"] == 1
    assert prog["active_masteries_count"] == 1


def test_7axis_vault_reactivity():
    """Verify 7-axis qualification (tools, traits, attributes, skills, stamina) for vault breach."""
    v = ANCIENT_VAULTS["vault_sol_serpent"]

    # 1. Qualified via lockpick tool item
    char_item = CharacterSheet(
        name="ItemDelver", ancestry="Human", background="Scout", inventory=["lockpick_set"], stamina=0
    )
    aff_item = get_vault_affordances_for_scene(v.vault_scene, char_item, {})
    assert any(a.id == v.breach_action_id for a in aff_item)

    # 2. Qualified via locksmith trait
    char_trait = CharacterSheet(
        name="TraitDelver", ancestry="Human", background="Scout", traits=["locksmith"], stamina=0
    )
    aff_trait = get_vault_affordances_for_scene(v.vault_scene, char_trait, {})
    assert any(a.id == v.breach_action_id for a in aff_trait)

    # 3. Qualified via high wits attribute
    char_attr = CharacterSheet(
        name="AttrDelver", ancestry="Human", background="Scout", attributes={"wits": 14}, stamina=0
    )
    aff_attr = get_vault_affordances_for_scene(v.vault_scene, char_attr, {})
    assert any(a.id == v.breach_action_id for a in aff_attr)

    # 4. Qualified via cunning skill
    char_skill = CharacterSheet(
        name="SkillDelver", ancestry="Human", background="Scout", skills={"cunning": 2}, stamina=0
    )
    aff_skill = get_vault_affordances_for_scene(v.vault_scene, char_skill, {})
    assert any(a.id == v.breach_action_id for a in aff_skill)

    # 5. Qualified via physical stamina
    char_stam = CharacterSheet(name="StamDelver", ancestry="Human", background="Scout", stamina=2)
    aff_stam = get_vault_affordances_for_scene(v.vault_scene, char_stam, {})
    assert any(a.id == v.breach_action_id for a in aff_stam)

    # 6. Unqualified character with 0 stamina, no tools, low stats
    char_none = CharacterSheet(
        name="Unqualified", ancestry="Human", background="Scout", stamina=0, attributes={"wits": 10}, skills={"cunning": 0}
    )
    aff_none = get_vault_affordances_for_scene(v.vault_scene, char_none, {})
    assert not any(a.id == v.breach_action_id for a in aff_none)


def test_field_keystone_attunement_and_realign():
    """Verify attuning a keystone in the field and realigning at the vault crypt."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="FieldDelver",
        ancestry="Human",
        background="Infiltrator",
        markers=["marker_keystone_frost_titan"],
        stamina=5,
    )

    # 1. In the field (e.g. at bazaar_center or another scene)
    field_state = GameState(
        build_id="af-build-001",
        session_id="field-attune-session",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
        world_flags={"vault_unlocked_vault_frost_titan": True},
    )

    legal_acts = [a.id for a in engine.get_legal_actions(field_state)]
    assert "vault_attune_frost_titan" in legal_acts

    # Execute attunement in field
    attuned_state, obs = engine.step(field_state, "vault_attune_frost_titan")
    assert obs.success
    assert attuned_state.world_flags.get("vault_attuned_vault_frost_titan") is True
    assert "marker_attuned_vault_frost_titan" in attuned_state.character.markers
    assert attuned_state.character.stamina == 8  # 5 + 3

    # Now attunement is no longer available in field
    subsequent_acts = [a.id for a in engine.get_legal_actions(attuned_state)]
    assert "vault_attune_frost_titan" not in subsequent_acts

    # 2. Return to reach_frost_cavern_vault and realign reliquary
    vault_state = attuned_state.evolve(
        current_region="province_reach",
        current_scene="reach_frost_cavern_vault",
    )
    vault_acts = [a.id for a in engine.get_legal_actions(vault_state)]
    assert "vault_realign_frost_titan" in vault_acts

    # Step realignment
    renewed_state, renew_obs = engine.step(vault_state, "vault_realign_frost_titan")
    assert renew_obs.success
    assert renewed_state.world_flags.get("vault_attuned_vault_frost_titan") is False
    assert renewed_state.character.stamina == 10  # 8 + 2


def test_delver_rank_progression():
    """Verify progressive unlock of delver ranks across 0 to 6 vaults."""
    assert get_delver_rank(0)["title"] == "Unproven Delver"
    assert get_delver_rank(1)["title"] == "Crypt Breacher"
    assert get_delver_rank(2)["title"] == "Tomb Raider"
    assert get_delver_rank(3)["title"] == "Vault Specialist"
    assert get_delver_rank(4)["title"] == "Master Infiltrator"
    assert get_delver_rank(5)["title"] == "Lord of Five Vaults"
    assert get_delver_rank(6)["title"] == "Grandmaster of Crypts"

    flags: Dict[str, Any] = {}
    markers = []
    for idx, v in enumerate(ANCIENT_VAULTS.values(), start=1):
        flags[f"vault_breached_{v.id}"] = True
        markers.append(v.keystone_marker)
        prog = evaluate_vaults_progress(flags, [], markers)
        assert prog["breached_count"] == idx
        assert prog["active_keystones_count"] == idx

    final_prog = evaluate_vaults_progress(flags, [], markers)
    assert final_prog["delver_rank"] == "Grandmaster of Crypts"
    assert final_prog["progress_pct"] == 100.0


def test_vaults_replay_determinism():
    """Verify bit-for-bit replay determinism across breach and keystone transitions."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    def run_trajectory():
        char = CharacterSheet(
            name="DeterministicDelver",
            ancestry="Human",
            background="Infiltrator",
            traits=["locksmith"],
            stamina=10,
            inventory=["item_lockpicks"],
        )
        s = GameState(
            build_id="af-build-001",
            session_id="det-vault-session",
            character=char,
            current_region="province_reach",
            current_scene="reach_frost_cavern_vault",
        )
        s, _ = engine.step(s, "vault_breach_frost_titan")
        s, _ = engine.step(s, "vault_attune_frost_titan")
        s, _ = engine.step(s, "vault_realign_frost_titan")
        return s.fingerprint()

    fp1 = run_trajectory()
    fp2 = run_trajectory()
    assert fp1 == fp2, "Replay execution produced diverging state fingerprints!"


def test_asgi_vaults_endpoint():
    """Verify GET and HEAD /api/game/vaults endpoint returns correct metadata."""
    async def run_asgi(path: str, method: str = "GET"):
        scope = {
            "type": "http",
            "method": method,
            "path": path,
            "query_string": b"",
            "headers": [],
        }
        messages = []

        async def receive():
            return {"type": "http.request", "body": b""}

        async def send(message):
            messages.append(message)

        await app(scope, receive, send)

        status = 0
        headers = {}
        body = b""
        for msg in messages:
            if msg["type"] == "http.response.start":
                status = msg["status"]
                headers = dict(msg.get("headers", []))
            elif msg["type"] == "http.response.body":
                body += msg.get("body", b"")
        return status, headers, body

    # 1. GET /api/game/vaults
    status, headers, body = asyncio.run(run_asgi("/api/game/vaults", "GET"))
    assert status == 200
    assert b"application/json" in headers.get(b"content-type", b"")
    data = json.loads(body.decode("utf-8"))
    assert data["total_vaults"] == 6
    assert len(data["vaults"]) == 6

    # 2. HEAD /api/game/vaults
    h_status, h_headers, h_body = asyncio.run(run_asgi("/api/game/vaults", "HEAD"))
    assert h_status == 200
    assert len(h_body) == 0
