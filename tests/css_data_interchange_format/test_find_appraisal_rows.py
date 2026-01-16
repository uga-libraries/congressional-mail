"""
Tests for the function find_appraisal_rows(),
which finds metadata rows with topics or text that indicate they are different categories for appraisal
and return as a df and log results.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from css_data_interchange_format import find_appraisal_rows
from test_appraisal_check_df import df_to_list
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the log, if made by the test"""
        log_paths = [os.path.join('test_data', 'appraisal_check_log.csv'),
                     os.path.join('test_data', 'appraisal_delete_log.csv')]
        for log_path in log_paths:
            if os.path.exists(log_path):
                os.remove(log_path)

    def test_all_multiple(self):
        """Test for when all appraisal categories are present and reach row matches multiple categories"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['20240101', 'case1', r'..\documents\academy rejection.txt', 'academy rejection.txt', 'x'],
                              ['20240202', 'academy 01', r'..\documents\formletters\good job.doc', 'good job.doc', 'x'],
                              ['20240303', 'case admin', r'..\documents\formletters\good job.doc', 'good job.doc', 'x'],
                              ['20240404', 'academy02', r'..\documents\casework\good job.doc', 'good job.doc', 'x']],
                             columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in appraisal_df are correct.
        result = df_to_list(appraisal_df)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category'],
                    ['20240101', 'case1', r'..\documents\academy rejection.txt', 'academy rejection.txt',
                     'Academy_Application|Casework'],
                    ['20240202', 'academy 01', r'..\documents\formletters\good job.doc', 'good job.doc',
                     'Academy_Application|Job_Application'],
                    ['20240303', 'case admin', r'..\documents\formletters\good job.doc', 'good job.doc',
                     'Casework|Job_Application'],
                    ['20240404', 'academy02', r'..\documents\casework\good job.doc', 'good job.doc',
                     'Academy_Application|Casework|Job_Application']]
        self.assertEqual(expected, result, "Problem with test for all - multiple, appraisal_df")

        # Tests the values in appraisal_check_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for all - multiple, appraisal_check_log.csv")

        # Tests the values in appraisal_delete_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20240101', 'case1', r'..\documents\academy rejection.txt', 'academy rejection.txt', 'x',
                     'Academy_Application|Casework'],
                    ['20240202', 'academy 01', r'..\documents\formletters\good job.doc', 'good job.doc', 'x',
                     'Academy_Application|Job_Application'],
                    ['20240303', 'case admin', r'..\documents\formletters\good job.doc', 'good job.doc', 'x',
                     'Casework|Job_Application'],
                    ['20240404', 'academy02', r'..\documents\casework\good job.doc', 'good job.doc', 'x',
                     'Academy_Application|Casework|Job_Application']]
        self.assertEqual(expected, result, "Problem with test for all - multiple, appraisal_delete_log.csv")

    def test_all_single(self):
        """Test for when all appraisal categories are present and each row matches a single category"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['20240101', 'Admin', r'..\documents\objects\academy.txt', 'academy.txt', 'x'],
                              ['20240202', 'Case1', '', '', 'x'],
                              ['20240303', 'jobapp', r'..\documents\objects\position.txt', 'position.txt', 'x'],
                              ['20240404', 'Arts', '', 'artist recommendation.txt', 'x'],
                              ['20240505', 'Admin', r'..\documents\objects\intern rec.txt', '', 'x'],
                              ['20240606', 'Admin',  '', 'legal_case.txt', 'x']],
                             columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in appraisal_df are correct.
        result = df_to_list(appraisal_df)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category'],
                    ['20240101', 'Admin', r'..\documents\objects\academy.txt', 'academy.txt', 'Academy_Application'],
                    ['20240202', 'Case1', '', '', 'Casework'],
                    ['20240303', 'jobapp', r'..\documents\objects\position.txt', 'position.txt', 'Job_Application'],
                    ['20240505', 'Admin', r'..\documents\objects\intern rec.txt', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for all - single, appraisal_df")

        # Tests the values in appraisal_check_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20240606', 'Admin', 'BLANK', 'legal_case.txt', 'x', 'Casework'],
                    ['20240404', 'Arts', 'BLANK', 'artist recommendation.txt', 'x', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for all - single, appraisal_check_log.csv")

        # Tests the values in appraisal_delete_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20240101', 'Admin', r'..\documents\objects\academy.txt', 'academy.txt', 'x', 'Academy_Application'],
                    ['20240202', 'Case1', 'BLANK', 'BLANK', 'x', 'Casework'],
                    ['20240303', 'jobapp', r'..\documents\objects\position.txt', 'position.txt', 'x', 'Job_Application'],
                    ['20240505', 'Admin', r'..\documents\objects\intern rec.txt', 'BLANK', 'x', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for all - single, appraisal_delete_log.csv")

    def test_one(self):
        """Test for when only one appraisal category is present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['20240101', 'CASE1', '', '', 'x'],
                              ['20240202', 'case 2', '', '', 'x'],
                              ['20240303', 'Arts', '', '', 'x'],
                              ['20240404', 'Case3', r'..\documents\casework\3.txt', '3.txt', 'x'],
                              ['20240505', 'Econ', r'..\documents\objects\case.txt', 'case.txt', 'x'],
                              ['20240506', 'Econ', r'..\documents\casework\3.txt', '3.txt', 'x']],
                             columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in appraisal_df are correct.
        result = df_to_list(appraisal_df)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category'],
                    ['20240101', 'CASE1', '', '', 'Casework'],
                    ['20240202', 'case 2', '', '', 'Casework'],
                    ['20240404', 'Case3', r'..\documents\casework\3.txt', '3.txt', 'Casework'],
                    ['20240506', 'Econ', r'..\documents\casework\3.txt', '3.txt', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for one, appraisal_df")

        # Tests the values in appraisal_check_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20240505', 'Econ', r'..\documents\objects\case.txt', 'case.txt', 'x', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for one, appraisal_check_log.csv")

        # Tests the values in appraisal_delete_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20240101', 'CASE1', 'BLANK', 'BLANK', 'x', 'Casework'],
                    ['20240202', 'case 2', 'BLANK', 'BLANK', 'x', 'Casework'],
                    ['20240404', 'Case3', r'..\documents\casework\3.txt', '3.txt', 'x', 'Casework'],
                    ['20240506', 'Econ', r'..\documents\casework\3.txt', '3.txt', 'x', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for one, appraisal_delete_log.csv")

    def test_none(self):
        """Test for when no rows match any appraisal categories"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['20240101', 'arts', r'..\documents\objects\a1.txt', 'a1.txt', 'x'],
                              ['20240202', 'Science', '', '', 'x'],
                              ['20240303', 'Pets', '', '', 'x']],
                             columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in appraisal_df are correct.
        result = df_to_list(appraisal_df)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for something, appraisal_df")

        # Tests the values in appraisal_check_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for something, appraisal_check_log.csv")

        # Tests the values in appraisal_delete_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for something, appraisal_delete_log.csv")


if __name__ == '__main__':
    unittest.main()
