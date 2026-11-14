from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import math

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gym.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return redirect("/homepage")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register in app"""

    if request.method == "POST":
        # Check entries (username, email, password)
        # Add new user to database
        # Create session from user_id
        # Redirect to homepage

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username:
            return apology("Please enter a username", 400)

        if not password:
            return apology("Please enter a password", 400)

        if not confirm_password:
            return apology("Please confirm password", 400)
        
        if not email:
            return apology("Please enter your email", 400)

        if '@' not in email:
            return apology("Please enter a valid email", 400)

        if len(password) < 8:
            return apology("Password must contain at least 8 characters", 400)
        
        if password != confirm_password:
            return apology("Passwords do not match", 400)

        if db.execute("SELECT 1 FROM users WHERE email = ?", email):
            return apology("Email already registered", 400)
        
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",  username
        )

        if len(rows) != 0:
            return apology("Username already exists", 400)

        user_id = db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", username, email, generate_password_hash(password))

        session["user_id"] = user_id

        return redirect("/homepage")

    else:
        # GET method: load page
        return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        # Check entries (email, password)
        # Create session from user_id
        # Redirect to homepage

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")

        if not password:
            return apology("Please enter your password", 403)
        
        if not email:
            return apology("Please enter your email", 403)

        if '@' not in email:
            return apology("Email not valid", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE email = ?",  email
        )

        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
            return apology("Invalid email and/or password", 403)

        session["user_id"] = rows[0]["user_id"]

        return redirect("/homepage")

    else:
        # GET method: load page
        return render_template("login.html")

@app.route("/logout", methods = ["POST"])
@login_required
def logout():
    session.clear()
    return redirect("/login")


@app.route("/homepage", methods = ["GET"])
@login_required
def homepage():
    # if request.method == "POST":
    return render_template("homepage.html")
@app.route("/log", methods=["GET", "POST"])
@login_required
def log():
    if request.method == "POST":
        exercise_id = request.form.get("exercise_id")

        try:
            weight = float(request.form.get("weight"))
            reps = int(request.form.get("reps"))
        except (ValueError, TypeError):
            return apology("Weight and repetitions must be numbers")

        if not math.isfinite(weight) or weight < 0:
            return apology("Weight must be 0 or more")

        if reps < 1:
            return apology("Repetitions must be at least 1")

        if not db.execute("SELECT 1 FROM exercises WHERE exercise_id = ?", exercise_id):
            return apology("Exercise does not exist")

        db.execute(
            "INSERT INTO workout_log (user_id, exercise_id, weight, reps) VALUES (?, ?, ?, ?)",
            session["user_id"], exercise_id, weight, reps
        )

        flash("Set saved!")
        return redirect("/log")

    exercises = db.execute(
        "SELECT exercise_id, exercise_name FROM exercises ORDER BY exercise_name"
    )
    return render_template("log.html", exercises=exercises)

@app.route("/history")
@login_required
def history():
    # Join tables exercises and workout_log to extract exercise_name, weight, reps and recorded_at columns
    sets = db.execute(
        """
        SELECT e.exercise_name, w.weight, w.reps,
            datetime(w.recorded_at, 'localtime') AS recorded_at
        FROM workout_log w
        JOIN exercises e ON e.exercise_id = w.exercise_id
        WHERE w.user_id = ?
        ORDER BY w.recorded_at DESC, w.log_id DESC
        """,
        session["user_id"]
    )
    return render_template("history.html", sets=sets) 