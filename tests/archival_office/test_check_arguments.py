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

    def test_error_input_directory(self):
        """Test for when the input_directory path does not exist"""
        # Runs the function being tested.
        sys_argv = ['archival_office_correspondence_data.py', 'path_error', 'access']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, None, "Problem with error input directory, input_directory")
        self.assertEqual(metadata_path, None, "Problem with error input directory, metadata_path")
        self.assertEqual(script_mode, 'access', "Problem with error input directory, script_mode")
        self.assertEqual(errors_list, ["Provided input_directory 'path_error' does not exist"],
                         "Problem with error input directory, errors_list")

    def test_error_script_mode(self):
        """Test for when the script_mode is not one of the expected values"""

        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['archival_office_correspondence_data.py', input_dir, 'mode_error']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, input_dir, "Problem with error script mode, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archive.dat'),
                         "Problem with error script mode, metadata_path")
        self.assertEqual(script_mode, None, "Problem with error script mode, script_mode")
        self.assertEqual(errors_list, ["Provided mode 'mode_error' is not 'access' or 'preservation'"],
                         "Problem with error script mode, errors_list")

    def test_missing_both(self):
        """Test for when both required arguments are missing"""
        # Runs the function being tested.
        sys_argv = ['archival_office_correspondence_data.py']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, None, "Problem with missing both, input_directory")
        self.assertEqual(metadata_path, None, "Problem with missing both, metadata_path")
        self.assertEqual(script_mode, None, "Problem with missing both, script_mode")
        self.assertEqual(errors_list, ['Missing required arguments, input_directory and script_mode'],
                         "Problem with missing both, errors_list")

    def test_missing_metadata(self):
        """Test for when the archive.dat file is not in the input_directory"""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'no_metadata')
        sys_argv = ['archival_office_correspondence_data.py', input_dir]
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, input_dir, "Problem with missing metadata, input_directory")
        self.assertEqual(metadata_path, None, "Problem with missing metadata, metadata_path")
        self.assertEqual(script_mode, None, "Problem with missing metadata, script_mode")
        self.assertEqual(errors_list, ['No archive.dat file in the input_directory'],
                         "Problem with missing metadata, errors_list")

    def test_too_many(self):
        """Test for when too many arguments are provided, with none being expected values"""
        # Runs the function being tested.
        sys_argv = ['archival_office_correspondence_data.py', 'path_error', 'mode_error', 'extra_error']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, None, "Problem with too many, input_directory")
        self.assertEqual(metadata_path, None, "Problem with too many, metadata_path")
        self.assertEqual(script_mode, None, "Problem with too many, script_mode")
        self.assertEqual(errors_list, ["Provided input_directory 'path_error' does not exist",
                                       "Provided mode 'mode_error' is not 'access' or 'preservation'",
                                       "Provided more than the required arguments, input_directory and script_mode"],
                         "Problem with too many, errors_list")


if __name__ == '__main__':
    unittest.main()
