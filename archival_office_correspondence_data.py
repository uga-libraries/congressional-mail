"""
Draft script to prepare access copies from an export in the Archival Office Correspondence Data format.
"""
import os
import pandas as pd
import sys
from css_archiving_format import check_argument, save_df, split_congress_year


if __name__ == 'main':

    # Gets the path to the metadata file from the script argument.
    # If it is missing or not a valid path, prints an error and exits the script.
    md_path, error_message = check_argument(sys.argv)
    if error_message:
        print(error_message)
        sys.exit(1)

    # Reads the metadata file into a pandas dataframe.

    # Removes columns with personally identifiable information, if they are present.

    # Saves the redacted data to a CSV file in the folder with the original metadata file.
    # save_df(md_df, os.path.dirname(md_path))

    # Saves a copy of the redacted data to one CSV per Congress Year in the folder with the original metadata file.
    # split_congress_year(md_df, os.path.dirname(md_path))
