"""
Tests for the function appraisal_check_df(), which makes a df of all rows to check for possible appraisal.
To simplify testing, a small subset of the metadata columns are used.
"""
import pandas as pd
import unittest
from cms_data_interchange_format import appraisal_check_df
from test_read_metadata_file import df_to_list


class MyTestCase(unittest.TestCase):

    def test_multiple(self):
        """ Test for when the keyword is in multiple columns"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20230101', r'..\doc\legal case.txt', 'Concern re doe case'],
                           ['20230202', r'..\doc\CASE.txt', 'POSSIBLE CASE']],
                          columns=['date_in', 'correspondence_document_name', 'correspondence_text'])
        df_check = appraisal_check_df(df, 'case', 'Casework')

        # Tests the values in df_check are correct.
        result = df_to_list(df_check)
        expected = [['date_in', 'correspondence_document_name', 'correspondence_text', 'Appraisal_Category'],
                    ['20230101', r'..\doc\legal case.txt', 'Concern re doe case', 'Casework'],
                    ['20230202', r'..\doc\CASE.txt', 'POSSIBLE CASE', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for multiple columns")

    def test_one(self):
        """ Test for when the keyword is in one column"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20230101', r'..\doc\case_file.txt', 'note1'],
                           ['20230202', r'..\doc\file2.txt', 'LEGAL CASE'],
                           ['20230303', r'..\doc\CASE_FILE.txt', 'note3'],
                           ['20230404', r'..\doc\file4.txt', 'case']],
                          columns=['date_in', 'correspondence_document_name', 'correspondence_text'])
        df_check = appraisal_check_df(df, 'case', 'Casework')

        # Tests the values in df_check are correct.
        result = df_to_list(df_check)
        expected = [['date_in', 'correspondence_document_name', 'correspondence_text', 'Appraisal_Category'],
                    ['20230101', r'..\doc\case_file.txt', 'note1', 'Casework'],
                    ['20230202', r'..\doc\file2.txt', 'LEGAL CASE', 'Casework'],
                    ['20230303', r'..\doc\CASE_FILE.txt', 'note3', 'Casework'],
                    ['20230404', r'..\doc\file4.txt', 'case', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for one column")

    def test_none(self):
        """ Test for when the keyword is not in any column"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20230101', r'..\doc\file.txt', 'note'],
                           ['20230202', r'..\doc\file2.txt', 'note2']],
                          columns=['date_in', 'correspondence_document_name', 'correspondence_text'])
        df_check = appraisal_check_df(df, 'case', 'Casework')

        # Tests the values in df_check are correct.
        result = df_to_list(df_check)
        expected = [['date_in', 'correspondence_document_name', 'correspondence_text', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no match for appraisal)")


if __name__ == '__main__':
    unittest.main()
