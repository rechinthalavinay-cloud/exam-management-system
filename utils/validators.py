import re


def validate_student(data, is_update=False):
    errors = []

    name = data.get("student_name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    course = data.get("course", "").strip()

    if not is_update or "student_name" in data:
        if not name or len(name) < 2:
            errors.append("Student name must be at least 2 characters")

    if not is_update or "email" in data:
        if not email or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            errors.append("Valid email is required")

    if not is_update or "phone" in data:
        if not phone or not re.match(r"^\d{10}$", phone):
            errors.append("Phone must be exactly 10 digits")

    if not is_update or "course" in data:
        if not course or len(course) < 2:
            errors.append("Course name is required")

    return errors


def validate_exam(data, is_update=False):
    errors = []

    exam_name = data.get("exam_name", "").strip()
    subject = data.get("subject", "").strip()
    total_marks = data.get("total_marks")

    if not is_update or "exam_name" in data:
        if not exam_name or len(exam_name) < 2:
            errors.append("Exam name must be at least 2 characters")

    if not is_update or "subject" in data:
        if not subject or len(subject) < 2:
            errors.append("Subject is required")

    if not is_update or "total_marks" in data:
        try:
            total = int(total_marks)
            if total <= 0 or total > 1000:
                errors.append("Total marks must be between 1 and 1000")
        except (TypeError, ValueError):
            errors.append("Total marks must be a valid number")

    return errors


def validate_result(data, total_marks=None, is_update=False):
    errors = []

    student_id = data.get("student_id")
    exam_id = data.get("exam_id")
    marks = data.get("marks")

    if not is_update or "student_id" in data:
        try:
            if int(student_id) <= 0:
                errors.append("Valid student is required")
        except (TypeError, ValueError):
            errors.append("Valid student is required")

    if not is_update or "exam_id" in data:
        try:
            if int(exam_id) <= 0:
                errors.append("Valid exam is required")
        except (TypeError, ValueError):
            errors.append("Valid exam is required")

    if not is_update or "marks" in data:
        try:
            marks_val = int(marks)
            if marks_val < 0:
                errors.append("Marks cannot be negative")
            if total_marks is not None and marks_val > total_marks:
                errors.append(f"Marks cannot exceed total marks ({total_marks})")
        except (TypeError, ValueError):
            errors.append("Marks must be a valid number")

    return errors


def validate_login(data):
    errors = []
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username:
        errors.append("Username is required")
    if not password:
        errors.append("Password is required")

    return errors
