"""
Draft script to prepare preservation and access copies from an export in the Archival Office Correspondence Data format.
Required arguments: input_directory (path to the folder with the css export) and script_mode (access or preservation).
"""
from datetime import date
import numpy as np
import os
import pandas as pd
import sys
from css_archiving_format import file_deletion_log


def check_arguments(arg_list):
    """Verify the required script arguments are present and valid and get the path to the metadata file"""

    # Default values for the variables calculated by this function.
    input_dir = None
    md_path = None
    mode = None
    errors = []

    # Both arguments are missing (only the script path is present).
    # Return immediately, or it would also have the error one missing required argument.
    if len(arg_list) == 1:
        errors.append("Missing required arguments, input_directory and script_mode")
        return input_dir, md_path, mode, errors

    # At least the first argument is present.
    # Verifies it is a valid path, and if so that it contains the expected DAT file.
    if len(arg_list) > 1:
        if os.path.exists(arg_list[1]):
            input_dir = arg_list[1]
            if os.path.exists(os.path.join(input_dir, 'archive.dat')):
                md_path = os.path.join(input_dir, 'archive.dat')
            else:
                errors.append(f"No archive.dat file in the input_directory")
        else:
            errors.append(f"Provided input_directory '{arg_list[1]}' does not exist")

    # Both required arguments are present.
    # Verifies the second is one of the expected modes.
    if len(arg_list) > 2:
        if arg_list[2] in ('access', 'preservation', 'test'):
            mode = arg_list[2]
        else:
            errors.append(f"Provided mode '{arg_list[2]}' is not 'access' or 'preservation'")
    else:
        errors.append("Missing one of the required arguments, input_directory or script_mode")

    # More than the expected two required arguments are present.
    if len(arg_list) > 3:
        errors.append("Provided more than the required arguments, input_directory and script_mode")

    return input_dir, md_path, mode, errors


def check_metadata(df, output_dir):
    """This is a quickly made function for looking at the metadata, to decide if it is complete enough to keep
    but needs to be refined if we do keep it"""

    # Tests if all expected columns are present and if there are any unexpected columns.
    column_names = df.columns.tolist()
    expected = ['name', 'title', 'organization', 'address_line_1', 'address_line_2', 'city', 'state_code',
                'zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic',
                'letter_date', 'staffer_initials', 'document_number', 'comments']
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

    # Calculates the number and percentage of blank cells in each column, and saves it all to a CSV.
    blank_count = df.eq('').sum()
    total_rows = len(df.index)
    blank_percent = round((blank_count / total_rows) * 100, 2)
    columns_df = pd.concat([columns_present, blank_count, blank_percent], axis=1)
    columns_df.columns = ['Present', 'Blank_Count', 'Blank_Percent']
    print(columns_df)
    columns_df.to_csv(os.path.join(output_dir, 'usability_report_metadata.csv'), index=True, index_label='Column_Name')

    # Counts the number of each topic
    df['correspondence_topic'] = df['correspondence_topic'].replace('', 'BLANK')
    df_counts = df['correspondence_topic'].value_counts().reset_index()
    df_counts.columns = ['Topic', 'Topic_Count']
    df_counts.to_csv(os.path.join(output_dir, 'topics_report.csv'), index=False)

    # Checking the rows with a possible file name
    blank_count = df['document_number'].eq('').sum()
    doc_num_count = df['document_number'].nunique()
    q_count = df['document_number'].str.startswith('Q').sum()
    with open(os.path.join(output_dir, 'file_names_options.txt'), 'w', newline='') as report:
        report.write(f'Document number blank        : {blank_count}\n')
        report.write(f'Document number unique values: {doc_num_count}\n')
        report.write(f'Comments with Q# (filename?) : {q_count}\n')


def find_casework_rows(df, output_dir):
    """Find metadata rows with topics or text that indicate they are casework,
     return as df and log results"""

    # Column correspondence_type includes the text "case" (case-insensitive).
    corr_type = df['correspondence_type'].str.contains('case', case=False, na=False)
    df_type = df[corr_type]
    df = df[~corr_type]

    # Column correspondence_topic includes the text "case" (case-insensitive).
    corr_topic = df['correspondence_topic'].str.contains('case', case=False, na=False)
    df_topic = df[corr_topic]
    df = df[~corr_topic]

    # Column correspondence_subtopic includes the text "case" (case-insensitive).
    corr_subtopic = df['correspondence_subtopic'].str.contains('case', case=False, na=False)
    df_subtopic = df[corr_subtopic]
    df = df[~corr_subtopic]

    # Column comments includes the text "case" (case-insensitive).
    comments = df['comments'].str.contains('case', case=False, na=False)
    df_comments = df[comments]
    df = df[~comments]

    # Makes a log with any remaining rows with "case" in any column.
    # This may show us another pattern that indicates casework or may be another use of the word case.
    case = np.column_stack([df[col].str.contains('case', case=False, na=False) for col in df])
    if len(df.loc[case.any(axis=1)].index) > 0:
        df.loc[case.any(axis=1)].to_csv(os.path.join(output_dir, 'case_remains_log.csv'), index=False)

    # Makes a single dataframe with all rows that indicate casework
    # and also saves to a log for review for any that are not really casework.
    df_casework = pd.concat([df_type, df_topic, df_subtopic, df_comments], axis=0, ignore_index=True)
    df_casework.to_csv(os.path.join(output_dir, 'case_delete_log.csv'), index=False)
    return df_casework


def read_metadata(path):
    """Read the metadata file into a dataframe"""

    # Makes a list from the file contents with one list per row and one item per column,
    # splitting the data into columns based on the character position and removing extra spaces.
    rows_list = []
    positions = [(0, 39), (39, 69), (69, 99), (99, 129), (129, 159), (159, 189), (189, 191), (191, 201), (201, 251),
                 (251, 301), (301, 351), (351, 357), (357, 361), (361, 371), (371, 471)]
    with open(path) as open_file:
        for line in open_file:
            row_list = [line[slice(*pos)].strip() for pos in positions]
            rows_list.append(row_list)

    # Save as a dataframe, with column names.
    # TODO: verify these column names.
    # TODO: add error handling for if the data is not the expected number of columns?
    columns_list = ['name', 'title', 'organization', 'address_line_1', 'address_line_2', 'city', 'state_code',
                    'zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic',
                    'letter_date', 'staffer_initials', 'document_number', 'comments']
    df = pd.DataFrame(rows_list, columns=columns_list, dtype=str)

    # Removes blank rows, which are present in some of the data exports.
    # Blank rows have an empty string in every column.
    # Source: Microsoft Copilot
    df = df[~(df == '').all(axis=1)]

    return df


def remove_casework_rows(df, df_case):
    """Remove metadata rows with topics or text that indicate they are casework and return the updated df"""

    # Makes an updated dataframe with just rows in df that are not in df_case.
    df_merge = df.merge(df_case, how='left', indicator=True)
    df_update = df_merge[df_merge['_merge'] == 'left_only'].drop(columns=['_merge'])

    return df_update


def remove_casework_letters(input_dir):
    """Remove casework letters received from constituents (no individual letters sent back by the office)"""

    # Reads the deletion log into a dataframe, which is in the parent folder of input_dir if it is present.
    # If it is not, there are no files to delete.
    try:
        df = pd.read_csv(os.path.join(os.path.dirname(input_dir), 'case_delete_log.csv'))
    except FileNotFoundError:
        print(f"No deletion log in {os.path.dirname(input_dir)}")
        return

    # Deletes letters received, based on the document name in the comments column, if any.
    # If there is a document name, it is formatted "Q# optional text", referring to a file named #.txt.
    comments_df = df.dropna(subset=['comments']).copy()
    q_df = comments_df[comments_df['comments'].str.startswith('Q')].copy()
    q_list = q_df['comments'].tolist()
    if len(q_list) > 0:

        # Creates a file deletion log, with a header row.
        log_path = os.path.join(os.path.dirname(input_dir),
                                f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv")
        file_deletion_log(log_path, None, 'header')

        for q_number in q_list:
            # Change "text" to match the folder name in the export which contains the letters, if different.
            q_number = q_number.split(' ')[0]
            file_path = os.path.join(input_dir, 'text', f"{q_number.replace('Q', '')}.txt")
            try:
                file_deletion_log(log_path, file_path, 'Casework')
                os.remove(file_path)
            except FileNotFoundError:
                file_deletion_log(log_path, file_path, note='Cannot delete: FileNotFoundError')


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed. Includes names and address information.
    # TODO: confirm this list
    remove = ['name', 'title', 'organization', 'address_line_1', 'address_line_2']

    # Removes every column on the remove list from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    df = df.drop(remove, axis=1, errors='ignore')

    return df


def split_congress_year(df, output_dir):
    """Make one CSV per Congress Year"""

    # Saves rows without a year (date is a not a number, could be blank or text) to a CSV, if any.
    df_undated = df[pd.to_numeric(df['letter_date'], errors='coerce').isnull()]
    if len(df_undated.index) > 0:
        df_undated.to_csv(os.path.join(output_dir, 'undated.csv'), index=False)

    # Removes rows without a year from the dataframe, so the rest can be split by Congress Year.
    df = df[pd.to_numeric(df['letter_date'], errors='coerce').notnull()].copy()

    # Adds a column with the year received, which will be used to calculate the Congress Year.
    # Column letter_date is formatted YYMMDD.
    # First the two digit year is extracted, and then it is made a four-digit year by adding 1900 or 2000.
    df.loc[:, 'year'] = df['letter_date'].astype(str).str[:2].astype(int)
    df.loc[df['year'] >= 60, 'year'] = df['year'] + 1900
    df.loc[df['year'] < 60, 'year'] = df['year'] + 2000

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

    # # Finds rows in the metadata that are for casework and saves to a CSV.
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
        md_df.to_csv(os.path.join(output_directory, 'archive_redacted.csv'), index=False)
        split_congress_year(md_df, output_directory)

    if script_mode == 'test':
        check_metadata(md_df, output_directory)
