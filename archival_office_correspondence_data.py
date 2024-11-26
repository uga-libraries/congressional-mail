"""
Draft script to prepare access copies from an export in the Archival Office Correspondence Data format.
Required argument: path to the DAT file with the metadata export.
"""
import numpy as np
import os
import pandas as pd
import sys


def check_arguments(arg_list):
    """Verify the required script arguments are present and valid and get the path to the metadata file"""

    # Default values for the variables calculated by this function.
    input_dir = None
    md_path = None
    mode = None
    errors = []

    # Both arguments are missing (only the script path is present).
    if len(arg_list) == 1:
        errors.append("Missing required arguments, input_directory and script_mode")

    # At least the first argument is present.
    # Verifies it is a valid path, and if so that it contains the expected DAT file.
    if len(arg_list) > 1:
        if os.path.exists(arg_list[1]):
            input_dir = arg_list[1]
            if os.path.exists(os.path.join(input_dir, 'archive.dat')):
                md_path = os.path.join(input_dir, 'archive.dat')
            else:
                errors.append(f"No archive.dat file in the input_directory")
        else:
            errors.append(f"Provided input_directory '{arg_list[1]}' does not exist")

    # Both required arguments are present.
    # Verifies the second is one of the expected modes.
    if len(arg_list) > 2:
        if arg_list[2] in ('access', 'preservation'):
            mode = arg_list[2]
        else:
            errors.append(f"Provided mode '{arg_list[2]} is not 'access' or 'preservation'")

    # More than the expected two required arguments are present.
    if len(arg_list) > 3:
        errors.append("Provided more than the required arguments, input_directory and script_mode")

    return input_dir, md_path, mode, errors


def read_metadata(path):
    """Read the metadata file into a dataframe"""

    # Makes a list from the file contents with one list per row and one item per column,
    # splitting the data into columns based on the character position and removing extra spaces.
    rows_list = []
    positions = [(0, 39), (39, 69), (69, 99), (99, 129), (129, 159), (159, 189), (189, 191), (191, 201), (201, 251),
                 (251, 301), (301, 351), (351, 357), (357, 361), (361, 371), (371, 471)]
    with open(path) as open_file:
        for line in open_file:
            row_list = [line[slice(*pos)].strip() for pos in positions]
            rows_list.append(row_list)

    # Save as a dataframe, with column names.
    # TODO: verify these column names.
    # TODO: add error handling for if the data is not the expected number of columns?
    columns_list = ['name', 'title', 'organization', 'address_line_1', 'address_line_2', 'city', 'state_code',
                    'zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic',
                    'letter_date', 'staffer_initials', 'document_number', 'comments']
    df = pd.DataFrame(rows_list, columns=columns_list, dtype=str)

    return df


def remove_casework(df, input_dir):
    """Remove rows with topics or text that indicate they are case mail"""

    # Removes row if any column includes the text "CASE".
    # It is typically within the columns correspondence_topic or comments
    # and includes a few rows that are not really casework, such as "Casey" or his "on the case" catchphrase,
    # which is necessary to protect privacy and keep time required reasonable.
    # Deleted rows are saved to a log for review.
    includes_casework = np.column_stack([df[col].str.contains('CASE', case=False, na=False) for col in df])
    df.loc[includes_casework.any(axis=1)].to_csv(os.path.join(input_dir, 'casework_deletion_log.csv'), index=False)
    df = df.loc[~includes_casework.any(axis=1)]

    return df


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed. Includes names and address information.
    # TODO: confirm this list
    remove = ['name', 'title', 'organization', 'address_line_1', 'address_line_2']

    # Removes every column on the remove list from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    df = df.drop(remove, axis=1, errors='ignore')

    return df


def split_congress_year(df, input_dir):
    """Make one CSV per Congress Year in the folder with the original metadata file"""

    # Saves rows without a year (date is a not a number, could be blank or text) to a CSV.
    # TODO: confirm that text in place of date should be in undated: usually an error in the number of columns.
    # TODO: decide on file name and where it saves.
    df_undated = df[pd.to_numeric(df['letter_date'], errors='coerce').isnull()]
    df_undated.to_csv(os.path.join(input_dir, 'undated.csv'), index=False)

    # Removes rows without a year from the dataframe, so the rest can be split by Congress Year.
    df = df[pd.to_numeric(df['letter_date'], errors='coerce').notnull()].copy()

    # Adds a column with the year received, which will be used to calculate the Congress Year.
    # Column letter_date is formatted YYMMDD.
    # First the two digit year is extracted, and then it is made a four-digit year by adding 1900 or 2000.
    # TODO: confirm 1960 as the cut off for 1900s vs 2000s.
    df.loc[:, 'year'] = df['letter_date'].astype(str).str[:2].astype(int)
    df.loc[df['year'] >= 60, 'year'] = df['year'] + 1900
    df.loc[df['year'] < 60, 'year'] = df['year'] + 2000

    # Adds a column with the Congress Year received, which is a two-year range starting with an odd year.
    # First, if the year received is even, the Congress Year is year-1 to year.
    # Second, if the year received is odd, the Congress Year is year to year+1.
    df.loc[df['year'] % 2 == 0, 'congress_year'] = (df['year'] - 1).astype(str) + '-' + df['year'].astype(str)
    df.loc[df['year'] % 2 == 1, 'congress_year'] = df['year'].astype(str) + '-' + (df['year'] + 1).astype(str)

    # Splits the data by Congress Year received and saves each to a separate CSV.
    # The year and congress_year columns are first removed, so the CSV only has the original columns.
    # TODO: decide on file name and where it saves.
    for congress_year, cy_df in df.groupby('congress_year'):
        cy_df = cy_df.drop(['year', 'congress_year'], axis=1)
        cy_df.to_csv(os.path.join(input_dir, f'{congress_year}.csv'), index=False)


if __name__ == '__main__':

    # Validates the script argument values and calculates the path to the metadata file.
    # If there are any errors, prints them and exits the script.
    input_directory, metadata_path, script_mode, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Reads the metadata file into a pandas dataframe.
    md_df = read_metadata(metadata_path)

    # Removes columns with personally identifiable information, if they are present.
    md_df = remove_pii(md_df)

    # Removes rows for casework, if they are present.
    md_df = remove_casework(md_df, os.path.dirname(metadata_path))

    # Saves the redacted data to a CSV file in the folder with the original metadata file.
    save_df(md_df, os.path.dirname(metadata_path))

    # Saves a copy of the redacted data to one CSV per Congress Year in the folder with the original metadata file.
    split_congress_year(md_df, os.path.dirname(metadata_path))
