import os
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd

from config import DATA_DIR
from utils.team_normalizer import normalize_name


def _slugify(name: str) -> str:
    """
    Transforma 'France Ligue 1' em 'france-ligue-1'.
    Usado como league_id nas rotas.
    """
    return (
        str(name)
        .strip()
        .lower()
        .replace(".csv", "")
        .replace("_", "-")
        .replace(" ", "-")
    )


def list_leagues() -> List[Dict[str, str]]:
    """
    Lista todos os CSVs da pasta data/leagues
    e monta uma lista de ligas.
    """
    leagues: List[Dict[str, str]] = []

    if not DATA_DIR.exists():
        return []

    for csv_path in DATA_DIR.glob("*.csv"):
        name = csv_path.stem  # nome sem .csv
        leagues.append(
            {
                "league_id": _slugify(name),
                "name": name,
                "filename": csv_path.name,
            }
        )

    return leagues


def get_league_path(league_id: str) -> Optional[Path]:
    """
    Recebe league_id (ex: 'france-ligue-1')
    e tenta encontrar o CSV correspondente.
    """
    if not DATA_DIR.exists():
        return None

    for csv_path in DATA_DIR.glob("*.csv"):
        name = csv_path.stem
        if _slugify(name) == league_id:
            return csv_path

    return None


def list_teams_from_league(league_id: str) -> List[Dict[str, str]]:
    """
    Lê o CSV da liga e devolve lista de times.
    Assumindo que a primeira coluna é o nome do time,
    ou que exista uma coluna chamada 'Team' ou 'team'.
    """
    csv_path = get_league_path(league_id)
    if not csv_path or not csv_path.exists():
        return []

    df = pd.read_csv(csv_path, sep=";", engine="python")

    # tenta descobrir a coluna de nome
    name_col = None
    for candidate in ["Team", "team", "Nome", "nome"]:
        if candidate in df.columns:
            name_col = candidate
            break

    if name_col is None:
        # se não achar, usa a primeira coluna
        name_col = df.columns[0]

    teams = []
    for raw_name in df[name_col].dropna().unique():
        norm = normalize_name(str(raw_name))
        teams.append(
            {
                "team_id": norm,
                "name": str(raw_name),
            }
        )
    return teams
