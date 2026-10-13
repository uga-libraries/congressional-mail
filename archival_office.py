"""
Draft script to prepare preservation and access copies from an export in the Archival Office Correspondence Data format.

Required arguments:
metadata_path (path to the archive.date file)
output_directory (path to the folder where script ouputs are saved)
"""
import os
import pandas as pd
import sys


def check_blanks(df, output_dir):
    """Make a report with the number and percentage of blank cells in each column"""
    blank_count = df.eq('').sum()
    total_rows = len(df.index)
    blank_percent = round((blank_count / total_rows) * 100, 2)
    columns_df = pd.concat([blank_count, blank_percent], axis=1)
    columns_df.columns = ['Blank_Count', 'Blank_Percent']
    columns_df.to_csv(os.path.join(output_dir, 'metadata_review_blanks.csv'), index=True, index_label='Column_Name')

def check_documents(df, output_dir):
    """Make a report with the number of occurrences per document_id"""
    df['document_number'] = df['document_number'].replace('', 'BLANK')
    df_counts = df['document_number'].value_counts().reset_index()
    df_counts.columns = ['Document_Number', 'Document_Number_Count']
    df_counts.to_csv(os.path.join(output_dir, 'metadata_review_document_number.csv'), index=False)

def check_topics(df, output_dir):
    """Make a report with the number of occurrences per topic"""
    df['correspondence_topic'] = df['correspondence_topic'].replace('', 'BLANK')
    df_counts = df['correspondence_topic'].value_counts().reset_index()
    df_counts.columns = ['Topic', 'Topic_Count']
    df_counts.to_csv(os.path.join(output_dir, 'metadata_review_topics.csv'), index=False)

def read_metadata(md_path):
    """Read the metadata file into a dataframe"""

    # Reads the metadata into a list of lists, with one list per row,
    # splitting each row into one item per column based on the character position and removing extra spaces.
    rows_list = []
    positions = [(0, 39), (39, 69), (69, 99), (99, 129), (129, 159), (159, 189), (189, 191), (191, 201), (201, 251),
                 (251, 301), (301, 351), (351, 357), (357, 361), (361, 371), (371, 471)]
    with open(md_path) as open_file:
        for line in open_file:
            row_list = [line[slice(*pos)].strip() for pos in positions]
            rows_list.append(row_list)

    # Saves as a dataframe, with column names.
    columns_list = ['name', 'title', 'organization', 'address_line_1', 'address_line_2', 'city', 'state_code',
                    'zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic',
                    'letter_date', 'staffer_initials', 'document_number', 'comments']
    df = pd.DataFrame(rows_list, columns=columns_list, dtype=str)

    # Removes blank rows, which have an empty string in every column.
    df = df[~(df == '').all(axis=1)]

    return df


if __name__ == '__main__':

    # Gets the script arguments.
    metadata_path = sys.argv[1]
    output_directory = sys.argv[2]

    # Reads the metadata file into a pandas dataframe and saves as a csv.
    md_df = read_metadata(metadata_path)
    md_df.to_csv(os.path.join(output_directory, 'archive_metadata.csv'), index=False)

    # Creates reports to summarize the metadata.
    check_blanks(md_df, output_directory)
    check_documents(md_df, output_directory)
    check_topics(md_df, output_directory)
