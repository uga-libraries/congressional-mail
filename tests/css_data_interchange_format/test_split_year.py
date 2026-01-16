import os
import pandas as pd
import shutil
import unittest
from css_data_interchange_format import split_year
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function output"""
        output_path = os.path.join('test_data', 'correspondence_metadata_by_year')
        shutil.rmtree(output_path)

    def test_date_blank(self):
        """Test for when some of the letters do not have a date (date_in column is blank)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['GA', '30102-1056', '', ''],
                              ['GA', '30062-2748', '', 'INSUTAX1']],
                             columns=['state_code', 'zip_code', 'date_in', 'group_name'])
        split_year(md_df, 'test_data')

        # Tests that undated.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', 'undated.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['GA', '30102-1056', 'BLANK', 'BLANK'],
                    ['GA', '30062-2748', 'BLANK', 'INSUTAX1']]
        self.assertEqual(expected, result, "Problem with test for blank years, undated.csv")

    def test_multiple_years(self):
        """Test for when the letters are from multiple years"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['MI', '49068-1164', '19980412', 'INSUTAX2'],
                              ['GA', '30152-3929', '20121130', 'SSCUTS1'],
                              ['FL', '32448-5365', '20121231', 'SSCUTS1']],
                             columns=['state_code', 'zip_code', 'date_in', 'group_name'])
        split_year(md_df, 'test_data')

        # Tests that 1998.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '1998.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['MI', '49068-1164', '19980412', 'INSUTAX2']]
        self.assertEqual(expected, result, "Problem with test for multiple years, 1998")

        # Tests that 2012.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '2012.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['GA', '30152-3929', '20121130', 'SSCUTS1'],
                    ['FL', '32448-5365', '20121231', 'SSCUTS1']]
        self.assertEqual(expected, result, "Problem with test for multiple years, 2012")

        # Tests that undated.csv was not made.
        result = os.path.exists(os.path.join('test_data', 'correspondence_metadata_by_year', 'undated.csv'))
        self.assertEqual(False, result, "Problem with test for even years, undated")

    def test_one_year(self):
        """Test for when the letters are from the same year"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['VA', '22031-4339', '19970412', 'TOUR'],
                              ['GA', '30082-1838', '19970412', 'SSCUTS2'],
                              ['GA', '30328-4628', '19971015', 'TOUR']],
                             columns=['state_code', 'zip_code', 'date_in', 'group_name'])
        split_year(md_df, 'test_data')

        # Tests that 1997.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'correspondence_metadata_by_year', '1997.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'group_name'],
                    ['VA', '22031-4339', '19970412', 'TOUR'],
                    ['GA', '30082-1838', '19970412', 'SSCUTS2'],
                    ['GA', '30328-4628', '19971015', 'TOUR']]
        self.assertEqual(expected, result, "Problem with test for one year, 1997")

        # Tests that undated.csv was not made.
        result = os.path.exists(os.path.join('test_data', 'correspondence_metadata_by_year', 'undated.csv'))
        self.assertEqual(False, result, "Problem with test for odd years, undated")


if __name__ == '__main__':
    unittest.main()
