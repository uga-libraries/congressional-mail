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
              'addr1', 'addr2', 'addr3', 'addr4', 'city', 'state', 'extra']
    df = df.drop(remove, axis=1, errors="ignore")
