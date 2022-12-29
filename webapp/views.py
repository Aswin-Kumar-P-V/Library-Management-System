from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from .models import Book, User, Category
from . import db
from flask_login import login_required, login_user, logout_user, current_user
import json

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    return render_template("home.html", user = current_user)

@views.route("/home")
@login_required
def student_home():
    return render_template("student_home.html", user = current_user)

@views.route("/add-book")
@login_required
def add_book():
    return render_template("add_book.html", user = current_user)

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