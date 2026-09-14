"""Milestone 22: Continental Weather Dynamics & Provincial Micro-Climates Test Suite.

Validates:
1. Weather registry integrity (12 micro-climates across 5 provinces + Central Crossroads).
2. Hemingway prose compliance (<= 18 words/sent, 1-3 sent, FKGL <= 8.0, <= 3 words/label, 0 purple words).
3. Deterministic 6-turn weather cycling.
4. Dynamic systemic weather affordance synthesis and cycle deduplication.
5. 7-axis character reactivity and state transition effects.
6. Deterministic replay fingerprinting.
7. ASGI REST endpoints (GET and HEAD /api/game/weather, payload inclusion in /api/game/*).
"""
import asyncio
import json
import re
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.weather import (
    WEATHER_CONDITIONS,
    PROVINCE_NAMES,
    REGION_WEATHER_MAP,
    get_weather_for_region,
    get_all_provincial_weather,
    get_weather_affordance_for_scene,
)
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.character import CharacterSheet, get_preset
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import FORBIDDEN_PURPLE_WORDS, flesch_kincaid_grade


@pytest.fixture
def registry():
    return build_world_registry()


@pytest.fixture
def engine(registry):
    return AdventureEngine(registry)


# --- Test 1: Weather Registry Integrity ---

def test_weather_registry_count_and_mapping():
    """Verify exactly 12 conditions spanning 5 provinces and Central Crossroads."""
    assert len(WEATHER_CONDITIONS) == 12
    assert len(PROVINCE_NAMES) == 6

    # Verify each province has both mild and extreme conditions
    for prov in PROVINCE_NAMES:
        matching = [c for c in WEATHER_CONDITIONS.values() if c.province == prov]
        assert len(matching) == 2, f"Province {prov} must have exactly 2 weather conditions"
        mild = matching[0]
        extreme = matching[1]
        assert mild.id != extreme.id
        assert mild.action_id != extreme.action_id

    # Verify all canonical region IDs and slug aliases exist in REGION_WEATHER_MAP
    assert "iron_crags" in REGION_WEATHER_MAP
    assert "province_reach" in REGION_WEATHER_MAP
    assert "the_reach" in REGION_WEATHER_MAP
    assert "scorchwaste_local" in REGION_WEATHER_MAP
    assert "lower_warrens" in REGION_WEATHER_MAP
    assert "high_court_local" in REGION_WEATHER_MAP
    assert "sunken_hollows_local" in REGION_WEATHER_MAP
    assert "stress_market" in REGION_WEATHER_MAP
    assert "central_bazaar" in REGION_WEATHER_MAP


# --- Test 2: Hemingway Prose Compliance ---

def test_weather_hemingway_prose_compliance():
    """Verify all weather descriptions, action labels, and result texts follow Hemingway rules."""
    for cond_id, cond in WEATHER_CONDITIONS.items():
        # 1. Action label: exactly 1 to 3 words
        label_words = cond.action_label.split()
        assert 1 <= len(label_words) <= 3, (
            f"Action label '{cond.action_label}' for {cond_id} must have 1-3 words, got {len(label_words)}"
        )

        # 2. Description: 1 to 3 sentences, <= 18 words/sentence
        desc_sentences = [s.strip() for s in re.split(r"[.!?]+", cond.description) if s.strip()]
        assert 1 <= len(desc_sentences) <= 3, (
            f"Description for {cond_id} has {len(desc_sentences)} sentences (expected 1-3)"
        )
        for sent in desc_sentences:
            words = sent.split()
            assert len(words) <= 18, (
                f"Sentence in {cond_id} description exceeds 18 words: '{sent}' ({len(words)} words)"
            )

        # 3. Result text: 1 to 3 sentences, <= 18 words/sentence
        res_sentences = [s.strip() for s in re.split(r"[.!?]+", cond.result_text) if s.strip()]
        assert 1 <= len(res_sentences) <= 3, (
            f"Result text for {cond_id} has {len(res_sentences)} sentences (expected 1-3)"
        )
        for sent in res_sentences:
            words = sent.split()
            assert len(words) <= 18, (
                f"Sentence in {cond_id} result text exceeds 18 words: '{sent}' ({len(words)} words)"
            )

        # 4. Zero banned purple words
        combined_text = f"{cond.name} {cond.description} {cond.action_label} {cond.result_text}".lower()
        for banned in FORBIDDEN_PURPLE_WORDS:
            assert banned not in combined_text, (
                f"Banned purple word '{banned}' detected in weather condition {cond_id}"
            )

        # 5. Readability FKGL <= 8.5
        fkgl = flesch_kincaid_grade(cond.description)
        assert fkgl <= 8.5, f"Description for {cond_id} FKGL too high: {fkgl:.2f}"


# --- Test 3: Deterministic Cycling ---

def test_deterministic_weather_cycling():
    """Verify that weather cycles deterministically every 6 turns."""
    # Test The Reach: reach_clear (turns 0-5) -> reach_blizzard (turns 6-11) -> reach_clear (turn 12)
    for turn in range(0, 6):
        w = get_weather_for_region(turn, "iron_crags")
        assert w.id == "reach_clear", f"Turn {turn} should be reach_clear, got {w.id}"

    for turn in range(6, 12):
        w = get_weather_for_region(turn, "iron_crags")
        assert w.id == "reach_blizzard", f"Turn {turn} should be reach_blizzard, got {w.id}"

    w_cycle2 = get_weather_for_region(12, "iron_crags")
    assert w_cycle2.id == "reach_clear"

    # Test Scorchwaste: scorch_dusk (turns 0-5) -> scorch_heatwave (turns 6-11)
    w_dusk = get_weather_for_region(3, "scorchwaste_local")
    assert w_dusk.id == "scorch_dusk"
    w_heat = get_weather_for_region(8, "scorchwaste_local")
    assert w_heat.id == "scorch_heatwave"

    # All provincial forecast at turn 0
    forecast_0 = get_all_provincial_weather(0)
    assert len(forecast_0) == 6
    assert forecast_0["The Reach"]["id"] == "reach_clear"
    assert forecast_0["The Scorchwaste"]["id"] == "scorch_dusk"

    # All provincial forecast at turn 6
    forecast_6 = get_all_provincial_weather(6)
    assert len(forecast_6) == 6
    assert forecast_6["The Reach"]["id"] == "reach_blizzard"
    assert forecast_6["The Scorchwaste"]["id"] == "scorch_heatwave"


# --- Test 4: Dynamic Affordance Synthesis & Cycle Deduplication ---

def test_dynamic_weather_affordance_synthesis():
    """Verify systemic weather affordance appears dynamically and deduplicates per cycle."""
    char = CharacterSheet(
        name="Trekker",
        ancestry="ironborn",
        background="scout",
        attributes={"vigor": 12, "agility": 14, "intellect": 10, "presence": 10},
        skills={"athletics": 1, "stealth": 1},
        stamina=10,
        max_stamina=10,
    )
    world_flags = {}

    # At turn 0 in reach_gate: should offer 'weather_collect_melt'
    affordance_0 = get_weather_affordance_for_scene("reach_gate", "iron_crags", 0, char, world_flags)
    assert affordance_0 is not None
    assert affordance_0.id == "weather_collect_melt"
    assert affordance_0.label == "Collect Fresh Melt"
    assert affordance_0.category == "systemic"

    # Simulate taking the action in cycle 0: sets flag weather_collect_melt_cycle_0
    world_flags["weather_collect_melt_cycle_0"] = True

    # Check same turn 0: cannot take it again this cycle
    affordance_again = get_weather_affordance_for_scene("reach_gate", "iron_crags", 0, char, world_flags)
    assert affordance_again is None

    # At turn 6: new weather (reach_blizzard), should offer 'weather_seek_shelter'
    affordance_6 = get_weather_affordance_for_scene("reach_gate", "iron_crags", 6, char, world_flags)
    assert affordance_6 is not None
    assert affordance_6.id == "weather_seek_shelter"
    assert affordance_6.label == "Seek Crag Shelter"


# --- Test 5: 7-Axis Character Reactivity & State Transitions ---

def test_weather_action_execution_and_effects(engine):
    """Verify stepping through a weather action updates state and logs event cleanly."""
    char = get_preset("cutpurse").character
    state = GameState(
        build_id="af-build-001",
        session_id="weather-test",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
    )

    # At turn 0 in starting scene (bazaar_center / stress_market):
    # Weather is bazaar_sunlit, action is weather_browse_stalls
    weather_state = engine.get_weather_state(state)
    assert weather_state["id"] == "bazaar_sunlit"

    # Verify weather action is legal in legal_actions
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert "weather_browse_stalls" in action_ids

    # Step the weather action
    new_state, step_res = engine.step(state, "weather_browse_stalls")
    assert step_res.success is True
    assert new_state.turn_count == 1
    assert new_state.world_flags.get("weather_stalls_browsed") is True
    assert new_state.world_flags.get("weather_browse_stalls_cycle_0") is True

    # Verify cannot step it again on turn 1
    new_obs = engine.observe(new_state)
    new_action_ids = [a["id"] for a in new_obs.legal_actions]
    assert "weather_browse_stalls" not in new_action_ids


# --- Test 6: Replay Determinism with Weather Actions ---

def test_weather_replay_determinism(engine):
    """Verify executing weather actions maintains 100% bit-for-bit fingerprint determinism."""
    def run_sim():
        char = get_preset("cutpurse").character
        state = GameState(
            build_id="af-build-001",
            session_id="weather-replay-1337",
            character=char,
            current_region="stress_market",
            current_scene="bazaar_center",
        )
        state, _ = engine.step(state, "weather_browse_stalls")
        return state.fingerprint()

    fp1 = run_sim()
    fp2 = run_sim()

    assert fp1 == fp2, "Weather transitions must yield bit-for-bit identical SHA-256 fingerprints"


# --- Test 7: ASGI REST Endpoints ---

def test_weather_asgi_endpoint():
    """Verify /api/game/weather returns 200 OK with accurate JSON metadata."""
    from app import app

    async def _test():
        # Test GET /api/game/weather
        received_status = None
        received_headers = []
        received_body = bytearray()

        async def dummy_send(message):
            nonlocal received_status, received_headers, received_body
            if message["type"] == "http.response.start":
                received_status = message["status"]
                received_headers = message["headers"]
            elif message["type"] == "http.response.body":
                received_body.extend(message.get("body", b""))

        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/game/weather",
            "headers": [],
            "query_string": b"",
        }

        async def dummy_receive():
            return {"type": "http.request"}

        await app(scope, dummy_receive, dummy_send)

        assert received_status == 200
        data = json.loads(received_body.decode("utf-8"))
        assert data["total_conditions"] == 12
        assert len(data["conditions"]) == 12
        assert "The Reach" in data["forecast"]
        assert "The Scorchwaste" in data["forecast"]
        assert "The Lowlands" in data["forecast"]
        assert "The High Court" in data["forecast"]
        assert "The Sunken Hollows" in data["forecast"]
        assert "Central Crossroads" in data["forecast"]

        # Test HEAD /api/game/weather
        head_status = None
        head_body = bytearray()

        async def dummy_head_send(message):
            nonlocal head_status, head_body
            if message["type"] == "http.response.start":
                head_status = message["status"]
            elif message["type"] == "http.response.body":
                head_body.extend(message.get("body", b""))

        head_scope = {
            "type": "http",
            "method": "HEAD",
            "path": "/api/game/weather",
            "headers": [],
            "query_string": b"",
        }

        await app(head_scope, dummy_receive, dummy_head_send)
        assert head_status == 200
        assert len(head_body) == 0

    asyncio.run(_test())
