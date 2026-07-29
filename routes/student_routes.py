from flask import Blueprint, jsonify, request

from controllers.student_controller import (
    create_student,
    delete_student,
    get_all_students,
    get_student,
    update_student,
)
from utils.auth import token_required

student_bp = Blueprint("students", __name__, url_prefix="/api/students")


@student_bp.route("", methods=["GET"])
@token_required
def list_students():
    response, status = get_all_students()
    return jsonify(response), status


@student_bp.route("/<int:student_id>", methods=["GET"])
@token_required
def get_one(student_id):
    response, status = get_student(student_id)
    return jsonify(response), status


@student_bp.route("", methods=["POST"])
@token_required
def create():
    data = request.get_json(silent=True) or {}
    response, status = create_student(data)
    return jsonify(response), status


@student_bp.route("/<int:student_id>", methods=["PUT"])
@token_required
def update(student_id):
    data = request.get_json(silent=True) or {}
    response, status = update_student(student_id, data)
    return jsonify(response), status


@student_bp.route("/<int:student_id>", methods=["DELETE"])
@token_required
def delete(student_id):
    response, status = delete_student(student_id)
    return jsonify(response), status
