import numpy as np
import unittest
from cms_data_interchange_format import find_academy_rows
from test_df_search import make_df
from test_read_metadata_file import df_to_list


class MyTestCase(unittest.TestCase):

    def test_code_desc(self):
        """Test for when the column code_description indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', 'ACAD - Academy Nominations'],
                ['30601', '', '', 'academy nominations'],
                ['30602', '', '', 'Nominations'],
                ['30603', '', '', ''],
                ['30604', '', '', 'nomination_academy'],
                ['30605', '', '', 'ACADEMY'],
                ['30606', '', '', np.nan],
                ['30607', '', '', 'ACAD'],
                ['30608', '', '', 'ACAD 25']]
        df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', '', 'ACAD - Academy Nominations', 'Academy_Application'],
                    ['30601', '', '', 'academy nominations', 'Academy_Application'],
                    ['30604', '', '', 'nomination_academy', 'Academy_Application'],
                    ['30605', '', '', 'ACADEMY', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30607', '', '', 'ACAD', 'Academy_Application'],
                    ['30608', '', '', 'ACAD 25', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for code_desc df_academy_check")

    def test_corr_doc(self):
        """Test for when the column correspondence_document_name indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'path\\academy appointment.doc', '', ''],
                ['30601', 'academy issue.doc', '', ''],
                ['30602', 'path\\ACADEMY', '', ''],
                ['30603', 'academy', '', ''],
                ['30604', '', '', ''],
                ['30605', 'path\\military.doc', '', ''],
                ['30606', np.nan, '', ''],
                ['30607', 'path\\acad.doc', '', ''],
                ['30608', 'path\\Acad25.pdf', '', '']]
        df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', 'path\\academy appointment.doc', '', '', 'Academy_Application'],
                    ['30601', 'academy issue.doc', '', '', 'Academy_Application'],
                    ['30602', 'path\\ACADEMY', '', '', 'Academy_Application'],
                    ['30603', 'academy', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30607', 'path\\acad.doc', '', '', 'Academy_Application'],
                    ['30608', 'path\\Acad25.pdf', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_academy_check")

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', 'Sports Academy', ''],
                ['30601', '', 'academy appointment request', ''],
                ['30602', '', 'HELP WITH ACADEMY ISSUE', ''],
                ['30603', '', 'academy', ''],
                ['30604', '', '', ''],
                ['30605', '', np.nan, ''],
                ['30606', '', 'Military', ''],
                ['30607', '', 'acad', ''],
                ['30608', '', 'acad25', '']]
        df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', 'Sports Academy', '', 'Academy_Application'],
                    ['30601', '', 'academy appointment request', '', 'Academy_Application'],
                    ['30602', '', 'HELP WITH ACADEMY ISSUE', '', 'Academy_Application'],
                    ['30603', '', 'academy', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30607', '', 'acad', '', 'Academy_Application'],
                    ['30608', '', 'acad25', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_academy_check")

    def test_none(self):
        """Test for when no rows have academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', np.nan, np.nan, np.nan],
                ['30601-academy', 'file.doc', 'two', 'b'],
                ['30602', 'file.doc', '', 'c']]
        df = make_df(rows)
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
