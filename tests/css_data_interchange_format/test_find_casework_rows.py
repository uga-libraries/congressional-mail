"""
Tests for the function find_casework_rows(),
which finds metadata rows with topics or text that indicate they are casework and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_data_interchange_format import find_casework_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_both(self):
        """Test for when both patterns indicating casework are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', ''],
                           ['20250402', '', '', ''],
                           ['20250403', '', '', ''],
                           ['20250404', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for both, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for both, df_casework_check")

    def test_doc_name(self):
        """Test for when the column communication_document_name indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', ''],
                           ['20250402', '', '', ''],
                           ['20250403', '', '', ''],
                           ['20250404', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for both, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for both, df_casework_check")

    def test_group_name(self):
        """Test for when the column group_name indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', ''],
                           ['20250402', '', '', ''],
                           ['20250403', '', '', ''],
                           ['20250404', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for group_name, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for group_name, df_casework_check")

    def test_none(self):
        """Test for when no patterns indicating casework are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', ''],
                           ['20250402', '', '', ''],
                           ['20250403', '', '', ''],
                           ['20250404', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none, df_casework_check")


if __name__ == '__main__':
    unittest.main()
