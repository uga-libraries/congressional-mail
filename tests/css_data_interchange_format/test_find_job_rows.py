import numpy as np
import unittest
from css_data_interchange_format import find_job_rows
from test_df_search import make_df
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_doc_name(self):
        """Test for when the column communication_document_name indicates job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', '', 'job app', '', ''],
                ['20250402', '', 'intern dc.doc', '', ''],
                ['20250403', '', 'docs\\Interview Officer.txt', '', ''],
                ['20250404', '', 'docs\\INTERNSHIP', '', ''],
                ['20250405', '', '', ''],
                ['20250406', '', 'docs\\Jobs Act.txt', '', ''],
                ['20250407', '', 'docs\\Jobs Act.txt', '', ''],
                ['20250408', '', np.nan, '', ''],
                ['20250409', '', 'docs\\act.txt', '', '']]
        df = make_df(rows)
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', 'job app', '', '', 'Job_Application'],
                    ['20250402', '', 'intern dc.doc', '', '', 'Job_Application'],
                    ['20250403', '', 'docs\\Interview Officer.txt', '', '', 'Job_Application'],
                    ['20250404', '', 'docs\\INTERNSHIP', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250406', '', 'docs\\Jobs Act.txt', '', '', 'Job_Application'],
                    ['20250407', '', 'docs\\Jobs Act.txt', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_job_check")

    def test_file_name(self):
        """Test for when the column file_name indicates job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', '', '', 'resume', ''],
                ['20250402', '', '', 'job.doc.pdf', ''],
                ['20250403', '', '', 'DC JobApp.doc', ''],
                ['20250404', '', '', 'URGENT JOB REQUEST', ''],
                ['20250405', '', '', '', ''],
                ['20250406', '', '', 'good_job.pdf', ''],
                ['20250407', '', '', 'job.pdf', ''],
                ['20250408', '', '', np.nan, ''],
                ['20250409', '', '', 'text.txt', '']]
        df = make_df(rows)
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', '', 'resume', '', 'Job_Application'],
                    ['20250402', '', '', 'job.doc.pdf', '', 'Job_Application'],
                    ['20250403', '', '', 'DC JobApp.doc', '', 'Job_Application'],
                    ['20250404', '', '', 'URGENT JOB REQUEST', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for file_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250406', '', '', 'good_job.pdf', '', 'Job_Application'],
                    ['20250407', '', '', 'job.pdf', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for file_name, df_job_check")

    def test_group_name(self):
        """Test for when the column group_name indicates job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'job app', '', '', ''],
                ['20250402', 'intern dc', '', '', ''],
                ['20250403', 'DC Interview Maybe', '', '', ''],
                ['20250404', 'LOCAL INTERNSHIP', '', '', ''],
                ['20250405', '', '', '', ''],
                ['20250406', 'Jobs Report', '', '', ''],
                ['20250407', 'econ_jobs', '', '', ''],
                ['20250408', np.nan, '', '', ''],
                ['20250409', 'Request', '', '', '']]
        df = make_df(rows)
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'job app', '', '', '', 'Job_Application'],
                    ['20250402', 'intern dc', '', '', '', 'Job_Application'],
                    ['20250403', 'DC Interview Maybe', '', '', '', 'Job_Application'],
                    ['20250404', 'LOCAL INTERNSHIP', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250406', 'Jobs Report', '', '', '', 'Job_Application'],
                    ['20250407', 'econ_jobs', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_job_check")

    def test_none(self):
        """Test for no patterns indicating job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', np.nan, 'docs\\doc.txt', 'file.txt', np.nan],
                ['20250402', '', 'docs\\doc.txt', '', ''],
                ['20250403', 'Admin', 'docs\\doc.txt', '', '']]
        df = make_df(rows)
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
        rows = [['20250401', '', '', '', 'resume'],
                ['20250402', '', '', '', 'job.doc_info'],
                ['20250403', '', '', '', 'Schedule Interview Soon'],
                ['20250404', '', '', '', 'DC INTERNSHIP'],
                ['20250405', '', '', '', ''],
                ['20250406', '', '', '', 'job'],
                ['20250407', '', '', '', 'Jobs Act'],
                ['20250408', '', '', '', np.nan],
                ['20250409', '', '', '', 'Act 123']]
        df = make_df(rows)
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', '', '', 'resume', 'Job_Application'],
                    ['20250402', '', '', '', 'job.doc_info', 'Job_Application'],
                    ['20250403', '', '', '', 'Schedule Interview Soon', 'Job_Application'],
                    ['20250404', '', '', '', 'DC INTERNSHIP', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250406', '', '', '', 'job', 'Job_Application'],
                    ['20250407', '', '', '', 'Jobs Act', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for text, df_job_check")


if __name__ == '__main__':
    unittest.main()
