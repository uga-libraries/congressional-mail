"""
Tests for the function find_casework_rows(),
which finds metadata rows with topics or text that indicate they are casework and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_data_interchange_format import find_casework_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_both(self):
        """Test for when both patterns indicating casework are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', 'doc\\Case Work - Initial Reply.doc', '', ''],
                           ['20250402', 'case12', 'doc\\doc.txt', '', ''],
                           ['20250403', 'CASE 1', '', '', ''],
                           ['20250404', '', 'doc\\initialssacase.doc', '', ''],
                           ['20250405', '', 'doc\\Close Favorably - Casework.doc', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250402', 'case12', 'doc\\doc.txt', '', '', 'Casework'],
                    ['20250403', 'CASE 1', '', '', '', 'Casework'],
                    ['20250401', '', 'doc\\Case Work - Initial Reply.doc', '', '', 'Casework'],
                    ['20250404', '', 'doc\\initialssacase.doc', '', '', 'Casework'],
                    ['20250405', '', 'doc\\Close Favorably - Casework.doc', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for both, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for both, df_casework_check")

    def test_doc_name(self):
        """Test for when the column communication_document_name indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', 'doc\\Buck Letter - Casework.doc', '', ''],
                           ['20250402', '', 'doc\\Casework - Initial Reply.doc', '', ''],
                           ['20250403', '', 'doc\\Close Favorably - Case work.doc', '', ''],
                           ['20250404', '', 'doc\\Initial Reply - Casework.doc', '', ''],
                           ['20250405', '', 'doc\\Interim - Casework.doc', '', ''],
                           ['20250406', '', 'doc\\Open Sixth District Casework.doc', '', ''],
                           ['20250407', '', 'doc\\Napster Case.doc', '', ''],
                           ['20250408', '', 'doc\\initialssacase.doc', '', ''],
                           ['20250409', '', 'doc\\Open Sixth District Cases.doc', '', ''],
                           ['20250410', '', 'doc\\Antitrust Case.doc', '', ''],
                           ['20250411', '', 'doc\\doc.txt', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', 'doc\\Buck Letter - Casework.doc', '', '', 'Casework'],
                    ['20250402', '', 'doc\\Casework - Initial Reply.doc', '', '', 'Casework'],
                    ['20250403', '', 'doc\\Close Favorably - Case work.doc', '', '', 'Casework'],
                    ['20250404', '', 'doc\\Initial Reply - Casework.doc', '', '', 'Casework'],
                    ['20250405', '', 'doc\\Interim - Casework.doc', '', '', 'Casework'],
                    ['20250406', '', 'doc\\Open Sixth District Casework.doc', '', '', 'Casework'],
                    ['20250408', '', 'doc\\initialssacase.doc', '', '', 'Casework'],
                    ['20250409', '', 'doc\\Open Sixth District Cases.doc', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for both, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250407', '', 'doc\\Napster Case.doc', '', '', 'Casework'],
                    ['20250410', '', 'doc\\Antitrust Case.doc', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for both, df_casework_check")

    def test_group_name(self):
        """Test for when the column group_name indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'casework12', '', '', ''],
                           ['20250402', 'CASE 1', '', '', ''],
                           ['20250403', 'legal case concern', '', '', ''],
                           ['20250404', 'Smith Case', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'casework12', '', '', '', 'Casework'],
                    ['20250402', 'CASE 1', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250403', 'legal case concern', '', '', '', 'Casework'],
                    ['20250404', 'Smith Case', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_casework_check")

    def test_none(self):
        """Test for when no patterns indicating casework are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', '', ''],
                           ['20250402', '', 'doc\\doc.txt', '', ''],
                           ['20250403', '', 'doc\\doc.txt', 'doc.txt', ''],
                           ['20250404', '', '', 'doc.txt', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_casework_check")


if __name__ == '__main__':
    unittest.main()
