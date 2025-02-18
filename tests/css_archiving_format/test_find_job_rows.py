"""
Tests for the function find_job_rows(),
which finds metadata rows with topics or text that indicate they are job applications and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_archiving_format import find_job_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_all(self):
        """Test for when all patterns indicating job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Resume', 'job request', 'Resume', 'job request', r'..\doc\resume.txt'],
                              ['30601', '', '', 'Intern', 'summer job request', r'..\doc\job interview.doc'],
                              ['30602', 'Intern', '', 'Resume', '', ''],
                              ['30603', 'Resume', 'job request', '', '', ''],
                              ['30604', '', 'Job Request', '', 'job request', ''],
                              ['30605', 'Admin', 'job request', 'Resume', '', r'..\doc\resume.txt']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name'])
        df_job = find_job_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name', 'Appraisal_Category'],
                    ['30602', 'Intern', '', 'Resume', '', '', 'Job_Application'],
                    ['30601', '', '', 'Intern', 'summer job request', r'..\doc\job interview.doc', 'Job_Application'],
                    ['30600', 'Resume', 'job request', 'Resume', 'job request', r'..\doc\resume.txt', 'Job_Application'],
                    ['30603', 'Resume', 'job request', '', '', '', 'Job_Application'],
                    ['30604', '', 'Job Request', '', 'job request', '', 'Job_Application'],
                    ['30605', 'Admin', 'job request', 'Resume', '', r'..\doc\resume.txt', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for all patterns")

    def test_in_text(self):
        """Test for when column in_text contains "job request" (case-insensitive)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Gen', ' new job request', 'Gen', 'info sent', ''],
                              ['30601', 'Admin', 'job requested', 'Admin', '', r'..\doc\response.doc'],
                              ['30602', '', 'Job Request', '', '', ''],
                              ['30603', 'Arts', '', '', '', ''],
                              ['30604', '', 'note', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name'])
        df_job = find_job_rows(md_df)
        
        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name', 'Appraisal_Category'],
                    ['30600', 'Gen', ' new job request', 'Gen', 'info sent', '', 'Job_Application'],
                    ['30601', 'Admin', 'job requested', 'Admin', '', r'..\doc\response.doc', 'Job_Application'],
                    ['30602', '', 'Job Request', '', '', '', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for in_text")

    def test_in_topic(self):
        """Test for when column in_topic contains one of the topics indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Intern^General', '', '', '', ''],
                              ['30601', 'Admin^Resumes', '', '', 'Note', ''],
                              ['30602', 'Housing', '', 'Housing', '', ''],
                              ['30603', 'Resumes', '', 'Economy', '', ''],
                              ['30604', 'Intern', '', '', '', ''],
                              ['30605', 'Music', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name'])
        df_job = find_job_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name', 'Appraisal_Category'],
                    ['30600', 'Intern^General', '', '', '', '', 'Job_Application'],
                    ['30601', 'Admin^Resumes', '', '', 'Note', '', 'Job_Application'],
                    ['30603', 'Resumes', '', 'Economy', '', '', 'Job_Application'],
                    ['30604', 'Intern', '', '', '', '', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for all patterns")

    def test_none(self):
        """Test for when no patterns indicating job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Farms', '', '', 'Note', ''],
                              ['30601', 'Cats', '', 'Cats', '', ''],
                              ['30602', 'Economy', '', 'Econ Plan', '', r'..\doc\econ-outlook.doc']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name'])
        df_job = find_job_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no patterns matched)")

    def test_out_document_name(self):
        """Test for when column out_document_name contains "job interview" or "resume.txt" (case-insensitive)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Admin', '', '', '', r'..\doc\Doe Job Interview.txt'],
                              ['30601', 'Arts', '', '', '', r'..\doc\file.txt'],
                              ['30602', 'Admin', '', 'Admin', 'Files', r'..\doc\resume.txt'],
                              ['30603', '', '', '', 'Note', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name'])
        df_job = find_job_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name', 'Appraisal_Category'],
                    ['30600', 'Admin', '', '', '', r'..\doc\Doe Job Interview.txt', 'Job_Application'],
                    ['30602', 'Admin', '', 'Admin', 'Files', r'..\doc\resume.txt', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for all patterns")

    def test_out_text(self):
        """Test for when column out_text contains "job request" (case-insensitive)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Farms', '', 'Agriculture', 'Note', ''],
                              ['30601', 'Admin', '', 'Admin', 'District Job Request', ''],
                              ['30602', '', '', 'Economy', '', ''],
                              ['30603', '', '', '', 'job request', ''],
                              ['30604', 'Admin', '', '', 'job request - accept', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name'])
        df_job = find_job_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name', 'Appraisal_Category'],
                    ['30601', 'Admin', '', 'Admin', 'District Job Request', '', 'Job_Application'],
                    ['30603', '', '', '', 'job request', '', 'Job_Application'],
                    ['30604', 'Admin', '', '', 'job request - accept', '', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for out_text")

    def test_out_topic(self):
        """"Test for when column out_topic contains one of the topics indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', 'Economy', 'text', r'..\doc\form\econ.doc'],
                              ['30601', '', '', 'Gen^Resumes', '', ''],
                              ['30602', '', '', 'Intern', '', ''],
                              ['30603', '', '', 'Intern^Admin', 'note', ''],
                              ['30604', '', '', 'Water', '', ''],
                              ['30605', '', '', 'Resumes', 'note', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name'])
        df_job = find_job_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'out_document_name', 'Appraisal_Category'],
                    ['30601', '', '', 'Gen^Resumes', '', '', 'Job_Application'],
                    ['30602', '', '', 'Intern', '', '', 'Job_Application'],
                    ['30603', '', '', 'Intern^Admin', 'note', '', 'Job_Application'],
                    ['30605', '', '', 'Resumes', 'note', '', 'Job_Application']]
        self.assertEqual(result, expected, "Problem with test for out_topic")

        
if __name__ == '__main__':
    unittest.main()
