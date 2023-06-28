import os
import requests


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

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_book(isbn):

    # Convert ISBN to string with leading text for use as dictionary key
    isbn_str = "ISBN:" + str(isbn)

    # Contact API

    try:
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
        print(url)
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

     # Parse response

    try:
        info = response.json()

        return {
            "title": info[isbn_str]["title"],
            "author": info[isbn_str]["authors"][0]["name"],
            "publisher": info[isbn_str]["publishers"][0]["name"],
            "publish_date": info[isbn_str]["publish_date"],
            "cover_small": info[isbn_str]["cover"]["small"],
            "cover_large": info[isbn_str]["cover"]["large"]
        }
    except (KeyError, TypeError, ValueError):
        return None