"""
Draft script to update the metadata file from a css/cms export to make it more usable.
"""
import pandas as pd
import sys

if __name__ == '__main__':
    # Gets the path to the metadata file from the script argument.
    # TODO: error checking
    md_path = sys.argv[1]

    # Reads the metadata file into a pandas dataframe.
    # TODO: limiting the number of rows for testing to avoid a ParserError within the data
    # TODO: document the encoding errors?
    df = pd.read_csv(md_path, delimiter="\t", nrows=1000, encoding_errors="ignore")

    # Removes the personal identifying columns from the dataframe, if they are present.
    # Nothing happens, due to errors="ignore", if any are not present.
    remove = ['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
              'addr1', 'addr2', 'addr3', 'addr4', 'city', 'state']
    df = df.drop(remove, axis=1, errors="ignore")

    # Prints the remaining columns for archivist review, in case any additional ones might contain private information.
    print("\nColumns remaining in the constituent mail metadata after removing personal identifiers are listed below.")
    print("To remove any of these columns from the metadata, add them to the 'remove' list and run the script again.")
    for column_name in df.columns.tolist():
        print('\t', column_name)

