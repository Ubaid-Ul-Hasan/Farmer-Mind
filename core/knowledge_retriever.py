from typing import Any, Optional
from utils.loader import load_all


_kb: dict[str, Any] = {}


def _get_kb() -> dict[str, Any]:
    global _kb
    if not _kb:
        _kb = load_all()
    return _kb


def retrieve_crop(crop_name: str) -> Optional[dict]:
    kb = _get_kb()
    return kb["crops"].get(crop_name)


def retrieve_problem(tokens: list[str]) -> Optional[dict]:
    kb = _get_kb()
    best_key = None
    best_score = 0
    for key, entry in kb["problems"].items():
        score = sum(1 for t in tokens if t in key or any(t in c.lower() for c in entry.get("causes", [])))
        if score > best_score:
            best_score = score
            best_key = key
    return kb["problems"].get(best_key) if best_key else None


def retrieve_symptoms(tokens: list[str]) -> list[dict]:
    kb = _get_kb()
    results = []
    for symptom in kb["symptoms"]["symptoms"]:
        score = sum(1 for t in tokens if t in symptom["keywords"])
        if score > 0:
            results.append((score, symptom))
    results.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in results[:3]]


def retrieve_machinery(tokens: list[str]) -> Optional[dict]:
    kb = _get_kb()
    machinery = kb["machinery"]

    # Direct machine name match
    for machine_key in machinery:
        if machine_key in tokens:
            # Also try to find specific problem
            problems = machinery[machine_key].get("common_problems", {})
            best_prob = None
            best_score = 0
            for prob_key, prob_data in problems.items():
                symptoms = prob_data.get("symptoms", [])
                causes = prob_data.get("causes", [])
                combined = " ".join(symptoms + (causes if isinstance(causes, list) else [])).lower()
                score = sum(1 for t in tokens if t in combined)
                if score > best_score:
                    best_score = score
                    best_prob = (prob_key, prob_data)
            if best_prob:
                return {"machine": machine_key, "problem": best_prob[0], "detail": best_prob[1]}
            return machinery[machine_key]

    # Keyword scan across all machines and problems
    best_match = None
    best_score = 0
    for machine_key, machine_data in machinery.items():
        for prob_key, prob_data in machine_data.get("common_problems", {}).items():
            symptoms = prob_data.get("symptoms", [])
            causes = prob_data.get("causes", [])
            combined = " ".join(symptoms + (causes if isinstance(causes, list) else [])).lower()
            score = sum(1 for t in tokens if t in combined)
            # also score on problem key words
            score += sum(1 for t in tokens if t in prob_key)
            if score > best_score:
                best_score = score
                best_match = {"machine": machine_key, "problem": prob_key, "detail": prob_data}

    return best_match if best_score > 0 else None


def retrieve_rules(intent: str, tokens: list[str]) -> Optional[dict]:
    kb = _get_kb()
    rules = kb["rules"]

    rule_map = {
        "irrigation_information": "irrigation_rules",
        "weather_problem": "weather_rules",
        "fertilizer_information": "fertilizer_rules",
        "land_preparation": "land_preparation_rules",
    }

    rule_group_key = rule_map.get(intent)
    if not rule_group_key:
        for group_key in rules:
            rule_group_key = group_key
            break

    best_rule = None
    best_score = 0
    for group_key, rule_list in rules.items():
        for rule in rule_list:
            score = sum(1 for t in tokens if t in rule.get("keywords", []))
            if score > best_score:
                best_score = score
                best_rule = rule

    return best_rule if best_score > 0 else None


def retrieve_experience(tokens: list[str], crop_name: Optional[str]) -> list[str]:
    kb = _get_kb()
    exp = kb["experience"]
    results = []

    for entry in exp.get("general_wisdom", []):
        if any(t in entry["keywords"] for t in tokens):
            results.append(entry["experience"])

    if crop_name:
        crop_tips = exp.get("crop_specific_experience", {}).get(crop_name, [])
        for tip in crop_tips:
            if any(t in tip["keywords"] for t in tokens):
                results.append(tip["tip"])

    return results[:2]
