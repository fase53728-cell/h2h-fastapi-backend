from pathlib import Path

# Pasta base do projeto (onde está este arquivo)
BASE_DIR = Path(__file__).resolve().parent

# Pasta onde ficam as ligas (cada liga é uma pasta dentro de data/)
# Ex: data/laliga_espanha, data/premier_league, etc.
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
