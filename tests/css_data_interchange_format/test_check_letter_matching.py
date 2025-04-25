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

    def test_all(self):
        """Test for all matching variations"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['GA', '30600', np.nan],
                              ['GA', '30601', r'..\documents\formletters\form_a.txt'],
                              ['GA', '30601', r'..\documents\formletters\form_a.txt'],
                              ['GA', '30602', r'..\documents\formletters\form_c.txt'],
                              ['GA', '30602-0001', r'..\documents\formletters\form_c.txt'],
                              ['GA', '30603', r'..\documents\objects\100.txt'],
                              ['GA', '30604', r'..\documents\200.txt'],
                              ['GA', '30605', r'..\documents\201.txt'],
                              ['GA', '30605', r'..\documents\202.txt']],
                             columns=['state_code', 'zip_code', 'communication_document_name'])
        output_directory = os.path.join('test_data', 'test_check_letter_matching')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '4'],
                    ['Directory_Only', '3'],
                    ['Match', '2'],
                    ['Metadata_Blank', '1']]
        self.assertEqual(result, expected, "Problem with test for all, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        result.sort()
        expected = [['Category', 'Path'],
                    ['Directory Only', fr'{input_directory}\documents\formletters\form_b.txt'],
                    ['Directory Only', fr'{input_directory}\documents\objects\200.txt'],
                    ['Directory Only', fr'{input_directory}\documents\objects\300.txt'],
                    ['Metadata Only', fr'{input_directory}\documents\200.txt'],
                    ['Metadata Only', fr'{input_directory}\documents\201.txt'],
                    ['Metadata Only', fr'{input_directory}\documents\202.txt'],
                    ['Metadata Only', fr'{input_directory}\documents\formletters\form_c.txt']]
        self.assertEqual(result, expected, "Problem with test for all, details")

    def test_blanks(self):
        """Test for when the document column includes blanks"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['GA', '30600', np.nan],
                              ['GA', '30601', r'..\documents\formletters\form_a.txt'],
                              ['GA', '30602', r'..\documents\formletters\form_b.txt'],
                              ['GA', '30602-0001', np.nan],
                              ['GA', '30603', r'..\documents\objects\100.txt'],
                              ['GA', '30604', r'..\documents\objects\200.txt'],
                              ['GA', '30605', r'..\documents\objects\300.txt'],
                              ['GA', '30606', np.nan],],
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
                    ['Metadata_Blank', '3']]
        self.assertEqual(result, expected, "Problem with test for blanks, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        expected = [['Category', 'Path']]
        self.assertEqual(result, expected, "Problem with test for blanks, details")

    def test_directory_only(self):
        """Test for when some file paths are in the directory but not the metadata"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['GA', '30601', r'..\documents\formletters\form_a.txt'],
                              ['GA', '30603', r'..\documents\objects\100.txt']],
                             columns=['state_code', 'zip_code', 'communication_document_name'])
        output_directory = os.path.join('test_data', 'test_check_letter_matching')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '0'],
                    ['Directory_Only', '3'],
                    ['Match', '2'],
                    ['Metadata_Blank', '0']]
        self.assertEqual(result, expected, "Problem with test for directory_only, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        result.sort()
        expected = [['Category', 'Path'],
                    ['Directory Only', fr'{input_directory}\documents\formletters\form_b.txt'],
                    ['Directory Only', fr'{input_directory}\documents\objects\200.txt'],
                    ['Directory Only', fr'{input_directory}\documents\objects\300.txt']]
        self.assertEqual(result, expected, "Problem with test for directory_only, details")

    def test_duplicates(self):
        """Test for when the document column includes duplicates"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['GA', '30601', r'..\documents\formletters\form_a.txt'],
                              ['GA', '30602', r'..\documents\formletters\form_b.txt'],
                              ['GA', '30602', r'..\documents\formletters\form_b.txt'],
                              ['GA', '30602', r'..\documents\formletters\form_b.txt'],
                              ['GA', '30603', r'..\documents\objects\100.txt'],
                              ['GA', '30604', r'..\documents\objects\200.txt'],
                              ['GA', '30604', r'..\documents\objects\200.txt'],
                              ['GA', '30605', r'..\documents\objects\300.txt']],
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
        self.assertEqual(result, expected, "Problem with test for duplicates, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        expected = [['Category', 'Path']]
        self.assertEqual(result, expected, "Problem with test for duplicates, details")

    def test_match(self):
        """Test for when the document column matches the directory contents"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['GA', '30601', r'..\documents\formletters\form_a.txt'],
                              ['GA', '30602', r'..\documents\formletters\form_b.txt'],
                              ['GA', '30603', r'..\documents\objects\100.txt'],
                              ['GA', '30604', r'..\documents\objects\200.txt'],
                              ['GA', '30605', r'..\documents\objects\300.txt']],
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
        md_df = pd.DataFrame([['GA', '30601', r'..\documents\formletters\form_a.txt'],
                              ['GA', '30602', r'..\documents\formletters\form_b.txt'],
                              ['GA', '30606', r'..\documents\formletters\form_c.txt'],
                              ['GA', '30603', r'..\documents\objects\100.txt'],
                              ['GA', '30604', r'..\documents\objects\200.txt'],
                              ['GA', '30607', r'..\documents\objects\202.txt'],
                              ['GA', '30605', r'..\documents\objects\300.txt'],
                              ['GA', '30608', r'..\documents\objects\303.txt']],
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
