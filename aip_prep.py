"""
Script to split an export of any type into folders small enough for AIPs in our preservation system (ARCHive).
Also starts the metadata.csv. Add the remaining fields in Excel and then run general_aip.py to make the AIPs.

The export should have letters deleted for appraisal but the original (non-redacted metadata)
prior to running this script.

The initial copy of the export may be deleted after confirming this script ran correctly
and creating the access copies.

Required argument: input_directory (path to the folder with the export)

Script outputs:
- Folder "aips_dir" in the parent folder of the input_directory
    - Copy of export split into folders with maximum of 10,000 files per folder
    - File "metadata.csv" with the AIP folder, title, and version filled in
- File "empty_subfolders_log.txt", if any, in the parent folder of the input_directory
"""

import csv
from datetime import datetime
import os
from pathlib import Path
import shutil
import sys


def metadata_csv(csv_path, row):
    """Make the metadata.csv (if row is header) and add a row to the metadata.csv (header or one AIP's data)"""
    if row == 'header':
        with open(csv_path, 'w', newline='') as md_csv:
            md_writer = csv.writer(md_csv)
            md_writer.writerow(['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'])
    else:
        with open(csv_path, 'a', newline='') as md_csv:
            md_writer = csv.writer(md_csv)
            md_writer.writerow(row)


if __name__ == '__main__':

    # Gets the path to the export from the script argument.
    input_directory = sys.argv[1]

    # Makes a folder aips_dir in the parent folder of the input_directory for most script output.
    output_directory = os.path.dirname(input_directory)
    aips_dir = os.path.join(output_directory, 'aips_dir')
    os.mkdir(aips_dir)
    
    # Starts the metadata.csv.
    metadata_csv_path = os.path.join(aips_dir, 'metadata.csv')
    metadata_csv(metadata_csv_path, 'header')
    
    # Copies metadata (loose files directly within input_directory) to AIP folder and adds to metadata.csv.
    # Skips the documents folder that contains the exported letters.
    aip_folder_path = os.path.join(aips_dir, 'metadata')
    os.mkdir(aip_folder_path)
    for metadata_file in os.listdir(input_directory):
        if not metadata_file == 'documents':
            shutil.copy2(os.path.join(input_directory, metadata_file), os.path.join(aip_folder_path, metadata_file))
    metadata_csv(metadata_csv_path, ['', '', 'metadata', '', 'CSS Metadata', '1'])

    # For each type folder, copies into AIP folders (maximum 10,000 files) while maintaining folder hierarchy,
    # and adds to metadata.csv.
    for type_folder in os.listdir(os.path.join(input_directory, 'documents')):
        type_path = os.path.join(input_directory, 'documents', type_folder)
        # Gets the path to every file in the type folder, including if it is in subfolders.
        file_paths_list = []
        for root, dirs, files in os.walk(type_path):
            for file in files:
                file_paths_list.append(os.path.join(root, file))
            # Makes a log of any empty subfolders, since those will not be included in the final AIPs.
            if not dirs and not files:
                with open(os.path.join(output_directory, 'empty_subfolders_log.txt'), 'a') as log:
                    log.write(f'{root} was empty on {datetime.now().strftime("%Y-%m-%d")} '
                              f'when this export was split into smaller folders for AIP creation\n')
        # Copies every 10,000 files, including replicating subfolders, to an AIP folder.
        for i in range(0, len(file_paths_list), 10000):
            # Makes folder for this AIP.
            seq_number = i // 10000 + 1
            aip_folder_name = f'{type_folder.lower()}_{seq_number}'
            aip_folder_path = os.path.join(aips_dir, aip_folder_name)
            os.mkdir(aip_folder_path)
            # Copies files for this AIP.
            # The relative path to the file is used to replicate the subfolders.
            included_files = file_paths_list[i:i + 10000]
            for file_path in included_files:
                relative_path = Path(file_path).relative_to(type_path)
                subfolder_path = os.path.join(aip_folder_path, os.path.dirname(relative_path))
                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)
                shutil.copy2(file_path, os.path.join(aip_folder_path, relative_path))
            # Add to metadata.csv
            metadata_csv(metadata_csv_path, ['', '', aip_folder_name, '', f'CSS {type_folder} {seq_number}', '1'])
