from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# This page is only neccessary if you are logging Users in

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='successs')
                login_user(user, remember=True)
                ## Need to change the below line to correspond with "Home Page"
                return redirect(url_for('views.base'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist. If problem persists, please email jreese@restore.com for assistance.', category='error')
    
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully. See you soon!', category='successs')
    return redirect(url_for('auth.login'))

## Thinking of not doing a sign up page because I would create the logins for the users.

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # Requirements can be changed to your liking

        user = User.query.filter_by(email=username).first()
        if user:
            flash('Email already exists', category='error')
        elif len(last_name) < 2:
            flash('Are you sure that is your name? It might be longer.', category='error')
        elif len(username) < 5:
            flash('Please enter a valid username.', category='error')
        elif len(password1) < 7:
            flash('Your password must be at least 8 characters', category='error')
        elif password1 != password2:
            flash('Your passwords do not match!', category='error')
        else:
            new_user =User(username=username, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.today'))
            

    return render_template("signup.html", user=current_user)