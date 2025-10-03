"""
Tests for the function find_casework_rows(), which finds rows that pertain to casework.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from archival_office_correspondence_data import find_casework_rows
from test_script import csv_to_list


def df_to_list(df):
    """Convert a dataframe to a list for easier comparison"""
    df.fillna('nan', inplace=True)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the logs, if made by the test"""
        log_paths = [os.path.join('test_data', 'case_delete_log.csv'),
                     os.path.join('test_data', 'case_remains_log.csv')]
        for log_path in log_paths:
            if os.path.exists(log_path):
                os.remove(log_path)

    def test_case_comments(self):
        """Test for when the column comments contains the string "case" and is deleted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'type', 'topic', 'subtopic', 'I AM ON THE CASE'],
                              ['30601', 'type', 'topic', 'subtopic', 'Casework'],
                              ['30602', 'type', 'topic', 'subtopic', 'SEND CASE TO ATL'],
                              ['30603', 'type', 'topic', 'subtopic', 'case']],
                             columns=['zip_code', 'correspondence_type', 'correspondence_topic',
                                      'correspondence_subtopic', 'comments'])
        casework_df = find_casework_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['30600', 'type', 'topic', 'subtopic', 'I AM ON THE CASE'],
                    ['30601', 'type', 'topic', 'subtopic', 'Casework'],
                    ['30602', 'type', 'topic', 'subtopic', 'SEND CASE TO ATL'],
                    ['30603', 'type', 'topic', 'subtopic', 'case']]
        self.assertEqual(expected, result, "Problem with test for case - comments, df")

        # Tests the case remains log was not made.
        result = os.path.exists(os.path.join('test_data', 'case_remains_log.csv'))
        self.assertEqual(False, result, "Problem with test for case - comments, case log")

        # Tests the values in the case delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_delete_log.csv'))
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['30600', 'type', 'topic', 'subtopic', 'I AM ON THE CASE'],
                    ['30601', 'type', 'topic', 'subtopic', 'Casework'],
                    ['30602', 'type', 'topic', 'subtopic', 'SEND CASE TO ATL'],
                    ['30603', 'type', 'topic', 'subtopic', 'case']]
        self.assertEqual(expected, result, "Problem with test for case - comments, delete log")

    def test_case_subtopic(self):
        """Test for when the column correspondence_subtopic contains the string "case" and is deleted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'type', 'topic', 'LEGAL CASE', 'comments'],
                              ['30601', 'type', 'topic', 'Casework', 'comments'],
                              ['30602', 'type', 'topic', 'NEW CASE SS', 'comments'],
                              ['30603', 'type', 'topic', 'case', 'comments']],
                             columns=['zip_code', 'correspondence_type', 'correspondence_topic',
                                      'correspondence_subtopic', 'comments'])
        casework_df = find_casework_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['30600', 'type', 'topic', 'LEGAL CASE', 'comments'],
                    ['30601', 'type', 'topic', 'Casework', 'comments'],
                    ['30602', 'type', 'topic', 'NEW CASE SS', 'comments'],
                    ['30603', 'type', 'topic', 'case', 'comments']]
        self.assertEqual(expected, result, "Problem with test for case - subtopic, df")

        # Tests the case remains log was not made.
        result = os.path.exists(os.path.join('test_data', 'case_remains_log.csv'))
        self.assertEqual(False, result, "Problem with test for case - subtopic, case log")

        # Tests the values in the case delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_delete_log.csv'))
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['30600', 'type', 'topic', 'LEGAL CASE', 'comments'],
                    ['30601', 'type', 'topic', 'Casework', 'comments'],
                    ['30602', 'type', 'topic', 'NEW CASE SS', 'comments'],
                    ['30603', 'type', 'topic', 'case', 'comments']]
        self.assertEqual(expected, result, "Problem with test for case - subtopic, delete log")

    def test_case_topic(self):
        """Test for when the correspondence_topic contains the string "case" and is deleted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'type', 'LEGAL CASE', 'subtopic', 'comments'],
                              ['30601', 'type', 'Casework', 'subtopic', 'comments'],
                              ['30602', 'type', 'SEND CASE TO ATL', 'subtopic', 'comments'],
                              ['30603', 'type', 'case', 'subtopic', 'comments']],
                             columns=['zip_code', 'correspondence_type', 'correspondence_topic',
                                      'correspondence_subtopic', 'comments'])
        casework_df = find_casework_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['30600', 'type', 'LEGAL CASE', 'subtopic', 'comments'],
                    ['30601', 'type', 'Casework', 'subtopic', 'comments'],
                    ['30602', 'type', 'SEND CASE TO ATL', 'subtopic', 'comments'],
                    ['30603', 'type', 'case', 'subtopic', 'comments']]
        self.assertEqual(expected, result, "Problem with test for case - topic, df")

        # Tests the case remains log was not made.
        result = os.path.exists(os.path.join('test_data', 'case_remains_log.csv'))
        self.assertEqual(False, result, "Problem with test for case - topic, case log")

        # Tests the values in the case delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_delete_log.csv'))
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['30600', 'type', 'LEGAL CASE', 'subtopic', 'comments'],
                    ['30601', 'type', 'Casework', 'subtopic', 'comments'],
                    ['30602', 'type', 'SEND CASE TO ATL', 'subtopic', 'comments'],
                    ['30603', 'type', 'case', 'subtopic', 'comments']]
        self.assertEqual(expected, result, "Problem with test for case - topic, delete log")

    def test_case_type(self):
        """Test for when the column correspondence_type contains the string "case" and is deleted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'CASE', 'topic', 'subtopic', 'comments'],
                              ['30601', 'Casework', 'topic', 'subtopic', 'comments'],
                              ['30602', 'legal case', 'topic', 'subtopic', 'comments']],
                             columns=['zip_code', 'correspondence_type', 'correspondence_topic',
                                      'correspondence_subtopic', 'comments'])
        casework_df = find_casework_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['30600', 'CASE', 'topic', 'subtopic', 'comments'],
                    ['30601', 'Casework', 'topic', 'subtopic', 'comments'],
                    ['30602', 'legal case', 'topic', 'subtopic', 'comments']]
        self.assertEqual(expected, result, "Problem with test for case - type, df")

        # Tests the case remains log was not made.
        result = os.path.exists(os.path.join('test_data', 'case_remains_log.csv'))
        self.assertEqual(False, result, "Problem with test for case - type, case log")

        # Tests the values in the case delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_delete_log.csv'))
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['30600', 'CASE', 'topic', 'subtopic', 'comments'],
                    ['30601', 'Casework', 'topic', 'subtopic', 'comments'],
                    ['30602', 'legal case', 'topic', 'subtopic', 'comments']]
        self.assertEqual(expected, result, "Problem with test for case - type, delete log")

    def test_casework_some(self):
        """Test for when some rows contain the string case and are deleted, and one row is not"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'CASE', 'VET', '', ''],
                              ['30601', 'ITEM', 'CASEWORK', '', 'Q1234'],
                              ['30602', 'ITEM', 'OF-GEN, CASE', '', 'NOTE'],
                              ['30603', 'ITEM', 'OF-GEN', 'Legal Case', ''],
                              ['30604', 'ITEM', 'TR-RAL', '', 'SENT TO CASE WORK, ATL'],
                              ['30605', 'ITEM', 'TR-RAL', '', '']],
                             columns=['zip_code', 'correspondence_type', 'correspondence_topic',
                                      'correspondence_subtopic', 'comments'])
        casework_df = find_casework_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['30600', 'CASE', 'VET', '', ''],
                    ['30601', 'ITEM', 'CASEWORK', '', 'Q1234'],
                    ['30602', 'ITEM', 'OF-GEN, CASE', '', 'NOTE'],
                    ['30603', 'ITEM', 'OF-GEN', 'Legal Case', ''],
                    ['30604', 'ITEM', 'TR-RAL', '', 'SENT TO CASE WORK, ATL']]
        self.assertEqual(expected, result, "Problem with test for casework - some, df")

        # Tests the case remains log was not made.
        result = os.path.exists(os.path.join('test_data', 'case_remains_log.csv'))
        self.assertEqual(False, result, "Problem with test for casework - some, case log")

        # Tests the values in the case delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_delete_log.csv'))
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['30600', 'CASE', 'VET', 'nan', 'nan'],
                    ['30601', 'ITEM', 'CASEWORK', 'nan', 'Q1234'],
                    ['30602', 'ITEM', 'OF-GEN, CASE', 'nan', 'NOTE'],
                    ['30603', 'ITEM', 'OF-GEN', 'Legal Case', 'nan'],
                    ['30604', 'ITEM', 'TR-RAL', 'nan', 'SENT TO CASE WORK, ATL']]
        self.assertEqual(expected, result, "Problem with test for casework - some, delete log")

    def test_no_casework(self):
        """Test for when none of the tested columns contain the string case and nothing is deleted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['CASEYVILLE', 'ITEM', 'PR', '', 'I AM ON IT'],
                              ['ATHENS', 'ITEM', 'OF-GEN', '', 'NOTE'],
                              ['CASE', 'ITEM', 'TR-RAL', '', 'NOTE']],
                             columns=['city', 'correspondence_type', 'correspondence_topic',
                                      'correspondence_subtopic', 'comments'])
        casework_df = find_casework_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['city', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments']]
        self.assertEqual(expected, result, "Problem with test for no casework, df")

        # Tests the values in the case remains log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_remains_log.csv'))
        expected = [['city', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments'],
                    ['CASEYVILLE', 'ITEM', 'PR', 'nan', 'I AM ON IT'],
                    ['CASE', 'ITEM', 'TR-RAL', 'nan', 'NOTE']]
        self.assertEqual(expected, result, "Problem with test for no casework, case log")

        # Tests the values in the case delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_delete_log.csv'))
        expected = [['city', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic', 'comments']]
        self.assertEqual(expected, result, "Problem with test for no casework, delete log")


if __name__ == '__main__':
    unittest.main()
