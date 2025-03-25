"""
Tests for the function delete_appraisal_letters(),
which deletes letters received from constituents and individual casework letters sent back by the office
because they are one of the types of letters not retained for appraisal reasons.
To simplify input, the test uses dataframes with only a few of the columns present in a real export.
"""
from datetime import date
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import delete_appraisal_letters
from test_script import csv_to_list, files_in_dir


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the folders and files made by tests, if present."""

        # Delete the copy of test data.
        test_dirs = [os.path.join('test_data', 'delete_appraisal_letters', 'in_document_name'),
                     os.path.join('test_data', 'delete_appraisal_letters', 'out_document_name_blobexport'),
                     os.path.join('test_data', 'delete_appraisal_letters', 'out_document_name_dos')]
        for test_dir in test_dirs:
            if os.path.exists(os.path.join(test_dir, 'Name_Constituent_Mail_Export')):
                shutil.rmtree(os.path.join(test_dir, 'Name_Constituent_Mail_Export'))

        # Delete the file deletion log.
        # Most tests have deletion logs than copies of test data, so test_dirs list is updated.
        log = f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv"
        test_dirs.extend([os.path.join('test_data', 'delete_appraisal_letters', 'error_new'),
                          os.path.join('test_data', 'delete_appraisal_letters', 'filenotfounderror')])
        for test_dir in test_dirs:
            if os.path.exists(os.path.join(test_dir, log)):
                os.remove(os.path.join(test_dir, log))

    def test_in_document_name(self):
        """Test for deleting files in the in_document_name column"""
        # Makes a copy of the test data in the repo, since the script alters the data.
        output_dir = os.path.join('test_data', 'delete_appraisal_letters', 'in_document_name')
        shutil.copytree(os.path.join(output_dir, 'Name_Constituent_Mail_Export_copy'),
                        os.path.join(output_dir, 'Name_Constituent_Mail_Export'))

        # Makes variables needed as function input and runs the function being tested.
        input_dir = os.path.join(output_dir, 'Name_Constituent_Mail_Export')
        appraisal_df = pd.DataFrame([['Anderson', r'..\documents\BlobExport\objects\111111.txt',
                                      r'..\documents\BlobExport\formletters\form_a.txt', 'Academy_Application'],
                                     ['Blue', r'..\documents\BlobExport\objects\222222.txt', '', 'Academy_Application'],
                                     ['Cooper', '', r'..\documents\BlobExport\formletters\test.txt', 'Casework']],
                                    columns=['last', 'in_document_name', 'out_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_dir, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\objects\111111.txt'.replace('..', input_dir),
                     0.2, today, today, '45F12DDF78B657FA2DC1B0A2A0FB3ADD', 'Academy_Application'],
                    [r'..\documents\objects\222222.txt'.replace('..', input_dir),
                     0.7, today, today, '2CAA9E5BD685EFE4C9FCC9473375A86B', 'Academy_Application'],]
        self.assertEqual(result, expected, "Problem with test for in_document_name, file deletion log")

        # Tests the contents of the input_dir, that all files that should be deleted are gone.
        result = files_in_dir(input_dir)
        expected = ['form_a.txt', '333333.txt']
        self.assertEqual(result, expected, "Problem with test for in_document_name, directory contents")

    def test_out_document_name_blobexport(self):
        """Test for deleting files in the out_document_name column, for the path pattern including 'BlobExport'"""
        # Makes a copy of the test data in the repo, since the script alters the data.
        output_dir = os.path.join('test_data', 'delete_appraisal_letters', 'out_document_name_blobexport')
        shutil.copytree(os.path.join(output_dir, 'Name_Constituent_Mail_Export_copy'),
                        os.path.join(output_dir, 'Name_Constituent_Mail_Export'))

        # Makes variables needed as function input and runs the function being tested.
        input_dir = os.path.join(output_dir, 'Name_Constituent_Mail_Export')
        appraisal_df = pd.DataFrame([['Anderson', '', r'..\documents\BlobExport\formletters\form_a.txt', 'Casework'],
                                     ['Dudley', '', r'..\documents\BlobExport\indivletters\400.txt', 'Casework'],
                                     ['Evans', '', r'..\documents\BlobExport\indivletters\500.txt', 'Casework']],
                                    columns=['last', 'in_document_name', 'out_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_dir, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\indivletters\400.txt'.replace('..', input_dir),
                     2.4, today, today, '4CF163BB5919075DD6FEB7FC8D2AF3A8', 'Casework'],
                    [r'..\documents\indivletters\500.txt'.replace('..', input_dir),
                     1.8, today, today, '64ADE70B27A5D7923C5D3805B5671668', 'Casework'], ]
        self.assertEqual(result, expected, "Problem with test for out_document_name blobexport, file deletion log")

        # Tests the contents of the input_dir, that all files that should be deleted are gone.
        result = files_in_dir(input_dir)
        expected = ['form_a.txt', '100.txt']
        self.assertEqual(result, expected, "Problem with test for out_document_name blobexport, directory contents")

    def test_out_document_name_dos(self):
        """Test for deleting files in the out_document_name column, for the path pattern including 'dos'"""
        # Makes a copy of the test data in the repo, since the script alters the data.
        output_dir = os.path.join('test_data', 'delete_appraisal_letters', 'out_document_name_dos')
        shutil.copytree(os.path.join(output_dir, 'Name_Constituent_Mail_Export_copy'),
                        os.path.join(output_dir, 'Name_Constituent_Mail_Export'))

        # Makes variables needed as function input and runs the function being tested.
        input_dir = os.path.join(output_dir, 'Name_Constituent_Mail_Export')
        appraisal_df = pd.DataFrame([['Anderson', '', r'\\office-dc\dos\public\form\form_a.txt', 'Casework'],
                                     ['Blue', '', '', 'Casework'],
                                     ['Dudley', '', r'\\office-dc\dos\public\letter\111111.txt', 'Academy_Application'],
                                     ['Evans', '', r'\\office-atl\dos\public\letter\333333.txt', 'Casework']],
                                    columns=['last', 'in_document_name', 'out_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_dir, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\letter\111111.txt'.replace('..', input_dir),
                     0.2, today, today, '45F12DDF78B657FA2DC1B0A2A0FB3ADD', 'Academy_Application'],
                    [r'..\documents\letter\333333.txt'.replace('..', input_dir),
                     0.7, today, today, '2CAA9E5BD685EFE4C9FCC9473375A86B', 'Casework'], ]
        self.assertEqual(result, expected, "Problem with test for out_document_name dos, file deletion log")

        # Tests the contents of the input_dir, that all files that should be deleted are gone.
        result = files_in_dir(input_dir)
        expected = ['form_a.txt', 'test.txt', '222222.txt']
        self.assertEqual(result, expected, "Problem with test for out_document_name dos, directory contents")

    def test_error_new(self):
        """Test for when paths in the metadata do not match expected patterns"""
        # Makes variables needed as function input and runs the function being tested.
        # Makes variables needed as function input and runs the function being tested.
        output_dir = os.path.join('test_data', 'delete_appraisal_letters', 'error_new')
        input_dir = os.path.join(output_dir, 'Name_Constituent_Mail_Export')
        appraisal_df = pd.DataFrame([['Anderson', r'objects\111111.txt', r'form\test.txt', 'Academy_Application'],
                                     ['Evans', '', r'indivletters\500.txt', 'Casework']],
                                    columns=['last', 'in_document_name', 'out_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_dir, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'objects\111111.txt', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'Cannot determine file path: new path pattern in metadata'],
                    [r'indivletters\500.txt', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'Cannot determine file path: new path pattern in metadata']]
        self.assertEqual(result, expected, "Problem with test for error_new, file deletion log")

    def test_filenotfounderror(self):
        """Test for when files in the metadata are not present and cannot be deleted"""
        # Makes variables needed as function input and runs the function being tested.
        output_dir = os.path.join('test_data', 'delete_appraisal_letters', 'filenotfounderror')
        input_dir = os.path.join(output_dir, 'Name_Constituent_Mail_Export')
        appraisal_df = pd.DataFrame([['Anderson', r'..\documents\BlobExport\objects\111111.txt',
                                      r'..\documents\BlobExport\formletters\test.txt', 'Academy_Application'],
                                     ['Evans', '', r'..\documents\BlobExport\indivletters\500.txt', 'Casework']],
                                    columns=['last', 'in_document_name', 'out_document_name', 'Appraisal_Category'])
        delete_appraisal_letters(input_dir, appraisal_df)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\objects\111111.txt'.replace('..', input_dir),
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\indivletters\500.txt'.replace('..', input_dir),
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Cannot delete: FileNotFoundError']]
        self.assertEqual(result, expected, "Problem with test for filenotfounderror, file deletion log")


if __name__ == '__main__':
    unittest.main()
