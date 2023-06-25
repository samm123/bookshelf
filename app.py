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

    isbn = request.form.get("isbn")

    info = {}
    info = get_book(isbn)

    print(info)

    print(info[f'ISBN:{str(isbn)}']['title'])

    return render_template("lookup.html")