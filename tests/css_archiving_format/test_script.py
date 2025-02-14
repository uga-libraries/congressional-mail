"""
Tests for the script css_archiving_format.py
"""
from datetime import date
import os
import pandas as pd
import shutil
import subprocess
import unittest


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('nan')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


def files_in_dir(dir_path):
    """Make a list of every file in a directory, for testing the result of the function"""
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_list.append(file)
    return file_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Remove script outputs, if they were made"""
        # Files saved in the parent of input_directory.
        filenames = ['archiving_correspondence_redacted.csv', '2021-2022.csv', '2023-2024.csv', 'case_remains_log.csv',
                     'case_delete_log.csv', f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv"]
        for filename in filenames:
            file_path = os.path.join('test_data', 'script', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Copy of input_directory made for this test.
        folders = ['Access_Constituent_Mail_Export', 'Preservation_Constituent_Mail_Export']
        for folder in folders:
            if os.path.exists(os.path.join('test_data', 'script', folder)):
                shutil.rmtree(os.path.join('test_data', 'script', folder))

    def test_correct_access(self):
        """Test for when the script runs correctly and is in access mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'Access_Constituent_Mail_Export_copy'),
                        os.path.join('test_data', 'script', 'Access_Constituent_Mail_Export'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'Access_Constituent_Mail_Export')
        subprocess.run(f"python {script_path} {input_directory} access", shell=True)

        # Tests the contents of the case delete log.
        csv_path = os.path.join('test_data', 'script', 'case_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Ms.', 'Diane', 'D.', 'Dudly', 'nan', 'nan', 'nan', 'nan', '456 D St', 'nan', 'nan', 'nan',
                     'D city', 'DE', '45678', 'nan', 'd100', 'General', 'Email', '20210101', 'Prison Case',
                     'nan', r'..\documents\BlobExport\objects\444444.txt', 'nan', 'r400', 'General', 'Email',
                     '20210111', 'D', 'nan', r'..\documents\BlobExport\indivletters\000004.txt', 'nan'],
                    ['Ms.', 'Emma', 'E.', 'Evans', 'nan', 'nan', 'nan', 'nan', '567 E St', 'nan', 'nan', 'nan',
                     'E city', 'ME', '56789', 'nan', 'e100', 'General', 'Email', '20210101', 'Casework Issues',
                     'nan', r'..\documents\BlobExport\objects\555555.txt', 'nan', 'r500', 'General', 'Email',
                     '20210111', 'E', 'nan', r'..\documents\BlobExport\indivletters\000005.txt', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, case delete log")

        # Tests that no case remains log was made.
        result = os.path.exists(os.path.join('test_data', 'script', 'case_remains_log.csv'))
        self.assertEqual(result, False, "Problem with test for access, case remains log")

        # Tests the contents of archiving_correspondence_redacted.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_redacted.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'A1', 'nan',
                     r'..\documents\BlobExport\objects\111111.txt', 'nan', 'r100', 'General', 'Email', '20210111',
                     'A', 'nan', r'..\documents\BlobExport\formletters\A', 'nan'],
                    ['B city', 'WY', '23456', 'nan', 'b200', 'General', 'Email', '20230202', 'B1^B2', 'Note',
                     r'..\documents\BlobExport\objects\222222.txt', 'nan', 'r200', 'General', 'Email', '20230212',
                     'B', 'nan', r'..\documents\BlobExport\formletters\B', 'nan'],
                    ['C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'A1', 'nan',
                     r'..\documents\BlobExport\objects\333333.txt', 'nan', 'r300', 'General', 'Email', '20240313',
                     'A', 'nan', r'..\documents\BlobExport\formletters\A', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, archiving_correspondence_redacted.csv")

        # Tests the contents of 2021-2022.csv.
        csv_path = os.path.join('test_data', 'script', '2021-2022.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'A1', 'nan',
                     r'..\documents\BlobExport\objects\111111.txt', 'nan', 'r100', 'General', 'Email', '20210111',
                     'A', 'nan', r'..\documents\BlobExport\formletters\A', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, 2021-2022.csv")

        # Tests the contents of 2023-2024.csv.
        csv_path = os.path.join(os.getcwd(), 'test_data', 'script', '2023-2024.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['B city', 'WY', '23456', 'nan', 'b200', 'General', 'Email', '20230202', 'B1^B2', 'Note',
                     r'..\documents\BlobExport\objects\222222.txt', 'nan', 'r200', 'General', 'Email', '20230212',
                     'B', 'nan', r'..\documents\BlobExport\formletters\B', 'nan'],
                    ['C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'A1', 'nan',
                     r'..\documents\BlobExport\objects\333333.txt', 'nan', 'r300', 'General', 'Email', '20240313',
                     'A', 'nan', r'..\documents\BlobExport\formletters\A', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, 2023-2024.csv")

        # Tests that no undated.csv was made.
        result = os.path.exists(os.path.join(os.getcwd(), 'test_data', 'script', 'undated.csv'))
        self.assertEqual(result, False, "Problem with test for access, undated.csv")

    def test_correct_preservation(self):
        """Test for when the script runs correctly and is in preservation mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'Preservation_Constituent_Mail_Export_copy'),
                        os.path.join('test_data', 'script', 'Preservation_Constituent_Mail_Export'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'Preservation_Constituent_Mail_Export')
        subprocess.run(f"python {script_path} {input_directory} preservation", shell=True)

        # Tests the contents of the case delete log.
        csv_path = os.path.join('test_data', 'script', 'case_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Ms.', 'Diane', 'D.', 'Dudly', 'nan', 'nan', 'nan', 'nan', '456 D St', 'nan', 'nan', 'nan',
                     'D city', 'DE', '45678', 'nan', 'd100', 'General', 'Email', '20210101', 'Prison Case', 'nan',
                     r'..\documents\BlobExport\objects\444444.txt', 'nan', 'r400', 'General', 'Email', '20210111',
                     'D', 'nan', r'..\documents\BlobExport\formletters\D.txt', 'nan'],
                    ['Ms.', 'Emma', 'E.', 'Evans', 'nan', 'nan', 'nan', 'nan', '567 E St', 'nan', 'nan', 'nan',
                     'E city', 'ME', '56789', 'nan', 'e100', 'General', 'Email', '20210101', 'Casework Issues', 'nan',
                     r'..\documents\BlobExport\objects\555555.txt', 'nan', 'r500', 'General', 'Email', '20210111',
                     'E', 'nan', r'..\documents\BlobExport\indivletters\000005.txt', 'nan'],
                    ['Ms.', 'Fiona', 'F.', 'Fowler', 'nan', 'nan', 'nan', 'nan', '678 F St', 'nan', 'nan', 'nan',
                     'F city', 'FL', '67890', 'nan', 'f100', 'General', 'Email', '20210101',
                     'Social Security^Casework', 'nan', 'nan', 'nan', 'r600',
                     'General', 'Email', '20210111', 'F', 'nan', r'..\documents\BlobExport\formletters\F.txt', 'nan'],
                    ['Ms.', 'Ann', 'A.', 'Anderson', 'nan', 'MD', 'nan', 'nan', '123 A St', 'nan', 'nan', 'nan',
                     'A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'A1', 'This is casework',
                     r'..\documents\BlobExport\objects\111111.txt', 'nan', 'r100', 'General', 'Email', '20210111',
                     'nan', 'nan', r'..\documents\BlobExport\indivletters\000001.txt', 'nan'],
                    ['Mr.', 'Clive', 'C.', 'Cooper', 'Jr.', 'nan', 'CEO', 'Company', 'Attn: C', 'Division', 'POBox',
                     '345 C St', 'C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'C1',
                     'Maybe casework', r'..\documents\BlobExport\objects\333333.txt', 'nan', 'r300', 'General',
                     'Email', '20240313', 'C', 'nan', r'..\documents\BlobExport\indivletters\000003.txt', 'nan']]
        self.assertEqual(result, expected, "Problem with test for preservation, case delete log")

        # Tests the contents of the case remains log.
        csv_path = os.path.join('test_data', 'script', 'case_remains_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Ms.', 'Gretel', 'G.', 'Green', 'nan', 'nan', 'nan', 'nan', '789 G St', 'nan', 'nan', 'nan',
                     'G city', 'GA', '78901', 'nan', 'g100', 'General', 'Email', '20210101', 'G1', 'nan',
                     r'..\documents\BlobExport\objects\777777.txt', 'nan', 'r700', 'General', 'Email', '20210111',
                     'nan', 'nan', r'..\documents\BlobExport\indivletters\000007.txt', 'Court case']]
        self.assertEqual(result, expected, "Problem with test for preservation, case remains log")

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        csv_path = os.path.join('test_data', 'script', f"file_deletion_log_{today}.csv")
        result = csv_to_list(csv_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\objects\444444.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\objects\555555.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\objects\111111.txt'.replace('..', input_directory),
                     '0.0', today, today, '49C13D076A41E65DBE137D695E22A6A7', 'casework'],
                    [r'..\documents\objects\333333.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\indivletters\000005.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\indivletters\000001.txt'.replace('..', input_directory),
                     '0.1', today, today, '21E65C7B733959A8B3E6071EB0748BF6', 'casework'],
                    [r'..\documents\indivletters\000003.txt'.replace('..', input_directory),
                    '3.5', today, today, '3E273CCDD4D24DBFCD55B519999BABC7', 'casework']]
        self.assertEqual(result, expected, "Problem with test for preservation, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = ['archiving_correspondence.dat', 'B.txt', 'C.txt', 'D.txt', 'F.txt', '000007.txt',
                    '222222.txt', '666666.txt', '777777.txt']
        self.assertEqual(result, expected, "Problem with test for preservation, input_directory contents")

        # Tests the access script mode outputs were not made.
        output_directory = os.path.join('test_data', 'script')
        result = [os.path.exists(os.path.join(output_directory, 'archiving_correspondence_redacted.csv')),
                  os.path.exists(os.path.join(output_directory, '2021-2022.csv')),
                  os.path.exists(os.path.join(output_directory, '2023-2024.csv'))]
        expected = [False, False, False]
        self.assertEqual(result, expected, "Problem with test for preservation, access script mode outputs")

    def test_error_argument(self):
        """Test for when the script exits due to an argument error."""
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path}", shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script and tests that it prints the correct error.
        output = subprocess.run(f"python {script_path}", shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Missing required arguments, input_directory and script_mode\r\n"
        self.assertEqual(result, expected, "Problem with test for error argument, printed error")


if __name__ == '__main__':
    unittest.main()
