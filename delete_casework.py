"""
Draft script to delete casework from the metadata files and the letters themselves for any export type.
Use the metadata files produced by this script for making access copies

Script arguments: path to the folder with the exported content (input_path) and the export type (export_type).
Use the type name from the script (e.g., css_archiving_format)
"""
import numpy as np
import os
import sys


def check_arguments(arg_list):
    """Get the path to the exported content and export type supplied as required script arguments"""

    in_path = None
    ex_type = None
    errors = []

    # Both required arguments are missing (only the script path is present).
    if len(arg_list) == 1:
        errors.append("Missing required arguments, input_path and export_type")

    # At least the first required argument is present.
    # Checks if the first argument is a valid path, and assigns to input_path if so.
    if len(arg_list) > 1:
        if os.path.exists(arg_list[1]):
            in_path = arg_list[1]
        else:
            errors.append(f"Provided path to input_path does not exist: {arg_list[1]}")

    # Both required arguments are present.
    # Checks if the second argument is one of the expected values, and assigns to export_type if so.
    if len(arg_list) > 2:
        type_list = ['archival_office_correspondence_data', 'cms_data_interchange_format',
                     'css_archiving_format', 'css_data_interchange_format']
        if arg_list[2] in type_list:
            ex_type = arg_list[2]
        else:
            errors.append(f"Provided export_type '{arg_list[2]}' is not an expected export type")

    # More than two arguments are present.
    if len(arg_list) > 3:
        errors.append("Too many arguments provided. Expect two arguments: input_path and export_type")

    return in_path, ex_type, errors


def remove_metadata_archival_office(df, input_dir):
    """Remove metadata rows for casework for the archival_office_correspondence_data type and log the results"""

    # Removes row if any column includes the text "CASE".
    # It is typically within the columns correspondence_topic or comments
    # and includes a few rows that are not really casework, such as "Casey" or his "on the case" catchphrase,
    # which is necessary to protect privacy and keep time required reasonable.
    # Deleted rows are saved to a log for review.
    includes_casework = np.column_stack([df[col].str.contains('CASE', case=False, na=False) for col in df])
    df.loc[includes_casework.any(axis=1)].to_csv(os.path.join(input_dir, 'casework_deletion_log.csv'), index=False)
    df = df.loc[~includes_casework.any(axis=1)]

    return df


def remove_metadata_cms_data(df, input_dir):
    """Remove metadata rows for casework for the cms_data_interchange_format type and log the results"""

    # Rows with "case" in any column are saved to a log for review.
    # We have not found casework in this export type, but this will let us catch it in future donations.
    # This may show us another pattern that indicates casework or may be another use of the word case.
    includes_case = np.column_stack([df[col].str.contains('case', case=False, na=False) for col in df])
    df.loc[includes_case.any(axis=1)].to_csv(os.path.join(input_dir, 'row_includes_case_log.csv'), index=False)

    return df


def remove_metadata_css_archiving(df, input_dir):
    """Remove metadata rows for casework for the css_archiving_format type and log the results"""

    # Removes row if column in_topic includes one of the topics that indicates casework.
    # There may be more than one topic in that column.
    # Deleted rows are saved to a log for review.
    # TODO: combine deleted content into a single log.
    topics_list = ['Casework', 'Casework Issues', 'Prison Case']
    casework_topic = df['in_topic'].str.contains('|'.join(topics_list), na=False)
    df[casework_topic].to_csv(os.path.join(input_dir, 'topic_deletion_log.csv'), index=False)
    df = df[~casework_topic]

    # Removes row if any column includes the text "casework".
    # This removes some rows where the text indicates they are not casework,
    # which is necessary to protect privacy and keep time required reasonable.
    # Deleted rows are saved to a log for review.
    includes_casework = np.column_stack([df[col].str.contains('casework', case=False, na=False) for col in df])
    df.loc[includes_casework.any(axis=1)].to_csv(os.path.join(input_dir, 'casework_anywhere_deletion_log.csv'),
                                                 index=False)
    df = df.loc[~includes_casework.any(axis=1)]

    # Remaining rows with "case" in any column are saved to a log for review.
    # This may show us another pattern that indicates casework or may be another use of the word case.
    includes_case = np.column_stack([df[col].str.contains('case', case=False, na=False) for col in df])
    df.loc[includes_case.any(axis=1)].to_csv(os.path.join(input_dir, 'row_includes_case_log.csv'), index=False)

    return df


def remove_metadata_css_data(df, input_dir):
    """Remove metadata rows for casework for the css_data_interchange_format type and log the results."""

    # Removes row if column group_name starts with "CASE".
    # There are other groups which included "case" that are retained, referring to legal cases of national interest.
    # Deleted rows are saved to a log for review.
    # TODO: combine deleted content into a single log.
    group = df['group_name'].str.startswith('CASE', na=False)
    df[group].to_csv(os.path.join(input_dir, 'group_deletion_log.csv'), index=False)
    df = df[~group]

    # Removes row if any column includes the text "casework".
    # Deleted rows are saved to a log for review.
    includes_casework = np.column_stack([df[col].str.contains('casework', case=False, na=False) for col in df])
    df.loc[includes_casework.any(axis=1)].to_csv(os.path.join(input_dir, 'casework_deletion_log.csv'), index=False)
    df = df.loc[~includes_casework.any(axis=1)]

    # Remaining rows with "case" in any column are saved to a log for review.
    # This may show us another pattern that indicates casework or may be another use of the word case.
    includes_case = np.column_stack([df[col].str.contains('case', case=False, na=False) for col in df])
    df.loc[includes_case.any(axis=1)].to_csv(os.path.join(input_dir, 'row_includes_case_log.csv'), index=False)

    return df


if __name__ == '__main__':

    # Gets the path to the folder with the data export and the export type from the script arguments.
    # If either are missing or not expected values, prints the error(s) and exits the script.
    input_path, export_type, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Removes rows for casework from metadata and produces logs of what is deleted and remaining rows with "case".

    # TODO Delete the letters based on the deletion log.
