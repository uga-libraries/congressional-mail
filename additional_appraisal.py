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

if __name__ == '__main__':

    # Validates the script argument values.
    # If there are any errors, prints them and exits the script.

    # Gets information for the file deletion log and saves to a csv in the output_directory.

    # Gets metadata rows for the appraisal delete log and saves to a csv in the output_directory.