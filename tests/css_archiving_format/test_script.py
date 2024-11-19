"""
Tests for the script css_archiving_format.py
"""
import os
import pandas as pd
import shutil
import subprocess
import unittest


def csv_to_list(csv_path, delimiter=','):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path, delimiter=delimiter, dtype=str)
    df = df.fillna('nan')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Remove script outputs, if they were made"""
        filenames = ['Access_Copy.csv', '2021-2022.csv', '2023-2024.csv', 'deletion_log.csv', 'row_includes_case_log.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', 'script', filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        if os.path.exists(os.path.join('test_data', 'script', 'preservation_test')):
            shutil.rmtree(os.path.join('test_data', 'script', 'preservation_test'))

    def test_correct_access(self):
        """Test for when the script runs correctly and is in access mode."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'access_test')
        subprocess.run(f"python {script_path} {input_directory} access", shell=True)

        # Tests the contents of Access_Copy.csv.
        csv_path = os.path.join('test_data', 'script', 'Access_Copy.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'A1', 'nan', 'fileA100',
                     'nan', 'r100', 'General', 'Email', '20210111', 'formA', 'nan', 'replyA100', 'nan'],
                    ['B city', 'WY', '23456', 'nan', 'b200', 'General', 'Email', '20230202', 'B1^B2', 'Note',
                     'fileB200', 'nan', 'r200', 'General', 'Email', '20230212', 'formB', 'nan', 'replyB200', 'nan'],
                    ['C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'C1', 'nan', 'fileC300',
                     'nan', 'r300', 'General', 'Email', '20240313', 'formC', 'nan', 'replyC300', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, Access_Copy.csv")

        # Tests the contents of 2021-2022.csv.
        csv_path = os.path.join('test_data', 'script', '2021-2022.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'A1', 'nan', 'fileA100',
                     'nan', 'r100', 'General', 'Email', '20210111', 'formA', 'nan', 'replyA100', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, 2021-2022")

        # Tests the contents of 2023-2024.csv.
        csv_path = os.path.join(os.getcwd(), 'test_data', 'script', '2023-2024.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['B city', 'WY', '23456', 'nan', 'b200', 'General', 'Email', '20230202', 'B1^B2', 'Note',
                     'fileB200', 'nan', 'r200', 'General', 'Email', '20230212', 'formB', 'nan', 'replyB200', 'nan'],
                    ['C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'C1', 'nan', 'fileC300',
                     'nan', 'r300', 'General', 'Email', '20240313', 'formC', 'nan', 'replyC300', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, 2023-2024")

    def test_correct_preservation(self):
        """Test for when the script runs correctly and is in preservation mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'preservation_test_copy'),
                        os.path.join('test_data', 'script', 'preservation_test'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'preservation_test')
        subprocess.run(f"python {script_path} {input_directory} preservation", shell=True)

        # Tests the contents of archiving_correspondence.dat.
        csv_path = os.path.join('test_data', 'script', 'preservation_test', 'archiving_correspondence.dat')
        result = csv_to_list(csv_path, '\t')
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'nan', 'nan', 'nan', 'nan', '234 B St', 'Apt 7', 'nan', 'nan',
                     'B city', 'WY', '23456', 'nan', 'b200', 'General', 'Email', '20230202', 'B1^B2', 'Note',
                     'fileB200', 'nan', 'r200', 'General', 'Email', '20230212', 'formB', 'nan', 'replyB200', 'nan'],
                    ['Ms.', 'Gretel', 'G.', 'Green', 'nan', 'nan', 'nan', 'nan', '789 G St', 'nan', 'nan', 'nan',
                     'G city', 'GA', '78901', 'nan', 'g100', 'General', 'Email', '20210101', 'G1', 'nan', 'fileG100',
                     'nan', 'r700', 'General', 'Email', '20210111', 'formG', 'nan', 'reply_case', 'nan']]
        self.assertEqual(result, expected, "Problem with test for preservation, DAT")

        # Tests the contents of the deletion log.
        csv_path = os.path.join('test_data', 'script', 'deletion_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Ms.', 'Diane', 'D.', 'Dudly', 'nan', 'nan', 'nan', 'nan', '456 D St', 'nan', 'nan', 'nan',
                     'D city', 'DE', '45678', 'nan', 'd100', 'General', 'Email', '20210101', 'Prison Case', 'nan',
                     'fileD100', 'nan', 'r400', 'General', 'Email', '20210111', 'formD', 'nan', 'replyD100', 'nan'],
                    ['Ms.', 'Emma', 'E.', 'Evans', 'nan', 'nan', 'nan', 'nan', '567 E St', 'nan', 'nan', 'nan',
                     'E city', 'ME', '56789', 'nan', 'e100', 'General', 'Email', '20210101', 'Casework Issues', 'nan',
                     'fileE100', 'nan', 'r500', 'General', 'Email', '20210111', 'formE', 'nan', 'replyE100', 'nan'],
                    ['Ms.', 'Fiona', 'F.', 'Fowler', 'nan', 'nan', 'nan', 'nan', '678 F St', 'nan', 'nan', 'nan',
                     'F city', 'FL', '67890', 'nan', 'f100', 'General', 'Email', '20210101',
                     'Social Security^Casework', 'nan', 'fileF100', 'nan', 'r600', 'General', 'Email', '20210111',
                     'formF', 'nan', 'replyF100', 'nan'],
                    ['Ms.', 'Ann', 'A.', 'Anderson', 'nan', 'MD', 'nan', 'nan', '123 A St', 'nan', 'nan', 'nan',
                     'A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'A1', 'nan',
                     'file_casework', 'nan', 'r100', 'General', 'Email', '20210111', 'formA', 'nan', 'replyA100', 'nan'],
                    ['Mr.', 'Clive', 'C.', 'Cooper', 'Jr.', 'nan', 'CEO', 'Company', 'Attn: C', 'Division', 'POBox',
                     '345 C St', 'C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'C1', 'nan',
                     'fileC300', 'nan', 'r300', 'General', 'Email', '20240313', 'formC', 'nan', 'reply_casework', 'nan']]
        self.assertEqual(result, expected, "Problem with test for preservation, deletion log")

        # Tests the contents of the case log.
        csv_path = os.path.join('test_data', 'script', 'row_includes_case_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Ms.', 'Gretel', 'G.', 'Green', 'nan', 'nan', 'nan', 'nan', '789 G St', 'nan', 'nan', 'nan',
                     'G city', 'GA', '78901', 'nan', 'g100', 'General', 'Email', '20210101', 'G1', 'nan', 'fileG100',
                     'nan', 'r700', 'General', 'Email', '20210111', 'formG', 'nan', 'reply_case', 'nan']]
        self.assertEqual(result, expected, "Problem with test for preservation, case log")

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
