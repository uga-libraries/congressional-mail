"""
Tests for the script archival_office_correspondence_data.py
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
        filenames = ['Access_Copy.csv', '1997-1998.csv', 'undated.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_correct(self):
        """Test for when the script runs correctly."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'archival_office_correspondence_data.py')
        md_path = os.path.join('test_data', 'script_md.dat')
        subprocess.run(f"python {script_path} {md_path}", shell=True)

        # Tests the contents of Access_Copy.csv.
        csv_path = os.path.join('test_data', 'Access_Copy.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'correspondence_type', 'correspondence_topic',
                     'correspondence_subtopic', 'letter_date', 'staffer_initials', 'document_number', 'comments'],
                    ['LOS ANGELES', 'CA', '12345', 'ISSUE', 'HE-MAN', 'nan', '970813', 'FWIW', '725SAT100', 'CD123'],
                    ['CAIRO', 'GA', '30001', 'ISSUE', 'CASE', 'nan', '980801', 'TBD', 'nan', 'nan'],
                    ['ATLANTA', 'GA', '30000-0001', 'ISSUE', 'TD-GEN', 'nan', '971001', 'FWIW', '725SAT101', 'nan'],
                    ['ATLANTA', 'GA', '30002', 'ISSUE', 'nan', 'nan', 'nan', 'FWIW', 'nan',
                     'A COMMENT THAT IS AS LONG AS IS PERMITTED BY THE FIELD LENGTH FOR THE COMMENTS COLUMN, '
                     'THE LAST ONE'],
                    ['COLUMBUS', 'GA', '30003', 'ISSUE', 'AG-TOB', 'ABC', '980113', 'TBD', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for correct, Access_Copy.csv")

        # Tests the contents of 1997-1998.csv.
        csv_path = os.path.join('test_data', '1997-1998.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'correspondence_type', 'correspondence_topic',
                     'correspondence_subtopic', 'letter_date', 'staffer_initials', 'document_number', 'comments'],
                    ['LOS ANGELES', 'CA', '12345', 'ISSUE', 'HE-MAN', 'nan', '970813', 'FWIW', '725SAT100', 'CD123'],
                    ['CAIRO', 'GA', '30001', 'ISSUE', 'CASE', 'nan', '980801', 'TBD', 'nan', 'nan'],
                    ['ATLANTA', 'GA', '30000-0001', 'ISSUE', 'TD-GEN', 'nan', '971001', 'FWIW', '725SAT101', 'nan'],
                    ['COLUMBUS', 'GA', '30003', 'ISSUE', 'AG-TOB', 'ABC', '980113', 'TBD', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for correct, 1997-1998")

        # Tests the contents of undated.csv.
        csv_path = os.path.join('test_data', 'undated.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'correspondence_type', 'correspondence_topic',
                     'correspondence_subtopic', 'letter_date', 'staffer_initials', 'document_number', 'comments'],
                    ['ATLANTA', 'GA', '30002', 'ISSUE', 'nan', 'nan', 'nan', 'FWIW', 'nan',
                     'A COMMENT THAT IS AS LONG AS IS PERMITTED BY THE FIELD LENGTH FOR THE COMMENTS COLUMN, '
                     'THE LAST ONE']]
        self.assertEqual(result, expected, "Problem with test for correct, undated")

    def test_error_argument(self):
        """Test for when the script exits due to an argument error."""
        script_path = os.path.join(os.getcwd(), '..', '..', 'archival_office_correspondence_data.py')

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
