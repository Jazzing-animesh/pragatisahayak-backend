from flask import Blueprint, jsonify, request

from app.models.category import BusinessCategory
from app.models.competitor import Competitor
from app.models.location import Village

analysis_bp = Blueprint("analysis", __name__, url_prefix="/api")


@analysis_bp.post("/analyze")
def analyze_business():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": True,
            "message": "Request body must be a JSON object",
            "code": "INVALID_JSON",
        }), 400

    village_id = data.get("village_id")
    category_id = data.get("category_id")

    if not village_id or not category_id:
        return jsonify({
            "error": True,
            "message": "village_id and category_id are required",
            "code": "MISSING_FIELDS",
        }), 400

    village = Village.query.get(village_id)
    category = BusinessCategory.query.get(category_id)

    if village is None:
        return jsonify({
            "error": True,
            "message": "Village not found",
            "code": "VILLAGE_NOT_FOUND",
        }), 404

    if category is None:
        return jsonify({
            "error": True,
            "message": "Business category not found",
            "code": "CATEGORY_NOT_FOUND",
        }), 404

    competitors = Competitor.query.filter_by(
        category_id=category_id,
        block_id=village.block_id,
    ).order_by(Competitor.distance_km).all()

    competitor_count = len(competitors)

    if competitor_count == 0:
        competition_level = "low"
    elif competitor_count <= 3:
        competition_level = "medium"
    else:
        competition_level = "high"

    return jsonify({
        "village": village.to_dict(),
        "category": category.to_dict(),
        "competitors": [c.to_dict() for c in competitors],
        "analysis": {
            "competition_level": competition_level,
            "competitor_count": competitor_count,
            "estimated_investment": {
                "min": category.investment_min,
                "max": category.investment_max,
            },
            "typical_margin": category.typical_margin,
            "risk_level": category.risk_level,
            "breakeven_months": category.breakeven_months,
        },
    }), 200
