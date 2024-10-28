"""
Tests for the script css_archiving_format.py
"""
import os
import pandas as pd
import subprocess
import unittest


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('nan')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Remove script outputs, if they were made"""
        filenames = ['CSS_Access_Copy.csv', '2021-2022.csv', '2023-2024.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_correct(self):
        """Test for when the script runs correctly."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        md_path = os.path.join('test_data', 'script_md.dat')
        subprocess.run(f"python {script_path} {md_path}", shell=True)

        # Tests the contents of CSS_Access_Copy.csv.
        csv_path = os.path.join('test_data', 'CSS_Access_Copy.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'A1', 'nan', 'fileA100',
                     'nan', 'r100', 'General', 'Email', '20210111', 'formA', 'nan', 'replyA100', 'nan'],
                    ['B city', 'WY', '23456', 'nan', 'b200', 'Case', 'Email', '20230202', 'B1^B2', 'Note', 'fileB200',
                     'nan', 'r200', 'Case', 'Email', '20230212', 'formB', 'nan', 'replyB200', 'nan'],
                    ['C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'C1', 'nan', 'fileC300',
                     'nan', 'r300', 'General', 'Email', '20240313', 'formC', 'nan', 'replyC300', 'nan']]
        self.assertEqual(result, expected, "Problem with test for correct, CSS_Access_Copy.csv")

        # Tests the contents of 2021-2022.csv.
        csv_path = os.path.join('test_data', '2021-2022.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'A1', 'nan', 'fileA100',
                     'nan', 'r100', 'General', 'Email', '20210111', 'formA', 'nan', 'replyA100', 'nan']]
        self.assertEqual(result, expected, "Problem with test for correct, 2021-2022")

        # Tests the contents of 2023-2024.csv.
        csv_path = os.path.join(os.getcwd(), 'test_data', '2023-2024.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['B city', 'WY', '23456', 'nan', 'b200', 'Case', 'Email', '20230202', 'B1^B2', 'Note', 'fileB200',
                     'nan', 'r200', 'Case', 'Email', '20230212', 'formB', 'nan', 'replyB200', 'nan'],
                    ['C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'C1', 'nan', 'fileC300',
                     'nan', 'r300', 'General', 'Email', '20240313', 'formC', 'nan', 'replyC300', 'nan']]
        self.assertEqual(result, expected, "Problem with test for correct, 2023-2024")

    def test_error_argument(self):
        """Test for when the script exits due to an argument error."""
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path}", shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script and tests that it prints the correct error.
        output = subprocess.run(f"python {script_path}", shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Missing required argument: path to the metadata file\r\n"
        self.assertEqual(result, expected, "Problem with test for error argument, printed error")


if __name__ == '__main__':
    unittest.main()
