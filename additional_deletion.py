"""
Get file metadata and metadata rows for files that will be deleted after manual appraisal review,
so they can be properly logged and exlucded from the access copy redacted metadata.

Prior to running the script move all files to be deleted into a single directory.
Do not delete until after running this script.

Arguments (all required):
    export_type: cms_dif, css_arch, or css_dif
    delete_directory: path to the folder with files to delete (may contain subfolders)
    input_directory: path to the folder with the export
    output_directory: path to the folder where script outputs will be saved

Returns:
    file_deletion_log_addition.csv
    appraisal_delete_log_addition.csv
"""
import csv
from datetime import date, datetime
import hashlib
import os
import pandas as pd
import sys
import time


def check_arguments(arg_list):
    """Verify the required script arguments are present and valid"""

    # Default values for the variables calculated by this function.
    export = None
    delete_dir = None
    input_dir = None
    output_dir = None
    errors = []

    # Tests the values of each argument if the correct number (4) are provided.
    # Otherwise, returns a message about the number of arguments
    if len(arg_list) == 5:
        if arg_list[1] in ('cms_dif', 'css_arch', 'css_dif'):
            export = arg_list[1]
        else:
            errors.append("export_type is not an expected value")
        if os.path.exists(arg_list[2]):
            delete_dir = arg_list[2]
        else:
            errors.append("delete_directory is not a valid directory")
        if os.path.exists(arg_list[3]):
            input_dir = arg_list[3]
        else:
            errors.append("input_directory is not a valid directory")
        if os.path.exists(arg_list[4]):
            output_dir = arg_list[4]
        else:
            errors.append("output_directory is not a valid directory")
    elif len(arg_list) < 5:
        errors.append("At least one of the four required arguments is missing")
    else:
        errors.append("More than the expected four required arguments were provided")

    return export, delete_dir, input_dir, output_dir, errors


def update_delete_log(log_path, file_path):
    """Get information about the specified file and add it to the log"""

    # Get the metadata values required for the log.
    # FileNotFoundError can happen due to path lengths or special characters.
    try:
        size_kb = round(int(os.path.getsize(file_path)) / 1000, 1)
        date_c = datetime.strptime(time.ctime(os.path.getctime(file_path)), '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d')
        with open(file_path, 'rb') as f:
            file_data = f.read()
        md5 = hashlib.md5(file_data).hexdigest().upper()
        date_d = date.today().strftime('%Y-%m-%d')
        row = [file_path, size_kb, date_c, date_d, md5, 'Additional deletion: ADD REASON']
    except FileNotFoundError:
        row = [file_path, None, None, None, None, 'Additional deletion: FileNotFoundError']

    # Save the metadata as a row in the log.
    with open(log_path, 'a', newline='') as log:
        log_writer = csv.writer(log)
        log_writer.writerow(row)

if __name__ == '__main__':

    # Validates the script argument values.
    # If there are any errors, prints them and exits the script.
    export_type, delete_directory, input_directory, output_directory, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Starts the deletion log, with a header.
    deletion_log_path = os.path.join(output_directory, 'file_deletion_log_addition.csv')
    with open(deletion_log_path, 'w', newline='') as deletion_log:
        deletion_log_writer = csv.writer(deletion_log)
        deletion_log_writer.writerow(['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'])

    # Gets the path to every file in the delete_directory and adds it to the deletion log.
    for root, dirs, files in os.walk(delete_directory):
        for file in files:
            delete_file_path = os.path.join(root, file)
            update_delete_log(deletion_log_path, delete_file_path)

    # Gets metadata rows for the appraisal delete log and saves to a csv in the output_directory.