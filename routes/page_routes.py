from flask import Blueprint, render_template, session, redirect

page_bp = Blueprint("pages", __name__)


def login_required(view):
    def wrapped(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


@page_bp.route("/")
@login_required
def home():
    return render_template("index.html")


@page_bp.route("/login")
def login_page():
    if "user" in session:
        return redirect("/")
    return render_template("login.html")


@page_bp.route("/students")
@login_required
def students_page():
    return render_template("students.html")


@page_bp.route("/exams")
@login_required
def exams_page():
    return render_template("exams.html")


@page_bp.route("/results")
@login_required
def results_page():
    return render_template("results.html")


@page_bp.route("/analytics")
@login_required
def analytics_page():
    return render_template("analytics.html")


@page_bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("token", None)
    return redirect("/login")
