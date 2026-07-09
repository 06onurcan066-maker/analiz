from typing import List, Dict, Tuple
from collections import defaultdict

def compute_value_bets(sim_probs: Dict[str, float], odds: List[Dict]) -> List[Dict]:
    best_odds = {}
    for o in odds:
        key = (o["market"], o["selection"])
        if key not in best_odds or o["price"] > best_odds[key]["price"]:
            best_odds[key] = {"price": o["price"], "provider": o["provider"]}

    value_bets = []
    for (market, selection), meta in best_odds.items():
        sim_key = selection
        p = sim_probs.get(sim_key)
        if p is None:
            sim_key_alt = f"{market}_{selection}"
            p = sim_probs.get(sim_key_alt)
        if p is None:
            continue
        o = float(meta["price"])
        value = (o * p) - 1.0
        entry = {
            "market": market,
            "selection": selection,
            "provider": meta["provider"],
            "price": o,
            "sim_prob": p,
            "value": value,
            "is_value": value > 0
        }
        value_bets.append(entry)
    return value_bets


def detect_surebets(odds: List[Dict]) -> List[Dict]:
    best_by_market = defaultdict(dict)
    for o in odds:
        m = o["market"]
        s = o["selection"]
        if s not in best_by_market[m] or o["price"] > best_by_market[m][s]["price"]:
            best_by_market[m][s] = {"price": o["price"], "provider": o["provider"]}

    surebets = []
    for market, selections in best_by_market.items():
        implied_sum = sum(1.0 / float(v["price"]) for v in selections.values())
        if implied_sum < 1.0:
            total_investment = 1.0
            stakes = {}
            for sel, v in selections.items():
                stakes[sel] = ( (1.0 / float(v["price"])) / implied_sum ) * total_investment
            expected_return = sum(stakes[sel] * float(v["price"]) for sel, v in selections.items()) / len(selections)
            surebets.append({
                "market": market,
                "is_surebet": True,
                "implied_sum": implied_sum,
                "best_odds": selections,
                "stakes": stakes,
                "expected_return": expected_return
            })
    return surebets
