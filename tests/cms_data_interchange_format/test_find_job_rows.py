import numpy as np
import unittest
from cms_data_interchange_format import find_job_rows
from test_df_search import make_df
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_code_desc(self):
        """Test for when the column code_description indicates job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', 'JOB'],
                ['30601', '', '', 'Job^Admin'],
                ['30602', '', '', ''],
                ['30603', '', '', 'internship'],
                ['30604', '', '', 'interview_dc'],
                ['30605', '', '', 'DC Intern Orientation'],
                ['30606', '', '', 'NEW JOB APP'],
                ['30607', '', '', np.nan],
                ['30608', '', '', 'Admin']]
        df = make_df(rows)
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30603', '', '', 'internship', 'Job_Application'],
                    ['30604', '', '', 'interview_dc', 'Job_Application'],
                    ['30605', '', '', 'DC Intern Orientation', 'Job_Application'],
                    ['30606', '', '', 'NEW JOB APP', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', '', 'JOB', 'Job_Application'],
                    ['30601', '', '', 'Job^Admin', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_job_check")

    def test_corr_doc(self):
        """Test for when the column correspondence_document_name indicates job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'job_doc', '', ''],
                ['30601', 'job_doc2', '', ''],
                ['30602', '', '', ''],
                ['30603', 'job request', '', ''],
                ['30604', 'jobapp.txt', '', ''],
                ['30605', '\\doc\\Job.DOC.PDF', '', ''],
                ['30606', '\\doc\\RESUME', '', ''],
                ['30607', np.nan, '', ''],
                ['30608', '\\doc\\text.pdf', '', '']]
        df = make_df(rows)
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30603', 'job request', '', '', 'Job_Application'],
                    ['30604', 'jobapp.txt', '', '', 'Job_Application'],
                    ['30605', '\\doc\\Job.DOC.PDF', '', '', 'Job_Application'],
                    ['30606', '\\doc\\RESUME', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', 'job_doc', '', '', 'Job_Application'],
                    ['30601', 'job_doc2', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_job_check")

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', 'good job', ''],
                ['30601', '', 'jobless numbers down', ''],
                ['30602', '', '', ''],
                ['30603', '', 'internship', ''],
                ['30604', '', 'interview_reschedule', ''],
                ['30605', '', 'New Intern Orientation', ''],
                ['30606', '', 'CHECK JOB APP', ''],
                ['30607', '', np.nan, ''],
                ['30608', '', 'good', '']]
        df = make_df(rows)
        df_job, df_job_check = find_job_rows(df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30603', '', 'internship', '', 'Job_Application'],
                    ['30604', '', 'interview_reschedule', '', 'Job_Application'],
                    ['30605', '', 'New Intern Orientation', '', 'Job_Application'],
                    ['30606', '', 'CHECK JOB APP', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', 'good job', '', 'Job_Application'],
                    ['30601', '', 'jobless numbers down', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_job_check")

    def test_none(self):
        """Test for when no rows have job applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', np.nan, '', 'text'],
                ['30601', 'text', np.nan, ''],
                ['30602', '', 'text', np.nan]]
        df = make_df(rows)
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
