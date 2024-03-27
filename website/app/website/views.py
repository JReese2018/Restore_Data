from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from website import date_time
from .models import Shoes
from . import db

# This file is your backend to all your pages on your app. I left an example on how
# to post things to the database. This also shows how to use the flask functions like
# redirect, url_for, flash, etc. Feel free to delete this whenever you feel 
# comfortable. You can also reference the wardrobe docs.

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/addnewshoes', methods = ('GET', 'POST'))
@login_required
def addnewshoes():
    if request.method == 'POST':
        shoe_name = request.form['shoe_name']
        brand = request.form['brand']
        primary_color = request.form['primary_color']
        type = request.form['type']
        times_worn = 0
        last_time_worn = "N/A"
        worn_to_most = "N/A"
        wear_to_work = request.form.get('wear_to_work')
        wear_to_school = request.form.get('wear_to_school')
        wear_to_errands = request.form.get('wear_to_errands')
        wear_to_going_out = request.form.get('wear_to_going_out')
        wear_to_exercise = request.form.get('wear_to_exercise')
        user_id = current_user.id
        shoes = Shoes(brand=brand, primary_color=primary_color, type=type, times_worn=times_worn, last_time_worn=last_time_worn, worn_to_most=worn_to_most, user_id=user_id, wear_to_work=wear_to_work, wear_to_school=wear_to_school, wear_to_errands=wear_to_errands, wear_to_going_out=wear_to_going_out, wear_to_exercise=wear_to_exercise, shoe_name=shoe_name)
        db.session.add(shoes)
        db.session.commit()

        flash('Shoes added successfully!', category='successs')
        return redirect(url_for('views.shoes'))
    return render_template("addNewShoes.html", user=current_user)

    shoes_list = Shoes.query.filter_by(user_id=current_user.id)
    return render_template("shoes.html", user=current_user, shoes_list=shoes_list)

