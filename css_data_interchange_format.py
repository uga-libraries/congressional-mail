"""
Draft script to prepare access copies from an export in the CSS Data Interchange Format.
"""
import os
import pandas as pd
import sys
from css_archiving_format import save_df


if __name__ == '__main__':

    # Gets the paths to the metadata files from the script argument.
    # If the script argument is missing or any are not valid paths, prints an error and exits the script.

    # Reads the metadata files and combines into a pandas dataframe.

    # Removes columns with personally identifiable information, if they are present.

    # Saves the redacted data to a CSV file in the folder with the original metadata files.

    # Saves a copy of the redacted data to one CSV per Congress Year in the folder with the original metadata files.
