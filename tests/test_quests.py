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
