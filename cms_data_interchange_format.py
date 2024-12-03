"""
Draft script to prepare preservation and access copies from an export in the CMS Data Interchange Format.
Required arguments: input_directory (path to the folder with the cms export) and script_mode (access or preservation).
"""
import numpy as np
import os
import pandas as pd
import sys
from css_data_interchange_format import split_congress_year


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
            expected_files = ['1B.out', '2A.out', '2B.out', '2C.out']
            for file in expected_files:
                if os.path.exists(os.path.join(input_dir, file)):
                    # Key is extracted from the filename, for example out_2A.dat has a key of 2A.
                    md_paths[file[:2]] = os.path.join(input_dir, file)
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


def check_casework(df, output_dir):
    """Make log of rows with "case" to identify casework in future exports (none in collection currently)"""

    # Rows with "case" in any column are saved to a log for review, if any.
    # This may show us another pattern that indicates casework or may be another use of the word case.
    case = np.column_stack([df[col].str.contains('case', case=False, na=False) for col in df])
    if len(df.loc[case.any(axis=1)].index) > 0:
        df.loc[case.any(axis=1)].to_csv(os.path.join(output_dir, 'case_remains_log.csv'), index=False)


def read_metadata(paths):
    """Combine the metadata files into a dataframe"""

    # Read each metadata file in the paths dictionary into a separate dataframe,
    # including supplying the column headings.
    # TODO: confirm these column names
    # TODO: be more flexible about expected extra columns at the end of the export
    df_1b = pd.read_csv(paths['1B'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                        names=['record_type', 'constituent_id', 'address_id', 'address_type', 'primary_flag',
                               'default_address_flag', 'title', 'organization_name', 'address_line_1', 'address_line_2',
                               'address_line_3', 'address_line_4', 'city', 'state', 'zip_code', 'carrier_route',
                               'county', 'country', 'district', 'precinct', 'no_mail_flag', 'agency_code'])
    df_2a = pd.read_csv(paths['2A'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                        names=['record_type', 'constituent_id', 'correspondence_id', 'correspondence_type',
                               'staff', 'date_in', 'date_out', 'tickler_date', 'update_date', 'response_type',
                               'address_id', 'household_flag', 'household_id', 'extra1', 'extra2'])
    df_2b = pd.read_csv(paths['2B'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                        names=['record_type', 'constituent_id', 'correspondence_id', 'correspondence_code', 'position'])
    df_2c = pd.read_csv(paths['2C'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                        names=['record_type', 'constituent_id', 'correspondence_id', '2C_sequence_number',
                               'document_type', 'correspondence_document_name', 'file_location'])

    # Removes unneeded columns from each dataframe, except for ID columns needed for merging.
    # Otherwise, it would be too much data to merge.
    df_1b = remove_pii(df_1b)
    df_2a = remove_pii(df_2a)
    df_2b = remove_pii(df_2b)
    df_2c = remove_pii(df_2c)

    # Combine the dataframes using ID columns.
    # If an id is only in one table, the data is still included and has blanks for columns from the other table.
    # TODO need error handling if the id is blank?
    df = df_1b.merge(df_2a, on='constituent_id', how='outer')
    df = df.merge(df_2b, on='correspondence_id', how='outer')
    df = df.merge(df_2c, on='correspondence_id', how='outer')

    # Remove ID columns only used for merging.
    df = df.drop(['constituent_id_x', 'constituent_id_y', 'constituent_id', 'correspondence_id'],
                 axis=1, errors='ignore')

    # Removes blank rows, which are present in some of the data exports.
    # Blank rows have an empty string in every column.
    df.dropna(how='all', inplace=True)

    return df


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed. Includes names and address information
    # and "extra" columns due to extra blank columns at the end of each row in the export.
    # TODO: confirm this list (extra can have hint at subject but is an unexpected column)
    remove = ['record_type', 'address_id', 'address_type', 'primary_flag', 'default_address_flag', 'title',
              'organization_name', 'address_line_1', 'address_line_2', 'address_line_3', 'address_line_4',
              'carrier_route', 'county', 'district', 'precinct', 'no_mail_flag', 'agency_code', 'household_flag',
              'household_id', 'extra1', 'extra2']

    # Removes every column on the remove list from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    df = df.drop(remove, axis=1, errors='ignore')

    return df


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

    # For access, makes a copy of the data split by congress year.
    # For preservation, makes a log of rows with "case" for detecting casework.
    if script_mode == 'access':
        md_df.to_csv(os.path.join(output_directory, 'Access_Copy.csv'), index=False)
        split_congress_year(md_df, output_directory)
    else:
        check_casework(md_df, output_directory)
