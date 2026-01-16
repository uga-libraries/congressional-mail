import numpy as np
import os
import pandas as pd
import unittest
from css_data_interchange_format import restriction_report
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the report, if made by the test"""
        report_path = os.path.join('test_data', 'restriction_review.csv')
        if os.path.exists(report_path):
            os.remove(report_path)

    def test_all_restricted(self):
        """Test for when all rows are restricted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'citizen', 'a.txt'],
                              ['30601', 'citizenship', 'b.txt'],
                              ['30602', 'court', 'c.txt'],
                              ['30603', 'crime', 'd.txt'],
                              ['30604', 'criminal justice', 'e.txt']],
                             columns=['zip_code', 'group_name', 'file_name'])
        restriction_report(md_df, 'test_data')

        # Tests the contents of restriction_review.csv.
        result = csv_to_list(os.path.join('test_data', 'restriction_review.csv'))
        expected = [['zip_code', 'group_name', 'file_name'],
                    ['30600', 'citizen', 'a.txt'],
                    ['30601', 'citizenship', 'b.txt'],
                    ['30602', 'court', 'c.txt'],
                    ['30603', 'crime', 'd.txt'],
                    ['30604', 'criminal justice', 'e.txt']]
        self.assertEqual(expected, result, "Problem with test for all_restricted")

    def test_no_restricted(self):
        """Test for when no rows are restricted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', np.nan, 'a.txt'],
                              ['30601', 'openable', 'b.txt'],
                              ['30602', 'courtly', 'c.txt']],
                             columns=['zip_code', 'group_name', 'file_name'])
        restriction_report(md_df, 'test_data')

        # Tests the restriction_review.csv was not made.
        result = os.path.exists(os.path.join('test_data', 'restriction_review.csv'))
        expected = False
        self.assertEqual(expected, result, "Problem with test for no_restricted")

    def test_some_restricted(self):
        """Test for when some rows are restricted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'immigrant', 'a.txt'],
                              ['30601', 'immigration', 'b.txt'],
                              ['30602', np.nan, 'c.txt'],
                              ['30603', 'migrant', 'd.txt'],
                              ['30604', 'model citizen', 'd.txt'],
                              ['30605', 'fine to open', 'd.txt'],
                              ['30606', 'refugee', 'e.txt']],
                             columns=['zip_code', 'group_name', 'file_name'])
        restriction_report(md_df, 'test_data')

        # Tests the contents of restriction_review.csv.
        result = csv_to_list(os.path.join('test_data', 'restriction_review.csv'))
        expected = [['zip_code', 'group_name', 'file_name'],
                    ['30600', 'immigrant', 'a.txt'],
                    ['30601', 'immigration', 'b.txt'],
                    ['30603', 'migrant', 'd.txt'],
                    ['30606', 'refugee', 'e.txt']]
        self.assertEqual(expected, result, "Problem with test for some_restricted")


if __name__ == '__main__':
    unittest.main()
