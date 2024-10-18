"""
Tests for the script css_archiving_format.py
"""
import os
import pandas as pd
import subprocess
import unittest


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path)
    df = df.fillna('BLANK')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Remove script output, if it was made"""
        csv_path = os.path.join(os.getcwd(), 'test_data', 'CSS_Access_Copy.csv')
        if os.path.exists(csv_path):
            os.remove(csv_path)

    def test_correct(self):
        """Test for when the script runs correctly."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        md_path = os.path.join('test_data', 'script_md.dat')
        output = subprocess.run(f"python {script_path} {md_path}", shell=True, stdout=subprocess.PIPE)

        # Tests that it prints the correct message.
        result = output.stdout.decode('utf-8')
        expected = ("\r\nColumns remaining after removing personal identifiers are listed below.\r\nTo remove any of "
                    "these columns, add them to the 'remove' list in remove_pii() and run the script "
                    "again.\r\n\tcity\r\n\tstate\r\n\tzip\r\n\tcountry\r\n\tin_id\r\n\tin_type\r\n\tin_method\r\n"
                    "\tin_date\r\n\tin_topic\r\n\tin_text\r\n\tin_document_name\r\n\tin_fillin\r\n\tout_id\r\n"
                    "\tout_type\r\n\tout_method\r\n\tout_date\r\n\tout_topic\r\n\tout_text\r\n\tout_document_name\r\n"
                    "\tout_fillin\r\n")
        self.assertEqual(result, expected, "Problem with test for correct, printed message")

        # Tests that it saved the redacted data to a CSV.
        csv_path = os.path.join(os.getcwd(), 'test_data', 'CSS_Access_Copy.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['A city', 'AL', 12345, 'BLANK', 'a100', 'General', 'Email', 20240101, 'A1', 'BLANK', 'fileA100',
                     'BLANK', 'r100', 'General', 'Email', 20240111, 'formA', 'BLANK', 'replyA100', 'BLANK'],
                    ['B city', 'WY', 23456, 'BLANK', 'b200', 'Case', 'Email', 20240202, 'B1^B2', 'Note', 'fileB200',
                     'BLANK', 'r200', 'Case', 'Email', 20240212, 'formB', 'BLANK', 'replyB200', 'BLANK'],
                    ['C city', 'CO', 34567, 'BLANK', 'c300', 'General', 'Letter', 20240303, 'C1', 'BLANK', 'fileC300',
                     'BLANK', 'r300', 'General', 'Email', 20240313, 'formC', 'BLANK', 'replyC300', 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for correct, redacted CSV")

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
