from pathlib import Path

# Pasta base do projeto (onde está este arquivo)
BASE_DIR = Path(__file__).resolve().parent

# Pasta onde ficam os CSV das ligas
DATA_DIR = BASE_DIR / "data" / "leagues"
DATA_DIR.mkdir(parents=True, exist_ok=True)
