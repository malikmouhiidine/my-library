# importing os library to access envirement variables and some common functions
import os
# importing datetime for date formats and time helpers
import datetime
# importing SQL for an easy connection to the database
# in another words "Wrap SQLAlchemy to provide a simple SQL API."
from cs50 import SQL
# this is basically the framework
from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_from_directory
# to configure session to use filesystem (instead of signed cookies)
from flask_session import Session
from tempfile import mkdtemp
# hashing passwords and exceptions handling
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
# helpers functions
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


# handling what's going to happen when the root is visited
@app.route("/")
# login is required to visit this directory
# if the user is not log in it's going to be redirected to the login page
@login_required
# the function that's going to be called when this directory get's visited
def index():
    """Show the Books of the user"""
    # query that going to select all the rows in the books table where id column equal the user id
    # and storing all these rows in a "rows" variable
    rows = db.execute("SELECT * FROM books WHERE id = :id", id=session["user_id"])
    # initializing length to zero and where going to use it in the for loop
    length=0
    # for loop to khow how much rows is there 
    for row in rows:
        length += 1
    print(str(length)) # debugging output
    # rendering index.html template and passing rows and length the it's going to be a for loop there(jinja) as well
    return render_template("index.html", rows=rows, length=length)


# handling what's going to happen when this directory is visited
@app.route("/search", methods=["GET", "POST"])
# login is required to visit this directory
# if the user is not log in it's going to be redirected to the login page
@login_required
# the function that's going to be called when this directory get's visited
def search():
    """Giving the user the ability to search for a book."""
    # first of all if the method is get so he just want to get the page
    if request.method == "GET":
        return render_template("search.html") # so where going to render the page for him
    # but if the method is post that's another story
    else:
        # first checking if the form is messing something
        if not request.form.get("term") and not request.form.get("title") and not request.form.get("description"):
            # if it is return an apology using apology function from helpers.py
            return apology("Must provide an term", 403)
        # now if he got the result and he is on the searched page now and want to add this book
        elif request.form.get("title") and request.form.get("description"):
            now =datetime.datetime.now()
            date= now.strftime("%d/%m/%Y") # getting the date and formatting it in a simple form
            # query to insert the book with all the necessary informations
            db.execute(
                "INSERT INTO books (id, title, url, description, date) VALUES(:id, :title, :url, :description, :date)",
                                                                                                    id=session["user_id"],
                                                                                                    title=request.form.get("title"),
                                                                                                    url=request.form.get("url"),
                                                                                                    description=request.form.get("description"),
                                                                                                    date=date
                                                                                                    )
            # redirect to the home directory
            return redirect("/")

        # so nothing above is true so he just provided the term and want to searh for it
        else:
            # store the term first in "term"
            term = request.form.get("term")
            # render the searched template and passing the variable term and the lookup function
            return render_template("searched.html", term=term, lookup=lookup)


# handling what's going to happen when this directory is visited
@app.route("/addabook", methods=["GET", "POST"])
# login is required to visit this directory
# if the user is not log in it's going to be redirected to the login page
@login_required
# the function that's going to be called when this directory get's visited
def add():
    """add a book to the list"""
    # first of all if the method is get so he just want to get the page
    if request.method == "GET":
        # render it for him
        return render_template("addabook.html")
    # else if he already there and want to POST
    else:
        # check first if he entered all the required fields
        if not request.form.get("title") or not request.form.get("url"):
            # if he not return an apology
            return apology("missing something", 403)
        # else check if he(the user) respected the limit of words accepted
        elif len(request.form.get("description").split()) >= 300 or len(request.form.get("url").split()) >= 100 or len(request.form.get("title").split()) >= 100:
            # if he not return an apology
            return apology("more than 300 words", 403)

        # else if everything is fine
        else:
            # get the time and date now
            now =datetime.datetime.now()
            date= now.strftime("%d/%m/%Y")
            # insert to the books table a row with the book title and url and description and date and of course his(the user) id
            db.execute(
                "INSERT INTO books (id, title, url, description, date) VALUES(:id, :title, :url, :description, :date)",
                                                                                                    id=session["user_id"],
                                                                                                    title=request.form.get("title"),
                                                                                                    url=request.form.get("url"),
                                                                                                    description=request.form.get("description"),
                                                                                                    date=date
                                                                                                    )
            return redirect("/")


# handling what's going to happen when this directory is visited
@app.route("/delete", methods=["GET", "POST"])
# login is required to visit this directory
# if the user is not log in it's going to be redirected to the login page
@login_required
# the function that's going to be called when this directory get's visited
def delete():
    """delete a book from the list"""
    # first of all if the method is get so he just want to get the page
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



# handling what's going to happen when this directory is visited
@app.route("/register", methods=["GET", "POST"])
def register():
    # the function that's going to be called when this directory get's visited
    """Register user"""
    # first of all if the method is get so he just want to get the page
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



# handling what's going to happen when this directory is visited
@app.route("/login", methods=["GET", "POST"])
def login():
    # the function that's going to be called when this directory get's visited
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


# handling what's going to happen when this directory is visited
@app.route("/logout")
# the function that's going to be called when this directory get's visited
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