from flask import Blueprint, jsonify, request

from controllers.exam_controller import (
    create_exam,
    delete_exam,
    get_all_exams,
    get_exam,
    update_exam,
)
from utils.auth import token_required

exam_bp = Blueprint("exams", __name__, url_prefix="/api/exams")


@exam_bp.route("", methods=["GET"])
@token_required
def list_exams():
    response, status = get_all_exams()
    return jsonify(response), status


@exam_bp.route("/<int:exam_id>", methods=["GET"])
@token_required
def get_one(exam_id):
    response, status = get_exam(exam_id)
    return jsonify(response), status


@exam_bp.route("", methods=["POST"])
@token_required
def create():
    data = request.get_json(silent=True) or {}
    response, status = create_exam(data)
    return jsonify(response), status


@exam_bp.route("/<int:exam_id>", methods=["PUT"])
@token_required
def update(exam_id):
    data = request.get_json(silent=True) or {}
    response, status = update_exam(exam_id, data)
    return jsonify(response), status


@exam_bp.route("/<int:exam_id>", methods=["DELETE"])
@token_required
def delete(exam_id):
    response, status = delete_exam(exam_id)
    return jsonify(response), status
