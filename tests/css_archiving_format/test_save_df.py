"""
Tests for the function save_df(), which makes one CSV for all data.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_archiving_format import save_df
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function output, if it was created"""
        output_path = os.path.join('test_data', 'CSS_Access_Copy.csv')
        if os.path.exists(output_path):
            os.remove(output_path)

    def test_all_data(self):
        """Test for when all rows have data (no blank rows)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['GA', 30605, 11111, 'General', np.nan],
                              ['GA', 30605, 11112, 'General', 'email'],
                              ['MI', 49685, 11113, 'General', 'letter']],
                             columns=['state', 'zip', 'in_id', 'in_type', 'in_method'])
        save_df(md_df, 'test_data')

        # Tests that CSS_Access_Copy.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'CSS_Access_Copy.csv'))
        expected = [['state', 'zip', 'in_id', 'in_type', 'in_method'],
                    ['GA', 30605, 11111, 'General', 'BLANK'],
                    ['GA', 30605, 11112, 'General', 'email'],
                    ['MI', 49685, 11113, 'General', 'letter']]
        self.assertEqual(result, expected, "Problem with test for all data")

    def test_all_blank(self):
        """Test for when all rows are blank (no data)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([[np.nan, np.nan, np.nan, np.nan, np.nan],
                              [np.nan, np.nan, np.nan, np.nan, np.nan],
                              [np.nan, np.nan, np.nan, np.nan, np.nan]],
                             columns=['state', 'zip', 'in_id', 'in_type', 'in_method'])
        save_df(md_df, 'test_data')

        # Tests that 2009-2010.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'CSS_Access_Copy.csv'))
        expected = [['state', 'zip', 'in_id', 'in_type', 'in_method']]
        self.assertEqual(result, expected, "Problem with test for all blank")

    def test_some_data(self):
        """Test for when some rows have data and some rows are blank"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([[np.nan, np.nan, np.nan, np.nan, np.nan],
                              ['GA', 30605, 11111, 'General', 'email'],
                              [np.nan, np.nan, np.nan, np.nan, np.nan],
                              [np.nan, np.nan, np.nan, np.nan, np.nan],
                              ['GA', 30605, 11112, 'General', 'email'],
                              ['MI', 49685, 11113, 'General', 'letter'],
                              [np.nan, np.nan, np.nan, np.nan, np.nan],],
                             columns=['state', 'zip', 'in_id', 'in_type', 'in_method'])
        save_df(md_df, 'test_data')

        # Tests that 2009-2010.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'CSS_Access_Copy.csv'))
        expected = [['state', 'zip', 'in_id', 'in_type', 'in_method'],
                    ['GA', 30605, 11111, 'General', 'email'],
                    ['GA', 30605, 11112, 'General', 'email'],
                    ['MI', 49685, 11113, 'General', 'letter']]
        self.assertEqual(result, expected, "Problem with test for some data")

if __name__ == '__main__':
    unittest.main()
