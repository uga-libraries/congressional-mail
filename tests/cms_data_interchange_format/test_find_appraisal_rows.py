"""
Tests for the function find_appraisal_rows(),
which metadata rows for all the categories for appraisal, return df and log results
To simplify input, tests use dataframes with a few the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from cms_data_interchange_format import find_appraisal_rows
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

    def test_none(self):
        """Test for when no rows match any appraisal categories"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['20240101', 'A', 'file.doc', 'x'],
                              ['20240202', 'B', 'file.doc', 'x'],
                              ['20240303', 'C', 'file.doc', 'x']],
                             columns=['date_in', 'correspondence_code', 'correspondence_document_name',
                                      'correspondence_text'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in appraisal_df are correct.
        result = df_to_list(appraisal_df)
        expected = [['date_in', 'correspondence_code', 'correspondence_document_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no appraisal), appraisal_df")

        # Tests the values in appraisal_check_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['date_in', 'correspondence_code', 'correspondence_document_name', 'correspondence_text',
                     'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no appraisal), appraisal_check_log.csv")

        # Tests the values in appraisal_delete_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['date_in', 'correspondence_code', 'correspondence_document_name', 'correspondence_text',
                     'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no appraisal), appraisal_delete_log.csv")

    def test_one(self):
        """Test for when rows match only one appraisal category, if any"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['20240101', 'A', 'file.doc', 'academy issue'],
                              ['20240202', 'B', 'file.doc', 'sports academy'],
                              ['20240303', 'C', 'file.doc', 'summer camp'],
                              ['20240404', 'D', 'file.doc', 'casework - forwarded to me for a response'],
                              ['20240505', 'E', 'file.doc', 'Internship applicant'],
                              ['20240606', 'F', 'file.doc', 'create jobs now'],
                              ['20240707', 'G', 'file.doc', 'good job with this one']],
                             columns=['date_in', 'correspondence_code', 'correspondence_document_name',
                                      'correspondence_text'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in appraisal_df are correct.
        result = df_to_list(appraisal_df)
        expected = [['date_in', 'correspondence_code', 'correspondence_document_name', 'Appraisal_Category'],
                    ['20240101', 'A', 'file.doc', 'Academy_Application'],
                    ['20240404', 'D', 'file.doc', 'Casework'],
                    ['20240505', 'E', 'file.doc', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for one category, appraisal_df")

        # Tests the values in appraisal_check_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['date_in', 'correspondence_code', 'correspondence_document_name', 'correspondence_text',
                     'Appraisal_Category'],
                    ['20240202', 'B', 'file.doc', 'sports academy', 'Academy_Application'],
                    ['20240606', 'F', 'file.doc', 'create jobs now', 'Job_Application'],
                    ['20240707', 'G', 'file.doc', 'good job with this one', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for one category, appraisal_check_log.csv")

        # Tests the values in appraisal_delete_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['date_in', 'correspondence_code', 'correspondence_document_name', 'correspondence_text',
                     'Appraisal_Category'],
                    ['20240101', 'A', 'file.doc', 'academy issue', 'Academy_Application'],
                    ['20240404', 'D', 'file.doc', 'casework - forwarded to me for a response', 'Casework'],
                    ['20240505', 'E', 'file.doc', 'Internship applicant', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for one category, appraisal_delete_log.csv")

    def test_multiple(self):
        """Test for when rows match multiple appraisal categories, if any"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['20240101', 'A', 'file.doc', 'casework - internship'],
                              ['20240202', 'B', 'file.doc', 'x'],
                              ['20240303', 'C', 'file.doc', 'internship recommendation letter'],
                              ['20240404', 'D', 'file.doc', 'Closed case file for internship recommendation letter'],
                              ['20240505', 'E', 'recommendation.doc', 'case']],
                             columns=['date_in', 'correspondence_code', 'correspondence_document_name',
                                      'correspondence_text'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in appraisal_df are correct.
        result = df_to_list(appraisal_df)
        expected = [['date_in', 'correspondence_code', 'correspondence_document_name', 'Appraisal_Category'],
                    ['20240101', 'A', 'file.doc', 'Casework|Job_Application'],
                    ['20240303', 'C', 'file.doc', 'Job_Application|Recommendation'],
                    ['20240404', 'D', 'file.doc', 'Casework|Job_Application|Recommendation']]
        self.assertEqual(result, expected, "Problem with test for multiple categories, appraisal_df")

        # Tests the values in appraisal_check_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['date_in', 'correspondence_code', 'correspondence_document_name', 'correspondence_text',
                     'Appraisal_Category'],
                    ['20240505', 'E', 'recommendation.doc', 'case', 'Casework'],
                    ['20240505', 'E', 'recommendation.doc', 'case', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for multiple categories, appraisal_check_log.csv")

        # Tests the values in appraisal_delete_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['date_in', 'correspondence_code', 'correspondence_document_name', 'correspondence_text',
                     'Appraisal_Category'],
                    ['20240101', 'A', 'file.doc', 'casework - internship', 'Casework|Job_Application'],
                    ['20240303', 'C', 'file.doc', 'internship recommendation letter', 'Job_Application|Recommendation'],
                    ['20240404', 'D', 'file.doc', 'Closed case file for internship recommendation letter',
                     'Casework|Job_Application|Recommendation']]
        self.assertEqual(result, expected, "Problem with test for multiple categories, appraisal_delete_log.csv")


if __name__ == '__main__':
    unittest.main()
