"""Adversarial stress-test suite for ProseLinter.

Authored by Challenger M1.1 to empirically challenge and stress-test:
1. Malformed, empty, massive, and boundary-length inputs.
2. Tricky dialogue punctuation: nested quotes, em-dashes, ellipsis, Unicode quotes.
3. Strict word boundaries: 18/19 words per sentence; 3/4 words per action label; 60/61 dialogue words.
4. Readability boundaries: Grade 6-8 bounds, scientific/legal jargon rejection, micro-phrase bypass.
5. Syllable counter heuristics and resilience.
"""
from adventure_forge.linter.prose_linter import (
    ProseLinter,
    flesch_kincaid_grade,
    word_count,
    split_sentences,
    estimate_syllables,
    FORBIDDEN_PURPLE_WORDS,
)
from adventure_forge.content.schema import SceneNode
from adventure_forge.core.actions import Action


# ==============================================================================
# 1. Malformed, Empty, Massive, and Boundary-Length Inputs
# ==============================================================================

def test_empty_and_whitespace_inputs():
    linter = ProseLinter()
    for empty in ["", "   ", "\t\t\n\r\n", "   \n  \t "]:
        assert linter.lint_text(empty) == []
        assert linter.lint_dialogue(empty) == []
        assert flesch_kincaid_grade(empty) == 0.0
        assert word_count(empty) == 0
        assert split_sentences(empty) == []


def test_punctuation_only_inputs():
    linter = ProseLinter()
    punct_cases = [
        "...",
        "?!?!?!",
        "... --- ...",
        ",,, ;;; :::: () [] {}",
        "\"\"\" '''",
        "—–—",
    ]
    for p in punct_cases:
        assert linter.lint_text(p) == []
        assert linter.lint_dialogue(p) == []
        assert flesch_kincaid_grade(p) == 0.0
        assert word_count(p) == 0


def test_massive_sentence_rejection_and_performance():
    """Verify that a massive sentence (1,000 words) is caught and does not cause ReDoS."""
    linter = ProseLinter(max_sentence_words=18)
    massive_text = " ".join(["word"] * 1000) + "."
    errs = linter.lint_text(massive_text)
    assert len(errs) > 0
    assert any("exceeds 18 words" in e for e in errs)
    assert word_count(massive_text) == 1000


def test_massive_single_word_token():
    """Verify that a massive word token (10,000 chars) doesn't hang the syllable estimator."""
    long_token = "a" * 10000
    sylls = estimate_syllables(long_token)
    assert sylls >= 1


def test_unicode_and_special_characters():
    """Test accented characters, non-Latin scripts, and emojis."""
    linter = ProseLinter()
    # Emojis should not crash
    emoji_text = "⚔️ 🛡️ 🔥 🐉"
    assert linter.lint_text(emoji_text) == []
    assert word_count(emoji_text) == 0

    # Accented text
    accented = "Café shields withstand naïve dragon attacks."
    assert word_count(accented) == 6
    errs = linter.lint_text(accented)
    assert errs == []


# ==============================================================================
# 2. Dialogue Punctuation & Quotes
# ==============================================================================

def test_dialogue_nested_quotes():
    """Dialogue with nested quotes should split properly into sentences without losing words."""
    linter = ProseLinter(max_sentence_words=18)
    text = '"Hold!" shouted the guard. "Did he say \'surrender\' to the commander?"'
    sentences = split_sentences(text)
    assert len(sentences) >= 2
    errs = linter.lint_text(text)
    assert errs == []


def test_unicode_quotes_sentence_splitting():
    """Smart/curly quotes (U+201C, U+201D, U+2018, U+2019) at sentence boundaries."""
    text = "“Advance through the pass!” whispered the ranger. “Keep low to the ground.”"
    sentences = split_sentences(text)
    assert len(sentences) >= 2
    for s in sentences:
        assert word_count(s) <= 18


def test_dialogue_em_dashes_and_ellipses():
    """Em-dashes and ellipses should not fuse adjacent sentences or cause miscounts."""
    text = "Wait... who approaches? The shadow moves—silent and swift."
    sentences = split_sentences(text)
    assert len(sentences) >= 2
    total_words = word_count(text)
    sum_words = sum(word_count(s) for s in sentences)
    assert sum_words == total_words


# ==============================================================================
# 3. Exact Word Boundaries: 18/19 Words, 3/4 Label Words, 60/61 Dialogue Words
# ==============================================================================

def test_exact_sentence_boundary_18_vs_19_words():
    """A sentence with exactly 18 words passes; exactly 19 words is rejected."""
    linter = ProseLinter(max_sentence_words=18)

    # 18 words
    words_18 = "One two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen."
    assert word_count(words_18) == 18
    assert linter.lint_text(words_18, check_readability=False) == []

    # 19 words
    words_19 = "One two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen."
    assert word_count(words_19) == 19
    errs_19 = linter.lint_text(words_19, check_readability=False)
    assert len(errs_19) == 1
    assert "exceeds 18 words (19 words)" in errs_19[0]


def test_exact_action_label_boundary_3_vs_4_words():
    """Action labels with 1, 2, 3 words pass; 0 words or 4 words are rejected."""
    linter = ProseLinter(max_action_label_words=3)

    for valid_label in ["Attack", "Open chest", "Enter Grand Bazaar"]:
        assert 1 <= word_count(valid_label) <= 3
        scene = SceneNode(
            id="test_sc",
            title="T",
            region="R",
            description="Short desc.",
            base_actions=[Action(id="a1", label=valid_label, category="interaction")]
        )
        assert linter.lint_scene(scene) == []

    # 4 words -> rejected
    scene_4 = SceneNode(
        id="test_sc4",
        title="T",
        region="R",
        description="Short desc.",
        base_actions=[Action(id="a4", label="Go to Grand Bazaar", category="interaction")]
    )
    errs_4 = linter.lint_scene(scene_4)
    assert any("Label exceeds 3 words (4 words)" in e for e in errs_4)

    # 0 words -> rejected
    scene_0 = SceneNode(
        id="test_sc0",
        title="T",
        region="R",
        description="Short desc.",
        base_actions=[Action(id="a0", label="   ", category="interaction")]
    )
    errs_0 = linter.lint_scene(scene_0)
    assert any("Label exceeds 3 words (0 words)" in e for e in errs_0)


def test_exact_dialogue_boundary_60_vs_61_words():
    """Dialogue turn with exactly 60 words passes; 61 words is rejected."""
    linter = ProseLinter(max_dialogue_words=60, max_sentence_words=18)

    # 4 sentences of 15 words = 60 words
    sent_15 = "One two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen."
    dlg_60 = f"{sent_15} {sent_15} {sent_15} {sent_15}"
    assert word_count(dlg_60) == 60
    assert linter.lint_dialogue(dlg_60) == []

    # 61 words -> rejected
    sent_16 = "One two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen."
    dlg_61 = f"{sent_15} {sent_15} {sent_15} {sent_16}"
    assert word_count(dlg_61) == 61
    errs_61 = linter.lint_dialogue(dlg_61)
    assert any("Dialogue exceeds 60 words (61 words)" in e for e in errs_61)


# ==============================================================================
# 4. Purple Prose Detection Exhaustiveness
# ==============================================================================

def test_all_forbidden_purple_words_rejected():
    """Every single word in FORBIDDEN_PURPLE_WORDS must be rejected under any casing."""
    linter = ProseLinter()
    for word in FORBIDDEN_PURPLE_WORDS:
        # Lowercase
        errs_lower = linter.lint_text(f"The {word} is here.")
        assert any(f"Disallowed purple prose word found: '{word}'" in e for e in errs_lower), f"Failed to reject lowercase '{word}'"

        # Uppercase / Titlecase
        title_word = word.capitalize()
        errs_title = linter.lint_text(f"{title_word} surrounds the stone.")
        assert any(f"Disallowed purple prose word found: '{word}'" in e for e in errs_title), f"Failed to reject titlecase '{title_word}'"

        # ALL CAPS
        upper_word = word.upper()
        errs_upper = linter.lint_text(f"BEHOLD THE {upper_word}!")
        assert any(f"Disallowed purple prose word found: '{word}'" in e for e in errs_upper), f"Failed to reject uppercase '{upper_word}'"


# ==============================================================================
# 5. Readability Rejection: Scientific, Legal, Jargon & Grade Bounds
# ==============================================================================

def test_scientific_jargon_rejected_100_percent():
    """Scientific, medical, and legal jargon with grade > 8.0 must be 100% rejected."""
    linter = ProseLinter()
    adversarial_texts = [
        # Quantum physics
        "Quantum chromodynamics investigates non-Abelian gauge theories characterizing relativistic thermodynamic interactions.",
        # Biochemistry
        "Bioluminescent algae illuminates the underground cavern lake. Deoxyribonucleic acid sequencing reveals distinct mutations.",
        # Legal boilerplate
        "The indemnification agreement supersedes all prior unilateral covenants, warranties, and testamentary dispositions.",
        # Academic prose
        "Epistemological foundationalism posits incorrigible experiential justifications for perceptual assertions.",
    ]
    for text in adversarial_texts:
        grade = flesch_kincaid_grade(text)
        assert grade > 8.0, f"Expected grade > 8.0 for '{text}', got {grade}"
        errs = linter.lint_text(text)
        assert any("Readability grade" in e and "exceeds maximum 8.0" in e for e in errs), f"Linter failed to reject high readability: {text}"


def test_grade_bounds_6_to_8_exact_calibration():
    """Test strict enforcement when min_readability_grade=6.0 and max_readability_grade=8.0."""
    linter_bounded = ProseLinter(min_readability_grade=6.0, max_readability_grade=8.0)

    # Simple text (Grade < 6.0) -> rejected by min bound
    too_simple = "The cat sat on the mat. The dog ran fast."
    grade_simple = flesch_kincaid_grade(too_simple)
    assert grade_simple < 6.0
    errs_simple = linter_bounded.lint_text(too_simple)
    assert any("falls below minimum 6.0" in e for e in errs_simple)

    # Complex text (Grade > 8.0) -> rejected by max bound
    too_complex = "Bioluminescent algae illuminates the underground cavern lake. Water drips rhythmically from stalactites."
    grade_complex = flesch_kincaid_grade(too_complex)
    assert grade_complex > 8.0
    errs_complex = linter_bounded.lint_text(too_complex)
    assert any("exceeds maximum 8.0" in e for e in errs_complex)


def test_micro_phrase_readability_bypass():
    """Short labels, phrases, and commands (< min_readability_words) must bypass FKGL."""
    linter = ProseLinter(min_readability_words=5)
    # 4-word phrase with long syllables shouldn't trigger FKGL error
    short_high_syllable = "Ophthalmology clinic opens."  # 3 words, very high syllable ratio
    errs = linter.lint_text(short_high_syllable)
    assert errs == []


# ==============================================================================
# 6. Room and Dynamic Description Sentence Limits
# ==============================================================================

def test_scene_description_sentence_limits():
    """Room description exceeds max_room_sentences (default 3); dynamic exceeds 2."""
    linter = ProseLinter(max_room_sentences=3)

    # 4-sentence room description -> rejected
    scene_4_sent = SceneNode(
        id="sc_4",
        title="Four Sentences",
        region="reg",
        description="One sentence here. Second sentence here. Third sentence here. Fourth sentence here.",
        base_actions=[Action(id="a", label="Look", category="interaction")]
    )
    errs_room = linter.lint_scene(scene_4_sent)
    assert any("Description exceeds 3 sentences (4 sentences)" in e for e in errs_room)

    # 3-sentence room description -> accepted
    scene_3_sent = SceneNode(
        id="sc_3",
        title="Three Sentences",
        region="reg",
        description="One sentence here. Second sentence here. Third sentence here.",
        base_actions=[Action(id="a", label="Look", category="interaction")]
    )
    assert linter.lint_scene(scene_3_sent) == []


# ==============================================================================
# 7. Exact Mathematical FKGL Boundary Validation (5.99, 6.00, 7.00, 8.00, 8.01)
# ==============================================================================

def test_exact_grade_boundary_precision_599_600_700_800_801():
    """Mathematically verify FKGL boundaries at 5.99 (reject), 6.00 (accept), 7.00 (accept), 8.00 (accept), 8.01 (reject)."""
    linter = ProseLinter(min_readability_grade=6.0, max_readability_grade=8.0)

    # 5.99 FKGL (1 sentence, 15 words, 20 syllables)
    t599 = "cold dark stone gate deep night wind frost hall keep iron ancient silent cavern frozen."
    assert flesch_kincaid_grade(t599) == 5.99
    errs_599 = linter.lint_text(t599)
    assert any("Readability grade 5.99 falls below minimum 6.0" in e for e in errs_599)

    # 6.00 FKGL (2 sentences, 7 words, 12 syllables)
    t600 = "iron ancient cold. silent cavern frozen dark."
    assert flesch_kincaid_grade(t600) == 6.00
    assert linter.lint_text(t600) == []

    # 7.00 FKGL (1 sentence, 17 words, 23 syllables)
    t700 = "cold dark stone gate deep night wind frost hall keep blade iron ancient silent cavern frozen shadow."
    assert flesch_kincaid_grade(t700) == 7.00
    assert linter.lint_text(t700) == []

    # 8.00 FKGL (3 sentences, 19 words, 34 syllables)
    s1 = "iron ancient silent cavern frozen shadow."
    s2 = "pathway temple valley dungeon ancient cavern."
    s3 = "cold dark cavern frozen shadow pathway temple."
    t800 = f"{s1} {s2} {s3}"
    assert flesch_kincaid_grade(t800) == 8.00
    assert linter.lint_text(t800) == []

    # 8.01 FKGL (1 sentence, 11 words, 18 syllables)
    t801 = "cold dark stone gate iron ancient silent cavern frozen shadow pathway."
    assert flesch_kincaid_grade(t801) == 8.01
    errs_801 = linter.lint_text(t801)
    assert any("Readability grade 8.01 exceeds maximum 8.0" in e for e in errs_801)


# ==============================================================================
# 8. Syllable Heuristics & Formatting Edge Cases
# ==============================================================================

def test_syllable_heuristic_edge_cases():
    """Verify syllable counter handles edge cases without zero/negative return or crashes."""
    tricky_words = [
        ("a", 1),
        ("i", 1),
        ("don't", 1),
        ("it's", 1),
        ("watchman's", 2),
        ("bottle", 1),
        ("walked", 1),
        ("waited", 1),
        ("fissures", 2),
        ("rhythm", 1),
        ("abyss", 2),
        ("dynamite", 3),
    ]
    for word, expected in tricky_words:
        actual = estimate_syllables(word)
        assert actual == expected, f"Word '{word}' expected {expected} syllables, got {actual}"


def test_multiline_and_tab_formatted_prose():
    """Verify that multi-line text with carriage returns, tabs, and multiple spaces behaves identically."""
    linter = ProseLinter(max_sentence_words=18)
    formatted_text = "Iron bars\tsecure\tthe heavy\r\ntimber entrance.\r\nCold wind   blows through the gap."
    sentences = split_sentences(formatted_text)
    assert len(sentences) == 2
    assert word_count(sentences[0]) == 7
    assert word_count(sentences[1]) == 6
    assert linter.lint_text(formatted_text) == []
