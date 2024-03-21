from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Keeping the below code from previous project so it can be refered to easily.

# The parameters here must be the same as the ones in database meaning if you
# change something in the database on DBeaver (or whatever you use), make sure
# change it here.

# The "User" class will likely look similar across apps that have a user login

class Shirt(db.Model):
    shirt_id = db.Column(db.Integer, primary_key=True)
    shirt_name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(150), nullable=False)
    primary_color = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    times_worn = db.Column(db.Integer, nullable=False)
    last_time_worn = db.Column(db.String(50), default=func.now())
    worn_to_most = db.Column(db.String(50))
    wear_to_work = db.Column(db.String(50))
    wear_to_school = db.Column(db.String(50))
    wear_to_errands = db.Column(db.String(50))
    wear_to_going_out = db.Column(db.String(50))
    wear_to_exercise = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    todays_outfit = db.relationship('Todays_Outfit')
    random_clothes = db.relationship('Random_Clothes')

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
