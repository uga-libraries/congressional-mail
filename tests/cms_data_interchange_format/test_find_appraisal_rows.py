import os
import pandas as pd
import unittest
from cms_data_interchange_format import find_appraisal_rows
from test_read_metadata_file import df_to_list
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
        md_df = pd.DataFrame([['file_1.doc', 'x', 'y'],
                              ['file_2.doc', 'x', 'y'],
                              ['file_3.doc', 'x', 'y']],
                             columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in appraisal_df are correct.
        result = df_to_list(appraisal_df)
        expected = [['correspondence_document_name', 'code_description', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no appraisal), appraisal_df")

        # Tests the values in appraisal_check_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no appraisal), appraisal_check_log.csv")

        # Tests the values in appraisal_delete_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no appraisal), appraisal_delete_log.csv")

    def test_one(self):
        """Test for when rows match only one appraisal category, if any"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['file_1.doc', 'academy idea', 'x'],
                              ['file_2.doc', 'sports', 'x'],
                              ['file_3.doc', 'summer camp', 'x'],
                              ['file_4.doc', 'x', 'legal > case'],
                              ['file_5.doc', 'casework - forwarded to me for a response', 'x'],
                              ['file_6.doc', 'Internship applicant', 'x'],
                              ['file_7.doc', 'create jobs now', 'x'],
                              ['file_8.doc', 'x', 'academy nomination'],
                              ['file_9.doc', 'good job with this one', 'x']],
                             columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in appraisal_df are correct.
        result = df_to_list(appraisal_df)
        expected = [['correspondence_document_name', 'code_description', 'Appraisal_Category'],
                    ['file_1.doc', 'x', 'Academy_Application'],
                    ['file_5.doc', 'x', 'Casework'],
                    ['file_6.doc', 'x', 'Job_Application'],
                    ['file_8.doc', 'academy nomination', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for one category, appraisal_df")

        # Tests the values in appraisal_check_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_4.doc', 'x', 'legal > case', 'Casework'],
                    ['file_7.doc', 'create jobs now', 'x', 'Job_Application'],
                    ['file_9.doc', 'good job with this one', 'x', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for one category, appraisal_check_log.csv")

        # Tests the values in appraisal_delete_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_1.doc', 'academy idea', 'x', 'Academy_Application'],
                    ['file_5.doc', 'casework - forwarded to me for a response', 'x', 'Casework'],
                    ['file_6.doc', 'Internship applicant', 'x', 'Job_Application'],
                    ['file_8.doc', 'x', 'academy nomination', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for one category, appraisal_delete_log.csv")

    def test_multiple(self):
        """Test for when rows match multiple appraisal categories, if any"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['file_1.doc', 'casework > internship', 'x'],
                              ['file_2.doc', 'x', 'y'],
                              ['file_3.doc', 'internship recommendation letter', 'x'],
                              ['file_4.doc', 'internship recommendation letter closed case file', 'x'],
                              ['file_5.doc', 'rec.doc', 'case > rec']],
                             columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in appraisal_df are correct.
        result = df_to_list(appraisal_df)
        expected = [['correspondence_document_name', 'code_description', 'Appraisal_Category'],
                    ['file_1.doc', 'x', 'Casework|Job_Application'],
                    ['file_3.doc', 'x', 'Job_Application|Recommendation'],
                    ['file_4.doc', 'x', 'Casework|Job_Application|Recommendation']]
        self.assertEqual(expected, result, "Problem with test for multiple categories, appraisal_df")

        # Tests the values in appraisal_check_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_check_log.csv'))
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_5.doc', 'rec.doc', 'case > rec', 'Casework'],
                    ['file_5.doc', 'rec.doc', 'case > rec', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for multiple categories, appraisal_check_log.csv")

        # Tests the values in appraisal_delete_log.csv are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_1.doc', 'casework > internship', 'x', 'Casework|Job_Application'],
                    ['file_3.doc', 'internship recommendation letter', 'x', 'Job_Application|Recommendation'],
                    ['file_4.doc', 'internship recommendation letter closed case file', 'x',
                     'Casework|Job_Application|Recommendation']]
        self.assertEqual(expected, result, "Problem with test for multiple categories, appraisal_delete_log.csv")


if __name__ == '__main__':
    unittest.main()
