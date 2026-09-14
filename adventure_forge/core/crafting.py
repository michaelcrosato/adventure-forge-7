"""Master Field Crafting & Alchemical Synthesis System (Milestone 17).

Provides pure, deterministic field crafting and alchemical synthesis that
dynamically generates item affordances when the character possesses required
salvage ingredients, regional materials, and prerequisite skills or traits.
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class CraftingRecipe:
    """Specification of a deterministic crafting recipe."""
    id: str
    action_id: str
    label: str  # Exactly 1 to 3 words
    category: str  # "crafting"
    required_items: Dict[str, int]  # item_id -> quantity needed
    produced_item: str
    produced_quantity: int = 1
    required_skill: Optional[Tuple[str, int]] = None  # (skill_name, min_level)
    required_trait: Optional[str] = None  # trait_name
    stamina_cost: int = 0
    result_text: str = ""  # 1-2 short sentences, <= 18 words/sent
    log_event: str = ""

    def is_available(self, character: CharacterSheet, world_flags: Dict[str, Any]) -> bool:
        """Evaluate if the character can currently execute this recipe."""
        # Check stamina
        if character.stamina < self.stamina_cost:
            return False

        # Check skill requirement if any
        if self.required_skill is not None:
            skill_name, min_val = self.required_skill
            if character.get_skill(skill_name) < min_val:
                return False

        # Check trait requirement if any
        if self.required_trait is not None:
            if not character.has_trait(self.required_trait):
                return False

        # Check inventory items and quantities
        for item, count in self.required_items.items():
            if isinstance(character.inventory, dict):
                has_count = int(character.inventory.get(item, 0))
            elif isinstance(character.inventory, (list, tuple)):
                has_count = character.inventory.count(item)
            else:
                has_count = 1 if character.has_item(item) else 0
            if has_count < count:
                return False

        return True

    def build_effects(self) -> List[Dict[str, Any]]:
        """Construct the pure deterministic effects list for this crafting action."""
        effects: List[Dict[str, Any]] = []
        # Consume ingredients
        for item, count in self.required_items.items():
            for _ in range(count):
                effects.append({"remove_item": item})
        # Produce items
        for _ in range(self.produced_quantity):
            effects.append({"add_item": self.produced_item})
        # Record craft flag and emit log
        effects.append({"set_flag": {"flag": f"crafted_{self.id}", "value": True}})
        if self.log_event:
            effects.append({"log_event": self.log_event})
        return effects


CRAFTING_RECIPES: Dict[str, CraftingRecipe] = {
    "lockpick": CraftingRecipe(
        id="lockpick",
        action_id="craft_lockpick",
        label="Forge Lockpick",
        category="crafting",
        required_items={"scrap_metal": 1, "flint": 1},
        produced_item="lockpick",
        produced_quantity=1,
        stamina_cost=0,
        result_text="You shape the metal scrap with flint into a tension wrench and pick.",
        log_event="You crafted a lockpick.",
    ),
    "torch": CraftingRecipe(
        id="torch",
        action_id="craft_torch",
        label="Craft Torch",
        category="crafting",
        required_items={"cloth_scraps": 1, "pine_pitch": 1},
        produced_item="torch",
        produced_quantity=1,
        stamina_cost=0,
        result_text="You wrap scrap cloth around pitch pine to fashion a steady torch.",
        log_event="You crafted a torch.",
    ),
    "crowbar": CraftingRecipe(
        id="crowbar",
        action_id="craft_crowbar",
        label="Forge Lever",
        category="crafting",
        required_items={"scrap_metal": 2},
        produced_item="crowbar",
        produced_quantity=1,
        stamina_cost=1,
        result_text="You bend the heavy metal scrap into a sturdy prying lever.",
        log_event="You forged a crowbar.",
    ),
    "mask": CraftingRecipe(
        id="mask",
        action_id="craft_mask",
        label="Craft Mask",
        category="crafting",
        required_items={"cloth_scraps": 1, "charcoal": 1},
        produced_item="mask",
        produced_quantity=1,
        stamina_cost=0,
        result_text="You layer porous cloth with charcoal powder to filter toxic fumes.",
        log_event="You crafted a filter mask.",
    ),
    "tonic": CraftingRecipe(
        id="tonic",
        action_id="craft_tonic",
        label="Brew Tonic",
        category="crafting",
        required_items={"algae_sample": 1, "water_skin": 1},
        produced_item="herbal_salve",
        produced_quantity=1,
        stamina_cost=0,
        result_text="You crush the algae into water to brew a cleansing medicinal balm.",
        log_event="You brewed a medicinal salve.",
    ),
    "pitch_seal": CraftingRecipe(
        id="pitch_seal",
        action_id="craft_pitch_seal",
        label="Brew Pitch Seal",
        category="crafting",
        required_items={"pine_pitch": 1, "tallow": 1},
        produced_item="waterproof_seal",
        produced_quantity=1,
        stamina_cost=0,
        result_text="You blend sticky pitch with tallow into a tight waterproof seal.",
        log_event="You brewed a waterproof seal.",
    ),
    "climbing_rope": CraftingRecipe(
        id="climbing_rope",
        action_id="craft_climbing_rope",
        label="Weave Rope",
        category="crafting",
        required_items={"cloth_scraps": 2},
        produced_item="climbing_rope",
        produced_quantity=1,
        stamina_cost=1,
        result_text="You braid thick cloth strips into a durable climbing line.",
        log_event="You braided a climbing rope.",
    ),
    "desert_cowl": CraftingRecipe(
        id="desert_cowl",
        action_id="craft_desert_cowl",
        label="Stitch Cowl",
        category="crafting",
        required_items={"cloth_scraps": 1, "tallow": 1},
        produced_item="cloak",
        produced_quantity=1,
        stamina_cost=0,
        result_text="You stitch treated cloth into a desert cowl to deflect harsh heat.",
        log_event="You stitched a protective cowl.",
    ),
    "acid_vial": CraftingRecipe(
        id="acid_vial",
        action_id="craft_acid_vial",
        label="Brew Acid Vial",
        category="crafting",
        required_items={"sulfur_dust": 1, "salt_crust": 1, "empty_flask": 1},
        produced_item="acid_vial",
        produced_quantity=1,
        stamina_cost=0,
        result_text="You mix sulfur dust and caustic mineral salts in the glass vial.",
        log_event="You brewed a vial of acid.",
    ),
    "fire_striker": CraftingRecipe(
        id="fire_striker",
        action_id="craft_fire_striker",
        label="Craft Striker",
        category="crafting",
        required_items={"flint": 1, "scrap_metal": 1},
        produced_item="fire_striker",
        produced_quantity=1,
        stamina_cost=0,
        result_text="You chip the flint edge against steel to form a fire striker.",
        log_event="You crafted a fire striker.",
    ),
}


def get_crafting_recipes() -> Dict[str, CraftingRecipe]:
    """Return all available crafting recipes."""
    return dict(CRAFTING_RECIPES)
