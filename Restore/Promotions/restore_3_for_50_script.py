import pandas as pd

## Read te data
print('Data pulled on 1/2/24')
print('Loading the data...')
file_path = r'C:\Users\jason\Documents\GitHub\Restore_Data\Restore\Promotions\restore_3_for_50_data.csv'
df  = pd.read_csv(file_path)

## Getting rid of unneeded columns
print('Dropping columns...')
df = df.drop(columns=['Studio Code', 'Purchase Date', 'Invoice ID', 'Client ID', 'Therapy Category', 'Business Category', 'Sales Rep', 'Autopay Status', 'Tax Amount', 'Discount', 'Quantity', 'Credit Used'])

## Last column is named incorrectly when pulling
print('Renaming columns: ')
df = df.rename(columns={"Unnamed: 17": "Total"})
df = df.rename(columns={"First Name": "first_name"})
df = df.rename(columns={"Phone #": "number"})
df = df.rename(columns={"Last Name": "last_name"})
df = df.rename(columns={"Email": "email"})

## Filtering
print('Filtering the data...')
df = df.loc[(df['Item'] == 'Core Service | 3 Pack') & (df['Total'] == '$50.00')]

## Index resetting
print('Resetting indexes...')
df = df.reset_index()
df = df.drop(columns=['index'])



## Calculations
print('Performing calculations...')
text_list = []
for index, rows in df.iterrows():
    my_list = [rows.first_name, rows.last_name, rows.number, rows.email]
    text_list.append(my_list)


## Create frame and export
print('Compiling results...')
final_text_list = pd.DataFrame(text_list, columns=['First Name', 'Last Name', 'Phone Number', 'Email'])

print('Here is your list of people who purchase the 3 for $50 deal')
print(final_text_list)
while True:
    excel_file = input('Would you like to create an excel sheet with this? (y/n): ')
    if excel_file == 'y':
        excel_sheet_name = input('Name the excel file: ')
        print('Saving...')
        final_text_list.to_excel(f'{excel_sheet_name}.xlsx')
        print(f'Success! Saved file as "{excel_sheet_name}"')
        break
    elif excel_file == 'n':
        print('Re-run the program to start over')
        break
    else:
        print('Please enter y for yes or n for no')