from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
#from website import date_time
from datetime import datetime
from .models import User, User_Feedback, Counter, Credit_list
from sqlalchemy.sql.expression import func, select, desc
from . import db
import pandas as pd
import io

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
            core_list_df_reset = core_list_df.set_index(['Full Name', 'Email', 'Phone Number', 'Credit Description', 'Remaining Credits'])
            print('Here is your list')
            print(core_list_df_reset)
            print('Adding columns...')
            core_list_df['First Contact Rep Initials'] = ''
            core_list_df['Second Contact Rep Initials'] = ''
            core_list_df['Third Contact Rep Initials'] = ''
            core_list_df['Notes'] = ''
            print('Saving...')
            filename = (f'Skin_Health_{converted_utilization}_{date_time}.xlsx')
            excel_data = io.BytesIO()
            core_list_df.to_excel(excel_data, index=False)
            excel_data.seek(0)
            return send_file(excel_data, as_attachment=True, download_name=filename)
        
            ## We need to figure out how to get the program to download the csv and redirect to table page
            #return redirect(url_for('views.credit_utilization_list', table=core_list_df_reset.to_html(classes='table table-striped'), utilization=converted_utilization))
            
        
        elif service_type == 'Medical':
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

            ## Seperating bundles from packs
            print('Seperating bundles from packs...')
            df_bundles = df.loc[df['credit_description'].str.contains('bundle', case=False)]

            ## Bundles Calculations
            print('Performing bundles calculations...')
            bundles_contact_list = []
            for index, row in df_bundles.iterrows():
                remaining = int(row['remaining_credits'])
                total = int(row['initial_credits'])
                calculated_percentage = (remaining / total) * 100
                utilization = 100 - calculated_percentage
                if utilization > converted_utilization:
                    bundles_list = [row.full_name, row.email, row.phone, row.credit_description, row.remaining_credits]
                    bundles_contact_list.append(bundles_list)

            ## Create frame
            print('Compiling results...')
            bundles_frame = pd.DataFrame(bundles_contact_list, columns=['Full Name', 'Email', 'Phone Number', 'Credit Description', 'Remaining Credits'])

            ## Working on packs
            print('Finding packs...')
            df_packs = df.loc[df['credit_description'].str.contains('pack', case=False)]

            df_packs = df_packs.drop(columns=["initial_credits"])

            print('Packs found. Reconfiguring columns...')
            df_packs['initial_credits'] = df_packs['credit_description'].str.extract(r'(\d+)\s*Pack')
            df_packs['initial_credits'] = df_packs['initial_credits'].astype(str).astype(int)

            ## Packs Calculations
            print('Performing more calculations...')
            packs_contact_list = []
            for index, row in df_packs.iterrows():
                remaining = row['remaining_credits']
                initial = row['initial_credits']
                calculated_percentage = (remaining / initial) * 100
                utilization = 100 - calculated_percentage
                if utilization > converted_utilization:
                    packs_list = [row.full_name, row.email, row.phone, row.credit_description, row.remaining_credits]
                    packs_contact_list.append(packs_list)

            ## Create frame
            print('Compiling results...')
            packs_frame = pd.DataFrame(packs_contact_list, columns=['Full Name', 'Email', 'Phone Number', 'Credit Description', 'Remaining Credits'])


            ## Combining List
            print('Combining Lists...')
            medical_text_list = pd.concat([bundles_frame, packs_frame], axis=0)

            medical_text_list_reset = medical_text_list.set_index(['Full Name', 'Email', 'Phone Number', 'Credit Description', 'Remaining Credits'])
            print('Here is your list')
            print(medical_text_list_reset)
            print('Adding columns...')
            medical_text_list['First Contact Rep Initials'] = ''
            medical_text_list['Second Contact Rep Initials'] = ''
            medical_text_list['Third Contact Rep Initials'] = ''
            medical_text_list['Notes'] = ''
            print('Saving...')
            filename = (f'Skin_Health_{converted_utilization}_{date_time}.xlsx')
            excel_data = io.BytesIO()
            medical_text_list.to_excel(excel_data, index=False)
            excel_data.seek(0)
            return send_file(excel_data, as_attachment=True, download_name=filename)
        
            ## We need to figure out how to get the program to download the csv and redirect to table page
            #return redirect(url_for('views.credit_utilization_list', table=medical_text_list_reset.to_html(classes='table table-striped'), utilization=converted_utilization))
            
        
        elif service_type == 'Skin Health':
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
            skin_list_df = pd.DataFrame(contact_list, columns=['Full Name', 'Email', 'Phone Number', 'Credit Description', 'Remaining Credits'])
            print(skin_list_df)
            skin_list_df_reset = skin_list_df.set_index(['Full Name', 'Email', 'Phone Number', 'Credit Description', 'Remaining Credits'])
            print('Here is your list')
            print(skin_list_df_reset)
            print('Adding columns...')
            skin_list_df['First Contact Rep Initials'] = ''
            skin_list_df['Second Contact Rep Initials'] = ''
            skin_list_df['Third Contact Rep Initials'] = ''
            skin_list_df['Notes'] = ''
            print('Saving...')
            filename = (f'Skin_Health_{converted_utilization}_{date_time}.xlsx')
            excel_data = io.BytesIO()
            skin_list_df.to_excel(excel_data, index=False)
            excel_data.seek(0)
            return send_file(excel_data, as_attachment=True, download_name=filename)
        
            ## We need to figure out how to get the program to download the csv and redirect to table page
            #return redirect(url_for('views.credit_utilization_list', table=skin_list_df_reset.to_html(classes='table table-striped'), utilization=converted_utilization))

    return render_template("credit_utilization.html", user=current_user, form=form)

@views.route('/credit-utilization/list', methods=['GET'])
@login_required
def credit_utilization_list():
    table = request.args.get('table', '')
    utilization = request.args.get('utilization', '')
    return render_template('credit_utilization_list.html', user=current_user, table=table, utilization=utilization)

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

