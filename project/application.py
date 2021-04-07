import os
import methods
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, login_required

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bio50.db")

# Constant variable names:
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

# Configure application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@login_required
def index():
    cards = db.execute("SELECT id, scp, title, bodytext, txtin, txtgiv, txtout, txtret FROM cards")
    for node in cards:
        node["bodytext"] = node["bodytext"].splitlines()
        node["txtin"] = node["txtin"].splitlines()
        node["txtout"] = node["txtout"].splitlines()
    return render_template("index.html", cards=cards)


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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def valid_method(method_name):
    method_name = method_name.lower().strip()
    ext_id = repr(db.execute("SELECT scp FROM cards")).find("{'scp': '" + method_name + "'}")
    return method_name if ext_id != -1 else ""


@app.route("/process", methods=["GET", "POST"])
@login_required
def process():
    """Get text file from user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # ensure method was uploaded
        if not request.form.get("method"):
            return apology("must provide method", 400)
        # query database for method
        method = valid_method(request.form.get("method").lower())
        # Ensure method is method
        if method == "":
            return apology("method not valid", 400)
        # check if the post request has the file part
        if 'file' not in request.files:
            return apology("no file part", 400)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return apology("no selected file", 400)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            db.execute("INSERT INTO files (name, user_id) VALUES(?, ?)", filename, session.get("user_id"))
            ext_id = db.execute("SELECT MAX(id) FROM files WHERE name = ? AND user_id = ?",
                                filename, session.get("user_id"))[0]["MAX(id)"]
            filename = str(filename.rsplit('.', 1)[0].lower()) + f"_({ext_id})." + str(filename.rsplit('.', 1)[1].lower())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # display given file:
            given = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(given, "r") as f:
                given = f.read().splitlines()
            # display returned file
            returned = eval(f"methods.{method}(os.path.join(app.config['UPLOAD_FOLDER'], filename))")
            with open(returned, "r") as f:
                returned = f.read().splitlines()
            # return redirect(url_for('uploaded_file', filename=filename))
            return render_template("processed.html", given=given, returned=returned)

    # user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("process.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
