## Import Pandas
import pandas as pd

## Read CSV
df = pd.read_csv('last_3_months.csv')

## Dropping unnecessary columns
df = df.drop(columns=['Studio Code', 'Invoice ID', 'Client ID', 'Therapy Category', 'Business Category', 'Sales Rep', 'Autopay Status', 'Tax Amount', 'Amount', 'Discount', 'Credit Used', 'Quantity'])

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
#amount = input('All purchases above: $')
#amount = int(amount)
## For now, we will input 350
amount = 350
for index, row in no_membership_df.iterrows():
    if row['Amount Paid'] < amount:
        continue
    else:
        my_list = [row['Name'], row['Phone Number'], row['Email'], row['Item'], row['Amount Paid'], row['Purchase Date']]
        above_amount.append(my_list)

## Creating final dataframe
above_amount_df = pd.DataFrame(above_amount, columns=['Name', 'Phone Number', 'Email', 'Item', 'Amount Paid', 'Purchase Date'])