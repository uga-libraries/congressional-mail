"""
Tests for the script css_data_interchange_format.py
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
        filenames = ['Access_Copy.csv', '1999-2000.csv', '2011-2012.csv', 'undated.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', 'script', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_correct(self):
        """Test for when the script runs correctly."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')
        md_path = os.path.join('test_data', 'script')
        subprocess.run(f"python {script_path} {md_path}", shell=True)

        # Tests the contents of Access_Copy.csv.
        csv_path = os.path.join('test_data', 'script', 'Access_Copy.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Ellijay', 'GA', '30540', 'USA', 'usmail', 'nan', 'C', '20000427', '20000427', 'nan', '20000427',
                     'usmail', 'TOUR5', 'OUTGOING', r'..\documents\formletters\flag.doc.doc', 'flag.doc', ' ', 'nan'],
                    ['Atlanta', 'GA', '30327-4346', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan', 'usmail',
                     'nan', 'OUTGOING', r'..\documents\formletters\30046.doc.doc', '30046.doc', ' ', 'nan'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990331', '19990402', 'nan', '19990331',
                     'usmail', 'INTTAX', 'OUTGOING', r'..\documents\formletters\inttax.doc.doc', 'inttax.doc',
                     ' ', 'nan'],
                    ['Smyrna', 'GA', '30080-1944', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan',
                     'usmail', 'nan', 'OUTGOING', r'..\documents\formletters\Airline Passenger BOR Act2 1999.doc',
                     'Airline Passenger BOR Act2 1999', ' ', 'nan'],
                    ['Marietta', 'GA', '30067-8581', 'USA', 'nan', '513', 'C', '20000427', '20000427', 'nan',
                     '20000427', 'imail', 'nan', 'OUTGOING', r'..\documents\indivletters\2076104.doc',
                     'nan', ' ', 'nan'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990315', '19990402', 'nan', '19990315',
                     'usmail', 'INTTAX', 'OUTGOING', r'..\documents\formletters\busintax.doc.doc', 'busintax.doc',
                     ' ', 'nan'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '513', 'C', '20120914', '20120914', 'nan',
                     '20120914', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\2103422.html', '2103422',
                     ' ', 'nan'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '551', 'C', '19990315', '19990402', 'nan',
                     '19990315', 'imail', 'nan', 'INCOMING', r'..\documents\objects\4007000.eml', 'nan',
                     '1c8614bf01caf83e00010e44.eml', 'nan'],
                    ['Washington', 'DC', '20420-0002', 'USA', 'nan', '513', 'C', '19990721', '19990721', 'nan',
                     '19990721', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\208956.html', '208956',
                     ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for correct, Access_Copy.csv")

        # Tests the contents of 1999-2000.csv.
        csv_path = os.path.join('test_data', 'script', '1999-2000.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Ellijay', 'GA', '30540', 'USA', 'usmail', 'nan', 'C', '20000427', '20000427', 'nan', '20000427',
                     'usmail', 'TOUR5', 'OUTGOING', r'..\documents\formletters\flag.doc.doc', 'flag.doc',
                     ' ', 'nan'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990331', '19990402', 'nan', '19990331',
                     'usmail', 'INTTAX', 'OUTGOING', r'..\documents\formletters\inttax.doc.doc', 'inttax.doc',
                     ' ', 'nan'],
                    ['Marietta', 'GA', '30067-8581', 'USA', 'nan', '513', 'C', '20000427', '20000427', 'nan',
                     '20000427', 'imail', 'nan', 'OUTGOING', r'..\documents\indivletters\2076104.doc',
                     'nan', ' ', 'nan'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990315', '19990402', 'nan', '19990315',
                     'usmail', 'INTTAX', 'OUTGOING', r'..\documents\formletters\busintax.doc.doc', 'busintax.doc',
                     ' ', 'nan'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '551', 'C', '19990315', '19990402', 'nan',
                     '19990315', 'imail', 'nan', 'INCOMING', r'..\documents\objects\4007000.eml', 'nan',
                     '1c8614bf01caf83e00010e44.eml', 'nan'],
                    ['Washington', 'DC', '20420-0002', 'USA', 'nan', '513', 'C', '19990721', '19990721', 'nan',
                     '19990721', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\208956.html', '208956',
                     ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for correct, 1999-2000")

        # Tests the contents of 2011-2012.csv.
        csv_path = os.path.join('test_data', 'script', '2011-2012.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '513', 'C', '20120914', '20120914', 'nan',
                     '20120914', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\2103422.html',
                     '2103422', ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for correct, 2011-2012")

        # Tests the contents of undated.csv.
        csv_path = os.path.join('test_data', 'script', 'undated.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Atlanta', 'GA', '30327-4346', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan', 'usmail',
                     'nan', 'OUTGOING', r'..\documents\formletters\30046.doc.doc', '30046.doc', ' ', 'nan'],
                    ['Smyrna', 'GA', '30080-1944', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan', 'usmail',
                     'nan', 'OUTGOING', r'..\documents\formletters\Airline Passenger BOR Act2 1999.doc',
                     'Airline Passenger BOR Act2 1999', ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for correct, undated")

    def test_error_argument(self):
        """Test for when the script exits due to an argument error."""
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path}", shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script and tests that it prints the correct error.
        output = subprocess.run(f"python {script_path}", shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Missing required argument: path to the metadata folder\r\n"
        self.assertEqual(result, expected, "Problem with test for error argument, printed error")


if __name__ == '__main__':
    unittest.main()

