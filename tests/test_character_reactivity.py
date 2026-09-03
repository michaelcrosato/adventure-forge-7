from adventure_forge.verification.counterfactual import verify_counterfactual_divergence


def test_character_counterfactual_divergence():
    passed, msg, evidence = verify_counterfactual_divergence()
    assert passed, f"{msg}: {evidence}"
