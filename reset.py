import csv
import os

#%%
def delete_file(file_name):
    os.remove(file_name)

#%%
todelete = [
    '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/pre_data.csv',
    '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/tmp_data.csv',
    '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/maize_yield_east_java.csv',
    '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/data.csv',
    'temp.csv',
    'pre_temp_data.csv',
    'tmp_temp_data.csv'
]

for file in todelete:
    if (os.path.exists(file)):
        delete_file(file)

print('All output files deleted!')