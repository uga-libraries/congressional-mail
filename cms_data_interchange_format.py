"""
Draft script to prepare preservation and access copies from an export in the CMS Data Interchange Format.
Required arguments: input_directory (path to the folder with the cms export) and script_mode (access or preservation).
"""
import numpy as np
import os
import pandas as pd
import sys
from css_data_interchange_format import split_congress_year


def appraisal_check_df(df, keyword, category):
    """Returns a df with all rows that contain the specified keyword in any of the columns
    likely to indicate appraisal is needed, with a new column for the appraisal category"""

    # Makes a series for each column with if each row contain the keyword (case-insensitive), excluding blanks.
    doc_name = df['correspondence_document_name'].str.contains(keyword, case=False, na=False)
    text = df['correspondence_text'].str.contains(keyword, case=False, na=False)

    # Makes a dataframe with all rows containing the keyword in at least one of the columns.
    df_check = df[doc_name | text].copy()

    # Adds a column with the appraisal category.
    df_check['Appraisal_Category'] = category

    return df_check


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
            expected_files = ['1B.out', '2A.out', '2B.out', '2C.out', '2D.out']
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


def find_academy_rows(df):
    """Find metadata rows with topics or text that indicate they are academy applications and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column correspondence_text includes one or more keywords that indicate academy applications.
    keywords_list = ['academy appointment', 'academy issue', 'academy nomination', 'military academy']
    corr_text = df['correspondence_text'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_corr_text = df[corr_text].copy()
    df = df[~corr_text]

    # Adds a column for the appraisal category.
    df_corr_text['Appraisal_Category'] = 'Academy_Application'

    # Makes another dataframe with rows containing "academy" to check for new patterns indicating academy applications.
    df_academy_check = appraisal_check_df(df, 'academy', 'Academy_Application')

    return df_corr_text, df_academy_check


def find_appraisal_rows(df, output_dir):
    """Find metadata rows for all the categories for appraisal, return df and log results"""

    # Calls the functions for each appraisal category.
    df_academy, df_academy_check = find_academy_rows(df)
    df_casework, df_casework_check = find_casework_rows(df)
    df_job, df_job_check = find_job_rows(df)
    df_recommendation, df_recommendation_check = find_recommendation_rows(df)

    # Makes a log with rows to check to refine appraisal decisions. These were not marked for appraisal
    # but have a simple keyword (e.g., case) that could be new indicators for appraisal.
    # Rows that fit more than one appraisal category are repeated.
    df_check = pd.concat([df_academy_check, df_casework_check, df_job_check, df_recommendation_check],
                         axis=0, ignore_index=True)
    df_check.to_csv(os.path.join(output_dir, 'appraisal_check_log.csv'), index=False)

    # Makes a single dataframe with all rows that indicate appraisal
    # and also saves to a log for review for any that are not correct identifications.
    # Rows that fit more than one appraisal category are combined.
    df_appraisal = pd.concat([df_academy, df_casework, df_job, df_recommendation], axis=0, ignore_index=True)
    df_appraisal = df_appraisal.astype(str)
    df_appraisal = df_appraisal.groupby([col for col in df_appraisal.columns if col != 'Appraisal_Category'])[
        'Appraisal_Category'].apply(lambda x: '|'.join(map(str, x))).reset_index()
    df_appraisal.to_csv(os.path.join(output_dir, 'appraisal_delete_log.csv'), index=False)

    # Removes the column 'correspondence_text', which is the only column currently likely to contain PII
    # that is needed for more comprehensive appraisal.
    df_appraisal.drop(['correspondence_text'], axis=1, inplace=True)
    return df_appraisal


def find_casework_rows(df):
    """Find metadata rows with topics or text that indicate they are casework and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column correspondence_text includes one or more keywords that indicate casework.
    keywords_list = ['case file', 'case has', 'case open', 'casework', 'forwarded to me', 'open case']
    corr_text = df['correspondence_text'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_corr_text = df[corr_text].copy()
    df = df[~corr_text]

    # Adds a column for the appraisal category.
    df_corr_text['Appraisal_Category'] = 'Casework'

    # Makes another dataframe with rows containing "academy" to check for new patterns indicating academy applications.
    df_casework_check = appraisal_check_df(df, 'case', 'Casework')

    return df_corr_text, df_casework_check


def find_job_rows(df):
    """Find metadata rows with topics or text that indicate they are job applications and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column correspondence_text includes one or more keywords that indicate job applications.
    keywords_list = ['intern assignment', 'intern response', 'internship']
    corr_text = df['correspondence_text'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_corr_text = df[corr_text].copy()
    df = df[~corr_text]

    # Adds a column for the appraisal category.
    df_corr_text['Appraisal_Category'] = 'Job_Application'

    # Makes another dataframe with rows containing "academy" to check for new patterns indicating academy applications.
    df_job_check = appraisal_check_df(df, 'job', 'Job_Application')

    return df_corr_text, df_job_check


def find_recommendation_rows(df):
    """Find metadata rows with topics or text that indicate they are recommendations and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column correspondence_text includes one or more keywords that indicate recommendations.
    keywords_list = ['generic recommendation', 'letter of recommendation', 'letters of recommendation',
                     'recommendation letter']
    corr_text = df['correspondence_text'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_corr_text = df[corr_text].copy()
    df = df[~corr_text]

    # Adds a column for the appraisal category.
    df_corr_text['Appraisal_Category'] = 'Recommendation'

    # Makes another dataframe with rows containing "academy" to check for new patterns indicating academy applications.
    df_recommendation_check = appraisal_check_df(df, 'recommendation', 'Recommendation')

    return df_corr_text, df_recommendation_check


def read_metadata(paths):
    """Combine the metadata files into a dataframe"""

    # Reads each metadata file into a separate dataframe.
    df_1b = read_metadata_file('1B', paths['1B'])
    df_2a = read_metadata_file('2A', paths['2A'])
    df_2b = read_metadata_file('2B', paths['2B'])
    df_2c = read_metadata_file('2C', paths['2C'])
    df_2d = read_metadata_file('2D', paths['2D'])

    # Removes columns that might identify individual constituents, except columns needed for merging or appraisal.
    # If these were not removed, it would be too much data to merge.
    df_1b = remove_pii(df_1b)
    df_2a = remove_pii(df_2a)
    df_2b = remove_pii(df_2b)
    df_2c = remove_pii(df_2c)
    df_2d = remove_pii(df_2d)

    # Combine the dataframes using ID columns.
    # If an id is only in one table, the data is still included and has blanks for columns from the other table.
    # Must drop constituent_id_x before the final merge to avoid a pandas MergeError from duplicate column names.
    # TODO need error handling if the id is blank?
    df = df_1b.merge(df_2a, on='constituent_id', how='outer')
    df = df.merge(df_2b, on='correspondence_id', how='outer')
    df = df.merge(df_2c, on='correspondence_id', how='outer')
    df.drop(['constituent_id_x'], axis=1, inplace=True)
    df = df.merge(df_2d, on='correspondence_id', how='outer')

    # Remove ID columns only used for merging.
    # Columns needed for appraisal are retained until after metadata rows for appraisal are identified.
    df.drop(['constituent_id_x', 'constituent_id_y', 'constituent_id', 'correspondence_id'],
            axis=1, errors='ignore', inplace=True)

    # Removes blank rows, which are present in some of the data exports.
    # Blank rows have an empty string in every column.
    df.dropna(how='all', inplace=True)

    return df


def read_metadata_file(file_id, file_path):
    """Read a single metadata file into a dataframe, adding column names"""

    # Dictionary of column names for each file.
    columns_dict = {'1B': ['record_type', 'constituent_id', 'address_id', 'address_type', 'primary_flag',
                           'default_address_flag', 'title', 'organization_name', 'address_line_1', 'address_line_2',
                           'address_line_3', 'address_line_4', 'city', 'state', 'zip_code', 'carrier_route',
                           'county', 'country', 'district', 'precinct', 'no_mail_flag', 'agency_code'],
                    '2A': ['record_type', 'constituent_id', 'correspondence_id', 'correspondence_type', 'staff',
                           'date_in', 'date_out', 'tickler_date', 'update_date', 'response_type', 'address_id',
                           'household_flag', 'household_id', 'extra1', 'extra2'],
                    '2B': ['record_type', 'constituent_id', 'correspondence_id', 'correspondence_code', 'position'],
                    '2C': ['record_type', 'constituent_id', 'correspondence_id', '2C_sequence_number',
                           'document_type', 'correspondence_document_name', 'file_location'],
                    '2D': ['record_type', 'constituent_id', 'correspondence_id', '2D_sequence_number', 'text_type',
                           'correspondence_text']}

    # Read into dataframe, with a warning if characters have to be skipped.
    try:
        df = pd.read_csv(file_path, delimiter='\t', dtype=str, on_bad_lines='warn', names=columns_dict[file_id])
    except UnicodeDecodeError:
        print(f"\nUnicodeDecodeError when trying to read the metadata file {file_id}.")
        print("The file will be read by ignoring encoding errors, skipping characters that cause an error.\n")
        df = pd.read_csv(file_path, delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                         names=columns_dict[file_id])

    return df


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed. Includes names and address information
    # and "extra" columns due to extra blank columns at the end of each row in the export.
    # TODO: confirm this list (extra can have hint at subject but is an unexpected column)
    remove = ['record_type', 'address_id', 'address_type', 'primary_flag', 'default_address_flag', 'title',
              'organization_name', 'address_line_1', 'address_line_2', 'address_line_3', 'address_line_4',
              'carrier_route', 'county', 'district', 'precinct', 'no_mail_flag', 'agency_code', 'household_flag',
              'household_id', 'extra1', 'extra2', '2D_sequence_number', 'text_type']

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
    # Columns with PII must be removed now to save memory, given the size of the data.
    md_df = read_metadata(metadata_paths_dict)

    # For access, makes a copy of the metadata with tables merged and PII removed and
    # makes a copy of the data split by congress year.
    if script_mode == 'access':
        md_df.to_csv(os.path.join(output_directory, 'Access_Copy.csv'), index=False)
        split_congress_year(md_df, output_directory)
