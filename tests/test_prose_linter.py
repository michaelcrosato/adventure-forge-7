"""Comprehensive Test Suite for Prose Linter and Readability Gates."""
from adventure_forge.linter.prose_linter import (
    ProseLinter,
    flesch_kincaid_grade,
    word_count,
    split_sentences
)
from adventure_forge.content.loader import build_world_registry
from adventure_forge.content.schema import SceneNode
from adventure_forge.core.actions import Action


def test_shipped_content_passes_linter():
    """Verify that shipped world registry passes all linter checks once remediated."""
    registry = build_world_registry()
    linter = ProseLinter()
    passed, errors = linter.lint_registry(registry)
    assert passed, f"Prose linter found violations: {errors}"


def test_linter_rejects_purple_prose():
    linter = ProseLinter()
    purple_text = "The labyrinthine shadows danced with unfathomable malice across the gossamer floor."
    errs = linter.lint_text(purple_text)
    assert any("Disallowed purple prose" in e for e in errs)


def test_linter_rejects_long_sentences():
    linter = ProseLinter(max_sentence_words=18)
    long_text = "This is an excessively long and unnecessarily verbose sentence that goes on and on and contains far more than eighteen words in a single thought."
    errs = linter.lint_text(long_text)
    assert any("exceeds 18 words" in e for e in errs)


def test_linter_rejects_high_readability_grade():
    """Grade > 8.0 must trigger a readability linter error."""
    linter = ProseLinter()
    high_grade_prose = (
        "Bioluminescent algae illuminates the underground cavern lake. "
        "Water drips rhythmically from stalactites."
    )
    assert flesch_kincaid_grade(high_grade_prose) > 8.0
    errs = linter.lint_text(high_grade_prose)
    assert any("Readability grade" in e and "exceeds" in e for e in errs)


def test_linter_accepts_valid_hemingway_prose():
    """Crisp, active-voice sentences with grade <= 8.0 must produce zero errors."""
    linter = ProseLinter()
    valid_prose = (
        "Torch smoke clings to the damp stone archway. "
        "Two city watchmen lean on halberds."
    )
    assert flesch_kincaid_grade(valid_prose) <= 8.0
    errs = linter.lint_text(valid_prose)
    assert errs == []


def test_linter_enforces_action_label_word_count():
    """Action labels must be strictly 1-3 words."""
    linter = ProseLinter(max_action_label_words=3)
    scene = SceneNode(
        id="test_scene",
        title="Test Scene",
        region="test_region",
        description="Cold wind whips down the shale slope. Sheer rock rises into the mist.",
        base_actions=[
            Action(id="act_valid_1", label="Look", category="interaction"),
            Action(id="act_valid_2", label="Take sword", category="interaction"),
            Action(id="act_valid_3", label="Enter Grand Bazaar", category="interaction"),
            Action(id="act_invalid_4", label="Go to Grand Bazaar", category="interaction"),
            Action(id="act_invalid_empty", label="", category="interaction"),
        ]
    )
    errs = linter.lint_scene(scene)
    assert any("act_invalid_4" in e and "exceeds 3 words" in e for e in errs)
    assert any("act_invalid_empty" in e and "exceeds 3 words" in e for e in errs)
    assert not any("act_valid_1" in e for e in errs)
    assert not any("act_valid_2" in e for e in errs)
    assert not any("act_valid_3" in e for e in errs)


def test_linter_handles_edge_cases_cleanly():
    """Ensure empty strings, whitespace, punctuation, and micro-phrases do not crash or false-positive."""
    linter = ProseLinter()
    assert linter.lint_text("") == []
    assert linter.lint_text("   \n\t  ") == []
    assert linter.lint_text("... !?  ...") == []
    assert linter.lint_text("Welcome.") == []
    assert linter.lint_text("Look around.") == []
    assert linter.lint_text("The lock clicks open.") == []


def test_flesch_kincaid_grade_edge_cases():
    """Ensure flesch_kincaid_grade is immune to division by zero and returns 0.0 on empty inputs."""
    assert flesch_kincaid_grade("") == 0.0
    assert flesch_kincaid_grade("   ") == 0.0
    assert flesch_kincaid_grade("...!?") == 0.0
    assert isinstance(flesch_kincaid_grade("Normal sentence."), float)


def test_dialogue_quotation_sentence_splitting():
    """Sentences ending with quotation marks must split correctly."""
    text = '"Halt!" shouted the watchman. "State your business."'
    sentences = split_sentences(text)
    assert len(sentences) >= 2


def test_configurable_readability_bounds():
    """Test optional min_readability_grade and custom max_readability_grade."""
    linter_strict = ProseLinter(min_readability_grade=6.0)
    simple_text = "The cat sat. The dog ran."
    errs = linter_strict.lint_text(simple_text)
    assert any("Readability grade" in e and "falls below" in e for e in errs)

    linter_lenient = ProseLinter(max_readability_grade=15.0)
    moderate_text = "Iron bars secure the heavy timber entrance. Gale-force gusts howling through limestone fissures."
    assert linter_lenient.lint_text(moderate_text) == []


def test_dialogue_linting():
    """Dialogue turns exceeding 60 words must be flagged."""
    linter = ProseLinter(max_dialogue_words=60)
    long_dlg = " ".join(["word"] * 65)
    errs = linter.lint_dialogue(long_dlg)
    assert any("Dialogue exceeds 60 words" in e for e in errs)
