from typing import Any, Optional
from core import knowledge_retriever as kr


def reason(intent: str, tokens: list[str], crop_name: Optional[str]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "intent": intent,
        "crop": crop_name,
        "crop_data": None,
        "symptoms": [],
        "rule": None,
        "machinery": None,
        "experience": [],
        "problem": None,
    }

    if crop_name:
        result["crop_data"] = kr.retrieve_crop(crop_name)

    if intent == "symptom_diagnosis":
        result["symptoms"] = kr.retrieve_symptoms(tokens)

    elif intent in ("irrigation_information", "fertilizer_information",
                    "weather_problem", "land_preparation"):
        result["rule"] = kr.retrieve_rules(intent, tokens)
        if crop_name and result["crop_data"]:
            pass  # crop_data already set above

    elif intent == "machinery_problem":
        result["machinery"] = kr.retrieve_machinery(tokens)

    elif intent == "crop_information":
        if not result["crop_data"]:
            result["crop_data"] = _search_any_crop(tokens)

    elif intent == "disease_information":
        result["symptoms"] = kr.retrieve_symptoms(tokens)
        result["problem"] = kr.retrieve_problem(tokens)

    elif intent == "pest_information":
        result["symptoms"] = kr.retrieve_symptoms(tokens)

    elif intent == "harvesting":
        if not result["crop_data"]:
            result["crop_data"] = _search_any_crop(tokens)

    result["experience"] = kr.retrieve_experience(tokens, crop_name)

    return result


def _search_any_crop(tokens: list[str]) -> Optional[dict]:
    from utils.loader import load
    crops = load("crops.json")
    for token in tokens:
        if token in crops:
            return crops[token]
    return None
