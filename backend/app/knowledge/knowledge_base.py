import json
import re
from pathlib import Path

_DATA_PATH = Path(__file__).parent / "data" / "domain_knowledge.json"

with open(_DATA_PATH, encoding="utf-8") as f:
    _ENTRIES: list[dict] = json.load(f)


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z]+", text.lower()))


def search(query: str, top_k: int = 3) -> list[dict]:
    """Very simple keyword-overlap search over the local knowledge base.

    This intentionally avoids embeddings/vector DBs to keep the MVP local
    and dependency-light, while still giving the agent grounded domain
    knowledge to cite for meteorology/climate/disaster questions.
    """
    query_lower = query.lower()
    query_tokens = _tokenize(query)

    scored = []
    for entry in _ENTRIES:
        score = 0
        for kw in entry["keywords"]:
            if kw in query_lower:
                score += 3
        score += len(query_tokens & _tokenize(entry["topic"])) * 2
        score += len(query_tokens & _tokenize(entry["content"]))
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored[:top_k]]


def get_all_topics() -> list[str]:
    return [entry["topic"] for entry in _ENTRIES]
