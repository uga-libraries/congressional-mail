"""
Test for the function check_letter_matching(), which compares the letters in the metadata to the input directory.
To simplify testing, only a few columns are used for the dataframe.
"""
import numpy as np
import os
import pandas as pd
import unittest
from cms_data_interchange_format import check_letter_matching
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the reports, if made by the test"""
        for report in ('usability_report_matching.csv', 'usability_report_matching_details.csv'):
            report_path = os.path.join('test_data', 'check_letter_matching', report)
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_all(self):
        """Test for all matching variations"""
        # Makes variables to use as test input and runs the function.
        rows_list = [['20220101', 'forms\\extra.txt'],
                     ['20220102', 'forms\\2.txt'],
                     ['20220103', 'forms\\3.txt'],
                     ['20210402', np.nan],
                     ['20240501', 'in-email\\1.txt'],
                     ['20240503', 'in-email\\extra.txt']]
        md_df = pd.DataFrame(rows_list, columns=['date_in', 'correspondence_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '2'],
                    ['Directory_Only', '3'],
                    ['Match', '3'],
                    ['Metadata_Blank', '1']]
        self.assertEqual(result, expected, "Problem with test for all, matching csv")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'), sort=True)
        expected = [['Category', 'Path'],
                    ['Directory Only', f'{input_directory}\\documents\\forms\\1.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\in-email\\2.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\in-email\\3.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\forms\\extra.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\in-email\\extra.txt'],]
        self.assertEqual(result, expected, "Problem with test for all, matching details csv")

    def test_blanks(self):
        """Test for when the document column includes blanks"""
        # Makes variables to use as test input and runs the function.
        rows_list = [['20210401', np.nan], ['20210402', np.nan], ['20210403', np.nan],
                     ['20220101', 'forms\\1.txt'], ['20220102', 'forms\\2.txt'], ['20220103', 'forms\\3.txt'],
                     ['20210404', np.nan], ['20210405', np.nan], ['20210406', np.nan],
                     ['20240501', 'in-email\\1.txt'], ['20240502', 'in-email\\2.txt'], ['20240503', 'in-email\\3.txt'],
                     ['20210407', np.nan], ['20210408', np.nan], ['20210409', np.nan],]
        md_df = pd.DataFrame(rows_list, columns=['date_in', 'correspondence_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '0'],
                    ['Directory_Only', '0'],
                    ['Match', '6'],
                    ['Metadata_Blank', '9']]
        self.assertEqual(result, expected, "Problem with test for blanks, matching csv")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        expected = [['Category', 'Path']]
        self.assertEqual(result, expected, "Problem with test for blanks, matching details csv")

    def test_directory_only(self):
        """Test for when some file paths are in the directory but not the metadata"""
        # Makes variables to use as test input and runs the function.
        rows_list = [['20220101', 'forms\\1.txt'], ['20220103', 'forms\\3.txt'], ['20240502', 'in-email\\2.txt']]
        md_df = pd.DataFrame(rows_list, columns=['date_in', 'correspondence_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '0'],
                    ['Directory_Only', '3'],
                    ['Match', '3'],
                    ['Metadata_Blank', '0']]
        self.assertEqual(result, expected, "Problem with test for directory_only, matching csv")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'), sort=True)
        expected = [['Category', 'Path'],
                    ['Directory Only', f'{input_directory}\\documents\\forms\\2.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\in-email\\1.txt'],
                    ['Directory Only', f'{input_directory}\\documents\\in-email\\3.txt']]
        self.assertEqual(result, expected, "Problem with test for directory_only, matching details csv")

    def test_duplicates(self):
        """Test for when the document column includes duplicates, which are not counted"""
        # Makes variables to use as test input and runs the function.
        rows_list = [['20220101', 'forms\\1.txt'], ['20220102', 'forms\\2.txt'], ['20220103', 'forms\\3.txt'],
                     ['20220103', 'forms\\3.txt'], ['20240501', 'in-email\\1.txt'], ['20240501', 'in-email\\1.txt'],
                     ['20240501', 'in-email\\1.txt'], ['20240502', 'in-email\\2.txt'], ['20240503', 'in-email\\3.txt']]
        md_df = pd.DataFrame(rows_list, columns=['date_in', 'correspondence_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '0'],
                    ['Directory_Only', '0'],
                    ['Match', '6'],
                    ['Metadata_Blank', '0']]
        self.assertEqual(result, expected, "Problem with test for duplicates, matching csv")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        expected = [['Category', 'Path']]
        self.assertEqual(result, expected, "Problem with test for duplicates, matching details csv")

    def test_match(self):
        """Test for when the document column matches the directory contents"""
        # Makes variables to use as test input and runs the function.
        rows_list = [['20220101', 'forms\\1.txt'], ['20220102', 'forms\\2.txt'], ['20220103', 'forms\\3.txt'],
                     ['20240501', 'in-email\\1.txt'], ['20240502', 'in-email\\2.txt'], ['20240503', 'in-email\\3.txt']]
        md_df = pd.DataFrame(rows_list, columns=['date_in', 'correspondence_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '0'],
                    ['Directory_Only', '0'],
                    ['Match', '6'],
                    ['Metadata_Blank', '0']]
        self.assertEqual(result, expected, "Problem with test for match, matching csv")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'))
        expected = [['Category', 'Path']]
        self.assertEqual(result, expected, "Problem with test for match, matching details csv")

    def test_metadata_only(self):
        """Test for when some file paths are in the metadata but not the directory"""
        # Makes variables to use as test input and runs the function.
        rows_list = [['20211013', 'documents\\1.txt'], ['20211017', 'forms\\extra.txt'],
                     ['20220101', 'forms\\1.txt'], ['20220102', 'forms\\2.txt'], ['20220103', 'forms\\3.txt'],
                     ['20240501', 'in-email\\1.txt'], ['20240502', 'in-email\\2.txt'], ['20240503', 'in-email\\3.txt']]
        md_df = pd.DataFrame(rows_list, columns=['date_in', 'correspondence_document_name'])
        output_directory = os.path.join('test_data', 'check_letter_matching')
        input_directory = os.path.join(output_directory, 'Name_Constituent_Mail_Export')
        check_letter_matching(md_df, output_directory, input_directory)

        # Tests the values in usability_report_matching.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching.csv'))
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '2'],
                    ['Directory_Only', '0'],
                    ['Match', '6'],
                    ['Metadata_Blank', '0']]
        self.assertEqual(result, expected, "Problem with test for metadata_only, matching csv")

        # Tests the values in usability_report_matching_details.csv are correct.
        result = csv_to_list(os.path.join(output_directory, 'usability_report_matching_details.csv'), sort=True)
        expected = [['Category', 'Path'],
                    ['Metadata Only', f'{input_directory}\\documents\\documents\\1.txt'],
                    ['Metadata Only', f'{input_directory}\\documents\\forms\\extra.txt']]
        self.assertEqual(result, expected, "Problem with test for metadata_only, matching details csv")


if __name__ == '__main__':
    unittest.main()
