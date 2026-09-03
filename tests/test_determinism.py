from adventure_forge.verification.determinism import verify_replay_determinism


def test_determinism_and_fingerprints():
    passed, msg = verify_replay_determinism()
    assert passed, msg
