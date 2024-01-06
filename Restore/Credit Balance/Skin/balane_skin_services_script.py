import pandas as pd

## Change what is in the quotes to the name of the csv file order for the program to work
print('Data pulled on 1/5/24')
## File path is different on laptop and pc
laptop_file_path = r'C:\Users\jason\Documents\GitHub\Restore_Data\Restore\Credit Balance\Skin\balance_skin_services_data.csv'
pc_file_path = r'C:\Users\jason\OneDrive\Documents\GitHub\Restore_Data\Restore\Credit Balance\Skin\balance_skin_services_data.csv'
file_path = input('Are you on the laptop or pc: ')
if file_path == 'laptop':
    df  = pd.read_csv(laptop_file_path)
elif file_path == 'pc':
    df  = pd.read_csv(pc_file_path)
else:
    print('Unrecognized input. Rerun the program')
    quit()
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
wanted_utilization = int(input('What percentage of utilization would you like: %'))
## Calculations
print('Performing calculations...')
contact_list = []
for index, row in df.iterrows():
    remaining = row['remaining_credits']
    initial = row['initial_credits']
    calculated_percentage = (remaining / initial) * 100
    utilization = 100 - calculated_percentage
    if utilization > wanted_utilization:
        my_list = [row.full_name, row.email, row.phone, row.credit_description, row.remaining_credits]
        contact_list.append(my_list)

## Create frame and export
print('Compiling results...')
skin_list_df = pd.DataFrame(contact_list, columns=['Full Name', 'Email', 'Phone Number', 'Credit Description', 'Remaining Credits'])

print('Here is your list')
print(skin_list_df)



## Asking to create an excel sheet
while True:
    excel_file = input('Would you like to create an excel sheet with this? (y/n): ')
    if excel_file == 'y':
        excel_sheet_name = input('Name the excel file: ')
        print('Adding columns...')
        skin_list_df['First Contact Rep Initials'] = ''
        skin_list_df['Second Contact Rep Initials'] = ''
        skin_list_df['Third Contact Rep Initials'] = ''
        skin_list_df['Notes'] = ''
        print('Saving...')
        skin_list_df.to_excel(f'{excel_sheet_name}.xlsx')
        print(f'Success! Saved file as "{excel_sheet_name}"')
        break
    elif excel_file == 'n':
        print('Re-run the program to start over')
        break
    else:
        print('Please enter y for yes or n for no')