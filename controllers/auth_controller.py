from models.database import get_db
from utils.auth import create_token, hash_password, verify_password
from utils.validators import validate_login


def login_user(data):
    errors = validate_login(data)
    if errors:
        return {"success": False, "message": errors[0]}, 400

    username = data["username"].strip()
    password = data["password"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not verify_password(user["password"], password):
        return {"success": False, "message": "Invalid username or password"}, 401

    token = create_token(username)
    return {
        "success": True,
        "message": "Login successful",
        "token": token,
        "username": username,
    }, 200


def seed_admin_user():
    """Create default admin if no users exist."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM users")
    count = cursor.fetchone()["count"]

    if count == 0:
        hashed = hash_password("admin123")
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            ("admin", hashed),
        )
        db.commit()

    cursor.close()
