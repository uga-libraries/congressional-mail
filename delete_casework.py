"""
Draft script to delete casework from the metadata files and the letters themselves for any export type.
Use the metadata files produced by this script for making access copies

Script arguments: path to the folder with the exported content and the export type.
Use the type name from the script (e.g., css_archiving_format)
"""
import os
import sys


def check_arguments(arg_list):
    """Get the path to the exported content and export type supplied as required script arguments"""

    ex_path = None
    ex_type = None
    errors = []

    # Both required arguments are missing (only the script path is present).
    if len(arg_list) == 1:
        errors.append("Missing required arguments, export_path and export_type")

    # At least the first required argument is present.
    # Checks if the first argument is a valid path, and assigns to export_path if so.
    if len(arg_list) > 1:
        if os.path.exists(arg_list[1]):
            ex_path = arg_list[1]
        else:
            errors.append(f"Provided path to export_path does not exist: {arg_list[1]}")

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
        errors.append("Too many arguments provided. Expect two arguments: export_path and export_type")

    return ex_path, ex_type, errors


if __name__ == '__main__':

    # Gets the path to the folder with the data export and the export type from the script arguments.
    # If either are missing or not expected values, prints the error(s) and exits the script.
    export_path, export_type, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # TODO Remove from metadata and produce logs, using export-specific function.

    # TODO Delete the letters based on the deletion log.
