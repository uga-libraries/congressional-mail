"""
Get the metadata rows for files that will be restricted based on review of folders instead of metadata.
Initially developing this with css data interchange format.

Arguments: path to the export (input_directory) and folder with files to restrict (restrict_directory)
Returns: additiona_restrictions.csv in parent folder of the input directory
"""
import os
import pandas as pd
import sys
from css_data_interchange_format import read_metadata


def metadata_paths(input_dir):
    """Get paths of the four DAT files in the input directory and return as a dictionary"""
    # Before this script is run, would already know these files are in the expected location.
    md_paths = {'1B':os.path.join(input_dir,'out_1B.dat'),
                '2A':os.path.join(input_dir,'out_2A.dat'),
                '2C':os.path.join(input_dir,'out_2C.dat'),
                '2D':os.path.join(input_dir,'out_2D.dat')}
    return md_paths


def make_restrict_list(restrict_dir):
    """Get names of all files in the restriction directory"""
    restrict = []
    for file in os.listdir(restrict_dir):
        restrict.append(file)
    return restrict


if __name__ == '__main__':

    # Variables from script arguments.
    input_directory = sys.argv[1]
    restrict_directory = sys.argv[2]
    output_directory = os.path.dirname(restrict_directory)

    # Read the metadata, including merging tables.
    # Calculate metadata paths and import functions from css_data_interchange_format.py
    metadata_paths_dict = metadata_paths(input_directory)
    md_df = read_metadata(metadata_paths_dict)

    # Get list of filenames to restrict.
    # Convert to paths to match the metadata.
    restrict_list = make_restrict_list(restrict_directory)

    # Find metadata row(s) matching the each path, if any.

    # Save to additional_restrictions.csv