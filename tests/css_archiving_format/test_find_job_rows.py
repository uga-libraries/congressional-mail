import numpy as np
import unittest
from css_archiving_format import find_job_rows
from test_df_search import make_df
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_in_document_name(self):
        """Test for when column in_document_name contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '..\\doc\\job_file.txt', '', '', '', '', ''],
                ['30601', '', '', '..\\doc\\jobs\\file.doc', '', '', '', '', ''],
                ['30602', '', '', '..\\doc\\file.doc', '', '', '', '', ''],
                ['30603', '', '', 'internship', '', '', '', '', ''],
                ['30604', '', '', 'interview.doc', '', '', '', '', ''],
                ['30605', '', '', '..\\doc\\Intern App.doc', '', '', '', '', ''],
                ['30606', '', '', '..\\doc\\JOB APP', '', '', '', '', ''],
                ['30607', '', '', '', '', '', '', '', ''],
                ['30608', '', '', np.nan, '', '', '', '', '']]
        md_df = make_df(rows)                     
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', 'internship', '', '', '', '', '', 'Job_Application'],
                    ['30604', '', '', 'interview.doc', '', '', '', '', '', 'Job_Application'],
                    ['30605', '', '', '..\\doc\\Intern App.doc', '', '', '', '', '', 'Job_Application'],
                    ['30606', '', '', '..\\doc\\JOB APP', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '..\\doc\\job_file.txt', '', '', '', '', '', 'Job_Application'],
                    ['30601', '', '', '..\\doc\\jobs\\file.doc', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job_check")

    def test_in_fillin(self):
        """Test for when column in_fillin contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', 'check if job', '', '', '', ''],
                ['30601', '', '', '', 'job', '', '', '', ''],
                ['30602', '', '', '', 'text', '', '', '', ''],
                ['30603', '', '', '', 'job request', '', '', '', ''],
                ['30604', '', '', '', 'jobapp_info', '', '', '', ''],
                ['30605', '', '', '', 'Send Job.doc file', '', '', '', ''],
                ['30606', '', '', '', 'ASK RESUME', '', '', '', ''],
                ['30607', '', '', '', '', '', '', '', ''],
                ['30608', '', '', '', np.nan, '', '', '', '']]
        md_df = make_df(rows)
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', 'job request', '', '', '', '', 'Job_Application'],
                    ['30604', '', '', '', 'jobapp_info', '', '', '', '', 'Job_Application'],
                    ['30605', '', '', '', 'Send Job.doc file', '', '', '', '', 'Job_Application'],
                    ['30606', '', '', '', 'ASK RESUME', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_fillin, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', 'check if job', '', '', '', '', 'Job_Application'],
                    ['30601', '', '', '', 'job', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_fillin, df_job_check")

    def test_in_text(self):
        """Test for when column in_text contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', 'Freelance job', '', '', '', '', '', ''],
                ['30601', '', 'JOB', '', '', '', '', '', ''],
                ['30602', '', 'Request', '', '', '', '', '', ''],
                ['30603', '', 'internship', '', '', '', '', '', ''],
                ['30604', '', 'interview_yes', '', '', '', '', '', ''],
                ['30605', '', 'New Intern DC', '', '', '', '', '', ''],
                ['30606', '', 'NEW JOB APP', '', '', '', '', '', ''],
                ['30607', '', '', '', '', '', '', '', ''],
                ['30608', '', np.nan, '', '', '', '', '', '']]
        md_df = make_df(rows)
        df_job, df_job_check = find_job_rows(md_df)
        
        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', 'internship', '', '', '', '', '', '', 'Job_Application'],
                    ['30604', '', 'interview_yes', '', '', '', '', '', '', 'Job_Application'],
                    ['30605', '', 'New Intern DC', '', '', '', '', '', '', 'Job_Application'],
                    ['30606', '', 'NEW JOB APP', '', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', 'Freelance job', '', '', '', '', '', '', 'Job_Application'],
                    ['30601', '', 'JOB', '', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_job_check")

    def test_in_topic(self):
        """Test for when column in_topic contains one of the topics indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'Job^General', '', '', '', '', '', '', ''],
                ['30601', 'Job Hunting', '', '', '', '', '', '', ''],
                ['30602', 'Parks', '', '', '', '', '', '', ''],
                ['30603', 'job request', '', '', '', '', '', '', ''],
                ['30604', 'jobapp_2', '', '', '', '', '', '', ''],
                ['30605', 'Sent Job.doc Already', '', '', '', '', '', '', ''],
                ['30606', 'REQUEST RESUME', '', '', '', '', '', '', ''],
                ['30607', '', '', '', '', '', '', '', ''],
                ['30608', np.nan, '', '', '', '', '', '', '']]
        md_df = make_df(rows)
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', 'job request', '', '', '', '', '', '', '', 'Job_Application'],
                    ['30604', 'jobapp_2', '', '', '', '', '', '', '', 'Job_Application'],
                    ['30605', 'Sent Job.doc Already', '', '', '', '', '', '', '', 'Job_Application'],
                    ['30606', 'REQUEST RESUME', '', '', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Job^General', '', '', '', '', '', '', '', 'Job_Application'],
                    ['30601', 'Job Hunting', '', '', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_job_check")

    def test_none(self):
        """Test for when no patterns indicating job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'Farms', '', '', '', '', 'Note', '', ''],
                ['30601', 'Cats', np.nan, np.nan, np.nan, 'Cats', np.nan, np.nan, np.nan],
                ['30602', 'Economy', '', '', '', 'Econ Plan', '', '..\\doc\\econ-outlook.doc', '']]
        md_df = make_df(rows)
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched), df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched), df_job_check")

    def test_out_document_name(self):
        """Test for when column out_document_name contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', '', '', '..\\doc\\Doe Job.txt', ''],
                ['30601', '', '', '', '', '', '', '..\\doc\\job_file.txt', ''],
                ['30602', '', '', '', '', '', '', '..\\doc\\file.txt', ''],
                ['30603', '', '', '', '', '', '', '', 'internship'],
                ['30604', '', '', '', '', '', '', 'interview.doc', ''],
                ['30605', '', '', '', '', '', '', '..\\Doc\\Intern DC.doc', ''],
                ['30606', '', '', '', '', '', '', '..\\doc\\JOB APP', ''],
                ['30607', '', '', '', '', '', '', '', ''],
                ['30608', '', '', '', '', '', '', np.nan, '']]
        md_df = make_df(rows)
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', '', '', 'internship', 'Job_Application'],
                    ['30604', '', '', '', '', '', '', 'interview.doc', '', 'Job_Application'],
                    ['30605', '', '', '', '', '', '', '..\\Doc\\Intern DC.doc', '', 'Job_Application'],
                    ['30606', '', '', '', '', '', '', '..\\doc\\JOB APP', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', '', '..\\doc\\Doe Job.txt', '', 'Job_Application'],
                    ['30601', '', '', '', '', '', '', '..\\doc\\job_file.txt', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job_check")

    def test_out_fillin(self):
        """Test for when column out_fillin contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', '', '', '', 'check if job'],
                ['30601', '', '', '', '', '', '', '', 'second jobs'],
                ['30602', '', '', '', '', '', '', '', 'request form'],
                ['30603', '', '', '', '', '', '', '', 'job request'],
                ['30604', '', '', '', '', '', '', '', 'jobapp_local'],
                ['30605', '', '', '', '', '', '', '', 'Sent Job.doc Today'],
                ['30606', '', '', '', '', '', '', '', 'REVIEW RESUME'],
                ['30607', '', '', '', '', '', '', '', ''],
                ['30608', '', '', '', '', '', '', '', np.nan]]
        md_df = make_df(rows)
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', '', '', 'job request', 'Job_Application'],
                    ['30604', '', '', '', '', '', '', '', 'jobapp_local', 'Job_Application'],
                    ['30605', '', '', '', '', '', '', '', 'Sent Job.doc Today', 'Job_Application'],
                    ['30606', '', '', '', '', '', '', '', 'REVIEW RESUME', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', '', '', 'check if job', 'Job_Application'],
                    ['30601', '', '', '', '', '', '', '', 'second jobs', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_job_check")

    def test_out_text(self):
        """Test for when column out_text contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', '', 'Job numbers', '', ''],
                ['30601', '', '', '', '', '', 'District Job', '', ''],
                ['30602', '', '', '', '', '', 'report', '', ''],
                ['30603', '', '', '', '', '', 'internship', '', ''],
                ['30604', '', '', '', '', '', 'interview_sarah', '', ''],
                ['30605', '', '', '', '', '', 'DC Intern Orientation', '', ''],
                ['30606', '', '', '', '', '', 'CHECK JOB APP', '', ''],
                ['30607', '', '', '', '', '', '', '', ''],
                ['30608', '', '', '', '', '', np.nan, '', '']]
        md_df = make_df(rows)
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', 'internship', '', '', 'Job_Application'],
                    ['30604', '', '', '', '', '', 'interview_sarah', '', '', 'Job_Application'],
                    ['30605', '', '', '', '', '', 'DC Intern Orientation', '', '', 'Job_Application'],
                    ['30606', '', '', '', '', '', 'CHECK JOB APP', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', 'Job numbers', '', '', 'Job_Application'],
                    ['30601', '', '', '', '', '', 'District Job', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_job_check")

    def test_out_topic(self):
        """"Test for when column out_topic contains one of the topics indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', 'JOB OUTLOOK', '', '', ''],
                ['30601', '', '', '', '', 'Admin^Job', '', '', ''],
                ['30602', '', '', '', '', 'Admin', '', '', ''],
                ['30603', '', '', '', '', 'job request', '', '', ''],
                ['30604', '', '', '', '', 'jobapplication', '', '', ''],
                ['30605', '', '', '', '', 'DC Intern App', '', '', ''],
                ['30606', '', '', '', '', 'UPDATE JOB APP', '', '', ''],
                ['30607', '', '', '', '', '', '', '', ''],
                ['30608', '', '', '', '', np.nan, '', '', '']]
        md_df = make_df(rows)
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', 'job request', '', '', '', 'Job_Application'],
                    ['30604', '', '', '', '', 'jobapplication', '', '', '', 'Job_Application'],
                    ['30605', '', '', '', '', 'DC Intern App', '', '', '', 'Job_Application'],
                    ['30606', '', '', '', '', 'UPDATE JOB APP', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text', 
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', 'JOB OUTLOOK', '', '', '', 'Job_Application'],
                    ['30601', '', '', '', '', 'Admin^Job', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_job_check")

        
if __name__ == '__main__':
    unittest.main()
