"""
Draft script to prepare preservation and access copies from an export in the CMS Data Interchange Format.
Required arguments: input_directory (path to the folder with the cms export) and script_mode (access or preservation).
"""
import os
import pandas as pd
import sys
from css_data_interchange_format import split_congress_year


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
        expected_files = ['1B.out', '2A.out', '2B.out', '2C.out']
        for file in expected_files:
            if os.path.exists(os.path.join(arg_list[1], file)):
                # Key is extracted from the filename, for example 2A.out has a key of 2A.
                paths_dict[file[:2]] = os.path.join(arg_list[1], file)
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
    df = df[~(df == '').all(axis=1)]

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

    # Gets the paths to the metadata files from the script argument.
    # If the script argument is missing or any are not valid paths, prints the errors and exits the script.
    paths_dictionary, errors_list = get_paths(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Calculates parent folder of the input_directory, which is where script outputs are saved.
    output_directory = os.path.dirname(sys.argv[1])

    # Reads the metadata files, removes columns with PII, and combines into a pandas dataframe.
    md_df = read_metadata(paths_dictionary)

    # Saves the redacted data to a CSV file.
    md_df.to_csv(os.path.join(output_directory, 'Access_Copy.csv'), index=False)

    # Saves a copy of the redacted data to one CSV per Congress Year in the folder with the original metadata files.
    split_congress_year(md_df, output_directory)
