"""
Draft script to prepare preservation and access copies from an export in the CSS Data Interchange Format.
Required arguments: input_directory (path to the folder with the css export) and script_mode (access or preservation).
"""
from datetime import date
import numpy as np
import os
import pandas as pd
import sys
from css_archiving_format import file_deletion_log


def check_arguments(arg_list):
    """Verify the required script arguments are present and valid and get the paths to the metadata files"""

    # Default values for the variables calculated by this function.
    input_dir = None
    md_paths = {}
    mode = None
    errors = []

    # Both arguments are missing (only the script path is present).
    # Return immediately, or it would also have the error one missing required argument.
    if len(arg_list) == 1:
        errors.append("Missing required arguments, input_directory and script_mode")
        return input_dir, md_paths, mode, errors

    # At least the first argument is present.
    # Verifies it is a valid path, and if so gets the paths to the expected metadata files.
    if len(arg_list) > 1:
        if os.path.exists(arg_list[1]):
            input_dir = arg_list[1]
            # TODO: finalize the tables to include
            expected_files = ['out_1B.dat', 'out_2A.dat', 'out_2C.dat']
            for file in expected_files:
                if os.path.exists(os.path.join(input_dir, file)):
                    # Key is extracted from the filename, for example out_2A.dat has a key of 2A.
                    md_paths[file[4:6]] = os.path.join(input_dir, file)
                else:
                    errors.append(f'Metadata file {file} is not in the input_directory')
        else:
            errors.append(f"Provided input_directory '{arg_list[1]}' does not exist")

    # Both required arguments are present.
    # Verifies the second is one of the expected modes.
    if len(arg_list) > 2:
        if arg_list[2] in ('access', 'preservation'):
            mode = arg_list[2]
        else:
            errors.append(f"Provided mode '{arg_list[2]}' is not 'access' or 'preservation'")
    else:
        errors.append("Missing one of the required arguments, input_directory or script_mode")

    # More than the expected two required arguments are present.
    if len(arg_list) > 3:
        errors.append("Provided more than the required arguments, input_directory and script_mode")

    return input_dir, md_paths, mode, errors


def find_casework_rows(df, output_dir):
    """Find metadata rows with topics or text that indicate they are casework,
     return as a df and log results"""

    # Column group_name starts with "CASE", if any.
    # There are other groups which included "case" that are retained, referring to legal cases of national interest.
    group = df['group_name'].str.startswith('CASE', na=False)
    df_group = df[group]
    df = df[~group]

    # Any column includes the text "casework".
    casework = np.column_stack([df[col].str.contains('casework', case=False, na=False) for col in df])
    df_cw = df.loc[casework.any(axis=1)]
    df = df.loc[~casework.any(axis=1)]

    # Makes a log with any remaining rows with "case" in any column.
    # This may show us another pattern that indicates casework or may be another use of the word case.
    case = np.column_stack([df[col].str.contains('case', case=False, na=False) for col in df])
    if len(df.loc[case.any(axis=1)].index) > 0:
        df.loc[case.any(axis=1)].to_csv(os.path.join(output_dir, 'case_remains_log.csv'), index=False)

    # Makes a single dataframe with all rows that indicate casework
    # and also saves to a log for review for any that are not really casework.
    df_casework = pd.concat([df_group, df_cw], axis=0, ignore_index=True)
    df_casework.to_csv(os.path.join(output_dir, 'case_delete_log.csv'), index=False)
    return df_casework


def read_metadata(paths):
    """Combine the metadata files into a dataframe"""

    # Read each metadata file in the paths dictionary into a separate dataframe,
    # including supplying the column headings.
    # TODO: confirm these column names
    # TODO: be more flexible about expected extra columns at the end of the export
    columns_1b = ['record_type', 'person_id', 'address_id', 'address_type', 'primary_flag', 'default_address_flag',
                  'title', 'organization_name', 'address_line_1', 'address_line_2', 'address_line_3', 'address_line_4',
                  'city', 'state_code', 'zip_code', 'carrier_route', 'county', 'country', 'district', 'precinct',
                  'no_mail_flag', 'deliverability', 'extra1', 'extra2', 'extra3', 'extra4']
    columns_2a = ['record_type', 'person_id', 'communication_id', 'workflow_id', 'workflow_person_id',
                  'communication_type', 'user_id', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                  'update_date', 'response_type', 'address_id', 'email_address', 'household_flag', 'household_id',
                  'group_name', 'salutation', 'extra']
    columns_2c = ['record_type', 'person_id', 'communication_id', 'document_type', 'communication_document_name',
                  'communication_document_id', 'file_location', 'file_name']

    try:
        df_1b = pd.read_csv(paths['1B'], delimiter='\t', dtype=str, on_bad_lines='warn', names=columns_1b)
    except UnicodeDecodeError:
        print("\nUnicodeDecodeError when trying to read the metadata file 1B.")
        print("The file will be read by ignoring encoding errors, skipping characters that cause an error.\n")
        df_1b = pd.read_csv(paths['1B'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                            names=columns_1b)

    try:
        df_2a = pd.read_csv(paths['2A'], delimiter='\t', dtype=str, on_bad_lines='warn', names=columns_2a)
    except UnicodeDecodeError:
        print("\nUnicodeDecodeError when trying to read the metadata file 2A.")
        print("The file will be read by ignoring encoding errors, skipping characters that cause an error.\n")
        df_2a = pd.read_csv(paths['2A'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                            names=columns_2a)

    try:
        df_2c = pd.read_csv(paths['2C'], delimiter='\t', dtype=str, on_bad_lines='warn', names=columns_2c)
    except UnicodeDecodeError:
        print("\nUnicodeDecodeError when trying to read the metadata file 2C.")
        print("The file will be read by ignoring encoding errors, skipping characters that cause an error.\n")
        df_2c = pd.read_csv(paths['2C'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                            names=columns_2c)

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
    df.dropna(how='all', inplace=True)

    return df


def remove_casework_rows(df, df_case):
    """Remove metadata rows with topics or text that indicate they are casework and return the updated df"""

    # Makes an updated dataframe with just rows in df that are not in df_case.
    df_merge = df.merge(df_case, how='left', indicator=True)
    df_update = df_merge[df_merge['_merge'] == 'left_only'].drop(columns=['_merge'])

    return df_update


def remove_casework_letters(input_dir):
    """Remove casework letters received from constituents and individual casework letters sent back by the office"""

    # Reads the deletion log into a dataframe, which is in the parent folder of input_dir if it is present.
    # If it is not, there are no files to delete.
    try:
        df = pd.read_csv(os.path.join(os.path.dirname(input_dir), 'case_delete_log.csv'))
    except FileNotFoundError:
        print(f"No case delete log in {os.path.dirname(input_dir)}")
        return

    # Deletes letters received and sent based on communication_document_name.
    doc_df = df.dropna(subset=['communication_document_name']).copy()
    doc_list = doc_df['communication_document_name'].tolist()
    if len(doc_list) > 0:

        # Creates a file deletion log, with a header row.
        log_path = os.path.join(os.path.dirname(input_dir),
                                f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv")
        file_deletion_log(log_path, None, True)

        # If there is a document name, it is formatted ..\documents\FOLDER\filename.ext
        # Does not delete form letters, which are in FOLDER formletters
        for name in doc_list:
            if 'formletters' not in name:
                file_path = name.replace('..', input_dir)
                try:
                    file_deletion_log(log_path, file_path)
                    os.remove(file_path)
                except FileNotFoundError:
                    file_deletion_log(log_path, file_path, note='Cannot delete: FileNotFoundError')


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
    """Make one CSV per Congress Year"""

    # Saves rows without a year (date is a not a number, could be blank or text) to a CSV, if any.
    # TODO: decide on file name and where it saves.
    df_undated = df[pd.to_numeric(df['date_in'], errors='coerce').isnull()]
    if len(df_undated.index) > 0:
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
    for congress_year, cy_df in df.groupby('congress_year'):
        cy_df = cy_df.drop(['year', 'congress_year'], axis=1)
        cy_df.to_csv(os.path.join(output_dir, f'{congress_year}.csv'), index=False)


if __name__ == '__main__':

    # Validates the script argument values and calculates the paths to the metadata files.
    # If there are any errors, prints them and exits the script.
    input_directory, metadata_paths_dict, script_mode, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Calculates parent folder of the input_directory, which is where script outputs are saved.
    output_directory = os.path.dirname(input_directory)

    # Reads the metadata files, removes columns with PII, and combines into a pandas dataframe.
    md_df = read_metadata(metadata_paths_dict)

    # Finds rows in the metadata that are for casework and saves to a CSV.
    casework_df = find_casework_rows(md_df, output_directory)

    # For preservation, deletes the casework files, which is an appraisal decision.
    # It uses the log from find_casework_rows() to know what to delete.
    if script_mode == 'preservation':
        remove_casework_letters(input_directory)

    # For access, makes a copy of the metadata with tables merged and rows for casework and columns for PII removed
    # and makes a copy of the data split by congress year.
    if script_mode == 'access':
        md_df = remove_casework_rows(md_df, casework_df)
        md_df.to_csv(os.path.join(output_directory, 'Access_Copy.csv'), index=False)
        split_congress_year(md_df, output_directory)

