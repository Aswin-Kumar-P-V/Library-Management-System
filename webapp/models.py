from . import db
from flask_login import UserMixin
from flask import Blueprint, render_template, request, redirect, flash, url_for

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    publisher = db.Column(db.String(200))
    publication = db.Column(db.String(200))
    category = db.Column(db.String(200))
    status = db.Column(db.String(200))
    borrowed_date = db.Column(db.DateTime)
    return_by = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User( db.Model, UserMixin):
    id = db.Column(db.Integer,  primary_key = True)
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    books = db.relationship("Book")
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        flash("Account created", category = "success")

class Category( db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Category = db.Column(db.String(150), unique = True)

    def add(self):
        db.session.add(self)
        db.session.commit()
        flash("Category successfully added", category = "success")

