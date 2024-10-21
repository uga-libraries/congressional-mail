"""
Draft script to prepare access copies from an export in the Archival Office Correspondence Data format.
"""
import os
import pandas as pd
import sys
from css_archiving_format import check_argument, save_df, split_congress_year


def read_metadata(path):
    """Read the metadata file into a dataframe"""

    # Makes a list from the file contents with one list per row and one item per column,
    # splitting the data into columns based on the character position and removing extra spaces.
    # TODO: original data can be all caps. Should we change the case or leave it?
    rows_list = []
    positions = [(0, 39), (39, 69), (69, 99), (99, 129), (129, 159), (159, 189), (189, 191), (191, 201), (201, 251),
                 (251, 301), (301, 351), (351, 357), (357, 361), (361, 371), (371, 471)]
    with open(path) as open_file:
        for line in open_file:
            row_list = [line[slice(*pos)].strip() for pos in positions]
            rows_list.append(row_list)

    # Save as a dataframe, with column names.
    # TODO: verify these column names.
    columns_list = ['name', 'title', 'organization', 'address_line_1', 'address_line_2', 'city', 'state_code',
                    'zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic',
                    'letter_date', 'staffer_initials', 'document_number', 'comments']
    df = pd.DataFrame(rows_list, columns=columns_list, dtype=str)

    return df


if __name__ == '__main__':

    # Gets the path to the metadata file from the script argument.
    # If it is missing or not a valid path, prints an error and exits the script.
    md_path, error_message = check_argument(sys.argv)
    if error_message:
        print(error_message)
        sys.exit(1)

    # Reads the metadata file into a pandas dataframe.
    md_df = read_metadata(md_path)

    # Removes columns with personally identifiable information, if they are present.

    # Saves the redacted data to a CSV file in the folder with the original metadata file.
    # save_df(md_df, os.path.dirname(md_path))

    # Saves a copy of the redacted data to one CSV per Congress Year in the folder with the original metadata file.
    # split_congress_year(md_df, os.path.dirname(md_path))
