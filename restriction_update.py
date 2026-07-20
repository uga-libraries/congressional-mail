"""
Get the metadata rows for files that will be restricted based on review of folders instead of metadata.
Initially developing this with css data interchange format.

Arguments: path to the export (input_directory) and folder with files to restrict (restrict_directory)
Returns: additiona_restrictions.csv in parent folder of the input directory
"""
import os
import sys


if __name__ == '__main__':

    # Variables from script arguments.
    input_directory = sys.argv[1]
    restrict_directory = sys.argv[2]
    output_directory = os.path.dirname(restrict_directory)

    # Read the metadata, including merging tables.
    # Calculate metadata paths and import functions from css_data_interchange_format.py

    # Get list of filenames to restrict.
    # Convert to paths to match the metadata.

    # Find metadata row(s) matching the each path, if any.

    # Save to additional_restrictions.csv