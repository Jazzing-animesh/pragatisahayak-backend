from functools import wraps

import jwt
from flask import current_app, jsonify, request

from app.models.user import User


def _error(message, code, status_code):
    return jsonify({
        "error": True,
        "message": message,
        "code": code,
    }), status_code


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return _error(
                "Authorization token is required",
                "AUTH_TOKEN_REQUIRED",
                401,
            )

        token = auth_header.split(" ", 1)[1].strip()

        if not token:
            return _error(
                "Authorization token is required",
                "AUTH_TOKEN_REQUIRED",
                401,
            )

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return _error(
                "Token has expired",
                "AUTH_TOKEN_EXPIRED",
                401,
            )
        except jwt.InvalidTokenError:
            return _error(
                "Invalid authorization token",
                "AUTH_TOKEN_INVALID",
                401,
            )

        user_id = payload.get("user_id")

        if not user_id:
            return _error(
                "Invalid token payload",
                "AUTH_TOKEN_INVALID",
                401,
            )

        user = User.query.get(user_id)

        if user is None:
            return _error(
                "User not found",
                "AUTH_USER_NOT_FOUND",
                401,
            )

        request.current_user = user
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.current_user.role != "admin":
            return _error(
                "Admin access is required",
                "AUTH_ADMIN_REQUIRED",
                403,
            )

        return f(*args, **kwargs)

    return decorated
