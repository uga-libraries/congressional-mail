import pandas as pd
import unittest
from css_archiving_format import remove_restricted_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_delimiter(self):
        """Test for when columns in md_df have delimiters in the topic columns"""
        # Makes dataframes to use as test input and runs the function.
        md_df = pd.DataFrame([['Anders', '12345', 'citizen^open', r'..\objects\1.txt', 'open'],
                              ['Blooms', '23456', 'citizen^refugee', r'..\objects\2.txt', 'open'],
                              ['Cliver', '34567', 'court', r'..\objects\3.txt', 'immigrant^immigration'],
                              ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen'],
                              ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']],
                             columns=['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'])
        restrict_df = pd.DataFrame([['Anders', '12345', 'citizen^open', r'..\objects\1.txt', 'open', 'citizen', 'open'],
                                    ['Blooms', '23456', 'citizen^refugee', r'..\objects\2.txt', 'open', 'citizen', 'open'],
                                    ['Blooms', '23456', 'citizen^refugee', r'..\objects\2.txt', 'open', 'refugee', 'open'],
                                    ['Cliver', '34567', 'court', r'..\objects\3.txt', 'immigrant^immigration', 'court', 'immigrant'],
                                    ['Cliver', '34567', 'court', r'..\objects\3.txt', 'immigrant^immigration', 'court', 'migration'],
                                    ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen', 'citizen', 'court'],
                                    ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen', 'citizen', 'citizen'],
                                    ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen', 'migrant', 'court'],
                                    ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen', 'migrant', 'citizen']],
                                   columns=['last', 'zip', 'in_topic', 'in_document_name', 'out_topic', 'in_topic_split', 'out_topic_split'])
        md_df = remove_restricted_rows(md_df, restrict_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'],
                    ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']]
        self.assertEqual(expected, result, "Problem with test for delimiter")

    def test_no_delimiter(self):
        """Test for when columns in md_df have the same datatype as restriction_review.csv"""
        # Makes dataframes to use as test input and runs the function.
        md_df = pd.DataFrame([['Anders', '12345', 'citizen', r'..\objects\1.txt', 'response'],
                              ['Blooms', '23456', 'citizen', r'..\objects\2.txt', 'response'],
                              ['Cliver', '34567', 'open_ok', r'..\objects\3.txt', 'response'],
                              ['Dudley', '45678', 'migrant', r'..\objects\4.txt', 'response'],
                              ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']],
                             columns=['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'])
        restrict_df = pd.DataFrame([['Anders', '12345', 'citizen', r'..\objects\1.txt', 'response', 'citizen', 'response'],
                                    ['Blooms', '23456', 'citizen', r'..\objects\2.txt', 'response', 'citizen', 'response'],
                                    ['Dudley', '45678', 'migrant', r'..\objects\4.txt', 'response', 'migrant', 'response']],
                                   columns=['last', 'zip', 'in_topic', 'in_document_name', 'out_topic', 'in_topic_split', 'out_topic_split'])
        md_df = remove_restricted_rows(md_df, restrict_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'],
                    ['Cliver', '34567', 'open_ok', r'..\objects\3.txt', 'response'],
                    ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']]
        self.assertEqual(expected, result, "Problem with test for no_delimiter")


if __name__ == '__main__':
    unittest.main()
