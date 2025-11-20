from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd

from config import DATA_DIR


def list_leagues() -> List[Dict[str, str]]:
    """
    Lista as ligas disponíveis como PASTAS dentro de data/.
    """
    leagues: List[Dict[str, str]] = []

    if not DATA_DIR.exists():
        return leagues

    for item in DATA_DIR.iterdir():
        if item.is_dir():
            leagues.append(
                {
                    "league_id": item.name,  
                    "name": item.name,
                }
            )

    leagues.sort(key=lambda x: x["name"].lower())
    return leagues


def get_league_dir(league_id: str) -> Optional[Path]:
    league_dir = DATA_DIR / league_id
    if league_dir.exists() and league_dir.is_dir():
        return league_dir
    return None


def list_teams_from_league(league_id: str) -> List[Dict[str, str]]:
    league_dir = get_league_dir(league_id)
    if not league_dir:
        return []

    teams: List[Dict[str, str]] = []

    for csv_path in league_dir.glob("*.csv"):
        team_id = csv_path.stem
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
    league_dir = get_league_dir(league_id)
    if not league_dir:
        return None

    csv_path = league_dir / f"{team_id}.csv"
    if not csv_path.exists():
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
