from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Keeping the below code from previous project so it can be refered to easily.

# The parameters here must be the same as the ones in database meaning if you
# change something in the database on DBeaver (or whatever you use), make sure
# change it here.

# The "User" class will likely look similar across apps that have a user login

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)

class User_Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    feedback = db.Column(db.String(10000))
