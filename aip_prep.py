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


def empty_log(output_dir, empty_path):
    """Make a text file with the path to any empty subfolder"""

    # If this is the first empty subfolder (log does not exist), creates it with explanatory text and adds the path.
    # Otherwise, adds the path to the existing log.
    log_path = os.path.join(output_dir, 'empty_subfolders_log.txt')
    if not os.path.exists(log_path):
        with open(log_path, 'w') as log:
            log.write(f'{empty_path} was empty on {datetime.now().strftime("%Y-%m-%d")} '
                      f'when this export was split into smaller folders for AIP creation\n')
    else:
        with open(log_path, 'a') as log:
            log.write(f'{empty_path} was empty on {datetime.now().strftime("%Y-%m-%d")} '
                      f'when this export was split into smaller folders for AIP creation\n')


def metadata_aip(input_dir, aips_dir):
    """Make the AIP for the metadata, which are the files directly within the input_dir"""

    # Makes a folder for the AIP.
    # There are always few enough files for the metadata to be a single AIP.
    aip_path = os.path.join(aips_dir, 'metadata')
    os.mkdir(aip_path)

    # Copies all files directly within input_dir to the AIP folder.
    # The only other thing in that location is a folder named "documents".
    for metadata_file in os.listdir(input_dir):
        if not metadata_file == 'documents':
            shutil.copy2(os.path.join(input_dir, metadata_file), os.path.join(aip_path, metadata_file))


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


def type_aip(aips_dir, metadata_path, paths_list, type_path):
    """Copies every 10,000 files, including replicating subfolders, to an AIP folder."""
    for i in range(0, len(paths_list), 10000):

        # Makes a folder for this AIP.
        seq_number = i // 10000 + 1
        aip_folder_name = f'{os.path.basename(type_path).lower()}_{seq_number}'
        aip_folder_path = os.path.join(aips_dir, aip_folder_name)
        os.mkdir(aip_folder_path)

        # Copies the files for this AIP.
        # The relative path to the file is used to replicate the subfolders.
        included_files = paths_list[i:i + 10000]
        for file_path in included_files:
            relative_path = Path(file_path).relative_to(type_path)
            subfolder_path = os.path.join(aip_folder_path, os.path.dirname(relative_path))
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
            shutil.copy2(file_path, os.path.join(aip_folder_path, relative_path))

        # Adds this AIP to the metadata csv.
        metadata_csv(metadata_path, ['', '', aip_folder_name, '', f'CSS {type_folder} {seq_number}', '1'])


def type_files(output_dir, type_path):
    """Returns a list with the path to every file in the type folder, including if it is within subfolders"""
    paths_list = []
    for root, dirs, files in os.walk(type_path):
        for file in files:
            paths_list.append(os.path.join(root, file))
        # Makes a log of any empty subfolders, since those will not be included in the final AIPs.
        if not dirs and not files:
            empty_log(output_dir, root)
    return paths_list


if __name__ == '__main__':

    # Gets the path to the export from the script argument.
    input_directory = sys.argv[1]

    # Makes a folder aips_dir in the parent folder of the input_directory for most script output.
    output_directory = os.path.dirname(input_directory)
    aips_directory = os.path.join(output_directory, 'aips_dir')
    os.mkdir(aips_directory)
    
    # Starts the metadata.csv.
    metadata_csv_path = os.path.join(aips_directory, 'metadata.csv')
    metadata_csv(metadata_csv_path, 'header')
    
    # Copies metadata files to an AIP folder and adds it to the metadata.csv.
    metadata_aip(input_directory, aips_directory)
    metadata_csv(metadata_csv_path, ['', '', 'metadata', '', 'CSS Metadata', '1'])

    # For each type folder, copies into AIP folders (maximum 10,000 files) while maintaining folder hierarchy,
    # and adds to metadata.csv.
    for type_folder in os.listdir(os.path.join(input_directory, 'documents')):
        type_folder_path = os.path.join(input_directory, 'documents', type_folder)
        file_paths_list = type_files(output_directory, type_folder_path)
        type_aip(aips_directory, metadata_csv_path, file_paths_list, type_folder_path)
