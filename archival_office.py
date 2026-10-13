"""
Draft script to prepare preservation and access copies from an export in the Archival Office Correspondence Data format.
Required arguments: input_directory (path to the folder with the css export) and script_mode (access or preservation).
"""
import os
import pandas as pd
import sys


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

    # For access, removes rows for casework and columns with PII from the metadata
    # and makes a copy of the data split by congress year.
    if script_mode == 'access':
        md_df.to_csv(os.path.join(output_directory, 'archive_redacted.csv'), index=False)

    if script_mode == 'test':
        check_metadata(md_df, output_directory)
