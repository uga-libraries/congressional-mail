"""
Script to automate workflows for an export in the CSS Archiving Format.
Required arguments: input_directory (path to the folder with the export) and script_mode.

Script modes
accession: produce usability and appraisal reports; export not changed
appraisal: delete letters due to appraisal; metadata not changed
preservation: prepare export for general_aip.py script [TBD]
access: remove metadata rows for appraisal and columns for PII and make copy of metadata split by congress year
"""
import csv
from datetime import date, datetime
import hashlib
import numpy as np
import os
import pandas as pd
import re
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
    """Compare the files in the metadata to the files in the export"""

    # Makes a list of paths for the letters in the documents folder within the input directory.
    # This way, the metadata file is not counted as missing.
    input_dir_paths = []
    for root, dirs, files in os.walk(os.path.join(input_dir, 'documents')):
        for file in files:
            file_path = os.path.join(root, file)
            input_dir_paths.append(file_path)

    # Makes a list of paths for letters from constituents in the metadata,
    # updating the path to match how the directory is structured in the export.
    in_doc_df = df.dropna(subset=['in_document_name']).copy()
    in_doc_df['in_document_name'] = in_doc_df['in_document_name'].apply(update_path, input_dir=input_dir)
    in_doc_list = in_doc_df['in_document_name'].tolist()

    # Makes a list of paths for letters to constituents in the metadata,
    # updating the path to match how the directory is structured in the export.
    out_doc_df = df.dropna(subset=['out_document_name']).copy()
    out_doc_df['out_document_name'] = out_doc_df['out_document_name'].apply(update_path, input_dir=input_dir)
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
    """Find metadata rows with topics or text that indicate they are academy applications and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column in_topic includes one or more of the topics that indicate academy applications.
    topics_list = ['Academy Applicant', 'Military Service Academy']
    in_topic = df['in_topic'].str.contains('|'.join(topics_list), case=False, na=False)
    df_in_topic = df[in_topic]
    df = df[~in_topic]

    # Column out_topic includes one or more of the topics that indicate academy applications.
    out_topic = df['out_topic'].str.contains('|'.join(topics_list), case=False, na=False)
    df_out_topic = df[out_topic]
    df = df[~out_topic]

    # Column in_text includes "academy nomination" (case-insensitive).
    in_text = df['in_text'].str.contains('academy nomination', case=False, na=False)
    df_in_text = df[in_text]
    df = df[~in_text]

    # Column out_text includes "academy nomination" (case-insensitive).
    out_text = df['out_text'].str.contains('academy nomination', case=False, na=False)
    df_out_text = df[out_text]
    df = df[~out_text]

    # Makes a single dataframe with all rows that indicate academy applications
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_academy = pd.concat([df_in_topic, df_out_topic, df_in_text, df_out_text], axis=0, ignore_index=True)
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
    return df_appraisal


def find_casework_rows(df):
    """Find metadata rows with topics or text that indicate they are casework and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column in_topic includes one or more of the topics that indicate casework.
    topics_list = ['Casework', 'Prison Case']
    in_topic = df['in_topic'].str.contains('|'.join(topics_list), case=False, na=False)
    df_in_topic = df[in_topic]
    df = df[~in_topic]

    # Column out_topic includes one or more of the topics that indicate casework.
    out_topic = df['out_topic'].str.contains('|'.join(topics_list), case=False, na=False)
    df_out_topic = df[out_topic]
    df = df[~out_topic]

    # Column out_text is equal to a keyword that indicates casework.
    keyword_list = ['case', 'case!']
    out_text = df['out_text'].str.lower().isin(keyword_list)
    df_out_text = df[out_text]
    df = df[~out_text]

    # Any column includes a phrase that indicates casework.
    case_list = ['added to case', 'already open', 'case closed', 'case for', 'case has been opened', 'case issue',
                 'case work', 'casew', 'closed case', 'open case', 'started case']
    case_phrase = np.column_stack([df[col].str.contains('|'.join(case_list), case=False, na=False) for col in df])
    df_phrase = df.loc[case_phrase.any(axis=1)]
    df = df.loc[~case_phrase.any(axis=1)]

    # Makes a single dataframe with all rows that indicate casework
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_casework = pd.concat([df_in_topic, df_out_topic, df_out_text, df_phrase], axis=0, ignore_index=True)
    df_casework['Appraisal_Category'] = "Casework"

    # Makes another dataframe with rows containing "case" to check for new patterns that could indicate casework.
    df_casework_check = appraisal_check_df(df, 'case', 'Casework')

    return df_casework, df_casework_check


def find_job_rows(df):
    """Find metadata rows with topics or text that indicate they are job applications and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column in_topic includes one or more of the topics that indicate job applications.
    topics_list = ['Intern', 'Resume']
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

    # Makes a single dataframe with all rows that indicate job applications
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_job = pd.concat([df_in_topic, df_out_topic, df_in_text, df_out_text, df_in_doc, df_out_doc],
                       axis=0, ignore_index=True)
    df_job['Appraisal_Category'] = 'Job_Application'

    # Makes another dataframe with rows containing "job" to check for new patterns that could indicate job applications.
    df_job_check = appraisal_check_df(df, 'job', 'Job_Application')

    return df_job, df_job_check


def find_recommendation_rows(df):
    """Find metadata rows with topics or text that indicate they are recommendations and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column in_topic includes Recommendations.
    in_topic = df['in_topic'].str.contains('Recommendation', case=False, na=False)
    df_in_topic = df[in_topic]
    df = df[~in_topic]

    # Column out_topic includes Recommendations.
    out_topic = df['out_topic'].str.contains('Recommendation', case=False, na=False)
    df_out_topic = df[out_topic]
    df = df[~out_topic]

    # Column in_text includes a phrase (case_insensitive) that indicates a recommendation.
    phrase_list = ['Letter of recommendation', 'policy for recommendation', 'rec for', 'wrote recommendation']
    in_text = df['in_text'].str.contains('|'.join(phrase_list), case=False, na=False)
    df_in_text = df[in_text]
    df = df[~in_text]

    # Column out_text includes a phrase (case_insensitive) that indicates a recommendation.
    out_text = df['out_text'].str.contains('|'.join(phrase_list), case=False, na=False)
    df_out_text = df[out_text]
    df = df[~out_text]

    # Makes a single dataframe with all rows that indicate recommendations
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_recommendation = pd.concat([df_in_topic, df_out_topic, df_in_text, df_out_text], axis=0, ignore_index=True)
    df_recommendation['Appraisal_Category'] = 'Recommendation'

    # Makes another dataframe with rows containing "recommendation" to check for new patterns that could
    # indicate recommendations.
    df_recommendation_check = appraisal_check_df(df, 'recommendation', 'Recommendation')

    return df_recommendation, df_recommendation_check


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
    remove = ['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
              'addr1', 'addr2', 'addr3', 'addr4', 'in_text', 'in_fillin', 'out_text', 'out_fillin']

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
    df_undated = df[pd.to_numeric(df['in_date'], errors='coerce').isnull()]
    if len(df_undated.index) > 0:
        df_undated.to_csv(os.path.join(cy_dir, 'undated.csv'), index=False)

    # Removes rows without a year from the dataframe, so the rest can be split by Congress Year.
    df = df[pd.to_numeric(df['in_date'], errors='coerce').notnull()].copy()

    # Adds a column with the year received, which will be used to calculate the Congress Year.
    # Column in_date is formatted YYYYMMDD.
    df.loc[:, 'year'] = df['in_date'].astype(str).str[:4].astype(int)

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

    # Makes a dataframe and a csv of metadata rows that indicate appraisal.
    # This is used in most of the modes.
    appraisal_df = find_appraisal_rows(md_df, output_directory)

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
    # Run in appraisal mode first to remove letters.
    elif script_mode == 'preservation':
        print("\nThe script is running in preservation mode.")
        print("The steps are TBD.")

    # For access, removes rows for appraisal and columns with PII from the metadata
    # and makes a copy of the data split by congress year.
    elif script_mode == 'access':
        print("\nThe script is running in access mode.")
        print("It will remove rows for deleted letters and columns with PII,"
              " and make copies of the metadata split by congress year")
        md_df = remove_appraisal_rows(md_df, appraisal_df)
        md_df = remove_pii(md_df)
        md_df.to_csv(os.path.join(output_directory, 'archiving_correspondence_redacted.csv'), index=False)
        split_congress_year(md_df, output_directory)
