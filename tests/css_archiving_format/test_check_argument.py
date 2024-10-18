"""
Tests for the function check_argument(), which verifies the required argument is present and a valid path.
For input, tests use a list with argument values. In production, this would be the contents of sys.argv.
"""
import os
import unittest
from css_archiving_format import check_argument


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the required argument is present and the path exists."""
        # Runs the function being tested.
        md_path, error_message = check_argument(['css_archiving_format.py', os.path.join('test_data', 'check_arg_md.dat')])

        # Tests the value of md_path.
        expected = os.path.join('test_data', 'check_arg_md.dat')
        self.assertEqual(md_path, expected, "Problem with correct, md_path")

        # Tests the value of error_message.
        self.assertEqual(error_message, None, "Problem with correct, error_message")

    def test_missing(self):
        """Test for when the required argument is missing."""
        # Runs the function being tested.
        md_path, error_message = check_argument(['css_archiving_format.py'])

        # Tests the value of md_path.
        self.assertEqual(md_path, None, "Problem with missing, md_path")

        # Tests the value of error_message.
        expected = "Missing required argument: path to the metadata file"
        self.assertEqual(error_message, expected, "Problem with missing, error_message")

    def test_path_error(self):
        """Test for when the required argument is a path that does not exist."""
        # Runs the function being tested.
        md_path, error_message = check_argument(['css_archiving_format.py', os.path.join('error', 'file.dat')])

        # Tests the value of md_path.
        self.assertEqual(md_path, None, "Problem with path error, md_path")

        # Tests the value of error_message.
        expected = f"Provided path does not exist: {os.path.join('error', 'file.dat')}"
        self.assertEqual(error_message, expected, "Problem with path error, error_message")


if __name__ == '__main__':
    unittest.main()
