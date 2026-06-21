from typing import Any, Optional


def generate(intent: str, data: dict[str, Any], original_query: str) -> str:
    crop = data.get("crop")
    crop_data = data.get("crop_data")

    if intent == "irrigation_information":
        return _irrigation_response(crop, crop_data, data.get("rule"))

    elif intent == "fertilizer_information":
        return _fertilizer_response(crop, crop_data, data.get("rule"))

    elif intent == "symptom_diagnosis":
        return _symptom_response(data.get("symptoms", []), crop)

    elif intent == "disease_information":
        return _disease_response(crop, crop_data, data.get("symptoms", []), data.get("problem"))

    elif intent == "pest_information":
        return _pest_response(crop, crop_data, data.get("symptoms", []))

    elif intent == "crop_information":
        return _crop_info_response(crop, crop_data)

    elif intent == "machinery_problem":
        return _machinery_response(data.get("machinery"))

    elif intent == "weather_problem":
        return _weather_response(data.get("rule"))

    elif intent == "market_problem":
        return _market_response()

    elif intent == "land_preparation":
        return _land_response(data.get("rule"))

    elif intent == "harvesting":
        return _harvesting_response(crop, crop_data)

    else:
        return _fallback_response(data.get("experience", []))


def _irrigation_response(crop: Optional[str], crop_data: Optional[dict], rule: Optional[dict]) -> str:
    lines = []

    if rule:
        lines.append(rule["response"])
        lines.append("")

    if crop and crop_data:
        irr = crop_data.get("irrigation", {})
        count = irr.get("total_count", "varies by conditions")
        stages = irr.get("critical_stages", [])
        req = irr.get("water_requirement_mm")

        lines.append(f"Based on field experience with {crop.title()}:")
        lines.append(f"  - Total irrigations required: {count}")
        if req:
            lines.append(f"  - Seasonal water requirement: approximately {req} mm")
        if stages:
            lines.append(f"  - Critical irrigation stages: {', '.join(stages)}")

    if not lines:
        lines.append("Irrigation timing depends on soil type, weather conditions, and crop growth stage.")
        lines.append("Monitor soil moisture at 15 to 20 cm depth and irrigate when soil feels dry at that depth.")

    return "\n".join(lines)


def _fertilizer_response(crop: Optional[str], crop_data: Optional[dict], rule: Optional[dict]) -> str:
    lines = []

    if rule:
        lines.append(rule["response"])
        lines.append("")

    if crop and crop_data:
        fert = crop_data.get("fertilizer", {})
        n = fert.get("nitrogen_kg_per_acre")
        p = fert.get("phosphorus_kg_per_acre")
        k = fert.get("potassium_kg_per_acre")
        app = fert.get("application", "")

        lines.append(f"Recommended fertilizer schedule for {crop.title()} per acre:")
        if n:
            lines.append(f"  - Nitrogen (N): {n} kg")
        if p:
            lines.append(f"  - Phosphorus (P): {p} kg")
        if k:
            lines.append(f"  - Potassium (K): {k} kg")
        if app:
            lines.append(f"  - Application method: {app}")

    if not lines:
        lines.append("Fertilizer requirements vary by soil test results and crop type.")
        lines.append("Conduct a soil test before applying fertilizers to determine actual crop needs.")

    return "\n".join(lines)


def _symptom_response(symptoms: list[dict], crop: Optional[str]) -> str:
    if not symptoms:
        return (
            "No specific symptom pattern matched in the knowledge base.\n"
            "Describe the affected plant part, color change, and spread pattern for a more accurate diagnosis."
        )

    lines = ["Possible causes based on described symptoms:"]
    lines.append("")

    top = symptoms[0]
    for i, cause in enumerate(top["general_causes"], 1):
        lines.append(f"  {i}. {cause}")

    if crop and crop in top.get("crop_specific", {}):
        lines.append("")
        lines.append(f"Specific note for {crop.title()}:")
        lines.append(f"  {top['crop_specific'][crop]}")

    lines.append("")
    lines.append(f"Recommended action:")
    lines.append(f"  {top['action']}")

    return "\n".join(lines)


def _disease_response(crop: Optional[str], crop_data: Optional[dict],
                      symptoms: list[dict], problem: Optional[dict]) -> str:
    lines = []

    if crop and crop_data:
        diseases = crop_data.get("common_diseases", [])
        if diseases:
            lines.append(f"Common diseases affecting {crop.title()}:")
            for d in diseases:
                lines.append(f"  - {d.capitalize()}")
            lines.append("")

    if symptoms:
        top = symptoms[0]
        lines.append("Based on described symptoms:")
        for cause in top["general_causes"]:
            lines.append(f"  - {cause}")
        lines.append("")
        lines.append(f"Recommended action: {top['action']}")

    elif problem:
        lines.append("Likely diagnosis based on problem description:")
        for cause in problem.get("causes", []):
            lines.append(f"  - {cause}")
        lines.append("")
        lines.append(f"Action: {problem.get('diagnosis', 'Consult an agronomist.')}")

    if not lines:
        lines.append("Provide more details about the affected crop and visible symptoms for accurate disease diagnosis.")

    return "\n".join(lines)


def _pest_response(crop: Optional[str], crop_data: Optional[dict], symptoms: list[dict]) -> str:
    lines = []

    if crop and crop_data:
        pests = crop_data.get("common_pests", [])
        if pests:
            lines.append(f"Common pests affecting {crop.title()}:")
            for p in pests:
                lines.append(f"  - {p.capitalize()}")
            lines.append("")

    if symptoms:
        top = symptoms[0]
        if top.get("crop_specific") and crop and crop in top["crop_specific"]:
            lines.append(f"Field note for {crop.title()}:")
            lines.append(f"  {top['crop_specific'][crop]}")
            lines.append("")
        lines.append(f"Recommended action: {top['action']}")

    if not lines:
        lines.append("Identify the pest before applying any insecticide.")
        lines.append("Collect and inspect damaged plant parts. Apply control only when pest levels exceed economic threshold.")

    return "\n".join(lines)


def _crop_info_response(crop: Optional[str], crop_data: Optional[dict]) -> str:
    if not crop_data:
        return "Crop not found in the knowledge base. Please specify a common crop such as wheat, rice, cotton, or maize."

    c = crop_data
    lines = [f"Crop Profile: {crop.title() if crop else 'Unknown'}"]
    lines.append("")
    lines.append(f"  Season       : {c.get('season', 'N/A').title()}")
    lines.append(f"  Sowing time  : {c.get('sowing_time', 'N/A')}")
    lines.append(f"  Harvest time : {c.get('harvest_time', 'N/A')}")
    lines.append(f"  Duration     : {c.get('duration_days', 'N/A')} days")
    lines.append(f"  Seed rate    : {c.get('seed_rate_kg_per_acre', 'N/A')} kg per acre")
    lines.append(f"  Yield target : {c.get('yield_potential_maunds_per_acre', 'N/A')} maunds per acre")
    lines.append(f"  Suitable soil: {', '.join(c.get('soil_type', [])) if c.get('soil_type') else 'N/A'}")
    lines.append(f"  Soil pH range: {c.get('ph_range', 'N/A')}")

    if c.get("notes"):
        lines.append("")
        lines.append(f"Field note: {c['notes']}")

    return "\n".join(lines)


def _machinery_response(machinery: Optional[dict]) -> str:
    if not machinery:
        return (
            "No specific machinery problem matched.\n"
            "Describe the machine type (tractor, tube well, thresher) and specific symptom for a targeted diagnosis."
        )

    if "problem" in machinery and "detail" in machinery:
        detail = machinery["detail"]
        lines = [f"Diagnosis for {machinery.get('machine', 'machine').replace('_', ' ').title()} — "
                 f"{machinery['problem'].replace('_', ' ').title()}:"]
        lines.append("")
        causes = detail.get("causes", [])
        if isinstance(causes, list):
            lines.append("Possible causes:")
            for c in causes:
                lines.append(f"  - {c}")
        elif isinstance(causes, dict):
            lines.append("Possible causes by symptom:")
            for k, v in causes.items():
                lines.append(f"  - {k.title()} smoke: {v}")
        lines.append("")
        lines.append(f"Recommended action: {detail.get('solution', 'Consult a qualified mechanic.')}")
        return "\n".join(lines)

    # general machine info
    lines = ["Maintenance schedule:"]
    schedule = machinery.get("maintenance_schedule", {})
    for interval, tasks in schedule.items():
        lines.append(f"  {interval.replace('_', ' ').title()}: {', '.join(tasks)}")
    return "\n".join(lines)


def _weather_response(rule: Optional[dict]) -> str:
    if rule:
        return rule["response"]
    return (
        "Weather conditions directly affect irrigation, fertilizer timing, and disease pressure.\n"
        "Monitor local forecasts and adjust farming operations accordingly."
    )


def _market_response() -> str:
    from utils.loader import load
    exp = load("experience.json")
    market = exp.get("market_knowledge", {})
    lines = ["Market and selling guidance:"]
    lines.append("")
    for tip in market.get("tips", []):
        lines.append(f"  - {tip}")
    lines.append("")
    lines.append("Price factors to consider:")
    for factor in market.get("price_factors", [])[:4]:
        lines.append(f"  - {factor}")
    return "\n".join(lines)


def _land_response(rule: Optional[dict]) -> str:
    if rule:
        return rule["response"]
    return (
        "Proper land preparation improves water infiltration, root growth, and germination.\n"
        "Deep tillage every 3 to 4 years breaks compaction. Laser leveling improves irrigation efficiency by 20 to 30 percent."
    )


def _harvesting_response(crop: Optional[str], crop_data: Optional[dict]) -> str:
    if crop and crop_data:
        lines = [f"Harvesting guidelines for {crop.title()}:"]
        lines.append(f"  - Expected harvest time : {crop_data.get('harvest_time', 'N/A')}")
        lines.append(f"  - Crop duration         : {crop_data.get('duration_days', 'N/A')} days from sowing")
        if crop_data.get("notes"):
            lines.append("")
            lines.append(f"  Field note: {crop_data['notes']}")
        return "\n".join(lines)
    return (
        "Harvest when the crop reaches physiological maturity.\n"
        "Delayed harvesting causes field losses through shattering, lodging, and quality deterioration."
    )


def _fallback_response(experience: list[str]) -> str:
    if experience:
        return "Based on farming experience:\n\n" + "\n\n".join(f"  {e}" for e in experience)
    return (
        "Please provide more details about your crop, the problem you are observing, "
        "or the specific information you need. You can ask about irrigation, fertilizers, "
        "diseases, pests, machinery, or any specific crop."
    )
