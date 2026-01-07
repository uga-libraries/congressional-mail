import os
import unittest
from aip_prep import metadata_csv
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the metadata.csv, if made"""
        csv_path = os.path.join(os.getcwd(), 'metadata.csv')
        if os.path.exists(csv_path):
            os.remove(csv_path)

    def test_new(self):
        """Test for making the metadata.csv for the first time"""
        # Runs the function.
        csv_path = os.path.join(os.getcwd(), 'metadata.csv')
        metadata_csv(csv_path, 'header')

        # Tests the contents of the metadata.csv.
        result = csv_to_list(csv_path)
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version']]
        self.assertEqual(expected, result, "Problem with test for new metadata.csv")

    def test_addition(self):
        """Test for adding rows to an existing metadata.csv"""
        # Runs the function three times, the first time to make it and the other two to add to an existing csv.
        csv_path = os.path.join(os.getcwd(), 'metadata.csv')
        metadata_csv(csv_path, 'header')
        metadata_csv(csv_path, ['', '', 'metadata', '', 'Constituent Mail Metadata', '1'])
        metadata_csv(csv_path, ['', '', 'form_1', '', 'Constituent Mail Form 1', '1'])
        metadata_csv(csv_path, ['', '', 'form_2', '', 'Constituent Mail Form 2', '1'])

        # Tests the contents of the metadata.csv.
        result = csv_to_list(csv_path)
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'],
                    ['BLANK', 'BLANK', 'metadata', 'BLANK', 'Constituent Mail Metadata', 1],
                    ['BLANK', 'BLANK', 'form_1', 'BLANK', 'Constituent Mail Form 1', 1],
                    ['BLANK', 'BLANK', 'form_2', 'BLANK', 'Constituent Mail Form 2', 1]]
        self.assertEqual(expected, result, "Problem with test for addition to metadata.csv")


if __name__ == '__main__':
    unittest.main()
