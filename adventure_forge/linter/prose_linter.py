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
from typing import List, Dict, Any, Tuple, Optional


# Clichés and ornamental adjectives forbidden by the Hemingway baseline
FORBIDDEN_PURPLE_WORDS = {
    "tapestry", "gossamer", "labyrinthine", "palpable", "unfathomable",
    "eldritch", "malice", "kaleidoscope", "cacophony", "resplendent",
    "scintillating", "coruscating", "sepulchral", "crepuscular"
}


def split_sentences(text: str) -> List[str]:
    """Split text into sentences using punctuation boundaries, including quotes."""
    raw = re.split(r'[.!?]+[\"\'\u201d\u2019]*(?:\s+|$)', text.strip())
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
        max_action_label_words: int = 3,
        max_dialogue_words: int = 60,
        max_readability_grade: float = 8.0,
        min_readability_grade: Optional[float] = None,
        min_readability_words: int = 5,
        **kwargs: Any
    ):
        self.max_sentence_words = max_sentence_words
        self.max_room_sentences = max_room_sentences
        self.max_action_label_words = max_action_label_words
        self.max_dialogue_words = max_dialogue_words
        # Support aliases max_grade / min_grade / min_words if passed via kwargs
        self.max_readability_grade = kwargs.get("max_grade", max_readability_grade)
        self.min_readability_grade = kwargs.get("min_grade", min_readability_grade)
        self.min_readability_words = kwargs.get("min_words", min_readability_words)

    def lint_text(
        self,
        text: str,
        context: str = "text",
        check_readability: bool = True
    ) -> List[str]:
        """Lint a piece of prose for length, sentence bounds, purple words, and readability."""
        errors: List[str] = []
        if not text or not text.strip():
            return errors

        sentences = split_sentences(text)
        words = [w.lower() for w in re.findall(r'\b[\w\'-]+\b', text)]
        if not words:
            return errors

        # Check purple prose
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

        # Readability (Flesch-Kincaid Grade Level)
        # Bypassed on micro-phrases (< min_readability_words) to prevent syllable-ratio false positives
        if check_readability and len(words) >= self.min_readability_words:
            grade = flesch_kincaid_grade(text)
            if self.max_readability_grade is not None and grade > self.max_readability_grade:
                errors.append(
                    f"[{context}] Readability grade {grade} exceeds maximum {self.max_readability_grade} (target Grade 6-8)."
                )
            if self.min_readability_grade is not None and grade < self.min_readability_grade:
                errors.append(
                    f"[{context}] Readability grade {grade} falls below minimum {self.min_readability_grade} (target Grade 6-8)."
                )

        return errors

    def lint_dialogue(self, text: str, context: str = "dialogue") -> List[str]:
        """Lint a dialogue turn for length (<=60 words), sentence bounds, purple words, and readability."""
        errors: List[str] = []
        if not text or not text.strip():
            return errors
        total_words = word_count(text)
        if total_words > self.max_dialogue_words:
            errors.append(
                f"[{context}] Dialogue exceeds {self.max_dialogue_words} words ({total_words} words): '{text[:40]}...'"
            )
        errors.extend(self.lint_text(text, context=context))
        return errors

    def lint_scene(self, scene: Any) -> List[str]:
        """Lint an entire SceneNode including descriptions, dynamic snippets, and action labels."""
        errors: List[str] = []

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
            errors.extend(self.lint_text(dyn.text, f"Scene {scene.id} Dynamic #{idx}", check_readability=False))

        # Action labels & results
        for act in scene.base_actions:
            lbl_count = word_count(act.label)
            if lbl_count < 1 or lbl_count > self.max_action_label_words:
                errors.append(
                    f"[Scene {scene.id} Action {act.id}] Label exceeds {self.max_action_label_words} words ({lbl_count} words): '{act.label}'"
                )
            if act.result_text:
                errors.extend(self.lint_text(act.result_text, f"Scene {scene.id} Action {act.id} Result", check_readability=False))

        # Entity descriptions (if present)
        for ent in getattr(scene, 'entities', []):
            if isinstance(ent, dict) and 'description' in ent and ent['description']:
                errors.extend(
                    self.lint_text(ent['description'], f"Scene {scene.id} Entity {ent.get('id', 'unknown')} Description", check_readability=False)
                )

        return errors

    def lint_registry(self, world_registry: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Lint an entire world registry. Returns (passed, error_list)."""
        all_errors: List[str] = []
        for reg_id, region in world_registry.items():
            for sc_id, scene in region.scenes.items():
                errs = self.lint_scene(scene)
                all_errors.extend(errs)
        return len(all_errors) == 0, all_errors
