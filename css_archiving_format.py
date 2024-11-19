"""
Draft script to prepare access copies from an export in the CSS Archiving Format.
Required arguments: input_directory (path to the folder with the css export) and script_mode (access or preservation).
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
            if os.path.exists(os.path.join(input_dir, 'archiving_correspondence.dat')):
                md_path = os.path.join(input_dir, 'archiving_correspondence.dat')
            else:
                errors.append(f"No archiving_correspondence.dat file in the input_directory")
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
    # TODO: document ParserError?. Rows that are printed by on_bad_lines='warn' are not included in the output.
    # TODO: document the encoding errors?
    df = pd.read_csv(path, delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn')

    # Removes blank rows, which are present in some of the data exports.
    df.dropna(how='all', inplace=True)

    return df


def remove_casework(df, input_dir):
    """Remove rows with topics or text that indicate they are case mail"""

    # Removes row if column in_topic includes one of the topics that indicates casework.
    # There may be more than one topic in that column.
    # Deleted rows are saved to a log for review.
    # TODO: combine deleted content into a single log.
    topics_list = ['Casework', 'Casework Issues', 'Prison Case']
    casework_topic = df['in_topic'].str.contains('|'.join(topics_list), na=False)
    df[casework_topic].to_csv(os.path.join(input_dir, 'topic_deletion_log.csv'), index=False)
    df = df[~casework_topic]

    # Removes row if any column includes the text "casework".
    # This removes some rows where the text indicates they are not casework,
    # which is necessary to protect privacy and keep time required reasonable.
    # Deleted rows are saved to a log for review.
    includes_casework = np.column_stack([df[col].str.contains('casework', case=False, na=False) for col in df])
    df.loc[includes_casework.any(axis=1)].to_csv(os.path.join(input_dir, 'casework_anywhere_deletion_log.csv'),
                                                 index=False)
    df = df.loc[~includes_casework.any(axis=1)]

    # Remaining rows with "case" in any column are saved to a log for review.
    # This may show us another pattern that indicates casework or may be another use of the word case.
    includes_case = np.column_stack([df[col].str.contains('case', case=False, na=False) for col in df])
    df.loc[includes_case.any(axis=1)].to_csv(os.path.join(input_dir, 'row_includes_case_log.csv'), index=False)

    return df


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed. Includes names and address information.
    # TODO: confirm this list
    remove = ['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
              'addr1', 'addr2', 'addr3', 'addr4']

    # Removes every column on the remove list from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    df = df.drop(remove, axis=1, errors='ignore')
    
    return df


def split_congress_year(df, output_dir):
    """Make one CSV per Congress Year"""

    # Saves rows without a year (date is a not a number, could be blank or text) to a CSV, if any.
    # TODO: confirm that text in place of date should be in undated: usually an error in the number of columns.
    # TODO: decide on file name and where it saves.
    df_undated = df[pd.to_numeric(df['in_date'], errors='coerce').isnull()]
    if len(df_undated.index) > 0:
        df_undated.to_csv(os.path.join(output_dir, 'undated.csv'), index=False)

    # Removes rows without a year from the dataframe, so the rest can be split by Congress Year.
    df = df[pd.to_numeric(df['in_date'], errors='coerce').notnull()].copy()

    # Adds a column with the year received, which will be used to calculate the Congress Year.
    # Column in_date is formatted YYYYMMDD.
    df.loc[:, 'year'] = df['in_date'].astype(str).str[:4].astype(int)

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
        cy_df.to_csv(os.path.join(output_dir, f'{congress_year}.csv'), index=False)


if __name__ == '__main__':

    # Validates the script argument values and calculates the path to the metadata file.
    # If there are any errors, prints them and exits the script.
    input_directory, metadata_path, script_mode, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Calculates parent folder of the input_directory, which is where script outputs are saved.
    output_directory = os.path.dirname(input_directory)

    # Reads the metadata file into a pandas dataframe.
    md_df = read_metadata(metadata_path)

    # For access, removes columns with PII and makes a copy of the data split by congress year.
    # For preservation, removes rows for casework and deletes the casework files themselves.
    if script_mode == 'access':
        md_df = remove_pii(md_df)
        md_df.to_csv(os.path.join(output_directory, 'Access_Copy.csv'), index=False)
        split_congress_year(md_df, output_directory)
    else:
        md_df = remove_casework(md_df, os.path.dirname(metadata_path))
        md_df.to_csv(os.path.join(output_directory, os.path.basename(metadata_path)), sep='\t', index=False)
