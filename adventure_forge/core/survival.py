"""Milestone 26: Continental Survival Camping, Wilderness Foraging & Field Rations System.

Provides 15 wilderness foraging sites (3 per province across 5 provinces),
6 regional campsites and hearths, 6 survival cooking recipes (5 provincial + 1 Grand Feast),
and field consumption affordances with stamina recovery and regional markers.
"""
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class ForagingSpot:
    """A provincial wilderness location where edible ingredients can be gathered."""
    scene_id: str
    ingredient_id: str
    ingredient_name: str
    province: str
    action_id: str
    action_label: str       # Exactly 1 to 3 words
    result_text: str

    def to_dict(self, is_foraged: bool = False) -> Dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "ingredient_id": self.ingredient_id,
            "ingredient_name": self.ingredient_name,
            "province": self.province,
            "action_id": self.action_id,
            "action_label": self.action_label,
            "is_foraged": is_foraged,
        }


@dataclass(frozen=True)
class CookingRecipe:
    """A field recipe cooked at campsites and consumed anywhere for nourishment."""
    id: str
    name: str
    province: str
    cooked_item_id: str
    required_ingredients: List[str]
    cook_action_id: str
    cook_action_label: str   # Exactly 1 to 3 words
    cook_result_text: str
    eat_action_id: str
    eat_action_label: str    # Exactly 1 to 3 words
    eat_result_text: str
    stamina_restored: int
    health_restored: int
    granted_marker: Optional[str]
    description: str

    def to_dict(self, can_cook: bool = False, count_held: int = 0) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "cooked_item_id": self.cooked_item_id,
            "required_ingredients": list(self.required_ingredients),
            "cook_action_id": self.cook_action_id,
            "cook_action_label": self.cook_action_label,
            "eat_action_id": self.eat_action_id,
            "eat_action_label": self.eat_action_label,
            "stamina_restored": self.stamina_restored,
            "health_restored": self.health_restored,
            "granted_marker": self.granted_marker,
            "description": self.description,
            "can_cook": can_cook,
            "count_held": count_held,
        }


# --- 15 Provincial Wilderness Foraging Sites (3 per Province) ---

FORAGING_SPOTS: Dict[str, ForagingSpot] = {
    # 1. The Reach
    "reach_high_pass_gate": ForagingSpot(
        scene_id="reach_high_pass_gate",
        ingredient_id="foraged_frost_lichen",
        ingredient_name="Alpine Frost Lichen",
        province="The Reach",
        action_id="survival_forage_high_pass",
        action_label="Forage Lichen",
        result_text="You scrape crisp frost lichen from the stone crevasse. The mountain herb smells of pine needles.",
    ),
    "reach_frost_cavern_gate": ForagingSpot(
        scene_id="reach_frost_cavern_gate",
        ingredient_id="foraged_frost_lichen",
        ingredient_name="Alpine Frost Lichen",
        province="The Reach",
        action_id="survival_forage_frost_cavern",
        action_label="Forage Lichen",
        result_text="You scrape crisp frost lichen from the stone crevasse. The mountain herb smells of pine needles.",
    ),
    "reach_wind_hollow_gate": ForagingSpot(
        scene_id="reach_wind_hollow_gate",
        ingredient_id="foraged_frost_lichen",
        ingredient_name="Alpine Frost Lichen",
        province="The Reach",
        action_id="survival_forage_wind_hollow",
        action_label="Forage Lichen",
        result_text="You scrape crisp frost lichen from the stone crevasse. The mountain herb smells of pine needles.",
    ),

    # 2. The Scorchwaste
    "scorchwaste_canyon_oasis_gate": ForagingSpot(
        scene_id="scorchwaste_canyon_oasis_gate",
        ingredient_id="foraged_dune_succulent",
        ingredient_name="Dune Water-Succulent",
        province="The Scorchwaste",
        action_id="survival_forage_canyon_oasis",
        action_label="Forage Succulents",
        result_text="You harvest thick water succulents from the damp sand. Cool moisture beads upon your knife blade.",
    ),
    "scorchwaste_nomad_well_gate": ForagingSpot(
        scene_id="scorchwaste_nomad_well_gate",
        ingredient_id="foraged_dune_succulent",
        ingredient_name="Dune Water-Succulent",
        province="The Scorchwaste",
        action_id="survival_forage_nomad_well",
        action_label="Forage Succulents",
        result_text="You harvest thick water succulents from the damp sand. Cool moisture beads upon your knife blade.",
    ),
    "scorchwaste_dune_ridge_gate": ForagingSpot(
        scene_id="scorchwaste_dune_ridge_gate",
        ingredient_id="foraged_dune_succulent",
        ingredient_name="Dune Water-Succulent",
        province="The Scorchwaste",
        action_id="survival_forage_dune_ridge",
        action_label="Forage Succulents",
        result_text="You harvest thick water succulents from the damp sand. Cool moisture beads upon your knife blade.",
    ),

    # 3. The Lowlands
    "lowlands_smuggler_cove_gate": ForagingSpot(
        scene_id="lowlands_smuggler_cove_gate",
        ingredient_id="foraged_marsh_parsley",
        ingredient_name="Marsh Reed-Parsley",
        province="The Lowlands",
        action_id="survival_forage_smuggler_cove",
        action_label="Forage Parsley",
        result_text="You pluck wild marsh parsley from the river bank. The pungent herb refreshes your senses.",
    ),
    "lowlands_canal_sluice_gate": ForagingSpot(
        scene_id="lowlands_canal_sluice_gate",
        ingredient_id="foraged_marsh_parsley",
        ingredient_name="Marsh Reed-Parsley",
        province="The Lowlands",
        action_id="survival_forage_canal_sluice",
        action_label="Forage Parsley",
        result_text="You pluck wild marsh parsley from the river bank. The pungent herb refreshes your senses.",
    ),
    "lowlands_potters_quay_gate": ForagingSpot(
        scene_id="lowlands_potters_quay_gate",
        ingredient_id="foraged_marsh_parsley",
        ingredient_name="Marsh Reed-Parsley",
        province="The Lowlands",
        action_id="survival_forage_potters_quay",
        action_label="Forage Parsley",
        result_text="You pluck wild marsh parsley from the river bank. The pungent herb refreshes your senses.",
    ),

    # 4. The High Court
    "high_court_grand_basilica_gate": ForagingSpot(
        scene_id="high_court_grand_basilica_gate",
        ingredient_id="foraged_royal_truffle",
        ingredient_name="Gilded Royal Truffle",
        province="The High Court",
        action_id="survival_forage_grand_basilica",
        action_label="Forage Truffles",
        result_text="You unearth a dark royal truffle near the ancient oaks. Rich aromas rise from the damp loam.",
    ),
    "high_court_royal_archive_gate": ForagingSpot(
        scene_id="high_court_royal_archive_gate",
        ingredient_id="foraged_royal_truffle",
        ingredient_name="Gilded Royal Truffle",
        province="The High Court",
        action_id="survival_forage_royal_archive",
        action_label="Forage Truffles",
        result_text="You unearth a dark royal truffle near the ancient oaks. Rich aromas rise from the damp loam.",
    ),
    "high_court_catacomb_kings_gate": ForagingSpot(
        scene_id="high_court_catacomb_kings_gate",
        ingredient_id="foraged_royal_truffle",
        ingredient_name="Gilded Royal Truffle",
        province="The High Court",
        action_id="survival_forage_catacomb_kings",
        action_label="Forage Truffles",
        result_text="You unearth a dark royal truffle near the ancient oaks. Rich aromas rise from the damp loam.",
    ),

    # 5. The Sunken Hollows
    "sunken_hollows_fungal_forest_gate": ForagingSpot(
        scene_id="sunken_hollows_fungal_forest_gate",
        ingredient_id="foraged_glow_mushroom",
        ingredient_name="Bioluminescent Cave Cap",
        province="The Sunken Hollows",
        action_id="survival_forage_fungal_forest",
        action_label="Forage Mushrooms",
        result_text="You gather glowing blue mushrooms from the cave wall. Soft phosphorescence illuminates your fingers.",
    ),
    "sunken_hollows_glow_grotto_gate": ForagingSpot(
        scene_id="sunken_hollows_glow_grotto_gate",
        ingredient_id="foraged_glow_mushroom",
        ingredient_name="Bioluminescent Cave Cap",
        province="The Sunken Hollows",
        action_id="survival_forage_glow_grotto",
        action_label="Forage Mushrooms",
        result_text="You gather glowing blue mushrooms from the cave wall. Soft phosphorescence illuminates your fingers.",
    ),
    "sunken_hollows_coral_chasm_gate": ForagingSpot(
        scene_id="sunken_hollows_coral_chasm_gate",
        ingredient_id="foraged_glow_mushroom",
        ingredient_name="Bioluminescent Cave Cap",
        province="The Sunken Hollows",
        action_id="survival_forage_coral_chasm",
        action_label="Forage Mushrooms",
        result_text="You gather glowing blue mushrooms from the cave wall. Soft phosphorescence illuminates your fingers.",
    ),
}

# --- 6 Regional Campsite Rest & Hearth Scenes ---

CAMPSITE_SCENES: Dict[str, str] = {
    "reach_timber_camp_quarters": "The Reach (Highland Timber Camp)",
    "scorchwaste_canyon_oasis_quarters": "The Scorchwaste (Hidden Oasis Hearth)",
    "lowlands_dock_tavern_quarters": "The Lowlands (Anchor Inn Hearth)",
    "high_court_knight_barracks_quarters": "The High Court (Palatine Armory Hearth)",
    "sunken_hollows_glow_grotto_quarters": "The Sunken Hollows (Glowstone Grotto Hearth)",
    "bazaar_center": "Central Crossroads (Wayfarer Hearth)",
}

# --- 6 Survival Field Cooking Recipes ---

COOKING_RECIPES: Dict[str, CookingRecipe] = {
    "highland_stew": CookingRecipe(
        id="highland_stew",
        name="Highland Frost Stew",
        province="The Reach",
        cooked_item_id="item_highland_stew",
        required_ingredients=["foraged_frost_lichen"],
        cook_action_id="survival_cook_highland_stew",
        cook_action_label="Cook Highland Stew",
        cook_result_text="You simmer the frost lichen into a hearty broth. Thick steam warms your weathered face.",
        eat_action_id="survival_eat_highland_stew",
        eat_action_label="Eat Highland Stew",
        eat_result_text="You eat the steaming mountain stew. Warmth spreads through cold limbs.",
        stamina_restored=8,
        health_restored=3,
        granted_marker="marker_mountain_warmth",
        description="Warm mountain broth that shields against freezing alpine gales.",
    ),
    "dune_jerky": CookingRecipe(
        id="dune_jerky",
        name="Sunfire Cured Jerky",
        province="The Scorchwaste",
        cooked_item_id="item_dune_jerky",
        required_ingredients=["foraged_dune_succulent"],
        cook_action_id="survival_cook_dune_jerky",
        cook_action_label="Cook Dune Jerky",
        cook_result_text="You smoke the succulent pulp over dry mesquite coals. The cured jerky packs firm moisture.",
        eat_action_id="survival_eat_dune_jerky",
        eat_action_label="Eat Dune Jerky",
        eat_result_text="You chew the hearty desert jerky. Cool water essence relieves your thirst.",
        stamina_restored=8,
        health_restored=3,
        granted_marker="marker_desert_hydration",
        description="Cured succulent strips that quench dehydration in scorching heat.",
    ),
    "marsh_broth": CookingRecipe(
        id="marsh_broth",
        name="Marsh Parsley Broth",
        province="The Lowlands",
        cooked_item_id="item_marsh_broth",
        required_ingredients=["foraged_marsh_parsley"],
        cook_action_id="survival_cook_marsh_broth",
        cook_action_label="Cook Marsh Broth",
        cook_result_text="You steep marsh parsley in a clay pot. Herbal vapors clear the swamp phlegm from your lungs.",
        eat_action_id="survival_eat_marsh_broth",
        eat_action_label="Eat Marsh Broth",
        eat_result_text="You drink the bitter marsh broth. Herbal medicine cleanses all bog toxins.",
        stamina_restored=8,
        health_restored=3,
        granted_marker="marker_swamp_cleansed",
        description="Bitter canal brew that cleanses bog toxins and murky sickness.",
    ),
    "royal_roast": CookingRecipe(
        id="royal_roast",
        name="Gilded Truffle Roast",
        province="The High Court",
        cooked_item_id="item_royal_roast",
        required_ingredients=["foraged_royal_truffle"],
        cook_action_id="survival_cook_royal_roast",
        cook_action_label="Cook Royal Roast",
        cook_result_text="You roast the royal truffle with salted butter. Golden crust forms across the fragrant dish.",
        eat_action_id="survival_eat_royal_roast",
        eat_action_label="Eat Royal Roast",
        eat_result_text="You savor the rich roasted truffle. Elegant flavors restore your dignity and poise.",
        stamina_restored=8,
        health_restored=3,
        granted_marker="marker_noble_satiety",
        description="Roasted truffle meal that restores royal composure.",
    ),
    "grotto_mash": CookingRecipe(
        id="grotto_mash",
        name="Luminescent Grotto Mash",
        province="The Sunken Hollows",
        cooked_item_id="item_grotto_mash",
        required_ingredients=["foraged_glow_mushroom"],
        cook_action_id="survival_cook_grotto_mash",
        cook_action_label="Cook Grotto Mash",
        cook_result_text="You crush glowing mushrooms into warm cave paste. The mash glows with gentle blue light.",
        eat_action_id="survival_eat_grotto_mash",
        eat_action_label="Eat Grotto Mash",
        eat_result_text="You swallow the glowing cave mash. Deep subterranean energy fills your chest.",
        stamina_restored=8,
        health_restored=3,
        granted_marker="marker_abyssal_vigor",
        description="Luminescent cave puree. It fortifies lung depth in water.",
    ),
    "grand_feast": CookingRecipe(
        id="grand_feast",
        name="Continental Grand Feast",
        province="Continental",
        cooked_item_id="item_grand_feast",
        required_ingredients=["foraged_frost_lichen", "foraged_dune_succulent", "foraged_marsh_parsley"],
        cook_action_id="survival_cook_grand_feast",
        cook_action_label="Cook Grand Feast",
        cook_result_text="You combine provincial delicacies into a grand kettle. Savory steam draws hungry smiles.",
        eat_action_id="survival_eat_grand_feast",
        eat_action_label="Eat Grand Feast",
        eat_result_text="You finish the grand feast. Fresh strength fills your bones.",
        stamina_restored=10,
        health_restored=10,
        granted_marker="marker_master_survivalist",
        description="A grand campfire banquet. The feast restores complete vitality.",
    ),
}

ITEM_TO_RECIPE: Dict[str, CookingRecipe] = {
    r.cooked_item_id: r for r in COOKING_RECIPES.values()
}


def evaluate_survival_progress(
    world_flags: Dict[str, Any],
    inventory: Any = None
) -> Dict[str, Any]:
    """Compute foraging counts, meals prepared, rations held, and survival rank."""
    inv_list: List[str] = []
    if isinstance(inventory, (list, tuple)):
        inv_list = [str(i).lower() for i in inventory]
    elif isinstance(inventory, (set, dict)):
        inv_list = [str(k).lower() for k in inventory]

    foraged_count = sum(1 for spot_id in FORAGING_SPOTS if world_flags.get(f"survival_foraged_{spot_id}"))
    meals_cooked = int(world_flags.get("survival_meals_cooked", 0))

    if meals_cooked >= 6:
        rank_title = "👑 Continental Master Forager"
    elif meals_cooked >= 3:
        rank_title = "🍳 Provincial Chef"
    elif meals_cooked >= 1:
        rank_title = "🏕️ Camp Cook"
    else:
        rank_title = "Trail Wanderer"

    recipes_status = {}
    for r_id, r in COOKING_RECIPES.items():
        has_all_ingredients = all(ing.lower() in inv_list for ing in r.required_ingredients)
        count_held = sum(1 for item in inv_list if item == r.cooked_item_id.lower())
        recipes_status[r_id] = r.to_dict(
            can_cook=has_all_ingredients,
            count_held=count_held,
        )

    return {
        "foraged_count": foraged_count,
        "total_spots": len(FORAGING_SPOTS),
        "meals_cooked": meals_cooked,
        "rank_title": rank_title,
        "is_cook": meals_cooked >= 1,
        "is_chef": meals_cooked >= 3,
        "is_master": meals_cooked >= 6,
        "recipes": recipes_status,
    }


def get_survival_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic survival affordances (Forage, Rest At Camp, Cook, Eat)."""
    from adventure_forge.core.actions import Action
    actions: List[Action] = []

    # Defensive inventory resolution
    inv_list: List[str] = []
    if isinstance(character.inventory, (list, tuple)):
        inv_list = [str(i).lower() for i in character.inventory]
    elif isinstance(character.inventory, (set, dict)):
        inv_list = [str(k).lower() for k in character.inventory]

    # 1. Wilderness Foraging
    spot = FORAGING_SPOTS.get(scene_id)
    if spot:
        is_foraged = bool(world_flags.get(f"survival_foraged_{scene_id}"))
        if not is_foraged:
            actions.append(Action(
                id=spot.action_id,
                label=spot.action_label,
                category="systemic",
                effects=[
                    {"set_flag": {"flag": f"survival_foraged_{scene_id}", "value": True}},
                    {"add_item": spot.ingredient_id},
                    {"log_event": f"Harvested {spot.ingredient_name} from the wild."},
                ],
                result_text=spot.result_text,
                risk="low",
                stamina_cost=0,
            ))

    # 2. Campsite Rest & Field Cooking
    if scene_id in CAMPSITE_SCENES:
        # 2a. Rest At Camp
        actions.append(Action(
            id="survival_rest_camp",
            label="Rest At Camp",
            category="systemic",
            effects=[
                {"modify_health": 5},
                {"modify_stamina": 5},
                {"log_event": "You rested by the campfire hearth and recovered vitality."},
            ],
            result_text="You stoke the embers and rest on clean wool bedrolls. Warm broth restores your strength.",
            risk="low",
            stamina_cost=0,
        ))

        # 2b. Cook Recipes
        for r in COOKING_RECIPES.values():
            has_all = all(ing.lower() in inv_list for ing in r.required_ingredients)
            if has_all:
                effects: List[Dict[str, Any]] = [
                    {"add_item": r.cooked_item_id},
                    {"add_flag": {"flag": "survival_meals_cooked", "value": 1}},
                    {"log_event": f"Prepared {r.name} over the campfire."},
                ]
                for ing in r.required_ingredients:
                    effects.append({"remove_item": ing})

                actions.append(Action(
                    id=r.cook_action_id,
                    label=r.cook_action_label,
                    category="crafting",
                    effects=effects,
                    result_text=r.cook_result_text,
                    risk="low",
                    stamina_cost=1,
                ))

    # 3. Eat Cooked Rations (Available anywhere in the world when holding item)
    seen_cooked_items = set()
    for item in inv_list:
        if item in ITEM_TO_RECIPE and item not in seen_cooked_items:
            seen_cooked_items.add(item)
            recipe = ITEM_TO_RECIPE[item]
            effects = [
                {"remove_item": recipe.cooked_item_id},
                {"modify_stamina": recipe.stamina_restored},
                {"modify_health": recipe.health_restored},
                {"log_event": f"Consumed {recipe.name} and regained vitality."},
            ]
            if recipe.granted_marker:
                effects.append({"add_marker": recipe.granted_marker})

            actions.append(Action(
                id=recipe.eat_action_id,
                label=recipe.eat_action_label,
                category="systemic",
                effects=effects,
                result_text=recipe.eat_result_text,
                risk="low",
                stamina_cost=0,
            ))

    return actions
