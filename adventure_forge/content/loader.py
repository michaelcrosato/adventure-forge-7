"""World Content Loader and Link Validator.

Assembles and validates the contiguous world graph across all regions, POIs, and scenes.
"""
from typing import Dict, Any, List, Set, Tuple
from adventure_forge.content.schema import RegionManifest, SceneNode
from adventure_forge.core.actions import Action


def build_world_registry() -> Dict[str, RegionManifest]:
    """Build and return the comprehensive shipped world registry."""
    from adventure_forge.content.data.crags import build_iron_crags_region
    from adventure_forge.content.data.warrens import build_lower_warrens_region
    from adventure_forge.content.data.scorchwaste import build_scorchwaste_region
    from adventure_forge.content.data.court import build_high_court_region
    from adventure_forge.content.data.hollows import build_sunken_hollows_region
    from adventure_forge.content.data.stress_market import build_stress_market_region
    from adventure_forge.content.data.provinces.reach import build_reach_province
    from adventure_forge.content.data.provinces.lowlands import build_lowlands_province
    from adventure_forge.content.data.provinces.scorchwaste import build_scorchwaste_province
    from adventure_forge.content.data.provinces.high_court import build_high_court_province
    from adventure_forge.content.data.provinces.sunken_hollows import build_sunken_hollows_province

    return {
        "iron_crags": build_iron_crags_region(),
        "lower_warrens": build_lower_warrens_region(),
        "scorchwaste_local": build_scorchwaste_region(),
        "high_court_local": build_high_court_region(),
        "sunken_hollows_local": build_sunken_hollows_region(),
        "stress_market": build_stress_market_region(),
        "province_reach": build_reach_province(),
        "province_lowlands": build_lowlands_province(),
        "province_scorchwaste": build_scorchwaste_province(),
        "province_high_court": build_high_court_province(),
        "province_sunken_hollows": build_sunken_hollows_province(),
    }


def validate_world_links(registry: Dict[str, RegionManifest]) -> Tuple[bool, List[str]]:
    """Verify that every target_scene reference in any action or entity resolves to a valid scene."""
    all_scenes: Set[str] = set()
    for region in registry.values():
        for scene_id in region.scenes.keys():
            all_scenes.add(scene_id)

    errors = []
    for reg_id, region in registry.items():
        for sc_id, scene in region.scenes.items():
            # Check base actions
            for act in scene.base_actions:
                if act.target_scene and act.target_scene not in all_scenes:
                    errors.append(f"[{sc_id}] Action '{act.id}' targets unknown scene: '{act.target_scene}'")
            # Check entities
            for ent in scene.entities:
                dest = ent.get("climb_destination")
                if dest and dest not in all_scenes:
                    errors.append(f"[{sc_id}] Entity '{ent.get('id')}' destination unknown: '{dest}'")

    return len(errors) == 0, errors
