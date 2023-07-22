from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from helpers import get_book, apology, login_required
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///books.db")

@app.route("/")
@login_required
def index():

    # Get all books associated with current user
    books = db.execute("SELECT * FROM books WHERE user_id = ?", session["user_id"])
    
    return render_template("index.html", books=books)

@app.route("/book/<int:id>")
@login_required
def book(id):

    book = db.execute("SELECT * FROM books WHERE book_id = ?", id)

    return render_template("book.html", book=book)

@app.route("/book_edit", methods=["POST"])
@login_required
def book_edit():

    book_id = request.form.get("book_id")

    book = db.execute("SELECT * FROM books WHERE book_id = ?", book_id)

    return render_template("book_edit.html", book=book)

@app.route("/delete_book", methods=["POST"])
@login_required
def delete_book():

    book_id = request.form.get("book_id")

    db.execute("DELETE FROM books WHERE book_id = ?", book_id)

    return redirect("/")


@app.route("/update_book", methods=["POST"])
@login_required
def update_book():

    db.execute("UPDATE books SET (author, title, publisher, year, cover_L) = (?, ?, ?, ?, ?) WHERE book_id = ?", 
               request.form.get("author"), request.form.get("title"), request.form.get("publisher"), request.form.get("year"), request.form.get("cover_L"), request.form.get("book_id"))
    
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User submits registration form (POST)
    if request.method == "POST":
         
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirm password was submitted
        elif not request.form.get("confirmation"):
            return apology("must re-type password", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)
        
        # Query database for exisiting username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not already exist, insert if free
        if len(rows) > 0:
            return apology("Username already taken", 400)
        else:
            phash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", request.form.get("username"), phash)

            return redirect("/login")

    # User reached route via GET
    else:

        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

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

@app.route("/add_book", methods=["POST"])
@login_required
def add_book():

    # Put form data into dictionary
    book_data = {}
    book_data = request.form.to_dict(flat=False)

    # Insert form data into book database
    db.execute("INSERT INTO books (author, title, publisher, year, cover_L, user_id) VALUES (?, ?, ?, ?, ?, ?)", 
               book_data["author"], book_data["title"], book_data["publisher"], book_data["publish_date"], book_data["cover_L"], session["user_id"])

    # Redirect to index
    return redirect("/")

@app.route("/lookup", methods=["GET", "POST"])
def lookup():

    # If form is submitted
    if request.method == "POST":
        
        isbn = request.form.get("isbn")

        info = {}
        info = get_book(isbn) 

        if info != None:
            return render_template("add_book_filled.html", author=info['author'], title=info['title'], publisher=info['publisher'], publish_date=info['publish_date'], cover_large=info['cover_large'])
        else:
            return render_template("add_book.html")
    
    else:
        return render_template("lookup.html")