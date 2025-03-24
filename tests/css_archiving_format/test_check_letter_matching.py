"""
Tests for the function check_letter_matching, which compares the letters in the metadata to the input directory.
To simplify testing, only a few columns are used for the dataframe.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_archiving_format import check_letter_matching
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the reports, if made by the test"""
        output_paths = [os.path.join('test_data', 'check_letter_matching', 'all'),
                        os.path.join('test_data', 'check_letter_matching', 'blanks'),
                        os.path.join('test_data', 'check_letter_matching', 'directory_only'),
                        os.path.join('test_data', 'check_letter_matching', 'match'),
                        os.path.join('test_data', 'check_letter_matching', 'metadata_only')]
        for output_path in output_paths:
            reports = [os.path.join(output_path, 'usability_report_matching.csv'), 
                       os.path.join(output_path, 'usability_report_matching_details.csv')]
            for report in reports:
                if os.path.exists(report):
                    os.remove(report)

    def test_all(self):
        """Test for all possible outcomes of matching and not matching"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', np.nan, np.nan],
                              ['30602', np.nan, r'..\BlobExport\documents\formletters\form_a.txt'],
                              ['30603', r'..\BlobExport\documents\indivletters\300.txt', np.nan],
                              ['30604', r'..\BlobExport\documents\indivletters\400.txt',
                               r'..\BlobExport\documents\formletters\form_b.txt']],
                             columns=['zip', 'in_document_name', 'out_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching', 'all')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', 2],
                    ['Directory_Only', 4],
                    ['Match', 2],
                    ['Metadata_Blank', 4]]
        self.assertEqual(result, expected, "Problem with test for all, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'), sort=True)
        expected = [['Category', 'Path'],
                    ['Directory Only', f'{input_directory}\\documents\\formletters\\form_c.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\indivletters\\100.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\indivletters\\200.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\indivletters\\500.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\formletters\\form_b.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\indivletters\\300.txt']]
        self.assertEqual(result, expected, "Problem with test for all, details")

    def test_blanks(self):
        """Test for when the document columns include blanks"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', np.nan, np.nan],
                              ['30602', np.nan, np.nan],
                              ['30603', np.nan, np.nan],
                              ['30604', r'..\BlobExport\documents\indivletters\400.txt',
                              np.nan],
                              ['30605', np.nan, r'..\BlobExport\documents\formletters\form_c.txt']],
                             columns=['zip', 'in_document_name', 'out_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching', 'blanks')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', 0],
                    ['Directory_Only', 0],
                    ['Match', 2],
                    ['Metadata_Blank', 8]]
        self.assertEqual(result, expected, "Problem with test for blanks, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        expected = [['Category', 'Path']]
        self.assertEqual(result, expected, "Problem with test for blanks, details")

    def test_directory_only(self):
        """Test for when some letters are in the directory but not the metadata"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', r'..\BlobExport\documents\indivletters\100.txt',
                               r'..\BlobExport\documents\formletters\form_a.txt']],
                             columns=['zip', 'in_document_name', 'out_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching', 'directory_only')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', 0],
                    ['Directory_Only', 6],
                    ['Match', 2],
                    ['Metadata_Blank', 0]]
        self.assertEqual(result, expected, "Problem with test for directory_only, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'), sort=True)
        expected = [['Category', 'Path'],
                    ['Directory Only', f'{input_directory}\\documents\\formletters\\form_b.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\formletters\\form_c.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\indivletters\\200.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\indivletters\\300.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\indivletters\\400.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\indivletters\\500.txt']]
        self.assertEqual(result, expected, "Problem with test for directory_only, details")

    def test_match(self):
        """Test for when the metadata and input directory match (some repeat)"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', r'..\BlobExport\documents\indivletters\100.txt',
                               r'..\BlobExport\documents\formletters\form_a.txt'],
                              ['30602', r'..\BlobExport\documents\indivletters\200.txt',
                               r'..\BlobExport\documents\formletters\form_a.txt'],
                              ['30603', r'..\BlobExport\documents\indivletters\300.txt',
                              r'..\BlobExport\documents\formletters\form_b.txt'],
                              ['30604', r'..\BlobExport\documents\indivletters\400.txt',
                              r'..\BlobExport\documents\formletters\form_b.txt'],
                              ['30605', r'..\BlobExport\documents\indivletters\500.txt',
                              r'..\BlobExport\documents\formletters\form_c.txt']],
                             columns=['zip', 'in_document_name', 'out_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching', 'match')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', 0],
                    ['Directory_Only', 0],
                    ['Match', 8],
                    ['Metadata_Blank', 0]]
        self.assertEqual(result, expected, "Problem with test for match, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        expected = [['Category', 'Path']]
        self.assertEqual(result, expected, "Problem with test for match, details")

    def test_metadata_only(self):
        """Test for when some letters are in the metadata but not the directory"""
        # Makes variables to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', r'..\BlobExport\documents\indivletters\100.txt',
                               r'..\BlobExport\documents\formletters\form_a.txt'],
                              ['30602', r'..\BlobExport\documents\indivletters\200.txt',
                               r'..\BlobExport\documents\formletters\form_a.txt'],
                              ['30603', r'..\BlobExport\documents\indivletters\300.txt',
                              r'..\BlobExport\documents\formletters\form_b.txt'],
                              ['30604', r'..\BlobExport\documents\indivletters\400.txt',
                              r'..\BlobExport\documents\formletters\form_b.txt'],
                              ['30605', r'..\BlobExport\documents\indivletters\500.txt',
                              r'..\BlobExport\documents\formletters\form_c.txt']],
                             columns=['zip', 'in_document_name', 'out_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching', 'metadata_only')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', 7],
                    ['Directory_Only', 0],
                    ['Match', 1],
                    ['Metadata_Blank', 0]]
        self.assertEqual(result, expected, "Problem with test for metadata_only, summary")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'), sort=True)
        expected = [['Category', 'Path'],
                    ['Metadata Only', f'{input_directory}\\documents\\formletters\\form_b.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\formletters\\form_c.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\indivletters\\100.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\indivletters\\200.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\indivletters\\300.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\indivletters\\400.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\indivletters\\500.txt']]
        self.assertEqual(result, expected, "Problem with test for metadata_only, details")


if __name__ == '__main__':
    unittest.main()
