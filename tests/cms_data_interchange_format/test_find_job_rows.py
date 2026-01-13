"""
Tests for the function find_job_rows(), which finds metadata rows that are or might be job applications
To simplify testing, a small subset of the columns from an export are used
"""
import pandas as pd
import unittest
from cms_data_interchange_format import find_job_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', 'Intern Assignments', ''],
                           ['30601', '', 'good job with everything', ''],
                           ['30602', '', 'batch intern response', ''],
                           ['30603', '', 'INTERNSHIP', ''],
                           ['30604', '', 'Jobs Act', '']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', 'Intern Assignments', '', 'Job_Application'],
                    ['30602', '', 'batch intern response', '', 'Job_Application'],
                    ['30603', '', 'INTERNSHIP', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30601', '', 'good job with everything', '', 'Job_Application'],
                    ['30604', '', 'Jobs Act', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_job_check")

    def test_none(self):
        """Test for when no rows have job applications"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', 'doc.doc', 'one', 'a'],
                           ['30601', 'doc.doc', 'two', 'b'],
                           ['30602', 'doc.doc', 'three', 'c']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_job_check")


if __name__ == '__main__':
    unittest.main()
