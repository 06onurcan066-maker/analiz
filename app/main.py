from fastapi import FastAPI
from app.api.simulate import router as simulate_router
from app.api.football import router as football_router

app = FastAPI(title="Dynamic Bet & Score Analytics Engine - Core API", version="0.1.0")

app.include_router(simulate_router, prefix="/api")
app.include_router(football_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}
