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

    def test_casework(self):
        """Test for when there is casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Casework Issues', ''],
                              ['30601', 'Health^Casework', 'Note'],
                              ['30602', 'Health', 'General interest'],
                              ['30603', 'Social Security', 'Open Case']],
                             columns=['zip', 'in_topic', 'in_text'])
        casework_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'Casework Issues', ''],
                    ['30601', 'Health^Casework', 'Note'],
                    ['30603', 'Social Security', 'Open Case']]
        self.assertEqual(result, expected, "Problem with test for casework, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'Casework Issues', 'nan'],
                    ['30601', 'Health^Casework', 'Note'],
                    ['30603', 'Social Security', 'Open Case']]
        self.assertEqual(result, expected, "Problem with test for casework, appraisal delete log")

    def test_no_appraisal(self):
        """Test for when there are no indicators for appraisal"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Keep', ''],
                              ['30601', 'Healthcare', 'Legislation']],
                             columns=['zip', 'in_topic', 'in_text'])
        casework_df = find_appraisal_rows(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(casework_df)
        expected = [['zip', 'in_topic', 'in_text']]
        self.assertEqual(result, expected, "Problem with test for no appraisal, df")

        # Tests the values in the appraisal delete log are correct.
        result = csv_to_list(os.path.join('test_data', 'appraisal_delete_log.csv'))
        expected = [['zip', 'in_topic', 'in_text']]
        self.assertEqual(result, expected, "Problem with test for no casework, appraisal delete log")


if __name__ == '__main__':
    unittest.main()
