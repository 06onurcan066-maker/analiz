from fastapi import APIRouter, HTTPException
from typing import Optional
from app.services.api_football import fetch_fixtures, fetch_fixture_by_id

router = APIRouter()

@router.get("/external/fixtures")
async def get_fixtures(league: Optional[int] = None, season: Optional[int] = None, date: Optional[str] = None):
    try:
        data = await fetch_fixtures(league=league, season=season, date=date)
        return data
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@router.get("/external/fixture/{fixture_id}")
async def get_fixture(fixture_id: int):
    try:
        data = await fetch_fixture_by_id(fixture_id)
        return data
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
