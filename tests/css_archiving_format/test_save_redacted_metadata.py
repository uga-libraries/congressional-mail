import os
import shutil

import pandas as pd
import unittest
from css_archiving_format import save_redacted_metadata
from test_script import csv_to_list


def make_df(rows):
    """Make a df for test input"""
    column_names = ['in_date', 'in_topic', 'in_document_name', 'out_date', 'out_topic', 'out_document_name',
                    'in_document_name_split', 'out_document_name_split']
    df = pd.DataFrame(rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the CSV and folder of CSVs by year, if made"""
        csv_path = os.path.join('test_data', 'archiving_correspondence_redacted.csv')
        if os.path.exists(csv_path):
            os.remove(csv_path)
        csv_folder = os.path.join('test_data', 'correspondence_metadata_by_year')
        if os.path.exists(csv_folder):
            shutil.rmtree(csv_folder)

    def test_duplicate(self):
        """Test when there are duplicate rows from delimiters in the document name columns"""
        # Makes test input and runs the function.
        rows = [['20001010', 'A', '1.txt^2.txt^3.txt', '20001011', 'AA', 'A.txt', '1.txt', 'A.txt'],
                ['20001010', 'A', '1.txt^2.txt^3.txt', '20001011', 'AA', 'A.txt', '2.txt', 'A.txt'],
                ['20001010', 'A', '1.txt^2.txt^3.txt', '20001011', 'AA', 'A.txt', '3.txt', 'A.txt'],
                ['20001010', 'B', '4.txt^5.txt', '20001011', 'BB', 'B1.txt^B2.txt', '4.txt', 'B1.txt'],
                ['20001010', 'B', '4.txt^5.txt', '20001011', 'BB', 'B1.txt^B2.txt', '4.txt', 'B2.txt'],
                ['20001010', 'B', '4.txt^5.txt', '20001011', 'BB', 'B1.txt^B2.txt', '5.txt', 'B1.txt'],
                ['20001010', 'B', '4.txt^5.txt', '20001011', 'BB', 'B1.txt^B2.txt', '5.txt', 'B2.txt']]
        df = make_df(rows)
        save_redacted_metadata(df, 'test_data')

        # Verifies the CSV has the expected contents.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_redacted.csv'))
        expected = [['in_date', 'in_topic', 'in_document_name', 'out_date', 'out_topic', 'out_document_name'],
                    ['20001010', 'A', '1.txt^2.txt^3.txt', '20001011', 'AA', 'A.txt'],
                    ['20001010', 'B', '4.txt^5.txt', '20001011', 'BB', 'B1.txt^B2.txt']]
        self.assertEqual(expected, result, "Problem with test for duplicate, csv")

    def test_unique(self):
        """Test when there are no duplicate rows because there were no delimiters in the document name columns"""
        # Makes test input and runs the function.
        rows = [['20001010', 'A', '1.txt', '20001011', 'AA', 'A.txt', '1.txt', 'A.txt'],
                ['20001010', 'A', '2.txt', '20001011', 'AA', 'A.txt', '2.txt', 'A.txt'],
                ['20001010', 'B', '3.txt', '20001011', 'BB', 'B.txt', '3.txt', 'B.txt']]
        df = make_df(rows)
        save_redacted_metadata(df, 'test_data')

        # Verifies the CSV has the expected contents.
        result = csv_to_list(os.path.join('test_data', 'archiving_correspondence_redacted.csv'))
        expected = [['in_date', 'in_topic', 'in_document_name', 'out_date', 'out_topic', 'out_document_name'],
                    ['20001010', 'A', '1.txt', '20001011', 'AA', 'A.txt'],
                    ['20001010', 'A', '2.txt', '20001011', 'AA', 'A.txt'],
                    ['20001010', 'B', '3.txt', '20001011', 'BB', 'B.txt']]
        self.assertEqual(expected, result, "Problem with test for unique, csv")


if __name__ == '__main__':
    unittest.main()
