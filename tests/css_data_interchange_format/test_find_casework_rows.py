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
        df = pd.DataFrame([['20250401', 'Admin', 'doc\\Casework - Initial Reply.doc', ''],
                           ['20250402', 'case12', 'doc\\doc.txt', ''],
                           ['20250403', 'CASE 1', '', ''],
                           ['20250404', 'Admin', 'doc\\initialssacase.doc', ''],
                           ['20250405', 'Admin', 'doc\\Close Favorably - Casework.doc', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category'],
                    ['20250402', 'case12', 'doc\\doc.txt', '', 'Casework'],
                    ['20250403', 'CASE 1', '', '', 'Casework'],
                    ['20250401', 'Admin', 'doc\\Casework - Initial Reply.doc', '', 'Casework'],
                    ['20250404', 'Admin', 'doc\\initialssacase.doc', '', 'Casework'],
                    ['20250405', 'Admin', 'doc\\Close Favorably - Casework.doc', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for both, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for both, df_casework_check")

    def test_doc_name(self):
        """Test for when the column communication_document_name indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'Admin', 'doc\\Buck Letter - Casework.doc', ''],
                           ['20250402', 'Admin', 'doc\\Casework - Initial Reply.doc', ''],
                           ['20250403', 'Admin', 'doc\\Close Favorably - Casework.doc', ''],
                           ['20250404', 'Admin', 'doc\\Initial Reply - Casework.doc', ''],
                           ['20250405', 'Admin', 'doc\\Interim - Casework.doc', ''],
                           ['20250406', 'Admin', 'doc\\Open Sixth District Casework.doc', ''],
                           ['20250407', 'Admin', 'doc\\Napster Case.doc', ''],
                           ['20250408', 'Admin', 'doc\\initialssacase.doc', ''],
                           ['20250409', 'Admin', 'doc\\Open Sixth District Cases.doc', ''],
                           ['20250410', 'Admin', 'doc\\Antitrust Case.doc', ''],
                           ['20250411', 'Admin', 'doc\\doc.txt', 'case_file.txt']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category'],
                    ['20250401', 'Admin', 'doc\\Buck Letter - Casework.doc', '', 'Casework'],
                    ['20250402', 'Admin', 'doc\\Casework - Initial Reply.doc', '', 'Casework'],
                    ['20250403', 'Admin', 'doc\\Close Favorably - Casework.doc', '', 'Casework'],
                    ['20250404', 'Admin', 'doc\\Initial Reply - Casework.doc', '', 'Casework'],
                    ['20250405', 'Admin', 'doc\\Interim - Casework.doc', '', 'Casework'],
                    ['20250406', 'Admin', 'doc\\Open Sixth District Casework.doc', '', 'Casework'],
                    ['20250408', 'Admin', 'doc\\initialssacase.doc', '', 'Casework'],
                    ['20250409', 'Admin', 'doc\\Open Sixth District Cases.doc', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for both, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category'],
                    ['20250407', 'Admin', 'doc\\Napster Case.doc', '', 'Casework'],
                    ['20250410', 'Admin', 'doc\\Antitrust Case.doc', '', 'Casework'],
                    ['20250411', 'Admin', 'doc\\doc.txt', 'case_file.txt', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for both, df_casework_check")

    def test_group_name(self):
        """Test for when the column group_name indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'case12', 'doc\\doc.txt', ''],
                           ['20250402', 'CASE 1', '', ''],
                           ['20250403', 'legal case concern', '', ''],
                           ['20250404', 'Smith Case', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category'],
                    ['20250401', 'case12', 'doc\\doc.txt', '', 'Casework'],
                    ['20250402', 'CASE 1', '', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for group_name, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category'],
                    ['20250403', 'legal case concern', '', '', 'Casework'],
                    ['20250404', 'Smith Case', '', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for group_name, df_casework_check")

    def test_none(self):
        """Test for when no patterns indicating casework are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'Admin', '', ''],
                           ['20250402', 'Admin', 'doc\\doc.txt', ''],
                           ['20250403', '', 'doc\\doc.txt', 'doc.txt'],
                           ['20250404', '', '', 'doc.txt']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none, df_casework_check")


if __name__ == '__main__':
    unittest.main()
