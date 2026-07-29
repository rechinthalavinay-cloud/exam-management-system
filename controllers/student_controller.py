from models.database import get_db
from utils.validators import validate_student


def get_all_students():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students = cursor.fetchall()
    cursor.close()
    return {"success": True, "data": students}, 200


def get_student(student_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()

    if not student:
        return {"success": False, "message": "Student not found"}, 404

    return {"success": True, "data": student}, 200


def create_student(data):
    errors = validate_student(data)
    if errors:
        return {"success": False, "message": errors[0]}, 400

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students (student_name, email, phone, course)
            VALUES (%s, %s, %s, %s)
            """,
            (
                data["student_name"].strip(),
                data["email"].strip(),
                data["phone"].strip(),
                data["course"].strip(),
            ),
        )
        db.commit()
        new_id = cursor.lastrowid
    except Exception as e:
        db.rollback()
        cursor.close()
        if "Duplicate" in str(e):
            return {"success": False, "message": "Email already exists"}, 409
        return {"success": False, "message": "Failed to create student"}, 500

    cursor.execute("SELECT * FROM students WHERE id = %s", (new_id,))
    student = cursor.fetchone()
    cursor.close()
    return {"success": True, "message": "Student created", "data": student}, 201


def update_student(student_id, data):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    if not cursor.fetchone():
        cursor.close()
        return {"success": False, "message": "Student not found"}, 404

    errors = validate_student(data, is_update=True)
    if errors:
        cursor.close()
        return {"success": False, "message": errors[0]}, 400

    try:
        cursor.execute(
            """
            UPDATE students
            SET student_name = %s, email = %s, phone = %s, course = %s
            WHERE id = %s
            """,
            (
                data["student_name"].strip(),
                data["email"].strip(),
                data["phone"].strip(),
                data["course"].strip(),
                student_id,
            ),
        )
        db.commit()
    except Exception as e:
        db.rollback()
        cursor.close()
        if "Duplicate" in str(e):
            return {"success": False, "message": "Email already exists"}, 409
        return {"success": False, "message": "Failed to update student"}, 500

    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    return {"success": True, "message": "Student updated", "data": student}, 200


def delete_student(student_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM students WHERE id = %s", (student_id,))
    if not cursor.fetchone():
        cursor.close()
        return {"success": False, "message": "Student not found"}, 404

    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    db.commit()
    cursor.close()
    return {"success": True, "message": "Student deleted"}, 200
