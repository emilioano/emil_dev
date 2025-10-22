import os
import shutil
import pandas as pd
from tqdm import tqdm

# Define the folder to scan
#folder_path = 'files'  # Replace with your actual folder path
folder_path = r'\\corp.hitachi-powergrids.com\SE\ERPLN\ERPLN_Dev\win\Z'       # Folder where the files are located

# List all files in the folder
file_list = [f for f in tqdm(os.listdir(folder_path), desc='Reading files:') if os.path.isfile(os.path.join(folder_path, f))]

# Create a DataFrame
df = pd.DataFrame({'Files': file_list})

# Save to Excel
output_excel = 'file_list.xlsx'
df.to_excel(output_excel, index=False, engine='openpyxl')

print(f"Excel file '{output_excel}' created with {len(file_list)} filenames.")
