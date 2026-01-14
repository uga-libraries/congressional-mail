"""
Tests for the function find_casework_rows(), which finds metadata rows that are or might be casework
To simplify testing, a small subset of the columns from an export are used
"""
import pandas as pd
import unittest
from cms_data_interchange_format import find_casework_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_code_desc(self):
        """Test for when the column code_scription indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', '', 'New case file'],
                           ['30601', '', '', 'case has been closed'],
                           ['30602', '', '', 'Case Open'],
                           ['30603', '', '', 'CASEWORK'],
                           ['30604', '', '', ''],
                           ['30605', '', '', 'Maybe not case work'],
                           ['30606', '', '', 'Forwarded to me for a response'],
                           ['30607', '', '', 'Add to open case'],
                           ['30608', '', '', 'Potential case'],
                           ['30609', '', '', 'case']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', '', 'New case file', 'Casework'],
                    ['30601', '', '', 'case has been closed', 'Casework'],
                    ['30602', '', '', 'Case Open', 'Casework'],
                    ['30603', '', '', 'CASEWORK', 'Casework'],
                    ['30605', '', '', 'Maybe not case work', 'Casework'],
                    ['30606', '', '', 'Forwarded to me for a response', 'Casework'],
                    ['30607', '', '', 'Add to open case', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30608', '', '', 'Potential case', 'Casework'],
                    ['30609', '', '', 'case', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_casework_check")

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', 'New case file', ''],
                           ['30601', '', 'case has been closed', ''],
                           ['30602', '', 'Case Open', ''],
                           ['30603', '', 'CASEWORK', ''],
                           ['30604', '', 'Forwarded to me for a response', ''],
                           ['30605', '', 'Add to open case', ''],
                           ['30606', '', 'Potential case', ''],
                           ['30607', '', 'Maybe not case work', '']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', 'New case file', '', 'Casework'],
                    ['30601', '', 'case has been closed', '', 'Casework'],
                    ['30602', '', 'Case Open', '', 'Casework'],
                    ['30603', '', 'CASEWORK', '', 'Casework'],
                    ['30604', '', 'Forwarded to me for a response', '', 'Casework'],
                    ['30605', '', 'Add to open case', '', 'Casework'],
                    ['30607', '', 'Maybe not case work', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30606', '', 'Potential case', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_casework_check")

    def test_none(self):
        """Test for when no rows have casework"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', 'file_1.doc', 'one', 'a'],
                           ['30601', 'file_2.doc', 'two', 'b'],
                           ['30602', 'file_3.doc', 'three', 'c']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_casework_check")


if __name__ == '__main__':
    unittest.main()
