from adventure_forge.linter.prose_linter import ProseLinter, flesch_kincaid_grade, word_count
from adventure_forge.content.loader import build_world_registry


def test_shipped_content_passes_linter():
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
