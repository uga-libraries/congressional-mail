"""
Tests for the function find_casework_rows(), which finds rows that pertain to casework.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from css_data_interchange_format import find_casework_rows
from test_script import csv_to_list


def df_to_list(df):
    """Convert a dataframe to a list for easier comparison"""
    df.fillna('nan', inplace=True)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the logs, if made by the test"""
        log_paths = [os.path.join('test_data', 'case_remains_log.csv'),
                     os.path.join('test_data', 'case_delete_log.csv')]
        for log_path in log_paths:
            if os.path.exists(log_path):
                os.remove(log_path)

    def test_both(self):
        """Test for when both indicators for casework (casework anywhere or group starts with case) are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'CASE1', ''],
                              ['30601', '', 'This is casework'],
                              ['30602', 'CASE2', ''],
                              ['30603', '', 'Send casework to ATL']],
                             columns=['zip_code', 'group_name', 'communication_document_id'])
        casework_df = find_casework_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30600', 'CASE1', ''],
                    ['30602', 'CASE2', ''],
                    ['30601', '', 'This is casework'],
                    ['30603', '', 'Send casework to ATL']]
        self.assertEqual(result, expected, "Problem with test for both, df")

        # Tests the case remains log was not made.
        result = os.path.exists(os.path.join('test_data', 'case_remains_log.csv'))
        self.assertEqual(result, False, "Problem with test for both, case log")

        # Tests the values in the case delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_delete_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30600', 'CASE1', 'nan'],
                    ['30602', 'CASE2', 'nan'],
                    ['30601', 'nan', 'This is casework'],
                    ['30603', 'nan', 'Send casework to ATL']]
        self.assertEqual(result, expected, "Problem with test for both, deletion log")

    def test_casework(self):
        """Test for when any column contains the word casework (is deleted)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'Casework'],
                              ['30601', '', 'This is casework'],
                              ['30602', '', 'Special case'],
                              ['30603', '', 'Send casework to ATL'],
                              ['30604', 'AG CASEWORK', ''],
                              ['casework', '', '']],
                             columns=['zip_code', 'group_name', 'communication_document_id'])
        casework_df = find_casework_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30600', '', 'Casework'],
                    ['30601', '', 'This is casework'],
                    ['30603', '', 'Send casework to ATL'],
                    ['30604', 'AG CASEWORK', ''],
                    ['casework', '', '']]
        self.assertEqual(result, expected, "Problem with test for casework, df")

        # Tests the values of the case remains log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_remains_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30602', 'nan', 'Special case']]
        self.assertEqual(result, expected, "Problem with test for casework, case log")

        # Tests the values in the case delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_delete_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30600', 'nan', 'Casework'],
                    ['30601', 'nan', 'This is casework'],
                    ['30603', 'nan', 'Send casework to ATL'],
                    ['30604', 'AG CASEWORK', 'nan'],
                    ['casework', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for casework, deletion log")

    def test_group_name(self):
        """Test for when the column group_name starts with CASE, which indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'CASE1', ''],
                              ['30601', 'COURT CASE', ''],
                              ['30602', 'CASE22', ''],
                              ['30603', 'EDUCATION', '']],
                             columns=['zip_code', 'group_name', 'communication_document_id'])
        casework_df = find_casework_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30600', 'CASE1', ''],
                    ['30602', 'CASE22', '']]
        self.assertEqual(result, expected, "Problem with test for group_name, df")

        # Tests the values of the case remains log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_remains_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30601', 'COURT CASE', 'nan']]
        self.assertEqual(result, expected, "Problem with test for group_name, case log")

        # Tests the values in the case delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_delete_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id'],
                    ['30600', 'CASE1', 'nan'],
                    ['30602', 'CASE22', 'nan']]
        self.assertEqual(result, expected, "Problem with test for group_name, deletion log")

    def test_no_casework(self):
        """Test for when no rows are casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Education', ''],
                              ['30601', 'Education', ''],
                              ['30602', 'Transportation', '']],
                             columns=['zip_code', 'group_name', 'communication_document_id'])
        casework_df = find_casework_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip_code', 'group_name', 'communication_document_id']]
        self.assertEqual(result, expected, "Problem with test for no casework, df")

        # Tests the case remains log was not made.
        result = os.path.exists(os.path.join('test_data', 'case_remains_log.csv'))
        self.assertEqual(result, False, "Problem with test for no casework, case log")

        # Tests the values in the case delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_delete_log.csv'))
        expected = [['zip_code', 'group_name', 'communication_document_id']]
        self.assertEqual(result, expected, "Problem with test for no casework, deletion log")


if __name__ == '__main__':
    unittest.main()
