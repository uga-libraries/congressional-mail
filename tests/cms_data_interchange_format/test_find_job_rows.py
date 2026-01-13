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
        df = pd.DataFrame([['', 'Intern Assignments', ''],
                           ['', 'good job with everything', ''],
                           ['', 'batch intern response', ''],
                           ['', 'INTERNSHIP', ''],
                           ['', 'Jobs Act', '']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['', 'Intern Assignments', '', 'Job_Application'],
                    ['', 'batch intern response', '', 'Job_Application'],
                    ['', 'INTERNSHIP', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['', 'good job with everything', '', 'Job_Application'],
                    ['', 'Jobs Act', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_job_check")

    def test_none(self):
        """Test for when no rows have job applications"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['doc.doc', 'one', 'a'],
                           ['doc.doc', 'two', 'b'],
                           ['doc.doc', 'three', 'c']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_job_check")


if __name__ == '__main__':
    unittest.main()
