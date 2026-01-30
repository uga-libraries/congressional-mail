import numpy as np
import pandas as pd
import unittest
from css_data_interchange_format import find_academy_rows
from test_df_search import make_df
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):
    
    def test_doc_name(self):
        """Test for when the column communication_document_name contains academy"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', '', 'docs\\ACADEMYday25.txt', '', ''],
                ['20250402', '', '', '', ''],
                ['20250403', '', np.nan, '', ''],
                ['20250404', '', 'docs\\ACADEMY\\doc.txt', '', ''],
                ['20250405', '', 'docs\\25Academy', '', ''],
                ['20250406', '', 'docs\\doc.txt', '', ''],
                ['20250407', '', 'academy', '', '']]
        df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', 'docs\\ACADEMYday25.txt', '', '', 'Academy_Application'],
                    ['20250404', '', 'docs\\ACADEMY\\doc.txt', '', '', 'Academy_Application'],
                    ['20250405', '', 'docs\\25Academy', '', '', 'Academy_Application'],
                    ['20250407', '', 'academy', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_academy_check")

    def test_file_name(self):
        """Test for when the column file_name contains academy"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', '', '', 'ACADEMYday25.txt', ''],
                ['20250402', '', '', '', ''],
                ['20250403', '', '', np.nan, ''],
                ['20250404', '', '', 'ACADEMYdoc.txt', ''],
                ['20250405', '', '', '25Academy', ''],
                ['20250406', '', '', 'doc.txt', ''],
                ['20250407', '', '', 'academy', '']]
        df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', '', 'ACADEMYday25.txt', '', 'Academy_Application'],
                    ['20250404', '', '', 'ACADEMYdoc.txt', '', 'Academy_Application'],
                    ['20250405', '', '', '25Academy', '', 'Academy_Application'],
                    ['20250407', '', '', 'academy', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_academy_check")

    def test_group_name(self):
        """Test for when the column group_name indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'ACADEMY DAY', '', '', ''],
                           ['20250402', '2025_Academy_Day', '', '', ''],
                           ['20250403', 'academy', '', '', ''],
                           ['20250404', np.nan, '', '', ''],
                           ['20250405', '', '', '', ''],
                           ['20250406', 'BoardAcademy', '', '', ''],
                           ['20250407', 'Admin', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'ACADEMY DAY', '', '', '', 'Academy_Application'],
                    ['20250402', '2025_Academy_Day', '', '', '', 'Academy_Application'],
                    ['20250403', 'academy', '', '', '', 'Academy_Application'],
                    ['20250406', 'BoardAcademy', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_academy_check")

    def test_none(self):
        """Test for no patterns indicating academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250402Academy', '', 'docs\\doc.txt', 'file.txt', ''],
                           ['20250402', np.nan, 'docs\\doc.txt', np.nan, np.nan],
                           ['20250403', 'Interviews', 'docs\\doc.txt', 'int.txt', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_academy_check")

    def test_text(self):
        """Test for when the column text indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', '', 'ACADEMY DAY'],
                           ['20250402', '', '', '', 'academy'],
                           ['20250403', '', '', '', 'interviews academy25'],
                           ['20250404', '', '', '', ''],
                           ['20250405', '', '', '', 'keep'],
                           ['20250406', '', '', '', 'BoardAcademy'],
                           ['20250407', '', '', '', np.nan]],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', '', '', 'ACADEMY DAY', 'Academy_Application'],
                    ['20250402', '', '', '', 'academy', 'Academy_Application'],
                    ['20250403', '', '', '', 'interviews academy25', 'Academy_Application'],
                    ['20250406', '', '', '', 'BoardAcademy', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for text, df_academy_check")


if __name__ == '__main__':
    unittest.main()
