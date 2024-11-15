"""
Tests for the function remove_casework(), which removes rows that pertain to casework.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from css_data_interchange_format import remove_casework
from test_script import csv_to_list


def df_to_list(df):
    """Convert a dataframe to a list for easier comparison"""
    df.fillna('nan', inplace=True)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the logs, if made by the test"""
        paths = [os.path.join('test_data', 'casework_deletion_log.csv'),
                 os.path.join('test_data', 'group_deletion_log.csv'),
                 os.path.join('test_data', 'row_includes_case_log.csv')]
        for path in paths:
            if os.path.exists(path):
                os.remove(path)

    def test_casework(self):
        """Test for when a column contains the word casework (is deleted)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'Casework'],
                              ['30601', '', 'This is casework'],
                              ['30602', '', 'Special case'],
                              ['30603', '', 'Send casework to ATL'],
                              ['30604', 'AG CASEWORK', ''],
                              ['casework', '', '']],
                             columns=['zip_code', 'group_name', 'communication_document_id'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30602', '', 'Special case'],]
        self.assertEqual(result, expected, "Problem with test for casework, df")

        # Tests the values in the casework deletion log are correct.
        result = csv_to_list(os.path.join('test_data', 'casework_deletion_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30600', 'nan', 'Casework'],
                    ['30601', 'nan', 'This is casework'],
                    ['30603', 'nan', 'Send casework to ATL'],
                    ['30604', 'AG CASEWORK', 'nan'],
                    ['casework', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for casework, deletion log")

        # Tests the values of the row includes case log are correct.
        result = csv_to_list(os.path.join('test_data', 'row_includes_case_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30602', 'nan', 'Special case']]
        self.assertEqual(result, expected, "Problem with test for casework, case log")

    def test_group_name(self):
        """Test for when the column group_name starts with CASE, which indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'CASE1', ''],
                              ['30601', 'COURT CASE', ''],
                              ['30602', 'CASE22', ''],
                              ['30603', 'EDUCATION', '']],
                             columns=['zip_code', 'group_name', 'communication_document_id'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30601', 'COURT CASE', ''],
                    ['30603', 'EDUCATION', '']]
        self.assertEqual(result, expected, "Problem with test for group_name, df")

        # Tests the values in the deletion log are correct.
        result = csv_to_list(os.path.join('test_data', 'group_deletion_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30600', 'CASE1', 'nan'],
                    ['30602', 'CASE22', 'nan']]
        self.assertEqual(result, expected, "Problem with test for group_name, deletion log")

        # Tests the values of the row includes case log are correct.
        result = csv_to_list(os.path.join('test_data', 'row_includes_case_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30601', 'COURT CASE', 'nan']]
        self.assertEqual(result, expected, "Problem with test for group_name, case log")

    def test_no_casework(self):
        """Test for when no rows are casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Education', ''],
                              ['30601', 'Education', ''],
                              ['30602', 'Transportation', '']],
                             columns=['zip_code', 'group_name', 'communication_document_id'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30600', 'Education', ''],
                    ['30601', 'Education', ''],
                    ['30602', 'Transportation', '']]
        self.assertEqual(result, expected, "Problem with test for no casework, df")

        # Tests the values of the row includes case log are correct.
        result = csv_to_list(os.path.join('test_data', 'row_includes_case_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id']]
        self.assertEqual(result, expected, "Problem with test for no casework, case log")


if __name__ == '__main__':
    unittest.main()
