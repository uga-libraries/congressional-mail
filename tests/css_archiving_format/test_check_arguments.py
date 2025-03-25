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

    def test_error_mode(self):
        """Test for when the mode argument is not an expected value."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['css_archiving_format.py', input_dir, 'unexpected']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = ["Provided mode 'unexpected' is not one of the expected modes"]
        self.assertEqual(input_directory, input_dir, "Problem with error - mode, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_correspondence.dat'),
                         "Problem with error - mode, metadata_path")
        self.assertEqual(script_mode, None, "Problem with error - mode, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with error - mode, errors_list")

    def test_error_path_dat(self):
        """Test for when input_directory contains no archiving correspondence dat file."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'no_dat')
        sys_argv = ['css_archiving_format.py', input_dir, 'access']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = ["No archiving_correspondence.dat file in the input_directory"]
        self.assertEqual(input_directory, input_dir, "Problem with error - path dat, input_directory")
        self.assertEqual(metadata_path, None, "Problem with error - path dat, metadata_path")
        self.assertEqual(script_mode, 'access', "Problem with error - path dat, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with error - path dat, errors_list")

    def test_error_path_invalid(self):
        """Test for when input_directory is a path that does not exist."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'error')
        sys_argv = ['css_archiving_format.py', input_dir, 'access']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = [f"Provided input_directory '{input_dir}' does not exist"]
        self.assertEqual(input_directory, None, "Problem with error - path invalid, input_directory")
        self.assertEqual(metadata_path, None, "Problem with error - path invalid, metadata_path")
        self.assertEqual(script_mode, 'access', "Problem with error - path invalid, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with error - path invalid, errors_list")

    def test_error_too_many_arg(self):
        """Test for when more than the required two arguments are provided."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['css_archiving_format.py', input_dir, 'access', 'extra', 'extra2']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = ["Provided more than the required arguments, input_directory and script_mode"]
        self.assertEqual(input_directory, input_dir, "Problem with error - too many arg, input_directory")
        self.assertEqual(metadata_path, os.path.join(input_dir, 'archiving_correspondence.dat'),
                         "Problem with error - too many arg, metadata_path")
        self.assertEqual(script_mode, 'access', "Problem with error - too many arg, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with error - too many arg, errors_list")

    def test_errors(self):
        """Test for multiple errors."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'missing')
        sys_argv = ['css_archiving_format.py', input_dir, 'error', 'bonus']
        input_directory, metadata_path, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_errors = [f"Provided input_directory '{input_dir}' does not exist",
                           "Provided mode 'error' is not one of the expected modes",
                           "Provided more than the required arguments, input_directory and script_mode"]
        self.assertEqual(input_directory, None, "Problem with errors, input_directory")
        self.assertEqual(metadata_path, None, "Problem with errors, metadata_path")
        self.assertEqual(script_mode, None, "Problem with errors, script_mode")
        self.assertEqual(errors_list, expected_errors, "Problem with errors, errors_list")


if __name__ == '__main__':
    unittest.main()
