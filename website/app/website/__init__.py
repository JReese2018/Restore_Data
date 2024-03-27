from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import datetime

db = SQLAlchemy()

# Name of database (Whatever you want inside the quotes)

DB_NAME = "restore"

# If you want to put a date (Not Required)

now = datetime.now() 
date_time = now.strftime("%m/%d/%Y")

# 'secretKey' can be anything

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:password@localhost/{DB_NAME}'
    db.init_app(app)



    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')    
    app.register_blueprint(auth, url_prefix='/')

    # Not sure if below line is necceary

    from .models import User, User_Feedback # Tables from Database

    create_database(app)

    # Need  below for loging in User
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# This creates the database (I use DBeaver and it pops up after refreshing)

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')