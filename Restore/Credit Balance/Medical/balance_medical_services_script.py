import pandas as pd

## Change what is in the quotes to the name of the csv file order for the program to work
print('Data pulled on 1/5/24')
## File path is different on laptop and pc
laptop_file_path = r'C:\Users\jason\Documents\GitHub\Restore_Data\Restore\Promotions\balance_medical_services_data.csv'
pc_file_path = r'C:\Users\jason\OneDrive\Documents\GitHub\Restore_Data\Restore\Credit Balance\Medical\balance_medical_services_data.csv'
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
    if utilization > wanted_utilization:
        bundles_list = [row.full_name, row.email, row.phone, row.credit_description, row.remaining_credits]
        bundles_contact_list.append(bundles_list)

## Create frame
print('Compiling results...')
bundles_frame = pd.DataFrame(bundles_contact_list, columns=['Full Name', 'Email', 'Phone', 'Credit Description', 'Remaining Credits'])

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
    if utilization > wanted_utilization:
        packs_list = [row.full_name, row.email, row.phone, row.credit_description, row.remaining_credits]
        packs_contact_list.append(packs_list)

## Create frame
print('Compiling results...')
packs_frame = pd.DataFrame(packs_contact_list, columns=['Full Name', 'Email', 'Phone', 'Credit Description', 'Remaining Credits'])


## Combining List
print('Combining Lists...')
medical_text_list = pd.concat([bundles_frame, packs_frame], axis=0)


print('Here is your list')
print(medical_text_list)

## Asking to create an excel sheet
while True:
    excel_file = input('Would you like to create an excel sheet with this? (y/n): ')
    if excel_file == 'y':
        excel_sheet_name = input('Name the excel file: ')
        print('Adding columns...')
        medical_text_list['First Contact Rep Initials'] = ''
        medical_text_list['Second Contact Rep Initials'] = ''
        medical_text_list['Third Contact Rep Initials'] = ''
        medical_text_list['Notes'] = ''
        print('Saving...')
        medical_text_list.to_excel(f'{excel_sheet_name}.xlsx')
        print(f'Success! Saved file as "{excel_sheet_name}"')
        break
    elif excel_file == 'n':
        print('Re-run the program to start over')
        break
    else:
        print('Please enter y for yes or n for no')