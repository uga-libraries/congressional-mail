import pandas as pd
import unittest
from css_archiving_format import remove_restricted_rows
from test_read_metadata import df_to_list


def make_df(rows, df_type):
    """Make a dataframe with the provided rows and column names based on the type"""

    # Column name options.
    md_column = ['last', 'zip', 'in_topic', 'in_document_name', 'out_topic']
    r_column = ['last', 'zip', 'in_topic', 'in_document_name', 'out_topic', 'in_topic_split', 'out_topic_split']

    # Make the dataframe, matching the column to the df_type.
    if df_type == 'md':
        df = pd.DataFrame(rows, columns=md_column)
    else:
        df = pd.DataFrame(rows, columns=r_column)
    return df


class MyTestCase(unittest.TestCase):

    def test_delimiter(self):
        """Test for when columns in md_df have delimiters in the topic columns"""
        # Makes dataframes to use as test input and runs the function.
        rows = [['Anders', '12345', 'citizen^open', r'..\objects\1.txt', 'open'],
                ['Blooms', '23456', 'citizen^refugee', r'..\objects\2.txt', 'open'],
                ['Cliver', '34567', 'court', r'..\objects\3.txt', 'immigrant^immigration'],
                ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen'],
                ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']]
        md_df = make_df(rows, 'md')
        rows = [['Anders', '12345', 'citizen^open', r'..\objects\1.txt', 'open', 'citizen', 'open'],
                ['Blooms', '23456', 'citizen^refugee', r'..\objects\2.txt', 'open', 'citizen', 'open'],
                ['Blooms', '23456', 'citizen^refugee', r'..\objects\2.txt', 'open', 'refugee', 'open'],
                ['Cliver', '34567', 'court', r'..\objects\3.txt', 'immigrant^immigration', 'court', 'immigrant'],
                ['Cliver', '34567', 'court', r'..\objects\3.txt', 'immigrant^immigration', 'court', 'migration'],
                ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen', 'citizen', 'court'],
                ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen', 'citizen', 'citizen'],
                ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen', 'migrant', 'court'],
                ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen', 'migrant', 'citizen']]
        restrict_df = make_df(rows, 'restrict')
        md_df = remove_restricted_rows(md_df, restrict_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'],
                    ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']]
        self.assertEqual(expected, result, "Problem with test for delimiter")

    def test_no_delimiter(self):
        """Test for when columns in md_df have the same datatype as restriction_review.csv"""
        # Makes dataframes to use as test input and runs the function.
        rows = [['Anders', '12345', 'citizen', r'..\objects\1.txt', 'response'],
                ['Blooms', '23456', 'citizen', r'..\objects\2.txt', 'response'],
                ['Cliver', '34567', 'open_ok', r'..\objects\3.txt', 'response'],
                ['Dudley', '45678', 'migrant', r'..\objects\4.txt', 'response'],
                ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']]
        md_df = make_df(rows, 'md')
        rows = [['Anders', '12345', 'citizen', r'..\objects\1.txt', 'response', 'citizen', 'response'],
                ['Blooms', '23456', 'citizen', r'..\objects\2.txt', 'response', 'citizen', 'response'],
                ['Dudley', '45678', 'migrant', r'..\objects\4.txt', 'response', 'migrant', 'response']]
        restrict_df = make_df(rows, 'restrict')
        md_df = remove_restricted_rows(md_df, restrict_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'],
                    ['Cliver', '34567', 'open_ok', r'..\objects\3.txt', 'response'],
                    ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']]
        self.assertEqual(expected, result, "Problem with test for no_delimiter")


if __name__ == '__main__':
    unittest.main()
