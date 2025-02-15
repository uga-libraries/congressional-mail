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


def file_deletion_log(log_path, file_path, header=False, note=None):
    """Make or update the file deletion log, so data is saved as soon as a file is deleted
    Modelled after https://github.com/uga-libraries/accessioning-scripts/blob/main/technical-appraisal-logs.py"""

    # Makes a new log with a header row.
    # If a file already exists with this name, it will be overwritten.
    if header is True:
        with open(log_path, 'w', newline='') as log:
            log_writer = csv.writer(log)
            log_writer.writerow(['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'])

    # Adds a row for a file that could not be deleted to an existing log.
    elif note:
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
            log_writer.writerow([file_path, size_kb, date_c, date_d, md5, 'casework'])


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


def find_casework_rows(df, output_dir):
    """Find metadata rows with topics or text that indicate they are casework,
     return as a df and log results"""

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

    # Makes a log with any remaining rows with "case" in any column.
    # This may show us another pattern that indicates casework or may be another use of the word case.
    case = np.column_stack([df[col].str.contains('case', case=False, na=False) for col in df])
    if len(df.loc[case.any(axis=1)].index) > 0:
        df.loc[case.any(axis=1)].to_csv(os.path.join(output_dir, 'case_remains_log.csv'), index=False)

    # Makes a single dataframe with all rows that indicate casework
    # and also saves to a log for review for any that are not really casework.
    df_casework = pd.concat([df_topic, df_cw, df_phrase], axis=0, ignore_index=True)
    df_casework.to_csv(os.path.join(output_dir, 'case_delete_log.csv'), index=False)
    return df_casework


def remove_casework_rows(df, df_case):
    """Remove metadata rows with topics or text that indicate they are casework and return the updated df"""

    # Makes an updated dataframe with just rows in df that are not in df_case.
    df_merge = df.merge(df_case, how='left', indicator=True)
    df_update = df_merge[df_merge['_merge'] == 'left_only'].drop(columns=['_merge'])

    return df_update


def remove_casework_letters(input_dir):
    """Remove casework letters received from constituents and individual casework letters sent back by the office"""

    # Reads the case delete log into a dataframe, which is in the parent folder of input_dir if it is present.
    # If it is not, there are no files to delete.
    try:
        df = pd.read_csv(os.path.join(os.path.dirname(input_dir), 'case_delete_log.csv'))
    except FileNotFoundError:
        print(f"No case delete log in {os.path.dirname(input_dir)}")
        return

    # Creates a file deletion log, with a header row.
    log_path = os.path.join(os.path.dirname(input_dir), f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv")
    file_deletion_log(log_path, None, True)

    # Deletes letters received based on in_document_name.
    # If there is a document name, it is formatted ..\documents\BlobExport\objects\filename.txt
    in_doc_df = df.dropna(subset=['in_document_name']).copy()
    in_doc_list = in_doc_df['in_document_name'].tolist()
    for name in in_doc_list:
        file_path = name.replace('..', input_dir)
        try:
            file_deletion_log(log_path, file_path)
            os.remove(file_path)
        except FileNotFoundError:
            file_deletion_log(log_path, file_path, note='Cannot delete: FileNotFoundError')

    # Deletes individual letters (not form letters) sent based on out_document_name.
    out_doc_df = df.dropna(subset=['out_document_name']).copy()
    out_doc_list = out_doc_df['out_document_name'].tolist()
    for name in out_doc_list:
        # Paths for formletters include the folder "formletter" or "form".
        if 'form' not in name:
            # Make an absolute path from name, which starts ..\documents or \\name-office\dos.
            if name.startswith('..'):
                file_path = name.replace('..', input_dir)
            else:
                file_path = re.sub('\\\\\\\\[a-z]+-[a-z]+', '', name)
                file_path = input_dir + file_path
            # Only delete if it is a file. Sometimes, out_document_name has the path to a folder instead.
            if os.path.isfile(file_path):
                file_deletion_log(log_path, file_path)
                os.remove(file_path)
            elif not os.path.exists(file_path):
                file_deletion_log(log_path, file_path, note='Cannot delete: FileNotFoundError')


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed. Includes names and address information.
    remove = ['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
              'addr1', 'addr2', 'addr3', 'addr4']

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

    # Finds rows in the metadata that are for casework and saves to a CSV.
    casework_df = find_casework_rows(md_df, output_directory)

    # For preservation, deletes the casework files, which is an appraisal decision.
    # It uses the log from find_casework_rows() to know what to delete.
    if script_mode == 'preservation':
        remove_casework_letters(input_directory)

    # For access, removes rows for casework and columns with PII from the metadata
    # and makes a copy of the data split by congress year.
    if script_mode == 'access':
        md_df = remove_casework_rows(md_df, casework_df)
        md_df = remove_pii(md_df)
        md_df.to_csv(os.path.join(output_directory, 'archiving_correspondence_redacted.csv'), index=False)
        split_congress_year(md_df, output_directory)
