from flask import Flask, jsonify, request, session

import config
from controllers.auth_controller import login_user, seed_admin_user
from models.database import close_db
from routes.auth_routes import auth_bp
from routes.exam_routes import exam_bp
from routes.page_routes import page_bp
from routes.result_routes import result_bp
from routes.student_routes import student_bp


def create_app():
    app = Flask(__name__)

    app.config["MYSQL_HOST"] = config.MYSQL_HOST
    app.config["MYSQL_USER"] = config.MYSQL_USER
    app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
    app.config["MYSQL_DB"] = config.MYSQL_DB
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["JWT_SECRET"] = config.JWT_SECRET
    app.config["JWT_EXPIRY_HOURS"] = config.JWT_EXPIRY_HOURS
    app.config["PASS_PERCENTAGE"] = config.PASS_PERCENTAGE

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(result_bp)
    app.register_blueprint(page_bp)

    app.teardown_appcontext(close_db)

    @app.route("/api/login", methods=["POST"])
    def web_login():
        """Session + JWT login for the web UI."""
        data = request.get_json(silent=True) or request.form.to_dict()
        response, status = login_user(data)

        if status == 200:
            session["user"] = response["username"]
            session["token"] = response["token"]

        return jsonify(response), status

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "message": "Internal server error"}), 500

    with app.app_context():
        try:
            seed_admin_user()
        except Exception:
            pass

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)