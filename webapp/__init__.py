from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "LMS.db"
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "@swin239"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views
    from .auth import auth
    
    if not path.exists("instance\\LMS.db"):
        with app.app_context():
            from .models import User, Book
            db.create_all()
            print("Database created")
    

    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")
    
    return app