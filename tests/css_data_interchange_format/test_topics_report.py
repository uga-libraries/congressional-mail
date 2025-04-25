"""
Tests for the function topics_report(). which makes a report of the number of times each topic is used.
To simplify testing, md_df has only a few of the columns that are in a normal export.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_data_interchange_format import topics_report
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the report, if made by the test"""
        report_path = os.path.join('test_data', 'topics_report.csv')
        if os.path.exists(report_path):
            os.remove(report_path)

    def test_all(self):
        """Test for all variations of group"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Farms'], ['30601', np.nan], ['30602', 'Pet Parade'],
                              ['30603', 'Farms'], ['30604', 'Farms'], ['30606', 'education']],
                             columns=['zip_code', 'group_name'])
        topics_report(md_df, 'test_data')

        # Tests the contents of the topics report.
        result = csv_to_list(os.path.join('test_data', 'topics_report.csv'))
        expected = [['Topic', 'Topic_Count'],
                    ['Farms', '3'],
                    ['BLANK', '1'],
                    ['Pet Parade', '1'],
                    ['education', '1']]
        self.assertEqual(result, expected, "Problem with test for all")

    def test_blanks(self):
        """Test for when group is blank"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', np.nan], ['30601', np.nan], ['30602', np.nan],
                              ['30603', np.nan], ['30604', np.nan], ['30606', np.nan]],
                             columns=['zip_code', 'group_name'])
        topics_report(md_df, 'test_data')

        # Tests the contents of the topics report.
        result = csv_to_list(os.path.join('test_data', 'topics_report.csv'))
        expected = [['Topic', 'Topic_Count'],
                    ['BLANK', '6']]
        self.assertEqual(result, expected, "Problem with test for blanks")

    def test_repeat(self):
        """Test for when groups are repeated"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Econ'], ['30601', 'Farms'], ['30602', 'Farms'],
                              ['30603', 'Econ'], ['30604', 'Farms'], ['30605', 'Farms'],
                              ['30606', 'Pets'], ['30607', 'Pets'], ['30608', 'Pets']],
                             columns=['zip_code', 'group_name'])
        topics_report(md_df, 'test_data')

        # Tests the contents of the topics report.
        result = csv_to_list(os.path.join('test_data', 'topics_report.csv'))
        expected = [['Topic', 'Topic_Count'],
                    ['Farms', '4'],
                    ['Pets', '3'],
                    ['Econ', '2']]
        self.assertEqual(result, expected, "Problem with test for repeat")

    def test_unique(self):
        """Test for when each group is used once"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Econ'], ['30601', 'farm - aid'], ['30602', 'pets']],
                             columns=['zip_code', 'group_name'])
        topics_report(md_df, 'test_data')

        # Tests the contents of the topics report.
        result = csv_to_list(os.path.join('test_data', 'topics_report.csv'))
        expected = [['Topic', 'Topic_Count'],
                    ['Econ', '1'],
                    ['farm - aid', '1'],
                    ['pets', '1']]
        self.assertEqual(result, expected, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
