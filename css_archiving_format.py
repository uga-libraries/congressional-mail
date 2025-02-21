"""
Draft script to prepare preservation and access copies from an export in the CSS Archiving Format.
Required arguments: input_directory (path to the folder with the css export) and script_mode (access or preservation).
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
    # Verifies it is a valid path, and if so that it contains the expected DAT file.
    if len(arg_list) > 1:
        if os.path.exists(arg_list[1]):
            input_dir = arg_list[1]
            if os.path.exists(os.path.join(input_dir, 'archiving_correspondence.dat')):
                md_path = os.path.join(input_dir, 'archiving_correspondence.dat')
            elif os.path.exists(os.path.join(input_dir, 'archiving_correspondence.dat')):
                md_path = os.path.join(input_dir, 'archiving_CORRESPONDENCE.dat')
            else:
                errors.append(f"No archiving_correspondence.dat file in the input_directory")
        else:
            errors.append(f"Provided input_directory '{arg_list[1]}' does not exist")

    # Both required arguments are present.
    # Verifies the second is one of the expected modes.
    if len(arg_list) > 2:
        if arg_list[2] in ('access', 'preservation'):
            mode = arg_list[2]
        else:
            errors.append(f"Provided mode '{arg_list[2]} is not 'access' or 'preservation'")

    # More than the expected two required arguments are present.
    if len(arg_list) > 3:
        errors.append("Provided more than the required arguments, input_directory and script_mode")

    return input_dir, md_path, mode, errors


def delete_appraisal_letters(input_dir, df_appraisal):
    """Deletes letters received from constituents and individual letters sent back by the office
    because they are one of the types of letters not retained for appraisal reasons"""

    # Creates a file deletion log, with a header row.
    log_path = os.path.join(os.path.dirname(input_dir), f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv")
    file_deletion_log(log_path, None, 'header')

    # For every row in df_appraisal, delete any letter in the in_document_name and out_document_name columns.
    # The letter path has to be reformatted to match the actual export.
    for row in df_appraisal.itertuples():

        # Deletes letters received from constituents, if the "in" column isn't blank.
        if row.in_document_name != '':
            name = row.in_document_name
            file_path = name.replace('..', input_dir)
            file_path = file_path.replace('\\BlobExport', '')
            try:
                file_deletion_log(log_path, file_path, row.Appraisal_Category)
                os.remove(file_path)
            except FileNotFoundError:
                file_deletion_log(log_path, file_path, 'Cannot delete: FileNotFoundError')

        # Deletes individual letters, not form letters, sent to constituents, if the "out" column isn't blank.
        if row.out_document_name != '' and 'form' not in row.out_document_name:
            name = row.out_document_name
            # Make an absolute path from name, which starts ..\documents or \\name-office\dos\public.
            if name.startswith('..'):
                file_path = name.replace('..', input_dir)
                file_path = file_path.replace('\\BlobExport', '')
            else:
                file_path = re.sub('\\\\[a-z]+-[a-z]+\\\\dos\\\\public', 'documents', name)
                file_path = input_dir + file_path
            # Only delete if it is a file. Sometimes, out_document_name has the path to a folder instead.
            if os.path.isfile(file_path):
                file_deletion_log(log_path, file_path, row.Appraisal_Category)
                os.remove(file_path)
            elif not os.path.exists(file_path):
                file_deletion_log(log_path, file_path, 'Cannot delete: FileNotFoundError')


def file_deletion_log(log_path, file_path, note):
    """Make or update the file deletion log, so data is saved as soon as a file is deleted
    Data included follows https://github.com/uga-libraries/accessioning-scripts/blob/main/technical-appraisal-logs.py"""

    # Makes a new log with a header row.
    # If a file already exists with this name, it will be overwritten.
    if note == 'header':
        with open(log_path, 'w', newline='') as log:
            log_writer = csv.writer(log)
            log_writer.writerow(['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'])

    # Adds a row for a file that could not be deleted to an existing log.
    elif note == 'Cannot delete: FileNotFoundError':
        # Adds the file to the log.
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

    # Column in_topic includes Academy Applicant or Military Service Academy.
    in_topic = df['in_topic'].str.contains('|'.join(['Academy Applicant', 'Military Service Academy']), na=False)
    df_in_topic = df[in_topic]
    df = df[~in_topic]

    # Column out_topic includes Academy Applicant or Military Service Academy.
    out_topic = df['out_topic'].str.contains('|'.join(['Academy Applicant', 'Military Service Academy']), na=False)
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

    # Makes another dataframe with any remaining rows with "academy" in any column
    # and adds a column for the potential appraisal category to aid in review.
    # This may show us another pattern that indicates academy applications or may be another use of the word academy.
    check = np.column_stack([df[col].str.contains('academy', case=False, na=False) for col in df])
    df_academy_check = df.loc[check.any(axis=1)].copy()
    df_academy_check['Appraisal_Category'] = 'Academy_Application'

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
    df_appraisal = df_appraisal.groupby([col for col in df_appraisal.columns if col != 'Appraisal_Category'])['Appraisal_Category'].apply(lambda x: '|'.join(map(str, x))).reset_index()
    df_appraisal.to_csv(os.path.join(output_dir, 'appraisal_delete_log.csv'), index=False)
    return df_appraisal


def find_casework_rows(df):
    """Find metadata rows with topics or text that indicate they are casework and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column in_topic includes one or more of the topics that indicates casework.
    topics_list = ['Casework', 'Casework Issues', 'Prison Case']
    casework_topic = df['in_topic'].str.contains('|'.join(topics_list), na=False)
    df_topic = df[casework_topic]
    df = df[~casework_topic]

    # Column includes the text "casework".
    # This includes a few rows with phrases like "this is not casework",
    # which is necessary to protect privacy and keep time required reasonable.
    casework = np.column_stack([df[col].str.contains('casework', case=False, na=False) for col in df])
    df_cw = df.loc[casework.any(axis=1)]
    df = df.loc[~casework.any(axis=1)]

    # Column has a phrase with "case" that indicates casework.
    # Specific phrases are used to avoid unnecessarily removing other topics like legal cases.
    case_list = ['added to case', 'already open', 'closed case', 'open case', 'started case']
    case_phrase = np.column_stack([df[col].str.contains('|'.join(case_list), case=False, na=False) for col in df])
    df_phrase = df.loc[case_phrase.any(axis=1)]
    df = df.loc[~case_phrase.any(axis=1)]

    # Makes a single dataframe with all rows that indicate casework
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_casework = pd.concat([df_topic, df_cw, df_phrase], axis=0, ignore_index=True)
    df_casework['Appraisal_Category'] = "Casework"

    # Makes another dataframe with any remaining rows with "case" in any column
    # and adds a column for the potential appraisal category to aid in review.
    # This may show us another pattern that indicates casework or may be another use of the word case.
    check = np.column_stack([df[col].str.contains('case', case=False, na=False) for col in df])
    df_casework_check = df.loc[check.any(axis=1)].copy()
    df_casework_check['Appraisal_Category'] = 'Casework'

    return df_casework, df_casework_check


def find_job_rows(df):
    """Find metadata rows with topics or text that indicate they are job applications and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column in_topic includes Intern or Resumes.
    in_topic = df['in_topic'].str.contains('|'.join(['Intern', 'Resumes']), na=False)
    df_in_topic = df[in_topic]
    df = df[~in_topic]

    # Column out_topic includes Intern or Resumes.
    out_topic = df['out_topic'].str.contains('|'.join(['Intern', 'Resumes']), na=False)
    df_out_topic = df[out_topic]
    df = df[~out_topic]

    # Column in_text includes "job request" (case-insensitive).
    in_text = df['in_text'].str.contains('job request', case=False, na=False)
    df_in_text = df[in_text]
    df = df[~in_text]

    # Column out_text includes "job request" (case-insensitive).
    out_text = df['out_text'].str.contains('job request', case=False, na=False)
    df_out_text = df[out_text]
    df = df[~out_text]

    # Column out_document_name includes "job interview" or "resume.txt" (case-insensitive).
    out_doc = df['out_document_name'].str.contains('|'.join(['job interview', 'resume.txt']), case=False, na=False)
    df_out_doc = df[out_doc]
    df = df[~out_doc]

    # Makes a single dataframe with all rows that indicate job applications
    # and adds a column for the appraisal category (needed for the file deletion log).
    df_job = pd.concat([df_in_topic, df_out_topic, df_in_text, df_out_text, df_out_doc], axis=0, ignore_index=True)
    df_job['Appraisal_Category'] = 'Job_Application'

    # Makes another dataframe with any remaining rows with "job" in any column
    # and adds a column for the potential appraisal category to aid in review.
    # This may show us another pattern that indicates job applications or may be another use of the word job.
    check = np.column_stack([df[col].str.contains('job', case=False, na=False) for col in df])
    df_job_check = df.loc[check.any(axis=1)].copy()
    df_job_check['Appraisal_Category'] = 'Job_Application'

    return df_job, df_job_check


def find_recommendation_rows(df):
    """Find metadata rows with topics or text that indicate they are recommendations and return as a df
    Once a row matches one pattern, it is not considered for other patterns."""

    # Column in_topic includes Recommendations.
    in_topic = df['in_topic'].str.contains('Recommendations', na=False)
    df_in_topic = df[in_topic]
    df = df[~in_topic]

    # Column out_topic includes Recommendations.
    out_topic = df['out_topic'].str.contains('Recommendations', na=False)
    df_out_topic = df[out_topic]
    df = df[~out_topic]

    # Column in_text includes a phrase (case_insensitive) that indicates a recommendation.
    phrase_list = ['Letter of recommendation', 'policy for recommendations', 'rec for', 'wrote recommendation']
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

    # Makes another dataframe with any remaining rows with "recommendation" in any column
    # and adds a column for the potential appraisal category to aid in review.
    # This may show us another pattern that indicates recommendations or may be another use of the word recommendation.
    check = np.column_stack([df[col].str.contains('recommendation', case=False, na=False) for col in df])
    df_recommendation_check = df.loc[check.any(axis=1)].copy()
    df_recommendation_check['Appraisal_Category'] = 'Recommendation'

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

    # Makes an updated dataframe with just rows in df that are not in df_appraisal.
    df_merge = df.merge(df_appraisal, how='left', indicator=True)
    df_update = df_merge[df_merge['_merge'] == 'left_only'].drop(columns=['_merge'])

    return df_update


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed because they include names or addresses.
    remove = ['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
              'addr1', 'addr2', 'addr3', 'addr4', 'in_text', 'in_fillin', 'out_text', 'out_fillin']

    # Removes every column on the remove list from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    df = df.drop(remove, axis=1, errors='ignore')
    
    return df


def split_congress_year(df, output_dir):
    """Make one CSV per Congress Year"""

    # Saves rows without a year (date is a not a number, could be blank or text) to a CSV, if any.
    df_undated = df[pd.to_numeric(df['in_date'], errors='coerce').isnull()]
    if len(df_undated.index) > 0:
        df_undated.to_csv(os.path.join(output_dir, 'undated.csv'), index=False)

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

    # Splits the data by Congress Year received and saves each to a separate CSV.
    # The year and congress_year columns are first removed, so the CSV only has the original columns.
    for congress_year, cy_df in df.groupby('congress_year'):
        cy_df = cy_df.drop(['year', 'congress_year'], axis=1)
        cy_df.to_csv(os.path.join(output_dir, f'{congress_year}.csv'), index=False)


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

    # Finds rows in the metadata that are for appraisal and saves to a CSV.
    appraisal_df = find_appraisal_rows(md_df, output_directory)

    # For preservation, deletes files for appraisal decisions.
    # It uses the log from find_appraisal_rows() to know what to delete.
    if script_mode == 'preservation':
        delete_appraisal_letters(input_directory, appraisal_df)

    # For access, removes rows for appraisal and columns with PII from the metadata
    # and makes a copy of the data split by congress year.
    if script_mode == 'access':
        md_df = remove_appraisal_rows(md_df, appraisal_df)
        md_df = remove_pii(md_df)
        md_df.to_csv(os.path.join(output_directory, 'archiving_correspondence_redacted.csv'), index=False)
        split_congress_year(md_df, output_directory)
