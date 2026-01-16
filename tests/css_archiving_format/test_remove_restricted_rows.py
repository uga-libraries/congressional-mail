import os
import pandas as pd
import unittest
from css_archiving_format import remove_restricted_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_delimiter(self):
        """Test for when columns in md_df have delimiters in the topic columns"""
        # Makes dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['Anders', '12345', 'citizen^open', r'..\objects\1.txt', 'open'],
                              ['Blooms', '23456', 'citizen^refugee', r'..\objects\2.txt', 'open'],
                              ['Cliver', '34567', 'court', r'..\objects\3.txt', 'immigrant^immigration'],
                              ['Dudley', '45678', 'citizen^migrant', r'..\objects\4.txt', 'court^citizen'],
                              ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']],
                             columns=['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'])
        output_directory = os.path.join('test_data', 'remove_restricted_rows', 'delimiter')
        md_df = remove_restricted_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'],
                    ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']]
        self.assertEqual(expected, result, "Problem with test for type_same")

    def test_no_restrictions(self):
        """Test for when there is no restriction_review.csv"""
        # Makes dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['Anders', '12345', 'open', r'..\objects\1.txt', 'ok'],
                              ['Blooms', '23456', 'open', r'..\objects\2.txt', 'ok'],
                              ['Cliver', '34567', 'open', r'..\objects\3.txt', 'ok']],
                             columns=['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'])
        output_directory = os.path.join('test_data')
        md_df = remove_restricted_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'],
                    ['Anders', '12345', 'open', r'..\objects\1.txt', 'ok'],
                    ['Blooms', '23456', 'open', r'..\objects\2.txt', 'ok'],
                    ['Cliver', '34567', 'open', r'..\objects\3.txt', 'ok']]
        self.assertEqual(expected, result, "Problem with test for no_restrictions")

    def test_type_different(self):
        """Test for when columns in md_df have a different datatype as restriction_review.csv"""
        # Makes dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['Anders', 12345, 'citizen', r'..\objects\1.txt', 'response'],
                              ['Blooms', 23456, 'citizen', r'..\objects\2.txt', 'response'],
                              ['Cliver', 34567, 'open_ok', r'..\objects\3.txt', 'response'],
                              ['Dudley', 45678, 'migrant', r'..\objects\4.txt', 'response'],
                              ['Everly', 56789, 'open_ok', r'..\objects\5.txt', 'response']],
                             columns=['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'])
        output_directory = os.path.join('test_data', 'remove_restricted_rows', 'no_delimiter')
        md_df = remove_restricted_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'],
                    ['Cliver', '34567', 'open_ok', r'..\objects\3.txt', 'response'],
                    ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']]
        self.assertEqual(expected, result, "Problem with test for type_different")

    def test_type_same(self):
        """Test for when columns in md_df have the same datatype as restriction_review.csv"""
        # Makes dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['Anders', '12345', 'citizen', r'..\objects\1.txt', 'response'],
                              ['Blooms', '23456', 'citizen', r'..\objects\2.txt', 'response'],
                              ['Cliver', '34567', 'open_ok', r'..\objects\3.txt', 'response'],
                              ['Dudley', '45678', 'migrant', r'..\objects\4.txt', 'response'],
                              ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']],
                             columns=['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'])
        output_directory = os.path.join('test_data', 'remove_restricted_rows', 'no_delimiter')
        md_df = remove_restricted_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name', 'out_topic'],
                    ['Cliver', '34567', 'open_ok', r'..\objects\3.txt', 'response'],
                    ['Everly', '56789', 'open_ok', r'..\objects\5.txt', 'response']]
        self.assertEqual(expected, result, "Problem with test for type_same")


if __name__ == '__main__':
    unittest.main()
