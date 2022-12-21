from flask import Blueprint, render_template, request, redirect, flash, url_for
from .models import Book, User, Category
from . import db
from flask_login import login_required, login_user, logout_user, current_user
views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    return render_template("home.html")

@views.route("/home")
@login_required
def student_home():
    return render_template("student_home.html")

@views.route("/add-book")
@login_required
def add_book():
    return render_template("add_book.html")

@views.route("/add-category", methods = ["GET", "POST"])
@login_required
def add_category():
    if request.method == "POST":
            new_cat = request.form.get("category")
            cat = Category.query.filter_by(Category = new_cat).first()
            if cat:
                flash("Category already exists", category = "error")
            else:
                add_cat = Category(Category = new_cat)
                add_cat.add()
    return render_template("add_category.html")
    