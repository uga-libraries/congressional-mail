"""
Test for the function check_letter_matching(), which compares the letters in the metadata to the input directory.
To simplify testing, only a few columns are used for the dataframe.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_data_interchange_format import check_letter_matching
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the reports, if made by the test"""
        for report in ('usability_report_matching.csv', 'usability_report_matching_details.csv'):
            report_path = os.path.join('test_data', 'test_check_letter_matching', report)
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_match(self):
        """Test for when the document column includes blanks (the rest match)"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['ga', '30601', r'..\documents\formletters\form_a.txt'],
                              ['ga', '30601', r'..\documents\formletters\form_b.txt'],
                              ['ga', '30601', r'..\documents\objects\100.txt'],
                              ['ga', '30601', r'..\documents\objects\200.txt'],
                              ['ga', '30601', r'..\documents\objects\300.txt']],
                             columns=['state_code', 'zip_code', 'communication_document_name'])
        output_directory = os.path.join('test_data', 'test_check_letter_matching')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '0'],
                    ['Directory_Only', '0'],
                    ['Match', '5'],
                    ['Metadata_Blank', '0']]
        self.assertEqual(result, expected, "Problem with test for match, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        expected = [['Category', 'Path']]
        self.assertEqual(result, expected, "Problem with test for match, details")

    def test_metadata_only(self):
        """Test for when some file paths are in the metadata but not the directory"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['ga', '30601', r'..\documents\formletters\form_a.txt'],
                              ['ga', '30601', r'..\documents\formletters\form_b.txt'],
                              ['ga', '30601', r'..\documents\formletters\form_c.txt'],
                              ['ga', '30601', r'..\documents\objects\100.txt'],
                              ['ga', '30601', r'..\documents\objects\200.txt'],
                              ['ga', '30601', r'..\documents\objects\202.txt'],
                              ['ga', '30601', r'..\documents\objects\300.txt'],
                              ['ga', '30601', r'..\documents\objects\303.txt']],
                             columns=['state_code', 'zip_code', 'communication_document_name'])
        output_directory = os.path.join('test_data', 'test_check_letter_matching')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '3'],
                    ['Directory_Only', '0'],
                    ['Match', '5'],
                    ['Metadata_Blank', '0']]
        self.assertEqual(result, expected, "Problem with test for metadata_only, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        result.sort()
        expected = [['Category', 'Path'],
                    ['Metadata Only', fr'{input_directory}\documents\formletters\form_c.txt'],
                    ['Metadata Only', fr'{input_directory}\documents\objects\202.txt'],
                    ['Metadata Only', fr'{input_directory}\documents\objects\303.txt']]
        self.assertEqual(result, expected, "Problem with test for metadata_only, details")


if __name__ == '__main__':
    unittest.main()
