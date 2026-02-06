"""
Script to automate workflows for an export in the CMS Data Interchange Format.
Required arguments: input_directory (path to the folder with the export) and script_mode.

Script modes
accession: produce usability and appraisal reports; export not changed
appraisal: delete letters due to appraisal and make report of possible restrictions; metadata not changed
access: remove metadata rows for appraisal and restrictions and columns for PII,
        make copy of metadata split by calendar year,
        and make a copy of incoming and outgoing correspondence in folders by topic

For appraisal and access, appraisal_delete_log.csv (made by accession mode) must be in the output directory.
For access mode, review_restrictions.csv (made by appraisal mode) must be in the output directory.
This allows the archivist to review and edit these documents without needing to update the script.
"""
import csv
from datetime import date
import os
import pandas as pd
import shutil
import sys
import css_data_interchange_format as css_dif
from css_archiving_format import file_deletion_log, read_csv, remove_appraisal_rows


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
    """Compare the files in the metadata to the files in the export,
    reformatting the metadata paths and making all characters lowercase, so they can match"""

    # Makes a list of paths for the letters in the documents folder within the input directory.
    # This way, the metadata files are not counted as missing.
    input_dir_paths = []
    for root, dirs, files in os.walk(os.path.join(input_dir, 'documents')):
        for file in files:
            file_path = os.path.join(root, file)
            file_path = file_path.lower()
            input_dir_paths.append(file_path)

    # Makes a list of paths in the metadata, updating the path to match how the directory is structured in the export.
    doc_df = df.dropna(subset=['correspondence_document_name']).copy()
    doc_df['correspondence_document_name'] = doc_df['correspondence_document_name'].apply(update_path, input_dir=input_dir)
    doc_df['correspondence_document_name'] = doc_df['correspondence_document_name'].str.lower()
    metadata_paths = doc_df['correspondence_document_name'].tolist()

    # Number of metadata rows without a file path.
    blank_total = df['correspondence_document_name'].isna().sum()

    # Compares the list of file paths in the metadata to the export directory.
    metadata_only = list(set(metadata_paths) - set(input_dir_paths))
    directory_only = list(set(input_dir_paths) - set(metadata_paths))
    match = list(set(metadata_paths) & set(input_dir_paths))

    # Saves a summary of the results.
    metadata_total = len(metadata_only) + len(match) + blank_total
    with open(os.path.join(output_dir, 'usability_report_matching.csv'), 'w', newline='') as report:
        report_writer = csv.writer(report)
        report_writer.writerow(['Category', 'Row/File_Count', 'Row_Percent'])
        report_writer.writerow(['Match', len(match), f'{int(round(len(match) / metadata_total * 100, 0))}%'])
        report_writer.writerow(['Metadata_Only', len(metadata_only), f'{int(round(len(metadata_only) / metadata_total * 100, 0))}%'])
        report_writer.writerow(['Metadata_Blank', blank_total, f'{int(round(blank_total / metadata_total * 100, 0))}%']),
        report_writer.writerow(['Directory_Only', len(directory_only), 'n/a'])

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


def df_search(df, keywords, category):
    """Returns a df with all rows that contain any of the keywords indicating this category of appraisal"""

    # Columns to search, which are the ones that reasonably might indicate appraisal.
    columns_list = ['correspondence_document_name', 'correspondence_text', 'code_description']

    # Makes a dataframe with any row containing one of the keywords in at lease one of the columns searched.
    # Keyword matches are case-insensitive and will not match blanks.
    match = df[columns_list].astype(str).agg(' '.join, axis=1).str.contains(keywords, case=False, na=False)
    df_match = df[match].copy()

    # Adds a column with the appraisal category.
    df_match['Appraisal_Category'] = category

    # Makes a second df without the matches.
    # This is used to skip matched rows when doing additional searches, like for the check_df.
    df_no_match = df[~match].copy()

    return df_match, df_no_match


def df_search_exact(df, keywords_list, category):
    """Returns a df with all rows that exactly match any of the keywords indicating this category of appraisal"""

    # Columns to search, which are the ones that reasonably might indicate appraisal.
    columns_list = ['correspondence_document_name', 'correspondence_text', 'code_description']

    # Makes a dataframe with any row that only contains one of the keywords, including matching case,
    # in at least one of the columns searched.
    match = df[columns_list].isin(keywords_list).any(axis=1)
    df_match = df[match].copy()

    # Adds a column with the appraisal category.
    df_match['Appraisal_Category'] = category

    # Makes a second df without the matches.
    # This is used to skip matched rows when doing additional searches, like for the check_df.
    df_no_match = df[~match].copy()

    return df_match, df_no_match


def find_academy_rows(df):
    """Find metadata rows with keywords that indicate they might be academy applications
    and return as two dfs, one with more certainty (df_academy) and one with less (df_academy_check)"""

    # Makes df with more certainty.
    df_academy, df_unmatched = df_search(df, 'academy', 'Academy_Application')

    # Makes df with less certainty, only searching rows that are not in df_academy, to find for new patterns.
    # TODO update term now that df_academy is simplified to searching for just academy.
    df_academy_check, df_unmatched = df_search(df_unmatched, 'academy', 'Academy_Application')

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
    """Find metadata rows with keywords that indicate they might be casework
    and return as a two dfs, one with more certain (df_casework) and one with less (df_casework_check)"""

    # Column code_description includes one or more keywords that indicate casework.
    keywords_list = ['case file', 'case has', 'case open', 'casework', 'case work', 'forwarded to me', 'open case']
    code_desc = df['code_description'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_code_desc = df[code_desc].copy()
    df = df[~code_desc]

    # Column correspondence_document_name includes one or more keywords that indicate casework.
    corr_doc = df['correspondence_document_name'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_corr_doc = df[corr_doc].copy()
    df = df[~corr_doc]

    # Column correspondence_text includes one or more keywords that indicate casework.
    corr_text = df['correspondence_text'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_corr_text = df[corr_text].copy()
    df = df[~corr_text]

    # Makes a single dataframe with all rows that indicate casework and adds a column for the appraisal category.
    df_casework = pd.concat([df_code_desc, df_corr_doc, df_corr_text], axis=0, ignore_index=True)
    df_casework['Appraisal_Category'] = 'Casework'

    # Makes a dataframe with rows containing "case" to check for new patterns indicating casework.
    df_casework_check = appraisal_check_df(df, 'case', 'Casework')

    return df_casework, df_casework_check


def find_job_rows(df):
    """Find metadata rows with keywords that indicate they might be job applications
    and return as a two dfs, one with more certain (df_job) and one with less (df_job_check)"""

    # Makes df with more certainty.
    keyword_string = 'intern |internship|interview|job app|job request|job.doc|jobapp|resume'
    df_job, df_unmatched = df_search(df, keyword_string, 'Job_Application')
    # Makes df with less certainty, only searching rows that are not in df_job, to look for new keywords.
    df_job_check, df_unmatched = df_search(df_unmatched, 'job', 'Job_Application')

    return df_job, df_job_check


def find_recommendation_rows(df):
    """Find metadata rows with keywords that indicate they might be recommendations
    and return as two dfs, one with more certainty (df_recommendation) and one with less (df_recommendation_check)"""

    # Makes df with more certainty.
    keyword_string = 'intern rec|page rec|rec for|recommendation'
    df_rec, df_unmatched = df_search(df, keyword_string, 'Recommendation')

    # Makes df with less certainty, only searching rows that are not in df_recommendation, to look for new keywords.
    # TODO update term now that df_recommendation is searching for recommendation.
    df_rec_check, df_unmatched = df_search(df_unmatched, 'recommendation', 'Recommendation')

    return df_rec, df_rec_check


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

    # Combine the dataframes using ID columns. If the ID is not in 2A (which describes each letter)
    # it is not included in the merged dataframe, to reduce the number of very incomplete rows.
    # Must drop constituent_id_x to continue merging to avoid a pandas MergeError from duplicate column names.
    df = df_2a.merge(df_1b, on='constituent_id', how='left')
    df = df.merge(df_2b, on='correspondence_id', how='left')
    df = df.merge(df_2c, on='correspondence_id', how='left')
    df.drop(['constituent_id_x'], axis=1, inplace=True)
    df = df.merge(df_2d, on='correspondence_id', how='left')
    df = df.merge(df_8a, left_on='correspondence_code', right_on='code', how='left')

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


def restriction_report(df, output_dir):
    """Make report of any row with a topic that require restriction if they are about individuals' situations"""

    # List of topics (adjust based on topics_report.csv from accession mode of this script)
    restrict_list = ['citizen', 'citizenship', 'court', 'crime', 'criminal justice',
                     'immigrant', 'immigration', 'migrant', 'refugee']

    # Save the subset of the df where the topic matches any term in the restrict list to the output directory.
    # No report is made if no topics are present.
    report_df = df[df['code_description'].isin(restrict_list)]
    if len(report_df.index) > 0:
        report_df.to_csv(os.path.join(output_dir, 'restriction_review.csv'), index=False)


def topics_sort(df, input_dir, output_dir):
    """Sort copy of incoming and outgoing correspondence into folders by topic"""
    os.mkdir(os.path.join(output_dir, 'Correspondence_by_Topic'))

    # Sorts a copy of correspondence from constituents ("in" letters) by topic.
    in_df = topics_sort_df(df, 'in-email')
    topic_list = in_df['code_description'].unique()
    for topic in topic_list:
        doc_list = in_df.loc[in_df['code_description'] == topic, 'correspondence_document_name'].tolist()
        topic_path = css_dif.topics_sort_folder(topic, output_dir, 'from_constituents')
        for doc in doc_list:
            topics_sort_copy(doc, input_dir, output_dir, topic_path)
        css_dif.topics_sort_delete_empty(topic_path)

    # Sorts a copy of correspondence to constituents ("out" letters) by topic.
    out_df = topics_sort_df(df, 'out-custom')
    topic_list = out_df['code_description'].unique()
    for topic in topic_list:
        doc_list = out_df.loc[out_df['code_description'] == topic, 'correspondence_document_name'].tolist()
        topic_path = css_dif.topics_sort_folder(topic, output_dir, 'to_constituents')
        for doc in doc_list:
            topics_sort_copy(doc, input_dir, output_dir, topic_path)
        css_dif.topics_sort_delete_empty(topic_path)


def topics_sort_copy(doc, input_dir, output_dir, topic_path):
    """Copy document to topic folder and log if error"""
    # Gets the path for the current doc location by updating the path in the metadata.
    doc_path = update_path(doc, input_dir)

    # Copies the doc to the topic_path folder.
    # If the doc is not in the expected location, logs it instead.
    # It is common to have docs in the metadata but not in the input directory.
    doc_name = doc.split('\\')[-1]
    doc_new_path = os.path.join(topic_path, doc_name)
    try:
        shutil.copy2(doc_path, doc_new_path)
    except FileNotFoundError:
        with open(os.path.join(output_dir, 'topics_sort_file_not_found.csv'), 'a', newline='') as log:
            log_writer = csv.writer(log)
            topic = topic_path.split('\\')[-2]
            log_writer.writerow([topic, doc])


def topics_sort_df(df, letter_type):
    """Make a dataframe with any row that has any value in topic and the letter type as part of the document name"""
    # Initial df, with any row of the specified type that has some value in topic (code_description)
    # and the letter type in correspondence_document_name.
    topic_df = df[df['correspondence_document_name'].str.contains(letter_type, na=False)]
    topic_df = topic_df.dropna(subset=['code_description'])

    # Removes any duplicate combinations of topic(code_description) and correspondence_document_name.
    topic_df = topic_df.drop_duplicates(subset=['code_description', 'correspondence_document_name'])
    return topic_df


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
    if md_path.lower().startswith(folders):
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

    # For accession, generates reports about the usability of the export and what might be deleted for appraisal.
    # The export is not changed in this mode.
    if script_mode == 'accession':
        print("\nThe script is running in accession mode.")
        print("It will produce usability and appraisal reports and not change the export.")
        appraisal_df = find_appraisal_rows(md_df, output_directory)
        md_df.drop(['correspondence_text'], axis=1, inplace=True)
        check_metadata_usability(md_df, output_directory)
        check_letter_matching(md_df, output_directory, input_directory)
        topics_report(md_df, output_directory)

    # For appraisal, deletes letters due to appraisal and makes a report of letters that might be restricted.
    # Restricted letters would not be included in the access copy.
    # The metadata file is not changed in this mode.
    elif script_mode == 'appraisal':
        print("\nThe script is running in appraisal mode.")
        print("It will delete letters due to appraisal and make a report of metadata to review for restrictions,"
              "but not change the metadata file.")
        try:
            appraisal_df = read_csv(os.path.join(output_directory, 'appraisal_delete_log.csv'))
        except FileNotFoundError:
            print("No appraisal_delete_log.csv in the output directory. Cannot do appraisal without it.")
            sys.exit(1)
        md_df.drop(['correspondence_text'], axis=1, inplace=True)
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)
        restriction_report(md_df, output_directory)

    # For access, removes rows for appraisal and restriction and columns with PII from the metadata,
    # makes a copy of the data split by calendar year, and makes a copy of the letters organized by topic.
    elif script_mode == 'access':
        print("\nThe script is running in access mode.")
        print("It will remove rows for deleted or restricted letters and columns with PII, "
              "make copies of the metadata split by calendar year, "
              "and make a copy of the letters to and from constituents organized by topic")
        try:
            appraisal_df = read_csv(os.path.join(output_directory, 'appraisal_delete_log.csv'))
        except FileNotFoundError:
            print("No appraisal_delete_log.csv in the output directory. Cannot do access without it.")
            sys.exit(1)
        try:
            restrict_df = read_csv(os.path.join(output_directory, 'restriction_review.csv'))
        except FileNotFoundError:
            print("No restriction_review.csv in the output directory. Cannot do access without it.")
            sys.exit(1)
        md_df = remove_appraisal_rows(md_df, appraisal_df)
        md_df = css_dif.remove_restricted_rows(md_df, restrict_df)
        md_df.drop(['correspondence_text'], axis=1, inplace=True)
        md_df.to_csv(os.path.join(output_directory, 'archiving_correspondence_redacted.csv'), index=False)
        css_dif.split_year(md_df, output_directory)
        topics_sort(md_df, input_directory, output_directory)
