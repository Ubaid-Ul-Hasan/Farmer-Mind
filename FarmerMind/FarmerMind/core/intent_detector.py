from typing import List


INTENT_KEYWORDS: dict[str, List[str]] = {
    "irrigation_information": [
        "water", "irrigate", "irrigation", "watering", "moisture",
        "flood", "drip", "sprinkler", "wet", "dry", "thirsty", "drought",
        "rain", "rainfall", "postpone", "schedule", "when irrigate"
    ],
    "fertilizer_information": [
        "fertilizer", "fertiliser", "urea", "nitrogen", "phosphorus",
        "potassium", "npk", "dap", "ssp", "manure", "compost", "nutrient",
        "deficiency", "zinc", "iron", "boron", "feed", "top dress"
    ],
    "disease_information": [
        "disease", "fungal", "fungus", "rust", "blight", "mildew",
        "rot", "wilt", "smut", "blast", "virus", "bacterial", "pathogen",
        "infection", "infected", "spots", "lesion", "spray", "fungicide"
    ],
    "pest_information": [
        "pest", "insect", "aphid", "aphids", "bollworm", "caterpillar", "worm",
        "whitefly", "thrips", "beetle", "mite", "larva", "larvae",
        "infestation", "damage", "eaten", "holes", "chewed", "bug",
        "armyworm", "borer", "mealybug", "scale", "nematode", "weevil",
        "deal", "control", "kill", "spray insecticide", "eliminate"
    ],
    "crop_information": [
        "sow", "sowing", "planting", "variety", "seed", "seed rate",
        "germination", "transplant", "yield", "season", "duration",
        "grow", "growth", "cultivate", "acre", "production",
        "best crop", "suitable crop", "profile", "ph", "soil type"
    ],
    "symptom_diagnosis": [
        "leaves", "leaf", "yellow", "brown", "white", "black", "spots",
        "wilting", "drooping", "curl", "curling", "dying", "dead",
        "diagnose", "symptom", "showing", "dropping", "boll",
        "powder", "coating", "stunted", "shriveled", "cracking",
        "discolor", "turning", "strange", "wrong"
    ],
    "machinery_problem": [
        "tractor", "pump", "tube well", "engine", "machine", "thresher",
        "sprayer", "motor", "oil", "smoke", "start", "overheat",
        "hydraulic", "repair", "maintenance", "service", "break", "fault"
    ],
    "weather_problem": [
        "rain", "frost", "hail", "storm", "flood", "drought", "heat",
        "cold", "temperature", "humidity", "forecast", "weather",
        "tomorrow", "climate", "season"
    ],
    "market_problem": [
        "price", "market", "sell", "selling", "buyer", "profit", "loss",
        "income", "rate", "cost", "store", "storage", "trade", "mandi"
    ],
    "land_preparation": [
        "tillage", "plow", "plough", "cultivate", "prepare", "soil",
        "land", "field preparation", "subsoil", "compaction", "saline",
        "alkaline", "reclaim", "leveling", "laser"
    ],
    "harvesting": [
        "harvest", "harvesting", "harvested", "cut", "reap", "combine",
        "pick", "mature", "maturity", "ready", "ripe", "ripening",
        "threshing", "post harvest", "moisture content", "when harvest"
    ],
}

INTENT_WEIGHTS: dict[str, int] = {
    "irrigation_information": 1,
    "fertilizer_information": 1,
    "disease_information": 1,
    "pest_information": 1,
    "crop_information": 1,
    "symptom_diagnosis": 1,
    "machinery_problem": 2,
    "weather_problem": 1,
    "market_problem": 2,
    "land_preparation": 2,
    "harvesting": 1,
}


def detect_intent(tokens: List[str]) -> str:
    scores: dict[str, int] = {intent: 0 for intent in INTENT_KEYWORDS}
    token_set = set(tokens)

    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            kw_tokens = kw.split()
            if all(kt in token_set for kt in kw_tokens):
                scores[intent] += INTENT_WEIGHTS.get(intent, 1)

    best_intent = max(scores, key=lambda k: scores[k])

    if scores[best_intent] == 0:
        return "general_inquiry"

    return best_intent
