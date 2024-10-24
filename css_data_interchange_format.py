"""
Draft script to prepare access copies from an export in the CSS Data Interchange Format.
Required argument: path to the metadata folder (contains all needed DAT files).
"""
import os
import pandas as pd
import sys
from css_archiving_format import save_df


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
    df_1b = pd.read_csv(paths['1B'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                        names=['record_type', 'person_id', 'address_id', 'address_type', 'primary_flag',
                               'default_address_flag', 'title', 'organization_name', 'address_line_1', 'address_line_2',
                               'address_line_3', 'address_line_4', 'city', 'state_code', 'zip_code', 'carrier_route',
                               'county', 'country', 'district', 'precinct', 'no_mail_flag', 'deliverability'])
    df_2a = pd.read_csv(paths['2A'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                        names=['record_type', 'person_id', 'communication_id', 'workflow_id', 'workflow_person_id',
                               'communication_type', 'user_id', 'approved_by', 'status', 'date_in', 'date_out',
                               'reminder_date', 'update_date', 'response_type', 'address_id', 'email_address',
                               'household_flag', 'household_id', 'group_name', 'salutation'])
    df_2c = pd.read_csv(paths['2C'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                        names=['record_type', 'person_id', 'communication_id', 'document_type',
                               'communication_document_name', 'communication_document_id', 'file_location',
                               'file_name'])

    # Combine the dataframes using ID columns.
    # If an id is only in one table, the data is still included and has blanks for columns from the other table.
    df = df_1b.merge(df_2a, on='person_id', how='outer')
    df = df.merge(df_2c, on='communication_id', how='outer')

    return df


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed. Includes names and address information.
    # As well as identifiers that are no longer needed after combining tables.
    # TODO: confirm this list
    remove = ['record_type_x', 'person_id_x', 'address_id_x', 'address_type', 'primary_flag', 'default_address_flag',
              'title', 'organization_name', 'address_line_1', 'address_line_2', 'address_line_3', 'address_line_4',
              'carrier_route', 'county', 'district', 'precinct', 'no_mail_flag', 'deliverability', 'record_type_y',
              'communication_id', 'workflow_id', 'workflow_person_id', 'user_id', 'address_id_y', 'email_address',
              'household_flag', 'household_id', 'salutation', 'record_type', 'person_id_y', 'communication_document_id']

    # Removes every column on the remove list from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    df = df.drop(remove, axis=1, errors='ignore')

    # Prints the remaining columns for archivist review, in case any additional ones might contain private information.
    # TODO: confirm this is desired
    print("\nColumns remaining after removing personal identifiers are listed below.")
    print("To remove any of these columns, add them to the 'remove' list in remove_pii() and run the script again.")
    for column_name in df.columns.tolist():
        print(f'\t{column_name}')

    return df


if __name__ == '__main__':

    # Gets the paths to the metadata files from the script argument.
    # If the script argument is missing or any are not valid paths, prints the errors and exits the script.
    paths_dictionary, errors_list = get_paths(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Reads the metadata files and combines into a pandas dataframe.
    md_df = read_metadata(paths_dictionary)

    # Removes columns with personally identifiable information, if they are present.
    md_df = remove_pii(md_df)

    # Saves the redacted data to a CSV file in the folder with the original metadata files.

    # Saves a copy of the redacted data to one CSV per Congress Year in the folder with the original metadata files.
