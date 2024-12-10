"""
Tests for the script archival_office_correspondence_data.py
"""
from datetime import date
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
        filenames = ['archive_redacted.csv', '1997-1998.csv', 'undated.csv',
                     f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv", 'metadata_deletion_log.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', 'script', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        if os.path.exists(os.path.join('test_data', 'script', 'preservation_test')):
            shutil.rmtree(os.path.join('test_data', 'script', 'preservation_test'))

    def test_access(self):
        """Test for when the script runs in access mode."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'archival_office_correspondence_data.py')
        input_directory = os.path.join('test_data', 'script', 'access_test')
        subprocess.run(f"python {script_path} {input_directory} access", shell=True)

        output_directory = os.path.join('test_data', 'script')

        # Tests the contents of archive_redacted.csv.
        csv_path = os.path.join(output_directory, 'archive_redacted.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'correspondence_type', 'correspondence_topic',
                     'correspondence_subtopic', 'letter_date', 'staffer_initials', 'document_number', 'comments'],
                    ['LOS ANGELES', 'CA', '12345', 'ISSUE', 'HE-MAN', 'nan', '970813', 'FWIW', '725SAT100', 'CD123'],
                    ['CAIRO', 'GA', '30001', 'ISSUE', 'nan', 'nan', '980801', 'TBD', 'nan', 'nan'],
                    ['ATLANTA', 'GA', '30000-0001', 'ISSUE', 'TD-GEN', 'nan', '971001', 'FWIW', '725SAT101', 'nan'],
                    ['ATLANTA', 'GA', '30002', 'ISSUE', 'nan', 'nan', 'nan', 'FWIW', 'nan',
                     'A COMMENT THAT IS AS LONG AS IS PERMITTED BY THE FIELD LENGTH FOR THE COMMENTS COLUMN, '
                     'THE LAST ONE'],
                    ['COLUMBUS', 'GA', '30003', 'ISSUE', 'AG-TOB', 'ABC', '980113', 'TBD', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, archive_redacted.csv")

        # Tests the contents of 1997-1998.csv.
        csv_path = os.path.join(output_directory, '1997-1998.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'correspondence_type', 'correspondence_topic',
                     'correspondence_subtopic', 'letter_date', 'staffer_initials', 'document_number', 'comments'],
                    ['LOS ANGELES', 'CA', '12345', 'ISSUE', 'HE-MAN', 'nan', '970813', 'FWIW', '725SAT100', 'CD123'],
                    ['CAIRO', 'GA', '30001', 'ISSUE', 'nan', 'nan', '980801', 'TBD', 'nan', 'nan'],
                    ['ATLANTA', 'GA', '30000-0001', 'ISSUE', 'TD-GEN', 'nan', '971001', 'FWIW', '725SAT101', 'nan'],
                    ['COLUMBUS', 'GA', '30003', 'ISSUE', 'AG-TOB', 'ABC', '980113', 'TBD', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, 1997-1998")

        # Tests the contents of undated.csv.
        csv_path = os.path.join(output_directory, 'undated.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'correspondence_type', 'correspondence_topic',
                     'correspondence_subtopic', 'letter_date', 'staffer_initials', 'document_number', 'comments'],
                    ['ATLANTA', 'GA', '30002', 'ISSUE', 'nan', 'nan', 'nan', 'FWIW', 'nan',
                     'A COMMENT THAT IS AS LONG AS IS PERMITTED BY THE FIELD LENGTH FOR THE COMMENTS COLUMN, '
                     'THE LAST ONE']]
        self.assertEqual(result, expected, "Problem with test for access, undated")

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

    def test_preservation(self):
        """Test for when the script runs in preservation mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'preservation_test_copy'),
                        os.path.join('test_data', 'script', 'preservation_test'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'archival_office_correspondence_data.py')
        input_directory = os.path.join('test_data', 'script', 'preservation_test')
        subprocess.run(f"python {script_path} {input_directory} preservation", shell=True)

        output_directory = os.path.join('test_data', 'script')
        today = date.today().strftime('%Y-%m-%d')

        # Tests the contents of archive.dat.
        csv_path = os.path.join(input_directory, 'archive.dat')
        result = csv_to_list(csv_path, '\t')
        expected = [['name', 'title', 'organization', 'address_line_1', 'address_line_2', 'city', 'state_code',
                     'zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic',
                     'letter_date', 'staffer_initials', 'document_number', 'comments'],
                    ['NEWTON, I.M.', 'INVENTOR', 'nan', '9000 ROAD', 'nan', 'CAIRO', 'GA', '30001', 'ISSUE',
                     'nan', 'nan', '980801', 'TBD', 'nan', 'Q222222'],
                    ['OLIVIA, JOAN, DR.', 'PROFESSOR', 'nan', 'BIG UNIVERSITY', 'ABC ST', 'ATLANTA', 'GA',
                     '30000-0001', 'ISSUE', 'TD-GEN', 'nan', '971001', 'FWIW', '725SAT101', 'nan'],
                    ['SMITH', 'nan', 'AN INSTITUTE', 'PO BOX 123', '1000 MAIN', 'COLUMBUS', 'GA', '30003', 'ISSUE',
                     'AG-TOB', 'ABC', '980113', 'TBD', 'nan', 'Comment']]
        self.assertEqual(result, expected, "Problem with test for preservation, DAT")

        # Tests the contents of the file deletion log.
        csv_path = os.path.join(output_directory, f"file_deletion_log_{today}.csv")
        result = csv_to_list(csv_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [os.path.join(input_directory, 'text', '111111.txt'), '0.0', today, today,
                     '6ECB035862F8047CC98F39AA54F62C15', 'nan'],
                    [os.path.join(input_directory, 'text', '444444.txt'), '0.1', today, today,
                     'C29C5262DF8A6B0072322ED6942BE134', 'nan'],
                    [os.path.join(input_directory, 'text', '000000.txt'), 'nan', 'nan', 'nan', 'nan',
                     'Cannot delete: FileNotFoundError']]
        self.assertEqual(result, expected, "Problem with test for preservation, file deletion log")

        # Tests the contents of the metadata deletion log.
        csv_path = os.path.join(output_directory, 'metadata_deletion_log.csv')
        result = csv_to_list(csv_path)
        expected = [['name', 'title', 'organization', 'address_line_1', 'address_line_2', 'city', 'state_code',
                     'zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic',
                     'letter_date', 'staffer_initials', 'document_number', 'comments'],
                    ['MILLER, FRANK A., MR.', 'nan', 'nan', '123 HOLLYWOOD', 'nan', 'LOS ANGELES', 'CA', '12345',
                     'ISSUE', 'CASE', 'nan', '970813', 'FWIW', '725SAT100', 'Q111111'],
                    ['nan', 'CEO', 'START UP Z', '444 BROAD ST', 'nan', 'ATLANTA', 'GA', '30002', 'ISSUE', 'CASE',
                     'nan', 'nan', 'FWIW', 'nan', 'Q444444'],
                    ['Zayne', 'nan', 'nan', '456 Street', 'nan', 'ATLANTA', 'GA', '30004', 'ISSUE', 'CASE', 'nan',
                     '980113', 'TBD', 'nan', 'Q000000']]
        self.assertEqual(result, expected, "Problem with test for preservation, metadata deletion log")

        # Tests the correct files were deleted.
        result = files_in_dir(os.path.join(input_directory, 'text'))
        expected = ['222222.txt', '333333.txt', '555555.txt', 'ED55-1.txt', 'F01-11.txt']
        self.assertEqual(result, expected, "Problem with test for preservation, files deleted")


if __name__ == '__main__':
    unittest.main()
