"""Pure business viability calculations.

The functions in this module deliberately do not access a database or an AI
service.  Callers load the relevant objects and pass them in.
"""


def _number(value, default=0.0):
    """Return a finite numeric value, or ``default`` for missing values."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return float(default)
    return number


def _text(value):
    """Return a normalized lowercase string for safe comparisons."""
    return str(value or "").strip().lower()


def _get(obj, name, default=None):
    """Read either an object attribute or a dictionary key."""
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def compute_viability(category, village, competitors, available_capital):
    """Calculate a business viability score from 0 to 100.

    Args:
        category: Object or dictionary with investment range, risk, margin,
            and sector fields.
        village: Object or dictionary with population, literacy, occupation,
            and distance-to-city fields.
        competitors: A list of competitor objects. Only its length is used.
        available_capital: User's available margin money in rupees.

    Returns:
        A dictionary containing the integer total score, label, and component
        scores for demand, competition, capital, infrastructure, and risk.
    """
    investment_min = max(0.0, _number(_get(category, "investment_min")))
    investment_max = max(investment_min, _number(_get(category, "investment_max")))
    avg_investment = (investment_min + investment_max) / 2.0

    population = max(0.0, _number(_get(village, "population")))
    demand_pts = min(30.0, population / 200.0)

    occupation = _text(_get(village, "primary_occupation"))
    sector = _text(_get(category, "sector"))
    if occupation == "agriculture" and sector == "manufacturing":
        demand_pts = min(30.0, demand_pts + 3.0)
    elif occupation == "mixed" and sector == "service":
        demand_pts = min(30.0, demand_pts + 2.0)

    comp_count = len(competitors) if competitors else 0
    comp_pts = max(5.0, 25.0 - (max(0, comp_count) * 5.0))

    capital = max(0.0, _number(available_capital))
    margin_ratio = capital / avg_investment if avg_investment > 0 else 1.0
    if margin_ratio >= 0.25:
        cap_pts = 20.0
    elif margin_ratio >= 0.15:
        cap_pts = 16.0
    elif margin_ratio >= 0.10:
        cap_pts = 12.0
    else:
        cap_pts = 6.0

    city_km = max(0.0, _number(_get(village, "nearest_city_km")))
    if city_km <= 10:
        infra_pts = 15.0
    elif city_km <= 20:
        infra_pts = 12.0
    elif city_km <= 30:
        infra_pts = 8.0
    else:
        infra_pts = 5.0

    risk_map = {"low": 10.0, "medium": 7.0, "high": 4.0}
    risk_pts = risk_map.get(_text(_get(category, "risk_level")), 7.0)

    literacy_rate = max(0.0, _number(_get(village, "literacy_rate")))
    if literacy_rate >= 70:
        demand_pts = min(30.0, demand_pts + 2.0)
    elif literacy_rate < 45:
        demand_pts = max(0.0, demand_pts - 2.0)

    total = demand_pts + comp_pts + cap_pts + infra_pts + risk_pts
    total_score = min(100, max(0, int(round(total))))

    if total_score >= 86:
        label = "Excellent"
    elif total_score >= 71:
        label = "Very Good"
    elif total_score >= 51:
        label = "Good"
    elif total_score >= 31:
        label = "Below Average"
    else:
        label = "Poor"

    return {
        "total_score": total_score,
        "label": label,
        "breakdown": {
            "demand": int(round(demand_pts)),
            "competition": int(round(comp_pts)),
            "capital": int(round(cap_pts)),
            "infrastructure": int(round(infra_pts)),
            "risk": int(round(risk_pts)),
        },
    }


def get_alternatives(category, village, all_categories, competitors, capital):
    """Return up to three higher-potential alternative business categories.

    Categories that require more than five times the available capital are
    skipped. The returned dictionaries contain the predicted score and the
    investment range needed by a caller to render an explanation.
    """
    alternatives = []
    available_capital = max(0.0, _number(capital))
    current_id = _get(category, "id")
    village_name = _get(village, "name", "your village")

    for cat in all_categories or []:
        if _get(cat, "id") == current_id:
            continue

        investment_min = max(0.0, _number(_get(cat, "investment_min")))
        investment_max = max(investment_min, _number(_get(cat, "investment_max")))
        if investment_min > available_capital * 5:
            continue

        score = compute_viability(cat, village, competitors, available_capital)
        name = _get(cat, "name", "")
        alternatives.append(
            {
                "category_id": _get(cat, "id"),
                "name": name,
                "name_hi": _get(cat, "name_hi", ""),
                "score": score["total_score"],
                "label": score["label"],
                "investment_min": round(investment_min, 2),
                "investment_max": round(investment_max, 2),
                "why": (
                    f"Based on local demand and competition in {village_name}, "
                    f"{name} shows a viability score of "
                    f"{score['total_score']}/100."
                ),
            }
        )

    alternatives.sort(key=lambda item: item["score"], reverse=True)
    return alternatives[:3]