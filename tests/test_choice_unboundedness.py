from adventure_forge.verification.stress import verify_large_action_set


def test_choice_unboundedness_and_no_menu_caps():
    passed, msg, evidence = verify_large_action_set()
    assert passed, f"{msg}: {evidence}"
    assert evidence["action_count"] >= 100
