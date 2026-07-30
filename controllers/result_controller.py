from models.database import get_db
from utils.auth import calculate_grade
from utils.validators import validate_result


def _get_exam_total_marks(exam_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT total_marks FROM exams WHERE id = %s", (exam_id,))
    exam = cursor.fetchone()
    cursor.close()
    return exam["total_marks"] if exam else None


def get_all_results():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT
            r.id,
            r.student_id,
            r.exam_id,
            r.marks,
            r.grade,
            r.percentage,
            s.student_name,
            s.email,
            e.exam_name,
            e.subject,
            e.total_marks
        FROM results r
        INNER JOIN students s ON r.student_id = s.id
        INNER JOIN exams e ON r.exam_id = e.id
        ORDER BY r.id ASC
        """
    )
    results = cursor.fetchall()
    cursor.close()
    return {"success": True, "data": results}, 200


def get_result(result_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT
            r.*,
            s.student_name,
            e.exam_name,
            e.total_marks
        FROM results r
        INNER JOIN students s ON r.student_id = s.id
        INNER JOIN exams e ON r.exam_id = e.id
        WHERE r.id = %s
        """,
        (result_id,),
    )
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return {"success": False, "message": "Result not found"}, 404

    return {"success": True, "data": result}, 200


def create_result(data):
    exam_id = int(data["exam_id"])
    total_marks = _get_exam_total_marks(exam_id)
    if total_marks is None:
        return {"success": False, "message": "Exam not found"}, 404

    errors = validate_result(data, total_marks=total_marks)
    if errors:
        return {"success": False, "message": errors[0]}, 400

    marks = int(data["marks"])
    grade, percentage = calculate_grade(marks, total_marks)

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO results (student_id, exam_id, marks, grade, percentage)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (int(data["student_id"]), exam_id, marks, grade, percentage),
        )
        db.commit()
        new_id = cursor.lastrowid
    except Exception as e:
        db.rollback()
        cursor.close()
        if "Duplicate" in str(e):
            return {
                "success": False,
                "message": "Result already exists for this student and exam",
            }, 409
        return {"success": False, "message": "Failed to create result"}, 500

    cursor.execute(
        """
        SELECT r.*, s.student_name, e.exam_name, e.total_marks
        FROM results r
        INNER JOIN students s ON r.student_id = s.id
        INNER JOIN exams e ON r.exam_id = e.id
        WHERE r.id = %s
        """,
        (new_id,),
    )
    result = cursor.fetchone()
    cursor.close()
    return {"success": True, "message": "Result created", "data": result}, 201


def update_result(result_id, data):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM results WHERE id = %s", (result_id,))
    existing = cursor.fetchone()
    if not existing:
        cursor.close()
        return {"success": False, "message": "Result not found"}, 404

    exam_id = int(data.get("exam_id", existing["exam_id"]))
    total_marks = _get_exam_total_marks(exam_id)
    if total_marks is None:
        cursor.close()
        return {"success": False, "message": "Exam not found"}, 404

    errors = validate_result(data, total_marks=total_marks, is_update=True)
    if errors:
        cursor.close()
        return {"success": False, "message": errors[0]}, 400

    marks = int(data["marks"])
    grade, percentage = calculate_grade(marks, total_marks)

    try:
        cursor.execute(
            """
            UPDATE results
            SET student_id = %s, exam_id = %s, marks = %s, grade = %s, percentage = %s
            WHERE id = %s
            """,
            (
                int(data["student_id"]),
                exam_id,
                marks,
                grade,
                percentage,
                result_id,
            ),
        )
        db.commit()
    except Exception as e:
        db.rollback()
        cursor.close()
        if "Duplicate" in str(e):
            return {
                "success": False,
                "message": "Result already exists for this student and exam",
            }, 409
        return {"success": False, "message": "Failed to update result"}, 500

    cursor.execute(
        """
        SELECT r.*, s.student_name, e.exam_name, e.total_marks
        FROM results r
        INNER JOIN students s ON r.student_id = s.id
        INNER JOIN exams e ON r.exam_id = e.id
        WHERE r.id = %s
        """,
        (result_id,),
    )
    result = cursor.fetchone()
    cursor.close()
    return {"success": True, "message": "Result updated", "data": result}, 200


def delete_result(result_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM results WHERE id = %s", (result_id,))
    if not cursor.fetchone():
        cursor.close()
        return {"success": False, "message": "Result not found"}, 404

    cursor.execute("DELETE FROM results WHERE id = %s", (result_id,))
    db.commit()
    cursor.close()
    return {"success": True, "message": "Result deleted"}, 200


def get_analytics():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total_students = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM exams")
    total_exams = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM results")
    total_results = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT grade, COUNT(*) AS count
        FROM results
        GROUP BY grade
        ORDER BY count DESC
        """
    )
    grade_distribution = cursor.fetchall()

    cursor.execute(
        """
        SELECT
            s.student_name,
            AVG(r.percentage) AS avg_percentage,
            COUNT(r.id) AS exams_taken
        FROM students s
        LEFT JOIN results r ON s.id = r.student_id
        GROUP BY s.id, s.student_name
        ORDER BY avg_percentage DESC
        """
    )
    student_performance = cursor.fetchall()

    cursor.execute(
        """
        SELECT
            e.exam_name,
            e.subject,
            AVG(r.percentage) AS avg_percentage,
            MAX(r.percentage) AS highest,
            MIN(r.percentage) AS lowest,
            COUNT(r.id) AS students_count
        FROM exams e
        LEFT JOIN results r ON e.id = r.exam_id
        GROUP BY e.id, e.exam_name, e.subject
        """
    )
    exam_stats = cursor.fetchall()

    cursor.execute(
        """
        SELECT COUNT(*) AS passed
        FROM results
        WHERE grade != 'F'
        """
    )
    passed = cursor.fetchone()["passed"]

    pass_rate = round((passed / total_results * 100), 2) if total_results > 0 else 0

    cursor.close()

    return {
        "success": True,
        "data": {
            "total_students": total_students,
            "total_exams": total_exams,
            "total_results": total_results,
            "pass_rate": pass_rate,
            "grade_distribution": grade_distribution,
            "student_performance": student_performance,
            "exam_stats": exam_stats,
        },
    }, 200
