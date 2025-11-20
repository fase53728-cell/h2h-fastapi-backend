import unicodedata
import re

# Lista simples de sufixos comuns que atrapalham (pode ajustar depois)
_SUFFIXES = [
    "fc", "sc", "ac", "cf", "fk", "bk", "afc",
    "u19", "u20", "u21"
]

def _remove_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def normalize_name(name: str) -> str:
    """
    Normaliza nome de time para facilitar matching entre CSV / SofaScore / etc.
    Exemplo:
    "Atlético Mineiro FC" -> "atletico mineiro"
    """
    if not isinstance(name, str):
        return ""
    text = name.strip().lower()
    text = _remove_accents(text)

    # remove pontuações extras
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # quebra em palavras e remove sufixos conhecidos
    parts = text.split()
    filtered = [p for p in parts if p not in _SUFFIXES]

    if not filtered:
        filtered = parts

    return " ".join(filtered)
