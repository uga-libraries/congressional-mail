"""
Tests for the function remove_casework_letters(), which removes letters that pertain to casework.
"""
from datetime import date
import os
import shutil
import unittest
from css_data_interchange_format import remove_casework_letters
from test_script import csv_to_list, files_in_dir


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes test outputs, if created"""
        test_dir = os.path.join('test_data', 'remove_casework_letters')

        if os.path.exists(os.path.join(test_dir, 'deletion', 'export')):
            shutil.rmtree(os.path.join(test_dir, 'deletion', 'export'))

        today = date.today().strftime('%Y-%m-%d')
        paths = [os.path.join(test_dir, 'deletion', f'file_deletion_log_{today}.csv'),
                 os.path.join(test_dir, 'file_not_found', f'file_deletion_log_{today}.csv'),
                 os.path.join(test_dir, 'no_deletion_form', f'file_deletion_log_{today}.csv')]
        for path in paths:
            if os.path.exists(path):
                os.remove(path)

    def test_deletion(self):
        """Test for when the files in the metadata deletion log are present in the export and deleted"""
        # Makes a copy of the test data in the repo, since the script alters the data.
        output_dir = os.path.join('test_data', 'remove_casework_letters', 'deletion')
        shutil.copytree(os.path.join(output_dir, 'export_copy'),
                        os.path.join(output_dir, 'export'))

        # Runs the function being tested.
        input_directory = os.path.join(output_dir, 'export')
        remove_casework_letters(input_directory)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [os.path.join(input_directory, 'documents', 'objects', '100001.txt'),
                     '0.0', today, today, 'F270E85FDB08BDB6B7BE83270F077E6B', 'casework'],
                    [os.path.join(input_directory, 'documents', 'objects', '200002.txt'),
                     '0.0', today, today, 'F270E85FDB08BDB6B7BE83270F077E6B', 'casework']]
        self.assertEqual(result, expected, "Problem with test for deletion, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = []
        self.assertEqual(result, expected, "Problem with test for deletion, directory contents")

    def test_file_not_found(self):
        """Test for when the files in the metadata deletion log are not present in the export"""
        # Runs the function being tested.
        output_dir = os.path.join('test_data', 'remove_casework_letters', 'file_not_found')
        input_directory = os.path.join(output_dir, 'export')
        remove_casework_letters(input_directory)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [os.path.join(input_directory, 'documents', 'objects', '800000.txt'),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [os.path.join(input_directory, 'documents', 'objects', '900000.txt'),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError']]
        self.assertEqual(result, expected, "Problem with test for file not found, file deletion log")

        # Tests that no files have been deleted.
        result = files_in_dir(input_directory)
        expected = ['100001.txt', 'ABC-1.txt']
        self.assertEqual(result, expected, "Problem with test for file not found, directory contents")

    def test_no_deletion_blank(self):
        """Test for when there is a metadata deletion log but no rows have an associated file"""
        # Runs the function being tested.
        output_dir = os.path.join('test_data', 'remove_casework_letters', 'no_deletion_blank')
        input_directory = os.path.join(output_dir, 'export')
        remove_casework_letters(input_directory)

        # Tests the file deletion log was not made.
        result = os.path.exists(os.path.join(output_dir, f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        self.assertEqual(result, False, "Problem with test for no deletion - blank, file deletion log")

        # Tests that no files have been deleted.
        result = files_in_dir(input_directory)
        expected = ['ABC-1.txt']
        self.assertEqual(result, expected, "Problem with test for no deletion - blank, directory contents")

    def test_no_deletion_form(self):
        """Test for when there is a metadata deletion log but the associated files are form letters"""
        # Runs the function being tested.
        output_dir = os.path.join('test_data', 'remove_casework_letters', 'no_deletion_form')
        input_directory = os.path.join(output_dir, 'export')
        remove_casework_letters(input_directory)

        # Tests the contents of the file deletion log.
        # Code needs to be updated to not save (or delete after saving) if the report is empty (header only).
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes']]
        self.assertEqual(result, expected, "Problem with test for no deletion - form, file deletion log")

        # Tests that no files have been deleted.
        result = files_in_dir(input_directory)
        expected = ['100001.txt', '200002.txt']
        self.assertEqual(result, expected, "Problem with test for no deletion - form, directory contents")

    def test_no_log(self):
        """Test for when there is no metadata deletion log"""
        # Runs the function being tested.
        output_dir = os.path.join('test_data', 'remove_casework_letters', 'no_log')
        input_directory = os.path.join(output_dir, 'export')
        remove_casework_letters(input_directory)

        # Tests the file deletion log was not made.
        result = os.path.exists(os.path.join(output_dir, f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        self.assertEqual(result, False, "Problem with test for no log, file deletion log")

        # Tests that no files have been deleted.
        result = files_in_dir(input_directory)
        expected = ['ABC-1.txt']
        self.assertEqual(result, expected, "Problem with test for no log, directory contents")


if __name__ == '__main__':
    unittest.main()
