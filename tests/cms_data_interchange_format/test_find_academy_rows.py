"""
Tests for the function find_academy_rows(), which finds metadata rows that are or might be academy applications
To simplify testing, a small subset of the columns from an export are used
"""
import pandas as pd
import unittest
from cms_data_interchange_format import find_academy_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_code_desc(self):
        """Test for when the column code_description indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['', '', 'ACAD - Academy Nominations'],
                           ['', '', 'acad - academy nominations'],
                           ['', '', 'WEBACAD - Web Form Academy Nominations'],
                           ['', '', 'webacad - web form academy nominations'],
                           ['', '', 'academy nomination'],
                           ['', '', 'academy awards']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['', '', 'ACAD - Academy Nominations', 'Academy_Application'],
                    ['', '', 'acad - academy nominations', 'Academy_Application'],
                    ['', '', 'WEBACAD - Web Form Academy Nominations', 'Academy_Application'],
                    ['', '', 'webacad - web form academy nominations', 'Academy_Application'],
                    ['', '', 'academy nomination', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['', '', 'academy awards', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for code_desc df_academy_check")

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['', 'Sports Academy', ''],
                           ['', 'academy appointment request', ''],
                           ['', 'HELP WITH ACADEMY ISSUE', ''],
                           ['', 'academy vouchers', ''],
                           ['', 'Academy Nominations', ''],
                           ['', 'Military Academy - Application', '']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['', 'academy appointment request', '', 'Academy_Application'],
                    ['', 'HELP WITH ACADEMY ISSUE', '', 'Academy_Application'],
                    ['', 'Academy Nominations', '', 'Academy_Application'],
                    ['', 'Military Academy - Application', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for COLUMN, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['', 'Sports Academy', '', 'Academy_Application'],
                    ['', 'academy vouchers', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for COLUMN, df_academy_check")

    def test_none(self):
        """Test for when no rows have academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['file.doc', 'one', 'a'],
                           ['file.doc', 'two', 'b'],
                           ['file.doc', 'three', 'c']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_academy_check")


if __name__ == '__main__':
    unittest.main()
