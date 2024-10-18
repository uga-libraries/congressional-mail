"""
Draft script to update the metadata file from an export in the CSS Archiving Format to make it more usable.
"""
import os
import pandas as pd
import sys


def check_argument(arg_list):
    """Verify the required script argument is present and a valid path"""

    # Argument is missing (only the script path is present).
    if len(arg_list) == 1:
        return None, "Missing required argument: path to the metadata file"
    elif not os.path.exists(arg_list[1]):
        return None, f"Provided path does not exist: {arg_list[1]}"
    else:
        return arg_list[1], None


def read_metadata(path):
    """Read the metadata file into a dataframe"""
    # TODO: fix ParserError. Need to add nrows=1000 to read_csv to get it to read without errors
    # TODO: document the encoding errors?

    # This is a temporary workaround (only gets first 1000 rows) to avoid the first row with errors.
    df = pd.read_csv(path, delimiter='\t', nrows=1000, encoding_errors='ignore')
    print(df.head)

    # This will print the rows that have problems and skip them.
    # Non-error rows are read into the dataframe.
    # df = pd.read_csv(path, delimiter='\t', encoding_errors='ignore', on_bad_lines='warn')

    # This will just skip the rows that have problems.
    # Non-error rows are read into the dataframe.
    # df = pd.read_csv(path, delimiter='\t', encoding_errors='ignore', on_bad_lines='skip')

    # This will save all 4 data rows from the test but the last few columns it prints are blank.
    # TODO: save this to a CSV so I can look at all the data.
    # df = pd.read_csv(path, delimiter='\t+', encoding_errors='ignore', engine='python')

    # This is a temporary indicator for if anything was read to the dataframe.
    # print("Rows in the dataframe:", len(df.index))
    # print(df)
    return df


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed. Includes names and address information.
    # TODO: confirm this list
    remove = ['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
              'addr1', 'addr2', 'addr3', 'addr4']

    # Removes every column on the remove list from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    df = df.drop(remove, axis=1, errors='ignore')

    # Prints the remaining columns for archivist review, in case any additional ones might contain private information.
    # TODO: confirm this is desired
    print("\nColumns remaining after removing personal identifiers are listed below.")
    print("To remove any of these columns, add them to the 'remove' list in remove_pii() and run the script again.")
    for column_name in df.columns.tolist():
        print(f'\t{column_name}')
    
    return df


if __name__ == '__main__':

    # Gets the path to the metadata file from the script argument.
    # If it is missing or not a valid path, prints an error and exits the script.
    md_path, error_message = check_argument(sys.argv)
    if error_message:
        print(error_message)
        sys.exit(1)

    # Reads the metadata file into a pandas dataframe.
    md_df = read_metadata(md_path)

    # Removes columns with personally identifiable information, if they are present.
    md_df = remove_pii(md_df)

