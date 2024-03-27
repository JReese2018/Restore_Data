from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
#from website import date_time
from datetime import datetime
from .models import User, User_Feedback
from . import db

# This file is your backend to all your pages on your app. I left an example on how
# to post things to the database. This also shows how to use the flask functions like
# redirect, url_for, flash, etc.

## The below class allows file uploads. Note, we are not saving any of these files into a database
class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

## This is how we are getting the date and time
now = datetime.now() 
date_time = now.strftime("%m/%d/%Y")

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

## Going to work on this last
@views.route('/info', methods=['GET', 'POST'])
def info():
    return render_template("info.html", user=current_user)

@views.route('/credit-balance', methods=['GET', 'POST'])
def credit_balance():
    form = UploadFileForm()
    return render_template("credit_balance.html", user=current_user, form=form)

## This might be scrapped because tableu has a tab that can be used to get the same data that I was going to do I think
@views.route('/promotions', methods=['GET', 'POST'])
def promotions():
    return render_template("promotions.html", user=current_user)

@views.route('/month-comparison', methods=['GET', 'POST'])
def month_comparison():
    return render_template("month_comparison.html", user=current_user)

@views.route('/feedback', methods=['GET', 'POST'])
def feedback():
    date = date_time
    return render_template("feedback.html", user=current_user, date=date)

