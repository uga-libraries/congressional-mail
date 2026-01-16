"""
Tests for the function split_year(), which makes one CSV for letters received in each calendar year.
To simplify input, tests use dataframes with only some of the columns present in a real css/cms export
"""
import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import split_year
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function output"""
        output_path = os.path.join('test_data', 'correspondence_metadata_by_year')
        shutil.rmtree(output_path)

    def test_date_blank(self):
        """Test for when some of the letters do not have a date (in_date column is blank)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', np.nan, 'dogs', np.nan, 'pets'],
                              ['30602', np.nan, 'cats', np.nan, 'pets']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_year(md_df, 'test_data')

        # Tests that undated has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', 'undated.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    ['30601', 'BLANK', 'dogs', 'BLANK', 'pets'],
                    ['30602', 'BLANK', 'cats', 'BLANK', 'pets']]
        self.assertEqual(expected, result, "Problem with test for date blank, undated")

    def test_date_text(self):
        """Test for when data entry errors results in text rather than date (in_date column is a string)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', 'error', 'cats', '19950105', 'pets'],
                              ['30601', 'error_date', 'dogs', '19950105', 'pets']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_year(md_df, 'test_data')

        # Tests that undated has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', 'undated.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    ['30601', 'error', 'cats', '19950105', 'pets'],
                    ['30601', 'error_date', 'dogs', '19950105', 'pets']]
        self.assertEqual(expected, result, "Problem with test for date text, undated")

    def test_multiple_years(self):
        """Test for when the letters are from multiple years"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', '19970104', 'cats', '19970105', 'pets'],
                              ['30601', '19981001', 'dogs', '19981005', 'pets'],
                              ['30602', '19981202', 'cats', '19980105', 'pets'],
                              ['30603', '20090501', 'oranges', '20090509', 'fruit'],
                              ['30604', '20090502', 'oranges', '20090509', 'fruit'],
                              ['30605', '20090503', 'blueberries', '20090509', 'fruit']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_year(md_df, 'test_data')

        # Tests that 1997.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '1997.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    ['30601', '19970104', 'cats', '19970105', 'pets']]
        self.assertEqual(expected, result, "Problem with test for multiple years, 1997")

        # Tests that 1998.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '1998.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    ['30601', '19981001', 'dogs', '19981005', 'pets'],
                    ['30602', '19981202', 'cats', '19980105', 'pets']]
        self.assertEqual(expected, result, "Problem with test for multiple years, 1998")

        # Tests that 2009.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '2009.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    ['30603', '20090501', 'oranges', '20090509', 'fruit'],
                    ['30604', '20090502', 'oranges', '20090509', 'fruit'],
                    ['30605', '20090503', 'blueberries', '20090509', 'fruit']]
        self.assertEqual(expected, result, "Problem with test for multiple years, 2009")

    def test_one_year(self):
        """Test for when the letters are from the same year"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', '19900104', 'cats', '19900105', 'pets'],
                              ['30601', '19901001', 'dogs', '19901005', 'pets'],
                              ['30602', '19901202', 'cats', '19910105', 'pets'],
                              ['30603', '19900505', 'oranges', '19900509', 'fruit']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_year(md_df, 'test_data')

        # Tests that 1990.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '1990.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    ['30601', '19900104', 'cats', '19900105', 'pets'],
                    ['30601', '19901001', 'dogs', '19901005', 'pets'],
                    ['30602', '19901202', 'cats', '19910105', 'pets'],
                    ['30603', '19900505', 'oranges', '19900509', 'fruit']]
        self.assertEqual(expected, result, "Problem with test for one year, 1990")


if __name__ == '__main__':
    unittest.main()
