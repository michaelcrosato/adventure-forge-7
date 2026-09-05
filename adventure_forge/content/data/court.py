"""Region 4: The High Court of Veras.

Unique Mechanic: Legal Evidence, Cross-Examination, and Social Decorum.
"""
from adventure_forge.content.schema import RegionManifest, SceneNode, DynamicDescription
from adventure_forge.core.actions import Action


def build_high_court_region() -> RegionManifest:
    scenes = {}

    # Scene 1: The Grand Antechamber
    scenes["court_antechamber"] = SceneNode(
        id="court_antechamber",
        title="High Court Antechamber",
        region="high_court",
        description="Polished marble floors echo under heavy footsteps. Clerks in grey robes carry sealed scrolls.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"background_is": "noble_exile"},
                text="You recognize the heraldic seal of the Chief Magistrate."
            ),
            DynamicDescription(
                condition={"has_trait": "skeptical"},
                text="You catch a clerk hiding a forged document in his sleeve."
            )
        ],
        entities=[
            {
                "id": "archive_cabinet",
                "name": "Archive Cabinet",
                "tags": ["lockable", "scavengeable"],
                "initial_state": "locked"
            }
        ],
        base_actions=[
            Action(
                id="present_writ",
                label="Present legal writ",
                category="social",
                condition={"has_item": "legal_dossier"},
                effects=[
                    {"set_flag": {"flag": "granted_court_audience", "value": True}},
                    {"log_event": "The Chief Bailiff verified your sealed dossier."}
                ],
                target_scene="court_tribunal",
                result_text="The bailiff inspects the wax seal and opens the grand double doors.",
                risk="low"
            ),
            Action(
                id="plead_urgent_case",
                label="Plead urgent case",
                category="social",
                condition={"min_skill": {"skill": "rhetoric", "value": 3}},
                effects=[
                    {"set_flag": {"flag": "plea_admitted", "value": True}},
                    {"log_event": "Your persuasive legal rhetoric swayed the registrar."}
                ],
                target_scene="court_tribunal",
                result_text="The magistrate registrar stamps an emergency writ of summons.",
                risk="medium"
            ),
            Action(
                id="slip_into_tribunal",
                label="Sneak past bailiff",
                category="movement",
                condition={
                    "any_of": [
                        {"min_skill": {"skill": "stealth", "value": 3}},
                        {"min_skill": {"skill": "cunning", "value": 3}},
                        {"has_trait": "streetwise"}
                    ]
                },
                target_scene="court_tribunal",
                result_text="You slip past the bailiff behind the tall velvet curtains.",
                risk="medium"
            ),
            Action(
                id="exit_to_bazaar",
                label="Return to Bazaar",
                category="movement",
                target_scene="bazaar_center",
                result_text="You exit through the colonnade onto the public square.",
                risk="low"
            )
        ]
    )

    # Scene 2: The Tribunal
    scenes["court_tribunal"] = SceneNode(
        id="court_tribunal",
        title="The Marble Tribunal",
        region="high_court",
        description="Three judges sit behind an elevated cedar dais. Armed bailiffs flank the prisoner bar.",
        dynamic_descriptions=[
            DynamicDescription(
                condition={"min_skill": {"skill": "rhetoric", "value": 4}},
                text="The presiding judge leans forward with intense focus."
            )
        ],
        entities=[
            {
                "id": "bench_cedar",
                "name": "Magistrate Bench",
                "tags": ["interactable"]
            },
            {
                "id": "evidence_dossier",
                "name": "Exhibit Chest",
                "tags": ["lockable"],
                "initial_state": "locked"
            }
        ],
        base_actions=[
            Action(
                id="deliver_argument",
                label="Deliver argument",
                category="social",
                effects=[
                    {"set_flag": {"flag": "court_verdict_won", "value": True}},
                    {"modify_reputation": {"faction": "justiciars", "value": 15}},
                    {"log_event": "The high tribunal ruled in your favor with full exoneration."}
                ],
                result_text="The lead judge brings the iron gavel down with a resounding strike.",
                risk="low"
            ),
            Action(
                id="examine_statutes",
                label="Review legal statutes",
                category="interaction",
                effects=[
                    {"set_flag": {"flag": "memorized_court_precedents", "value": True}},
                    {"log_event": "You studied past judicial rulings on tribunal records."}
                ],
                result_text="Parchment records cite ancient laws and decrees.",
                risk="low"
            ),
            Action(
                id="leave_tribunal",
                label="Leave chamber",
                category="movement",
                target_scene="court_antechamber",
                result_text="You step back into the cool marble hallway.",
                risk="low"
            )
        ]
    )

    return RegionManifest(
        id="high_court",
        name="The High Court of Veras",
        mechanic_name="Legal Evidence & Judicial Debate",
        mechanic_description="Court writs, testimony verification, and forensic advocacy.",
        scenes=scenes
    )
