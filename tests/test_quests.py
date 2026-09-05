from adventure_forge.content.quests import get_continental_main_quest
from adventure_forge.core.character import CharacterSheet


def test_continental_quest_progression():
    quest = get_continental_main_quest()
    char = CharacterSheet(name="TestHero", ancestry="Plainsman", background="drifter")
    
    # Starting state: stage 1 active
    prog_0 = quest.evaluate_progress(char, {})
    assert prog_0["active_stage"] == "stage_crags_beacon"
    assert len(prog_0["completed_stages"]) == 0

    # Complete stage 1
    prog_1 = quest.evaluate_progress(char, {"crags_beacon_lit": True})
    assert "stage_crags_beacon" in prog_1["completed_stages"]
    assert prog_1["active_stage"] == "stage_warrens_ledger"

    # Complete all 5 stages across all 5 provinces
    full_flags = {
        "crags_beacon_lit": True,
        "has_watch_badge": True,
        "scorch_compass_secured": True,
        "court_verdict_won": True,
        "sunken_relic_secured": True,
    }
    prog_full = quest.evaluate_progress(char, full_flags)
    assert prog_full["is_finished"] is True
    assert len(prog_full["completed_stages"]) == 5
    assert len(quest.endings) == 3


def test_continental_quest_endings():
    """Verify all three campaign endings resolve correctly under their respective conditions."""
    quest = get_continental_main_quest()
    char = CharacterSheet(name="TestHero", ancestry="Plainsman", background="drifter")

    full_flags = {
        "crags_beacon_lit": True,
        "has_watch_badge": True,
        "scorch_compass_secured": True,
        "court_verdict_won": True,
        "sunken_relic_secured": True,
    }

    # No ending chosen yet
    prog = quest.evaluate_progress(char, full_flags)
    assert prog["is_finished"] is True
    assert prog["ending"] is None

    # Ending 1: Justiciar Order
    justiciar_flags = dict(full_flags)
    justiciar_flags["continental_ending_justiciar"] = True
    prog_j = quest.evaluate_progress(char, justiciar_flags)
    assert prog_j["ending"] == "justiciar_order"

    # Ending 2: Shadow Syndicate
    smuggler_flags = dict(full_flags)
    smuggler_flags["continental_ending_smuggler"] = True
    prog_s = quest.evaluate_progress(char, smuggler_flags)
    assert prog_s["ending"] == "shadow_syndicate"

    # Ending 3: Unbounded Ruler
    ruler_flags = dict(full_flags)
    ruler_flags["continental_ending_ruler"] = True
    prog_r = quest.evaluate_progress(char, ruler_flags)
    assert prog_r["ending"] == "unbounded_ruler"

    # Fallback resolution tests
    assert quest.resolve_ending({"five_seals_campaign_justiciar_order": True}) == "justiciar_order"
    assert quest.resolve_ending({"shadow_syndicate": True}) == "shadow_syndicate"
    assert quest.resolve_ending({"quest_ending": "unbounded_ruler"}) == "unbounded_ruler"
    assert quest.resolve_ending({"random_flag": True}) is None


def test_continental_quest_serialization():
    """Verify quest and stage to_dict serialization conforms to expected schema."""
    quest = get_continental_main_quest()
    data = quest.to_dict()
    assert data["id"] == "five_seals_campaign"
    assert len(data["stages"]) == 5
    assert "justiciar_order" in data["endings"]

    stage = quest.stages[0]
    s_data = stage.to_dict()
    assert s_data["id"] == "stage_crags_beacon"
    assert s_data["province"] == "reach"
    assert "iron_guard" in s_data["reputation_rewards"]

