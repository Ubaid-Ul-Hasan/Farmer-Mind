import json
from pathlib import Path
from typing import Any


KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

_cache: dict[str, Any] = {}


def load(filename: str) -> Any:
    if filename in _cache:
        return _cache[filename]
    path = KNOWLEDGE_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    _cache[filename] = data
    return data


def load_all() -> dict[str, Any]:
    return {
        "crops": load("crops.json"),
        "problems": load("problems.json"),
        "machinery": load("machinery.json"),
        "symptoms": load("symptoms.json"),
        "rules": load("rules.json"),
        "experience": load("experience.json"),
    }
