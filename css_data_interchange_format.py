"""
Draft script to prepare preservation and access copies from an export in the CSS Data Interchange Format.
Required argument: path to the metadata folder (contains all needed DAT files).
"""
import numpy as np
import os
import pandas as pd
import sys


def get_paths(arg_list):
    """Get the paths to the data tables in the folder supplied as script argument"""

    paths_dict = {}
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
        # TODO: finalize the tables to include
        expected_files = ['out_1B.dat', 'out_2A.dat', 'out_2C.dat']
        for file in expected_files:
            if os.path.exists(os.path.join(arg_list[1], file)):
                # Key is extracted from the filename, for example out_2A.dat has a key of 2A.
                paths_dict[file[4:6]] = os.path.join(arg_list[1], file)
            else:
                errors.append(f'Metadata file {file} is not in the metadata folder')

    return paths_dict, errors


def read_metadata(paths):
    """Combine the metadata files into a dataframe"""

    # Read each metadata file in the paths dictionary into a separate dataframe,
    # including supplying the column headings.
    # TODO: confirm these column names
    # TODO: be more flexible about expected extra columns at the end of the export
    df_1b = pd.read_csv(paths['1B'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                        names=['record_type', 'person_id', 'address_id', 'address_type', 'primary_flag',
                               'default_address_flag', 'title', 'organization_name', 'address_line_1', 'address_line_2',
                               'address_line_3', 'address_line_4', 'city', 'state_code', 'zip_code', 'carrier_route',
                               'county', 'country', 'district', 'precinct', 'no_mail_flag', 'deliverability',
                               'extra1', 'extra2', 'extra3', 'extra4'])
    df_2a = pd.read_csv(paths['2A'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                        names=['record_type', 'person_id', 'communication_id', 'workflow_id', 'workflow_person_id',
                               'communication_type', 'user_id', 'approved_by', 'status', 'date_in', 'date_out',
                               'reminder_date', 'update_date', 'response_type', 'address_id', 'email_address',
                               'household_flag', 'household_id', 'group_name', 'salutation', 'extra'])
    df_2c = pd.read_csv(paths['2C'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                        names=['record_type', 'person_id', 'communication_id', 'document_type',
                               'communication_document_name', 'communication_document_id', 'file_location',
                               'file_name'])

    # Removes unneeded columns from each dataframe, except for ID columns needed for merging.
    # Otherwise, it would be too much data to merge.
    df_1b = remove_pii(df_1b)
    df_2a = remove_pii(df_2a)
    df_2c = remove_pii(df_2c)

    # Combine the dataframes using ID columns.
    # If an id is only in one table, the data is still included and has blanks for columns from the other table.
    # TODO need error handling if the id is blank?
    df = df_1b.merge(df_2a, on='person_id', how='outer')
    df = df.merge(df_2c, on='communication_id', how='outer')

    # Remove ID columns only used for merging.
    df = df.drop(['person_id_x', 'person_id_y', 'communication_id'], axis=1, errors='ignore')

    # Removes blank rows, which are present in some of the data exports.
    # Blank rows have an empty string in every column.
    df = df[~(df == '').all(axis=1)]

    return df


def remove_casework(df, output_dir):
    """Remove rows with topics or text that indicate they are casework and log results"""

    # Deletion log path (used multiple times)
    del_log = os.path.join(output_dir, 'metadata_deletion_log.csv')

    # Removes row if column group_name starts with "CASE".
    # There are other groups which included "case" that are retained, referring to legal cases of national interest.
    # Deleted rows are saved to a log for review.
    group = df['group_name'].str.startswith('CASE', na=False)
    df[group].to_csv(os.path.join(del_log), index=False)
    df = df[~group]

    # Removes row if any column includes the text "casework".
    # Deleted rows, if any, are saved to a log for review.
    includes_casework = np.column_stack([df[col].str.contains('casework', case=False, na=False) for col in df])
    df.loc[includes_casework.any(axis=1)].to_csv(del_log, mode='a', header=not os.path.exists(del_log), index=False)
    df = df.loc[~includes_casework.any(axis=1)]

    # Remaining rows with "case" in any column are saved to a log for review.
    # This may show us another pattern that indicates casework or may be another use of the word case.
    includes_case = np.column_stack([df[col].str.contains('case', case=False, na=False) for col in df])
    df.loc[includes_case.any(axis=1)].to_csv(os.path.join(output_dir, 'case_remains_log.csv'), index=False)

    return df


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed. Includes names and address information
    # and "extra" columns due to extra blank columns at the end of each row in the export.
    # TODO: confirm this list (extra can have hint at subject but is an unexpected column)
    remove = ['record_type', 'address_id', 'address_type', 'primary_flag', 'default_address_flag',
              'title', 'organization_name', 'address_line_1', 'address_line_2', 'address_line_3', 'address_line_4',
              'carrier_route', 'county', 'district', 'precinct', 'no_mail_flag', 'deliverability', 'workflow_id',
              'workflow_person_id', 'user_id', 'address_id_y', 'email_address', 'household_flag', 'household_id',
              'salutation', 'extra', 'extra1', 'extra2', 'extra3', 'extra4']

    # Removes every column on the remove list from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    df = df.drop(remove, axis=1, errors='ignore')

    return df


def split_congress_year(df, output_dir):
    """Make one CSV per Congress Year in the folder with the original metadata files"""

    # Saves rows without a year (date is a not a number, could be blank or text) to a CSV.
    # TODO: decide on file name and where it saves.
    df_undated = df[pd.to_numeric(df['date_in'], errors='coerce').isnull()]
    df_undated.to_csv(os.path.join(output_dir, 'undated.csv'), index=False)

    # Removes rows without a year from the dataframe, so the rest can be split by Congress Year.
    df = df[pd.to_numeric(df['date_in'], errors='coerce').notnull()].copy()

    # Adds a column with the year received, which will be used to calculate the Congress Year.
    # Column in_date is formatted YYYYMMDD.
    df.loc[:, 'year'] = df['date_in'].astype(str).str[:4].astype(int)

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

    # Gets the paths to the metadata files from the script argument.
    # If the script argument is missing or any are not valid paths, prints the errors and exits the script.
    paths_dictionary, errors_list = get_paths(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Calculates parent folder of the input_directory, which is where script outputs are saved.
    output_directory = os.path.dirname(sys.argv[1])

    # Reads the metadata files and combines into a pandas dataframe.
    md_df = read_metadata(paths_dictionary)

    # Removes rows for casework, if they are present.
    md_df = remove_casework(md_df, output_directory)

    # Saves the redacted data to a CSV file.
    md_df.to_csv(os.path.join(output_directory, 'Access_Copy.csv'), index=False)

    # Saves a copy of the redacted data to one CSV per Congress Year in the folder with the original metadata files.
    split_congress_year(md_df, output_directory)
