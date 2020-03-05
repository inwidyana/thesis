#%%
import csv
import os
from shutil import copyfile

#%%
def create_file(file_name):
    new_file = open(file_name, 'w+')
    new_file.close()


def delete_file(file_name):
    os.remove(file_name)

#%%
def get_east_java_data(source_file, dest_file):
    with open(source_file) as source:
        source_data = csv.reader(source, delimiter=';')
        line_count = 0

        with open(dest_file, mode='w') as destination:
            dest_writer = csv.writer(
                destination, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in source_data:
                first_line = (line_count == 6)
                yogya_data = (((line_count - 6) % 11) == 0)

                # temp = row

                if first_line or yogya_data:
                    dest_writer.writerow([float(row[5])])
                    print('.', end='')

                if line_count % 10 == 0:
                    print('\n')

                line_count += 1

            print('\nTotal line created: ', (line_count / 11))

#%%
def group_into_yearly_data(source_file, dest_file):
    year_data = []

    with open(source_file) as csv_file:
        with open(dest_file, mode='w') as destination:
            dest_writer = csv.writer(
                destination, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            source_data = csv.reader(csv_file, delimiter=',')
            month_counter = 0
            line_counter = 0

            for row in source_data:
                year_data.append((float(row[0])))
                month_counter += 1

                if month_counter == 12:
                    dest_writer.writerow(year_data)
                    year_data.clear()
                    month_counter = 0
                    line_counter += 1
                    print('.', end='')

                if line_counter % 10 == 0:
                    print('\n')

            print('\nTotal line created: ', (line_counter))


#%%
pre_raw_data = '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/unprocessed data/pre_cru-ts-4.03-gridded_110.25e9.75s114.75e5.25s_19010116-20181216.csv'
tmp_raw_data = '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/unprocessed data/tmp_cru-ts-4.03-gridded_110.25e9.75s114.75e5.25s_19010116-20181216.csv'

pre_temp_data_name = 'pre_temp_data.csv'
tmp_temp_data_name = 'tmp_temp_data.csv'

pre_data_east_java_name = '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/pre_data.csv'
tmp_data_east_java_name = '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/tmp_data.csv'

yield_file_name = '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/unprocessed data/maize_yield_east_java.csv'
yield_file_dest = '/Users/indrawidyana/OneDrive - UGM 365/Thesis/Code/processed data/maize_yield_east_java.csv'

#%%

# Create temp file as a temporary storage
create_file(pre_temp_data_name)
create_file(tmp_temp_data_name)


#%%

# Filter out yogyakarta data from the dataset
get_east_java_data(pre_raw_data, pre_temp_data_name)
get_east_java_data(tmp_raw_data, tmp_temp_data_name)

#%%

# Create destination file for the processed dataset
create_file(pre_data_east_java_name)
create_file(pre_data_east_java_name)

#%%

# Group monthly data in temporary file into yearly on destination file
group_into_yearly_data(pre_temp_data_name, pre_data_east_java_name)
group_into_yearly_data(tmp_temp_data_name, tmp_data_east_java_name)

#%%

# Clean up
delete_file(pre_temp_data_name)
delete_file(tmp_temp_data_name)


#%%
# Copy yield data from unprocessed to processed
copyfile(yield_file_name, yield_file_dest)