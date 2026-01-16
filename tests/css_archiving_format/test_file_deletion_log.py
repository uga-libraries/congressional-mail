"""
Tests for the function file_deletion_log(),
which makes or updates the file deletion log, so data is saved as soon as a file is deleted.
"""
from datetime import date
import os
import unittest
from css_archiving_format import file_deletion_log
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the log, if made by the tests"""
        log_path = os.path.join('test_data', 'file_deletion_log', 'file_deletion_log_2025-02-15.csv')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_delete_two(self):
        """Test for adding two rows for files that can be deleted."""
        # Makes variables needed as function input.
        log_path = os.path.join(os.getcwd(), 'test_data', 'file_deletion_log', 'file_deletion_log_2025-02-15.csv')
        file_path_1 = os.path.join(os.getcwd(), 'test_data', 'file_deletion_log', 'to-delete-1.txt')
        file_path_2 = os.path.join(os.getcwd(), 'test_data', 'file_deletion_log', 'to-delete-2.txt')

        # Makes the log with a header.
        file_deletion_log(log_path, None, 'header')

        # Adds the first file for testing.
        file_deletion_log(log_path, file_path_1, 'Academy_Application')

        # Adds the second file for testing.
        file_deletion_log(log_path, file_path_2, 'Casework')

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [file_path_1, '0.0', '2025-04-07', today, '89D31DC38A6C7D68653F452A2F44AC3D', 'Academy_Application'],
                    [file_path_2, '1.2', '2025-04-07', today, '9452DF84756C849AE0ED9FE2A14948F5', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for delete two")

    def test_error_new(self):
        """Test for adding a row for a file with a new path format in the metadata."""
        # Makes variables needed as function input.
        log_path = os.path.join(os.getcwd(), 'test_data', 'file_deletion_log', 'file_deletion_log_2025-02-15.csv')
        file_path = os.path.join('new', 'pattern', 'to-delete.txt')

        # Makes the log with a header.
        file_deletion_log(log_path, None, 'header')

        # Adds the row for testing.
        file_deletion_log(log_path, file_path, 'Cannot determine file path: new path pattern in metadata')

        # Tests the contents of the file deletion log.
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [file_path, 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'Cannot determine file path: new path pattern in metadata']]
        self.assertEqual(expected, result, "Problem with test for error_new")

    def test_filenotfounderror(self):
        """Test for adding a row for a file that cannot be deleted."""
        # Makes variables needed as function input.
        log_path = os.path.join(os.getcwd(), 'test_data', 'file_deletion_log', 'file_deletion_log_2025-02-15.csv')
        file_path = os.path.join(os.getcwd(), 'test_data', 'file_deletion_log', 'to-delete-0.txt')

        # Makes the log with a header.
        file_deletion_log(log_path, None, 'header')

        # Adds the row for testing.
        file_deletion_log(log_path, file_path, 'Cannot delete: FileNotFoundError')

        # Tests the contents of the file deletion log.
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [file_path, 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Cannot delete: FileNotFoundError']]
        self.assertEqual(expected, result, "Problem with test for filenotfounderror")

    def test_header(self):
        """Test for making a new log with a header row."""
        # Makes variables needed as function input and runs the function being tested.
        log_path = os.path.join(os.getcwd(), 'test_data', 'file_deletion_log', 'file_deletion_log_2025-02-15.csv')
        file_deletion_log(log_path, None, 'header')

        # Tests the contents of the file deletion log.
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes']]
        self.assertEqual(expected, result, "Problem with test for header")


if __name__ == '__main__':
    unittest.main()
