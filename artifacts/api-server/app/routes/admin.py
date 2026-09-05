from flask import Blueprint, jsonify, request

from app import db
from app.models.category import BusinessCategory
from app.models.competitor import Competitor
from app.models.location import Block, District, State, Village
from app.models.scheme import GovernmentScheme
from app.models.user import User
from app.utils.auth_decorator import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/analytics")
@admin_required
def analytics():
    return jsonify({
        "states": State.query.count(),
        "districts": District.query.count(),
        "blocks": Block.query.count(),
        "villages": Village.query.count(),
        "categories": BusinessCategory.query.count(),
        "schemes": GovernmentScheme.query.count(),
        "competitors": Competitor.query.count(),
        "users": User.query.count(),
    }), 200


@admin_bp.get("/users")
@admin_required
def users():
    return jsonify([
        user.to_dict()
        for user in User.query.order_by(User.id).all()
    ]), 200


@admin_bp.delete("/users/<int:user_id>")
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({
            "error": True,
            "message": "User not found",
            "code": "USER_NOT_FOUND",
        }), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "User deleted successfully",
    }), 200
