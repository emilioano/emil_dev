import os
import shutil
import pandas as pd
from tqdm import tqdm

# Define paths
excel_file = 'file_move.xlsx'  # Excel file with From and To columns
source_folder = r'files'
#source_folder = r'\\corp.hitachi-powergrids.com\SE\ERPLN\ERPLN_Dev\win\Z'       # Folder where the files are located

# Dyrun to enable simulation mode.
dryrun = False

# Split filename before
splitfilenamebefore = '_Rev.'

# Folder name join delimiter
foldernamejoindelim = 'till'

# Creating empty list where possible error messages gets stored
errorlist = []

# Debug
#print(os.listdir(r'\\corp.hitachi-powergrids.com\SE\ERPLN\ERPLN_Dev\win\Z'))

# Load the Excel file and normalize column names
df = pd.read_excel(excel_file, engine='openpyxl')
df.columns = df.columns.str.strip().str.lower()

# Check required columns
if 'from' not in df.columns or 'to' not in df.columns:
    raise ValueError("Excel file must contain 'From' and 'To' columns.")

# Preload all relevant files once

print(f'Reading full file list from {source_folder}')
all_files = [
    f for f in tqdm(os.listdir(source_folder), desc="Reading files")
    if splitfilenamebefore in f and os.path.isfile(os.path.join(source_folder, f))
]
print(f'File list, files with name before: {splitfilenamebefore}, loaded successfully from {source_folder}')

#Debug
#input('Enter to continue')

# Iterate through each row in Excel
for index, row in df.iterrows():
    from_value = str(row['from'])
    to_value = str(row['to'])
    print(f'Reading from Excel. From: {from_value}, to: {to_value}.')

    # Create folder name like "ABC till XYZ"
    folder_name = f"{from_value} {foldernamejoindelim} {to_value}"
    target_folder = os.path.join(source_folder, folder_name)
    files_moved = False

    # Match files within the range
    for filename in all_files:

        name_part = filename.split(splitfilenamebefore)[0]

        if from_value <= name_part <= to_value:
            print(f'Working on file {filename}.')
            
            if not files_moved:
                    if not dryrun:
                        os.makedirs(target_folder, exist_ok=True)
                        files_moved = True
                    else:
                        print(f'** Dry run ** Target folder {target_folder} is now created or already exists')

            # Move the file
            if not dryrun:
                full_path = os.path.join(source_folder, filename)
                destination = os.path.join(target_folder, filename)
                try:
                    shutil.move(full_path, destination)
                    print(f"Moved {filename} to {target_folder}")
                except Exception as error:
                    print(f'Error occured when moving {filename}. Error: {error}. Will continue with next')
                    errorlist.append(f'Error when moving {filename}. Error: {error}.')
                    continue
            else:
                print(f'** Dry run ** Moved {filename} to {target_folder}')
        
if errorlist:
    print('Following issues occured during the process and those where skipped:')
    for error in errorlist:
        print(error)
