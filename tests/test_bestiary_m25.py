"""Milestone 25 Verification: Continental Bestiary & Apex Trophy Hunting System.

Tests cover:
1. 10 Continental Apex Beasts integrity across 5 provinces and Hemingway prose compliance.
2. Dynamic study affordances, weakness revelation, and stamina discount.
3. Apex hunting encounters, defeat resolution, and trophy item acquisition.
4. Menagerie trophy mounting affordances and inspection at Central Bazaar.
5. Hunter rank progression and defensive handling of inventory types.
6. Bit-for-bit deterministic replay with apex hunt actions.
7. ASGI serverless endpoint GET/HEAD at /api/game/bestiary.
"""
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.bestiary import (
    APEX_BEASTS,
    evaluate_bestiary_progress,
)
from adventure_forge.core.character import get_preset
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import (
    ProseLinter,
    FORBIDDEN_PURPLE_WORDS,
    split_sentences,
    word_count,
)
from app import app


@pytest.fixture
def engine() -> AdventureEngine:
    reg = build_world_registry()
    return AdventureEngine(reg)


@pytest.fixture
def base_state() -> GameState:
    preset = get_preset("warrior")
    return GameState(
        build_id="af-m25-test",
        session_id="test-session-bestiary",
        character=preset.character,
        current_region=preset.start_region,
        current_scene=preset.start_scene,
        rng=DeterministicRNG.from_seed(42),
    )


def test_bestiary_registry_integrity_and_prose(engine: AdventureEngine) -> None:
    """Validate 10 apex beasts, valid scene lairs, and 100% Hemingway prose compliance."""
    assert len(APEX_BEASTS) == 10
    provinces = {b.province for b in APEX_BEASTS.values()}
    assert len(provinces) == 5
    for prov in ["The Reach", "The Scorchwaste", "The Lowlands", "The High Court", "The Sunken Hollows"]:
        prov_beasts = [b for b in APEX_BEASTS.values() if b.province == prov]
        assert len(prov_beasts) == 2, f"Province {prov} must have exactly 2 apex beasts"

    linter = ProseLinter()

    for bid, beast in APEX_BEASTS.items():
        # Lair scene must exist in world graph
        scene = engine.get_scene(beast.lair_scene)
        assert scene is not None, f"Lair scene {beast.lair_scene} for {bid} missing from world graph"

        # Action labels must be 1-3 words
        for lbl in [beast.study_action_label, beast.hunt_action_label, f"Mount {beast.short_trophy_name}"]:
            wc = len(lbl.split())
            assert 1 <= wc <= 3, f"Label '{lbl}' exceeds 3 words ({wc} words)"

        # Prose check: description, weakness, study_text, hunt_text, trophy_perk
        for field_name, text in [
            ("description", beast.description),
            ("weakness", beast.weakness),
            ("study_result_text", beast.study_result_text),
            ("hunt_result_text", beast.hunt_result_text),
            ("trophy_perk", beast.trophy_perk),
        ]:
            errs = linter.lint_text(text, f"{bid} {field_name}")
            assert not errs, f"Prose errors in {bid} {field_name}: {errs}"

            # Word count <= 18 words per sentence
            sents = split_sentences(text)
            assert 1 <= len(sents) <= 3
            for s in sents:
                assert word_count(s) <= 18, f"Sentence '{s}' exceeds 18 words"

            # No purple words
            for pw in FORBIDDEN_PURPLE_WORDS:
                assert pw not in text.lower(), f"Forbidden purple word '{pw}' found in {bid} {field_name}"


def test_bestiary_study_affordance_and_weakness_discovery(engine: AdventureEngine, base_state: GameState) -> None:
    """Test anatomical study in lair scene, weakness discovery, and hunt stamina discount."""
    beast = APEX_BEASTS["frost_claw_manticore"]
    state = base_state.evolve(current_scene=beast.lair_scene, current_region="reach")

    legal = engine.get_legal_actions(state)
    action_ids = [a.id for a in legal]
    assert beast.study_action_id in action_ids
    assert beast.hunt_action_id in action_ids

    # Unstudied hunt cost is 8 stamina
    hunt_act_unstudied = next(a for a in legal if a.id == beast.hunt_action_id)
    assert hunt_act_unstudied.stamina_cost == beast.hunt_stamina_cost

    # Execute study action
    initial_stamina = state.character.stamina
    next_state, obs = engine.step(state, beast.study_action_id)
    assert obs.success
    assert next_state.world_flags.get(f"bestiary_studied_{beast.id}") is True
    assert next_state.character.stamina == initial_stamina - 1
    assert any("weakness" in ev.lower() for ev in obs.events)

    # After study, study action disappears and hunt stamina is discounted
    next_legal = engine.get_legal_actions(next_state)
    next_action_ids = [a.id for a in next_legal]
    assert beast.study_action_id not in next_action_ids
    assert beast.hunt_action_id in next_action_ids

    hunt_act_studied = next(a for a in next_legal if a.id == beast.hunt_action_id)
    assert hunt_act_studied.stamina_cost == beast.studied_stamina_cost


def test_bestiary_hunt_affordance_and_trophy_harvesting(engine: AdventureEngine, base_state: GameState) -> None:
    """Test apex hunting encounter victory, trophy acquisition, and lair exhaustion."""
    beast = APEX_BEASTS["dune_sand_leviathan"]
    # Study the beast first
    flags = dict(base_state.world_flags)
    flags[f"bestiary_studied_{beast.id}"] = True
    state = base_state.evolve(current_scene=beast.lair_scene, current_region="scorchwaste", world_flags=flags)

    legal = engine.get_legal_actions(state)
    assert beast.hunt_action_id in [a.id for a in legal]

    next_state, obs = engine.step(state, beast.hunt_action_id)
    assert obs.success
    assert next_state.world_flags.get(f"bestiary_hunted_{beast.id}") is True
    assert beast.trophy_id in next_state.character.inventory
    assert any("defeated" in ev.lower() for ev in obs.events)

    # In lair after defeat, neither study nor hunt are legal
    post_defeat_legal = engine.get_legal_actions(next_state)
    post_defeat_ids = [a.id for a in post_defeat_legal]
    assert beast.study_action_id not in post_defeat_ids
    assert beast.hunt_action_id not in post_defeat_ids


def test_bestiary_mounting_at_bazaar_menagerie(engine: AdventureEngine, base_state: GameState) -> None:
    """Test trophy mounting at Central Bazaar Menagerie and trophy removal from bag."""
    beast = APEX_BEASTS["mire_maw_behemoth"]
    # Give protagonist the trophy
    char = base_state.character.modify(inventory=list(base_state.character.inventory) + [beast.trophy_id])
    flags = dict(base_state.world_flags)
    flags[f"bestiary_hunted_{beast.id}"] = True
    state = base_state.evolve(current_scene="bazaar_center", current_region="stress_market", character=char, world_flags=flags)

    legal = engine.get_legal_actions(state)
    mount_act_id = f"bestiary_mount_{beast.id}"
    assert mount_act_id in [a.id for a in legal]
    assert "bestiary_inspect_menagerie" in [a.id for a in legal]

    # Mount trophy
    next_state, obs = engine.step(state, mount_act_id)
    assert obs.success
    assert next_state.world_flags.get(f"bestiary_mounted_{beast.id}") is True
    assert beast.trophy_id not in next_state.character.inventory

    # Inspect menagerie
    inspect_state, inspect_obs = engine.step(next_state, "bestiary_inspect_menagerie")
    assert inspect_obs.success
    assert any("menagerie" in ev.lower() for ev in inspect_obs.events)


def test_bestiary_hunter_rank_progression() -> None:
    """Test Hunter Rank calculations across milestones and defensive inventory handling."""
    # 0 hunted
    p0 = evaluate_bestiary_progress({}, inventory=[])
    assert p0["hunted_count"] == 0
    assert p0["rank_title"] == "Novice Trapper"
    assert p0["is_tracker"] is False

    # 1 hunted
    f1 = {"bestiary_hunted_frost_claw_manticore": True}
    p1 = evaluate_bestiary_progress(f1, inventory=["trophy_frost_claw_talon"])
    assert p1["hunted_count"] == 1
    assert p1["rank_title"] == "🎯 Provincial Tracker"
    assert p1["is_tracker"] is True
    assert p1["beasts"]["frost_claw_manticore"]["has_trophy"] is True

    # 3 hunted
    f3 = {
        "bestiary_hunted_frost_claw_manticore": True,
        "bestiary_hunted_iron_crag_wyrm": True,
        "bestiary_hunted_dune_sand_leviathan": True,
    }
    p3 = evaluate_bestiary_progress(f3, inventory={"trophy_crag_wyrm_scale": 1})
    assert p3["hunted_count"] == 3
    assert p3["rank_title"] == "🏹 Apex Hunter"
    assert p3["is_apex_hunter"] is True
    assert p3["beasts"]["iron_crag_wyrm"]["has_trophy"] is True

    # 5 hunted
    f5 = dict(f3)
    f5["bestiary_hunted_ashen_glass_stalker"] = True
    f5["bestiary_hunted_mire_maw_behemoth"] = True
    p5 = evaluate_bestiary_progress(f5, inventory=None)
    assert p5["hunted_count"] == 5
    assert p5["rank_title"] == "⚔️ Grandmaster Hunter"
    assert p5["is_grandmaster"] is True

    # 10 hunted (All)
    f10 = {f"bestiary_hunted_{b}": True for b in APEX_BEASTS}
    p10 = evaluate_bestiary_progress(f10, inventory=("trophy_manticore_talon",))
    assert p10["hunted_count"] == 10
    assert p10["rank_title"] == "👑 Continental Apex Slayer"
    assert p10["is_slayer"] is True


def test_bestiary_deterministic_replay(engine: AdventureEngine) -> None:
    """Test bit-for-bit replay determinism across bestiary encounters."""
    preset = get_preset("warrior")

    def run_trace(seed: int) -> str:
        s = GameState(
            build_id="af-m25-replay",
            session_id="replay-test",
            character=preset.character,
            current_region="reach",
            current_scene="reach_wind_hollow_sanctum",
            rng=DeterministicRNG.from_seed(seed),
        )
        # 1. Study beast
        s, _ = engine.step(s, "bestiary_study_frost_claw")
        # 2. Hunt beast
        s, _ = engine.step(s, "bestiary_hunt_frost_claw")
        return s.fingerprint()

    fp1 = run_trace(42)
    fp2 = run_trace(42)
    assert fp1 == fp2, "Bit-for-bit SHA-256 fingerprint match required across deterministic runs"


def test_bestiary_asgi_endpoint() -> None:
    """Test ASGI serverless endpoint GET /api/game/bestiary, HEAD, and /api/game/new inclusion."""
    import asyncio
    import json

    async def run_asgi(path: str, method: str = "GET", body: bytes = b""):
        response_data = {"status": 0, "headers": [], "body": b""}

        async def receive():
            return {"type": "http.request", "body": body}

        async def send(message):
            if message["type"] == "http.response.start":
                response_data["status"] = message["status"]
                response_data["headers"] = message.get("headers", [])
            elif message["type"] == "http.response.body":
                response_data["body"] += message.get("body", b"")

        scope = {
            "type": "http",
            "method": method,
            "path": path,
            "headers": [(b"host", b"localhost")],
        }
        await app(scope, receive, send)
        return response_data

    # 1. GET /api/game/bestiary
    res_get = asyncio.run(run_asgi("/api/game/bestiary", "GET"))
    assert res_get["status"] == 200
    assert any(k == b"content-type" and b"application/json" in v for k, v in res_get["headers"])
    body = json.loads(res_get["body"].decode("utf-8"))
    assert body["total_beasts"] == 10
    assert len(body["beasts"]) == 10

    # 2. HEAD /api/game/bestiary
    res_head = asyncio.run(run_asgi("/api/game/bestiary", "HEAD"))
    assert res_head["status"] == 200
    assert res_head["body"] == b""

    # 3. POST /api/game/new includes bestiary progress
    new_req_body = json.dumps({"preset": "warrior", "seed": 42}).encode("utf-8")
    res_new = asyncio.run(run_asgi("/api/game/new", "POST", new_req_body))
    assert res_new["status"] == 200
    new_data = json.loads(res_new["body"].decode("utf-8"))
    assert "bestiary" in new_data
    assert new_data["bestiary"]["total_beasts"] == 10
    assert new_data["bestiary"]["hunted_count"] == 0
    assert new_data["bestiary"]["rank_title"] == "Novice Trapper"
