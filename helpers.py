import os
import requests
import urllib.parse
import urllib.request
import json
import textwrap
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# def lookup(term):
#     """Look up quote for isbn."""

#     base_api_link = "https://www.googleapis.com/books/v1/volumes?q=y"
#     user_input = term
#     with urllib.request.urlopen(base_api_link + user_input) as f:
#         text = f.read()

#     decoded_text = text.decode("utf-8")
#     obj = json.loads(decoded_text)

#     return {
#         "title": obj["items"][0]["title"],
#         "description": obj["items"][0]["description"][:900],
#         "infoLink": obj["items"][0]["infoLink"]
#     }

def lookup(term):
    """Look up quote for term."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote_plus(term)}&key={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        volume_info = quote["items"][0]
        return {
            "title": volume_info["volumeInfo"]["title"],
            "description": volume_info["volumeInfo"]["description"],
            "previewLink": volume_info["volumeInfo"]["previewLink"],
            "infoLink": volume_info["volumeInfo"]["infoLink"],
            "subtitle": volume_info["volumeInfo"]["subtitle"],
        }
    except (KeyError, TypeError, ValueError):
        return None

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
