"""
Tests for the function get_paths, which gets the paths to all metadata files
in a folder provided as the script argument.
"""
import os
import unittest
from cms_data_interchange_format import get_paths


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when all metadata files are in the provided folder"""
        # Runs the function being tested.
        paths, errors_list = get_paths(['cms_data_interchange_format.py',
                                        os.path.join('test_data', 'get_paths_correct')])

        # Tests the value of paths
        expected = {'1B': os.path.join('test_data', 'get_paths_correct', '1B.out'),
                    '2A': os.path.join('test_data', 'get_paths_correct', '2A.out'),
                    '2B': os.path.join('test_data', 'get_paths_correct', '2B.out'),
                    '2C': os.path.join('test_data', 'get_paths_correct', '2C.out')}
        self.assertEqual(paths, expected, "Problem with test for correct, paths")

        # Tests the value of errors_list
        expected = []
        self.assertEqual(errors_list, expected, "Problem with test for correct, errors_list")

    def test_invalid_argument(self):
        """Test for when the metadata folder argument is a path that does not exist"""
        # Runs the function being tested.
        paths, errors_list = get_paths(['cms_data_interchange_format.py',
                                        os.path.join('test_data', 'get_paths_error')])

        # Tests the value of paths
        expected = {}
        self.assertEqual(paths, expected, "Problem with test for invalid argument, paths")

        # Tests the value of errors_list
        expected = [f"Provided path to metadata folder does not exist: {os.path.join('test_data', 'get_paths_error')}"]
        self.assertEqual(errors_list, expected, "Problem with test for invalid argument, errors_list")

    def test_no_argument(self):
        """Test for when the metadata folder argument is missing"""
        # Runs the function being tested.
        paths, errors_list = get_paths(['cms_data_interchange_format.py'])

        # Tests the value of paths
        expected = {}
        self.assertEqual(paths, expected, "Problem with test for no argument, paths")

        # Tests the value of errors_list
        expected = ['Missing required argument: path to the metadata folder']
        self.assertEqual(errors_list, expected, "Problem with test for no argument, errors_list")

    def test_no_metadata(self):
        """Test for when the metadata folder does not contain any of the required metadata files"""
        # Runs the function being tested.
        paths, errors_list = get_paths(['cms_data_interchange_format.py',
                                        os.path.join('test_data', 'get_paths_missing')])

        # Tests the value of paths
        expected = {}
        self.assertEqual(paths, expected, "Problem with test for no metadata, paths")

        # Tests the value of errors_list
        expected = ['Metadata file 1B.out is not in the metadata folder',
                    'Metadata file 2A.out is not in the metadata folder',
                    'Metadata file 2B.out is not in the metadata folder',
                    'Metadata file 2C.out is not in the metadata folder']
        self.assertEqual(errors_list, expected, "Problem with test for no metadata, errors_list")

    def test_some_metadata(self):
        """Test for when the metadata folder does not contain all of the required metadata files"""
        # Runs the function being tested.
        paths, errors_list = get_paths(['cms_data_interchange_format.py',
                                        os.path.join('test_data', 'get_paths_missing_some')])

        # Tests the value of paths
        expected = {'2A': os.path.join('test_data', 'get_paths_missing_some', '2A.out'),
                    '2C': os.path.join('test_data', 'get_paths_missing_some', '2C.out')}
        self.assertEqual(paths, expected, "Problem with test for no metadata, paths")

        # Tests the value of errors_list
        expected = ['Metadata file 1B.out is not in the metadata folder',
                    'Metadata file 2B.out is not in the metadata folder']
        self.assertEqual(errors_list, expected, "Problem with test for no metadata, errors_list")


if __name__ == '__main__':
    unittest.main()
