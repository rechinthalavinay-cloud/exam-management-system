from flask import Blueprint, jsonify, request

from controllers.result_controller import (
    create_result,
    delete_result,
    get_all_results,
    get_analytics,
    get_result,
    update_result,
)
from utils.auth import token_required

result_bp = Blueprint("results", __name__, url_prefix="/api/results")


@result_bp.route("", methods=["GET"])
@token_required
def list_results():
    response, status = get_all_results()
    return jsonify(response), status


@result_bp.route("/analytics", methods=["GET"])
@token_required
def analytics():
    response, status = get_analytics()
    return jsonify(response), status


@result_bp.route("/<int:result_id>", methods=["GET"])
@token_required
def get_one(result_id):
    response, status = get_result(result_id)
    return jsonify(response), status


@result_bp.route("", methods=["POST"])
@token_required
def create():
    data = request.get_json(silent=True) or {}
    response, status = create_result(data)
    return jsonify(response), status


@result_bp.route("/<int:result_id>", methods=["PUT"])
@token_required
def update(result_id):
    data = request.get_json(silent=True) or {}
    response, status = update_result(result_id, data)
    return jsonify(response), status


@result_bp.route("/<int:result_id>", methods=["DELETE"])
@token_required
def delete(result_id):
    response, status = delete_result(result_id)
    return jsonify(response), status
