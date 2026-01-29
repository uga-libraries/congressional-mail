from datetime import date
import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_data_interchange_format import delete_appraisal_letters
from test_script import csv_to_list, files_in_dir


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes test outputs, if created"""
        # Delete the copy of the test data
        test_dir = os.path.join('test_data', 'delete_appraisal_letters')
        if os.path.exists(os.path.join(test_dir, 'deletion', 'export')):
            shutil.rmtree(os.path.join(test_dir, 'deletion', 'export'))

        # Delete the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        paths = [os.path.join(test_dir, 'deletion', f'file_deletion_log_{today}.csv'),
                 os.path.join(test_dir, 'file_not_found', f'file_deletion_log_{today}.csv'),
                 os.path.join(test_dir, 'new_pattern', f'file_deletion_log_{today}.csv'),
                 os.path.join(test_dir, 'no_deletion_blank', f'file_deletion_log_{today}.csv'),
                 os.path.join(test_dir, 'no_deletion_empty', f'file_deletion_log_{today}.csv'),
                 os.path.join(test_dir, 'no_deletion_form', f'file_deletion_log_{today}.csv')]
        for path in paths:
            if os.path.exists(path):
                os.remove(path)

    def test_deletion(self):
        """Test for when the file paths in the metadata match files in the export and the files are deleted"""
        # Makes a copy of the test data in the repo, since the script alters the data.
        output_directory = os.path.join('test_data', 'delete_appraisal_letters', 'deletion')
        shutil.copytree(os.path.join(output_directory, 'export_copy'),
                        os.path.join(output_directory, 'export'))

        # Makes variables needed as function input and runs the function being tested.
        input_directory = os.path.join(output_directory, 'export')
        appraisal_df = pd.DataFrame([['20241201', '..\\documents\\objects\\100001.txt', 'Casework'],
                                     ['20241202', '..\\documents\\objects\\200002.txt', 'Casework']],
                                    columns=['date_in', 'communication_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [os.path.join(input_directory, 'documents', 'objects', '100001.txt'),
                     '0.0', today, today, 'F270E85FDB08BDB6B7BE83270F077E6B', 'Casework'],
                    [os.path.join(input_directory, 'documents', 'objects', '200002.txt'),
                     '0.0', today, today, 'F270E85FDB08BDB6B7BE83270F077E6B', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for deletion, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = []
        self.assertEqual(expected, result, "Problem with test for deletion, directory contents")

    def test_file_not_found(self):
        """Test for when the file paths in the metadata do not match files in the export"""
        # Makes variables needed as function input and runs the function being tested.
        output_directory = os.path.join('test_data', 'delete_appraisal_letters', 'file_not_found')
        input_directory = os.path.join(output_directory, 'export')
        appraisal_df = pd.DataFrame([['20241201', '..\\documents\\objects\\800000.txt', 'Casework'],
                                     ['20241202', '..\\documents\\objects\\900000.txt', 'Casework']],
                                    columns=['date_in', 'communication_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [os.path.join(input_directory, 'documents', 'objects', '800000.txt'),
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Cannot delete: FileNotFoundError'],
                    [os.path.join(input_directory, 'documents', 'objects', '900000.txt'),
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Cannot delete: FileNotFoundError']]
        self.assertEqual(expected, result, "Problem with test for file not found, file deletion log")

        # Tests that no files have been deleted.
        result = files_in_dir(input_directory)
        expected = ['100001.txt', 'ABC-1.txt']
        self.assertEqual(expected, result, "Problem with test for file not found, directory contents")

    def test_new_pattern(self):
        """Test for when the file paths in the metadata match files in the export but are a new pattern"""
        # Runs the function being tested.
        output_directory = os.path.join('test_data', 'delete_appraisal_letters', 'new_pattern')
        # Makes variables needed as function input and runs the function being tested.
        input_directory = os.path.join(output_directory, 'export')
        appraisal_df = pd.DataFrame([['20241201', '..\\letters\\100001.txt', 'Casework'],
                                     ['20241202', '..\\letters\\200002.txt', 'Casework']],
                                    columns=['date_in', 'communication_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        # Code needs to be updated to not save (or delete after saving) if the report is empty (header only).
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    ['..\\letters\\100001.txt', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'Cannot determine file path: new path pattern in metadata'],
                    ['..\\letters\\200002.txt', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'Cannot determine file path: new path pattern in metadata']]
        self.assertEqual(expected, result, "Problem with test for no deletion - form, file deletion log")

        # Tests that no files have been deleted.
        result = files_in_dir(input_directory)
        expected = ['100001.txt', '200002.txt']
        self.assertEqual(expected, result, "Problem with test for no deletion - form, directory contents")

    def test_no_deletion_blank(self):
        """Test for when the file paths in the metadata are blank (nan)"""
        # Runs the function being tested.
        output_directory = os.path.join('test_data', 'delete_appraisal_letters', 'no_deletion_empty')
        # Makes variables needed as function input and runs the function being tested.
        input_directory = os.path.join(output_directory, 'export')
        appraisal_df = pd.DataFrame([['20241201', np.nan, 'Casework'],
                                     ['20241202', np.nan, 'Casework']],
                                    columns=['date_in', 'communication_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes']]
        self.assertEqual(expected, result, "Problem with test for no deletion - blank, file deletion log")

        # Tests that no files have been deleted.
        result = files_in_dir(input_directory)
        expected = ['ABC-1.txt']
        self.assertEqual(expected, result, "Problem with test for no deletion - blank, directory contents")

    def test_no_deletion_empty_string(self):
        """Test for when the file paths in the metadata are empty strings"""
        # Runs the function being tested.
        output_directory = os.path.join('test_data', 'delete_appraisal_letters', 'no_deletion_empty')
        # Makes variables needed as function input and runs the function being tested.
        input_directory = os.path.join(output_directory, 'export')
        appraisal_df = pd.DataFrame([['20241201', '', 'Casework'],
                                     ['20241202', '', 'Casework']],
                                    columns=['date_in', 'communication_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes']]
        self.assertEqual(expected, result, "Problem with test for no deletion - empty string, file deletion log")

        # Tests that no files have been deleted.
        result = files_in_dir(input_directory)
        expected = ['ABC-1.txt']
        self.assertEqual(expected, result, "Problem with test for no deletion - empty string, directory contents")

    def test_no_deletion_form(self):
        """Test for when the file paths in the metadata match files in the export but are form letters (not deleted)"""
        # Runs the function being tested.
        output_directory = os.path.join('test_data', 'delete_appraisal_letters', 'no_deletion_form')
        # Makes variables needed as function input and runs the function being tested.
        input_directory = os.path.join(output_directory, 'export')
        appraisal_df = pd.DataFrame([['20241201', '..\\documents\\formletters\\100001.txt', 'Casework'],
                                     ['20241202', '..\\documents\\formletters\\200002.txt', 'Casework']],
                                    columns=['date_in', 'communication_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        # Code needs to be updated to not save (or delete after saving) if the report is empty (header only).
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes']]
        self.assertEqual(expected, result, "Problem with test for no deletion - form, file deletion log")

        # Tests that no files have been deleted.
        result = files_in_dir(input_directory)
        expected = ['100001.txt', '200002.txt']
        self.assertEqual(expected, result, "Problem with test for no deletion - form, directory contents")


if __name__ == '__main__':
    unittest.main()
