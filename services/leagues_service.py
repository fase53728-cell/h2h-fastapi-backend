from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd

from config import DATA_DIR


def list_leagues() -> List[Dict[str, str]]:
    """
    Lista as ligas disponíveis como PASTAS dentro de data/.
    Exemplo:
        data/laliga_espanha
        data/premier_league
    """
    leagues: List[Dict[str, str]] = []

    if not DATA_DIR.exists():
        return leagues

    for item in DATA_DIR.iterdir():
        if item.is_dir():
            leagues.append(
                {
                    "league_id": item.name,  # ex: "laliga_espanha"
                    "name": item.name,
                }
            )

    leagues.sort(key=lambda x: x["name"].lower())
    return leagues


def get_league_dir(league_id: str) -> Optional[Path]:
    """
    Retorna o caminho da pasta da liga.
    Ex: DATA_DIR / "laliga_espanha"
    """
    league_dir = DATA_DIR / league_id
    if league_dir.exists() and league_dir.is_dir():
        return league_dir
    return None


def list_teams_from_league(league_id: str) -> List[Dict[str, str]]:
    """
    Lista os times de uma liga com base nos arquivos CSV dentro da pasta da liga.
    Ex: data/laliga_espanha/Barcelona.csv
    """
    league_dir = get_league_dir(league_id)
    if not league_dir:
        return []

    teams: List[Dict[str, str]] = []

    for csv_path in league_dir.glob("*.csv"):
        team_id = csv_path.stem              # "Barcelona" ou "Real_Madrid"
        display_name = team_id.replace("_", " ")
        teams.append(
            {
                "team_id": team_id,
                "name": display_name,
                "filename": csv_path.name,
            }
        )

    teams.sort(key=lambda t: t["name"].lower())
    return teams


def get_team_row(league_id: str, team_id: str) -> Optional[Dict[str, object]]:
    """
    Lê o CSV de um time específico dentro da liga e retorna a primeira linha como dict.
    Ex: data/laliga_espanha/Barcelona.csv
    """
    league_dir = get_league_dir(league_id)
    if not league_dir:
        return None

    # tenta nome direto
    csv_path = league_dir / f"{team_id}.csv"
    if not csv_path.exists():
        # tenta trocar espaços por underline
        alt = team_id.replace(" ", "_")
        csv_path = league_dir / f"{alt}.csv"
        if not csv_path.exists():
            return None

    df = pd.read_csv(csv_path, sep=";", engine="python")

    if df.empty:
        return {}

    row = df.iloc[0].to_dict()
    row["team_id"] = team_id
    row["league_id"] = league_id
    row["__source_file__"] = csv_path.name
    return row
