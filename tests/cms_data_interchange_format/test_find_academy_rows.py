"""
Tests for the function find_academy_rows(), which finds metadata rows that are or might be academy applications
To simplify testing, a small subset of the columns from an export are used
"""
import pandas as pd
import unittest
from cms_data_interchange_format import find_academy_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_both(self):
        """Test for when both columns checked indicate academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['file_1.doc', 'academy appointment', 'acad - academy nominations'],
                           ['file_2.doc', 'academy appointment request', 'Academy Nominations'],
                           ['file_3.doc', 'HELP WITH ACADEMY ISSUE', 'acad - academy nominations'],
                           ['file_4.doc', 'Academy Issue', 'WEBACAD - Web Form Academy Nominations']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_1.doc', 'academy appointment', 'acad - academy nominations', 'Academy_Application'],
                    ['file_2.doc', 'academy appointment request', 'Academy Nominations', 'Academy_Application'],
                    ['file_3.doc', 'HELP WITH ACADEMY ISSUE', 'acad - academy nominations', 'Academy_Application'],
                    ['file_4.doc', 'Academy Issue', 'WEBACAD - Web Form Academy Nominations', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for both, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for both, df_academy_check")

    def test_code_desc(self):
        """Test for when the column code_description indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['file_1.doc', 'x', 'ACAD - Academy Nominations'],
                           ['file_2.doc', 'x', 'acad - academy nominations'],
                           ['file_3.doc', 'x', 'WEBACAD - Web Form Academy Nominations'],
                           ['file_4.doc', 'x', 'webacad - web form academy nominations'],
                           ['file_5.doc', 'x', 'academy nomination'],
                           ['file_6.doc', 'x', 'academy awards']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_1.doc', 'x', 'ACAD - Academy Nominations', 'Academy_Application'],
                    ['file_2.doc', 'x', 'acad - academy nominations', 'Academy_Application'],
                    ['file_3.doc', 'x', 'WEBACAD - Web Form Academy Nominations', 'Academy_Application'],
                    ['file_4.doc', 'x', 'webacad - web form academy nominations', 'Academy_Application'],
                    ['file_5.doc', 'x', 'academy nomination', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for code_desc, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_6.doc', 'x', 'academy awards', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for code_desc df_academy_check")

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['file_1.doc', 'Sports Academy', 'x'],
                           ['file_2.doc', 'academy appointment request', 'x'],
                           ['file_3.doc', 'HELP WITH ACADEMY ISSUE', 'x'],
                           ['file_4.doc', 'academy vouchers', 'x'],
                           ['file_5.doc', 'Academy Nominations', 'x'],
                           ['file_6.doc', 'Military Academy - Application', 'x']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_2.doc', 'academy appointment request', 'x', 'Academy_Application'],
                    ['file_3.doc', 'HELP WITH ACADEMY ISSUE', 'x', 'Academy_Application'],
                    ['file_5.doc', 'Academy Nominations', 'x', 'Academy_Application'],
                    ['file_6.doc', 'Military Academy - Application', 'x', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for COLUMN, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_1.doc', 'Sports Academy', 'x', 'Academy_Application'],
                    ['file_4.doc', 'academy vouchers', 'x', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for COLUMN, df_academy_check")

    def test_none(self):
        """Test for when no rows have academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['file_1.doc', 'one', 'a'],
                           ['file_2.doc', 'two', 'b'],
                           ['file_3.doc', 'three', 'c']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none, df_academy_check")


if __name__ == '__main__':
    unittest.main()
