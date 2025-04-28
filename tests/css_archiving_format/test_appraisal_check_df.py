"""
Tests for the function appraisal_check_df, which makes a df of all rows to check for possible appraisal.
Tests for check df for the four categories of appraisal are part of the "find_category_rows" tests.
"""
import pandas as pd
import unittest
from css_archiving_format import appraisal_check_df
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_multiple_columns(self):
        """Test for when the keyword is in multiple columns per row"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', 'note', r'doc\file1.txt', '', '', '', r'form\filea.txt', 'a_b'],
                           ['30601', '', 'CASE', r'doc\Case_File.txt', '', '', '', r'form\a.txt', ''],
                           ['30602', '', '', '', r'doc\file3.txt', '', 'Note', '', ''],
                           ['30603', '', '', '', '', 'started case Tue', r'case\abc.txt', '', 'Mr._Case']],
                          columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                   'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_check = appraisal_check_df(df, 'case', 'Casework')

        # Tests the values in df_check are correct.
        result = df_to_list(df_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', 'CASE', r'doc\Case_File.txt', '', '', '', r'form\a.txt', '', 'Casework'],
                    ['30603', '', '', '', '', 'started case Tue', r'case\abc.txt', '', 'Mr._Case', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for one column")

    def test_one_column(self):
        """Test for when the keyword is in one column per row"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', 'note', r'doc\file1.txt', '', '', '', r'form\filea.txt', 'a_b'],
                           ['30601', '', 'CASE', '', '', '', '', r'form\a.txt', ''],
                           ['30602', '', 'note', r'doc\Case_File.txt', '', '', '', '', ''],
                           ['30603', '', '', '', '', '', 'started case Tue', '', 'a_b'],
                           ['30604', '', 'note', r'doc\file2.txt', '', '', 'reply note', r'case\abc.txt', ''],
                           ['30605', '', '', '', r'doc\file3.txt', '', 'Note', '', ''],
                           ['30606', '', '', '', r'doc\file4.txt', '', 'Note', r'letter\123.txt', 'Mr._Case']],
                          columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                   'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_check = appraisal_check_df(df, 'case', 'Casework')

        # Tests the values in df_check are correct.
        result = df_to_list(df_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', 'CASE', '', '', '', '', r'form\a.txt', '', 'Casework'],
                    ['30602', '', 'note', r'doc\Case_File.txt', '', '', '', '', '', 'Casework'],
                    ['30603', '', '', '', '', '', 'started case Tue', '', 'a_b', 'Casework'],
                    ['30604', '', 'note', r'doc\file2.txt', '', '', 'reply note', r'case\abc.txt', '', 'Casework'],
                    ['30606', '', '', '', r'doc\file4.txt', '', 'Note', r'letter\123.txt', 'Mr._Case', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for one column")

    def test_no_column(self):
        """Test for when the keyword is in no columns"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', 'note', r'doc\file1.txt', '', '', '', r'form\filea.txt', 'a_b'],
                           ['30602', '', 'note', '', '', '', '', r'form\a.txt', ''],
                           ['30603', '', '', '', '', '', 'started Tue', '', 'a_b']],
                          columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                   'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_check = appraisal_check_df(df, 'case', 'Casework')

        # Tests the values in df_check are correct.
        result = df_to_list(df_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for no column")


if __name__ == '__main__':
    unittest.main()
