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

    def test_in_document_name(self):
        """Test for when column in_document_name contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', r'..\doc\Doe Job Interview.txt', '', '', '', '', ''],
                              ['30601', '', '', r'..\doc\job_file.txt', '', '', '', '', ''],
                              ['30602', '', '', r'..\doc\resume.txt', '', '', '', '', ''],
                              ['30603', '', '', '', '', '', '', '', ''],
                              ['30604', '', '', r'..\doc\jobs\file.doc', '', '', '', '', ''],
                              ['30605', '', '', r'..\doc\jobs\Resume_Regret.doc', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', r'..\doc\Doe Job Interview.txt', '', '', '', '', '', 'Job_Application'],
                    ['30602', '', '', r'..\doc\resume.txt', '', '', '', '', '', 'Job_Application'],
                    ['30605', '', '', r'..\doc\jobs\Resume_Regret.doc', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', r'..\doc\job_file.txt', '', '', '', '', '', 'Job_Application'],
                    ['30604', '', '', r'..\doc\jobs\file.doc', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job_check")

    def test_in_text(self):
        """Test for when column in_text contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', ' new job request', '', '', '', '', '', ''],
                              ['30601', '', 'job requested', '', '', '', '', '', ''],
                              ['30602', '', 'Job Request', '', '', '', '', '', ''],
                              ['30603', '', 'Freelance job', '', '', '', '', '', ''],
                              ['30604', '', 'note', '', '', '', '', '', ''],
                              ['30605', '', 'resume', '', '', '', '', '', ''],
                              ['30606', '', 'Forwarded Resume', '', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)
        
        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', ' new job request', '', '', '', '', '', '', 'Job_Application'],
                    ['30601', '', 'job requested', '', '', '', '', '', '', 'Job_Application'],
                    ['30602', '', 'Job Request', '', '', '', '', '', '', 'Job_Application'],
                    ['30605', '', 'resume', '', '', '', '', '', '', 'Job_Application'],
                    ['30606', '', 'Forwarded Resume', '', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', 'Freelance job', '', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_job_check")

    def test_in_topic(self):
        """Test for when column in_topic contains one of the topics indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Intern^General', '', '', '', '', '', '', ''],
                              ['30601', 'Admin^RESUMES', '', '', '', '', '', '', ''],
                              ['30602', 'Housing', '', '', '', '', '', '', ''],
                              ['30603', 'Resumes', '', '', '', '', '', '', ''],
                              ['30604', 'intern', '', '', '', '', '', '', ''],
                              ['30605', 'Job Hunting', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Intern^General', '', '', '', '', '', '', '', 'Job_Application'],
                    ['30601', 'Admin^RESUMES', '', '', '', '', '', '', '', 'Job_Application'],
                    ['30603', 'Resumes', '', '', '', '', '', '', '', 'Job_Application'],
                    ['30604', 'intern', '', '', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30605', 'Job Hunting', '', '', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_job_check")

    def test_none(self):
        """Test for when no patterns indicating job applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Farms', '', '', '', '', 'Note', '', ''],
                              ['30601', 'Cats', '', '', '', 'Cats', '', '', ''],
                              ['30602', 'Economy', '', '', '', 'Econ Plan', '', r'..\doc\econ-outlook.doc', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
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
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', r'..\doc\Doe Job Interview.txt', ''],
                              ['30601', '', '', '', '', '', '', r'..\doc\job_file.txt', ''],
                              ['30602', '', '', '', '', '', '', r'..\doc\resume.txt', ''],
                              ['30603', '', '', '', '', '', '', '', ''],
                              ['30604', '', '', '', '', '', '', r'..\doc\jobs\file.doc', ''],
                              ['30605', '', '', '', '', '', '', r'..\doc\jobs\Resume_Regret.doc', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', '', r'..\doc\Doe Job Interview.txt', '', 'Job_Application'],
                    ['30602', '', '', '', '', '', '', r'..\doc\resume.txt', '', 'Job_Application'],
                    ['30605', '', '', '', '', '', '', r'..\doc\jobs\Resume_Regret.doc', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', '', r'..\doc\job_file.txt', '', 'Job_Application'],
                    ['30604', '', '', '', '', '', '', r'..\doc\jobs\file.doc', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job_check")

    def test_out_fillin(self):
        """Test for when column out_fillin contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', '', 'internship'],
                              ['30601', '', '', '', '', '', '', '', 'second job interview'],
                              ['30602', '', '', '', '', '', '', '', 'send job request form'],
                              ['30603', '', '', '', '', '', '', '', ''],
                              ['30604', '', '', '', '', '', '', '', 'check of job'],
                              ['30605', '', '', '', '', '', '', '', 'RESUME']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', '', '', 'internship', 'Job_Application'],
                    ['30601', '', '', '', '', '', '', '', 'second job interview', 'Job_Application'],
                    ['30602', '', '', '', '', '', '', '', 'send job request form', 'Job_Application'],
                    ['30605', '', '', '', '', '', '', '', 'RESUME', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30604', '', '', '', '', '', '', '', 'check of job', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_job_check")

    def test_out_text(self):
        """Test for when column out_text contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', 'Job numbers', '', ''],
                              ['30601', '', '', '', '', '', 'District Job Request', '', ''],
                              ['30602', '', '', '', '', '', 'Jobs report', '', ''],
                              ['30603', '', '', '', '', '', 'job request', '', ''],
                              ['30604', '', '', '', '', '', 'job request - accept', '', ''],
                              ['30605', '', '', '', '', '', 'Doe resume', '', ''],
                              ['30606', '', '', '', '', '', 'RESUME', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', 'District Job Request', '', '', 'Job_Application'],
                    ['30603', '', '', '', '', '', 'job request', '', '', 'Job_Application'],
                    ['30604', '', '', '', '', '', 'job request - accept', '', '', 'Job_Application'],
                    ['30605', '', '', '', '', '', 'Doe resume', '', '', 'Job_Application'],
                    ['30606', '', '', '', '', '', 'RESUME', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', 'Job numbers', '', '', 'Job_Application'],
                    ['30602', '', '', '', '', '', 'Jobs report', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_job_check")

    def test_out_topic(self):
        """"Test for when column out_topic contains one of the topics indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', 'Economy', '', '', ''],
                              ['30601', '', '', '', '', 'Gen^resumes', '', '', ''],
                              ['30602', '', '', '', '', 'Intern', '', '', ''],
                              ['30603', '', '', '', '', 'INTERN^Admin', '', '', ''],
                              ['30604', '', '', '', '', 'Water', '', '', ''],
                              ['30605', '', '', '', '', 'Resumes', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', 'Gen^resumes', '', '', '', 'Job_Application'],
                    ['30602', '', '', '', '', 'Intern', '', '', '', 'Job_Application'],
                    ['30603', '', '', '', '', 'INTERN^Admin', '', '', '', 'Job_Application'],
                    ['30605', '', '', '', '', 'Resumes', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text', 
                     'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_job_check")

        
if __name__ == '__main__':
    unittest.main()
