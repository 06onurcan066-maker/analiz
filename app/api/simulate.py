from fastapi import APIRouter, HTTPException
from app.schemas import SimulationRequest, SimulationResult
from app.core.math_engine import estimate_lambdas, run_monte_carlo_async
from app.services.odds_utils import compute_value_bets, detect_surebets
from datetime import datetime

router = APIRouter()

@router.post("/simulate", response_model=SimulationResult)
async def simulate_endpoint(req: SimulationRequest):
    # Estimate lambdas
    λ_home, λ_away = estimate_lambdas(
        home_avg_scored=req.home.avg_goals_for_home,
        away_avg_scored=req.away.avg_goals_for_home if req.away.avg_goals_for_home is not None else req.away.avg_goals_for_away or 0.0,
        league_avg_home_goals=req.league.league_avg_home_goals,
        league_avg_away_goals=req.league.league_avg_away_goals,
        home_defense_factor=1.0,
        away_defense_factor=1.0
    )

    start = datetime.utcnow()
    mc = await run_monte_carlo_async(λ_home, λ_away, n_simulations=req.n_simulations or 10000)
    runtime = mc.get("runtime_seconds", 0.0)

    sim_probs = {
        "home": mc["prob_home_win"],
        "draw": mc["prob_draw"],
        "away": mc["prob_away_win"],
    }
    for t, prob_over in mc["totals_over_under"].items():
        key_over = f"over_{t.replace('.','_')}"
        key_under = f"under_{t.replace('.','_')}"
        sim_probs[key_over] = prob_over
        sim_probs[key_under] = 1.0 - prob_over

    sim_probs["both_teams_score"] = mc["both_teams_score"]

    odds_list = [o.dict() for o in req.odds] if hasattr(req, "odds") else []
    value_bets = compute_value_bets(sim_probs, odds_list)
    surebets = detect_surebets(odds_list)

    result = {
        "match_id": req.match_id,
        "n_simulations": mc["n_simulations"],
        "lambda_home": mc["lambda_home"],
        "lambda_away": mc["lambda_away"],
        "prob_home_win": mc["prob_home_win"],
        "prob_draw": mc["prob_draw"],
        "prob_away_win": mc["prob_away_win"],
        "top_scores": mc["top_scores"],
        "totals_over_under": mc["totals_over_under"],
        "both_teams_score": mc["both_teams_score"],
        "value_bets": value_bets,
        "surebets": surebets,
        "runtime_seconds": runtime,
        "run_at": datetime.utcnow()
    }
    return result
