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
        md_df = pd.DataFrame([['30600', 'GEN', 'Academy Applicant', 'Nomination', '', '', 'GEN', '', '', '', ''],
                              ['30601', 'GEN', 'Misc', 'Note', '', '', 'GEN', 'Misc', 'Note', '', ''],
                              ['30602', 'GEN', 'Casework', '', '', '', 'GEN', '', '', '', ''],
                              ['30603', 'GEN', 'Admin', '', '', '', 'GEN', 'Recommendations',
                               'wrote recommendation', '', ''],
                              ['30604', 'GEN', 'Social Security', 'Casework candidate', '', '', 'GEN',
                               '', '', '', ''],
                              ['30605', 'GEN', 'Intern', '', r'..\doc\resume.txt', '', 'GEN', '', 'job request',
                               '', ''],
                              ['30606', 'GEN', 'Congratulations', '', '', '', 'GEN', '', 'Good job', '', ''],
                              ['30607', 'GEN', 'Legislation', '', '', '', 'GEN', '', 'Idea noted', '', ''],
                              ['30608', 'GEN', 'Arts', 'International Acad', '', '', 'GEN', '', '', '', ''],
                              ['30609', 'GEN', 'Legal', 'Case against Napster', '', '', 'GEN', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values of the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'GEN', 'Academy Applicant', 'Nomination', '', '', 'GEN', '', '', '', '',
                     'Academy_Application'],
                    ['30602', 'GEN', 'Casework', '', '', '', 'GEN', '', '', '', '', 'Casework'],
                    ['30603', 'GEN', 'Admin', '', '', '', 'GEN', 'Recommendations', 'wrote recommendation', '', '',
                     'Recommendation'],
                    ['30604', 'GEN', 'Social Security', 'Casework candidate', '', '', 'GEN', '', '', '', '',
                     'Casework'],
                    ['30605', 'GEN', 'Intern', '', r'..\doc\resume.txt', '', 'GEN', '', 'job request', '', '',
                     'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for four categories, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'GEN', 'Academy Applicant', 'Nomination', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK',
                     'BLANK', 'BLANK', 'Academy_Application'],
                    ['30602', 'GEN', 'Casework', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'Casework'],
                    ['30603', 'GEN', 'Admin', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'Recommendations',
                     'wrote recommendation', 'BLANK', 'BLANK', 'Recommendation'],
                    ['30604', 'GEN', 'Social Security', 'Casework candidate', 'BLANK', 'BLANK', 'GEN', 'BLANK',
                     'BLANK', 'BLANK', 'BLANK', 'Casework'],
                    ['30605', 'GEN', 'Intern', 'BLANK', r'..\doc\resume.txt', 'BLANK', 'GEN', 'BLANK',
                     'job request', 'BLANK', 'BLANK', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for four categories, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30609', 'GEN', 'Legal', 'Case against Napster', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK',
                     'BLANK', 'BLANK', 'Casework'],
                    ['30606', 'GEN', 'Congratulations', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'Good job',
                     'BLANK', 'BLANK', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for four categories, appraisal check log")

    def test_three(self):
        """Test for when there are three categories for appraisal (academy applications, casework, job application)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'GEN', 'Academy Applicant', 'Nomination', '', '', 'GEN', '', '', '', ''],
                              ['30601', 'GEN', 'Casework', '', '', '', 'GEN', '', '', '', ''],
                              ['30602', 'GEN', 'Misc', 'Note', '', '', 'GEN', 'Misc', 'Note', '', ''],
                              ['30603', 'GEN', 'Social Security', 'Casework candidate', '', '', 'GEN',
                               '', '', '', ''],
                              ['30604', 'GEN', 'Intern', '', '', '', 'GEN', 'job request', '',
                               r'..\doc\resume.txt', ''],
                              ['30605', 'GEN', 'Judicial', 'Napster case', '', '', 'GEN', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values of the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'GEN', 'Academy Applicant', 'Nomination', '', '', 'GEN', '', '', '', '',
                     'Academy_Application'],
                    ['30601', 'GEN', 'Casework', '', '', '', 'GEN', '', '', '', '', 'Casework'],
                    ['30603', 'GEN', 'Social Security', 'Casework candidate', '', '', 'GEN', '', '', '', '',
                     'Casework'],
                    ['30604', 'GEN', 'Intern', '', '', '', 'GEN', 'job request', '', r'..\doc\resume.txt', '',
                     'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for three categories, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'GEN', 'Academy Applicant', 'Nomination', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK',
                     'BLANK', 'BLANK', 'Academy_Application'],
                    ['30601', 'GEN', 'Casework', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'Casework'],
                    ['30603', 'GEN', 'Social Security', 'Casework candidate', 'BLANK', 'BLANK', 'GEN', 'BLANK',
                     'BLANK', 'BLANK', 'BLANK', 'Casework'],
                    ['30604', 'GEN', 'Intern', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'job request', 'BLANK',
                     r'..\doc\resume.txt', 'BLANK', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for three categories, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30605', 'GEN', 'Judicial', 'Napster case', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK',
                     'BLANK', 'BLANK', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for three categories, appraisal check log")

    def test_two(self):
        """Test for when there are two categories for appraisal (academy applications and casework)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'GEN', 'Academy Applicant', 'Nomination', '', '', 'GEN', '', '', '', ''],
                              ['30601', 'GEN', 'Casework', '', '', '', 'GEN', '', '', '', ''],
                              ['30602', 'GEN', 'Misc', 'Note', '', '', 'GEN', 'Misc', 'Note', '', ''],
                              ['30603', 'GEN', 'Social Security', 'Casework candidate', '', '', 'GEN', '', '', '', ''],
                              ['30604', 'GEN', 'Culture', 'Acad Awards', '', '', 'GEN', '', '', '', ''],
                              ['30605', 'GEN', 'Farming', '', '', '', 'GEN', '', '', r'..\doc\case\file.doc', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values of the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'GEN', 'Academy Applicant', 'Nomination', '', '', 'GEN', '', '', '', '',
                     'Academy_Application'],
                    ['30601', 'GEN', 'Casework', '', '', '', 'GEN', '', '', '', '', 'Casework'],
                    ['30603', 'GEN', 'Social Security', 'Casework candidate', '', '', 'GEN', '', '', '', '',
                     'Casework']]
        self.assertEqual(expected, result, "Problem with test for two categories, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'GEN', 'Academy Applicant', 'Nomination', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK',
                     'BLANK', 'BLANK', 'Academy_Application'],
                    ['30601', 'GEN', 'Casework', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'Casework'],
                    ['30603', 'GEN', 'Social Security', 'Casework candidate', 'BLANK', 'BLANK', 'GEN', 'BLANK',
                     'BLANK', 'BLANK', 'BLANK', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for two categories, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30605', 'GEN', 'Farming', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK',
                     r'..\doc\case\file.doc', 'BLANK', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for two categories, appraisal check log")

    def test_one(self):
        """Test for when there is one category for appraisal (casework)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'GEN', 'Casework Issues', '', '', '', 'GEN', 'Casework', '', '', ''],
                              ['30601', 'GEN', 'Health^Casework', 'Note', '', '', 'GEN', '', '', '', ''],
                              ['30602', 'GEN', 'Health', 'GEN interest', '', '', 'GEN', '', 'Note', '', ''],
                              ['30603', 'GEN', 'Social Security', 'Open Case', '', '', 'GEN', '', '', '', ''],
                              ['30604', 'GEN', 'Admin', '', '', '', 'GEN', '', 'For Casey', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'GEN', 'Casework Issues', '', '', '', 'GEN', 'Casework', '', '', '', 'Casework'],
                    ['30601', 'GEN', 'Health^Casework', 'Note', '', '', 'GEN', '', '', '', '', 'Casework'],
                    ['30603', 'GEN', 'Social Security', 'Open Case', '', '', 'GEN', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for one category, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'GEN', 'Casework Issues', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'Casework', 'BLANK',
                     'BLANK', 'BLANK', 'Casework'],
                    ['30601', 'GEN', 'Health^Casework', 'Note', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'Casework'],
                    ['30603', 'GEN', 'Social Security', 'Open Case', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'BLANK',
                     'BLANK', 'BLANK', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for one category, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30604', 'GEN', 'Admin', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'BLANK', 'For Casey', 'BLANK',
                     'BLANK', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for one categories, appraisal check log")

    def test_none(self):
        """Test for when there are no indicators for appraisal"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'GEN', 'Arts', 'In support', '', '', 'GEN', '', '', '', ''],
                              ['30601', 'GEN', 'Healthcare', '', '', '', 'GEN', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for no appraisal, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for no appraisal, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for no categories, appraisal check log")

    def test_multiple(self):
        """Test for when there are rows that match multiple categories for appraisal"""
        md_df = pd.DataFrame([['30600', 'GEN', 'Casework^Academy Applicant', '', '', '', 'GEN', '', '', '', ''],
                              ['30601', 'GEN', 'Academy Applicant', 'Maybe casework', '', '', 'GEN', '',
                               'rec for doe', '', ''],
                              ['30602', 'GEN', 'Legal Case', '', '', '', 'GEN', 'Congrats', 'Good job', '', ''],
                              ['30603', 'GEN', 'Admin', 'note', r'doc\case.txt', '', 'GEN', 'Admin',
                               'recommendation', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values of the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'GEN', 'Casework^Academy Applicant', '', '', '', 'GEN', '', '', '', '',
                     'Academy_Application|Casework'],
                    ['30601', 'GEN', 'Academy Applicant', 'Maybe casework', '', '', 'GEN', '', 'rec for doe', '', '',
                     'Academy_Application|Casework|Recommendation'],
                    ['30603', 'GEN', 'Admin', 'note', r'doc\case.txt', '', 'GEN', 'Admin', 'recommendation', '', '',
                     'Recommendation']
        ]
        self.assertEqual(expected, result, "Problem with test for multiple categories, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'GEN', 'Casework^Academy Applicant', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'BLANK',
                     'BLANK', 'BLANK', 'BLANK', 'Academy_Application|Casework'],
                    ['30601', 'GEN', 'Academy Applicant', 'Maybe casework', 'BLANK', 'BLANK', 'GEN', 'BLANK',
                     'rec for doe', 'BLANK', 'BLANK', 'Academy_Application|Casework|Recommendation'],
                    ['30603', 'GEN', 'Admin', 'note', r'doc\case.txt', 'BLANK', 'GEN', 'Admin', 'recommendation',
                     'BLANK', 'BLANK', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for multiple categories, appraisal delete log")

        # Tests the values in the appraisal check log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30602', 'GEN', 'Legal Case', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'Congrats', 'Good job', 'BLANK',
                     'BLANK', 'Casework'],
                    ['30603', 'GEN', 'Admin', 'note', r'doc\case.txt', 'BLANK', 'GEN', 'Admin', 'recommendation',
                     'BLANK', 'BLANK', 'Casework'],
                    ['30602', 'GEN', 'Legal Case', 'BLANK', 'BLANK', 'BLANK', 'GEN', 'Congrats', 'Good job',
                     'BLANK', 'BLANK', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for multiple categories, appraisal check log")


if __name__ == '__main__':
    unittest.main()
