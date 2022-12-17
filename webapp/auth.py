from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Book, User, Category
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        u_name = request.form.get("uname")
        passwd = request.form.get("pass")
        if u_name == "librarian123" and passwd == "librarian@123":
            return redirect(url_for("views.home"))
        else:
            flash("Invalid credentials", category = "error")
    return render_template("login.html", methods = ["GET", "POST"])

@auth.route("/logout")
def logout():
    return "<h3>Logout</h3>"

@auth.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == 'POST':
        u_name = request.form.get("uname")
        passw = request.form.get("pass")
        c_pass = request.form.get("cpass")

        user = User.query.filter_by(username = u_name)
        if passw != c_pass:
            flash("Passwords does not match!!", category="error")
        elif user:
            flash("User already exists", category= "error")
        else:
            new_user = User(username = u_name, password = passw)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created", category = "success")
    return render_template("register.html")

@auth.route("/student-login", methods = ['GET', 'POST'])
def student_login():
    if request.method == "POST":
        u_name = request.form.get("uname")
        passwd =  request.form.get("pass")
        user = User.query.filter_by(username = u_name).first()
        if user:
            if user.password == passwd:
                return redirect(url_for("views.student_home"))
            else:
                flash("Invalid Password", category= "error")
        else:
            flash("User does not exist !! Try signing up", category= 'error')
    return render_template("student_login.html")

