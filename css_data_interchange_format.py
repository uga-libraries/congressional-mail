"""
Draft script to prepare access copies from an export in the CSS Data Interchange Format.
"""
import os
import pandas as pd
import sys
from css_archiving_format import save_df


def get_paths(arg_list):
    """Get the paths to the data tables in the folder supplied as script argument"""

    paths = {}
    errors = []

    # Argument is missing (only the script path is present).
    if len(arg_list) == 1:
        errors.append("Missing required argument: path to the metadata folder")
    # Argument is present but not a valid path.
    elif not os.path.exists(arg_list[1]):
        errors.append(f"Provided path to metadata folder does not exist: {arg_list[1]}")
    # Argument is correct.
    # Tests the paths to each expected metadata file.
    # If the metadata file is present, it updates the dictionary value for that path.
    # If it is missing, it adds to the errors list.
    else:
        expected_files = ['out_1B.dat', 'out_2A.dat']
        for file in expected_files:
            if os.path.exists(os.path.join(arg_list[1], file)):
                paths[file[:6]] = os.path.join(arg_list[1], file)
            else:
                errors.append(f'Metadata file {file} is not in the metadata folder')

    return paths, errors


if __name__ == '__main__':

    # Gets the paths to the metadata files from the script argument.
    # If the script argument is missing or any are not valid paths, prints the errors and exits the script.
    paths_dict, errors_list = get_paths(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Reads the metadata files and combines into a pandas dataframe.

    # Removes columns with personally identifiable information, if they are present.

    # Saves the redacted data to a CSV file in the folder with the original metadata files.

    # Saves a copy of the redacted data to one CSV per Congress Year in the folder with the original metadata files.
