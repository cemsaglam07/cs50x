import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash = round(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"], 2)
    rows = db.execute("SELECT symbol, SUM(shares) FROM purchases WHERE user_id = ? GROUP BY symbol", session["user_id"])
    rows = [row for row in rows if row["SUM(shares)"] != 0]
    wallet = cash
    for row in rows:
        row["sum"] = row["SUM(shares)"]
        row["name"] = lookup(row["symbol"])["name"]
        row["price"] = lookup(row["symbol"])["price"]
        row["total"] = round(row["price"] * row["sum"], 2)
        wallet += row["total"]
    return render_template("index.html", rows=rows, cash=cash, wallet=wallet)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        # Ensure symbol is valid
        elif not lookup(request.form.get("symbol")):
            return apology("symbol not valid", 400)
        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)
        elif not request.form.get("shares").isnumeric():
            return apology("shares must be positive", 400)
        symbol = request.form.get("symbol")
        name = lookup(request.form.get("symbol"))["name"]
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be positive", 400)
        price = float(lookup(request.form.get("symbol"))["price"])
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        if (int(request.form.get("shares")) * price) > cash:
            return apology("not enough cash", 400)
        else:
            db.execute("INSERT INTO purchases (user_id, symbol, shares, price) VALUES(?, ?, ?, ?)",
                       session["user_id"], symbol, shares, price)
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (price * shares), session["user_id"])
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    rows = db.execute("SELECT symbol, shares, price, time FROM purchases WHERE user_id = ?", session["user_id"])
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        # Query database for username
        quote = lookup(request.form.get("symbol"))
        # Ensure symbol is valid
        if not quote:
            return apology("symbol not valid", 400)
        # Render page to quoted.html
        return render_template("quoted.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        # Ensure password and confirmation matches
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        # Ensure username is unique
        if len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))) != 0:
            return apology("username taken", 400)
        # Insert user into "users"
        username = request.form.get("username")
        password = request.form.get("password")
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        # Ensure symbol is valid
        elif not lookup(request.form.get("symbol")):
            return apology("symbol not valid", 400)
        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)
        symbol = request.form.get("symbol")
        try:
            shares = 0 - int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be positive", 400)
        price = float(lookup(symbol)["price"])
        # Ensure user has stocks to sell
        checks = db.execute(
            "SELECT symbol, SUM(shares) FROM purchases WHERE user_id = ? AND symbol = ? GROUP BY symbol", session["user_id"], symbol)
        checks = [check for check in checks if check["SUM(shares)"] != 0][0]["SUM(shares)"]
        if abs(int(shares)) > int(checks):
            return apology("insufficient stock to sell", 400)
        # Get cash and remove the stock
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price) VALUES(?, ?, ?, ?)",
                   session["user_id"], symbol, shares, price)
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (price * shares), session["user_id"])
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        rows = db.execute("SELECT symbol, SUM(shares) FROM purchases WHERE user_id = ? GROUP BY symbol", session["user_id"])
        rows = [row for row in rows if row["SUM(shares)"] != 0]
        return render_template("sell.html", rows=rows)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
