"""
Temporary script to determine how many of the non-casework letters match the exported metadata,
finding letters just in the metadata and letters just in the directory.
Using check_arguments to get metadata path(s), even though don't need script mode otherwise.
Nothing is deleted, so this can be run on the original accession.
If decide to keep, will need to generalize more.

THIS IS UNTESTED
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


def compare_cms_dif(df_dir, df_md, input_dir):
    """Log differences between metadata and directory contents"""

    # Compare paths and save differences (metadata only and directory only) to a log.
    compare = df_dir.merge(df_md, how='outer', indicator=True)

    metadata_only = compare[compare['_merge'] == 'right_only']
    metadata_only = metadata_only.drop('_merge', axis=1)
    metadata_only.to_csv(os.path.join(os.path.dirname(input_dir), 'metadata_only.csv'), index=False)

    dir_only = compare[compare['_merge'] == 'left_only']
    dir_only = dir_only.drop('_merge', axis=1)
    dir_only.to_csv(os.path.join(os.path.dirname(input_dir), 'directory_only.csv'), index=False)

    # Print a summary of the results.
    counts = compare['_merge'].value_counts()
    total = len(compare.index)
    print(f"Out of {total} files in the metadata and/or directory:")
    print(f"{counts['right_only']} ({round(counts['right_only'] / total * 100, 2)}%) were just in the metadata,")
    print(f"{counts['left_only']} ({round(counts['left_only'] / total * 100, 2)}%) were just in the directory,")
    print(f"and {counts['both']} ({round(counts['both'] / total * 100, 2)}%) matched")


def directory_df(parent_dir, col_name):
    """Make df with relative path from folder within parent_dir to every file,
    using the same column name as the metadata"""
    paths = []
    for folder in os.listdir(parent_dir):
        for file in os.listdir(os.path.join(parent_dir, folder)):
            paths.append(os.path.join(folder, file))
    df = pd.DataFrame(paths, columns=[col_name])
    return df


if __name__ == '__main__':

    # CMS Data Interchange Format
    input_directory, metadata_paths_dict, script_mode, errors_list = cms_dif.check_arguments(sys.argv)
    md_df = cms_dif.read_metadata(metadata_paths_dict)
    df_dir = directory_df(os.path.join(input_directory, 'documents', 'documents'), 'correspondence_document_name')
    df_md = md_df['correspondence_document_name'].drop_duplicates().dropna().copy()
    compare_cms_dif(df_dir, df_md, input_directory)
