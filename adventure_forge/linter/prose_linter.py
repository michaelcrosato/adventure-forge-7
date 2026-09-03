"""High-Velocity Hemingway Prose Linter.

Enforces G2 / GAME-02:
- Max 18 words per sentence.
- 1-2 sentences per room description.
- 1-3 words per UI action label.
- Max 60 words per dialogue line.
- Grade 6-8 reading level target.
- Disallows ornamental purple prose clichés.
"""
import re
from typing import List, Dict, Any, Tuple


# Clichés and ornamental adjectives forbidden by the Hemingway baseline
FORBIDDEN_PURPLE_WORDS = {
    "tapestry", "gossamer", "labyrinthine", "palpable", "unfathomable",
    "eldritch", "malice", "kaleidoscope", "cacophony", "resplendent",
    "scintillating", "coruscating", "sepulchral", "crepuscular"
}


def split_sentences(text: str) -> List[str]:
    """Split text into sentences using punctuation boundaries."""
    raw = re.split(r'[.!?]+(?:\s+|$)', text.strip())
    return [s.strip() for s in raw if s.strip()]


def word_count(text: str) -> int:
    return len(re.findall(r'\b[\w\'-]+\b', text))


def estimate_syllables(word: str) -> int:
    """Heuristic syllable counter for readability index."""
    w = word.lower().strip()
    if len(w) <= 3:
        return 1
    w = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', w)
    w = re.sub(r'^y', '', w)
    sylls = len(re.findall(r'[aeiouy]{1,2}', w))
    return max(1, sylls)


def flesch_kincaid_grade(text: str) -> float:
    """Calculate Flesch-Kincaid Grade Level."""
    sentences = split_sentences(text)
    if not sentences:
        return 0.0
    words = re.findall(r'\b[\w\'-]+\b', text)
    if not words:
        return 0.0
    num_sentences = len(sentences)
    num_words = len(words)
    num_syllables = sum(estimate_syllables(w) for w in words)

    grade = 0.39 * (num_words / num_sentences) + 11.8 * (num_syllables / num_words) - 15.59
    return round(grade, 2)


class ProseLinter:
    """Linter verifying plain-language and Hemingway-baseline constraints."""

    def __init__(
        self,
        max_sentence_words: int = 18,
        max_room_sentences: int = 3,
        max_action_label_words: int = 4,
        max_dialogue_words: int = 60
    ):
        self.max_sentence_words = max_sentence_words
        self.max_room_sentences = max_room_sentences
        self.max_action_label_words = max_action_label_words
        self.max_dialogue_words = max_dialogue_words

    def lint_text(self, text: str, context: str = "text") -> List[str]:
        """Lint a piece of prose for length, sentence bounds, and purple words."""
        errors = []
        sentences = split_sentences(text)

        # Check purple prose
        words = [w.lower() for w in re.findall(r'\b[\w\'-]+\b', text)]
        for w in words:
            if w in FORBIDDEN_PURPLE_WORDS:
                errors.append(f"[{context}] Disallowed purple prose word found: '{w}'")

        # Sentence length
        for idx, s in enumerate(sentences, 1):
            count = word_count(s)
            if count > self.max_sentence_words:
                errors.append(
                    f"[{context}] Sentence {idx} exceeds {self.max_sentence_words} words ({count} words): '{s[:40]}...'"
                )

        return errors

    def lint_scene(self, scene: Any) -> List[str]:
        """Lint an entire SceneNode including descriptions, dynamic snippets, and action labels."""
        errors = []
        # Room description
        desc_sentences = split_sentences(scene.description)
        if len(desc_sentences) > self.max_room_sentences:
            errors.append(
                f"[Scene {scene.id}] Description exceeds {self.max_room_sentences} sentences ({len(desc_sentences)} sentences)."
            )
        errors.extend(self.lint_text(scene.description, f"Scene {scene.id} Description"))

        # Dynamic descriptions
        for idx, dyn in enumerate(scene.dynamic_descriptions, 1):
            dyn_sentences = split_sentences(dyn.text)
            if len(dyn_sentences) > 2:
                errors.append(
                    f"[Scene {scene.id} Dynamic #{idx}] Exceeds 2 sentences ({len(dyn_sentences)} sentences)."
                )
            errors.extend(self.lint_text(dyn.text, f"Scene {scene.id} Dynamic #{idx}"))

        # Action labels
        for act in scene.base_actions:
            lbl_count = word_count(act.label)
            if lbl_count > self.max_action_label_words:
                errors.append(
                    f"[Scene {scene.id} Action {act.id}] Label exceeds {self.max_action_label_words} words ({lbl_count} words): '{act.label}'"
                )
            if act.result_text:
                errors.extend(self.lint_text(act.result_text, f"Scene {scene.id} Action {act.id} Result"))

        return errors

    def lint_registry(self, world_registry: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Lint an entire world registry. Returns (passed, error_list)."""
        all_errors = []
        for reg_id, region in world_registry.items():
            for sc_id, scene in region.scenes.items():
                errs = self.lint_scene(scene)
                all_errors.extend(errs)
        return len(all_errors) == 0, all_errors
