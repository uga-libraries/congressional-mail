"""
Tests for the function find_job_rows(), 
which finds metadata rows with topics or text that indicate they are job applications and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_data_interchange_format import find_job_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_doc_name(self):
        """Test for when the column communication_document_name indicates job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', 'docs\\job.doc', '', ''],
                           ['20250402', '', 'docs\\JOBAPPS.txt', '', ''],
                           ['20250403', '', 'docs\\First Reply to Resume.txt', '', ''],
                           ['20250404', '', 'docs\\Testing resumed.doc', '', ''],
                           ['20250405', '', 'docs\\Interns - Thank you for resume.doc', '', ''],
                           ['20250406', '', 'docs\\Jobs Act.txt', '', ''],
                           ['20250407', '', 'docs\\Jobs Act.txt', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', 'docs\\job.doc', '', '', 'Job_Application'],
                    ['20250402', '', 'docs\\JOBAPPS.txt', '', '', 'Job_Application'],
                    ['20250403', '', 'docs\\First Reply to Resume.txt', '', '', 'Job_Application'],
                    ['20250405', '', 'docs\\Interns - Thank you for resume.doc', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250406', '', 'docs\\Jobs Act.txt', '', '', 'Job_Application'],
                    ['20250407', '', 'docs\\Jobs Act.txt', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_job_check")

    def test_group_name(self):
        """Test for when the column group_name indicates job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', '', ''],
                           ['20250402', 'jobapps1', '', '', ''],
                           ['20250403', 'JobApp2', '', '', ''],
                           ['20250404', 'Job Request', '', '', ''],
                           ['20250405', 'Jobs Act', '', '', ''],
                           ['20250406', 'RESUME', '', '', ''],
                           ['20250407', 'econ_jobs', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250402', 'jobapps1', '', '', '', 'Job_Application'],
                    ['20250403', 'JobApp2', '', '', '', 'Job_Application'],
                    ['20250404', 'Job Request', '', '', '', 'Job_Application'],
                    ['20250406', 'RESUME', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250405', 'Jobs Act', '', '', '', 'Job_Application'],
                    ['20250407', 'econ_jobs', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_job_check")

    def test_none(self):
        """Test for no patterns indicating job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', 'docs\\doc.txt', 'file.txt', ''],
                           ['20250402', '', 'docs\\doc.txt', '', ''],
                           ['20250403', 'Interviews', 'docs\\doc.txt', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_job_check")

    def test_text(self):
        """Test for when the column communication_document_name indicates job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', '', 'job.doc'],
                           ['20250402', '', '', '', 'JOBAPPS'],
                           ['20250403', '', '', '', 'promising job applicant'],
                           ['20250404', '', '', '', 'First Reply to Resume'],
                           ['20250405', '', '', '', 'Check for job'],
                           ['20250406', '', '', '', 'Thank you for resume - hire'],
                           ['20250407', '', '', '', 'Jobs Act.txt'],
                           ['20250408', '', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', '', '', 'job.doc', 'Job_Application'],
                    ['20250402', '', '', '', 'JOBAPPS', 'Job_Application'],
                    ['20250403', '', '', '', 'promising job applicant', 'Job_Application'],
                    ['20250404', '', '', '', 'First Reply to Resume', 'Job_Application'],
                    ['20250406', '', '', '', 'Thank you for resume - hire', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250405', '', '', '', 'Check for job', 'Job_Application'],
                    ['20250407', '', '', '', 'Jobs Act.txt', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for text, df_job_check")


if __name__ == '__main__':
    unittest.main()
