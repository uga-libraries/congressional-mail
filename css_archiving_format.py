"""
Script to automate workflows for an export in the CSS Archiving Format.
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
from datetime import date, datetime
import hashlib
import os
import pandas as pd
import re
import shutil
import sys
import time


def appraisal_check_df(df, keyword, category):
    """Returns a df with all rows that contain the specified keyword in any of the columns
    likely to indicate appraisal is needed, with a new column for the appraisal category"""

    # Makes a series for each column with if each row contain the keyword (case-insensitive), excluding blanks.
    in_topic = df['in_topic'].str.contains(keyword, case=False, na=False)
    in_doc = df['in_document_name'].str.contains(keyword, case=False, na=False)
    in_fillin = df['in_fillin'].str.contains(keyword, case=False, na=False)
    in_text = df['in_text'].str.contains(keyword, case=False, na=False)
    out_topic = df['out_topic'].str.contains(keyword, case=False, na=False)
    out_doc = df['out_document_name'].str.contains(keyword, case=False, na=False)
    out_fillin = df['out_fillin'].str.contains(keyword, case=False, na=False)
    out_text = df['out_text'].str.contains(keyword, case=False, na=False)

    # Makes a dataframe with all rows containing the keyword in at least one of the columns.
    df_check = df[in_topic | in_doc | in_fillin | in_text | out_topic | out_doc | out_fillin | out_text].copy()

    # Adds a column with the appraisal category.
    df_check['Appraisal_Category'] = category

    return df_check


def check_arguments(arg_list):
    """Verify the required script arguments are present and valid and get the path to the metadata file"""

    # Default values for the variables calculated by this function.
    input_dir = None
    md_path = None
    mode = None
    errors = []

    # Both arguments are missing (only the script path is present).
    if len(arg_list) == 1:
        errors.append("Missing required arguments, input_directory and script_mode")

    # At least the first argument is present.
    # Verifies it is a valid path, and if so that it contains the expected metadata file.
    if len(arg_list) > 1:
        if os.path.exists(arg_list[1]):
            input_dir = arg_list[1]
            if 'archiving_correspondence.dat' in os.listdir(input_dir):
                md_path = os.path.join(input_dir, 'archiving_correspondence.dat')
            elif 'archiving_CORRESPONDENCE.dat' in os.listdir(input_dir):
                md_path = os.path.join(input_dir, 'archiving_CORRESPONDENCE.dat')
            else:
                errors.append(f"No archiving_correspondence.dat file in the input_directory")
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

    return input_dir, md_path, mode, errors


def check_letter_matching(df, output_dir, input_dir):
    """Compare the files in the metadata to the files in the export,
    reformatting the metadata paths and making all characters lowercase, so they can match"""

    # Makes a list of paths for the letters in the documents folder within the input directory.
    # This way, the metadata file is not counted as missing.
    input_dir_paths = []
    for root, dirs, files in os.walk(os.path.join(input_dir, 'documents')):
        for file in files:
            file_path = os.path.join(root, file)
            file_path = file_path.lower()
            input_dir_paths.append(file_path)

    # Makes a list of paths for letters from constituents in the metadata,
    # updating the path to match how the directory is structured in the export.
    in_doc_df = df.dropna(subset=['in_document_name']).copy()
    in_doc_df['in_document_name'] = in_doc_df['in_document_name'].apply(update_path, input_dir=input_dir)
    in_doc_df['in_document_name'] = in_doc_df['in_document_name'].str.lower()
    in_doc_list = in_doc_df['in_document_name'].tolist()

    # Makes a list of paths for letters to constituents in the metadata,
    # updating the path to match how the directory is structured in the export.
    out_doc_df = df.dropna(subset=['out_document_name']).copy()
    out_doc_df['out_document_name'] = out_doc_df['out_document_name'].apply(update_path, input_dir=input_dir)
    out_doc_df['out_document_name'] = out_doc_df['out_document_name'].str.lower()
    out_doc_list = out_doc_df['out_document_name'].tolist()

    # Number of metadata rows without a file path.
    blank_in_doc = df['in_document_name'].isna().sum()
    blank_out_doc = df['out_document_name'].isna().sum()
    blank_total = blank_in_doc + blank_out_doc

    # Compares the combined list of file paths in the metadata to the export directory.
    metadata_paths = in_doc_list + out_doc_list
    metadata_only = list(set(metadata_paths) - set(input_dir_paths))
    directory_only = list(set(input_dir_paths) - set(metadata_paths))
    match = list(set(metadata_paths) & set(input_dir_paths))

    # Saves a summary of the results.
    metadata_total = len(metadata_only) + len(match) + blank_total
    with open(os.path.join(output_dir, 'usability_report_matching.csv'), 'w', newline='') as report:
        report_writer = csv.writer(report)
        report_writer.writerow(['Category', 'Row/File_Count', 'Row_Percent'])
        report_writer.writerow(['Match', len(match), f'{int(round(len(match)/metadata_total*100,0))}%'])
        report_writer.writerow(['Metadata_Only', len(metadata_only), f'{int(round(len(metadata_only)/metadata_total*100,0))}%'])
        report_writer.writerow(['Metadata_Blank', blank_total, f'{int(round(blank_total/metadata_total*100,0))}%']),
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
    """Return the number of rows that don't meet the expected formatting
    and save the rows to a csv"""

    # Dictionary of expected formatting patterns for each column.
    patterns = {'in_date': r'^\d{8}$',
                'out_date': r'^\d{8}$',
                'state': r'^[A-Z]\.?[A-Z]\.?$',
                'zip': r'^\d{5}(-\d{4})?(-X{4})?$'}

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


def check_metadata_formatting_multi(column, df, output_dir):
    """Return the number of rows that don't meet the expected formatting when more than one format is permitted
    and save the rows to a csv"""

    # Makes a dataframe with all rows that do not match any of the expected formatting, excluding blanks.
    # If the column is missing from the dataframe or blank, it returns default text instead of a row count.
    try:
        match_blob = df[column].str.contains(r'^..\\documents\\BlobExport\\', regex=True, na=False)
        match_dos = df[column].str.contains(r'^\\\\[a-z]+-[a-z]+\\dos\\public', regex=True, na=False)
        match_e = df[column].str.contains(r'^e:\\emailobj', regex=True, na=False)
    except KeyError:
        return 'column_missing'
    except AttributeError:
        return 'column_blank'
    df_no_match = df[~(match_blob | match_dos | match_e) & df[column].notna()]

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
    expected = ['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin']
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
    state_mismatch = check_metadata_formatting('state', df, output_dir)
    zip_mismatch = check_metadata_formatting('zip', df, output_dir)
    in_date_mismatch = check_metadata_formatting('in_date', df, output_dir)
    in_doc_mismatch = check_metadata_formatting_multi('in_document_name', df, output_dir)
    out_date_mismatch = check_metadata_formatting('out_date', df, output_dir)
    out_doc_mismatch = check_metadata_formatting_multi('out_document_name', df, output_dir)

    # Combines the number of formatting errors for the checked columns into a series, for adding to the report.
    # Other columns have "uncheckable", even if the column is missing from the export.
    formatting = pd.Series(data=['uncheckable', 'uncheckable', 'uncheckable', 'uncheckable', 'uncheckable',
                                 'uncheckable', 'uncheckable', 'uncheckable', 'uncheckable', 'uncheckable',
                                 'uncheckable', 'uncheckable', 'uncheckable', state_mismatch, zip_mismatch,
                                 'uncheckable', 'uncheckable', 'uncheckable', 'uncheckable', in_date_mismatch,
                                 'uncheckable', 'uncheckable', in_doc_mismatch, 'uncheckable', 'uncheckable',
                                 'uncheckable', 'uncheckable', out_date_mismatch, 'uncheckable', 'uncheckable',
                                 out_doc_mismatch, 'uncheckable'], index=expected)

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

    # For every row in df_appraisal, deletes any letter in the in_document_name and out_document_name columns.
    # The letter path has to be reformatted to match the actual export, and an error is logged if it is a new pattern.
    # Form letters are retained.
    df_appraisal = df_appraisal.astype(str)
    for row in df_appraisal.itertuples():
        name = row.in_document_name
        if name != '' and name != 'nan':
            file_path = update_path(name, input_dir)
            if file_path == 'error_new':
                file_deletion_log(log_path, name, 'Cannot determine file path: new path pattern in metadata')
            else:
                try:
                    file_deletion_log(log_path, file_path, row.Appraisal_Category)
                    os.remove(file_path)
                except FileNotFoundError:
                    file_deletion_log(log_path, file_path, 'Cannot delete: FileNotFoundError')

        # Deletes individual letters, not form letters, sent to constituents, if the "out" column isn't blank.
        name = row.out_document_name
        if name != '' and name != 'nan' and 'form' not in name:
            file_path = update_path(name, input_dir)
            if file_path == 'error_new':
                file_deletion_log(log_path, name, 'Cannot determine file path: new path pattern in metadata')
            # Only delete if it is a file. Sometimes, out_document_name has the path to a folder instead.
            else:
                if os.path.isfile(file_path):
                    file_deletion_log(log_path, file_path, row.Appraisal_Category)
                    os.remove(file_path)
                elif not os.path.exists(file_path):
                    file_deletion_log(log_path, file_path, 'Cannot delete: FileNotFoundError')


def df_search(df, keywords, category):
    """Returns a df with all rows that contain any of the keywords indicating this category of appraisal"""

    # Columns to search, which are the ones that reasonably might indicate appraisal.
    columns_list = ['in_topic', 'in_document_name', 'in_fillin', 'in_text',
                    'out_topic', 'out_document_name', 'out_fillin', 'out_text']

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


def file_deletion_log(log_path, file_path, note):
    """Make or update the file deletion log, so data is saved as soon as a file is deleted
    Data included follows https://github.com/uga-libraries/accessioning-scripts/blob/main/technical-appraisal-logs.py
    This is used by the scripts for other export types as well"""

    # Makes a new log with a header row.
    # If a file already exists with this name, it will be overwritten.
    if note == 'header':
        with open(log_path, 'w', newline='') as log:
            log_writer = csv.writer(log)
            log_writer.writerow(['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'])

    # Adds a row for a file with errors (cannot calculate file path or file is not found) to an existing log.
    elif note.startswith('Cannot'):
        with open(log_path, 'a', newline='') as log:
            log_writer = csv.writer(log)
            log_writer.writerow([file_path, None, None, None, None, note])

    # Adds a row for a file that can be deleted to an existing log.
    else:
        size_kb = round(int(os.path.getsize(file_path))/1000, 1)
        date_c = datetime.strptime(time.ctime(os.path.getctime(file_path)), '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d')
        with open(file_path, 'rb') as f:
            file_data = f.read()
        md5 = hashlib.md5(file_data).hexdigest().upper()
        date_d = date.today().strftime('%Y-%m-%d')
        with open(log_path, 'a', newline='') as log:
            log_writer = csv.writer(log)
            log_writer.writerow([file_path, size_kb, date_c, date_d, md5, note])


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
    return df_appraisal


def find_casework_rows(df):
    """Find metadata rows with topics or text that indicate they are casework and return as a df
    Once a row matches one pattern, it is not considered for other patterns.
    We will delete even if the phrase indicates it is not a case or casework
    because the fact they considered it might be a case suggests it includes sensitive personal information."""

    # Column in_topic includes one or more of the topics that indicate casework.
    topics_list = ['case work', 'casework', 'prison case']
    in_topic = df['in_topic'].str.contains('|'.join(topics_list), case=False, na=False)
    df_in_topic = df[in_topic]
    df = df[~in_topic]

    # Column out_topic includes one or more of the topics that indicate casework.
    out_topic = df['out_topic'].str.contains('|'.join(topics_list), case=False, na=False)
    df_out_topic = df[out_topic]
    df = df[~out_topic]

    # Column in_type is CASE.
    df_in_type = df[df['in_type'] == 'CASE']
    df = df[df['in_type'] != 'CASE']

    # Column out_type is CASE.
    df_out_type = df[df['out_type'] == 'CASE']
    df = df[df['out_type'] != 'CASE']

    # Column out_text exactly matches a keyword that indicates casework.
    # These would get too many false positives if added to the keywords list.
    exact_list = ['case', 'case!']
    out_text_exact = df['out_text'].str.lower().isin(exact_list)
    df_out_text_exact = df[out_text_exact]
    df = df[~out_text_exact]

    # Keywords used for all other columns.
    keywords_list = ['added to case', 'already open', 'case closed', 'case for', 'case has been opened',
                     'case issue', 'case work', 'casework', 'closed case', 'open case', 'started case']

    # Column in_text includes one of the keywords (case-insensitive).
    in_text = df['in_text'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_in_text = df[in_text]
    df = df[~in_text]

    # Column out_text includes one of the keywords (case-insensitive).
    out_text = df['out_text'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_out_text = df[out_text]
    df = df[~out_text]

    # Column in_document_name includes one of the keywords (case-insensitive).
    in_doc = df['in_document_name'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_in_doc = df[in_doc]
    df = df[~in_doc]

    # Column out_document_name includes one of the keywords (case-insensitive).
    out_doc = df['out_document_name'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_out_doc = df[out_doc]
    df = df[~out_doc]

    # Column out_fillin includes one of the keywords (case-insensitive).
    out_fill = df['out_fillin'].str.contains('|'.join(keywords_list), case=False, na=False)
    df_outfill = df[out_fill]
    df = df[~out_fill]

    # Makes a single dataframe with all rows that indicate casework
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_casework = pd.concat([df_in_topic, df_out_topic, df_in_type, df_out_type, df_out_text_exact,
                             df_in_text, df_out_text, df_in_doc, df_out_doc, df_outfill], axis=0, ignore_index=True)
    df_casework['Appraisal_Category'] = "Casework"

    # Makes another dataframe with rows containing "case" to check for new patterns that could indicate casework.
    df_casework_check = appraisal_check_df(df, 'case', 'Casework')

    return df_casework, df_casework_check


def find_job_rows(df):
    """Find metadata rows with topics or text that indicate they are job applications and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column in_topic includes one or more of the topics that indicate job applications.
    topics_list = ['intern', 'resume']
    in_topic = df['in_topic'].str.contains('|'.join(topics_list), case=False, na=False)
    df_in_topic = df[in_topic]
    df = df[~in_topic]

    # Column out_topic includes one or more of the topics that indicate job applications.
    out_topic = df['out_topic'].str.contains('|'.join(topics_list), case=False, na=False)
    df_out_topic = df[out_topic]
    df = df[~out_topic]

    # Column in_text includes "job request" (case-insensitive).
    word_list = ['job request', 'resume']
    in_text = df['in_text'].str.contains('|'.join(word_list), case=False, na=False)
    df_in_text = df[in_text]
    df = df[~in_text]

    # Column out_text includes "job request" (case-insensitive).
    out_text = df['out_text'].str.contains('|'.join(word_list), case=False, na=False)
    df_out_text = df[out_text]
    df = df[~out_text]

    # Column in_document_name includes text that indicates job applications (case-insensitive).
    names_list = ['job interview', 'resume']
    in_doc = df['in_document_name'].str.contains('|'.join(names_list), case=False, na=False)
    df_in_doc = df[in_doc]
    df = df[~in_doc]

    # Column out_document_name includes text that indicates job applications (case-insensitive).
    out_doc = df['out_document_name'].str.contains('|'.join(names_list), case=False, na=False)
    df_out_doc = df[out_doc]
    df = df[~out_doc]

    # Column out_fillin includes text that indicates job applications (case-insensitive).
    fill_list = ['intern', 'job interview', 'job request', 'resume']
    out_fill = df['out_fillin'].str.contains('|'.join(fill_list), case=False, na=False)
    df_out_fill = df[out_fill]
    df = df[~out_fill]

    # Makes a single dataframe with all rows that indicate job applications
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_job = pd.concat([df_in_topic, df_out_topic, df_in_text, df_out_text, df_in_doc, df_out_doc, df_out_fill],
                       axis=0, ignore_index=True)
    df_job['Appraisal_Category'] = 'Job_Application'

    # Makes another dataframe with rows containing "job" to check for new patterns that could indicate job applications.
    df_job_check = appraisal_check_df(df, 'job', 'Job_Application')

    return df_job, df_job_check


def find_recommendation_rows(df):
    """Find metadata rows with keywords that indicate they might be recommendations
    and return as two dfs, one with more certainty (df_recommendation) and one with less (df_recommendation_check)
    Once a row matches one pattern, it is not considered for other patterns."""

    # Makes df with more certainty.
    keywords = 'intern rec|page rec|rec for|recommendation'
    df_recommendation, df_unmatched = df_search(df, keywords, 'Recommendation')

    # Makes another dataframe with rows containing "recommendation" to check for new patterns that could
    # indicate recommendations.
    df_recommendation_check = appraisal_check_df(df, 'recommendation', 'Recommendation')

    return df_recommendation, df_recommendation_check


def read_csv(path):
    """Read a CSV produced by a previous mode of this script into a dataframe"""
    try:
        df = pd.read_csv(path, dtype=str, on_bad_lines='warn')
        return df
    except FileNotFoundError:
        raise FileNotFoundError


def read_metadata(path):
    """Read the metadata file into a dataframe"""
    try:
        df = pd.read_csv(path, delimiter='\t', dtype=str, on_bad_lines='warn')
    except UnicodeDecodeError:
        print("\nUnicodeDecodeError when trying to read the metadata file.")
        print("The file will be read by ignoring encoding errors, skipping characters that cause an error.\n")
        df = pd.read_csv(path, delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn')

    # Removes blank rows, which are present in some of the data exports.
    df.dropna(how='all', inplace=True)

    # Splits rows with multiple documents (in and/or out) so they can be matched to the files in the export.
    # The rest of the row is repeated for each in/out document combination.
    df['in_document_name'] = df['in_document_name'].str.split(r'^')
    df = df.explode('in_document_name')
    df['out_document_name'] = df['out_document_name'].str.split(r'^')
    df = df.explode('out_document_name')

    return df


def remove_appraisal_rows(df, df_appraisal):
    """Remove metadata rows for letters deleted during appraisal and return the updated df"""

    # Makes an updated dataframe with just rows in df that are not in df_appraisal.
    df_merge = df.merge(df_appraisal, how='left', indicator=True)
    df_update = df_merge[df_merge['_merge'] == 'left_only'].drop(columns=['_merge', 'Appraisal_Category'])

    return df_update


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names to remove because they include constituent names or addresses.
    remove = ['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
              'addr1', 'addr2', 'addr3', 'addr4', 'in_text', 'in_fillin', 'out_text', 'out_fillin']

    # Removes every column on the remove list from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    df = df.drop(remove, axis=1, errors='ignore')
    
    return df


def remove_restricted_rows(df, df_restrict):
    """Remove metadata rows for restricted letters (in preservation but not access copy) and return the updated df"""

    # Columns for individual topics when there is a delimiter are removed, so the row matches exactly,
    # and duplicate rows from splitting rows based on the delimiters for the review are also removed.
    df_restrict = df_restrict.drop(columns=['in_topic_split', 'out_topic_split'])
    df_restrict = df_restrict.drop_duplicates()

    # Makes an updated dataframe with just rows in df that are not in df_restrict.
    df_merge = df.merge(df_restrict, how='left', indicator=True)
    df_update = df_merge[df_merge['_merge'] == 'left_only'].drop(columns=['_merge'])

    return df_update


def restriction_report(df, output_dir):
    """Make report of any row with topics that require restriction if they are about individuals' situations"""

    # Make a copy of the df repeating any rows with delimited topics, one row per topic, for more accurate matches.
    # The original topic columns are retained so it can be matched to md_df for making the redacted access copy.
    df_restrict = df.copy()
    df_restrict['in_topic_split'] = df_restrict['in_topic'].str.split(r'^')
    df_restrict = df_restrict.explode('in_topic_split')
    df_restrict['out_topic_split'] = df_restrict['out_topic'].str.split(r'^')
    df_restrict = df_restrict.explode('out_topic_split')

    # List of topics (adjust based on topics_report.csv from accession mode of this script)
    restrict_list = ['citizen', 'citizenship', 'court', 'crime', 'criminal justice',
                     'immigrant', 'immigration', 'migrant', 'refugee']

    # Save the subset of the df where the topic matches any term in the restrict list to the output directory.
    # No report is made if no topics are present.
    report_df = df_restrict[df_restrict['in_topic_split'].isin(restrict_list) |
                            df_restrict['out_topic_split'].isin(restrict_list)]
    if len(report_df.index) > 0:
        report_df.to_csv(os.path.join(output_dir, 'restriction_review.csv'), index=False)


def split_year(df, output_dir):
    """Make one metadata CSV per calendar year for smaller amount of data to review"""

    # Makes a folder for all the CSVs.
    year_dir = os.path.join(output_dir, 'correspondence_metadata_by_year')
    os.mkdir(year_dir)

    # Saves rows without a year (date is a not a number, could be blank or text) to a CSV, if any.
    df_undated = df[pd.to_numeric(df['in_date'], errors='coerce').isnull()]
    if len(df_undated.index) > 0:
        df_undated.to_csv(os.path.join(year_dir, 'undated.csv'), index=False)

    # Removes rows without a year from the dataframe, so the rest can be split by calendar year.
    df = df[pd.to_numeric(df['in_date'], errors='coerce').notnull()].copy()

    # Adds a column with the year received. Column in_date is formatted YYYYMMDD.
    df.loc[:, 'year'] = df['in_date'].astype(str).str[:4].astype(int)

    # Splits the rows with date information by year received and saves each group to a separate CSV.
    # The year column is first removed, so the metadata CSVs only has the original columns.
    for year, df in df.groupby('year'):
        df = df.drop(['year'], axis=1)
        df.to_csv(os.path.join(year_dir, f'{year}.csv'), index=False)


def topics_report(df, output_dir):
    """Make a report with the frequency of each topic"""

    # Replace blanks with BLANK so that it is counted as a topic.
    df['in_topic'] = df['in_topic'].fillna('BLANK')
    df['out_topic'] = df['out_topic'].fillna('BLANK')

    # Get a count for each topic in each topic column.
    in_topic_counts = df['in_topic'].value_counts().reset_index()
    in_topic_counts.columns = ['Topic', 'In_Topic_Count']
    out_topic_counts = df['out_topic'].value_counts().reset_index()
    out_topic_counts.columns = ['Topic', 'Out_Topic_Count']

    # Combines the counts into a single dataframe, with 0 instead of NaN.
    df_counts = in_topic_counts.merge(out_topic_counts, how='outer', on='Topic')
    df_counts = df_counts.fillna(0)
    df_counts['In_Topic_Count'] = df_counts['In_Topic_Count'].astype(int)
    df_counts['Out_Topic_Count'] = df_counts['Out_Topic_Count'].astype(int)

    # Adds a totals column to the dataframe.
    df_counts['Total'] = df_counts['In_Topic_Count'] + df_counts['Out_Topic_Count']

    # Save to a CSV.
    df_counts.to_csv(os.path.join(output_dir, 'topics_report.csv'), index=False)


def topics_sort(df, input_dir, output_dir):
    """Sort copy of incoming and outgoing correspondence into folders by topic"""
    os.mkdir(os.path.join(output_dir, 'Correspondence_by_Topic'))

    # Sorts a copy of correspondence from constituents ("in" letters) by topic.
    in_df = topics_sort_df(df, 'in')
    topic_list = in_df['in_topic'].unique()
    for topic in topic_list:
        doc_list = in_df.loc[in_df['in_topic'] == topic, 'in_document_name'].tolist()
        topic_path = topics_sort_folder(topic, output_dir, 'from_constituents')
        for doc in doc_list:
            topics_sort_copy(doc, input_dir, output_dir, topic_path)
        topics_sort_delete_empty(topic_path)

    # Sorts a copy of correspondence to constituents ("out" letters) by topic.
    # In and out letters with the same topic are in the same topic folder, but different subfolders.
    out_df = topics_sort_df(df, 'out')
    topic_list = out_df['out_topic'].unique()
    for topic in topic_list:
        doc_list = out_df.loc[out_df['out_topic'] == topic, 'out_document_name'].tolist()
        topic_path = topics_sort_folder(topic, output_dir, 'to_constituents')
        for doc in doc_list:
            topics_sort_copy(doc, input_dir, output_dir, topic_path)
        topics_sort_delete_empty(topic_path)


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


def topics_sort_delete_empty(topic_path):
    """Delete the to/from constituents folder if empty, and then delete the topic folder if empty"""
    # Deletes the to/from constituents folder if it is empty, from none of the documents being in the export,
    if not os.listdir(topic_path):
        os.rmdir(topic_path)

        # Deletes the topic folder if it is also empty.
        # It could contain a from_constituents folder if the function is called to delete to_constituents.
        if not os.listdir(os.path.dirname(topic_path)):
            os.rmdir(os.path.dirname(topic_path))


def topics_sort_df(df, letter_type):
    """Make a dataframe with any row that has values in topic and document_name"""
    # Initial df, with any row that has some value in topic and document_name
    topic_column = f'{letter_type}_topic'
    doc_column = f'{letter_type}_document_name'
    topic_df = df.dropna(subset=[topic_column, doc_column]).copy()

    # If there is more than one topic or document_name in a row (divided by ^),
    # splits them to their own row, repeating the related topic or document_name for each row.
    topic_df[topic_column] = topic_df[topic_column].str.split(r'^')
    topic_df = topic_df.explode(topic_column)
    topic_df[doc_column] = topic_df[doc_column].str.split(r'^')
    topic_df = topic_df.explode(doc_column)

    # Removes any duplicate combinations of topic and document_name,
    # which is most common when the office sends the same letter to multiple constituents.
    topic_df = topic_df.drop_duplicates(subset=[topic_column, doc_column])
    return topic_df


def topics_sort_folder(topic, output_dir, type_folder_name):
    """Make a folder named with the topic and return the path to that folder"""
    # Replaces characters that Windows does not permit in a folder name with an underscore.
    for character in ('\\', '/', ':', '*', '?', '"', '<', '>', '|'):
        topic = topic.replace(character, '_')

    # Removes space or period from the end, as Windows is inconsistent in how it handles folders ending in either.
    topic = topic.rstrip('. ')

    # Makes the path, including a folder with the letter type.
    topic_path = os.path.join(output_dir, 'Correspondence_by_Topic', topic, type_folder_name)

    # Only makes the folder if it doesn't already exist. Even though topics are deduplicated before making folders,
    # we still get duplicates if the same topic exists in a ways that do and do not require cleanup.
    if not os.path.exists(topic_path):
        os.makedirs(topic_path)

    return topic_path


def update_path(md_path, input_dir):
    """Update a path found in the metadata to match the actual directory structure of the exports"""

    # So far, we have seen three ways that paths are formatted in the metadata:
    # ..\documents\BlobExport\folder\..\file.ext, where the export is \documents\folder\..\file.ext
    #  \\name-office\dos\public\folder\..\file.ext, where the export is \documents\folder\..\file.ext
    # e:\emailobj\folder\file.ext, where export pattern is unknown (none in export)
    if md_path.startswith('..'):
        updated_path = md_path.replace('..', input_dir)
        updated_path = updated_path.replace('\\BlobExport', '')
    elif '\\dos\\public\\' in md_path:
        updated_path = re.sub('\\\\[a-z]+-[a-z]+\\\\dos\\\\public', 'documents', md_path)
        updated_path = input_dir + updated_path
    elif md_path.startswith('e:\\emailobj\\'):
        updated_path = md_path.replace('e:', input_dir)
    else:
        updated_path = 'error_new'

    return updated_path


if __name__ == '__main__':

    # Validates the script argument values and calculates the path to the metadata file.
    # If there are any errors, prints them and exits the script.
    input_directory, metadata_path, script_mode, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Calculates parent folder of the input_directory, which is where script outputs are saved.
    output_directory = os.path.dirname(input_directory)

    # Reads the metadata file into a pandas dataframe.
    md_df = read_metadata(metadata_path)

    # For accession, generates reports about the usability of the export and what might be deleted for appraisal.
    # The export is not changed in this mode.
    if script_mode == 'accession':
        print("\nThe script is running in accession mode.")
        print("It will produce usability and appraisal reports and not change the export.")
        appraisal_df = find_appraisal_rows(md_df, output_directory)
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
        md_df = remove_restricted_rows(md_df, restrict_df)
        md_df = remove_pii(md_df)
        md_df.to_csv(os.path.join(output_directory, 'archiving_correspondence_redacted.csv'), index=False)
        split_year(md_df, output_directory)
        topics_sort(md_df, input_directory, output_directory)
