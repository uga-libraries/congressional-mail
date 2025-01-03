"""
Temporary script to determine how many of the non-casework letters match the exported metadata.
Using check_arguments to get metadata path(s), even though don't need script mode otherwise.
Nothing is deleted, so this can be run on the original accession.
If decide to keep, will need to generalize more.
"""
import csv
import os
import re
import sys
import css_archiving_format as css_a
import cms_data_interchange_format as cms_dif
import css_data_interchange_format as css_dif
import archival_office_correspondence_data as ao


def log(input_dir, row_data):
    log_path = os.path.join(os.path.dirname(input_dir), 'match_log.csv')
    with open(log_path, 'w', newline='') as log_csv:
        log_writer = csv.writer(log_csv)
        log_writer.writerow(row_data)


def match_css_archiving(df, input_dir):
    """Log every file and print totals"""
    files = 0
    matches = 0
    log(input_dir, ['Found', 'Path'])

    # Letters received by the office.
    in_doc_df = df.dropna(subset=['in_document_name']).copy()
    in_doc_list = in_doc_df['in_document_name'].tolist()
    for name in in_doc_list:
        files += 1
        file_path = name.replace('..', input_dir)
        if os.path.exists(file_path):
            log(input_dir, [True, file_path])
            matches += 1
        else:
            log(input_dir, [False, file_path])

    # Letters sent by the office.
    out_doc_df = df.dropna(subset=['out_document_name']).copy()
    out_doc_list = out_doc_df['out_document_name'].tolist()
    for name in out_doc_list:
        files += 1
        if name.startswith('..'):
            file_path = name.replace('..', input_dir)
        else:
            file_path = re.sub('\\\\\\\\[a-z]+-[a-z]+', '', name)
            file_path = input_dir + file_path
        if os.path.exists(file_path):
            log(input_dir, [True, file_path])
            matches += 1
        else:
            log(input_dir, [False, file_path])

    # Print summary
    match_percent = round(matches / files * 100, 2)
    print(f"Out of {files} files in the metadata, {match_percent}% ({matches}) were in the export")


def match_cms_dif(df, input_dir):
    """Log every file and print totals"""
    matches = 0
    log(input_dir, ['Found', 'Path'])

    doc_df = df.dropna(subset=['correspondence_document_name']).copy()
    doc_list = doc_df['correspondence_document_name'].unique().tolist()
    for name in doc_list:
        file_path = os.path.join(input_dir, 'documents', 'documents', name)
        if os.path.exists(file_path):
            log(input_dir, [True, file_path])
            matches += 1
        else:
            log(input_dir, [False, file_path])

    files = len(doc_list)
    match_percent = round(matches / files * 100, 2)
    print(f"Out of {files} files in the metadata, {match_percent}% ({matches}) were in the CMS DIF export")


def match_css_dif(df, input_dir):
    """Log every file and print totals"""
    files = 0
    matches = 0
    log(input_dir, ['Found', 'Path'])

    doc_df = df.dropna(subset=['communication_document_name']).copy()
    doc_list = doc_df['communication_document_name'].tolist()
    for name in doc_list:
        files += 1
        file_path = name.replace('..', input_dir)
        if os.path.exists(file_path):
            log(input_dir, [True, file_path])
            matches += 1
        else:
            log(input_dir, [False, file_path])

    match_percent = round(matches / files * 100, 2)
    print(f"Out of {files} files in the metadata, {match_percent}% ({matches}) were in the export")


if __name__ == '__main__':

    # # CSS Archiving Format
    # input_directory, metadata_path, script_mode, errors_list = css_a.check_arguments(sys.argv)
    # md_df = css_a.read_metadata(metadata_path)
    # md_df = css_a.remove_casework(md_df, os.path.dirname(input_directory))
    # match_css_archiving(md_df, input_directory)

    # CMS Data Interchange Format
    input_directory, metadata_paths_dict, script_mode, errors_list = cms_dif.check_arguments(sys.argv)
    md_df = cms_dif.read_metadata(metadata_paths_dict)
    match_cms_dif(md_df, input_directory)

    # # CSS Data Interchange Format
    # input_directory, metadata_paths_dict, script_mode, errors_list = css_dif.check_arguments(sys.argv)
    # md_df = css_dif.read_metadata(metadata_paths_dict)
    # md_df = css_dif.remove_casework(md_df, os.path.dirname(input_directory))
    # match_css_dif(md_df, input_directory)
