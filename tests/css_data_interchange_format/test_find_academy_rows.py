"""
Tests for the function find_academy_rows(), 
which finds metadata rows with topics or text that indicate they are academy applications and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_data_interchange_format import find_academy_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):
    
    def test_doc_name(self):
        """Test for when the column communication_document_name indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', 'docs\\ACADEMYday25.txt', '', ''],
                           ['20250402', '', 'docs\\doc.txt', '', ''],
                           ['20250403', '', 'docs\\academy_interviews.txt', '', ''],
                           ['20250404', '', 'docs\\ACADEMY\\doc.txt', '', ''],
                           ['20250405', '', 'docs\\25Academy.txt', '', ''],
                           ['20250406', '', 'docs\\doc.txt', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', 'docs\\ACADEMYday25.txt', '', '', 'Academy_Application'],
                    ['20250403', '', 'docs\\academy_interviews.txt', '', '', 'Academy_Application'],
                    ['20250404', '', 'docs\\ACADEMY\\doc.txt', '', '', 'Academy_Application'],
                    ['20250405', '', 'docs\\25Academy.txt', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_academy_check")

    def test_group_name(self):
        """Test for when the column group_name indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'ACADEMY DAY', '', '', ''],
                           ['20250402', 'Academy2025', '', '', ''],
                           ['20250403', 'academy interviews 25', '', '', ''],
                           ['20250404', '', '', '', ''],
                           ['20250405', '', '', '', ''],
                           ['20250406', 'BoardAcademy', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'ACADEMY DAY', '', '', '', 'Academy_Application'],
                    ['20250402', 'Academy2025', '', '', '', 'Academy_Application'],
                    ['20250403', 'academy interviews 25', '', '', '', 'Academy_Application'],
                    ['20250406', 'BoardAcademy', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_academy_check")

    def test_none(self):
        """Test for no patterns indicating academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', 'docs\\doc.txt', 'academy_file.txt', ''],
                           ['20250402', '', 'docs\\doc.txt', '', ''],
                           ['20250403', 'Interviews', 'docs\\doc.txt', 'intACADEMY.txt', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', 'docs\\doc.txt', 'academy_file.txt', '', 'Academy_Application'],
                    ['20250403', 'Interviews', 'docs\\doc.txt', 'intACADEMY.txt', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for none, df_academy_check")

    def test_text(self):
        """Test for when the column text indicates academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', '', 'ACADEMY DAY'],
                           ['20250402', '', '', '', 'academy'],
                           ['20250403', '', '', '', 'academy interviews 25'],
                           ['20250404', '', '', '', ''],
                           ['20250405', '', '', '', 'keep'],
                           ['20250406', '', '', '', 'BoardAcademy']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_academy, df_academy_check = find_academy_rows(df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', '', '', 'ACADEMY DAY', 'Academy_Application'],
                    ['20250402', '', '', '', 'academy', 'Academy_Application'],
                    ['20250403', '', '', '', 'academy interviews 25', 'Academy_Application'],
                    ['20250406', '', '', '', 'BoardAcademy', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for text, df_academy_check")


if __name__ == '__main__':
    unittest.main()
