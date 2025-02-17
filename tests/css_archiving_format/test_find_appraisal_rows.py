"""
Tests for the function find_appraisal_rows(),
which finds metadata rows with topics or text that indicate they are different categories for appraisal 
and return as a df and log results.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from css_archiving_format import find_appraisal_rows
from test_read_metadata import df_to_list
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the log, if made by the test"""
        log_path = os.path.join('test_data', 'appraisal_delete_log.csv')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_two(self):
        """Test for when there are two categories for appraisal (academy applications and casework)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Academy Applicant', 'Nomination', '', ''],
                              ['30601', 'Casework', '', '', ''],
                              ['30602', 'General', 'Note', 'General', 'Note'],
                              ['30603', 'Social Security', 'Casework candidate', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values of the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'],
                    ['30600', 'Academy Applicant', 'Nomination', '', ''],
                    ['30601', 'Casework', '', '', ''],
                    ['30603', 'Social Security', 'Casework candidate', '', '']]
        self.assertEqual(result, expected, "Problem with test for two categories, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'],
                    ['30600', 'Academy Applicant', 'Nomination', 'nan', 'nan'],
                    ['30601', 'Casework', 'nan', 'nan', 'nan'],
                    ['30603', 'Social Security', 'Casework candidate', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for two categories, appraisal delete log")

    def test_one(self):
        """Test for when there is one category for appraisal (casework)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Casework Issues', '', 'Casework', ''],
                              ['30601', 'Health^Casework', 'Note', '', ''],
                              ['30602', 'Health', 'General interest', '', 'Note'],
                              ['30603', 'Social Security', 'Open Case', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'],
                    ['30600', 'Casework Issues', '', 'Casework', ''],
                    ['30601', 'Health^Casework', 'Note', '', ''],
                    ['30603', 'Social Security', 'Open Case', '', '']]
        self.assertEqual(result, expected, "Problem with test for one category, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'],
                    ['30600', 'Casework Issues', 'nan', 'Casework', 'nan'],
                    ['30601', 'Health^Casework', 'Note', 'nan', 'nan'],
                    ['30603', 'Social Security', 'Open Case', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for one category, appraisal delete log")

    def test_none(self):
        """Test for when there are no indicators for appraisal"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Arts', 'In support', '', ''],
                              ['30601', 'Healthcare', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        appraisal_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(appraisal_df)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text']]
        self.assertEqual(result, expected, "Problem with test for no appraisal, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text']]
        self.assertEqual(result, expected, "Problem with test for no appraisal, appraisal delete log")


if __name__ == '__main__':
    unittest.main()
