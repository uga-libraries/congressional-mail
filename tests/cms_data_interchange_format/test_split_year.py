import numpy as np
import os
import pandas as pd
import shutil
import unittest
from cms_data_interchange_format import split_year
from test_script import csv_to_list, make_dir_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function output"""
        output_path = os.path.join('test_data', 'correspondence_metadata_by_year')
        shutil.rmtree(output_path)

    def test_date_in(self):
        """Test for when the year is from the date_in column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', '19910101', '20010101', '20010101', '20010101'],
                              ['30602', '19930101', '20010101', '20010101', '20010101'],
                              ['30603', '19930102', '20010101', '20010101', '20010101'],
                              ['30604', '19930103', '20010101', '20010101', '20010101'],
                              ['30605', '19930104', '20010101', '20010101', '20010101']],
                             columns=['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'])
        split_year(md_df, 'test_data')

        # Tests that correspondence_metadata_by_year only has the expected csvs.
        by_year = os.path.join('test_data', 'correspondence_metadata_by_year')
        result = make_dir_list(by_year)
        expected = [os.path.join(by_year, '1991.csv'),
                    os.path.join(by_year, '1993.csv')]
        self.assertEqual(expected, result, "Problem with test for date_in, directory")

        # Tests that 1991.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '1991.csv'))
        expected = [['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'],
                    ['30601', '19910101', '20010101', '20010101', '20010101']]
        self.assertEqual(expected, result, "Problem with test for date_in, 1991.csv")

        # Tests that 1993.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, '1993.csv'))
        expected = [['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'],
                    ['30602', '19930101', '20010101', '20010101', '20010101'],
                    ['30603', '19930102', '20010101', '20010101', '20010101'],
                    ['30604', '19930103', '20010101', '20010101', '20010101'],
                    ['30605', '19930104', '20010101', '20010101', '20010101']]
        self.assertEqual(expected, result, "Problem with test for date_in, 1993.csv")

    def test_date_out(self):
        """Test for when the year is from the date_out column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', 'Jan1', '19930101', '20010101', '20010101'],
                              ['30602', np.nan, '19930102', '20010101', '20010101'],
                              ['30603', np.nan, '19910101', '20010101', '20010101'],
                              ['30604', np.nan, '19930103', '20010101', '20010101'],
                              ['30605', np.nan, '19930104', '20010101', '20010101']],
                             columns=['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'])
        split_year(md_df, 'test_data')

        # Tests that correspondence_metadata_by_year only has the expected csvs.
        by_year = os.path.join('test_data', 'correspondence_metadata_by_year')
        result = make_dir_list(by_year)
        expected = [os.path.join(by_year, '1991.csv'),
                    os.path.join(by_year, '1993.csv')]
        self.assertEqual(expected, result, "Problem with test for date_out, directory")

        # Tests that 1991.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '1991.csv'))
        expected = [['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'],
                    ['30603', 'BLANK', '19910101', '20010101', '20010101']]
        self.assertEqual(expected, result, "Problem with test for date_out, 1991.csv")

        # Tests that 1993.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, '1993.csv'))
        expected = [['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'],
                    ['30601', 'Jan1', '19930101', '20010101', '20010101'],
                    ['30602', 'BLANK', '19930102', '20010101', '20010101'],
                    ['30604', 'BLANK', '19930103', '20010101', '20010101'],
                    ['30605', 'BLANK', '19930104', '20010101', '20010101']]
        self.assertEqual(expected, result, "Problem with test for date_out, 1993.csv")

    def test_reminder(self):
        """Test for when the year is from the tickler_date column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', 'Jan1', np.nan, '19930101', np.nan],
                              ['30602', np.nan, np.nan, '19910101', np.nan],
                              ['30603', np.nan, '19XX', '19930101', np.nan],
                              ['30604', np.nan, np.nan, '19930101', np.nan],
                              ['30605', np.nan, np.nan, '19930101', np.nan]],
                             columns=['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'])
        split_year(md_df, 'test_data')

        # Tests that correspondence_metadata_by_year only has the expected csvs.
        by_year = os.path.join('test_data', 'correspondence_metadata_by_year')
        result = make_dir_list(by_year)
        expected = [os.path.join(by_year, '1991.csv'),
                    os.path.join(by_year, '1993.csv')]
        self.assertEqual(expected, result, "Problem with test for reminder, directory")

        # Tests that 1991.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '1991.csv'))
        expected = [['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'],
                    ['30602', 'BLANK', 'BLANK', '19910101', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for reminder, 1991.csv")

        # Tests that 1993.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, '1993.csv'))
        expected = [['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'],
                    ['30601', 'Jan1', 'BLANK', '19930101', 'BLANK'],
                    ['30603', 'BLANK', '19XX', '19930101', 'BLANK'],
                    ['30604', 'BLANK', 'BLANK', '19930101', 'BLANK'],
                    ['30605', 'BLANK', 'BLANK', '19930101', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for reminder, 1993.csv")

    def test_undated(self):
        """Test for when no date columns have a year"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', 'Jan1', np.nan, np.nan, np.nan],
                              ['30602', np.nan, np.nan, np.nan, np.nan],
                              ['30603', '19XX', '19XX', '20XX', '20XX'],
                              ['30604', 'XXXX', np.nan, 'XXXX', np.nan],
                              ['30605', np.nan, np.nan, np.nan, np.nan]],
                             columns=['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'])
        split_year(md_df, 'test_data')

        # Tests that correspondence_metadata_by_year only has the expected csvs.
        by_year = os.path.join('test_data', 'correspondence_metadata_by_year')
        result = make_dir_list(by_year)
        expected = [os.path.join(by_year, 'undated.csv')]
        self.assertEqual(expected, result, "Problem with test for undated, directory")

        # Tests that undated.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', 'undated.csv'))
        expected = [['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'],
                    ['30601', 'Jan1', 'BLANK', 'BLANK', 'BLANK'],
                    ['30602', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['30603', '19XX', '19XX', '20XX', '20XX'],
                    ['30604', 'XXXX', 'BLANK', 'XXXX', 'BLANK'],
                    ['30605', 'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for undated, undated.csv")

    def test_update(self):
        """Test for when the year is from the update_date column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', 'Jan1', np.nan, '20010101', '19930101'],
                              ['30602', np.nan, '19XX', '20010101', '19930102'],
                              ['30603', np.nan, np.nan, '20010101', '19930103'],
                              ['30604', np.nan, np.nan, '20010101', '19930104'],
                              ['30605', np.nan, np.nan, '20010101', '19910101']],
                             columns=['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'])
        split_year(md_df, 'test_data')

        # Tests that correspondence_metadata_by_year only has the expected csvs.
        by_year = os.path.join('test_data', 'correspondence_metadata_by_year')
        result = make_dir_list(by_year)
        expected = [os.path.join(by_year, '1991.csv'),
                    os.path.join(by_year, '1993.csv')]
        self.assertEqual(expected, result, "Problem with test for update, directory")

        # Tests that 1991.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '1991.csv'))
        expected = [['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'],
                    ['30605', 'BLANK', 'BLANK', '20010101', '19910101']]
        self.assertEqual(expected, result, "Problem with test for update, 1991.csv")

        # Tests that 1993.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, '1993.csv'))
        expected = [['zip_code', 'date_in', 'date_out', 'tickler_date', 'update_date'],
                    ['30601', 'Jan1', 'BLANK', '20010101', '19930101'],
                    ['30602', 'BLANK', '19XX', '20010101', '19930102'],
                    ['30603', 'BLANK', 'BLANK', '20010101', '19930103'],
                    ['30604', 'BLANK', 'BLANK', '20010101', '19930104']]
        self.assertEqual(expected, result, "Problem with test for update, 1993.csv")


if __name__ == '__main__':
    unittest.main()
