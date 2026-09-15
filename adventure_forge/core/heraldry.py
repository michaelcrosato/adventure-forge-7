"""Milestone 27: Provincial Faction Heraldry, Renown Orders & Continental War Banners System.

Provides 5 Provincial Renown Orders situated at regional council chambers,
7-axis fealty pledges yielding provincial War Banners, dynamic banner display affordances,
central crossroads rallies, and Grandmaster of the Five Realms rank progression.
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class FactionOrder:
    """A prestigious provincial order with dedicated sanctum, heraldic banner, and renown oath."""
    id: str
    name: str
    province: str
    sanctum_scene: str
    faction_key: str
    banner_item_id: str
    banner_name: str
    crest_icon: str
    reputation_req: int
    alternate_attribute: str
    alternate_attr_val: int
    alternate_trait: str
    description: str
    pledge_action_id: str
    pledge_action_label: str   # Exactly 1 to 3 words
    pledge_result_text: str
    raise_action_id: str
    raise_action_label: str    # Exactly 1 to 3 words
    raise_result_text: str
    granted_marker: str

    def to_dict(
        self,
        is_pledged: bool = False,
        has_banner: bool = False,
        is_raised: bool = False
    ) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "province": self.province,
            "sanctum_scene": self.sanctum_scene,
            "faction_key": self.faction_key,
            "banner_item_id": self.banner_item_id,
            "banner_name": self.banner_name,
            "crest_icon": self.crest_icon,
            "reputation_req": self.reputation_req,
            "alternate_attribute": self.alternate_attribute,
            "alternate_attr_val": self.alternate_attr_val,
            "alternate_trait": self.alternate_trait,
            "description": self.description,
            "pledge_action_id": self.pledge_action_id,
            "pledge_action_label": self.pledge_action_label,
            "raise_action_id": self.raise_action_id,
            "raise_action_label": self.raise_action_label,
            "granted_marker": self.granted_marker,
            "is_pledged": is_pledged,
            "has_banner": has_banner,
            "is_raised": is_raised,
        }


FACTION_ORDERS: Dict[str, FactionOrder] = {
    "order_iron_peak": FactionOrder(
        id="order_iron_peak",
        name="Order of the Iron Peak",
        province="The Reach",
        sanctum_scene="reach_bastion_redoubt_chamber",
        faction_key="iron_guard",
        banner_item_id="item_banner_iron_peak",
        banner_name="Iron Peak War Banner",
        crest_icon="⛰️",
        reputation_req=5,
        alternate_attribute="strength",
        alternate_attr_val=14,
        alternate_trait="iron_gutted",
        description="Highland vanguard order sworn to stone bastions and mountain pass defense.",
        pledge_action_id="order_pledge_iron_peak",
        pledge_action_label="Pledge Iron Order",
        pledge_result_text="The bastion commander strikes an iron anvil. You take the oath and claim the highland banner.",
        raise_action_id="heraldry_raise_iron_peak",
        raise_action_label="Raise Iron Banner",
        raise_result_text="You plant the heavy iron banner in the stone. Mountain courage fills your limbs.",
        granted_marker="marker_banner_iron_valor",
    ),
    "order_sunfire_sands": FactionOrder(
        id="order_sunfire_sands",
        name="Order of the Sunfire Sands",
        province="The Scorchwaste",
        sanctum_scene="scorchwaste_canyon_oasis_chamber",
        faction_key="dune_nomads",
        banner_item_id="item_banner_sunfire_sands",
        banner_name="Sunfire Nomad Banner",
        crest_icon="☀️",
        reputation_req=5,
        alternate_attribute="endurance",
        alternate_attr_val=14,
        alternate_trait="sun_touched",
        description="Desert scout order sworn to dune caravans and secret oasis wells.",
        pledge_action_id="order_pledge_sunfire_sands",
        pledge_action_label="Pledge Nomad Order",
        pledge_result_text="The nomad elder touches your brow with ash. You take the oath and claim the desert banner.",
        raise_action_id="heraldry_raise_sunfire_sands",
        raise_action_label="Raise Nomad Banner",
        raise_result_text="You unfurl the sunfire banner against the dry wind. Desert endurance cools your blood.",
        granted_marker="marker_banner_desert_resilience",
    ),
    "order_salted_river": FactionOrder(
        id="order_salted_river",
        name="Order of the Salted River",
        province="The Lowlands",
        sanctum_scene="lowlands_canal_sluice_chamber",
        faction_key="river_guild",
        banner_item_id="item_banner_salted_river",
        banner_name="Salted River War Banner",
        crest_icon="⚓",
        reputation_req=5,
        alternate_attribute="agility",
        alternate_attr_val=14,
        alternate_trait="shadow_born",
        description="Canal river order sworn to barge waterways and marsh smuggler trade.",
        pledge_action_id="order_pledge_salted_river",
        pledge_action_label="Pledge River Order",
        pledge_result_text="The canal guildmaster signs the parchment scroll. You take the oath and claim the river banner.",
        raise_action_id="heraldry_raise_salted_river",
        raise_action_label="Raise River Banner",
        raise_result_text="You raise the salted river banner above your head. Sharp canal wits guide your blade.",
        granted_marker="marker_banner_river_cunning",
    ),
    "order_gilded_rose": FactionOrder(
        id="order_gilded_rose",
        name="Order of the Gilded Rose",
        province="The High Court",
        sanctum_scene="high_court_chancellor_court_chamber",
        faction_key="high_court",
        banner_item_id="item_banner_gilded_rose",
        banner_name="Gilded Rose Imperial Banner",
        crest_icon="🌹",
        reputation_req=5,
        alternate_attribute="presence",
        alternate_attr_val=14,
        alternate_trait="silver_tongue",
        description="Imperial noble order sworn to grand chambers and royal decrees.",
        pledge_action_id="order_pledge_gilded_rose",
        pledge_action_label="Pledge Court Order",
        pledge_result_text="The grand chancellor presents a royal seal. You take the oath and claim the gilded rose banner.",
        raise_action_id="heraldry_raise_gilded_rose",
        raise_action_label="Raise Court Banner",
        raise_result_text="You raise the gilded rose banner high. Sovereign authority stills hostile eyes.",
        granted_marker="marker_banner_court_prestige",
    ),
    "order_abyssal_trench": FactionOrder(
        id="order_abyssal_trench",
        name="Order of the Abyssal Trench",
        province="The Sunken Hollows",
        sanctum_scene="sunken_hollows_deep_siphon_chamber",
        faction_key="deep_delvers",
        banner_item_id="item_banner_abyssal_trench",
        banner_name="Abyssal Trench War Banner",
        crest_icon="🔱",
        reputation_req=5,
        alternate_attribute="willpower",
        alternate_attr_val=14,
        alternate_trait="abyssal_lung",
        description="Abyssal diving order sworn to deep ocean trenches and sunken vault depths.",
        pledge_action_id="order_pledge_abyssal_trench",
        pledge_action_label="Pledge Trench Order",
        pledge_result_text="The chief diver pours sea water upon your boots. You take the oath and claim the abyssal banner.",
        raise_action_id="heraldry_raise_abyssal_trench",
        raise_action_label="Raise Trench Banner",
        raise_result_text="You plant the abyssal trench banner into the ground. Subterranean resolve fortifies your lungs.",
        granted_marker="marker_banner_abyssal_daring",
    ),
}

BANNER_ITEM_TO_ORDER: Dict[str, FactionOrder] = {
    o.banner_item_id: o for o in FACTION_ORDERS.values()
}


def evaluate_orders_progress(
    world_flags: Dict[str, Any],
    inventory: Any = None,
    markers: Any = None
) -> Dict[str, Any]:
    """Compute faction pledges, war banners held, active banner buffs, and marshal rank."""
    inv_list: List[str] = []
    if isinstance(inventory, (list, tuple)):
        inv_list = [str(i).lower() for i in inventory]
    elif isinstance(inventory, (set, dict)):
        inv_list = [str(k).lower() for k in inventory]

    marker_list: List[str] = []
    if isinstance(markers, (list, tuple)):
        marker_list = [str(m).lower() for m in markers]
    elif isinstance(markers, (set, dict)):
        marker_list = [str(k).lower() for k in markers]

    pledged_count = sum(1 for o_id in FACTION_ORDERS if world_flags.get(f"heraldry_pledged_{o_id}"))
    banners_held = sum(1 for o in FACTION_ORDERS.values() if o.banner_item_id.lower() in inv_list)

    if banners_held >= 5:
        rank_title = "👑 Grandmaster of the Five Realms"
    elif banners_held >= 4:
        rank_title = "⚔️ High Faction Marshal"
    elif banners_held >= 3:
        rank_title = "🛡️ Continental Commander"
    elif banners_held >= 2:
        rank_title = "🚩 Provincial Banneret"
    elif banners_held >= 1:
        rank_title = "🗡️ Order Knight-Errant"
    else:
        rank_title = "Unsworn Wayfarer"

    active_banner_marker = None
    for o in FACTION_ORDERS.values():
        if o.granted_marker.lower() in marker_list:
            active_banner_marker = o.granted_marker
            break

    orders_status = {}
    for o_id, o in FACTION_ORDERS.items():
        is_pledged = bool(world_flags.get(f"heraldry_pledged_{o_id}"))
        has_b = o.banner_item_id.lower() in inv_list
        is_raised = o.granted_marker.lower() in marker_list
        orders_status[o_id] = o.to_dict(
            is_pledged=is_pledged,
            has_banner=has_b,
            is_raised=is_raised,
        )

    return {
        "pledged_count": pledged_count,
        "total_orders": len(FACTION_ORDERS),
        "banners_held": banners_held,
        "rank_title": rank_title,
        "is_knight": banners_held >= 1,
        "is_commander": banners_held >= 3,
        "is_grandmaster": banners_held >= 5,
        "active_banner_marker": active_banner_marker,
        "orders": orders_status,
    }


def get_heraldry_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic heraldry affordances (Pledge Order, Raise Banner, Rally Banners)."""
    from adventure_forge.core.actions import Action
    actions: List[Action] = []

    # Defensive inventory resolution
    inv_list: List[str] = []
    if isinstance(character.inventory, (list, tuple)):
        inv_list = [str(i).lower() for i in character.inventory]
    elif isinstance(character.inventory, (set, dict)):
        inv_list = [str(k).lower() for k in character.inventory]

    # Defensive marker resolution
    marker_list: List[str] = []
    if isinstance(character.markers, (list, tuple)):
        marker_list = [str(m).lower() for m in character.markers]
    elif isinstance(character.markers, (set, dict)):
        marker_list = [str(k).lower() for k in character.markers]

    # 1. Pledge Fealty in Sanctum Scenes
    for order in FACTION_ORDERS.values():
        if scene_id == order.sanctum_scene:
            is_pledged = bool(world_flags.get(f"heraldry_pledged_{order.id}"))
            has_banner = order.banner_item_id.lower() in inv_list
            if not is_pledged and not has_banner:
                # 7-Axis qualification check
                rep = character.get_reputation(order.faction_key)
                attr_val = character.get_attribute(order.alternate_attribute)
                has_t = character.has_trait(order.alternate_trait)

                if rep >= order.reputation_req or attr_val >= order.alternate_attr_val or has_t:
                    actions.append(Action(
                        id=order.pledge_action_id,
                        label=order.pledge_action_label,
                        category="social",
                        effects=[
                            {"set_flag": {"flag": f"heraldry_pledged_{order.id}", "value": True}},
                            {"add_item": order.banner_item_id},
                            {"modify_reputation": {"faction": order.faction_key, "value": 5}},
                            {"log_event": f"Sworn to the {order.name} and received {order.banner_name}."},
                        ],
                        result_text=order.pledge_result_text,
                        risk="low",
                        stamina_cost=0,
                    ))

    # 2. Raise Held War Banners in the field
    for item in inv_list:
        if item in BANNER_ITEM_TO_ORDER:
            order = BANNER_ITEM_TO_ORDER[item]
            if order.granted_marker.lower() not in marker_list:
                actions.append(Action(
                    id=order.raise_action_id,
                    label=order.raise_action_label,
                    category="systemic",
                    effects=[
                        {"add_marker": order.granted_marker},
                        {"modify_stamina": 3},
                        {"log_event": f"Raised the {order.banner_name} in honor of the {order.name}."},
                    ],
                    result_text=order.raise_result_text,
                    risk="low",
                    stamina_cost=0,
                ))

    # 3. Central Bazaar Heraldic Rally
    if scene_id == "bazaar_center":
        held_banners_count = sum(1 for item in inv_list if item in BANNER_ITEM_TO_ORDER)
        has_rallied = bool(world_flags.get("heraldry_rallied_bazaar"))
        if held_banners_count >= 1 and not has_rallied:
            actions.append(Action(
                id="heraldry_rally_banners",
                label="Rally Order Banners",
                category="social",
                effects=[
                    {"set_flag": {"flag": "heraldry_rallied_bazaar", "value": True}},
                    {"modify_stamina": 5},
                    {"log_event": "Assembled provincial banners at the Crossroads. Crowds celebrated your renown."},
                ],
                result_text="You unfurl the gathered provincial war banners before the crossroads assembly. The crowds cheer your renown.",
                risk="low",
                stamina_cost=0,
            ))

    return actions
