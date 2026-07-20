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


def make_df(path):
    """Makes df with all columns blank except the communication_document_name
    to document restricted files with no metadata"""
    column_names = ['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                    'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                    'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                    'file_name', 'text']
    df = pd.DataFrame([['', '', '', '', '', '', '', '', '', '', '', '', '', '', path, '', '', '', '']],
                      columns=column_names)
    return df


def make_restrict_list(restrict_dir):
    """Get names of all files in the restriction directory"""
    restrict = []
    for file in os.listdir(restrict_dir):
        restrict.append(file)
    return restrict


def save(output_dir, df):
    """Save a df with restricted rows to a CSV, which may already exist"""
    csv_path = os.path.join(output_dir, 'additional_restrictions.csv')
    if os.path.exists(csv_path):
        df.to_csv(csv_path, header=False, index=False, mode='a')
    else:
        df.to_csv(csv_path, header=True, index=False)


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
    for restrict_file in restrict_list:
        restrict_path = f'..\\documents\\imail\\{restrict_file}'

        # Find metadata row(s) matching the each path, if any, or make a df with just the document if not.
        # Even if there is no metadata row, we want a record that this file was restricted.
        restrict_df = md_df[md_df['communication_document_name'] == restrict_path]
        if len(restrict_df) == 0:
            restrict_df = make_df(restrict_path)

        # Save to additional_restrictions.csv.
        save(output_directory, restrict_df)
