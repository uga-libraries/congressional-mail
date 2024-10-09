"""
Draft script to update the metadata file from a css/cms export to make it more usable.
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


def remove_pii(df):
    """Remove columns with personally identifiable information (name and address) if they are present"""

    # List of column names that should be removed. Includes names and address information.
    # TODO: confirm this list
    remove = ['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
              'addr1', 'addr2', 'addr3', 'addr4', 'city', 'state']

    # Removes every column on the remove list from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    df = df.drop(remove, axis=1, errors="ignore")
    
    return df


if __name__ == '__main__':

    # Gets the path to the metadata file from the script argument.
    # If it is missing or not a valid path, prints an error and exits the script.
    md_path, error_message = check_argument(sys.argv)
    if error_message:
        print(error_message)
        sys.exit(1)

    # Reads the metadata file into a pandas dataframe.
    # TODO: limiting the number of rows for testing to avoid a ParserError within the data
    # TODO: document the encoding errors?
    md_df = pd.read_csv(md_path, delimiter="\t", nrows=1000, encoding_errors="ignore")

    # Removes columns with personally identifiable information, if they are present.
    md_df = remove_pii(md_df)

    # Prints the remaining columns for archivist review, in case any additional ones might contain private information.
    # TODO: confirm this is desired
    print("\nColumns remaining in the constituent mail metadata after removing personal identifiers are listed below.")
    print("To remove any of these columns from the metadata, add them to the 'remove' list and run the script again.")
    for column_name in md_df.columns.tolist():
        print(f'\t{column_name}')

