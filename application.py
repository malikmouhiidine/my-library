import os

import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_from_directory
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
db = SQL("sqlite:///library.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")



@app.route("/")
@login_required
def index():
    """Show the Books of the user"""
    rows = db.execute("SELECT * FROM books WHERE id = :id", id=session["user_id"])
    length=0
    for row in rows:
        length += 1
    print(str(length))
    return render_template("index.html", rows=rows, length=length)





@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("search.html")
    else:
        if not request.form.get("term") and not request.form.get("title") and not request.form.get("description"):
            return apology("Must provide an term", 403)

        elif request.form.get("title") and request.form.get("description"):
            now =datetime.datetime.now()
            date= now.strftime("%d/%m/%Y")
            db.execute(
                "INSERT INTO books (id, title, url, description, date) VALUES(:id, :title, :url, :description, :date)",
                                                                                                    id=session["user_id"],
                                                                                                    title=request.form.get("title"),
                                                                                                    url=request.form.get("url"),
                                                                                                    description=request.form.get("description"),
                                                                                                    date=date
                                                                                                    )
            return redirect("/")


        else:
            term = request.form.get("term")
            return render_template("searched.html", term=term, lookup=lookup)



@app.route("/addabook", methods=["GET", "POST"])
@login_required
def add():
    """add a book"""
    if request.method == "GET":
        return render_template("addabook.html")
    else:
        if not request.form.get("title") or not request.form.get("url"):
                return apology("missing something", 403)

        elif len(request.form.get("description").split()) >= 300 or len(request.form.get("url").split()) >= 100 or len(request.form.get("title").split()) >= 100:
            return apology("more than 300 words", 403)


        else:
            now =datetime.datetime.now()
            date= now.strftime("%d/%m/%Y")
            db.execute(
                "INSERT INTO books (id, title, url, description, date) VALUES(:id, :title, :url, :description, :date)",
                                                                                                    id=session["user_id"],
                                                                                                    title=request.form.get("title"),
                                                                                                    url=request.form.get("url"),
                                                                                                    description=request.form.get("description"),
                                                                                                    date=date
                                                                                                    )
            return redirect("/")



@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """delete a book"""
    if request.method == "GET":
        rows= db.execute("SELECT * FROM books WHERE id = :id", id=session["user_id"])
        length=0
        for row in rows:
            length += 1
        return render_template("delete.html", rows=rows, length=length)
    else:
        if not request.form.get("title"):
                return apology("missing something", 403)


        else:
            db.execute(
                "DELETE FROM books WHERE id=:id AND title=:title", id=session["user_id"], title=request.form.get("title"))
            return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("username") or not request.form.get("password"):
            return apology("Must provide a username and a password and confirm that password, please be sure to do all these steps", 403)
        elif not request.form.get("password") == request.form.get("confirmation") :
            print(request.form.get("password"))
            print(request.form.get("confirmation"))
            return apology("Please make sure that the confirmation match the password", 403)
        else:
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            if len(rows) == 1:
                return apology("Username already exists", 403)
            else:
                hash = generate_password_hash(request.form.get("password"))
                db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hash)
    return redirect("/")




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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)




@app.route('/favicon.ico')
def favicon():
    app.send_static_file('favicon.ico')