from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.leagues_service import list_leagues, list_teams_from_league

app = FastAPI(
    title="H2H Predictor Backend",
    version="0.1.0",
    description="Backend simples em FastAPI para servir listas de ligas e times a partir de CSVs."
)

# CORS liberado (ajuste depois se quiser travar por domínio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "API H2H Predictor online",
        "routes": [
            "/leagues",
            "/leagues/{league_id}/teams",
        ],
    }


@app.get("/leagues")
async def get_leagues():
    """
    Lista todas as ligas (CSVs) disponíveis em data/leagues.
    """
    leagues = list_leagues()
    return {"leagues": leagues}


@app.get("/leagues/{league_id}/teams")
async def get_teams(league_id: str):
    """
    Lista todos os times de uma liga (com base no CSV).
    """
    teams = list_teams_from_league(league_id)
    if not teams:
        raise HTTPException(status_code=404, detail="Liga não encontrada ou sem times")
    return {"league_id": league_id, "teams": teams}
