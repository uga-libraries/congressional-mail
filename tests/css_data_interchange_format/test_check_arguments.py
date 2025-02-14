"""
Tests for the function get_paths, which gets the paths to all metadata files
in a folder provided as the script argument.
"""
import os
import unittest
from css_data_interchange_format import check_arguments


class MyTestCase(unittest.TestCase):

    def test_correct_access(self):
        """Test for when both required arguments are present, input_directory path exists and
        all metadata files are present, and mode is access."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['cms_data_interchange_format.py', input_dir, 'access']
        input_directory, metadata_paths_dict, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_dict = {'1B': os.path.join(input_dir, 'out_1B.dat'),
                         '2A': os.path.join(input_dir, 'out_2A.dat'),
                         '2C': os.path.join(input_dir, 'out_2C.dat')}
        self.assertEqual(input_directory, input_dir, "Problem with correct - access, input_directory")
        self.assertEqual(metadata_paths_dict, expected_dict, "Problem with correct - access, metadata_paths_dict")
        self.assertEqual(script_mode, 'access', "Problem with correct - access, script_mode")
        self.assertEqual(errors_list, [], "Problem with correct - access, errors_list")

    def test_correct_preservation(self):
        """Test for when both required arguments are present, input_directory path exists and 
        all metadata files are present, and mode is access."""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['cms_data_interchange_format.py', input_dir, 'preservation']
        input_directory, metadata_paths_dict, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_dict = {'1B': os.path.join(input_dir, 'out_1B.dat'),
                         '2A': os.path.join(input_dir, 'out_2A.dat'),
                         '2C': os.path.join(input_dir, 'out_2C.dat')}
        self.assertEqual(input_directory, input_dir, "Problem with correct - preservation, input_directory")
        self.assertEqual(metadata_paths_dict, expected_dict, "Problem with correct - preservation, metadata_paths_dict")
        self.assertEqual(script_mode, 'preservation', "Problem with correct - preservation, script_mode")
        self.assertEqual(errors_list, [], "Problem with correct - preservation, errors_list")

    def test_error_input_directory(self):
        """Test for when the input_directory path does not exist"""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'path_error')
        sys_argv = ['cms_data_interchange_format.py', input_dir, 'access']
        input_directory, metadata_paths_dict, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, None, "Problem with error - input directory, input_directory")
        self.assertEqual(metadata_paths_dict, {}, "Problem with error - input directory, metadata_paths_dict")
        self.assertEqual(script_mode, 'access', "Problem with error - input directory, script_mode")
        self.assertEqual(errors_list, [f"Provided input_directory '{input_dir}' does not exist"],
                         "Problem with error - input directory, errors_list")

    def test_error_script_mode(self):
        """Test for when the script_mode is not one of the expected values"""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['cms_data_interchange_format.py', input_dir, 'mode_error']
        input_directory, metadata_paths_dict, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_dict = {'1B': os.path.join(input_dir, 'out_1B.dat'),
                         '2A': os.path.join(input_dir, 'out_2A.dat'),
                         '2C': os.path.join(input_dir, 'out_2C.dat')}
        self.assertEqual(input_directory, input_dir, "Problem with error - script mode, input_directory")
        self.assertEqual(metadata_paths_dict, expected_dict, "Problem with error - script mode, metadata_paths_dict")
        self.assertEqual(script_mode, None, "Problem with error - script mode, script_mode")
        self.assertEqual(errors_list, ["Provided mode 'mode_error' is not 'access' or 'preservation'"],
                         "Problem with error - script mode, errors_list")

    def test_missing_both_arg(self):
        """Test for when both required arguments are missing"""
        # Runs the function being tested.
        sys_argv = ['cms_data_interchange_format.py']
        input_directory, metadata_paths_dict, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, None, "Problem with missing both arguments, input_directory")
        self.assertEqual(metadata_paths_dict, {}, "Problem with missing both arguments, metadata_paths_dict")
        self.assertEqual(script_mode, None, "Problem with missing both arguments, script_mode")
        self.assertEqual(errors_list, ["Missing required arguments, input_directory and script_mode"],
                         "Problem with missing both arguments, errors_list")

    def test_missing_metadata(self):
        """Test for when no metadata files are in the input_directory"""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments')
        sys_argv = ['cms_data_interchange_format.py', input_dir, 'access']
        input_directory, metadata_paths_dict, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, input_dir, "Problem with missing metadata, input_directory")
        self.assertEqual(metadata_paths_dict, {}, "Problem with missing metadata, metadata_paths_dict")
        self.assertEqual(script_mode, 'access', "Problem with missing metadata, script_mode")
        self.assertEqual(errors_list, ['Metadata file out_1B.dat is not in the input_directory',
                                       'Metadata file out_2A.dat is not in the input_directory',
                                       'Metadata file out_2C.dat is not in the input_directory'],
                         "Problem with missing metadata, errors_list")

    def test_missing_metadata_some(self):
        """Test for when some metadata files are in the input_directory"""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'missing_metadata')
        sys_argv = ['cms_data_interchange_format.py', input_dir, 'access']
        input_directory, metadata_paths_dict, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_dict = {'2A': os.path.join(input_dir, 'out_2A.dat')}
        self.assertEqual(input_directory, input_dir, "Problem with missing metadata - some, input_directory")
        self.assertEqual(metadata_paths_dict, expected_dict,
                         "Problem with missing metadata - some, metadata_paths_dict")
        self.assertEqual(script_mode, 'access', "Problem with missing metadata - some, script_mode")
        self.assertEqual(errors_list, ['Metadata file out_1B.dat is not in the input_directory',
                                       'Metadata file out_2C.dat is not in the input_directory'],
                         "Problem with missing metadata - some, errors_list")

    def test_missing_one_arg(self):
        """Test for when one required argument (script_mode) is missing"""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'correct')
        sys_argv = ['cms_data_interchange_format.py', input_dir]
        input_directory, metadata_paths_dict, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        expected_dict = {'1B': os.path.join(input_dir, 'out_1B.dat'),
                         '2A': os.path.join(input_dir, 'out_2A.dat'),
                         '2C': os.path.join(input_dir, 'out_2C.dat')}
        self.assertEqual(input_directory, input_dir, "Problem with missing one argument, input_directory")
        self.assertEqual(metadata_paths_dict, expected_dict, "Problem with missing one argument, metadata_paths_dict")
        self.assertEqual(script_mode, None, "Problem with missing one argument, script_mode")
        self.assertEqual(errors_list, ["Missing one of the required arguments, input_directory or script_mode"],
                         "Problem with missing one argument, errors_list")

    def test_too_many_arg(self):
        """Test for when too many arguments are provided, with none being expected values"""
        # Runs the function being tested.
        input_dir = os.path.join('test_data', 'check_arguments', 'path_error')
        sys_argv = ['cms_data_interchange_format.py', input_dir, 'mode_error', 'extra_error']
        input_directory, metadata_paths_dict, script_mode, errors_list = check_arguments(sys_argv)

        # Tests the value of each of the four variables returned by the function
        self.assertEqual(input_directory, None, "Problem with too many arguments, input_directory")
        self.assertEqual(metadata_paths_dict, {}, "Problem with too many arguments, metadata_paths_dict")
        self.assertEqual(script_mode, None, "Problem with too many arguments, script_mode")
        self.assertEqual(errors_list, [f"Provided input_directory '{input_dir}' does not exist",
                                       "Provided mode 'mode_error' is not 'access' or 'preservation'",
                                       "Provided more than the required arguments, input_directory and script_mode"],
                         "Problem with too many arguments, errors_list")


if __name__ == '__main__':
    unittest.main()
