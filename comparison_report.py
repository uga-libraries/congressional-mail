"""
Temporary script to determine how many of the non-casework letters match the exported metadata,
finding letters just in the metadata and letters just in the directory.
Whereas letter_match_report.py was my first try, and it only checked if letters in the metadata were in the directory.

Comment out the other export types in main before running.
Using check_arguments to get metadata path(s), even though don't need script mode otherwise.
Nothing is deleted, so this can be run on the original accession.
"""
import csv
import os
import pandas as pd
import re
import sys
import css_archiving_format as css_a
import cms_data_interchange_format as cms_dif
import css_data_interchange_format as css_dif
import archival_office_correspondence_data as ao


def compare(df_dir, df_md, input_dir):
    """Log differences between metadata and directory contents"""

    # Compare paths and save differences (metadata only and directory only) to logs.
    compare_df = df_dir.merge(df_md, how='outer', indicator=True)

    metadata_only = compare_df[compare_df['_merge'] == 'right_only']
    metadata_only = metadata_only.drop('_merge', axis=1)
    metadata_only.to_csv(os.path.join(os.path.dirname(input_dir), 'metadata_only.csv'), index=False)

    dir_only = compare_df[compare_df['_merge'] == 'left_only']
    dir_only = dir_only.drop('_merge', axis=1)
    dir_only.to_csv(os.path.join(os.path.dirname(input_dir), 'directory_only.csv'), index=False)

    # Print a summary of the results.
    counts = compare_df['_merge'].value_counts()
    total = len(compare_df.index)
    print(f"Out of {total} files in the metadata and/or directory:")
    print(f"{counts['right_only']} ({round(counts['right_only'] / total * 100, 2)}%) were just in the metadata,")
    print(f"{counts['left_only']} ({round(counts['left_only'] / total * 100, 2)}%) were just in the directory,")
    print(f"and {counts['both']} ({round(counts['both'] / total * 100, 2)}%) matched")


def directory_df(parent_dir, col_name, start=None):
    """Make df with relative path from folder within parent_dir to every file,
    with the option of adding the same text to the beginning of all paths (start),
    using the same column name as the metadata"""
    paths = []
    for folder in os.listdir(parent_dir):
        for file in os.listdir(os.path.join(parent_dir, folder)):
            file_path = os.path.join(folder, file)
            if start:
                file_path = os.path.join(start, file_path)
            paths.append(file_path)
    df = pd.DataFrame(paths, columns=[col_name])
    return df


def multi_level_directory_df(parent_dir, col_name):
    """Make df with relative path from parent dir where file can be any level within that,
    using the same column name as the metadata"""
    paths = []
    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            paths.append(os.path.join(root, file))
    df = pd.DataFrame(paths, columns=[col_name])
    return df


def multi_column_metadata(df, input_dir, export):
    """Make metadata df combining columns in_document_name and out_document_name, with edits"""
    if export == 'documents':
        df = df.replace('BlobExport', 'blobexport', regex=True)
    in_doc = df['in_document_name'].drop_duplicates().dropna().copy()
    if export == 'dos':
        df['out_document_name'] = df['out_document_name'].replace('\\\\\\\\[a-z]+-[a-z]+',
                                                                  re.escape(input_dir), regex=True)
    out_doc = df['out_document_name'].drop_duplicates().dropna().copy()
    combined = pd.concat([in_doc, out_doc])
    combined_df = combined.to_frame(name='doc_name')
    return combined_df


if __name__ == '__main__':

    # # CMS Data Interchange Format
    # input_directory, metadata_paths_dict, script_mode, errors_list = cms_dif.check_arguments(sys.argv)
    # md_df = cms_dif.read_metadata(metadata_paths_dict)
    # dir_df = directory_df(os.path.join(input_directory, 'documents', 'documents'), 'correspondence_document_name')
    # md = md_df['correspondence_document_name'].drop_duplicates().dropna().copy()
    # compare(dir_df, md, input_directory)

    # # CSS Data Interchange Format
    # input_directory, metadata_paths_dict, script_mode, errors_list = css_dif.check_arguments(sys.argv)
    # md_df = css_dif.read_metadata(metadata_paths_dict)
    # md_df = css_dif.remove_casework(md_df, os.path.dirname(input_directory))
    # dir_df = directory_df(os.path.join(input_directory, 'documents', 'blobexport'),
    #                       'communication_document_name',
    #                       os.path.join('..', 'documents'))
    # md = md_df['communication_document_name'].drop_duplicates().dropna().copy()
    # compare(dir_df, md, input_directory)

    # # CSS Archiving Format: dos folder
    # input_directory, metadata_path, script_mode, errors_list = css_a.check_arguments(sys.argv)
    # md_df = css_a.read_metadata(metadata_path)
    # md_df = css_a.remove_casework(md_df, os.path.dirname(input_directory))
    # dir_df = multi_level_directory_df(os.path.join(input_directory, 'dos'), 'doc_name')
    # md = multi_column_metadata(md_df, input_directory, 'dos')
    # compare(dir_df, md, input_directory)

    # CSS Archiving Format: documents folder
    input_directory, metadata_path, script_mode, errors_list = css_a.check_arguments(sys.argv)
    md_df = css_a.read_metadata(metadata_path)
    md_df = css_a.remove_appraisal_rows(md_df, os.path.dirname(input_directory))
    dir_df = directory_df(os.path.join(input_directory, 'documents', 'blobexport'),
                          'doc_name', os.path.join('..', 'documents', 'blobexport'))
    md = multi_column_metadata(md_df, input_directory, 'documents')
    compare(dir_df, md, input_directory)
