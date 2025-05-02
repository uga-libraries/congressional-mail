"""
Script to automate workflows for an export in the CSS Data Interchange Format.
Required arguments: input_directory (path to the folder with the export) and script_mode.

Script modes
accession: produce usability and appraisal reports; export not changed
appraisal: delete letters due to appraisal; metadata not changed
preservation: prepare export for general_aip.py script [TBD]
access: remove metadata rows for appraisal and columns for PII and make copy of metadata split by congress year
"""
import csv
from datetime import date
from functools import reduce
import os
import pandas as pd
import sys
from css_archiving_format import file_deletion_log


def appraisal_check_df(df, keyword, category):
    """Returns a df with all rows that contain the specified keyword in any of the columns
    likely to indicate appraisal is needed, with a new column for the appraisal category"""

    # Makes a series for each column with if each row contain the keyword (case-insensitive), excluding blanks.
    group_name = df['group_name'].str.contains(keyword, case=False, na=False)
    doc_name = df['communication_document_name'].str.contains(keyword, case=False, na=False)
    file_name = df['file_name'].str.contains(keyword, case=False, na=False)
    text = df['text'].str.contains(keyword, case=False, na=False)

    # Makes a dataframe with all rows containing the keyword in at least one of the columns.
    df_check = df[group_name | doc_name | file_name | text].copy()

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
    if len(arg_list) == 1:
        errors.append("Missing required arguments, input_directory and script_mode")

    # At least the first argument is present.
    # Verifies it is a valid path, and if so that it contains the expected metadata files.
    if len(arg_list) > 1:
        if os.path.exists(arg_list[1]):
            input_dir = arg_list[1]
            expected_files = ['out_1B.dat', 'out_2A.dat', 'out_2C.dat', 'out_2D.dat']
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


def check_letter_matching(df, output_dir, input_dir):
    """Compare the files in the metadata to the files in the export"""

    # Makes a list of paths for the letters in the documents folder within the input directory.
    # This way, the metadata files are not counted as missing.
    input_dir_paths = []
    for root, dirs, files in os.walk(os.path.join(input_dir, 'documents')):
        for file in files:
            file_path = os.path.join(root, file)
            input_dir_paths.append(file_path)

    # Makes a list of paths in the metadata, updating the path to match how the directory is structured in the export.
    doc_df = df.dropna(subset=['communication_document_name']).copy()
    doc_df['communication_document_name'] = doc_df['communication_document_name'].apply(update_path, input_dir=input_dir)
    metadata_paths = doc_df['communication_document_name'].tolist()

    # Number of metadata rows without a file path.
    blank_total = df['communication_document_name'].isna().sum()

    # Compares the list of file paths in the metadata to the export directory.
    metadata_only = list(set(metadata_paths) - set(input_dir_paths))
    directory_only = list(set(input_dir_paths) - set(metadata_paths))
    match = list(set(metadata_paths) & set(input_dir_paths))

    # Saves a summary of the results.
    with open(os.path.join(output_dir, 'usability_report_matching.csv'), 'w', newline='') as report:
        report_writer = csv.writer(report)
        report_writer.writerow(['Category', 'Count'])
        report_writer.writerow(['Metadata_Only', len(metadata_only)])
        report_writer.writerow(['Directory_Only', len(directory_only)])
        report_writer.writerow(['Match', len(match)])
        report_writer.writerow(['Metadata_Blank', blank_total])

    # Saves the paths that did not match to a log.
    with open(os.path.join(output_dir, 'usability_report_matching_details.csv'), 'w', newline='') as report:
        log_writer = csv.writer(report)
        log_writer.writerow(['Category', 'Path'])
        for path in metadata_only:
            log_writer.writerow(['Metadata Only', path])
        for path in directory_only:
            log_writer.writerow(['Directory Only', path])


def check_metadata_formatting(column, df, output_dir):
    """Return the number of rows that don't meet the expected formatting
    and save the rows to a csv"""

    # Dictionary of expected formatting patterns for each column.
    patterns = {'communication_document_name': r'^..\\documents\\',
                'date_in': r'^\d{8}$',
                'date_out': r'^\d{8}$',
                'reminder_date': r'^\d{8}$',
                'state_code': r'^[A-Z][A-Z]$',
                'update_date': r'^\d{8}$',
                'zip_code': r'^\d{5}(-\d{4})?$'}

    # Makes a dataframe with all rows that do not match the expected formatting, excluding blanks.
    # If the column is missing from the dataframe or blank, it returns default text instead of a row count.
    try:
        match = df[column].str.contains(patterns[column], regex=True, na=False)
    except KeyError:
        return 'column_missing'
    except AttributeError:
        return 'column_blank'
    df_no_match = df[~match & df[column].notna()]

    # Saves the dataframe to a csv if there were any that did not match the expected formatting.
    no_match_count = len(df_no_match.index)
    if no_match_count > 0:
        df_no_match.to_csv(os.path.join(output_dir, f'metadata_formatting_errors_{column}.csv'), index=False)

    # Returns the number of rows that do not match the expected formatting, excluding blanks.
    return no_match_count


def check_metadata_usability(df, output_dir):
    """Test the usability of the metadata: columns present, number of blanks, and formatting errors"""

    # Tests if all expected columns are present and if there are any unexpected columns.
    column_names = df.columns.tolist()
    expected = ['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status', 'date_in',
                'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name', 'document_type',
                'communication_document_name', 'communication_document_id', 'file_location', 'file_name']
    columns_dict = dict.fromkeys(expected)
    match = list(set(expected).intersection(column_names))
    for column in match:
        columns_dict[column] = True
    missing = list(set(expected) - set(column_names))
    for column in missing:
        columns_dict[column] = False
    extra = list(set(column_names) - set(expected))
    for column in extra:
        columns_dict[column] = 'Error: unexpected column'
    columns_present = pd.Series(data=columns_dict, index=list(columns_dict.keys()))

    # Calculates the number of blank cells in each column.
    blank_count = df.isna().sum()

    # Calculates the percentage of blank cells in each column.
    total_rows = len(df.index)
    blank_percent = round((blank_count / total_rows) * 100, 2)

    # Calculates the number of cells with formatting errors in each column with predictable formatting
    # and also saves those rows to a csv.
    cdm_mismatch = check_metadata_formatting('communication_document_name', df, output_dir)
    date_in_mismatch = check_metadata_formatting('date_in', df, output_dir)
    date_out_mismatch = check_metadata_formatting('date_out', df, output_dir)
    reminder_mismatch = check_metadata_formatting('reminder_date', df, output_dir)
    state_mismatch = check_metadata_formatting('state_code', df, output_dir)
    update_mismatch = check_metadata_formatting('update_date', df, output_dir)
    zip_mismatch = check_metadata_formatting('zip_code', df, output_dir)

    # Combines the number of formatting errors for the checked columns into a series, for adding to the report.
    # Other columns have "uncheckable", even if the column is missing from the export.
    formatting = pd.Series(data=['uncheckable', state_mismatch, zip_mismatch, 'uncheckable', 'uncheckable',
                                 'uncheckable', 'uncheckable', date_in_mismatch, date_out_mismatch, reminder_mismatch,
                                 update_mismatch, 'uncheckable', 'uncheckable', 'uncheckable', cdm_mismatch,
                                 'uncheckable', 'uncheckable', 'uncheckable'], index=expected)

    # Combines the data about each column into a dataframe and saves as a CSV.
    columns_df = pd.concat([columns_present, blank_count, blank_percent, formatting], axis=1)
    columns_df.columns = ['Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors']
    columns_df.to_csv(os.path.join(output_dir, 'usability_report_metadata.csv'), index=True, index_label='Column_Name')


def delete_appraisal_letters(input_dir, output_dir, df_appraisal):
    """Deletes letters received from constituents and individual letters sent back by the office
    because they are one of the types of letters not retained for appraisal reasons"""

    # Creates a file deletion log, with a header row.
    log_path = os.path.join(output_dir, f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv")
    file_deletion_log(log_path, None, 'header')

    # For every row in df_appraisal, deletes any letter in the communication_document_name column except form letters.
    # The letter path has to be reformatted to match the actual export, and an error is logged if it is a new pattern.
    # Form letters are retained.
    df_appraisal = df_appraisal.astype(str)
    for row in df_appraisal.itertuples():
        name = row.communication_document_name
        if name != '' and name != 'nan' and 'formletters' not in name:
            file_path = update_path(name, input_dir)
            if file_path == 'error_new':
                file_deletion_log(log_path, name, 'Cannot determine file path: new path pattern in metadata')
            else:
                try:
                    file_deletion_log(log_path, file_path, row.Appraisal_Category)
                    os.remove(file_path)
                except FileNotFoundError:
                    file_deletion_log(log_path, file_path, 'Cannot delete: FileNotFoundError')
    

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

    # Makes another dataframe with rows containing "academy" to check for new patterns that could
    # indicate academy applications.
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
    df_appraisal = df_appraisal.groupby([col for col in df_appraisal.columns if col != 'Appraisal_Category'])['Appraisal_Category'].apply(lambda x: '|'.join(map(str, x))).reset_index()
    df_appraisal.to_csv(os.path.join(output_dir, 'appraisal_delete_log.csv'), index=False)

    # Removes the column 'text', which is the only column currently likely to contain PII
    # that is needed for more comprehensive appraisal.
    df_appraisal.drop(['text'], axis=1, inplace=True)
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

    # Makes another dataframe with rows containing "case" to check for new patterns that could indicate casework.
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

    # Makes another dataframe with rows containing "job" to check for new patterns that could indicate job applications.
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

    # Makes another dataframe with rows containing "recommendation" to check for new patterns that could
    # indicate recommendations.
    df_rec_check = appraisal_check_df(df, 'recommendation', 'Recommendation')

    return df_rec, df_rec_check


def form_letter_metadata(input_dir, output_dir):
    """Combine metadata from the tables related to form letters to a single csv"""

    # Read each metadata file into a separate dataframe, including supplying column headings.
    df_6a = form_letter_metadata_read('6A', input_dir)
    df_6b = form_letter_metadata_read('6B', input_dir)
    df_6c = form_letter_metadata_read('6C', input_dir)
    df_6d = form_letter_metadata_read('6D', input_dir)
    df_6f = form_letter_metadata_read('6F', input_dir)

    # Merge all dataframes into a single dataframe, always using the column 'document_id', and saves to CSV.
    # TODO: error handling if a df returns None
    df = reduce(lambda left, right: pd.merge(left, right, on=['document_id'], how='outer'),
                [df_6a, df_6b, df_6c, df_6d, df_6f])
    df.to_csv(os.path.join(output_dir, 'form_letter_metadata.csv'), index=False)


def form_letter_metadata_read(table_id, input_dir):
    """Read a single form letter metadata table into a dataframe or return an error"""

    columns_dict = {'6A': ['record_type', 'document_id', 'version', 'document_grouping_id', 'document_type',
                           'document_display_name', 'document_description', 'document_name', 'created_by',
                           'revised_by', 'approved_by', 'creation_date', 'revision_date', 'last_used_date',
                           'status', 'inactive_flag', 'virtual_directory'],
                    '6B': ['record_type', 'document_id', 'fill-in_field_name', 'label'],
                    '6C': ['record_type', 'document_id', 'code', 'code_type'],
                    '6D': ['record_type', 'document_id', 'document_name', 'user_id', 'attached_date', 'text',
                           'form_letter_attachment_flag', 'file_name'],
                    '6F': ['record_type', 'document_id', 'owned_by']}

    table_path = os.path.join(input_dir, f'out_{table_id}.dat')
    try:
        df = pd.read_csv(table_path, delimiter='\t', dtype=str, on_bad_lines='warn', names=columns_dict[table_id])
    except FileNotFoundError:
        print(f"\n Could not locate file for table {table_id} in {input_dir}")
        return None
    except UnicodeDecodeError:
        print(f"\nUnicodeDecodeError when trying to read the file for table {table_id}.")
        print("The file will be read by ignoring encoding errors, skipping characters that cause an error.\n")
        df = pd.read_csv(table_path, delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                         names=columns_dict[table_id])

    # Remove the record_type column, which every dataframe has, because it isn't helpful
    # and prevents a more efficient way to merge all 5 at once.
    df.drop(['record_type'], axis=1, inplace=True)

    return df


def read_metadata(paths):
    """Combine the metadata files into a dataframe"""

    # Read each metadata file in the paths dictionary into a separate dataframe,
    # including supplying the column headings.
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
    columns_2d = ['record_type', 'person_id', 'communication_id', '2d_sequence_number',
                  'text', 'date', 'time', 'user_id']

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

    try:
        df_2d = pd.read_csv(paths['2D'], delimiter='\t', dtype=str, on_bad_lines='warn', names=columns_2d)
    except UnicodeDecodeError:
        print("\nUnicodeDecodeError when trying to read the metadata file 2D.")
        print("The file will be read by ignoring encoding errors, skipping characters that cause an error.\n")
        df_2d = pd.read_csv(paths['2D'], delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn',
                            names=columns_2d)

    # Removes unneeded columns from each dataframe, except for ID columns needed for merging.
    # Otherwise, it would be too much data to merge.
    df_1b = remove_pii(df_1b)
    df_2a = remove_pii(df_2a)
    df_2c = remove_pii(df_2c)

    # Only using 2d for appraisal because of the free text field.
    # Drop the rest of the columns now and text after appraisal rows are identified.
    # Some columns overlap with columns kept in other tables, so not using remove_pii().
    df_2d = df_2d.drop(['record_type', 'person_id', '2d_sequence_number', 'date', 'time', 'user_id'],
                       axis=1, errors='ignore')

    # Combine the dataframes using ID columns.
    # If an id is only in one table, the data is still included and has blanks for columns from the other table.
    # TODO need error handling if the id is blank?
    df = df_1b.merge(df_2a, on='person_id', how='outer')
    df = df.merge(df_2c, on='communication_id', how='outer')
    df = df.merge(df_2d, on='communication_id', how='outer')

    # Remove ID columns only used for merging.
    df = df.drop(['person_id_x', 'person_id_y', 'communication_id'], axis=1, errors='ignore')

    # Removes blank rows, which are present in some of the data exports.
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


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names to remove because they include constituent names or addresses.
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
    # Column date_ is formatted YYYYMMDD.
    df.loc[:, 'year'] = df['date_in'].astype(str).str[:4].astype(int)

    # Adds a column with the Congress Year received, which is a two-year range starting with an odd year.
    # First, if the year received is even, the Congress Year is year-1 to year.
    # Second, if the year received is odd, the Congress Year is year to year+1.
    df.loc[df['year'] % 2 == 0, 'congress_year'] = (df['year'] - 1).astype(str) + '-' + df['year'].astype(str)
    df.loc[df['year'] % 2 == 1, 'congress_year'] = df['year'].astype(str) + '-' + (df['year'] + 1).astype(str)

    # Splits the rows with date information by Congress Year received and saves each group to a separate CSV.
    # The year and congress_year columns are first removed, so the CSV only has the original columns.
    for congress_year, cy_df in df.groupby('congress_year'):
        cy_df = cy_df.drop(['year', 'congress_year'], axis=1)
        cy_df.to_csv(os.path.join(cy_dir, f'{congress_year}.csv'), index=False)


def topics_report(df, output_dir):
    """Makes a report with the frequency of each group name, the only topic information we've seen in exports so far"""

    # Replace blanks with BLANK so that it is counted as a topic.
    df['group_name'] = df['group_name'].fillna('BLANK')

    # Gets a count for each topic.
    topic_counts = df['group_name'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Topic_Count']

    # Saves to a CSV.
    topic_counts.to_csv(os.path.join(output_dir, 'topics_report.csv'), index=False)


def update_path(md_path, input_dir):
    """Update a path found in the metadata to match the actual directory structure of the exports"""

    # So far, we have seen one way that paths are formatted in the metadata:
    # ..\documents\folder\..\file.ext, where the export is \documents\folder\..\file.ext
    if md_path.startswith('..\\documents'):
        updated_path = md_path.replace('..', input_dir)
    else:
        updated_path = 'error_new'

    return updated_path


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

    # Makes a dataframe and a csv of metadata rows that indicate appraisal.
    # This is used in most of the modes.
    appraisal_df = find_appraisal_rows(md_df, output_directory)

    # Removes the column 'text', now that identifying rows for appraisal is complete,
    # which is the only column currently likely to contain PII that is needed for more comprehensive appraisal.
    md_df.drop(['text'], axis=1, inplace=True)

    # The rest of the script is dependent on the mode.

    # For accession, generates reports about the usability of the export and what will be deleted for appraisal.
    # The export is not changed in this mode.
    if script_mode == 'accession':
        print("\nThe script is running in accession mode.")
        print("It will produce usability and appraisal reports and not change the export.")
        check_metadata_usability(md_df, output_directory)
        check_letter_matching(md_df, output_directory, input_directory)
        topics_report(md_df, output_directory)

    # For appraisal, deletes letters due to appraisal. The metadata file is not changed in this mode.
    elif script_mode == 'appraisal':
        print("\nThe script is running in appraisal mode.")
        print("It will delete letters due to appraisal but not change the metadata file.")
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

    # TODO For preservation, prepares the export for the general_aip.py script.
    elif script_mode == 'preservation':
        print("\nThe script is running in preservation mode.")
        print("The steps are TBD.")

    # For access, makes a copy of the metadata with tables merged and rows for appraisal and columns for PII removed
    # and makes a copy of the data split by congress year.
    elif script_mode == 'access':
        print("\nThe script is running in access mode.")
        print("It will remove rows for deleted letters, save the merged metadata tables without columns with PII,"
              " and make copies of the metadata split by congress year")
        md_df = remove_appraisal_rows(md_df, appraisal_df)
        md_df.to_csv(os.path.join(output_directory, 'archiving_correspondence_redacted.csv'), index=False)
        form_letter_metadata(input_directory, output_directory)
        split_congress_year(md_df, output_directory)

