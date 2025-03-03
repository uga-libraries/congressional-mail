"""
Tests for the function topics_report(), which makes a report of the number of times each topic is used.
To simplify testing, md_df has only a few of the columns that are in a normal export.
"""
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

    def test_function(self):
        """Test to develop the function. Not sure if I have variations or not."""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([[]], columns=['zip', 'in_topic', 'out_topic'])
        topics_report(md_df, 'test_data')

        # Tests the contents of the file deletion log.
        result = csv_to_list(os.path.join('test_data', 'topics_report.csv'))
        expected = [[]]
        self.assertEqual(result, expected, "Problem with test for function")


if __name__ == '__main__':
    unittest.main()
