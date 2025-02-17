"""
Tests for the function delete_appraisal_letters(),
which deletes letters received from constituents and individual casework letters sent back by the office
because they are one of the types of letters not retained for appraisal reasons
"""
from datetime import date
import os
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
        test_dirs.extend([os.path.join('test_data', 'delete_appraisal_letters', 'filenotfounderror')])
        for test_dir in test_dirs:
            if os.path.exists(os.path.join(test_dir, log)):
                os.remove(os.path.join(test_dir, log))

    def test_in_document_name(self):
        """Test for deleting files in the in_document_name column"""
        # Makes a copy of the test data in the repo, since the script alters the data.
        output_dir = os.path.join('test_data', 'delete_appraisal_letters', 'in_document_name')
        shutil.copytree(os.path.join(output_dir, 'Name_Constituent_Mail_Export_copy'),
                        os.path.join(output_dir, 'Name_Constituent_Mail_Export'))

        # Runs the function being tested.
        input_dir = os.path.join(output_dir, 'Name_Constituent_Mail_Export')
        delete_appraisal_letters(input_dir)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\objects\111111.txt'.replace('..', input_dir),
                     '0.2', today, today, '45F12DDF78B657FA2DC1B0A2A0FB3ADD', 'casework'],
                    [r'..\documents\objects\222222.txt'.replace('..', input_dir),
                     '0.7', today, today, '2CAA9E5BD685EFE4C9FCC9473375A86B', 'casework'],]
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

        # Runs the function being tested.
        input_dir = os.path.join(output_dir, 'Name_Constituent_Mail_Export')
        delete_appraisal_letters(input_dir)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\indivletters\400.txt'.replace('..', input_dir),
                     '2.4', today, today, '4CF163BB5919075DD6FEB7FC8D2AF3A8', 'casework'],
                    [r'..\documents\indivletters\500.txt'.replace('..', input_dir),
                     '1.8', today, today, '64ADE70B27A5D7923C5D3805B5671668', 'casework'], ]
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

        # Runs the function being tested.
        input_dir = os.path.join(output_dir, 'Name_Constituent_Mail_Export')
        delete_appraisal_letters(input_dir)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\letter\111111.txt'.replace('..', input_dir),
                     '0.2', today, today, '45F12DDF78B657FA2DC1B0A2A0FB3ADD', 'casework'],
                    [r'..\documents\letter\333333.txt'.replace('..', input_dir),
                     '0.7', today, today, '2CAA9E5BD685EFE4C9FCC9473375A86B', 'casework'], ]
        self.assertEqual(result, expected, "Problem with test for out_document_name dos, file deletion log")

        # Tests the contents of the input_dir, that all files that should be deleted are gone.
        result = files_in_dir(input_dir)
        expected = ['form_a.txt', 'test.txt', '222222.txt']
        self.assertEqual(result, expected, "Problem with test for out_document_name dos, directory contents")

    def test_filenotfounderror(self):
        """Test for when files in the metadata are not present and cannot be deleted"""
        # Runs the function being tested.
        output_dir = os.path.join('test_data', 'delete_appraisal_letters', 'filenotfounderror')
        input_dir = os.path.join(output_dir, 'Name_Constituent_Mail_Export')
        delete_appraisal_letters(input_dir)

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join(output_dir, f'file_deletion_log_{today}.csv')
        result = csv_to_list(log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\objects\111111.txt'.replace('..', input_dir),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\indivletters\500.txt'.replace('..', input_dir),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError']]
        self.assertEqual(result, expected, "Problem with test for file deletion log")


if __name__ == '__main__':
    unittest.main()
