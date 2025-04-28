"""
Tests for the function split_congress_year(), which makes one CSV for letters received in each Congress Year.
To simplify input, tests use dataframes with only some of the columns present in a real css/cms export
"""
import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import split_congress_year
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function output"""
        output_path = os.path.join('test_data', 'archiving_correspondence_by_congress_year')
        shutil.rmtree(output_path)

    def test_all(self):
        """Test for a combination of all date values: even, odd, blank, and text"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', '19870104', 'cats', np.nan, 'pets'],
                              ['30601', '19881001', 'dogs', '19881005', np.nan],
                              ['30602', '19881202', 'cats', '19890105', 'pets'],
                              ['30602', np.nan, 'cats', '19890105', 'pets'],
                              ['30603', '19810505', 'oranges', '19810509', 'fruit'],
                              ['30603', '19820505', 'oranges', '19820509', 'fruit'],
                              ['30603', 'date_error', 'oranges', '19820509', 'fruit']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_congress_year(md_df, 'test_data')

        # Tests that 1981-1982.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '1981-1982.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30603, 19810505, 'oranges', 19810509, 'fruit'],
                    [30603, 19820505, 'oranges', 19820509, 'fruit']]
        self.assertEqual(result, expected, "Problem with test for all years, 1981-1982")

        # Tests that 1987-1988.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '1987-1988.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30601, 19870104, 'cats', 'BLANK', 'pets'],
                    [30601, 19881001, 'dogs', 19881005, 'BLANK'],
                    [30602, 19881202, 'cats', 19890105, 'pets']]
        self.assertEqual(result, expected, "Problem with test for all years, 1987-1988")

        # Tests that undated.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', 'undated.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30602, 'BLANK', 'cats', 19890105, 'pets'],
                    [30603, 'date_error', 'oranges', 19820509, 'fruit']]
        self.assertEqual(result, expected, "Problem with test for all years, 1987-1988")

    def test_date_blank(self):
        """Test for when some of the letters do not have a date (in_date column is blank)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', np.nan, 'dogs', np.nan, 'pets'],
                              ['30602', np.nan, 'cats', np.nan, 'pets']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_congress_year(md_df, 'test_data')

        # Tests that undated has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', 'undated.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30601, 'BLANK', 'dogs', 'BLANK', 'pets'],
                    [30602, 'BLANK', 'cats', 'BLANK', 'pets']]
        self.assertEqual(result, expected, "Problem with test for date blank, undated")

    def test_date_text(self):
        """Test for when data entry errors results in text rather than date (in_date column is a string)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', 'error', 'cats', '19950105', 'pets'],
                              ['30601', 'error_date', 'dogs', '19950105', 'pets']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_congress_year(md_df, 'test_data')

        # Tests that undated has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', 'undated.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30601, 'error', 'cats', 19950105, 'pets'],
                    [30601, 'error_date', 'dogs', 19950105, 'pets']]
        self.assertEqual(result, expected, "Problem with test for date text, undated")

    def test_even_years(self):
        """Test for when the letters are from even numbered years"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', '19900104', 'cats', '19900105', 'pets'],
                              ['30601', '19901001', 'dogs', '19901005', 'pets'],
                              ['30602', '19901202', 'cats', '19910105', 'pets'],
                              ['30603', '20020505', 'oranges', '20020509', 'fruit']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_congress_year(md_df, 'test_data')

        # Tests that 1989-1990.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '1989-1990.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30601, 19900104, 'cats', 19900105, 'pets'],
                    [30601, 19901001, 'dogs', 19901005, 'pets'],
                    [30602, 19901202, 'cats', 19910105, 'pets']]
        self.assertEqual(result, expected, "Problem with test for even years, 1989-1990")

        # Tests that 2001-2002.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '2001-2002.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30603, 20020505, 'oranges', 20020509, 'fruit']]
        self.assertEqual(result, expected, "Problem with test for even years, 2001-2002")

    def test_odd_years(self):
        """Test for when the letters are from odd numbered years"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', '19970104', 'cats', '19970105', 'pets'],
                              ['30601', '19971001', 'dogs', '19971005', 'pets'],
                              ['30602', '19971202', 'cats', '19980105', 'pets'],
                              ['30603', '20090505', 'oranges', '20090509', 'fruit']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_congress_year(md_df, 'test_data')

        # Tests that 1997-1998.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '1997-1998.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30601, 19970104, 'cats', 19970105, 'pets'],
                    [30601, 19971001, 'dogs', 19971005, 'pets'],
                    [30602, 19971202, 'cats', 19980105, 'pets']]
        self.assertEqual(result, expected, "Problem with test for odd years, 1997-1998")

        # Tests that 2009-2010.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '2009-2010.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30603, 20090505, 'oranges', 20090509, 'fruit']]
        self.assertEqual(result, expected, "Problem with test for even years, 2009-2010")


if __name__ == '__main__':
    unittest.main()
