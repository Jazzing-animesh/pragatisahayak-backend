from flask import Blueprint, jsonify, request

from app.models.scheme import GovernmentScheme

schemes_bp = Blueprint("schemes", __name__, url_prefix="/api/schemes")


@schemes_bp.get("")
def get_schemes():
    schemes = GovernmentScheme.query.filter_by(is_active=True).order_by(
        GovernmentScheme.name
    ).all()
    return jsonify([scheme.to_dict() for scheme in schemes]), 200


@schemes_bp.get("/<int:scheme_id>")
def get_scheme(scheme_id):
    scheme = GovernmentScheme.query.get(scheme_id)

    if scheme is None:
        return jsonify({
            "error": True,
            "message": "Government scheme not found",
            "code": "SCHEME_NOT_FOUND",
        }), 404

    return jsonify(scheme.to_dict()), 200


@schemes_bp.post("/match")
def match_schemes():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": True,
            "message": "Request body must be a JSON object",
            "code": "INVALID_JSON",
        }), 400

    category = data.get("category")
    state = data.get("state")
    investment = data.get("investment")

    if not category or not state:
        return jsonify({
            "error": True,
            "message": "category and state are required",
            "code": "MISSING_FIELDS",
        }), 400

    schemes = GovernmentScheme.query.filter_by(is_active=True).all()
    matches = []

    for scheme in schemes:
        states = scheme.applicable_states or ["All"]
        categories = scheme.applicable_categories or ["All"]

        state_match = "All" in states or state in states
        category_match = "All" in categories or category in categories

        investment_match = True

        if investment is not None:
            try:
                amount = float(investment)
                investment_match = scheme.min_loan <= amount <= scheme.max_loan
            except (TypeError, ValueError):
                return jsonify({
                    "error": True,
                    "message": "investment must be a number",
                    "code": "INVALID_INVESTMENT",
                }), 400

        if state_match and category_match and investment_match:
            matches.append(scheme.to_dict())

    return jsonify({
        "matches": matches,
        "count": len(matches),
    }), 200
