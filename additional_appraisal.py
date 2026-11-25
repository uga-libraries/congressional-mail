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
import os
import pandas as pd
import sys


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
            delete_dir = arg_list[3]
        else:
            errors.append("input_directory is not a valid directory")
        if os.path.exists(arg_list[4]):
            delete_dir = arg_list[4]
        else:
            errors.append("output_directory is not a valid directory")
    elif len(arg_list) > 5:
        errors.append("At least one of the four required arguments is missing")
    else:
        errors.append("More than the expected four required arguments were provided")

    return export, delete_dir, input_dir, output_dir, errors






if __name__ == '__main__':

    # Validates the script argument values.
    # If there are any errors, prints them and exits the script.
    export_type, delete_directory, input_directory, output_directory, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Gets information for the file deletion log and saves to a csv in the output_directory.

    # Gets metadata rows for the appraisal delete log and saves to a csv in the output_directory.