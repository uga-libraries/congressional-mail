"""
Tests for the function remove_casework_letters(), which removes letters received or sent that pertain to casework.
"""
from datetime import date
import os
import shutil
import unittest
from css_archiving_format import remove_casework_letters
from test_script import csv_to_list, files_in_dir


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        output_dir = os.path.join('test_data', 'remove_casework_letters', 'correct')

        if os.path.exists(os.path.join(output_dir, 'css_export')):
            shutil.rmtree(os.path.join(output_dir, 'css_export'))

        today = date.today().strftime('%Y-%m-%d')
        if os.path.exists(os.path.join(output_dir, f'file_deletion_log_{today}.csv')):
            os.remove(os.path.join(output_dir, f'file_deletion_log_{today}.csv'))

        if os.path.exists(os.path.join('test_data', 'remove_casework_letters', 'path_error', f'file_deletion_log_{today}.csv')):
            os.remove(os.path.join('test_data', 'remove_casework_letters', 'path_error', f'file_deletion_log_{today}.csv'))

    def test_function(self):
        """Initial test for the development of the function"""
        # Makes a copy of the test data in the repo, since the script alters the data.
        output_dir = os.path.join('test_data', 'remove_casework_letters', 'correct')
        shutil.copytree(os.path.join(output_dir, 'css_export_copy'),
                        os.path.join(output_dir, 'css_export'))

        # Runs the function being tested.
        input_directory = os.path.join(output_dir, 'css_export')
        remove_casework_letters(input_directory)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\BlobExport\objects\111111.txt'.replace('..', input_directory),
                     '0.2', today, today, '45F12DDF78B657FA2DC1B0A2A0FB3ADD', 'casework'],
                    [r'..\documents\BlobExport\objects\222222.txt'.replace('..', input_directory),
                     '0.7', today, today, '2CAA9E5BD685EFE4C9FCC9473375A86B', 'casework'],
                    [r'..\documents\BlobExport\objects\333333.txt'.replace('..', input_directory),
                     '5.3', today, today, 'B98DDA428D28A598F8820EAA6AB515B6', 'casework'],
                    [r'..\documents\BlobExport\indivletters\400.txt'.replace('..', input_directory),
                     '2.4', today, today, '4CF163BB5919075DD6FEB7FC8D2AF3A8', 'casework'],
                    [r'..\documents\BlobExport\indivletters\500.txt'.replace('..', input_directory),
                     '1.8', today, today, '64ADE70B27A5D7923C5D3805B5671668', 'casework']]
        self.assertEqual(result, expected, "Problem with test for file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = ['form_a.txt', 'test.txt', '100.txt']
        self.assertEqual(result, expected, "Problem with test for directory contents")

    def test_path_error(self):
        """Initial test for the development of the function, FileNotFoundError"""
        # Runs the function being tested.
        output_dir = os.path.join('test_data', 'remove_casework_letters', 'path_error')
        input_directory = os.path.join(output_dir, 'css_export')
        remove_casework_letters(input_directory)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\BlobExport\objects\111111.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\BlobExport\objects\222222.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\BlobExport\objects\333333.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\BlobExport\indivletters\400.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\BlobExport\indivletters\500.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError']]
        self.assertEqual(result, expected, "Problem with test for file deletion log")


if __name__ == '__main__':
    unittest.main()
