from flask import Blueprint, render_template, request, redirect, flash, url_for
from .models import Book, User, Category
from . import db

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/home")
def student_home():
    return render_template("student_home.html")

@views.route("/add-book")
def add_book():
    return render_template("add_book.html")

@views.route("/add-category", methods = ["GET", "POST"])
def add_category():
    if request.method == "POST":
        new_cat = request.form.get("category")
        cat = Category.query.filter_by(Category = new_cat).first()
        if cat:
            flash("Category already exists", category = "error")
        else:
            add_cat = Category(Category = new_cat)
            db.session.add(add_cat)
            db.session.commit()
            flash("Category successfully added", category = "success")
    return render_template("add_category.html")
    