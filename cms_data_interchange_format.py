"""
Script to automate workflows for an export in the CMS Data Interchange Format.
Required arguments: input_directory (path to the folder with the export) and script_mode.

Script modes
accession: produce usability and appraisal reports; export not changed
appraisal: delete letters due to appraisal; metadata not changed
preservation: prepare export for general_aip.py script [TBD]
access: remove metadata rows for appraisal and columns for PII and make copy of metadata split by congress year
"""
import csv
from datetime import date
import os
import pandas as pd
import shutil
import sys
from css_data_interchange_format import remove_appraisal_rows, split_congress_year
from css_archiving_format import file_deletion_log


def appraisal_check_df(df, keyword, category):
    """Returns a df with all rows that contain the specified keyword in any of the columns
    likely to indicate appraisal is needed, with a new column for the appraisal category"""

    # Makes a series for each column with if each row contain the keyword (case-insensitive), excluding blanks.
    doc_name = df['correspondence_document_name'].str.contains(keyword, case=False, na=False)
    text = df['correspondence_text'].str.contains(keyword, case=False, na=False)
    code = df['code_description'].str.contains(keyword, case=False, na=False)

    # Makes a dataframe with all rows containing the keyword in at least one of the columns.
    df_check = df[doc_name | text | code].copy()

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
            expected_files = ['1B.out', '2A.out', '2B.out', '2C.out', '2D.out', '8A.out']
            for file in expected_files:
                if os.path.exists(os.path.join(input_dir, file)):
                    # Key is extracted from the filename, for example 2A.out has a key of 2A.
                    md_paths[file[:2]] = os.path.join(input_dir, file)
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
    doc_df = df.dropna(subset=['correspondence_document_name']).copy()
    doc_df['correspondence_document_name'] = doc_df['correspondence_document_name'].apply(update_path, input_dir=input_dir)
    metadata_paths = doc_df['correspondence_document_name'].tolist()

    # Number of metadata rows without a file path.
    blank_total = df['correspondence_document_name'].isna().sum()

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
    """Return the number of rows that don't meet the expected formatting and save the rows to a csv"""

    # Dictionary of expected formatting patterns for each column.
    patterns = {'correspondence_document_name': r'^attachments|^case-custom|^case-files|^documents|^enewsletters|'
                                                r'^form-attachments|^forms|^in-email|^out-custom',
                'date_in': r'^\d{8}$',
                'date_out': r'^\d{8}$',
                'state': r'^[A-Z][A-Z]$',
                'tickler_date': r'^\d{8}$',
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
    expected = ['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                'code_type', 'code', 'code_description', 'inactive_flag']
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
    cdn_mismatch = check_metadata_formatting('correspondence_document_name', df, output_dir)
    date_in_mismatch = check_metadata_formatting('date_in', df, output_dir)
    date_out_mismatch = check_metadata_formatting('date_out', df, output_dir)
    state_mismatch = check_metadata_formatting('state', df, output_dir)
    tickler_mismatch = check_metadata_formatting('tickler_date', df, output_dir)
    update_mismatch = check_metadata_formatting('update_date', df, output_dir)
    zip_mismatch = check_metadata_formatting('zip_code', df, output_dir)

    # Combines the number of formatting errors for the checked columns into a series, for adding to the report.
    # Other columns have "uncheckable", even if the column is missing from the export.
    formatting = pd.Series(data=['uncheckable', state_mismatch, zip_mismatch, 'uncheckable', 'uncheckable',
                                 'uncheckable', date_in_mismatch, date_out_mismatch, tickler_mismatch,
                                 update_mismatch, 'uncheckable', 'uncheckable', 'uncheckable', 'uncheckable',
                                 'uncheckable', cdn_mismatch, 'uncheckable', 'uncheckable', 'uncheckable',
                                 'uncheckable', 'uncheckable'], index=expected)

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

    # For every row in df_appraisal, deletes any letter in the correspondence_document_name column except form letters.
    # The letter path has to be reformatted to match the actual export, and an error is logged if it is a new pattern.
    # Form letters are retained.
    df_appraisal = df_appraisal.astype(str)
    for row in df_appraisal.itertuples():
        name = row.correspondence_document_name
        if name != '' and name != 'nan' and not name.startswith('form'):
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

    # Column correspondence_text includes one or more keywords that indicate academy applications.
    keywords_list = ['academy appointment', 'academy issue', 'academy nomination', 'military academy']
    corr_text = df['correspondence_text'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_corr_text = df[corr_text]
    df = df[~corr_text]

    # Column code_description includes "academy nomination".
    code_desc = df['code_description'].str.contains('academy nomination', case=False, na=False)
    df_code_desc = df[code_desc]
    df = df[~code_desc]

    # Makes a single dataframe with all rows that indicate academy applications
    # and adds a column for the appraisal category.
    df_academy = pd.concat([df_corr_text, df_code_desc], axis=0, ignore_index=True)
    df_academy['Appraisal_Category'] = 'Academy_Application'

    # Makes a dataframe with rows containing "academy" to check for new patterns indicating academy applications.
    df_academy_check = appraisal_check_df(df, 'academy', 'Academy_Application')

    return df_academy, df_academy_check


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

    # Makes a dataframe with rows containing "case" to check for new patterns indicating casework.
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

    # Makes a dataframe with rows containing "job" to check for new patterns indicating job applications.
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

    # Makes a dataframe with rows containing "recommendation" to check for new patterns indicating recommendations.
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
    df_8a = read_metadata_file('8A', paths['8A'])

    # Removes columns that might identify individual constituents, except columns needed for merging or appraisal.
    # If these were not removed, it would be too much data to merge.
    df_1b = remove_pii(df_1b)
    df_2a = remove_pii(df_2a)
    df_2b = remove_pii(df_2b)
    df_2c = remove_pii(df_2c)
    df_2d = remove_pii(df_2d)
    df_8a = remove_pii(df_8a)

    # Combine the dataframes using ID columns.
    # If an id is only in one table, the data is still included and has blanks for columns from the other table.
    # Must drop constituent_id_x to continue merging to avoid a pandas MergeError from duplicate column names.
    df = df_1b.merge(df_2a, on='constituent_id', how='outer')
    df = df.merge(df_2b, on='correspondence_id', how='outer')
    df = df.merge(df_2c, on='correspondence_id', how='outer')
    df.drop(['constituent_id_x'], axis=1, inplace=True)
    df = df.merge(df_2d, on='correspondence_id', how='outer')
    df = df.merge(df_8a, left_on='correspondence_code', right_on='code', how='outer')

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
                           'correspondence_text'],
                    '8A': ['record_type', 'code_type', 'code', 'code_description', 'inactive_flag']}

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


def sort_correspondence(df, input_dir, output_dir):
    """Sort copy of correspondence into folders by topic"""

    # Makes a dataframe with any row that is incoming correspondence (document is in "in-email")
    # with values (blanks are 'nan') in code_description and correspondence_document_name,
    # and any duplicate combinations of description and document names removed.
    sort_df = df[(df['code_description'] != 'nan') & (df['correspondence_document_name'].str.contains('in-email'))]
    sort_df = sort_df.drop_duplicates(subset=['code_description', 'correspondence_document_name'])

    # For each topic in code_description, makes a folder in the output directory with that topic
    # and copies all documents with that topic into the folder, updating the metadata path to match the directory.
    os.mkdir(os.path.join(output_dir, 'Correspondence_by_Topic'))
    topic_list = sort_df['code_description'].unique()
    for topic in topic_list:
        doc_list = sort_df.loc[sort_df['code_description'] == topic, 'correspondence_document_name'].tolist()
        # Characters that Windows does not permit in a folder name are replaced with an underscore.
        for character in ('\\', '/', ':', '*', '?', '"', '<', '>', '|'):
            topic = topic.replace(character, '_')
        topic_path = os.path.join(output_dir, 'Correspondence_by_Topic', topic)
        os.mkdir(topic_path)
        for doc in doc_list:
            doc_path = update_path(doc, input_dir)
            doc_new_path = os.path.join(topic_path, doc.split('\\')[-1])
            try:
                shutil.copy2(doc_path, doc_new_path)
            except FileNotFoundError:
                # If the expected file is not in the directory, adds the topic and doc path from the metadata to a log.
                with open(os.path.join(output_dir, 'topic_sort_file_not_found.csv'), 'a', newline='') as log:
                    log_writer = csv.writer(log)
                    log_writer.writerow([topic, doc])
        # Deletes the topic folder if it is still empty after checking for all the documents (all FileNotFoundError).
        if not os.listdir(topic_path):
            os.rmdir(topic_path)


def topics_report(df, output_dir):
    """Makes a report with the frequency of each code description, the topic column for this export"""

    # Replace blanks with BLANK so that it is counted as a topic.
    df['code_description'] = df['code_description'].fillna('BLANK')

    # Gets a count for each topic.
    topic_counts = df['code_description'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Topic_Count']

    # Saves to a CSV.
    topic_counts.to_csv(os.path.join(output_dir, 'topics_report.csv'), index=False)


def update_path(md_path, input_dir):
    """Update a path found in the metadata to match the actual directory structure of the exports"""

    # So far, we have seen one way that paths are formatted in the metadata:
    # folder\..\file.ext, where the export is \documents\folder\..\file.ext and folder is one of nine possibilities
    folders = ('attachments', 'case-custom', 'case-files', 'documents', 'enewsletters', 'form-attachments', 'forms',
               'in-email', 'out-custom')
    if md_path.startswith(folders):
        updated_path = os.path.join(input_dir, 'documents', md_path)
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
    md_df.drop(['correspondence_text'], axis=1, inplace=True)

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
        split_congress_year(md_df, output_directory)
