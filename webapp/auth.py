from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Book, User, Category, Librarian
from . import db
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        u_name = request.form.get("uname")
        passwd = request.form.get("pass")
        if u_name == "librarian123" and passwd == "librarian@123":
            curr_user = User.query.filter_by(username = "librarian123").first()
            login_user(curr_user, remember = True)
            return redirect(url_for("views.home"))
        else:
            flash("Invalid credentials", category = "error")
    return render_template("login.html", methods = ["GET", "POST"])

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/register", methods = ["GET", "POST"])
@login_required
def register():
    if request.method == 'POST':
        u_name = request.form.get("uname")
        passw = request.form.get("pass")
        c_pass = request.form.get("cpass")
        user = User.query.filter_by(username = u_name).first()
        if passw != c_pass:
            flash("Passwords does not match!!", category="error")
        elif user:
            flash("User already exists", category= "error")
        else:
            new_user = User(username = u_name, password = passw)
            new_user.add()
            
    return render_template("register.html")

@auth.route("/student-login", methods = ['GET', 'POST'])
def student_login():
    if request.method == "POST":
        u_name = request.form.get("uname")
        passwd =  request.form.get("pass")
        user = User.query.filter_by(username = u_name).first()
        if user:
            if user.password == passwd:
                login_user(user, remember = True)
                return redirect(url_for("views.student_home"))
            else:
                flash("Invalid Password", category= "error")
        else:
            flash("User does not exist !! Try signing up", category= 'error')
    return render_template("student_login.html")

