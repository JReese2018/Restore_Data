from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, session
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
#from website import date_time
from datetime import datetime
from .models import User, User_Feedback, Counter, Month_Comparison
from sqlalchemy.sql.expression import func, select, desc
from . import db
import pandas as pd
import io
import tempfile

# This file is your backend to all your pages on your app. I left an example on how
# to post things to the database. This also shows how to use the flask functions like
# redirect, url_for, flash, etc.

## The below classes allows file uploads. Note, we are not saving any of these files into a database
class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

class ComparisonFileForm(FlaskForm):
    file1 = FileField("File 1")
    file2 = FileField("File 2")
    submit = SubmitField('Upload File')

## This is how we are getting the date and time
now = datetime.now() 
date_time = now.strftime("%m/%d/%Y")

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    name = current_user.username.capitalize()
    return render_template("home.html", user=current_user, name=name)

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

            temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
            filename = temp_file.name
            skin_list_df.to_excel(filename, index=False)
            temp_file.close()
            download_filename = (f'{service_type} {converted_utilization} {date_time}.xlsx')
            session['file_path'] = filename
            session['download_filename'] = download_filename
            return redirect(url_for('views.credit_utilization_list', table=core_list_df_reset.to_html(classes='table table-striped'), utilization=converted_utilization))
            
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

            temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
            filename = temp_file.name
            skin_list_df.to_excel(filename, index=False)
            temp_file.close()
            download_filename = (f'{service_type} {converted_utilization} {date_time}.xlsx')
            session['file_path'] = filename
            session['download_filename'] = download_filename
            return redirect(url_for('views.credit_utilization_list', table=medical_text_list_reset.to_html(classes='table table-striped'), utilization=converted_utilization))
            
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

            temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
            filename = temp_file.name
            skin_list_df.to_excel(filename, index=False)
            temp_file.close()
            download_filename = (f'{service_type} {converted_utilization} {date_time}.xlsx')
            session['file_path'] = filename
            session['download_filename'] = download_filename
            return redirect(url_for('views.credit_utilization_list', table=skin_list_df_reset.to_html(classes='table table-striped'), utilization=converted_utilization))

    return render_template("credit_utilization.html", user=current_user, form=form)

@views.route('/credit-utilization/list', methods=['GET', 'POST'])
@login_required
def credit_utilization_list():
    table = request.args.get('table', '')
    utilization = request.args.get('utilization', '')
    if request.method == 'POST':
        file_path = session.get('file_path')
        download_filename = session.get('download_filename')
        return send_file(file_path, as_attachment=True, download_name=download_filename)
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
    form = ComparisonFileForm()
    previous = form.file1.data
    current = form.file2.data

    if request.method == 'POST':
        previous_df = pd.read_csv(previous)
        current_df = pd.read_csv(current)
        print('Cleaning data...')
        previous_df = previous_df.drop(columns=['Studio Code', 'Invoice ID', 'Client ID', 'Therapy Category', 'Business Category', 'Sales Rep', 'Autopay Status', 'Tax Amount', 'Amount', 'Discount', 'Gross adjusted Revenue', 'Quantity', 'Credit Used'])
        current_df = current_df.drop(columns=['Invoice ID', 'Client ID', 'Therapy Category', 'Business Category', 'Sales Rep', 'Autopay Status', 'Tax Amount', 'Amount', 'Discount', 'Gross adjusted Revenue', 'Quantity', 'Credit Used'])
        print('Creating new column for first and last names...')
        current_df['Name'] = current_df['First Name'] + ' ' + current_df['Last Name']
        current_df = current_df.drop(columns=['First Name', 'Last Name'])
        current_df = current_df[['Name', 'Email', 'Phone #', 'Item', 'Purchase Date']]
        previous_df['Name'] = previous_df['First Name'] + ' ' + previous_df['Last Name']
        previous_df = previous_df.drop(columns=['First Name', 'Last Name'])
        previous_df = previous_df[['Name', 'Email', 'Phone #', 'Item', 'Purchase Date']]
        print('Calculating Number of Membership in first dataset...')
        previous_discover_count = len(previous_df.loc[previous_df['Item'] == 'Discover Membership'])
        previous_levelup_count = len(previous_df.loc[previous_df['Item'] == 'Level Up Membership'])
        previous_elevate_count = len(previous_df.loc[previous_df['Item'] == 'Elevate Membership'])
        previous_core_count = len(previous_df.loc[previous_df['Item'] == 'Core Membership'])
        previous_restore_count = len(previous_df.loc[previous_df['Item'] == 'Restore Membership'])
        previous_restorecouples_count = len(previous_df.loc[previous_df['Item'] == 'Restore Membership - Couples'])
        previous_wellness_count = len(previous_df.loc[previous_df['Item'] == 'Wellness Membership'])
        previous_wellnesscouples_count = len(previous_df.loc[previous_df['Item'] == 'Wellness Membership - Couples'])
        previous_daily_count = len(previous_df.loc[previous_df['Item'] == 'Daily Membership'])
        previous_membership_count = len(previous_df)
        print('Identifying month...')
        previous_month = previous_df['Purchase Date'].head(1).str.split('/').str[0].values[0]
        if previous_month == '1':
            previous_month = 'January'
        elif previous_month == '2':
            previous_month = 'February'
        elif previous_month == '3':
            previous_month = 'March'
        elif previous_month == '4':
            previous_month = 'April'
        elif previous_month == '5':
            previous_month = 'May'
        elif previous_month == '6':
            previous_month = 'June'
        elif previous_month == '7':
            previous_month = 'July'
        elif previous_month == '8':
            previous_month = 'August'
        elif previous_month == '9':
            previous_month = 'September'
        elif previous_month == '10':
            previous_month = 'October'
        elif previous_month == '11':
            previous_month = 'November'
        elif previous_month == '12':
            previous_month = 'December'
        else:
            current_month = 'Month'
        print('Calculating Number of Membership in second dataset...')
        current_discover_count = len(current_df.loc[current_df['Item'] == 'Discover Membership'])
        current_levelup_count = len(current_df.loc[current_df['Item'] == 'Level Up Membership'])
        current_elevate_count = len(current_df.loc[current_df['Item'] == 'Elevate Membership'])
        current_core_count = len(current_df.loc[current_df['Item'] == 'Core Membership'])
        current_restore_count = len(current_df.loc[current_df['Item'] == 'Restore Membership'])
        current_restorecouples_count = len(current_df.loc[current_df['Item'] == 'Restore Membership - Couples'])
        current_wellness_count = len(current_df.loc[current_df['Item'] == 'Wellness Membership'])
        current_wellnesscouples_count = len(current_df.loc[current_df['Item'] == 'Wellness Membership - Couples'])
        current_daily_count = len(current_df.loc[current_df['Item'] == 'Daily Membership'])
        current_membership_count = len(current_df)
        print('Identifying month...')
        current_month = current_df['Purchase Date'].head(1).str.split('/').str[0].values[0]
        if current_month == '1':
            current_month = 'January'
        elif current_month == '2':
            current_month = 'February'
        elif current_month == '3':
            current_month = 'March'
        elif current_month == '4':
            current_month = 'April'
        elif current_month == '5':
            current_month = 'May'
        elif current_month == '6':
            current_month = 'June'
        elif current_month == '7':
            current_month = 'July'
        elif current_month == '8':
            current_month = 'August'
        elif current_month == '9':
            current_month = 'September'
        elif current_month == '10':
            current_month = 'October'
        elif current_month == '11':
            current_month = 'November'
        elif current_month == '12':
            current_month = 'December'
        else:
            current_month = 'Month'
        print('Identifying lost members, this could take a some time...')
        merged_df = pd.merge(previous_df, current_df, on='Name', suffixes=('_prev', '_current'), how='outer', indicator=True)
        lost_members = merged_df[merged_df['_merge'] == 'left_only'][['Name', 'Email_prev', 'Phone #_prev', 'Item_prev']].values.tolist()
        print('Identifying members who are in both datasets, this could take a some time...')
        overlap_members = []
        for index, row1 in previous_df.iterrows():
            for index, row2 in current_df.iterrows():
                name1 = row1['Name']
                name2 = row2['Name']
                if name1 != name2:
                    continue
                else:
                    my_list = [row1['Name'], row1['Email'], row1['Phone #'], row1['Item']]
                    overlap_members.append(my_list)
                    continue
            continue
        print('Configuring data...')
        lost_members_df = pd.DataFrame(lost_members, columns=['Name', 'Email', 'Phone #', 'Membership'])
        overlap_members_df = pd.DataFrame(overlap_members, columns=['Name', 'Email', 'Phone #', 'Membership'])

        
        print('Dropping Duplicates...')
        ## Dropping dulplicates
        lost_members_df = lost_members_df.drop_duplicates(subset=['Name'])
        overlap_members_df = overlap_members_df.drop_duplicates(subset=['Name'])
        print('Compiling results and wrapping up...')

        print('Here are your results')
        print(f'Total number of all memberships in {previous_month}: {previous_membership_count}')
        print(f'Number of Discover Memberships: {previous_discover_count}')
        print(f'Number of Level Up Memberships: {previous_levelup_count}')
        print(f'Number of Elevate Memberships: {previous_elevate_count}')
        print(f'Number of Core Memberships: {previous_core_count}')
        print(f'Number of Restore Memberships: {previous_restore_count}')
        print(f'Number of Restore Couples Memberships: {previous_restorecouples_count}')
        print(f'Number of Wellness Memberships: {previous_wellness_count}')
        print(f'Number of Wellness Couples Memberships: {previous_wellnesscouples_count}')
        print(f'Number of Daily Memberships: {previous_daily_count}')
        print('')
        print('')
        print('')
        print(f'Total number of all memberships in {current_month}: {current_membership_count}')
        print(f'Number of Discover Memberships: {current_discover_count}')
        print(f'Number of Level Up Memberships: {current_levelup_count}')
        print(f'Number of Elevate Memberships: {current_elevate_count}')
        print(f'Number of Core Memberships: {current_core_count}')
        print(f'Number of Restore Memberships: {current_restore_count}')
        print(f'Number of Restore Couples Memberships: {current_restorecouples_count}')
        print(f'Number of Wellness Memberships: {current_wellness_count}')
        print(f'Number of Wellness Couples Memberships: {current_wellnesscouples_count}')
        print(f'Number of Daily Memberships: {current_daily_count}')
        print('')
        print('')
        print('')
        print('Here are all of your lost members between the two datasets')
        print(lost_members_df)

        user_id = current_user.id
        compare = Month_Comparison(previous_membership_count=previous_membership_count, previous_discover_count=previous_discover_count, previous_levelup_count=previous_levelup_count, previous_elevate_count=previous_elevate_count, previous_core_count=previous_core_count, previous_restore_count=previous_restore_count, previous_restorecouples_count=previous_restorecouples_count, previous_wellness_count=previous_wellness_count, previous_wellnesscouples_count=previous_wellnesscouples_count, previous_daily_count=previous_daily_count, current_membership_count=current_membership_count, current_discover_count=current_discover_count, current_levelup_count=current_levelup_count, current_elevate_count=current_elevate_count, current_core_count=current_core_count, current_restore_count=current_restore_count, current_restorecouples_count=current_restorecouples_count, current_wellness_count=current_wellness_count, current_wellnesscouples_count=current_wellnesscouples_count, current_daily_count=current_daily_count, previous_month=previous_month, current_month=current_month, user_id=user_id)
        db.session.add(compare)
        db.session.commit()

        print('Adding columns...')
        lost_members_df['First Contact Rep Initials'] = ''
        lost_members_df['Second Contact Rep Initials'] = ''
        lost_members_df['Third Contact Rep Initials'] = ''
        lost_members_df['Notes'] = ''

        temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
        filename = temp_file.name
        lost_members_df.to_excel(filename, index=False)
        temp_file.close()
        download_filename = (f'Lost Members {previous_month} to {current_month} {date_time}.xlsx')
        session['file_path'] = filename
        session['download_filename'] = download_filename
        return redirect(url_for('views.month_comparison_list'))

    return render_template("month_comparison.html", user=current_user, form=form)


@views.route('/month-comparison/list', methods=['GET', 'POST'])
@login_required
def month_comparison_list():
    displays = Month_Comparison.query.filter_by(user_id=current_user.id).order_by(desc(Month_Comparison.month_comparison_id)).limit(1)
    if request.method == 'POST':
        file_path = session.get('file_path')
        download_filename = session.get('download_filename')
        return send_file(file_path, as_attachment=True, download_name=download_filename)
    
    return render_template('month_comparison_list.html', user=current_user, displays=displays)

@views.route('/spend-amount', methods=['GET', 'POST'])
@login_required
def spend_amount():
    form = UploadFileForm()

    if request.method == 'POST':
        spend_amount = request.form.get('spend_amount')
        uploaded_file = form.file.data
        ## Read CSV
        df = pd.read_csv(uploaded_file)
        ## Dropping unnecessary columns
        df = df.drop(columns=['Invoice ID', 'Client ID', 'Therapy Category', 'Business Category', 'Sales Rep', 'Autopay Status', 'Tax Amount', 'Amount', 'Discount', 'Credit Used', 'Quantity'])
        ## Combining names, reoragninzing and renaming
        df['Name'] = df['First Name'] + ' ' + df['Last Name']
        df = df.drop(columns=['First Name', 'Last Name'])
        df = df.rename(columns={'Phone #': 'Phone Number'})
        df = df.rename(columns={'Gross adjusted Revenue': 'Amount Paid'})
        df = df[['Name', 'Phone Number', 'Email', 'Item', 'Amount Paid', 'Purchase Date']]
        ## Cleaning data
        df = df.dropna()
        ## Getting rid of membership transactions
        no_membership = []
        counter = 1
        for index, row in df.iterrows():
            if 'Membership' in row['Item']:
                counter + 1
                continue
            else:
                my_list = [row['Name'], row['Phone Number'], row['Email'], row['Item'], row['Amount Paid'], row['Purchase Date']]
                no_membership.append(my_list)
                continue
        ## Turning list into dataframe
        no_membership_df = pd.DataFrame(no_membership, columns=['Name', 'Phone Number', 'Email', 'Item', 'Amount Paid', 'Purchase Date'])
        ## Asking User what amount they want to see
        above_amount = []
        amount = spend_amount
        int_amount = int(amount)
        for index, row in no_membership_df.iterrows():
            if row['Amount Paid'] < int_amount:
                continue
            else:
                my_list = [row['Name'], row['Phone Number'], row['Email'], row['Item'], row['Amount Paid'], row['Purchase Date']]
                above_amount.append(my_list)
        ## Creating final dataframe
        above_amount_df = pd.DataFrame(above_amount, columns=['Name', 'Phone Number', 'Email', 'Item', 'Amount Paid', 'Purchase Date'])
        ## Ordering from the largest to smallest
        above_amount_df = above_amount_df.sort_values('Amount Paid', ascending=False)
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
        filename = temp_file.name
        above_amount_df.to_excel(filename, index=False)
        temp_file.close()
        download_filename = (f'Spend amount above {amount} {date_time}.xlsx')
        ## Testing session.clear() method
        session.clear()
        session['file_path'] = filename
        session['download_filename'] = download_filename
        session['above_amount_table'] = above_amount_df.to_html(classes='table table-striped')

        return redirect(url_for('views.spend_amount_list', amount=amount))
    
    return render_template('spend_amount.html', user=current_user, form=form)

@views.route('/spend-amount/list', methods=['GET', 'POST'])
@login_required
def spend_amount_list():
    table_html = session.pop('above_amount_table', None)
    amount = request.args.get('amount', '')
    if request.method == 'POST':
        file_path = session.get('file_path')
        download_filename = session.get('download_filename')
        return send_file(file_path, as_attachment=True, download_name=download_filename)
    
    return render_template('spend_amount_list.html', user=current_user, table=table_html, amount=amount)

@views.route('/feedback', methods=['GET', 'POST'])
def feedback():
    date = date_time
    if request.method == 'POST':
        email = request.form.get('email')
        feedback = request.form.get('feedback')
        added_feedback = User_Feedback(email=email, feedback=feedback)
        db.session.add(added_feedback)
        db.session.commit()
        flash("Thank you for the feedback! If I have any follow ups for you, I'll send you a message to the email you provided.", category='success')
        return redirect(url_for('views.home'))
    return render_template("feedback.html", user=current_user, date=date)

