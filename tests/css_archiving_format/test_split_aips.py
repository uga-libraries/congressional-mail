"""
Tests for the function split_aip(), which makes a folder for every 10,000 files and starts the metadata.csv
for transforming these folders into AIPs for the preservation system.
"""
import os
import shutil
import unittest
from css_archiving_format import split_aips
from test_script import csv_to_list


def files_in_dir(dir_path):
    """Make a list of the path of every file in a directory, for testing the result of the function"""
    # TODO - update the version in test_script to use path for everything?
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def make_input_folder(folder_path, file_count):
    """Make a folder with the specified name and number of files for test input,
    since the needed number of files is larger than we want to store in a GitHub repo"""
    os.makedirs(folder_path)
    for i in range(1, file_count + 1):
        file_path = os.path.join(folder_path, f'file_{i}.txt')
        with open(file_path, 'w') as file:
            file.write("Test input")


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function input and output"""
        output_directory = os.path.join('test_data', 'split_aips')
        shutil.rmtree(output_directory)

    def test_function(self):
        """Test for initial development"""
        # Makes output directory and input directory with test data and runs the function.
        output_directory = os.path.join(os.getcwd(), 'test_data', 'split_aips')
        os.mkdir(output_directory)

        input_directory = os.path.join(os.getcwd(), 'test_data', 'split_aips', 'export')
        make_input_folder(input_directory, 3)
        make_input_folder(os.path.join(input_directory, 'documents'), 1)
        split_aips(input_directory, output_directory)

        # Tests the aip_dir has the correct contents.
        aip_dir = os.path.join(output_directory, 'aip_dir')
        result = files_in_dir(aip_dir)
        expected = [os.path.join(aip_dir, 'metadata.csv'),
                    os.path.join(aip_dir, 'metadata', 'file_1.txt'),
                    os.path.join(aip_dir, 'metadata', 'file_2.txt'),
                    os.path.join(aip_dir, 'metadata', 'file_3.txt')]
        self.assertEqual(expected, result, "Problem with test for function, aip_dir")

        # Tests the metadata.csv has the correct values.
        result = csv_to_list(os.path.join(aip_dir, 'metadata.csv'))
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'],
                    ['BLANK', 'BLANK', 'metadata', 'BLANK', 'CSS Metadata', 1]]
        self.assertEqual(expected, result, "Problem with test for function, metadata.csv")


if __name__ == '__main__':
    unittest.main()
