import pandas as pd

## Change what is in the quotes to the name of the csv file order for the program to work
print('Loading data...')
df  = pd.read_csv('balance_core_services.csv')
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
df.dropna()
print('Cleaning data...')
df['initial_credits'] = df['initial_credits'].astype(str).astype(int)
## Asking user what percentage do they want used
wanted_utilization = int(input('What percentage of utilization would you like: '))
## Calculations
print('Performing calculations...')
contact_list = []
for index, row in df.iterrows():
    remaining = row['remaining_credits']
    initial = row['initial_credits']
    calculated_percentage = (remaining / initial) * 100
    utilization = 100 - calculated_percentage
    if utilization > 60:
        my_list = [row.full_name, row.phone, row.credit_description, row.remaining_credits]
        df.append(my_list)

## Create frame and export
print('Compiling results...')
core_list_df = pd.DataFrame(contact_list, columns=['Full Name', 'Phone Number', 'Credit Description', 'Remaining Credits'])
print('')
excel_sheet_name = input('Name the excel  file: ')
df.to_excel(f'{excel_sheet_name}.xlsx')
