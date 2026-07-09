from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TeamStats(BaseModel):
    team_id: Optional[str]
    team_name: Optional[str]
    avg_goals_for_home: float = Field(..., description="Takımın iç saha başına ortalama gol")
    avg_goals_against_home: float = Field(..., description="Takımın iç saha başına ortalama yediği gol")
    avg_goals_for_away: Optional[float] = None
    avg_goals_against_away: Optional[float] = None

class LeagueAverages(BaseModel):
    league_avg_home_goals: float
    league_avg_away_goals: float

class OddsEntry(BaseModel):
    provider: str
    market: str
    selection: str
    price: float
    is_live: Optional[bool] = False

class SimulationRequest(BaseModel):
    match_id: Optional[str]
    home: TeamStats
    away: TeamStats
    league: LeagueAverages
    odds: List[OddsEntry] = []
    n_simulations: Optional[int] = 10000

class TopScore(BaseModel):
    score: str
    frequency: float

class SimulationResult(BaseModel):
    match_id: Optional[str]
    n_simulations: int
    lambda_home: float
    lambda_away: float
    prob_home_win: float
    prob_draw: float
    prob_away_win: float
    top_scores: List[TopScore]
    totals_over_under: Dict[str, float]
    both_teams_score: float
    value_bets: List[Dict]
    surebets: List[Dict]
    runtime_seconds: float
    run_at: datetime
