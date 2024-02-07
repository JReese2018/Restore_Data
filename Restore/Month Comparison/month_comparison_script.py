## Load Pandas
import pandas as pd
import time


print('Data pulled on 2/6/24')
previous_laptop_file_path = r'C:\Users\jason\Documents\GitHub\Restore_Data\Restore\Credit Balance\Medical\balance_medical_services_data.csv'
current_laptop_file_path = r'C:\Users\jason\Documents\GitHub\Restore_Data\Restore\Credit Balance\Medical\balance_medical_services_data.csv'

previous_pc_file_path = r'C:\Users\jason\OneDrive\Documents\GitHub\Restore_Data\Restore\Month Comparison\march2023.csv'
current_pc_file_path = r'C:\Users\jason\OneDrive\Documents\GitHub\Restore_Data\Restore\Month Comparison\january2024.csv'

file_path = input('Are you on the laptop or pc: ')
print('Importing data...')
if file_path == 'pc':
    previous_df = pd.read_csv(previous_pc_file_path)
    current_df = pd.read_csv(current_pc_file_path)
elif file_path == 'laptop':
    previous_df = pd.read_csv(previous_laptop_file_path)
    current_df = pd.read_csv(current_laptop_file_path)
print('Cleaning data...')
previous_df = previous_df.drop(columns=['Studio Code', 'Invoice ID', 'Client ID', 'Therapy Category', 'Business Category', 'Sales Rep', 'Autopay Status', 'Tax Amount', 'Amount', 'Discount', 'Gross adjusted Revenue', 'Quantity', 'Credit Used'])
current_df = current_df.drop(columns=['Studio Code', 'Invoice ID', 'Client ID', 'Therapy Category', 'Business Category', 'Sales Rep', 'Autopay Status', 'Tax Amount', 'Amount', 'Discount', 'Gross adjusted Revenue', 'Quantity', 'Credit Used'])
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
print('Compiling results and wrapping up...')
#time.sleep(3)

print(f'Number of Discover Memberships: {previous_discover_count}')
print(f'Number of Level Up Memberships: {previous_levelup_count}')
print(f'Number of Elevate Memberships: {previous_elevate_count}')
print(f'Number of Core Memberships: {previous_core_count}')
print(f'Number of Restore Memberships: {previous_restore_count}')
print(f'Number of Restore Couples Memberships: {previous_restorecouples_count}')
print(f'Number of Wellness Memberships: {previous_wellness_count}')
print(f'Number of Wellness Couples Memberships: {previous_wellnesscouples_count}')
print(f'Number of Daily Memberships: {previous_daily_count}')
print(f'Total number of all memberships in {previous_month}: {previous_membership_count}')
print('')
print('')
print('')
print(f'Number of Discover Memberships: {current_discover_count}')
print(f'Number of Level Up Memberships: {current_levelup_count}')
print(f'Number of Elevate Memberships: {current_elevate_count}')
print(f'Number of Core Memberships: {current_core_count}')
print(f'Number of Restore Memberships: {current_restore_count}')
print(f'Number of Restore Couples Memberships: {current_restorecouples_count}')
print(f'Number of Wellness Memberships: {current_wellness_count}')
print(f'Number of Wellness Couples Memberships: {current_wellnesscouples_count}')
print(f'Number of Daily Memberships: {current_daily_count}')
print(f'Total number of all memberships in {current_month}: {current_membership_count}')
print('')
print('')
print('')
print('Here are all of your lost members between the two datasets')
print(lost_members_df)
print('')
print('')
print('')
print('Here are all of you members who are in both datasets')
print(overlap_members_df)