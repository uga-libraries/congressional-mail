"""
Tests for the function check_arguments(), which verifies the required arguments are present and valid.
For input, tests use a list with argument values. In production, this would be the contents of sys_argv.
"""
import os
import unittest
from archival_office_correspondence_data import check_arguments


class MyTestCase(unittest.TestCase):

    def test_correct_access(self):
        """Test for when both required arguments are present, input_directory path exists, and mode is access."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['archival_office_correspondence_data.py', input_dir, 'access']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, input_dir, "Problem with correct - access, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archive.dat'),
                         "Problem with correct - access, metadata_path")
        self.assertEqual(script_mode, 'access', "Problem with correct - access, script_mode")
        self.assertEqual(errors_list, [], "Problem with correct - access, errors_list")

    def test_correct_preservation(self):
        """Test for when both required arguments are present, input_directory path exists, and mode is preservation."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['archival_office_correspondence_data.py', input_dir, 'preservation']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, input_dir, "Problem with correct - preservation, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archive.dat'),
                         "Problem with correct - preservation, metadata_path")
        self.assertEqual(script_mode, 'preservation', "Problem with correct - preservation, script_mode")
        self.assertEqual(errors_list, [], "Problem with correct - preservation, errors_list")


if __name__ == '__main__':
    unittest.main()
