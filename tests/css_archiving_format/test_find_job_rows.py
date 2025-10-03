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
        md_df = pd.DataFrame([['30600', 'Resume', 'job request', r'..\doc\resume.txt', '', 'Resume',
                               'job request', '', ''],
                              ['30601', '', '', '', '', 'Intern', 'summer job request', r'..\doc\job interview.doc', ''],
                              ['30602', 'Intern', '', '', '', 'Resume', '', '', ''],
                              ['30603', 'Resume', 'job request', '', '', '', '', '', ''],
                              ['30604', '', 'Job Request', '', '', '', 'job request', '', ''],
                              ['30605', 'Admin', 'job request', '', '', 'Resume', '', r'..\doc\resume.txt', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Resume', 'job request', r'..\doc\resume.txt', '', 'Resume', 'job request', '',
                     '', 'Job_Application'],
                    ['30602', 'Intern', '', '', '', 'Resume', '', '', '', 'Job_Application'],
                    ['30603', 'Resume', 'job request', '', '', '', '', '', '', 'Job_Application'],
                    ['30601', '', '', '', '', 'Intern', 'summer job request', r'..\doc\job interview.doc',
                     '', 'Job_Application'],
                    ['30605', 'Admin', 'job request', '', '', 'Resume', '', r'..\doc\resume.txt', '', 'Job_Application'],
                    ['30604', '', 'Job Request', '', '', '', 'job request', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for all patterns, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for all patterns, df_job_check")

    def test_in_document_name(self):
        """Test for when column in_document_name contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Admin', '', r'..\doc\Doe Job Interview.txt', '', '', '', '', ''],
                              ['30601', 'Arts', '', r'..\doc\job_file.txt', '', '', '', '', ''],
                              ['30602', 'Admin', '', r'..\doc\resume.txt', '', 'Admin', 'Files', '', ''],
                              ['30603', '', '', '', '', '', 'Note', '', ''],
                              ['30604', '', '', r'..\doc\jobs\file.doc', '', '', 'Note', '', ''],
                              ['30605', '', '', r'..\doc\jobs\Resume_Regret.doc', '', '', 'Note', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Admin', '', r'..\doc\Doe Job Interview.txt', '', '', '', '', '', 'Job_Application'],
                    ['30602', 'Admin', '', r'..\doc\resume.txt', '', 'Admin', 'Files', '', '', 'Job_Application'],
                    ['30605', '', '', r'..\doc\jobs\Resume_Regret.doc', '', '', 'Note', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', 'Arts', '', r'..\doc\job_file.txt', '', '', '', '', '', 'Job_Application'],
                    ['30604', '', '', r'..\doc\jobs\file.doc', '', '', 'Note', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job_check")

    def test_in_text(self):
        """Test for when column in_text contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Gen', ' new job request', '', '', 'Gen', 'info sent', '', ''],
                              ['30601', 'Admin', 'job requested', '', '', 'Admin', '', r'..\doc\response.doc', ''],
                              ['30602', '', 'Job Request', '', '', '', '', '', ''],
                              ['30603', 'Arts', 'Freelance job', '', '', '', '', '', ''],
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
                    ['30600', 'Gen', ' new job request', '', '', 'Gen', 'info sent', '', '', 'Job_Application'],
                    ['30601', 'Admin', 'job requested', '', '', 'Admin', '', r'..\doc\response.doc', '',
                     'Job_Application'],
                    ['30602', '', 'Job Request', '', '', '', '', '', '', 'Job_Application'],
                    ['30605', '', 'resume', '', '', '', '', '', '', 'Job_Application'],
                    ['30606', '', 'Forwarded Resume', '', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', 'Arts', 'Freelance job', '', '', '', '', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_job_check")

    def test_in_topic(self):
        """Test for when column in_topic contains one of the topics indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Intern^General', '', '', '', '', '', '', ''],
                              ['30601', 'Admin^RESUMES', '', '', '', '', 'Note', '', ''],
                              ['30602', 'Housing', '', '', '', 'Housing', '', '', ''],
                              ['30603', 'Resumes', '', '', '', 'Economy', '', '', ''],
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
                    ['30601', 'Admin^RESUMES', '', '', '', '', 'Note', '', '', 'Job_Application'],
                    ['30603', 'Resumes', '', '', '', 'Economy', '', '', '', 'Job_Application'],
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
        md_df = pd.DataFrame([['30600', 'Admin', '', '', '', '', '', r'..\doc\Doe Job Interview.txt', ''],
                              ['30601', 'Arts', '', '', '', '', '', r'..\doc\job_file.txt', ''],
                              ['30602', 'Admin', '', '', '', 'Admin', 'Files', r'..\doc\resume.txt', ''],
                              ['30603', '', '', '', '', '', 'Note', '', ''],
                              ['30604', '', '', '', '', '', 'Note', r'..\doc\jobs\file.doc', ''],
                              ['30605', '', '', '', '', '', 'Note', r'..\doc\jobs\Resume_Regret.doc', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Admin', '', '', '', '', '', r'..\doc\Doe Job Interview.txt', '', 'Job_Application'],
                    ['30602', 'Admin', '', '', '', 'Admin', 'Files', r'..\doc\resume.txt', '', 'Job_Application'],
                    ['30605', '', '', '', '', '', 'Note', r'..\doc\jobs\Resume_Regret.doc', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', 'Arts', '', '', '', '', '', r'..\doc\job_file.txt', '', 'Job_Application'],
                    ['30604', '', '', '', '', '', 'Note', r'..\doc\jobs\file.doc', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_job_check")

    def test_out_text(self):
        """Test for when column out_text contains a word or phrase indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Farms', '', '', '', 'Agriculture', 'Job numbers', '', ''],
                              ['30601', 'Admin', '', '', '', 'Admin', 'District Job Request', '', ''],
                              ['30602', '', '', '', '', 'Economy', '', 'Jobs report', ''],
                              ['30603', '', '', '', '', '', 'job request', '', ''],
                              ['30604', 'Admin', '', '', '', '', 'job request - accept', '', ''],
                              ['30605', 'Admin', '', '', '', '', 'Doe resume', '', ''],
                              ['30606', 'Admin', '', '', '', '', 'RESUME', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', 'Admin', '', '', '', 'Admin', 'District Job Request', '', '', 'Job_Application'],
                    ['30603', '', '', '', '', '', 'job request', '', '', 'Job_Application'],
                    ['30604', 'Admin', '', '', '', '', 'job request - accept', '', '', 'Job_Application'],
                    ['30605', 'Admin', '', '', '', '', 'Doe resume', '', '', 'Job_Application'],
                    ['30606', 'Admin', '', '', '', '', 'RESUME', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Farms', '', '', '', 'Agriculture', 'Job numbers', '', '', 'Job_Application'],
                    ['30602', '', '', '', '', 'Economy', '', 'Jobs report', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_job_check")

    def test_out_topic(self):
        """"Test for when column out_topic contains one of the topics indicating job applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', 'Economy', 'text', r'..\doc\form\econ.doc', ''],
                              ['30601', '', '', '', '', 'Gen^resumes', '', '', ''],
                              ['30602', '', '', '', '', 'Intern', '', '', ''],
                              ['30603', '', '', '', '', 'INTERN^Admin', 'note', '', ''],
                              ['30604', '', '', '', '', 'Water', '', '', ''],
                              ['30605', '', '', '', '', 'Resumes', 'note', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_job, df_job_check = find_job_rows(md_df)

        # Tests the values in df_job are correct.
        result = df_to_list(df_job)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', 'Gen^resumes', '', '', '', 'Job_Application'],
                    ['30602', '', '', '', '', 'Intern', '', '', '', 'Job_Application'],
                    ['30603', '', '', '', '', 'INTERN^Admin', 'note', '', '', 'Job_Application'],
                    ['30605', '', '', '', '', 'Resumes', 'note', '', '', 'Job_Application']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_job")

        # Tests the values in df_job_check are correct.
        result = df_to_list(df_job_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text', 
                     'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_job_check")

        
if __name__ == '__main__':
    unittest.main()
