#%%
import csv
import os

#%%
def create_file(file_name):
    new_file = open(file_name, 'w+')
    new_file.close()


def delete_file(file_name):
    os.remove(file_name)

#%%
# Select only the data we need. That is data from 1970 - 2017
def partition_data(file):
    # Create a temp file to store partitioned data
    temp_file = 'temp.csv'
    create_file(temp_file)

    with open(file) as src_file:
        with open(temp_file, mode='w') as dest_file:
            reader = csv.reader(src_file, delimiter=',')
            writer = csv.writer(dest_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for index,row in enumerate(reader):
                if (index < 69): # Remove data before 1970. Enumerate starts from 0 so 1970 = 69 instead of 70
                    continue
                elif (index > 116): # Skip row after 2017
                    continue

                writer.writerow(row)

    delete_file(file)
    os.rename(temp_file, file)

#%%
# Fromat the data in the form: var_10_t-1, var_11_t-1, var_12_t-1, var_1, var_2, var_3, var_4, var_5, var_6, var_7, var_8, var_9, var_10, var_11, var_12
def format_data(file):
    temp_file = 'temp.csv'
    create_file(temp_file)

    with open(file) as src_file:
        with open(temp_file, mode='w') as dest_file:
            reader = csv.reader(src_file, delimiter=',')
            writer = csv.writer(dest_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            previous_row = None

            for index,row in enumerate(reader):
                if (previous_row == None):
                    previous_row = row
                    continue
                else:
                    writer.writerow([previous_row[9], previous_row[10], previous_row[11], row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]])
                    previous_row = row

    delete_file(file)
    os.rename(temp_file, file)

#%%
# Yield only has one column therefore need its own function
def format_yield(file):
    temp_file = 'temp.csv'
    create_file(temp_file)

    with open(file) as src_file:
        with open(temp_file, mode='w') as dest_file:
            reader = csv.reader(src_file, delimiter=',')
            writer = csv.writer(dest_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            previous_row = None

            for index,row in enumerate(reader):
                if (previous_row == None):
                    previous_row = row
                    continue
                else:
                    writer.writerow([previous_row[0], row[0]])
                    previous_row = row

    delete_file(file)
    os.rename(temp_file, file)

#%%
def aggregate(pre_file, tmp_file, yield_file, dest):
    temp_file = 'temp.csv'
    create_file(temp_file)

    # Initialize writer
    with open(temp_file, mode='w') as dest_file:
        writer = csv.writer(dest_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Write header
        writer.writerow([
            'tmp_10_t-1', 'tmp_11_t-1', 'tmp_12_t-1', 'tmp_1', 'tmp_2', 'tmp_3', 'tmp_4', 'tmp_5', 'tmp_6', 'tmp_7', 'tmp_8', 'tmp_9', 'tmp_10', 'tmp_11', 'tmp_12',
            'pre_10_t-1', 'pre_11_t-1', 'pre_12_t-1', 'pre_1', 'pre_2', 'pre_3', 'pre_4', 'pre_5', 'pre_6', 'pre_7', 'pre_8', 'pre_9', 'pre_10', 'pre_11', 'pre_12',
            'yield_t-1', 'yield'
        ])

        with open(pre_file) as pre_file:
            with open(tmp_file) as tmp_file:
                with open(yield_file) as yield_file:
                    pre_file = csv.reader(pre_file, delimiter=',')
                    tmp_file = csv.reader(tmp_file, delimiter=',')
                    yield_file = csv.reader(yield_file, delimiter=',')

                    for (pre, tmp, yld) in zip(pre_file, tmp_file, yield_file): 
                        row = pre + tmp + yld
                        writer.writerow(pre + tmp + yld)

    os.rename(temp_file, dest)


#%%
pre_data_east_java_name = '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/pre_data.csv'
tmp_data_east_java_name = '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/tmp_data.csv'
yield_name = '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/maize_yield_east_java.csv'
dest_file = '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/data.csv'

#%%
partition_data(pre_data_east_java_name)
partition_data(tmp_data_east_java_name)

#%%
format_data(pre_data_east_java_name)
format_data(tmp_data_east_java_name)
format_yield(yield_name)

#%%
aggregate(pre_data_east_java_name, tmp_data_east_java_name, yield_name, dest_file)