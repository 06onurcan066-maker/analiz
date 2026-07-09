import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

HEADERS = {
    "x-apisports-key": settings.api_football_key,
    "Accept": "application/json",
}

async def fetch_fixtures(league: Optional[int] = None, season: Optional[int] = None, date: Optional[str] = None) -> Dict[str, Any]:
    url = f"{settings.api_football_base}/fixtures"
    params = {}
    if league:
        params["league"] = league
    if season:
        params["season"] = season
    if date:
        params["date"] = date

    async with httpx.AsyncClient(timeout=10.0, headers=HEADERS) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

async def fetch_fixture_by_id(fixture_id: int) -> Dict[str, Any]:
    url = f"{settings.api_football_base}/fixtures"
    params = {"id": fixture_id}
    async with httpx.AsyncClient(timeout=10.0, headers=HEADERS) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
