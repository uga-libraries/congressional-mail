import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import split_year
from test_script import csv_to_list, make_dir_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function output"""
        output_path = os.path.join('test_data', 'correspondence_metadata_by_year')
        shutil.rmtree(output_path)

    def test_in_date(self):
        """Test for when the year comes from in_date"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', '19970101', '19980109'],
                              ['30602', '19980101', '19990109'],
                              ['30603', '19980102', np.nan],
                              ['30604', '20090101', np.nan],
                              ['30605', '20090102', '20190109'],
                              ['30606', '20090103', 'january']],
                             columns=['zip', 'in_date', 'out_date'])
        split_year(md_df, 'test_data')

        # Tests that 'correspondence_metadata_by_year' has only the expected CSVs.
        by_year = os.path.join('test_data', 'correspondence_metadata_by_year')
        result = make_dir_list(by_year)
        expected = [os.path.join(by_year, '1997.csv'),
                    os.path.join(by_year, '1998.csv'),
                    os.path.join(by_year, '2009.csv')]
        self.assertEqual(expected, result, "Problem with test for in_date, directory")

        # Tests that 1997.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, '1997.csv'))
        expected = [['zip', 'in_date', 'out_date'],
                    ['30601', '19970101', '19980109']]
        self.assertEqual(expected, result, "Problem with test for in_date, 1997.csv")

        # Tests that 1998.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, '1998.csv'))
        expected = [['zip', 'in_date', 'out_date'],
                    ['30602', '19980101', '19990109'],
                    ['30603', '19980102', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for in_date, 1998.csv")

        # Tests that 2009.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, '2009.csv'))
        expected = [['zip', 'in_date', 'out_date'],
                    ['30604', '20090101', 'BLANK'],
                    ['30605', '20090102', '20190109'],
                    ['30606', '20090103', 'january']]
        self.assertEqual(expected, result, "Problem with test for in_date, 2009.csv")

    def test_out_date(self):
        """Test for when the year comes from out_date"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', np.nan, '19970101'],
                              ['30602', np.nan, '19980101'],
                              ['30603', np.nan, '19980102'],
                              ['30604', '2009Jan01', '20190101'],
                              ['30605', np.nan, '20190102'],
                              ['30606', 'Dec12', '19980103']],
                             columns=['zip', 'in_date', 'out_date'])
        split_year(md_df, 'test_data')

        # Tests that 'correspondence_metadata_by_year' has only the expected CSVs.
        by_year = os.path.join('test_data', 'correspondence_metadata_by_year')
        result = make_dir_list(by_year)
        expected = [os.path.join(by_year, '1997.csv'),
                    os.path.join(by_year, '1998.csv'),
                    os.path.join(by_year, '2019.csv')]
        self.assertEqual(expected, result, "Problem with test for out_date, directory")

        # Tests that 1997.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, '1997.csv'))
        expected = [['zip', 'in_date', 'out_date'],
                    ['30601', 'BLANK', '19970101']]
        self.assertEqual(expected, result, "Problem with test for out_date, 1997.csv")

        # Tests that 1998.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, '1998.csv'))
        expected = [['zip', 'in_date', 'out_date'],
                    ['30602', 'BLANK', '19980101'],
                    ['30603', 'BLANK', '19980102'],
                    ['30606', 'Dec12', '19980103']]
        self.assertEqual(expected, result, "Problem with test for out_date, 1998.csv")

        # Tests that 2019.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, '2019.csv'))
        expected = [['zip', 'in_date', 'out_date'],
                    ['30604', '2009Jan01', '20190101'],
                    ['30605', 'BLANK', '20190102']]
        self.assertEqual(expected, result, "Problem with test for out_date, 2019.csv")

    def test_undated(self):
        """Test for when neither date column has a year"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['30601', np.nan, '1997Jan01'],
                              ['30602', 'Dec12', np.nan],
                              ['30603', np.nan, np.nan],
                              ['30604', '2009Jan01', 'XXXXJan01']],
                             columns=['zip', 'in_date', 'out_date'])
        split_year(md_df, 'test_data')

        # Tests that 'correspondence_metadata_by_year' has only the expected CSVs.
        by_year = os.path.join('test_data', 'correspondence_metadata_by_year')
        result = make_dir_list(by_year)
        expected = [os.path.join(by_year, 'undated.csv')]
        self.assertEqual(expected, result, "Problem with test for undated, directory")

        # Tests that 1997.csv has the correct values.
        result = csv_to_list(os.path.join(by_year, 'undated.csv'))
        expected = [['zip', 'in_date', 'out_date'],
                    ['30601', 'BLANK', '1997Jan01'],
                    ['30602', 'Dec12', 'BLANK'],
                    ['30603', 'BLANK', 'BLANK'],
                    ['30604', '2009Jan01', 'XXXXJan01']]
        self.assertEqual(expected, result, "Problem with test for undated, undated.csv")


if __name__ == '__main__':
    unittest.main()
