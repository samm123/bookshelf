from flask import Flask, flash, redirect, render_template, request, session
from helpers import get_book

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/register")
def register():

    return render_template("register.html")

@app.route("/login")
def login():

    return render_template("login.html")

@app.route("/add_book")
def add_book():

    return render_template("add_book.html")

@app.route("/lookup", methods=["GET", "POST"])
def lookup():

    # If form is submitted
    if request.method == "POST":
        
        isbn = request.form.get("isbn")

        info = {}
        info = get_book(isbn)

        print(info)

        if info != None:
            return render_template("add_book_filled.html", author=info['author'], title=info['title'], publisher=info['publisher'], publish_date=info['publish_date'], cover_large=info['cover_large'])
        else:
            return render_template("add_book.html")
    
    else:
        return render_template("lookup.html")