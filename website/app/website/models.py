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
    counter = db.relationship('Counter')
    month_comparison = db.relationship('Month_Comparison')

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

class Month_Comparison(db.Model):
    month_comparison_id = db.Column(db.Integer, primary_key=True)
    previous_membership_count = db.Column(db.Integer, nullable=False)
    previous_discover_count = db.Column(db.Integer, nullable=False)
    previous_levelup_count = db.Column(db.Integer, nullable=False)
    previous_elevate_count = db.Column(db.Integer, nullable=False)
    previous_core_count = db.Column(db.Integer, nullable=False)
    previous_restore_count = db.Column(db.Integer, nullable=False)
    previous_restorecouples_count = db.Column(db.Integer, nullable=False)
    previous_wellness_count = db.Column(db.Integer, nullable=False)
    previous_wellnesscouples_count = db.Column(db.Integer, nullable=False)
    previous_daily_count = db.Column(db.Integer, nullable=False)
    current_membership_count = db.Column(db.Integer, nullable=False)
    current_discover_count = db.Column(db.Integer, nullable=False)
    current_levelup_count = db.Column(db.Integer, nullable=False)
    current_elevate_count = db.Column(db.Integer, nullable=False)
    current_core_count = db.Column(db.Integer, nullable=False)
    current_restore_count = db.Column(db.Integer, nullable=False)
    current_restorecouples_count = db.Column(db.Integer, nullable=False)
    current_wellness_count = db.Column(db.Integer, nullable=False)
    current_wellnesscouples_count = db.Column(db.Integer, nullable=False)
    current_daily_count = db.Column(db.Integer, nullable=False)
    previous_month = db.Column(db.String(150), nullable=False)
    current_month = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
