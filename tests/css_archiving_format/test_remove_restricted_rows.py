"""
Test for the function remove_restricted_rows(), which removes metadata rows for letters deleted during appraisal.
To simplify input, the test uses dataframes with only a few of the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from css_archiving_format import remove_restricted_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_no_restrictions(self):
        """Test for when there is no restriction_review.csv"""
        # Makes dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['Anders', '12345', 'open', r'..\objects\1.txt'],
                              ['Blooms', '23456', 'open', r'..\objects\2.txt'],
                              ['Cliver', '34567', 'open', r'..\objects\3.txt']],
                             columns=['last', 'zip', 'in_topic', 'in_document_name'])
        output_directory = os.path.join('test_data')
        md_df = remove_restricted_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name'],
                    ['Anders', '12345', 'open', r'..\objects\1.txt'],
                    ['Blooms', '23456', 'open', r'..\objects\2.txt'],
                    ['Cliver', '34567', 'open', r'..\objects\3.txt']]
        self.assertEqual(expected, result, "Problem with test for no_restrictions")

    def test_type_different(self):
        """Test for when columns in md_df have a different datatype as restriction_review.csv"""
        # Makes dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['Anders', 12345, 'citizen', r'..\objects\1.txt'],
                              ['Blooms', 23456, 'citizen', r'..\objects\2.txt'],
                              ['Cliver', 34567, 'open_ok', r'..\objects\3.txt'],
                              ['Dudley', 45678, 'migrant', r'..\objects\4.txt'],
                              ['Everly', 56789, 'open_ok', r'..\objects\5.txt']],
                             columns=['last', 'zip', 'in_topic', 'in_document_name'])
        output_directory = os.path.join('test_data', 'remove_restricted_rows')
        md_df = remove_restricted_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name'],
                    ['Cliver', '34567', 'open_ok', r'..\objects\3.txt'],
                    ['Everly', '56789', 'open_ok', r'..\objects\5.txt']]
        self.assertEqual(expected, result, "Problem with test for type_different")

    def test_type_same(self):
        """Test for when columns in md_df have the same datatype as restriction_review.csv"""
        # Makes dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['Anders', '12345', 'citizen', r'..\objects\1.txt'],
                              ['Blooms', '23456', 'citizen', r'..\objects\2.txt'],
                              ['Cliver', '34567', 'open_ok', r'..\objects\3.txt'],
                              ['Dudley', '45678', 'migrant', r'..\objects\4.txt'],
                              ['Everly', '56789', 'open_ok', r'..\objects\5.txt']],
                             columns=['last', 'zip', 'in_topic', 'in_document_name'])
        output_directory = os.path.join('test_data', 'remove_restricted_rows')
        md_df = remove_restricted_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'zip', 'in_topic', 'in_document_name'],
                    ['Cliver', '34567', 'open_ok', r'..\objects\3.txt'],
                    ['Everly', '56789', 'open_ok', r'..\objects\5.txt']]
        self.assertEqual(expected, result, "Problem with test for type_same")


if __name__ == '__main__':
    unittest.main()
