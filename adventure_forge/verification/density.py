"""Macro-World Interactable Density Verifier.

Enforces R5 / SYS-06 / Milestone 2 Invariant:
- Total scenes in world registry == 520.
- >= 50% of scenes (>= 260 scenes) offer 3+ meaningful interactables
  (non-movement base actions + environmental entities).
- Density distribution statistics per region.
"""
from typing import Dict, Any, Tuple, Optional
from adventure_forge.content.schema import RegionManifest
from adventure_forge.content.loader import build_world_registry


def verify_interactable_density(
    registry: Optional[Dict[str, RegionManifest]] = None
) -> Tuple[bool, str, Dict[str, Any]]:
    """Verify that >= 260 scenes offer >= 3 meaningful interactables."""
    if registry is None:
        registry = build_world_registry()

    total_scenes = 0
    dense_scenes = 0
    sparse_scenes = []
    region_stats = {}

    for reg_id, region in registry.items():
        reg_total = len(region.scenes)
        reg_dense = 0
        for sc_id, scene in region.scenes.items():
            total_scenes += 1
            non_move_actions = [a for a in scene.base_actions if a.category != "movement"]
            interactable_count = len(non_move_actions) + len(scene.entities)
            if interactable_count >= 3:
                dense_scenes += 1
                reg_dense += 1
            else:
                sparse_scenes.append((reg_id, sc_id, interactable_count))

        region_stats[reg_id] = {
            "total": reg_total,
            "dense": reg_dense,
            "dense_pct": round((reg_dense / reg_total * 100), 1) if reg_total > 0 else 0.0,
        }

    dense_pct = round((dense_scenes / total_scenes * 100), 2) if total_scenes > 0 else 0.0
    stats: Dict[str, Any] = {
        "total_scenes": total_scenes,
        "dense_scenes": dense_scenes,
        "dense_percentage": dense_pct,
        "required_dense": 260,
        "sparse_count": len(sparse_scenes),
        "region_stats": region_stats,
    }

    if total_scenes != 520:
        return False, f"Expected 520 total scenes in registry, found {total_scenes}.", stats

    if dense_scenes < 260:
        return False, (
            f"Interactable density invariant violated: only {dense_scenes}/{total_scenes} "
            f"({dense_pct}%) scenes have >= 3 interactables. Deficit: {260 - dense_scenes} scenes."
        ), stats

    return True, (
        f"Interactable density invariant satisfied: {dense_scenes}/{total_scenes} "
        f"scenes ({dense_pct}%) offer >= 3 meaningful interactables."
    ), stats
