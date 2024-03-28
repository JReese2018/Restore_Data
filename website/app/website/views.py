from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
#from website import date_time
from datetime import datetime
from .models import User, User_Feedback
from . import db
import pandas as pd

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

@views.route('/credit-utilization', methods=['GET', 'POST'])
@login_required
def credit_utilization():
    form = UploadFileForm()

    if request.method == 'POST':
        service_type = request.form.get('service_type')
        uploaded_file = form.file.data
        if service_type == 'Core':
            df = pd.read_csv(uploaded_file.stream)
            print('Loading the data...')

            ## Drop uneeded columns in current patch
            print('Dropping columns...')
            df = df.drop(columns=['Studio Name', 'Day of Issue Date', 'Day of Expire Date', 'Client ID', 'Business Category', 'Credit Source', 'Initial Credit Count', 'Used Credit Count', 'Index', 'Max date'])

            ## Rename columns
            print('Renaming columns...')
            df = df.rename(columns={'Full Name': 'full_name'})
            df = df.rename(columns={'Email': 'email'})
            df = df.rename(columns={'Phone #': 'phone'})
            df = df.rename(columns={'Credit Description': 'credit_description'})
            df = df.rename(columns={'Remaining Credits': 'remaining_credits'})

            ## Creating 'Initial Credits' Column
            print('Creating new column...')
            df['initial_credits'] = df['credit_description'].astype(str).str.extract(r'(\d+)', expand=False)

            ## Clean the data
            print('Configuring new column...')
            df = df.dropna()
            print('Cleaning data...')
            df['initial_credits'] = df['initial_credits'].astype(str).astype(int)

            ## Asking user what percentage do they want used
            wanted_utilization = request.form.get('utilization')
            converted_utilization = int(wanted_utilization)

            ## Calculations
            print('Performing calculations...')
            contact_list = []
            for index, row in df.iterrows():
                remaining = row['remaining_credits']
                initial = row['initial_credits']
                calculated_percentage = (remaining / initial) * 100
                utilization = 100 - calculated_percentage
                if utilization > converted_utilization:
                    my_list = [row.full_name, row.email, row.phone, row.credit_description, row.remaining_credits]
                    contact_list.append(my_list)

            ## Create frame and export
            print('Compiling results...')
            core_list_df = pd.DataFrame(contact_list, columns=['Full Name', 'Email', 'Phone Number', 'Credit Description', 'Remaining Credits'])

            print('Here is your list')
            print(core_list_df)



    return render_template("credit_utilization.html", user=current_user, form=form)

## This might be scrapped because tableu has a tab that can be used to get the same data that I was going to do I think
@views.route('/promotions', methods=['GET', 'POST'])
@login_required
def promotions():
    form = UploadFileForm()
    return render_template("promotions.html", user=current_user, form=form)

@views.route('/month-comparison', methods=['GET', 'POST'])
@login_required
def month_comparison():
    form = UploadFileForm()
    return render_template("month_comparison.html", user=current_user, form=form)

@views.route('/feedback', methods=['GET', 'POST'])
def feedback():
    date = date_time
    return render_template("feedback.html", user=current_user, date=date)

