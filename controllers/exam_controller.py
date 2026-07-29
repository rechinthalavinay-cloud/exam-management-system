from models.database import get_db
from utils.validators import validate_exam


def get_all_exams():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM exams ORDER BY id DESC")
    exams = cursor.fetchall()
    cursor.close()
    return {"success": True, "data": exams}, 200


def get_exam(exam_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM exams WHERE id = %s", (exam_id,))
    exam = cursor.fetchone()
    cursor.close()

    if not exam:
        return {"success": False, "message": "Exam not found"}, 404

    return {"success": True, "data": exam}, 200


def create_exam(data):
    errors = validate_exam(data)
    if errors:
        return {"success": False, "message": errors[0]}, 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO exams (exam_name, subject, total_marks)
        VALUES (%s, %s, %s)
        """,
        (
            data["exam_name"].strip(),
            data["subject"].strip(),
            int(data["total_marks"]),
        ),
    )
    db.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM exams WHERE id = %s", (new_id,))
    exam = cursor.fetchone()
    cursor.close()
    return {"success": True, "message": "Exam created", "data": exam}, 201


def update_exam(exam_id, data):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM exams WHERE id = %s", (exam_id,))
    if not cursor.fetchone():
        cursor.close()
        return {"success": False, "message": "Exam not found"}, 404

    errors = validate_exam(data, is_update=True)
    if errors:
        cursor.close()
        return {"success": False, "message": errors[0]}, 400

    cursor.execute(
        """
        UPDATE exams
        SET exam_name = %s, subject = %s, total_marks = %s
        WHERE id = %s
        """,
        (
            data["exam_name"].strip(),
            data["subject"].strip(),
            int(data["total_marks"]),
            exam_id,
        ),
    )
    db.commit()
    cursor.execute("SELECT * FROM exams WHERE id = %s", (exam_id,))
    exam = cursor.fetchone()
    cursor.close()
    return {"success": True, "message": "Exam updated", "data": exam}, 200


def delete_exam(exam_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM exams WHERE id = %s", (exam_id,))
    if not cursor.fetchone():
        cursor.close()
        return {"success": False, "message": "Exam not found"}, 404

    cursor.execute("DELETE FROM exams WHERE id = %s", (exam_id,))
    db.commit()
    cursor.close()
    return {"success": True, "message": "Exam deleted"}, 200
