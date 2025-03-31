"""
Tests for the function find_appraisal_rows(),
which finds metadata rows with topics or text that indicate they are different categories for appraisal 
and return as a df and log results.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from css_archiving_format import find_appraisal_rows
from test_read_metadata import df_to_list
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the log, if made by the test"""
        log_paths = [os.path.join('test_data', 'appraisal_check_log.csv'),
                     os.path.join('test_data', 'appraisal_delete_log.csv')]
        for log_path in log_paths:
            if os.path.exists(log_path):
                os.remove(log_path)

    def test_four(self):
        """Test for when there are all four categories for appraisal
        (academy applications, casework, job application, recommendations)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Academy Applicant', 'Nomination', '', '', '', ''],
                              ['30601', 'General', 'Note', '', 'General', 'Note', ''],
                              ['30602', 'Casework', '', '', '', '', ''],
                              ['30603', 'Admin', '', '', 'Recommendations', 'wrote recommendation', ''],
                              ['30604', 'Social Security', 'Casework candidate', '', '', '', ''],
                              ['30605', 'Intern', '', r'..\doc\resume.txt', 'job request', '', ''],
                              ['30606', 'Congratulations', '', '', '', '', 'Good job'],
                              ['30607', 'Legislation', '', '', '', '', 'Recommendation noted'],
                              ['30608', 'Arts', 'International Academy', '', '', '', ''],
                              ['30609', 'Legal', 'Case against Napster', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text',
                                      'out_document_name'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values of the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    ['30600', 'Academy Applicant', 'Nomination', '', '', '', '', 'Academy_Application'],
                    ['30602', 'Casework', '', '', '', '', '', 'Casework'],
                    ['30603', 'Admin', '', '', 'Recommendations', 'wrote recommendation', '', 'Recommendation'],
                    ['30604', 'Social Security', 'Casework candidate', '', '', '', '', 'Casework'],
                    ['30605', 'Intern', '', r'..\doc\resume.txt', 'job request', '', '', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for four categories, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    [30600, 'Academy Applicant', 'Nomination', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Academy_Application'],
                    [30602, 'Casework', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Casework'],
                    [30603, 'Admin', 'BLANK', 'BLANK', 'Recommendations', 'wrote recommendation', 'BLANK', 'Recommendation'],
                    [30604, 'Social Security', 'Casework candidate', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Casework'],
                    [30605, 'Intern', 'BLANK', r'..\doc\resume.txt', 'job request', 'BLANK', 'BLANK', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for four categories, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    [30608, 'Arts', 'International Academy', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Academy_Application'],
                    [30609, 'Legal', 'Case against Napster', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Casework'],
                    [30606, 'Congratulations', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Good job', 'Job_Application'],
                    [30607, 'Legislation', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Recommendation noted', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for four categories, appraisal check log")

    def test_three(self):
        """Test for when there are three categories for appraisal (academy applications, casework, job application)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Academy Applicant', 'Nomination', '', '', '', ''],
                              ['30601', 'Casework', '', '', '', '', ''],
                              ['30602', 'General', 'Note', '', 'General', 'Note', ''],
                              ['30603', 'Social Security', 'Casework candidate', '', '', '', ''],
                              ['30604', 'Intern', '', '', 'job request', '', r'..\doc\resume.txt'],
                              ['30605', 'Judicial', 'Napster case', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text',
                                      'out_document_name'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values of the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    ['30600', 'Academy Applicant', 'Nomination', '', '', '', '', 'Academy_Application'],
                    ['30601', 'Casework', '', '', '', '', '', 'Casework'],
                    ['30603', 'Social Security', 'Casework candidate', '', '', '', '', 'Casework'],
                    ['30604', 'Intern', '', '', 'job request', '', r'..\doc\resume.txt', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for three categories, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    [30600, 'Academy Applicant', 'Nomination', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Academy_Application'],
                    [30601, 'Casework', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Casework'],
                    [30603, 'Social Security', 'Casework candidate', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Casework'],
                    [30604, 'Intern', 'BLANK', 'BLANK', 'job request', 'BLANK', r'..\doc\resume.txt', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for three categories, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    [30605, 'Judicial', 'Napster case', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for four categories, appraisal check log")

    def test_two(self):
        """Test for when there are two categories for appraisal (academy applications and casework)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Academy Applicant', 'Nomination', '', '', '', ''],
                              ['30601', 'Casework', '', '', '', '', ''],
                              ['30602', 'General', 'Note', '', 'General', 'Note', ''],
                              ['30603', 'Social Security', 'Casework candidate', '', '', '', ''],
                              ['30604', 'Culture', 'Academy Awards', '', '', '', ''],
                              ['30605', 'Farming', '', '', '', '', r'..\doc\case\file.doc']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text',
                                      'out_document_name'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values of the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    ['30600', 'Academy Applicant', 'Nomination', '', '', '', '', 'Academy_Application'],
                    ['30601', 'Casework', '', '', '', '', '', 'Casework'],
                    ['30603', 'Social Security', 'Casework candidate', '', '', '', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for two categories, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    [30600, 'Academy Applicant', 'Nomination', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Academy_Application'],
                    [30601, 'Casework', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Casework'],
                    [30603, 'Social Security', 'Casework candidate', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for two categories, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    [30604, 'Culture', 'Academy Awards', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Academy_Application'],
                    [30605, 'Farming', 'BLANK', 'BLANK', 'BLANK', 'BLANK', r'..\doc\case\file.doc', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for four categories, appraisal check log")

    def test_one(self):
        """Test for when there is one category for appraisal (casework)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Casework Issues', '', '', 'Casework', '', ''],
                              ['30601', 'Health^Casework', 'Note', '', '', '', ''],
                              ['30602', 'Health', 'General interest', '', '', 'Note', ''],
                              ['30603', 'Social Security', 'Open Case', '', '', '', ''],
                              ['30604', 'Admin', '', '', '', 'For Casey', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text',
                                      'out_document_name'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    ['30600', 'Casework Issues', '', '', 'Casework', '', '', 'Casework'],
                    ['30601', 'Health^Casework', 'Note', '', '', '', '', 'Casework'],
                    ['30603', 'Social Security', 'Open Case', '', '', '', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for one category, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    [30600, 'Casework Issues', 'BLANK', 'BLANK', 'Casework', 'BLANK', 'BLANK', 'Casework'],
                    [30601, 'Health^Casework', 'Note', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Casework'],
                    [30603, 'Social Security', 'Open Case', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for one category, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    [30604, 'Admin', 'BLANK', 'BLANK', 'BLANK', 'For Casey', 'BLANK', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for four categories, appraisal check log")

    def test_none(self):
        """Test for when there are no indicators for appraisal"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Arts', 'In support', '', '', '', ''],
                              ['30601', 'Healthcare', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text',
                                      'out_document_name'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for no appraisal, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for no appraisal, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for four categories, appraisal check log")

    def test_multiple(self):
        """Test for when there are rows that match multiple categories for appraisal"""
        md_df = pd.DataFrame([['30600', 'Casework^Academy Applicant', '', '', '', '', ''],
                              ['30601', 'Academy Applicant', 'Maybe casework', '', '', 'rec for doe', ''],
                              ['30602', 'Legal Case', '', '', 'Congrats', 'Good job', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text',
                                      'out_document_name'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values of the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    ['30600', 'Casework^Academy Applicant', '', '', '', '', '', 'Academy_Application|Casework'],
                    ['30601', 'Academy Applicant', 'Maybe casework', '', '', 'rec for doe', '',
                     'Academy_Application|Casework|Recommendation']]
        self.assertEqual(result, expected, "Problem with test for multiple categories, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    [30600, 'Casework^Academy Applicant', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'Academy_Application|Casework'],
                    [30601, 'Academy Applicant', 'Maybe casework', 'BLANK', 'BLANK', 'rec for doe', 'BLANK',
                     'Academy_Application|Casework|Recommendation']]
        self.assertEqual(result, expected, "Problem with test for four categories, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'out_topic', 'out_text', 'out_document_name',
                     'Appraisal_Category'],
                    [30602, 'Legal Case', 'BLANK', 'BLANK', 'Congrats', 'Good job', 'BLANK', 'Casework'],
                    [30602, 'Legal Case', 'BLANK', 'BLANK', 'Congrats', 'Good job', 'BLANK', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for multiple categories, appraisal check log")


if __name__ == '__main__':
    unittest.main()
