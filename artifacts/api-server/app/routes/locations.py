from flask import Blueprint, jsonify, request

from app.models.location import State, District, Block, Village

locations_bp = Blueprint("locations", __name__, url_prefix="/api/locations")


@locations_bp.get("/states")
def get_states():
    states = State.query.order_by(State.name).all()
    return jsonify([state.to_dict() for state in states]), 200


@locations_bp.get("/states/<int:state_id>/districts")
def get_districts(state_id):
    state = State.query.get(state_id)

    if state is None:
        return jsonify({
            "error": True,
            "message": "State not found",
            "code": "STATE_NOT_FOUND",
        }), 404

    districts = District.query.filter_by(
        state_id=state_id
    ).order_by(District.name).all()

    return jsonify([district.to_dict() for district in districts]), 200


@locations_bp.get("/districts/<int:district_id>/blocks")
def get_blocks(district_id):
    district = District.query.get(district_id)

    if district is None:
        return jsonify({
            "error": True,
            "message": "District not found",
            "code": "DISTRICT_NOT_FOUND",
        }), 404

    blocks = Block.query.filter_by(
        district_id=district_id
    ).order_by(Block.name).all()

    return jsonify([block.to_dict() for block in blocks]), 200


@locations_bp.get("/blocks/<int:block_id>/villages")
def get_villages(block_id):
    block = Block.query.get(block_id)

    if block is None:
        return jsonify({
            "error": True,
            "message": "Block not found",
            "code": "BLOCK_NOT_FOUND",
        }), 404

    villages = Village.query.filter_by(
        block_id=block_id
    ).order_by(Village.name).all()

    return jsonify([village.to_dict() for village in villages]), 200


@locations_bp.get("/search")
def search_locations():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": True,
            "message": "Search query is required",
            "code": "SEARCH_QUERY_REQUIRED",
        }), 400

    pattern = f"%{query}%"

    states = State.query.filter(
        State.name.ilike(pattern)
    ).limit(20).all()

    districts = District.query.filter(
        District.name.ilike(pattern)
    ).limit(20).all()

    blocks = Block.query.filter(
        Block.name.ilike(pattern)
    ).limit(20).all()

    villages = Village.query.filter(
        Village.name.ilike(pattern)
    ).limit(20).all()

    return jsonify({
        "states": [state.to_dict() for state in states],
        "districts": [district.to_dict() for district in districts],
        "blocks": [block.to_dict() for block in blocks],
        "villages": [village.to_dict() for village in villages],
    }), 200
