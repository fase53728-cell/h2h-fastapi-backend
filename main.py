from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.leagues_service import (
    list_leagues,
    list_teams_from_league,
    get_team_row,
)

app = FastAPI(
    title="H2H Predictor Backend",
    version="0.2.0",
    description=(
        "Backend em FastAPI para ler CSVs por TIME dentro de pastas de ligas "
        "e servir dados para o painel H2H."
    ),
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
        "mode": "csv_por_time",
        "routes": [
            "/leagues",
            "/leagues/{league_id}/teams",
            "/leagues/{league_id}/team/{team_id}",
        ],
    }


@app.get("/leagues")
async def get_leagues():
    """
    Lista todas as ligas disponíveis (pastas dentro de data/leagues).
    """
    leagues = list_leagues()
    return {"leagues": leagues}


@app.get("/leagues/{league_id}/teams")
async def get_teams(league_id: str):
    """
    Lista todos os times de uma liga (com base nos CSVs por time).
    """
    teams = list_teams_from_league(league_id)
    if not teams:
        raise HTTPException(status_code=404, detail="Liga não encontrada ou sem times")
    return {"league_id": league_id, "teams": teams}


@app.get("/leagues/{league_id}/team/{team_id}")
async def get_team(league_id: str, team_id: str):
    """
    Retorna os dados (linha única) do CSV do time dentro da liga.
    """
    row = get_team_row(league_id, team_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Time não encontrado para essa liga")
    return row
