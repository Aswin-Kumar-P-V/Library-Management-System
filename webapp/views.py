from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, session
from .models import Book, User, Category
from . import db
from flask_login import login_required, login_user, logout_user, current_user
import json
import datetime 
import re

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    return render_template("home.html", user = current_user)

@views.route("/home")
@login_required
def student_home():
    books1 = Book.query.all()
    return render_template("student_home.html", user = current_user, books1 = books1)

@views.route("/add-book", methods = ["POST", "GET"])
@login_required
def add_book():

    if request.method == "POST":
        b_name = request.form.get("b_name")
        b_auth = request.form.get("b_author")
        b_publisher = request.form.get("b_publisher")
        b_publication = request.form.get("b_publication")
        b_p_year = datetime.datetime.strptime(b_publication, '%Y-%m-%d')
        b_cat = request.form.get("cat")
        b_count = request.form.get("b_no")

        book = Book(title = b_name, author = b_auth, publisher = b_publisher, publication_year = b_p_year, category = b_cat, status = "Available", count = b_count)
        book.add()
        
    allcat = Category.query.all()

    return render_template("add_book.html", user = current_user, allcat = allcat)

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
        
    allcat =  Category.query.all()
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
    users.pop(0)
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

@views.route("/view-update-user", methods = ["POST", "GET"])
@login_required
def update_user():
    userID = request.form.get("userID")
    user =  User.query.get(userID)
    return render_template("view_update_user.html", user = current_user, update_user = user)

@views.route("/view-books", methods = ["POST", "GET"])
@login_required
def view_books():
    books = Book.query.all()
    return render_template("view_book.html", user = current_user, books = books)

@views.route("/update-user", methods  = ["POST", "GET"])
@login_required
def update_user_details():
    users = User.query.all()
    if request.method == "POST":
        uName = request.form.get("Uname")
        uPass = request.form.get("Pass")
        uID = request.form.get("UID")
        user = User.query.get(int(uID))
        check_user = User.query.filter_by(username = uName).first()
        if check_user and check_user.id != user.id:
            flash("Username exists try again", category= "error")
            return redirect(url_for("views.update_user_details"))
        else:
            user.username =  uName
            user.password = uPass
            db.session.commit()
        flash("User details updated", category="success")
    users.pop(0)
    return render_template("view_users.html", users = users)

@views.route("/delete-book", methods = ["POST"])
@login_required
def delete_book():
    book = json.loads(request.data)
    bookID = book['bookID']
    book = Book.query.get(bookID)
    if book:
        db.session.delete(book)
        db.session.commit()
    return jsonify({})

@views.route("/search-book", methods = ["POST", "GET"])
@login_required

def search_book():
    if request.method == "POST":
        title = request.form.get("search")
        title = title.strip()

        if title == "":
            flash("Give some valid input", category="error")
            return render_template("search_book.html", user = current_user)
            
        obBook = Book()
        books = obBook.search(title = title)
       
        if books:
            return render_template("search_book.html", user = current_user, books = books)
    return render_template("search_book.html", user = current_user)

@views.route("/search-book-user", methods = ["POST", "GET"])
@login_required

def search_book_user():
    if request.method == "POST":
        title = request.form.get("search")
        title = title.strip()

        if title == "":
            flash("Give some valid input", category= "error")
            return render_template("student_home.html", user = current_user)
        obBook = Book()
        books = obBook.search(title = title)
        if books:
            return render_template("student_home.html", user = current_user, books = books)
    books1 = Book.query.all()
    return render_template("student_home.html", user = current_user, books1 = books1)            


@views.route("/select-issue-book", methods = ["POST", "GET"])
@login_required

def select_issue_book():
    if request.method == "POST":
        title = request.form.get("search")
        title = title.strip()

        if title == "":
            flash("Give some valid input", category= "error")
            return render_template("select_issue_book.html", user = current_user)
        obBook = Book()
        books = obBook.search(title = title)
        if books:
            return render_template("select_issue_book.html", user = current_user, books = books)
    books = Book.query.all()
    return render_template("select_issue_book.html", user = current_user, books1 = books)

@views.route("/select-issue-user", methods = ["POST", "GET"])
@login_required

def select_issue_user():
    if request.method == "POST":

        bookId = request.form.get("bookID")
        book = Book.query.get(bookId)
        if book.status != "Available":
            flash("Book no available!!", category="error")
            books = Book.query.all()
            return render_template("select_issue_book.html", user = current_user, books1 = books)
        
        session["bookId"] = bookId
        users = User.query.all()
        users.pop(0)
        book = Book.query.get(bookId)
        return render_template("select_issue_user.html", bookId = bookId, users = users, book = book)
    return render_template("select_issue_user.html")

@views.route("/issue-book", methods  = ["POST", "GET"])
@login_required

def issue_book():
    if request.method == "POST":
        if "bookId" in session:
            bookId = session["bookId"]
            userId = request.form.get("userId")
            
            user = User.query.get(userId)
            book = Book.query.get(bookId)
            if user.No_Books < 3:
                date =datetime.date.today()
                date1 = date +datetime.timedelta(days=7)
                
                session["b_date"] = date
                session["r_date"] = date1
                
                return render_template("issue_book_final.html", user = user, book = book, date = date, date1 = date1)
            else:
                users = User.query.all()
                users.pop(0)
                flash("Maximum no of books alloted for this user", category="error")
                return render_template("select_issue_user.html", bookId = bookId, users = users, book = book)
    return render_template("issue-book-final.html")

@views.route("/confirm-issue-book", methods = ["POST", "GET"])
@login_required

def confirm_issue_book():
    if request.method == "POST":
        if "bookId" in session:
            bookId = session["bookId"]
            userId = request.form.get("userId")

            user = User.query.get(userId)
            book = Book.query.get(bookId)

            
            if user.No_Books == 0 :
                user.book1 = book.title
                user.book1Borrow = datetime.datetime.today()
                user.book1Return = datetime.datetime.today() +datetime.timedelta(days=7)
                user.No_Books += 1  
                
            elif user.No_Books == 1:
                user.book2 = book.title
                user.book2Borrow = datetime.datetime.today()
                user.book2Return = datetime.datetime.today() +datetime.timedelta(days=7)
                user.No_Books += 1 
                
            elif user.No_Books == 2:
                user.book3 = book.title
                user.book3Borrow = datetime.datetime.today()
                user.book3Return = datetime.datetime.today() +datetime.timedelta(days=7)
                user.No_Books += 1 
            
            db.session.commit()

            book.count -= 1
            if book.count == 0:
                book.status = "Not Available"
            db.session.commit()
            flash("Book allocated", category="success")
            books = Book.query.all()
            return render_template("select_issue_book.html", user = current_user, books1 = books)

    books = Book.query.all()
    return render_template("select_issue_book.html", user = current_user, books1 = books)

@views.route("/return-book", methods = ["POST", "GET"])
@login_required

def return_book():
    if request.method == "POST":
        userId = request.form.get("userID")
        user = User.query.get(userId)
        return render_template("return_book.html", user = user)
    users = User.query.all()
    users.pop(0)
    return render_template("return_book.html", users = users)

@views.route("/return-book-submit", methods = ["POST", "GET"])
@login_required

def return_book_submit():
    if request.method == "POST":
        bookID = request.form.get("bookId")
        flash(bookID, category="success")
        redirect(url_for("views.home"))
    return jsonify({})
    