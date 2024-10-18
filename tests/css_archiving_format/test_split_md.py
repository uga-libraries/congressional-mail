"""
Tests for the function split_md(), which makes one CSV for letters received in each Congress Year.
To simplify input, tests use dataframes with only some of the columns present in a real css/cms export
"""
import os
import pandas as pd
import unittest
from css_archiving_format import split_md
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function output, if it was created"""
        filenames = ['1981-1982.csv', '1987-1988.csv', '1989-1990.csv', '1997-1998.csv',
                     '2001-2002.csv', '2009-2010.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_both_years(self):
        """Test for when the letters are from even and odd numbered years"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([[30601, 19870104, 'cats', 19880105, 'pets'],
                              [30601, 19881001, 'dogs', 19881005, 'pets'],
                              [30602, 19881202, 'cats', 19890105, 'pets'],
                              [30603, 19810505, 'oranges', 19810509, 'fruit'],
                              [30603, 19820505, 'oranges', 19820509, 'fruit']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_md(md_df, 'test_data')

        # Tests that 1981-1982.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '1981-1982.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30603, 19810505, 'oranges', 19810509, 'fruit'],
                    [30603, 19820505, 'oranges', 19820509, 'fruit']]
        self.assertEqual(result, expected, "Problem with test for both even and odd years, 1981-1982")

        # Tests that 1987-1988.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '1987-1988.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30601, 19870104, 'cats', 19880105, 'pets'],
                    [30601, 19881001, 'dogs', 19881005, 'pets'],
                    [30602, 19881202, 'cats', 19890105, 'pets']]
        self.assertEqual(result, expected, "Problem with test for both even and odd years, 1987-1988")

    def test_even_years(self):
        """Test for when the letters are from even numbered years"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([[30601, 19900104, 'cats', 19900105, 'pets'],
                              [30601, 19901001, 'dogs', 19901005, 'pets'],
                              [30602, 19901202, 'cats', 19910105, 'pets'],
                              [30603, 20020505, 'oranges', 20020509, 'fruit']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_md(md_df, 'test_data')

        # Tests that 1989-1990.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '1989-1990.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30601, 19900104, 'cats', 19900105, 'pets'],
                    [30601, 19901001, 'dogs', 19901005, 'pets'],
                    [30602, 19901202, 'cats', 19910105, 'pets']]
        self.assertEqual(result, expected, "Problem with test for even years, 1989-1990")

        # Tests that 2001-2002.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '2001-2002.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30603, 20020505, 'oranges', 20020509, 'fruit']]
        self.assertEqual(result, expected, "Problem with test for even years, 2001-2002")

    def test_odd_years(self):
        """Test for when the letters are from odd numbered years"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([[30601, 19970104, 'cats', 19970105, 'pets'],
                              [30601, 19971001, 'dogs', 19971005, 'pets'],
                              [30602, 19971202, 'cats', 19980105, 'pets'],
                              [30603, 20090505, 'oranges', 20090509, 'fruit']],
                             columns=['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'])
        split_md(md_df, 'test_data')

        # Tests that 1997-1998.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '1997-1998.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30601, 19970104, 'cats', 19970105, 'pets'],
                    [30601, 19971001, 'dogs', 19971005, 'pets'],
                    [30602, 19971202, 'cats', 19980105, 'pets']]
        self.assertEqual(result, expected, "Problem with test for odd years, 1997-1998")

        # Tests that 2009-2010.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '2009-2010.csv'))
        expected = [['zip', 'in_date', 'in_topic', 'out_date', 'out_topic'],
                    [30603, 20090505, 'oranges', 20090509, 'fruit']]
        self.assertEqual(result, expected, "Problem with test for even years, 2009-2010")


if __name__ == '__main__':
    unittest.main()
