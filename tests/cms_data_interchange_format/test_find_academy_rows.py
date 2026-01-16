import pandas as pd
import unittest
from cms_data_interchange_format import find_academy_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_code_desc(self):
        """Test for when the column code_description indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', '', 'ACAD - Academy Nominations'],
                           ['30601', '', '', 'acad - academy nominations'],
                           ['30602', '', '', 'WEBACAD - Web Form Academy Nominations'],
                           ['30603', '', '', 'webacad - web form academy nominations'],
                           ['30604', '', '', 'academy nomination'],
                           ['30605', '', '', 'academy awards']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', '', 'ACAD - Academy Nominations', 'Academy_Application'],
                    ['30601', '', '', 'acad - academy nominations', 'Academy_Application'],
                    ['30602', '', '', 'WEBACAD - Web Form Academy Nominations', 'Academy_Application'],
                    ['30603', '', '', 'webacad - web form academy nominations', 'Academy_Application'],
                    ['30604', '', '', 'academy nomination', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30605', '', '', 'academy awards', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for code_desc df_academy_check")

    def test_corr_doc(self):
        """Test for when the column correspondence_document_name indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', 'path/academy appointment.doc', '', ''],
                           ['30601', 'academy issue.doc', '', ''],
                           ['30602', 'ACADEMY NOMINATION', '', ''],
                           ['30603', 'path/check_academy.doc', '', ''],
                           ['30604', '', '', ''],
                           ['30605', 'path\\military academy.doc', '', '']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', 'path/academy appointment.doc', '', '', 'Academy_Application'],
                    ['30601', 'academy issue.doc', '', '', 'Academy_Application'],
                    ['30602', 'ACADEMY NOMINATION', '', '', 'Academy_Application'],
                    ['30605', 'path\\military academy.doc', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30603', 'path/check_academy.doc', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_academy_check")

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', 'Sports Academy', ''],
                           ['30601', '', 'academy appointment request', ''],
                           ['30602', '', 'HELP WITH ACADEMY ISSUE', ''],
                           ['30603', '', 'academy vouchers', ''],
                           ['30604', '', 'Academy Nominations', ''],
                           ['30605', '', 'Military Academy - Application', '']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30601', '', 'academy appointment request', '', 'Academy_Application'],
                    ['30602', '', 'HELP WITH ACADEMY ISSUE', '', 'Academy_Application'],
                    ['30604', '', 'Academy Nominations', '', 'Academy_Application'],
                    ['30605', '', 'Military Academy - Application', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', 'Sports Academy', '', 'Academy_Application'],
                    ['30603', '', 'academy vouchers', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_academy_check")

    def test_none(self):
        """Test for when no rows have academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', 'file.doc', 'one', 'a'],
                           ['30601', 'file.doc', 'two', 'b'],
                           ['30602', 'file.doc', 'three', 'c']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_academy_check")


if __name__ == '__main__':
    unittest.main()
