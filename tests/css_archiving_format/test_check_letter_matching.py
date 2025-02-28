"""
Tests for the function check_letter_matching, which compares the letters in the metadata to the input directory.
To simplify testing, only a few columns are used for the dataframe.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_archiving_format import check_letter_matching
from test_check_metadata_usability import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the report, if made by the test"""
        report_path = os.path.join('test_data', 'check_letter_matching', 'usability_report_matching.csv')
        if os.path.exists(report_path):
            os.remove(report_path)

    def test_match(self):
        """Test for when the metadata and input directory match."""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([[]], columns=[])
        output_directory = os.path.join('test_data', 'check_letter_matching')
        input_directory = os.path.join('test_data', 'check_letter_matching', 'match')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', 0],
                    ['Directory_Only', 0],
                    ['Match', 'tbd'],
                    ['Metadata_Blank', 0]]
        self.assertEqual(result, expected, "Problem with test for match")


if __name__ == '__main__':
    unittest.main()
