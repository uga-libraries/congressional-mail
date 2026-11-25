import os
import unittest
from css_data_interchange_format import make_finding_aid_inventory
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
            test_path = os.path.join('test_data', 'make_finding_aid_inventory', test_name)
            if os.path.exists(os.path.join(test_path, 'finding_aid_inventory.csv')):
                os.remove(os.path.join(test_path, 'finding_aid_inventory.csv'))
            by_topic_path = os.path.join(test_path, 'correspondence_by_topic')
            for topic in os.listdir(by_topic_path):
                if os.path.exists(os.path.join(by_topic_path, topic, 'document.txt')):
                    os.remove(os.path.join(by_topic_path, topic, 'document.txt'))

    def test_missing_metadata(self):
        """Testing error handling for if there is no metadata.csv to get the years"""
        # Makes variable needed for input, adds a file to each topic to determine the size, and runs the function.
        output_directory = os.path.join(os.getcwd(), 'test_data', 'make_finding_aid_inventory', 'missing_metadata')
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'cats'), 1000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'dogs'), 3000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'farm'), 5000)
        make_finding_aid_inventory(output_directory)

        # Tests the contents of finding_aid_inventory.csv.
        result = csv_to_list(os.path.join(output_directory, 'finding_aid_inventory.csv'))
        expected = [['title', 'hierarchical relationship', 'description level', 'publish', 'restrictions', 'start_date', 'end_date',
                    'extent portion', 'extent', 'extent type', 'container instance type', 'top container type'],
                    ['Constituent Mail Export [electronic files]', '1', 'series', 'True', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['Correspondence by Topic [electronic files]', '2', 'file', 'True', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['cats [electronic files]', '3', 'file', 'True', 'BLANK', 'unknown', 'unknown', 'Whole', '0.0001', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['dogs [electronic files]', '3', 'file', 'True', 'BLANK', '2021', '2024', 'Whole', '0.0002', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['farm [electronic files]', '3', 'file', 'True', 'BLANK', 'unknown', 'unknown', 'Whole', '0.0003', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['Correspondence Metadata [electronic files]', '2', 'file', 'True', 'BLANK', 'TBD', 'TBD', 'Whole', 'TBD', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['Form Letters [electronic files]', '2', 'file', 'True', 'BLANK', 'TBD', 'TBD', 'Whole', 'TBD', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['Original Export [electronic files]', '2', 'file', 'True', 'True', 'TBD', 'TBD', 'Whole', 'TBD', 'gigabyte(s)', 'electronic_records', 'electronic_records']]
        self.assertEqual(expected, result, "Problem with test for missing metadata")

    def test_size_differences(self):
        """Testing error handling for if there is no metadata.csv to get the years"""
        # Makes variable needed for input, adds a file to each topic to determine the size, and runs the function.
        output_directory = os.path.join('test_data', 'make_finding_aid_inventory', 'size_differences')
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', '2-decimal'), 500000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', '4-decimal-down'), 2000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', '4-decimal-up'), 11000)
        make_finding_aid_inventory(output_directory)

        # Tests the contents of finding_aid_inventory.csv.
        result = csv_to_list(os.path.join(output_directory, 'finding_aid_inventory.csv'))
        expected = [['title', 'hierarchical relationship', 'description level', 'publish', 'restrictions', 'start_date', 'end_date',
                    'extent portion', 'extent', 'extent type', 'container instance type', 'top container type'],
                    ['Constituent Mail Export [electronic files]', '1', 'series', 'True', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['Correspondence by Topic [electronic files]', '2', 'file', 'True', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['2-decimal [electronic files]', '3', 'file', 'True', 'BLANK', '1999', '1999', 'Whole', '0.026', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['4-decimal-down [electronic files]', '3', 'file', 'True', 'BLANK', '2001', '2003', 'Whole', '0.0001', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['4-decimal-up [electronic files]', '3', 'file', 'True', 'BLANK', '2001', '2003', 'Whole', '0.001', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['Correspondence Metadata [electronic files]', '2', 'file', 'True', 'BLANK', 'TBD', 'TBD', 'Whole', 'TBD', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['Form Letters [electronic files]', '2', 'file', 'True', 'BLANK', 'TBD', 'TBD', 'Whole', 'TBD', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['Original Export [electronic files]', '2', 'file', 'True', 'True', 'TBD', 'TBD', 'Whole', 'TBD', 'gigabyte(s)', 'electronic_records', 'electronic_records']]
        self.assertEqual(expected, result, "Problem with test for size differences")

    def test_year_differences(self):
        """Testing variations related to start and end year (see titles)"""
        # Makes variable needed for input, adds a file to each topic to determine the size, and runs the function.
        output_directory = os.path.join('test_data', 'make_finding_aid_inventory', 'year_differences')
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'blank years'), 10000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'multiple years'), 50000)
        make_doc(os.path.join(output_directory, 'correspondence_by_topic', 'one year'), 70000)
        make_finding_aid_inventory(output_directory)

        # Tests the contents of finding_aid_inventory.csv.
        result = csv_to_list(os.path.join(output_directory, 'finding_aid_inventory.csv'))
        expected = [['title', 'hierarchical relationship', 'description level', 'publish', 'restrictions', 'start_date', 'end_date',
                    'extent portion', 'extent', 'extent type', 'container instance type', 'top container type'],
                    ['Constituent Mail Export [electronic files]', '1', 'series', 'True', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['Correspondence by Topic [electronic files]', '2', 'file', 'True', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['blank years [electronic files]', '3', 'file', 'True', 'BLANK', '2011', '2023', 'Whole', '0.001', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['multiple years [electronic files]', '3', 'file', 'True', 'BLANK', '2001', '2003', 'Whole', '0.003', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['one year [electronic files]', '3', 'file', 'True', 'BLANK', '1999', '1999', 'Whole', '0.004', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['Correspondence Metadata [electronic files]', '2', 'file', 'True', 'BLANK', 'TBD', 'TBD', 'Whole', 'TBD', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['Form Letters [electronic files]', '2', 'file', 'True', 'BLANK', 'TBD', 'TBD', 'Whole', 'TBD', 'gigabyte(s)', 'electronic_records', 'electronic_records'],
                    ['Original Export [electronic files]', '2', 'file', 'True', 'True', 'TBD', 'TBD', 'Whole', 'TBD', 'gigabyte(s)', 'electronic_records', 'electronic_records']]
        self.assertEqual(expected, result, "Problem with test for year differences")


if __name__ == '__main__':
    unittest.main()
