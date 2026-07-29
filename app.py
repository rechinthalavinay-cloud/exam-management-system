from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# ---------------------------
# MySQL Configuration
# ---------------------------
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Root@123"
app.config["MYSQL_DB"] = "exam_db"

app.secret_key = "exam_secret_key"

mysql = MySQL(app)

# ===========================
# HOME PAGE
# ===========================

@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

    return render_template("index.html")
# ===========================
# LOGIN
# ===========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()

        if user:
            session["user"] = username
            return redirect("/")

        return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html")
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")

# ===========================
# STUDENT CRUD
# ===========================

# View Students
@app.route("/students")
def students():

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()

    return render_template("students.html", students=students)


# Add Student
@app.route("/add_student", methods=["POST"])
def add_student():

    student_name = request.form["student_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    course = request.form["course"]

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (student_name,email,phone,course)
        VALUES(%s,%s,%s,%s)
    """,(student_name,email,phone,course))

    mysql.connection.commit()
    cursor.close()

    flash("Student added successfully!", "success")
    return redirect("/students")


# Edit Student
@app.route("/edit_student/<int:id>")
def edit_student(id):

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM students WHERE id=%s",(id,))

    student = cursor.fetchone()

    cursor.close()

    return render_template("edit_student.html", student=student)


# Update Student
@app.route("/update_student/<int:id>", methods=["POST"])
def update_student(id):

    student_name = request.form["student_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    course = request.form["course"]

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE students
        SET student_name=%s,
            email=%s,
            phone=%s,
            course=%s
        WHERE id=%s
    """,(student_name,email,phone,course,id))

    mysql.connection.commit()
    cursor.close()

    return redirect("/students")


# Delete Student
@app.route("/delete_student/<int:id>")
def delete_student(id):

    cursor = mysql.connection.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s",(id,))

    mysql.connection.commit()
    cursor.close()

    return redirect("/students")

# ===========================
# EXAM CRUD
# ===========================

# View Exams
@app.route("/exams")
def exams():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM exams")

    exams = cursor.fetchall()

    cursor.close()

    return render_template("exams.html", exams=exams)


# Add Exam
@app.route("/add_exam", methods=["POST"])
def add_exam():

    exam_name = request.form["exam_name"]
    subject = request.form["subject"]
    total_marks = request.form["total_marks"]

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO exams
        (exam_name,subject,total_marks)
        VALUES(%s,%s,%s)
    """,(exam_name,subject,total_marks))

    mysql.connection.commit()
    cursor.close()

    return redirect("/exams")


# Edit Exam
@app.route("/edit_exam/<int:id>")
def edit_exam(id):

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM exams WHERE id=%s",(id,))

    exam = cursor.fetchone()

    cursor.close()

    return render_template("edit_exam.html", exam=exam)


# Update Exam
@app.route("/update_exam/<int:id>", methods=["POST"])
def update_exam(id):

    exam_name = request.form["exam_name"]
    subject = request.form["subject"]
    total_marks = request.form["total_marks"]

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE exams
        SET exam_name=%s,
            subject=%s,
            total_marks=%s
        WHERE id=%s
    """,(exam_name,subject,total_marks,id))

    mysql.connection.commit()
    cursor.close()

    return redirect("/exams")


# Delete Exam
@app.route("/delete_exam/<int:id>")
def delete_exam(id):

    cursor = mysql.connection.cursor()

    cursor.execute("DELETE FROM exams WHERE id=%s",(id,))

    mysql.connection.commit()
    cursor.close()

    return redirect("/exams")
# ===========================
# RESULTS CRUD
# ===========================

@app.route("/results")
def results():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM exams")
    exams = cursor.fetchall()

    cursor.execute("""
        SELECT
            results.id,
            students.student_name,
            exams.exam_name,
            results.marks
        FROM results
        INNER JOIN students
        ON results.student_id = students.id
        INNER JOIN exams
        ON results.exam_id = exams.id
    """)

    results = cursor.fetchall()

    cursor.close()

    return render_template(
        "results.html",
        students=students,
        exams=exams,
        results=results
    )
@app.route("/add_result", methods=["POST"])
def add_result():

    student_id = request.form["student_id"]
    exam_id = request.form["exam_id"]
    marks = request.form["marks"]

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO results
        (student_id, exam_id, marks)
        VALUES(%s, %s, %s)
    """, (student_id, exam_id, marks))

    mysql.connection.commit()
    cursor.close()

    return redirect("/results")
@app.route("/edit_result/<int:id>")
def edit_result(id):

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM exams")
    exams = cursor.fetchall()

    cursor.execute("SELECT * FROM results WHERE id=%s", (id,))
    result = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_result.html",
        result=result,
        students=students,
        exams=exams
    )
@app.route("/update_result/<int:id>", methods=["POST"])
def update_result(id):

    student_id = request.form["student_id"]
    exam_id = request.form["exam_id"]
    marks = request.form["marks"]

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE results
        SET student_id=%s,
            exam_id=%s,
            marks=%s
        WHERE id=%s
    """, (student_id, exam_id, marks, id))

    mysql.connection.commit()
    cursor.close()

    return redirect("/results")
@app.route("/delete_result/<int:id>")
def delete_result(id):

    cursor = mysql.connection.cursor()

    cursor.execute("DELETE FROM results WHERE id=%s", (id,))

    mysql.connection.commit()
    cursor.close()

    return redirect("/results")


# ===========================
# RUN APPLICATION
# ===========================

if __name__ == "__main__":
    app.run(debug=True)