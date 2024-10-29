"""
Draft script to prepare access copies from an export in the CSS Archiving Format.
"""
import os
import pandas as pd
import sys


def check_argument(arg_list):
    """Verify the required script argument is present and a valid path"""

    # Argument is missing (only the script path is present).
    if len(arg_list) == 1:
        return None, "Missing required argument: path to the metadata file"
    # Argument is present but not a valid path.
    elif not os.path.exists(arg_list[1]):
        return None, f"Provided path does not exist: {arg_list[1]}"
    # Argument is correct.
    else:
        return arg_list[1], None


def read_metadata(path):
    """Read the metadata file into a dataframe

    This does not need to stay a function if it ends up being one line,
    but is for now to make it easier to test error handling.
    """
    # TODO: document ParserError?. Rows that are printed by on_bad_lines='warn' are not included in the output.
    # TODO: document the encoding errors?
    df = pd.read_csv(path, delimiter='\t', dtype=str, encoding_errors='ignore', on_bad_lines='warn')

    # TODO: delete. This is a temporary indicator for testing if anything was read to the dataframe.
    # print("Rows in the dataframe:", len(df.index))

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
    
    return df


def save_df(df, input_dir):
    """Make one CSV with all data in the folder with the original metadata file"""

    # Removes blank rows, which are present in some of the data exports.
    df.dropna(how='all', inplace=True)

    # Saves the dataframe to a CSV.
    # TODO: decide on file name and where it saves.
    # TODO: confirm using CSV format.
    df.to_csv(os.path.join(input_dir, 'Access_Copy.csv'), index=False)


def split_congress_year(df, input_dir):
    """Make one CSV per Congress Year in the folder with the original metadata file"""

    # Saves rows without a year (date is a not a number, could be blank or text) to a CSV.
    # TODO: confirm that text in place of date should be in undated: usually an error in the number of columns.
    # TODO: confirm if should have a maximum size, for ones that are still too large to open in a spreadsheet.
    # TODO: decide on file name and where it saves.
    df_undated = df[pd.to_numeric(df['in_date'], errors='coerce').isnull()]
    df_undated.to_csv(os.path.join(input_dir, 'undated.csv'), index=False)

    # Removes rows without a year from the dataframe, so the rest can be split by Congress Year.
    df = df[pd.to_numeric(df['in_date'], errors='coerce').notnull()].copy()

    # Adds a column with the year received, which will be used to calculate the Congress Year.
    # Column in_date is formatted YYYYMMDD.
    # TODO: confirm that in_date is the correct date for this purpose. Also have out_date.
    df.loc[:, 'year'] = df['in_date'].astype(str).str[:4].astype(int)

    # Adds a column with the Congress Year received, which is a two-year range starting with an odd year.
    # First, if the year received is even, the Congress Year is year-1 to year.
    # Second, if the year received is odd, the Congress Year is year to year+1.
    df.loc[df['year'] % 2 == 0, 'congress_year'] = (df['year'] - 1).astype(str) + '-' + df['year'].astype(str)
    df.loc[df['year'] % 2 == 1, 'congress_year'] = df['year'].astype(str) + '-' + (df['year'] + 1).astype(str)

    # Splits the data by Congress Year received and saves each to a separate CSV.
    # The year and congress_year columns are first removed, so the CSV only has the original columns.
    # TODO: decide on file name and where it saves.
    # TODO: confirm using CSV format.
    for congress_year, cy_df in df.groupby('congress_year'):
        cy_df = cy_df.drop(['year', 'congress_year'], axis=1)
        cy_df.to_csv(os.path.join(input_dir, f'{congress_year}.csv'), index=False)


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

    # Saves the redacted data to a CSV file in the folder with the original metadata file.
    save_df(md_df, os.path.dirname(md_path))

    # Saves a copy of the redacted data to one CSV per Congress Year in the folder with the original metadata file.
    split_congress_year(md_df, os.path.dirname(md_path))
