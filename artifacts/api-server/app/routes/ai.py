from flask import Blueprint, jsonify, request

from app.utils.auth_decorator import token_required

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")


@ai_bp.post("/chat")
@token_required
def chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": True,
            "message": "Request body must be a JSON object",
            "code": "INVALID_JSON",
        }), 400

    message = data.get("message")

    if not message or not isinstance(message, str):
        return jsonify({
            "error": True,
            "message": "message is required",
            "code": "MESSAGE_REQUIRED",
        }), 400

    return jsonify({
        "message": "AI service is currently unavailable. Please try again later.",
        "response": "I received your question and will help with business guidance when the AI service is available.",
    }), 200
