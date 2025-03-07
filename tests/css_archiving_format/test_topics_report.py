"""
Tests for the function topics_report(), which makes a report of the number of times each topic is used.
To simplify testing, md_df has only a few of the columns that are in a normal export.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_archiving_format import topics_report
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the report, if made by the test"""
        report_path = os.path.join('test_data', 'topics_report.csv')
        if os.path.exists(report_path):
            os.remove(report_path)

    def test_all(self):
        """Test for when all data variations are present."""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', np.nan, 'Food'],
                              ['30602', 'Water', 'Water'],
                              ['30603', 'Water', 'Water'],
                              ['30604', 'Chess', 'Chess'],
                              ['30604', 'Baseball', 'Sports'],
                              ['30605', np.nan, 'Sports'],
                              ['30606', 'Water', 'Sports'],
                              ['30607', 'Puppies', 'Pets'],
                              ['30608', 'Puppies', 'Pets']],
                             columns=['zip', 'in_topic', 'out_topic'])
        topics_report(md_df, 'test_data')

        # Tests the contents of the file deletion log.
        result = csv_to_list(os.path.join('test_data', 'topics_report.csv'))
        expected = [['Topic', 'In_Topic_Count', 'Out_Topic_Count', 'Total'],
                    ['BLANK', '2', '0', '2'],
                    ['Baseball', '1', '0', '1'],
                    ['Chess', '1', '1', '2'],
                    ['Food', '0', '1', '1'],
                    ['Pets', '0', '2', '2'],
                    ['Puppies', '2', '0', '2'],
                    ['Sports', '0', '3', '3'],
                    ['Water', '3', '2', '5']]
        self.assertEqual(result, expected, "Problem with test for all")

    def test_blanks(self):
        """Test for when there are blanks in both topic columns."""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', np.nan, np.nan],
                              ['30602', 'Water', np.nan],
                              ['30603', np.nan, 'Water'],
                              ['30604', np.nan, 'Water']],
                             columns=['zip', 'in_topic', 'out_topic'])
        topics_report(md_df, 'test_data')

        # Tests the contents of the file deletion log.
        result = csv_to_list(os.path.join('test_data', 'topics_report.csv'))
        expected = [['Topic', 'In_Topic_Count', 'Out_Topic_Count', 'Total'],
                    ['BLANK', '3', '2', '5'],
                    ['Water', '1', '2', '3']]
        self.assertEqual(result, expected, "Problem with test for blanks")

    def test_shared(self):
        """Test for when the topics are both the in and out columns."""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', 'Water', 'Water'],
                              ['30602', 'Water', 'Water'],
                              ['30603', 'Sports', 'Baseball'],
                              ['30604', 'Baseball', 'Sports'],
                              ['30605', 'Puppies', 'Pets'],
                              ['30606', 'Puppies', 'Pets'],
                              ['30607', 'Puppies', 'Pets'],
                              ['30608', 'Pets', 'Puppies']],
                             columns=['zip', 'in_topic', 'out_topic'])
        topics_report(md_df, 'test_data')

        # Tests the contents of the file deletion log.
        result = csv_to_list(os.path.join('test_data', 'topics_report.csv'))
        expected = [['Topic', 'In_Topic_Count', 'Out_Topic_Count', 'Total'],
                    ['Baseball', '1', '1', '2'],
                    ['Pets', '1', '3', '4'],
                    ['Puppies', '3', '1', '4'],
                    ['Sports', '1', '1', '2'],
                    ['Water', '2', '2', '4']]
        self.assertEqual(result, expected, "Problem with test for shared")

    def test_unique(self):
        """Test for when the topics are only the in or out columns."""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', 'Chess', 'Sports'],
                              ['30602', 'Water', 'Ecology'],
                              ['30603', 'Water', 'Sports']],
                             columns=['zip', 'in_topic', 'out_topic'])
        topics_report(md_df, 'test_data')

        # Tests the contents of the file deletion log.
        result = csv_to_list(os.path.join('test_data', 'topics_report.csv'))
        expected = [['Topic', 'In_Topic_Count', 'Out_Topic_Count', 'Total'],
                    ['Chess', '1', '0', '1'],
                    ['Ecology', '0', '1', '1'],
                    ['Sports', '0', '2', '2'],
                    ['Water', '2', '0', '2']]
        self.assertEqual(result, expected, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
