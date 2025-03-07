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

    def test_function(self):
        """Test to develop the function. Not sure if I have variations or not."""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', np.nan, np.nan],
                              ['30602', 'Water', 'Water'],
                              ['30603', 'Water', 'Water'],
                              ['30604', 'Chess', 'Sports'],
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
                    ['BLANK', '2', '1', '3'],
                    ['Baseball', '1', '0', '1'],
                    ['Chess', '1', '0', '1'],
                    ['Pets', '0', '2', '2'],
                    ['Puppies', '2', '0', '2'],
                    ['Sports', '0', '4', '4'],
                    ['Water', '3', '2', '5']]
        self.assertEqual(result, expected, "Problem with test for function")


if __name__ == '__main__':
    unittest.main()
