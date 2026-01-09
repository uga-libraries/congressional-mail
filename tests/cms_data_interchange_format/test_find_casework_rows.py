"""
Tests for the function find_casework_rows(), which finds metadata rows that are or might be casework
To simplify testing, a small subset of the columns from an export are used
"""
import pandas as pd
import unittest
from cms_data_interchange_format import find_casework_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['file_1.doc', 'New case file', 'x'],
                           ['file_2.doc', 'case has been closed', 'x'],
                           ['file_3.doc', 'Case Open', 'x'],
                           ['file_4.doc', 'CASEWORK', 'x'],
                           ['file_5.doc', 'Forwarded to me for a response', 'x'],
                           ['file_6.doc', 'Add to open case', 'x'],
                           ['file_7.doc', 'Potential case', 'x'],
                           ['file_8.doc', 'Maybe not case work', 'x']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_1.doc', 'New case file', 'x', 'Casework'],
                    ['file_2.doc', 'case has been closed', 'x', 'Casework'],
                    ['file_3.doc', 'Case Open', 'x', 'Casework'],
                    ['file_4.doc', 'CASEWORK', 'x', 'Casework'],
                    ['file_5.doc', 'Forwarded to me for a response', 'x', 'Casework'],
                    ['file_6.doc', 'Add to open case', 'x', 'Casework'],
                    ['file_8.doc', 'Maybe not case work', 'x', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_7.doc', 'Potential case', 'x', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_casework_check")

    def test_none(self):
        """Test for when no rows have casework"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['file_1.doc', 'one', 'a'],
                           ['file_2.doc', 'two', 'b'],
                           ['file_3.doc', 'three', 'c']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_casework_check")


if __name__ == '__main__':
    unittest.main()
