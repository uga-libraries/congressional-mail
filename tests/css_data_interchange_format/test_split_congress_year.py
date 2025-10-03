"""
Tests for the function split_congress_year(), which makes one CSV for letters received in each Congress Year.
To simplify input, tests use dataframes with only some of the columns present in a real export
"""
import os
import shutil

import pandas as pd
import unittest
from css_data_interchange_format import split_congress_year
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function output"""
        output_path = os.path.join('test_data', 'archiving_correspondence_by_congress_year')
        shutil.rmtree(output_path)

    def test_all(self):
        """Test for a combination of all date variations: even, odd, and blank"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['MI', '49068-1164', '19980412', 'INSUTAX2'],
                              ['VA', '22031-4339', '19970412', 'TOUR'],
                              ['GA', '30102-1056', 'nan', 'nan'],
                              ['GA', '30082-1838', '19970412', 'SSCUTS2'],
                              ['GA', '30152-3929', '20121130', 'SSCUTS1'],
                              ['GA', '30062-2748', 'nan', 'INSUTAX1']],
                             columns=['state_code', 'zip_code', 'date_in', 'group_name'])
        split_congress_year(md_df, 'test_data')

        # Tests that 1997-1998.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '1997-1998.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['MI', '49068-1164', '19980412', 'INSUTAX2'],
                    ['VA', '22031-4339', '19970412', 'TOUR'],
                    ['GA', '30082-1838', '19970412', 'SSCUTS2']]
        self.assertEqual(expected, result, "Problem with test for all year variations, 1997-1998")

        # Tests that 2011-2012.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '2011-2012.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['GA', '30152-3929', '20121130', 'SSCUTS1']]
        self.assertEqual(expected, result, "Problem with test for all year variations, 2011-2012")

        # Tests that undated.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', 'undated.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['GA', '30102-1056', 'nan', 'nan'],
                    ['GA', '30062-2748', 'nan', 'INSUTAX1']]
        self.assertEqual(expected, result, "Problem with test for all year variations, undated.csv")

    def test_date_blank(self):
        """Test for when some of the letters do not have a date (date_in column is blank)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['GA', '30102-1056', '', ''],
                              ['GA', '30062-2748', '', 'INSUTAX1']],
                             columns=['state_code', 'zip_code', 'date_in', 'group_name'])
        split_congress_year(md_df, 'test_data')

        # Tests that undated.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', 'undated.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['GA', '30102-1056', 'nan', 'nan'],
                    ['GA', '30062-2748', 'nan', 'INSUTAX1']]
        self.assertEqual(expected, result, "Problem with test for blank years, undated.csv")

    def test_even_years(self):
        """Test for when the letters are from even numbered years"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['MI', '49068-1164', '19980412', 'INSUTAX2'],
                              ['GA', '30152-3929', '20121130', 'SSCUTS1'],
                              ['FL', '32448-5365', '20121231', 'SSCUTS1']],
                             columns=['state_code', 'zip_code', 'date_in', 'group_name'])
        split_congress_year(md_df, 'test_data')

        # Tests that 1997-1998.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '1997-1998.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['MI', '49068-1164', '19980412', 'INSUTAX2']]
        self.assertEqual(expected, result, "Problem with test for even years, 1997-1998")

        # Tests that 2011-2012.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '2011-2012.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['GA', '30152-3929', '20121130', 'SSCUTS1'],
                    ['FL', '32448-5365', '20121231', 'SSCUTS1']]
        self.assertEqual(expected, result, "Problem with test for even years, 2011-2012")

        # Tests that undated.csv was not made.
        result = os.path.exists(os.path.join('test_data', 'archiving_correspondence_by_congress_year', 'undated.csv'))
        self.assertEqual(False, result, "Problem with test for even years, undated")

    def test_odd_years(self):
        """Test for when the letters are from odd numbered years"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['VA', '22031-4339', '19970412', 'TOUR'],
                              ['GA', '30082-1838', '19970412', 'SSCUTS2'],
                              ['GA', '30328-4628', '20091015', 'TOUR']],
                             columns=['state_code', 'zip_code', 'date_in', 'group_name'])
        split_congress_year(md_df, 'test_data')

        # Tests that 1997-1998.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '1997-1998.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['VA', '22031-4339', '19970412', 'TOUR'],
                    ['GA', '30082-1838', '19970412', 'SSCUTS2']]
        self.assertEqual(expected, result, "Problem with test for odd years, 1997-1998")

        # Tests that 2009-2010.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_by_congress_year', '2009-2010.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['GA', '30328-4628', '20091015', 'TOUR']]
        self.assertEqual(expected, result, "Problem with test for odd years, 2009-2010")

        # Tests that undated.csv was not made.
        result = os.path.exists(os.path.join('test_data', 'archiving_correspondence_by_congress_year', 'undated.csv'))
        self.assertEqual(False, result, "Problem with test for odd years, undated")


if __name__ == '__main__':
    unittest.main()
