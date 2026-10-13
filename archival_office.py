"""
Draft script to prepare preservation and access copies from an export in the Archival Office Correspondence Data format.

Required arguments:
metadata_path (path to the archive.date file)
output_directory (path to the folder where script ouputs are saved)
"""
import os
import pandas as pd
import sys


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

    # Gets the script arguments
    metadata_path = sys.argv [1]
    output_directory = sys.argv [2]

    # Reads the metadata file into a pandas dataframe.
    md_df = read_metadata(metadata_path)
    md_df.to_csv(os.path.join(output_directory, 'archive.csv'), index=False)

    check_metadata(md_df, output_directory)
