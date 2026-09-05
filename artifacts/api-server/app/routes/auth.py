from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, current_app, jsonify, request

from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }

    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm="HS256",
    )


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": True,
            "message": "Request body must be a JSON object",
            "code": "INVALID_JSON",
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": True,
            "message": "email and password are required",
            "code": "MISSING_FIELDS",
        }), 400

    if len(password) < 6:
        return jsonify({
            "error": True,
            "message": "Password must be at least 6 characters",
            "code": "INVALID_PASSWORD",
        }), 400

    if User.query.filter_by(email=email).first():
        return jsonify({
            "error": True,
            "message": "Email is already registered",
            "code": "EMAIL_EXISTS",
        }), 409

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "user": user.to_dict(),
        "token": _token(user),
    }), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": True,
            "message": "Request body must be a JSON object",
            "code": "INVALID_JSON",
        }), 400

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password or ""):
        return jsonify({
            "error": True,
            "message": "Invalid email or password",
            "code": "INVALID_CREDENTIALS",
        }), 401

    return jsonify({
        "user": user.to_dict(),
        "token": _token(user),
    }), 200


@auth_bp.post("/refresh")
def refresh():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data.get("token"):
        return jsonify({
            "error": True,
            "message": "token is required",
            "code": "TOKEN_REQUIRED",
        }), 400

    try:
        payload = jwt.decode(
            data["token"],
            current_app.config["JWT_SECRET"],
            algorithms=["HS256"],
            options={"verify_exp": False},
        )
    except jwt.InvalidTokenError:
        return jsonify({
            "error": True,
            "message": "Invalid token",
            "code": "INVALID_TOKEN",
        }), 401

    user = User.query.get(payload.get("user_id"))

    if user is None:
        return jsonify({
            "error": True,
            "message": "User not found",
            "code": "USER_NOT_FOUND",
        }), 401

    return jsonify({"token": _token(user)}), 200
