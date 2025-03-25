"""
Tests for the function check_arguments(), which verifies the required arguments are present and valid.
For input, tests use a list with argument values. In production, this would be the contents of sys_argv.
"""
import os
import unittest
from css_archiving_format import check_arguments


class MyTestCase(unittest.TestCase):

    def test_correct_access(self):
        """Test for when both required arguments are present, input_directory path exists, and mode is access."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['css_archiving_format.py', input_dir, 'access']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)
        
        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, input_dir, "Problem with correct - access, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_correspondence.dat'),
                         "Problem with correct - access, metadata_path")
        self.assertEqual(script_mode, 'access', "Problem with correct - access, script_mode")
        self.assertEqual(errors_list, [], "Problem with correct - access, errors_list")

    def test_correct_accession(self):
        """Test for when both required arguments are present, input_directory path exists, and mode is accession."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct_caps')
        sys_argv = ['css_archiving_format.py', input_dir, 'accession']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, input_dir, "Problem with correct - accession, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_CORRESPONDENCE.dat'),
                         "Problem with correct - accession, metadata_path")
        self.assertEqual(script_mode, 'accession', "Problem with correct - accession, script_mode")
        self.assertEqual(errors_list, [], "Problem with correct - accession, errors_list")

    def test_correct_appraisal(self):
        """Test for when both required arguments are present, input_directory path exists, and mode is appraisal."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['css_archiving_format.py', input_dir, 'appraisal']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, input_dir, "Problem with correct - appraisal, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_correspondence.dat'),
                         "Problem with correct - appraisal, metadata_path")
        self.assertEqual(script_mode, 'appraisal', "Problem with correct - appraisal, script_mode")
        self.assertEqual(errors_list, [], "Problem with correct - access, errors_list")

    def test_correct_preservation(self):
        """Test for when both required arguments are present, input_directory path exists, and mode is preservation."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct_caps')
        sys_argv = ['css_archiving_format.py', input_dir, 'preservation']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, input_dir, "Problem with correct - preservation, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_CORRESPONDENCE.dat'),
                         "Problem with correct - preservation, metadata_path")
        self.assertEqual(script_mode, 'preservation', "Problem with correct - preservation, script_mode")
        self.assertEqual(errors_list, [], "Problem with correct - preservation, errors_list")

    def test_error_missing_one(self):
        """Test for when one required argument (mode) is missing."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['css_archiving_format.py', input_dir]
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = []
        self.assertEqual(input_directory, input_dir, "Problem with error - missing one, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_correspondence.dat'),
                         "Problem with error - missing one, metadata_path")
        self.assertEqual(script_mode, None, "Problem with error - missing one, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with error - missing one, errors_list")

    def test_error_missing_two(self):
        """Test for when both required arguments are missing."""
        # Runs the function being tested.
        sys_argv = ['css_archiving_format.py']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = ["Missing required arguments, input_directory and script_mode"]
        self.assertEqual(input_directory, None, "Problem with error - missing two, input_directory")
        self.assertEqual(metadata_path, None, "Problem with error - missing two, metadata_path")
        self.assertEqual(script_mode, None, "Problem with error - missing two, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with error - missing two, errors_list")

    def test_error_x(self):
        """Test for when ."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['css_archiving_format.py', input_dir, 'access']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = []
        self.assertEqual(input_directory, input_dir, "Problem with error - x, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_correspondence.dat'),
                         "Problem with error - x, metadata_path")
        self.assertEqual(script_mode, 'access', "Problem with error - x, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with error-x, errors_list")

    def test_error_x(self):
        """Test for when ."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['css_archiving_format.py', input_dir, 'access']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = []
        self.assertEqual(input_directory, input_dir, "Problem with error - x, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_correspondence.dat'),
                         "Problem with error - x, metadata_path")
        self.assertEqual(script_mode, 'access', "Problem with error - x, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with error-x, errors_list")

    def test_error_x(self):
        """Test for when ."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['css_archiving_format.py', input_dir, 'access']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = []
        self.assertEqual(input_directory, input_dir, "Problem with error - x, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_correspondence.dat'),
                         "Problem with error - x, metadata_path")
        self.assertEqual(script_mode, 'access', "Problem with error - x, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with error-x, errors_list")

    def test_error_x(self):
        """Test for when ."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['css_archiving_format.py', input_dir, 'access']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = []
        self.assertEqual(input_directory, input_dir, "Problem with error - x, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_correspondence.dat'),
                         "Problem with error - x, metadata_path")
        self.assertEqual(script_mode, 'access', "Problem with error - x, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with error-x, errors_list")


if __name__ == '__main__':
    unittest.main()
