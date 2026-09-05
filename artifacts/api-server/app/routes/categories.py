from flask import Blueprint, jsonify, request

from app.models.category import BusinessCategory


categories_bp = Blueprint(
    "categories",
    __name__,
    url_prefix="/api/categories",
)


@categories_bp.get("")
def get_categories():
    query = BusinessCategory.query

    sector = request.args.get("sector")
    risk_level = request.args.get("risk_level")

    if sector:
        query = query.filter(BusinessCategory.sector.ilike(sector))

    if risk_level:
        query = query.filter(BusinessCategory.risk_level.ilike(risk_level))

    categories = query.order_by(BusinessCategory.name).all()

    return jsonify([
        category.to_dict()
        for category in categories
    ]), 200


@categories_bp.get("/<int:category_id>")
def get_category(category_id):
    category = BusinessCategory.query.get(category_id)

    if category is None:
        return jsonify({
            "error": True,
            "message": "Business category not found",
            "code": "CATEGORY_NOT_FOUND",
        }), 404

    return jsonify(category.to_dict()), 200
