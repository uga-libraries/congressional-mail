"""
Tests for the function find_academy_rows(), 
which finds metadata rows with topics or text that indicate they are academy applications and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_archiving_format import find_academy_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):
    
    def test_all(self):
        """Test for when all patterns indicating academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Academy Applicant', 'For academy nomination', 'Military Service Academy',
                               'ACADEMY NOMINATION'],
                              ['30601', 'Military Service Academy^Admin', '', 'Military Service Academy', ''],
                              ['30602', 'Academy Applicant', '', 'Academy Applicant^Gen', 'Academy Nomination Letter'],
                              ['30603', '', 'academy nomination', '', 'For academy nomination support'],
                              ['30604', '', 'academy nomination', 'Academy Applicant', 'academy nomination']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy, df_academy_check = find_academy_rows(md_df)
        
        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30600', 'Academy Applicant', 'For academy nomination', 'Military Service Academy',
                     'ACADEMY NOMINATION', 'Academy_Application'],
                    ['30601', 'Military Service Academy^Admin', '', 'Military Service Academy', '',
                     'Academy_Application'],
                    ['30602', 'Academy Applicant', '', 'Academy Applicant^Gen', 'Academy Nomination Letter',
                     'Academy_Application'],
                    ['30604', '', 'academy nomination', 'Academy Applicant', 'academy nomination',
                     'Academy_Application'],
                    ['30603', '', 'academy nomination', '', 'For academy nomination support',
                     'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for all patterns, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for all patterns, df_academy_check")

    def test_in_text(self):
        """Test for when column in_text contains "academy nomination" (cass-insensitive)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Military', 'For Academy Nomination Letter', 'Military', ''],
                              ['30601', 'Economy', '', 'Economy', ''],
                              ['30602', 'Admin', 'academy nomination', '', 'note'],
                              ['30603', 'Arts', 'Arts academy', 'Arts', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30600', 'Military', 'For Academy Nomination Letter', 'Military', '', 'Academy_Application'],
                    ['30602', 'Admin', 'academy nomination', '', 'note', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for in_text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30603', 'Arts', 'Arts academy', 'Arts', '', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for in_text, df_academy_check")

    def test_in_topic(self):
        """Test for when column in_topic contains one of the topics indicating academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Science Academy', '', 'Water', ''],
                              ['30601', 'Military Service Academy', '', 'Admin', ''],
                              ['30602', 'Military^Academy Applicant', '', '', ''],
                              ['30603', 'Arts', '', '', ''],
                              ['30604', 'Military Service Academy^ADMIN', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30601', 'Military Service Academy', '', 'Admin', '', 'Academy_Application'],
                    ['30602', 'Military^Academy Applicant', '', '', '', 'Academy_Application'],
                    ['30604', 'Military Service Academy^ADMIN', '', '', '', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for in_topic, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30600', 'Science Academy', '', 'Water', '', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for in_topic, df_academy_check")

    def test_none(self):
        """Test for when no patterns indicating academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Arts', 'Note', 'Arts', 'Note'],
                              ['30601', 'Water', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no patterns matched), df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no patterns matched), df_academy_check")

    def test_out_text(self):
        """Test for when column out_text contains "academy nomination" (cass-insensitive)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', 'for academy nomination'],
                              ['30601', '', 'note', '', 'Academy Nomination acceptance'],
                              ['30602', 'Military', '', '', 'ACADEMY NOMINATION'],
                              ['30603', 'Arts', 'Note', 'Arts', 'Academy Note'],
                              ['30604', 'Science', '', 'Science', 'International Science Academy']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30600', '', '', '', 'for academy nomination', 'Academy_Application'],
                    ['30601', '', 'note', '', 'Academy Nomination acceptance', 'Academy_Application'],
                    ['30602', 'Military', '', '', 'ACADEMY NOMINATION', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for out_text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30603', 'Arts', 'Note', 'Arts', 'Academy Note', 'Academy_Application'],
                    ['30604', 'Science', '', 'Science', 'International Science Academy', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for out_text, df_academy_check")

    def test_out_topic(self):
        """Test for when column out_topic contains one of the topics indicating academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Transportation', '', 'Academy', ''],
                              ['30601', 'General', '', 'General^Military Service Academy', ''],
                              ['30602', 'General', '', 'Science Academy', 'Note'],
                              ['30603', '', '', 'Academy Applicant^Military', ''],
                              ['30604', '', '', 'Academy Applicant', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30601', 'General', '', 'General^Military Service Academy', '', 'Academy_Application'],
                    ['30603', '', '', 'Academy Applicant^Military', '', 'Academy_Application'],
                    ['30604', '', '', 'Academy Applicant', '', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for out_topic, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30600', 'Transportation', '', 'Academy', '', 'Academy_Application'],
                    ['30602', 'General', '', 'Science Academy', 'Note', 'Academy_Application']]
        self.assertEqual(result, expected, "Problem with test for out_topic, df_academy_check")


if __name__ == '__main__':
    unittest.main()
