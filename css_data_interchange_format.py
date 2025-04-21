"""
Draft script to prepare preservation and access copies from an export in the CSS Data Interchange Format.
Required arguments: input_directory (path to the folder with the css export) and script_mode.

Script modes
accession: produce usability and appraisal reports; export not changed
appraisal: delete letters due to appraisal; metadata not changed
preservation: prepare export for general_aip.py script [TBD]
access: remove metadata rows for appraisal and columns for PII and make copy of metadata split by congress year
"""
from datetime import date
import os
import pandas as pd
import sys
from css_archiving_format import file_deletion_log


def appraisal_check_df(df, keyword, category):
    """Returns a df with all rows that contain the specified keyword in any of three columns
    likely to indicate appraisal is needed, including a category label"""

    # Makes a series for each column with if each row contain the keyword (case-insensitive), excluding blanks.
    group_name = df['group_name'].str.contains(keyword, case=False, na=False)
    doc_name = df['communication_document_name'].str.contains(keyword, case=False, na=False)
    file_name = df['file_name'].str.contains(keyword, case=False, na=False)

    # Makes a dataframe with all rows containing the keyword in at least one of the columns.
    df_check = df[group_name | doc_name | file_name].copy()

    # Adds a column with the category.
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

    # At least the first argument is present.
    # Verifies it is a valid path, and if so that it contains the expected metadata files.
    if len(arg_list) > 1:
        if os.path.exists(arg_list[1]):
            input_dir = arg_list[1]
            expected_files = ['out_1B.dat', 'out_2A.dat', 'out_2C.dat']
            for file in expected_files:
                if os.path.exists(os.path.join(input_dir, file)):
                    # Key is extracted from the filename, for example out_2A.dat has a key of 2A.
                    md_paths[file[4:6]] = os.path.join(input_dir, file)
                else:
                    errors.append(f'No {file} file in the input_directory')
        else:
            errors.append(f"Provided input_directory '{arg_list[1]}' does not exist")

    # Only one required argument is present.
    if len(arg_list) == 2:
        errors.append("Missing one of the required arguments, input_directory or script_mode")

    # Both required arguments are present.
    # Verifies the second is one of the expected modes.
    if len(arg_list) > 2:
        if arg_list[2] in ('accession', 'appraisal', 'preservation', 'access'):
            mode = arg_list[2]
        else:
            errors.append(f"Provided mode '{arg_list[2]}' is not one of the expected modes")

    # More than the expected two required arguments are present.
    if len(arg_list) > 3:
        errors.append("Provided more than the required arguments, input_directory and script_mode")

    return input_dir, md_paths, mode, errors


def find_academy_rows(df):
    """Find metadata rows with topics or text that indicate they are academy applications and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column group_name includes "academy".
    group = df['group_name'].str.contains('academy', case=False, na=False)
    df_group = df[group]
    df = df[~group]

    # Column communication_document_name includes "academy".
    doc_name = df['communication_document_name'].str.contains('academy', case=False, na=False)
    df_doc_name = df[doc_name]
    df = df[~doc_name]

    # Makes a single dataframe with all rows that indicate academy applications
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_academy = pd.concat([df_group, df_doc_name], axis=0, ignore_index=True)
    df_academy['Appraisal_Category'] = 'Academy_Application'

    # Makes another dataframe with rows to check for new patterns that could indicate academy applications.
    df_academy_check = appraisal_check_df(df, 'academy', 'Academy_Application')

    return df_academy, df_academy_check


def find_appraisal_rows(df, output_dir):
    """Find metadata rows with topics or text that indicate they are different categories for appraisal,
     return as a df and log results"""

    # Call the functions for each appraisal category.
    df_academy, df_academy_check = find_academy_rows(df)
    df_casework, df_casework_check = find_casework_rows(df)
    df_job, df_job_check = find_job_rows(df)
    df_recommendation, df_recommendation_check = find_recommendation_rows(df)

    # Makes a log with rows to check to refine appraisal decisions. These were not marked for appraisal
    # but have a simple keyword (e.g., case) that could be a new indicators for appraisal.
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
    return df_appraisal


def find_casework_rows(df):
    """Find metadata rows with topics or text that indicate they are casework and return as a df
     Once a row matches one pattern, it is not considered for other patterns."""

    # Column group_name starts with "case", if any.
    group = df['group_name'].str.lower().str.startswith('case', na=False)
    df_group = df[group]
    df = df[~group]

    # Column communication_document_name includes one or more keywords that indicate casework.
    keywords_list = ['casework', 'initialssacase', 'open sixth district cases']
    doc_name = df['communication_document_name'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_doc_name = df[doc_name]
    df = df[~doc_name]

    # Makes a single dataframe with all rows that indicate casework
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_casework = pd.concat([df_group, df_doc_name], axis=0, ignore_index=True)
    df_casework['Appraisal_Category'] = 'Casework'

    # Makes another dataframe with rows to check for new patterns that could indicate casework.
    df_casework_check = appraisal_check_df(df, 'case', 'Casework')

    return df_casework, df_casework_check


def find_job_rows(df):
    """Find metadata rows with topics or text that indicate they are job applications and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column group_name includes one or more of the groups that indicate job applications.
    group_list = ['jobapp', 'job request', 'resume']
    group = df['group_name'].str.contains('|'.join(group_list), case=False, na=False)
    df_group = df[group]
    df = df[~group]

    # Column communication_document_name includes one or more keywords that indicate job applications.
    keywords_list = ['job.doc', 'jobapp', 'job applicant', 'reply to resume', 'thank you for resume']
    doc_name = df['communication_document_name'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_doc_name = df[doc_name]
    df = df[~doc_name]

    # Makes a single dataframe with all rows that indicate job applications
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_job = pd.concat([df_group, df_doc_name], axis=0, ignore_index=True)
    df_job['Appraisal_Category'] = 'Job_Application'

    # Makes another dataframe with rows to check for new patterns that could indicate job applications.
    df_job_check = appraisal_check_df(df, 'job', 'Job_Application')

    return df_job, df_job_check


def find_recommendation_rows(df):
    """Find metadata rows with topics or text that indicate they are recommendations and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column communication_document_name includes one or more keywords that indicate recommendations.
    keywords_list = ['intern rec', 'page rec']
    doc_name = df['communication_document_name'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_rec = df[doc_name].copy()
    df = df[~doc_name]

    # Adds a column for the appraisal category (needed for the file deletion log).
    df_rec['Appraisal_Category'] = 'Recommendation'

    # Makes another dataframe with rows to check for new patterns that could indicate recommendations.
    df_rec_check = appraisal_check_df(df, 'recommendation', 'Recommendation')

    return df_rec, df_rec_check


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


def remove_appraisal_rows(df, df_appraisal):
    """Remove metadata rows for letters deleted during appraisal and return the updated df"""

    # Makes sure all columns in both dataframes are strings,
    # since earlier steps can alter the type and the types must be the same for two rows to match.
    df = df.astype(str)
    df_appraisal.astype(str)

    # Makes an updated dataframe with just rows in df that are not in df_appraisal.
    df_merge = df.merge(df_appraisal, how='left', indicator=True)
    df_update = df_merge[df_merge['_merge'] == 'left_only'].drop(columns=['_merge', 'Appraisal_Category'])

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

    # Makes a folder for all the CSVs.
    cy_dir = os.path.join(output_dir, 'archiving_correspondence_by_congress_year')
    os.mkdir(cy_dir)

    # Saves rows without a year (date is a not a number, could be blank or text) to a CSV, if any.
    df_undated = df[pd.to_numeric(df['date_in'], errors='coerce').isnull()]
    if len(df_undated.index) > 0:
        df_undated.to_csv(os.path.join(cy_dir, 'undated.csv'), index=False)

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

    # Splits the data with date information by Congress Year received and saves each to a separate CSV.
    # The year and congress_year columns are first removed, so the CSV only has the original columns.
    for congress_year, cy_df in df.groupby('congress_year'):
        cy_df = cy_df.drop(['year', 'congress_year'], axis=1)
        cy_df.to_csv(os.path.join(cy_dir, f'{congress_year}_update.csv'), index=False)


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

    # Makes a dataframe and a csv of metadata rows that indicate appraisal.
    # This is used in most of the modes.
    appraisal_df = find_appraisal_rows(md_df, output_directory)

    # The rest of the script is dependent on the mode.

    # TODO For preservation, prepares the export for the general_aip.py script.
    # Run in appraisal mode first to remove letters.
    if script_mode == 'preservation':
        print("\nThe script is running in preservation mode.")
        print("The steps are TBD.")

    # For access, makes a copy of the metadata with tables merged and rows for casework and columns for PII removed
    # and makes a copy of the data split by congress year.
    elif script_mode == 'access':
        print("\nThe script is running in access mode.")
        print("It will remove rows for deleted letters and columns with PII from the merged metadata tables,"
              " and make copies of the metadata split by congress year")
        md_df = remove_appraisal_rows(md_df, appraisal_df)
        md_df.to_csv(os.path.join(output_directory, 'archiving_correspondence_redacted.csv'), index=False)
        split_congress_year(md_df, output_directory)

