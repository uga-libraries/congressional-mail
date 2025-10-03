"""
Tests for the function appraisal_check_df, which makes a df of all rows to check for possible appraisal.
To simplify testing, a small subset of the metadata columns are used.
"""
import pandas as pd
import unittest
from css_data_interchange_format import appraisal_check_df


def df_to_list(df):
    """Convert a dataframe to a list for easier comparison"""
    df.fillna('blank', inplace=True)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def test_multiple_columns(self):
        """Test for when the keyword is in multiple columns per row"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'Agriculture', r'..\documents\farms_case.txt', 'farms_case.txt', 'case?'],
                           ['20250402', 'Legal Case', r'..\documents\legal_case.txt', 'legal.txt', 'just in case'],
                           ['20250403', 'Legal', r'..\documents\legal.txt', 'legal.txt', 'aid'],
                           ['20250404', 'Case Management', r'..\documents\case.txt', 'case.txt', 'maybe case']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_check = appraisal_check_df(df, 'case', 'Casework')

        # Tests the values in df_check are correct.
        result = df_to_list(df_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'Agriculture', r'..\documents\farms_case.txt', 'farms_case.txt', 'case?', 'Casework'],
                    ['20250402', 'Legal Case', r'..\documents\legal_case.txt', 'legal.txt', 'just in case', 'Casework'],
                    ['20250404', 'Case Management', r'..\documents\case.txt', 'case.txt', 'maybe case', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for multiple columns")

    def test_one_column(self):
        """Test for when the keyword is in one column per row"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'Agriculture', r'..\documents\farms_case.txt', 'farms.txt', 'pro'],
                           ['20250402', 'Legal', r'..\documents\legal_case.txt', 'legal.txt', 'pro'],
                           ['20250403', 'Legal', r'..\documents\legal.txt', 'legal.txt', 'con'],
                           ['20250404', 'Case Management', r'..\documents\mgt.txt', 'mgt.txt', 'aid'],
                           ['20240405', 'Admin', r'..\documents\file.txt', 'file.txt', 'potential case']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_check = appraisal_check_df(df, 'case', 'Casework')

        # Tests the values in df_check are correct.
        result = df_to_list(df_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'Agriculture', r'..\documents\farms_case.txt', 'farms.txt', 'pro', 'Casework'],
                    ['20250402', 'Legal', r'..\documents\legal_case.txt', 'legal.txt', 'pro', 'Casework'],
                    ['20250404', 'Case Management', r'..\documents\mgt.txt', 'mgt.txt', 'aid', 'Casework'],
                    ['20240405', 'Admin', r'..\documents\file.txt', 'file.txt', 'potential case', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for one column")

    def test_no_column(self):
        """Test for when the keyword is in no columns"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'Agriculture', r'..\documents\farms.txt', 'farms.txt', 'Pro'],
                           ['20250402', 'Legal', r'..\documents\legal.txt', 'legal.txt', 'Con']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_check = appraisal_check_df(df, 'case', 'Casework')

        # Tests the values in df_check are correct.
        result = df_to_list(df_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for no column")


if __name__ == '__main__':
    unittest.main()
