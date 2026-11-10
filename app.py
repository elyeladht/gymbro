from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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

        # Check entries (username, email, password)
        # Create session from user_id
        # Redirect to homepage

        # username = request.form.get("username", "").strip()
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