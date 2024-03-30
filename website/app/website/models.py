from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Keeping the below code from previous project so it can be refered to easily.

# The parameters here must be the same as the ones in database meaning if you
# change something in the database on DBeaver (or whatever you use), make sure
# change it here.


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)

class User_Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    feedback = db.Column(db.String(10000))

## Would need to add a new column every time you add
class Counter(db.Model):
    counter_id = db.Column(db.Integer, primary_key=True)
    times_used_credit_balance = db.Column(db.Integer, nullable=False)
    times_used_promotions = db.Column(db.Integer, nullable=False)
    times_used_month_comparison = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))