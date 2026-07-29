import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Root@123")
MYSQL_DB = os.getenv("MYSQL_DB", "exam_db")

SECRET_KEY = os.getenv("SECRET_KEY", "exam_secret_key_change_in_production")
JWT_SECRET = os.getenv("JWT_SECRET", "jwt_secret_key_change_in_production")
JWT_EXPIRY_HOURS = 24

PASS_PERCENTAGE = 40
