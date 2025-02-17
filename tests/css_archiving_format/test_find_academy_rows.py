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
        df_academy = find_academy_rows(md_df)
        
        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'],
                    ['30600', 'Academy Applicant', 'For academy nomination', 'Military Service Academy',
                     'ACADEMY NOMINATION'],
                    ['30601', 'Military Service Academy^Admin', '', 'Military Service Academy', ''],
                    ['30602', 'Academy Applicant', '', 'Academy Applicant^Gen', 'Academy Nomination Letter'],
                    ['30604', '', 'academy nomination', 'Academy Applicant', 'academy nomination'],
                    ['30603', '', 'academy nomination', '', 'For academy nomination support']]
        self.assertEqual(result, expected, "Problem with test for all patterns")

    def test_in_text(self):
        """Test for when column in_text contains "academy nomination" (cass-insensitive)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Military', 'For Academy Nomination Letter', 'Military', ''],
                              ['30601', 'Economy', '', 'Economy', ''],
                              ['30602', 'Admin', 'academy nomination', '', 'note'],
                              ['30603', 'Arts', 'Note', 'Arts', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy = find_academy_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'],
                    ['30600', 'Military', 'For Academy Nomination Letter', 'Military', ''],
                    ['30602', 'Admin', 'academy nomination', '', 'note']]
        self.assertEqual(result, expected, "Problem with test for in_text")

    def test_in_topic(self):
        """Test for when column in_topic contains one of the topics indicating academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Water', '', 'Water', ''],
                              ['30601', 'Military Service Academy', '', 'Admin', ''],
                              ['30602', 'Military^Academy Applicant', '', '', ''],
                              ['30603', 'Arts', '', '', ''],
                              ['30604', 'Military Service Academy^ADMIN', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy = find_academy_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'],
                    ['30601', 'Military Service Academy', '', 'Admin', ''],
                    ['30602', 'Military^Academy Applicant', '', '', ''],
                    ['30604', 'Military Service Academy^ADMIN', '', '', '']]
        self.assertEqual(result, expected, "Problem with test for in_topic")

    def test_none(self):
        """Test for when no patterns indicating academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Arts', 'Note', 'Arts', 'Note'],
                              ['30601', 'Water', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy = find_academy_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text']]
        self.assertEqual(result, expected, "Problem with test for none (no patterns matched)")

    def test_out_text(self):
        """Test for when column out_text contains "academy nomination" (cass-insensitive)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', 'for academy nomination'],
                              ['30601', '', 'note', '', 'Academy Nomination acceptance'],
                              ['30602', 'Military', '', '', 'ACADEMY NOMINATION'],
                              ['30603', 'Arts', 'Note', 'Arts', 'Note'],
                              ['30604', 'Science', '', 'Science', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy = find_academy_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'],
                    ['30600', '', '', '', 'for academy nomination'],
                    ['30601', '', 'note', '', 'Academy Nomination acceptance'],
                    ['30602', 'Military', '', '', 'ACADEMY NOMINATION']]
        self.assertEqual(result, expected, "Problem with test for out_text")

    def test_out_topic(self):
        """Test for when column out_topic contains one of the topics indicating academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Transportation', '', '', ''],
                              ['30601', 'General', '', 'General^Military Service Academy', ''],
                              ['30602', 'General', '', '', 'Note'],
                              ['30603', '', '', 'Academy Applicant^Military', ''],
                              ['30604', '', '', 'Academy Applicant', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_academy = find_academy_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'],
                    ['30601', 'General', '', 'General^Military Service Academy', ''],
                    ['30603', '', '', 'Academy Applicant^Military', ''],
                    ['30604', '', '', 'Academy Applicant', '']]
        self.assertEqual(result, expected, "Problem with test for out_topic")


if __name__ == '__main__':
    unittest.main()
