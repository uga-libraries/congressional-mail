from datetime import date
import numpy as np
import os
import pandas as pd
import shutil
import unittest
from cms_data_interchange_format import delete_appraisal_letters
from test_script import csv_to_list, files_in_dir


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes test outputs, if created"""
        # Deletes the copy of the test data for the one test that deletes files.
        copy_path = os.path.join('test_data', 'delete_appraisal_letters', 'delete', 'documents')
        if os.path.exists(copy_path):
            shutil.rmtree(copy_path)

        # Deletes the file deletion log.
        log = f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv"
        log_path = os.path.join('test_data', 'delete_appraisal_letters', log)
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_delete(self):
        """Test for when the file paths in the metadata match files in the export and the files are deleted"""
        # Makes a copy of the test data in the repo, since the script alters the data.
        input_directory = os.path.join('test_data', 'delete_appraisal_letters', 'delete')
        shutil.copytree(os.path.join(input_directory, 'documents_copy'),
                        os.path.join(input_directory, 'documents'))

        # Makes variables needed as function input and runs the function being tested.
        output_directory = os.path.dirname(input_directory)
        appraisal_df = pd.DataFrame([['20241201', 'in-email\\2.txt', 'Casework'],
                                     ['20241202', 'out-custom\\1000.txt', 'Casework'],
                                     ['20241203', 'out-custom\\1001.txt', 'Academy_Application'],
                                     ['20241204', 'out-custom\\1002.txt', 'Casework']],
                                    columns=['date_in', 'correspondence_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [os.path.join(input_directory, 'documents', 'in-email', '2.txt'),
                     '0.1', today, today, 'BFC30C1C407A46A42D322B493E783D8A', 'Casework'],
                    [os.path.join(input_directory, 'documents', 'out-custom', '1000.txt'),
                     '0.1', today, today, '63260766491A2CF2E3DBD1B9C4FFDD53', 'Casework'],
                    [os.path.join(input_directory, 'documents', 'out-custom', '1001.txt'),
                     '0.6', today, today, '6CF993E723D5AD2B841A303056E0535B', 'Academy_Application'],
                    [os.path.join(input_directory, 'documents', 'out-custom', '1002.txt'),
                     '2.8', today, today, '2F48B70AB29E2B466768B6897A1640E2', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for delete, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(os.path.join(input_directory, 'documents'))
        expected = ['1.txt', '3.txt']
        self.assertEqual(expected, result, "Problem with test for delete, directory contents")

    def test_error_filenotfound(self):
        """Test for when the file paths in the metadata do not match files in the export"""
        # Makes variables needed as function input and runs the function being tested.
        input_directory = os.path.join('test_data', 'delete_appraisal_letters', 'error_filenotfound')
        output_directory = os.path.dirname(input_directory)
        appraisal_df = pd.DataFrame([['20241201', 'in-email\\2.txt', 'Casework'],
                                     ['20241202', 'out-custom\\1.txt', 'Academy_Application']],
                                    columns=['date_in', 'correspondence_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [os.path.join(input_directory, 'documents', 'in-email', '2.txt'),
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Cannot delete: FileNotFoundError'],
                    [os.path.join(input_directory, 'documents', 'out-custom', '1.txt'),
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Cannot delete: FileNotFoundError']]
        self.assertEqual(expected, result, "Problem with test for error_filenotfound, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(os.path.join(input_directory, 'documents'))
        expected = ['1.txt']
        self.assertEqual(expected, result, "Problem with test for error_filenotfound, directory contents")

    def test_error_new(self):
        """Test for when the file paths in the metadata are a new pattern"""
        # Makes variables needed as function input and runs the function being tested.
        input_directory = os.path.join('test_data', 'delete_appraisal_letters', 'error_new')
        output_directory = os.path.dirname(input_directory)
        appraisal_df = pd.DataFrame([['20241201', 'new\\1.txt', 'Casework'],
                                     ['20241202', 'new_folder\\1001.txt', 'Academy_Application']],
                                    columns=['date_in', 'correspondence_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    ['new\\1.txt', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                    'Cannot determine file path: new path pattern in metadata'],
                    ['new_folder\\1001.txt', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'Cannot determine file path: new path pattern in metadata']]
        self.assertEqual(expected, result, "Problem with test for error_new, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(os.path.join(input_directory, 'documents'))
        expected = ['1.txt']
        self.assertEqual(expected, result, "Problem with test for error_new, directory contents")

    def test_skip_blank(self):
        """Test for when the file paths in the metadata are blank (nan)"""
        # Makes variables needed as function input and runs the function being tested.
        input_directory = os.path.join('test_data', 'delete_appraisal_letters', 'skip_empty')
        output_directory = os.path.dirname(input_directory)
        appraisal_df = pd.DataFrame([['20241201', np.nan, 'Casework'],
                                     ['20241202', np.nan, 'Academy_Application']],
                                    columns=['date_in', 'correspondence_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes']]
        self.assertEqual(expected, result, "Problem with test for skip_blank, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(os.path.join(input_directory, 'documents'))
        expected = ['1000.txt', '1001.txt']
        self.assertEqual(expected, result, "Problem with test for skip_blank, directory contents")

    def test_skip_empty_string(self):
        """Test for when the file paths in the metadata are empty strings"""
        # Makes variables needed as function input and runs the function being tested.
        input_directory = os.path.join('test_data', 'delete_appraisal_letters', 'skip_empty')
        output_directory = os.path.dirname(input_directory)
        appraisal_df = pd.DataFrame([['20241201', '', 'Casework'],
                                     ['20241202', '', 'Academy_Application']],
                                    columns=['date_in', 'correspondence_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes']]
        self.assertEqual(expected, result, "Problem with test for skip_empty_string, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(os.path.join(input_directory, 'documents'))
        expected = ['1000.txt', '1001.txt']
        self.assertEqual(expected, result, "Problem with test for skip_empty_string, directory contents")

    def test_skip_form(self):
        """Test for when the file paths in the metadata are for form letters (not deleted)"""
        # Makes variables needed as function input and runs the function being tested.
        input_directory = os.path.join('test_data', 'delete_appraisal_letters', 'skip_form')
        output_directory = os.path.dirname(input_directory)
        appraisal_df = pd.DataFrame([['20241201', 'form-attachments\\1.txt', 'Casework'],
                                     ['20241202', 'form-attachments\\2.txt', 'Casework'],
                                     ['20241203', 'forms\\1.txt', 'Academy_Application']],
                                    columns=['date_in', 'correspondence_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_directory, output_directory, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_directory, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes']]
        self.assertEqual(expected, result, "Problem with test for skip_form, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(os.path.join(input_directory, 'documents'))
        expected = ['1.txt', '2.txt', '1.txt']
        self.assertEqual(expected, result, "Problem with test for skip_form, directory contents")


if __name__ == '__main__':
    unittest.main()
