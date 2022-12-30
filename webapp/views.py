from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from .models import Book, User, Category
from . import db
from flask_login import login_required, login_user, logout_user, current_user
import json
import datetime

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    return render_template("home.html", user = current_user)

@views.route("/home")
@login_required
def student_home():
    return render_template("student_home.html", user = current_user)

@views.route("/add-book", methods = ["POST", "GET"])
@login_required
def add_book():
    
    allcat = Category.query.all()

    if request.method == "POST":
        b_name = request.form.get("b_name")
        b_auth = request.form.get("b_author")
        b_publisher = request.form.get("b_publisher")
        b_publication = request.form.get("b_publication")
        b_p_year = datetime.datetime.strptime(b_publication, '%Y-%m-%d')

        b_cat = request.form.get("b_cat")
        book = Book(title = b_name, author = b_auth, publisher = b_publisher, publication_year = b_p_year, category = b_cat)
        book.add()
        
    return render_template("add_book.html", user = current_user, allcat = allcat)

@views.route("/add-category", methods = ["GET", "POST"])
@login_required
def add_category():

    allcat =  Category.query.all()

    if request.method == "POST":
            new_cat = request.form.get("category")
            cat = Category.query.filter_by(Category = new_cat).first()
            if cat:
                flash("Category already exists", category = "error")
            else:
                add_cat = Category(Category = new_cat)
                add_cat.add()
    return render_template("add_category.html", user = current_user, allcat = allcat)

@views.route("/delete-category", methods = ["POST"])
@login_required
def del_cat():
    cat = json.loads(request.data)
    catID = cat['catID']
    cat = Category.query.get(catID)
    if cat:
        db.session.delete(cat)
        db.session.commit()
    
    return jsonify({})

@views.route("/view-users", methods = ["GET", "POST"])
@login_required
def view_user():
    users = User.query.all()

    return render_template("view_users.html", users = users)

@views.route("/delete-user", methods = ["POST"])
@login_required
def del_user():
    user = json.loads(request.data)
    userID = user['userID']
    user = User.query.get(userID)
    if user:
        db.session.delete(user)
        db.session.commit()
    return jsonify({})

@views.route("/update-user", methods = ["POST", "GET"])
@login_required
def update_user():
    if request.method == "POST":
        userID = request.form.get("userID")
        user =  User.query.get(userID)
        return render_template("update_user.html", user = current_user, update_user = user)
    return jsonify({})

@views.route("/view-books", methods = ["POST", "GET"])
@login_required
def view_books():
    return render_template("view_book.html", user = current_user)