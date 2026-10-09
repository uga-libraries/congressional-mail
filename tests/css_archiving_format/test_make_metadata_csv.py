import os
import unittest
from css_archiving_format import make_metadata_csv
from test_script import csv_to_list


def make_doc(doc_path, lines):
    """Make a document.txt file in the specified location to determine an AIP's size"""
    with open(os.path.join(doc_path, 'document.txt'), 'w') as new_file:
        for i in range(lines):
            new_file.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')

class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the CSV and document added for size, if made"""
        test_names = ['missing_metadata', 'size_differences', 'year_differences']
        for test_name in test_names:
            test_path = os.path.join('test_data', 'make_metadata_csv', test_name)
            if os.path.exists(os.path.join(test_path, 'aspace_inventory.csv')):
                os.remove(os.path.join(test_path, 'aspace_inventory.csv'))
            by_topic_path = os.path.join(test_path, 'correspondence_by_topic')
            for topic in os.listdir(by_topic_path):
                if os.path.exists(os.path.join(by_topic_path, topic, 'document.txt')):
                    os.remove(os.path.join(by_topic_path, topic, 'document.txt'))

    def test_missing_metadata(self):
        """Testing error handling for if there is no metadata.csv to get the years"""
        # Makes variable needed for input, adds a file to each topic to determine the size, and runs the function.
        output_directory = os.path.join('test_data', 'make_metadata_csv', 'missing_metadata')
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'cats'), 1000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'dogs'), 3000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'farm'), 5000)
        make_metadata_csv(output_directory)

        # Tests the contents of aspace_inventory.csv.
        result = csv_to_list(os.path.join(output_directory, 'aspace_inventory.csv'))
        expected = [['title', 'start_date', 'end_date', 'extent'],
                    ['cats [electronic files]', 'unknown', 'unknown', '0.0001'],
                    ['dogs [electronic files]', '2021', '2024', '0.0002'],
                    ['farm [electronic files]', 'unknown', 'unknown', '0.0003']]
        self.assertEqual(expected, result, "Problem with test for missing metadata")

    def test_size_differences(self):
        """Testing error handling for if there is no metadata.csv to get the years"""
        # Makes variable needed for input, adds a file to each topic to determine the size, and runs the function.
        output_directory = os.path.join('test_data', 'make_metadata_csv', 'size_differences')
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', '2-decimal'), 500000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', '4-decimal-down'), 2000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', '4-decimal-up'), 11000)
        make_metadata_csv(output_directory)

        # Tests the contents of aspace_inventory.csv.
        result = csv_to_list(os.path.join(output_directory, 'aspace_inventory.csv'))
        expected = [['title', 'start_date', 'end_date', 'extent'],
                    ['2-decimal [electronic files]', '1999', '1999', '0.026'],
                    ['4-decimal-down [electronic files]', '2001', '2003', '0.0001'],
                    ['4-decimal-up [electronic files]', '2001', '2003', '0.001']]
        self.assertEqual(expected, result, "Problem with test for missing metadata")

    def test_year_differences(self):
        """Testing variations related to start and end year (see titles)"""
        # Makes variable needed for input, adds a file to each topic to determine the size, and runs the function.
        output_directory = os.path.join('test_data', 'make_metadata_csv', 'year_differences')
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'blank years'), 10000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'multiple years'), 50000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'one year'), 70000)
        make_metadata_csv(output_directory)

        # Tests the contents of aspace_inventory.csv.
        result = csv_to_list(os.path.join(output_directory, 'aspace_inventory.csv'))
        expected = [['title', 'start_date', 'end_date', 'extent'],
                    ['blank years [electronic files]', '2011', '2023', '0.001'],
                    ['multiple years [electronic files]', '2001', '2003', '0.003'],
                    ['one year [electronic files]', '1999', '1999', '0.004']]
        self.assertEqual(expected, result, "Problem with test for year differences")


if __name__ == '__main__':
    unittest.main()
