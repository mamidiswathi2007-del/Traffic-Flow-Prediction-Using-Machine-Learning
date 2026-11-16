import os
import sqlite3
from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash,
    current_app
)
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

def get_db():
    db_folder = os.path.join(current_app.root_path, "database")
    os.makedirs(db_folder, exist_ok=True)

    db_path = os.path.join(db_folder, "users.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login to access this page.", "error")
            return redirect(url_for("auth.login"))
        return function(*args, **kwargs)
    return wrapper

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect("/dashboard")

        flash("Invalid email or password.", "error")

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not name or not email or not password:
            flash("Please fill all fields.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        elif len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
        else:
            conn = get_db()
            try:
                conn.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, generate_password_hash(password))
                )
                conn.commit()
                flash("Registration successful. Please login.", "success")
                conn.close()
                return redirect(url_for("auth.login"))
            except sqlite3.IntegrityError:
                flash("This email is already registered.", "error")
            finally:
                conn.close()

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))