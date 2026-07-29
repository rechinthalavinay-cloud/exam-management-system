from flask import Blueprint, jsonify, request

from controllers.auth_controller import login_user
from utils.auth import token_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    response, status = login_user(data)
    return jsonify(response), status


@auth_bp.route("/verify", methods=["GET"])
@token_required
def verify():
    return jsonify({"success": True, "message": "Token is valid"}), 200
