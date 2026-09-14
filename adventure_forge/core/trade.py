"""Continental Trade Economy & Regional Commodity Exchange (Milestone 21).

Enforces:
- 5 unique provincial trade commodities with regional supply and demand arbitrage.
- Pure deterministic trade transactions (Buy, Barter, Sell) with coin and salvage parity.
- 7-axis character reactivity (backgrounds, skills, ancestry, and reputation unlock trade privileges).
- Milestone progression: Merchant Consortium Recognition and Master Trader title.
- High-velocity Hemingway prose (<= 18 words/sentence, 1-3 sentences, FKGL 6.0-8.0, 0 purple words).
- Strict 1-3 word UI action labels.
"""
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class Commodity:
    """A trade commodity produced in a specific province with regional price differentials."""
    id: str
    name: str
    origin_province: str
    origin_scene: str
    description: str
    base_buy_price: int  # in silver_coin
    base_sell_price: int  # in silver_coin
    import_bonuses: Dict[str, int]  # destination scene_id -> bonus coins paid on sell
    barter_item: str  # alternative item accepted for purchase without coin
    buy_result_text: str
    sell_result_text: str


COMMODITIES: Dict[str, Commodity] = {
    "iron_ore": Commodity(
        id="iron_ore",
        name="Highland Iron Ore",
        origin_province="The Reach",
        origin_scene="reach_dunwall_fort_gate",
        description="Highland stone pits yield unrefined iron ore. Mountain forges trade heavy ingots across provinces.",
        base_buy_price=1,
        base_sell_price=1,
        import_bonuses={
            "lowlands_oakhaven_port_gate": 1,          # total sell price: 2
            "sunken_hollows_glow_grotto_gate": 2,      # total sell price: 3 (deep demand)
        },
        barter_item="crowbar",
        buy_result_text="You purchase heavy iron ore from the smelter. Cold metal clinks inside your pack.",
        sell_result_text="You deliver heavy iron ore to the smith. The factor counts out silver coins into your hand.",
    ),
    "bog_whiskey": Commodity(
        id="bog_whiskey",
        name="Aged Bog Whiskey",
        origin_province="The Lowlands",
        origin_scene="lowlands_oakhaven_port_gate",
        description="Lowland brewers ferment rich peat barrels. Northern outposts purchase the potent spirits for warmth.",
        base_buy_price=1,
        base_sell_price=1,
        import_bonuses={
            "reach_dunwall_fort_gate": 1,              # total sell price: 2
            "high_court_grand_basilica_gate": 2,       # total sell price: 3 (noble luxury)
        },
        barter_item="tallow",
        buy_result_text="You purchase aged bog whiskey from the distiller. The corked jug smells of rich peat.",
        sell_result_text="You deliver aged bog whiskey to the inn. The keeper counts silver coins into your hand.",
    ),
    "sunfire_spice": Commodity(
        id="sunfire_spice",
        name="Sunfire Spice",
        origin_province="The Scorchwaste",
        origin_scene="scorchwaste_ashen_gate_gate",
        description="Dune traders gather spicy red desert powders. Great kitchen halls purchase every golden chest.",
        base_buy_price=1,
        base_sell_price=1,
        import_bonuses={
            "sunken_hollows_glow_grotto_gate": 1,      # total sell price: 2
            "high_court_grand_basilica_gate": 2,       # total sell price: 3 (court banquets)
        },
        barter_item="desert_cowl",
        buy_result_text="You purchase spicy red desert powder from the caravan. Sharp dust stings your nostrils.",
        sell_result_text="You deliver spicy desert powder to the kitchen. The chef weighs the sack and pays you coins.",
    ),
    "silk_bolt": Commodity(
        id="silk_bolt",
        name="Imperial Silk Bolt",
        origin_province="The High Court",
        origin_scene="high_court_grand_basilica_gate",
        description="Palace weavers produce clean silk cloth. Mountain leaders pay silver for every bolt.",
        base_buy_price=1,
        base_sell_price=1,
        import_bonuses={
            "lowlands_oakhaven_port_gate": 1,          # total sell price: 2
            "reach_dunwall_fort_gate": 2,              # total sell price: 3 (highland chieftains)
        },
        barter_item="legal_dossier",
        buy_result_text="You purchase fine woven silk from the court tailor. Soft fabric folds inside your pack.",
        sell_result_text="You deliver fine woven silk to the imperial merchant. The trader weighs your cloth and pays you silver.",
    ),
    "pearl_essence": Commodity(
        id="pearl_essence",
        name="Abyssal Pearl Essence",
        origin_province="The Sunken Hollows",
        origin_scene="sunken_hollows_glow_grotto_gate",
        description="Deep divers collect glowing sea oysters. City doctors pay silver for distilled fluids.",
        base_buy_price=1,
        base_sell_price=1,
        import_bonuses={
            "scorchwaste_ashen_gate_gate": 1,          # total sell price: 2
            "high_court_grand_basilica_gate": 2,       # total sell price: 3 (noble longevity)
        },
        barter_item="pitch_seal",
        buy_result_text="You purchase glowing pearl extract from the harbor diver. Cold glass rattles in your pouch.",
        sell_result_text="You deliver ocean pearl extract to the harbor chemist. The trader pays you silver coins.",
    ),
}

# Trade hubs: Central crossroads (all commodities available) + 5 provincial gateway fortresses
TRADE_HUBS: Dict[str, Dict[str, Any]] = {
    "bazaar_center": {
        "hub_name": "Grand Bazaar Market",
        "factor_title": "Grand Exchange Factor",
        "available_commodities": ["iron_ore", "bog_whiskey", "sunfire_spice", "silk_bolt", "pearl_essence"],
    },
    "reach_dunwall_fort_gate": {
        "hub_name": "Dunwall Foundry Gate",
        "factor_title": "Highland Ore Factor",
        "available_commodities": ["iron_ore"],
    },
    "lowlands_oakhaven_port_gate": {
        "hub_name": "Oakhaven Canal Docks",
        "factor_title": "Canal Spirit Merchant",
        "available_commodities": ["bog_whiskey"],
    },
    "scorchwaste_ashen_gate_gate": {
        "hub_name": "Ashen Gate Oasis",
        "factor_title": "Dune Spice Caravaneer",
        "available_commodities": ["sunfire_spice"],
    },
    "high_court_grand_basilica_gate": {
        "hub_name": "Grand Basilica Concourse",
        "factor_title": "Imperial Draper Factor",
        "available_commodities": ["silk_bolt"],
    },
    "sunken_hollows_glow_grotto_gate": {
        "hub_name": "Glow Grotto Quay",
        "factor_title": "Abyssal Pearl Factor",
        "available_commodities": ["pearl_essence"],
    },
}

COMMODITY_LABELS: Dict[str, Dict[str, str]] = {
    "iron_ore": {
        "buy": "Buy Iron Ore",
        "barter": "Barter Iron Ore",
        "sell": "Sell Iron Ore",
    },
    "bog_whiskey": {
        "buy": "Buy Bog Whiskey",
        "barter": "Barter Bog Whiskey",
        "sell": "Sell Bog Whiskey",
    },
    "sunfire_spice": {
        "buy": "Buy Sunfire Spice",
        "barter": "Barter Sunfire Spice",
        "sell": "Sell Sunfire Spice",
    },
    "silk_bolt": {
        "buy": "Buy Silk Bolt",
        "barter": "Barter Silk Bolt",
        "sell": "Sell Silk Bolt",
    },
    "pearl_essence": {
        "buy": "Buy Pearl Essence",
        "barter": "Barter Pearl Essence",
        "sell": "Sell Pearl Essence",
    },
}


def _has_clan_discount(commodity_id: str, character: CharacterSheet) -> bool:
    """Determine if character gets clan/background discounts for a commodity."""
    if commodity_id == "iron_ore":
        return (
            character.background in ("highland_scout", "Reachman")
            or character.ancestry == "Reachman"
            or character.has_marker("scout_cloak")
            or character.get_reputation("iron_guard") >= 10
        )
    elif commodity_id == "bog_whiskey":
        return (
            character.background == "cutpurse"
            or character.has_marker("thief_signet")
            or character.ancestry == "Lowlander"
            or character.get_skill("cunning") >= 3
        )
    elif commodity_id == "sunfire_spice":
        return (
            character.background == "dune_strider"
            or character.ancestry == "Nomad"
            or character.has_marker("nomad_sash")
            or character.get_reputation("desert_nomads") >= 10
        )
    elif commodity_id == "silk_bolt":
        return (
            character.background in ("noble_exile", "Noble Exile")
            or character.ancestry == "High-Kin"
            or character.has_marker("court_signet")
            or character.get_skill("rhetoric") >= 3
        )
    elif commodity_id == "pearl_essence":
        return (
            character.background == "abyssal_diver"
            or character.ancestry == "Deep-Dweller"
            or character.has_marker("abyssal_tattoos")
            or character.has_trait("water_breather")
        )
    return False


def get_trade_affordances_for_scene(
    scene_id: str,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Any]:
    """Synthesize dynamic trade affordances at recognized merchant hubs."""
    from adventure_forge.core.actions import Action

    hub_info = TRADE_HUBS.get(scene_id)
    if not hub_info:
        return []

    affordances: List[Action] = []
    available_commodities = hub_info["available_commodities"]

    # 1. Buy & Barter Affordances for commodities available at this hub
    for comm_id in available_commodities:
        comm = COMMODITIES.get(comm_id)
        if not comm:
            continue
        labels = COMMODITY_LABELS[comm_id]

        # Buy with silver coin
        has_coin = character.has_item("silver_coin")
        has_discount = _has_clan_discount(comm_id, character)

        if has_coin or has_discount:
            effects: List[Dict[str, Any]] = []
            if not has_discount:
                effects.append({"remove_item": "silver_coin"})
            effects.append({"add_item": comm_id})
            effects.append({"set_flag": {"flag": f"traded_{comm_id}", "value": True}})
            effects.append({"set_flag": {"flag": f"trade_hub_{scene_id}", "value": True}})
            effects.append({"add_flag": {"flag": "completed_trades", "value": 1}})
            effects.append({"log_event": f"You traded for {comm.name}."})

            affordances.append(Action(
                id=f"trade_buy_{comm_id}",
                label=labels["buy"],
                category="trade",
                effects=effects,
                result_text=comm.buy_result_text,
                risk="low",
                stamina_cost=0,
            ))

        # Barter with provincial salvage/tool if player lacks coins or wants to barter
        if character.has_item(comm.barter_item):
            barter_effects: List[Dict[str, Any]] = [
                {"remove_item": comm.barter_item},
                {"add_item": comm_id},
                {"set_flag": {"flag": f"traded_{comm_id}", "value": True}},
                {"set_flag": {"flag": f"trade_hub_{scene_id}", "value": True}},
                {"add_flag": {"flag": "completed_trades", "value": 1}},
                {"log_event": f"You bartered {comm.barter_item} for {comm.name}."},
            ]
            affordances.append(Action(
                id=f"trade_barter_{comm_id}",
                label=labels["barter"],
                category="trade",
                effects=barter_effects,
                result_text=comm.buy_result_text,
                risk="low",
                stamina_cost=0,
            ))

    # 2. Sell Affordances for commodities currently in player inventory
    for comm_id, comm in COMMODITIES.items():
        if character.has_item(comm_id):
            labels = COMMODITY_LABELS[comm_id]
            bonus_coins = comm.import_bonuses.get(scene_id, 0)
            total_payout = comm.base_sell_price + bonus_coins

            sell_effects: List[Dict[str, Any]] = [{"remove_item": comm_id}]
            for _ in range(total_payout):
                sell_effects.append({"add_item": "silver_coin"})

            sell_effects.append({"set_flag": {"flag": f"sold_{comm_id}", "value": True}})
            sell_effects.append({"set_flag": {"flag": f"trade_hub_{scene_id}", "value": True}})
            sell_effects.append({"add_flag": {"flag": "completed_trades", "value": 1}})

            if bonus_coins > 0:
                sell_effects.append({"add_flag": {"flag": "arbitrage_completed", "value": 1}})
                sell_effects.append({"set_flag": {"flag": f"arbitrage_{comm_id}_{scene_id}", "value": True}})
                sell_effects.append({"log_event": f"You sold {comm.name} at premium demand (+{bonus_coins} coins)."})
            else:
                sell_effects.append({"log_event": f"You sold {comm.name} to the merchant factor."})

            # Check for consortium milestone unlock
            sell_effects.append({"set_flag": {"flag": "check_merchant_milestone", "value": True}})

            affordances.append(Action(
                id=f"trade_sell_{comm_id}",
                label=labels["sell"],
                category="trade",
                effects=sell_effects,
                result_text=comm.sell_result_text,
                risk="low",
                stamina_cost=0,
            ))

    return affordances


def evaluate_trade_progress(
    world_flags: Dict[str, Any],
    inventory: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Evaluate full trade statistics, active commodity cargo, and milestone achievements."""
    inv = inventory or []
    commodities_held = [cid for cid in COMMODITIES.keys() if cid in inv]

    # Distinct trade hubs interacted with
    hubs_visited = [
        hub_id for hub_id in TRADE_HUBS.keys()
        if bool(world_flags.get(f"trade_hub_{hub_id}"))
    ]

    # Distinct commodities traded
    commodities_traded = [
        cid for cid in COMMODITIES.keys()
        if bool(world_flags.get(f"traded_{cid}")) or bool(world_flags.get(f"sold_{cid}"))
    ]

    completed_trades = int(world_flags.get("completed_trades", 0))
    arbitrage_completed = int(world_flags.get("arbitrage_completed", 0))

    # Milestones
    is_consortium_recognized = len(hubs_visited) >= 3 or bool(world_flags.get("merchant_consortium_recognized"))
    is_master_trader = (
        len(commodities_traded) >= 5
        and arbitrage_completed >= 2
    ) or bool(world_flags.get("master_trader_unlocked"))

    return {
        "commodities_held": commodities_held,
        "hubs_visited": hubs_visited,
        "hubs_visited_count": len(hubs_visited),
        "total_hubs": len(TRADE_HUBS),
        "commodities_traded": commodities_traded,
        "commodities_traded_count": len(commodities_traded),
        "completed_trades": completed_trades,
        "arbitrage_completed": arbitrage_completed,
        "is_consortium_recognized": is_consortium_recognized,
        "is_master_trader": is_master_trader,
    }
