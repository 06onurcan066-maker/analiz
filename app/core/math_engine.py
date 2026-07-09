import numpy as np
import time
from typing import Tuple, Dict, List
from collections import Counter
import asyncio
from datetime import datetime

def estimate_lambdas(
    home_avg_scored: float,
    away_avg_scored: float,
    league_avg_home_goals: float,
    league_avg_away_goals: float,
    home_defense_factor: float = 1.0,
    away_defense_factor: float = 1.0,
) -> Tuple[float, float]:
    att_home = home_avg_scored / max(1e-6, league_avg_home_goals)
    att_away = away_avg_scored / max(1e-6, league_avg_away_goals)

    λ_home = league_avg_home_goals * att_home * away_defense_factor
    λ_away = league_avg_away_goals * att_away * home_defense_factor

    return float(λ_home), float(λ_away)


def _run_monte_carlo_sync(lambda_home: float, lambda_away: float, n_simulations: int = 10000, minutes: int = 90, rng_seed: int = None) -> Dict:
    start = time.time()
    rng = np.random.default_rng(rng_seed)

    p_home_min = lambda_home / float(minutes)
    p_away_min = lambda_away / float(minutes)

    p_home_min = max(0.0, min(1.0, p_home_min))
    p_away_min = max(0.0, min(1.0, p_away_min))

    home_goals_matrix = rng.binomial(1, p_home_min, size=(n_simulations, minutes))
    away_goals_matrix = rng.binomial(1, p_away_min, size=(n_simulations, minutes))

    home_goals = home_goals_matrix.sum(axis=1)
    away_goals = away_goals_matrix.sum(axis=1)
    totals = home_goals + away_goals

    home_wins = np.sum(home_goals > away_goals) / n_simulations
    draws = np.sum(home_goals == away_goals) / n_simulations
    away_wins = np.sum(home_goals < away_goals) / n_simulations

    pairs = list(zip(home_goals.tolist(), away_goals.tolist()))
    cnt = Counter(pairs)
    top3 = cnt.most_common(3)
    top_scores = [{"score": f"{h}-{a}", "frequency": freq / n_simulations} for (h, a), freq in top3]

    thresholds = [1.5, 2.5, 3.5]
    totals_dict = {}
    for t in thresholds:
        totals_dict[str(t)] = float(np.sum(totals > t) / n_simulations)

    both_score_prob = float(np.sum((home_goals > 0) & (away_goals > 0)) / n_simulations)

    runtime = time.time() - start
    return {
        "n_simulations": n_simulations,
        "lambda_home": lambda_home,
        "lambda_away": lambda_away,
        "prob_home_win": float(home_wins),
        "prob_draw": float(draws),
        "prob_away_win": float(away_wins),
        "top_scores": top_scores,
        "totals_over_under": totals_dict,
        "both_teams_score": both_score_prob,
        "runtime_seconds": runtime,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

async def run_monte_carlo_async(lambda_home: float, lambda_away: float, n_simulations: int = 10000, minutes: int = 90, rng_seed: int = None) -> Dict:
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, _run_monte_carlo_sync, lambda_home, lambda_away, n_simulations, minutes, rng_seed)
    return result
