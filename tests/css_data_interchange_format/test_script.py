"""
Tests for the script css_data_interchange_format.py
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
        filenames = ['Preservation_Copy.csv', f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv",
                     'case_remains_log.csv', 'metadata_deletion_log.csv', 'Access_Copy.csv', '1999-2000.csv',
                     '2011-2012.csv', 'undated.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', 'script', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        if os.path.exists(os.path.join('test_data', 'script', 'access_test')):
            shutil.rmtree(os.path.join('test_data', 'script', 'access_test'))

        if os.path.exists(os.path.join('test_data', 'script', 'preservation_test')):
            shutil.rmtree(os.path.join('test_data', 'script', 'preservation_test'))

    def test_access(self):
        """Test for when the script runs correctly in access mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'access_test_copy'),
                        os.path.join('test_data', 'script', 'access_test'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'access_test')
        subprocess.run(f"python {script_path} {input_directory} access", shell=True)

        # Tests the contents of Preservation_Copy.csv.
        csv_path = os.path.join('test_data', 'script', 'Preservation_Copy.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Ellijay', 'GA', '30540', 'USA', 'usmail', 'nan', 'C', '20000427', '20000427', 'nan', '20000427',
                     'usmail', 'TOUR5', 'OUTGOING', r'..\documents\formletters\flag.doc', 'flag.doc', ' ', 'nan'],
                    ['Atlanta', 'GA', '30327-4346', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan', 'usmail',
                     'nan', 'OUTGOING', r'..\documents\formletters\30046.doc', '30046.doc', ' ', 'nan'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990331', '19990402', 'nan', '19990331',
                     'usmail', 'INTTAX', 'OUTGOING', r'..\documents\formletters\inttax.doc', 'inttax.doc',
                     ' ', 'nan'],
                    ['Smyrna', 'GA', '30080-1944', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan',
                     'usmail', 'nan', 'OUTGOING', r'..\documents\formletters\Airline Passenger BOR Act2 1999.doc',
                     'Airline Passenger BOR Act2 1999', ' ', 'nan'],
                    ['Marietta', 'GA', '30067-8581', 'USA', 'nan', '513', 'C', '20000427', '20000427', 'nan',
                     '20000427', 'imail', 'nan', 'OUTGOING', r'..\documents\indivletters\2076104.doc',
                     'nan', ' ', 'nan'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '513', 'C', '20120914', '20120914', 'nan',
                     '20120914', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\2103422.html', '2103422',
                     ' ', 'nan'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '551', 'C', '19990315', '19990402', 'nan',
                     '19990315', 'imail', 'nan', 'INCOMING', r'..\documents\objects\4007000.eml', 'nan',
                     '1c8614bf01caf83e00010e44.eml', 'nan'],
                    ['Washington', 'DC', '20420-0002', 'USA', 'nan', '513', 'C', '19990721', '19990721', 'nan',
                     '19990721', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\208956.html', '208956',
                     ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, Preservation_Copy.csv")

        # Tests that no case remains log was made.
        result = os.path.exists(os.path.join('test_data', 'script', 'case_remains_log.csv'))
        self.assertEqual(result, False, "Problem with test for access, case remains log")

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        csv_path = os.path.join('test_data', 'script', f"file_deletion_log_{today}.csv")
        result = csv_to_list(csv_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\indivletters\2070078.doc'.replace('..', input_directory),
                     '26.6', today, today, '7FF68E7C773483286AE3FEBDF2554EF8', 'casework']]
        self.assertEqual(result, expected, "Problem with test for access, file deletion log")

        # Tests the contents of the metadata deletion log.
        csv_path = os.path.join('test_data', 'script', 'metadata_deletion_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990315', '19990402', 'nan', '19990315',
                     'usmail', 'CASEWORK', 'OUTGOING', r'..\documents\indivletters\2070078.doc', '2070078.doc',
                     ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, metadata deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = ['out_1B.dat', 'out_2A.dat', 'out_2C.dat', '30046.doc', 'flag.doc', 'inttax.doc',
                    '2076104.doc', '4007000.eml']
        self.assertEqual(result, expected, "Problem with test for access, input_directory contents")

        # Tests the contents of Access_Copy.csv.
        csv_path = os.path.join('test_data', 'script', 'Access_Copy.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Ellijay', 'GA', '30540', 'USA', 'usmail', 'nan', 'C', '20000427', '20000427', 'nan', '20000427',
                     'usmail', 'TOUR5', 'OUTGOING', r'..\documents\formletters\flag.doc', 'flag.doc', ' ', 'nan'],
                    ['Atlanta', 'GA', '30327-4346', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan', 'usmail',
                     'nan', 'OUTGOING', r'..\documents\formletters\30046.doc', '30046.doc', ' ', 'nan'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990331', '19990402', 'nan', '19990331',
                     'usmail', 'INTTAX', 'OUTGOING', r'..\documents\formletters\inttax.doc', 'inttax.doc',
                     ' ', 'nan'],
                    ['Smyrna', 'GA', '30080-1944', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan',
                     'usmail', 'nan', 'OUTGOING', r'..\documents\formletters\Airline Passenger BOR Act2 1999.doc',
                     'Airline Passenger BOR Act2 1999', ' ', 'nan'],
                    ['Marietta', 'GA', '30067-8581', 'USA', 'nan', '513', 'C', '20000427', '20000427', 'nan',
                     '20000427', 'imail', 'nan', 'OUTGOING', r'..\documents\indivletters\2076104.doc',
                     'nan', ' ', 'nan'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '513', 'C', '20120914', '20120914', 'nan',
                     '20120914', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\2103422.html', '2103422',
                     ' ', 'nan'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '551', 'C', '19990315', '19990402', 'nan',
                     '19990315', 'imail', 'nan', 'INCOMING', r'..\documents\objects\4007000.eml', 'nan',
                     '1c8614bf01caf83e00010e44.eml', 'nan'],
                    ['Washington', 'DC', '20420-0002', 'USA', 'nan', '513', 'C', '19990721', '19990721', 'nan',
                     '19990721', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\208956.html', '208956',
                     ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, Access_Copy.csv")

        # Tests the contents of 1999-2000.csv.
        csv_path = os.path.join('test_data', 'script', '1999-2000.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Ellijay', 'GA', '30540', 'USA', 'usmail', 'nan', 'C', '20000427', '20000427', 'nan', '20000427',
                     'usmail', 'TOUR5', 'OUTGOING', r'..\documents\formletters\flag.doc', 'flag.doc',
                     ' ', 'nan'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990331', '19990402', 'nan', '19990331',
                     'usmail', 'INTTAX', 'OUTGOING', r'..\documents\formletters\inttax.doc', 'inttax.doc',
                     ' ', 'nan'],
                    ['Marietta', 'GA', '30067-8581', 'USA', 'nan', '513', 'C', '20000427', '20000427', 'nan',
                     '20000427', 'imail', 'nan', 'OUTGOING', r'..\documents\indivletters\2076104.doc',
                     'nan', ' ', 'nan'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '551', 'C', '19990315', '19990402', 'nan',
                     '19990315', 'imail', 'nan', 'INCOMING', r'..\documents\objects\4007000.eml', 'nan',
                     '1c8614bf01caf83e00010e44.eml', 'nan'],
                    ['Washington', 'DC', '20420-0002', 'USA', 'nan', '513', 'C', '19990721', '19990721', 'nan',
                     '19990721', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\208956.html', '208956',
                     ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, 1999-2000")

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
        self.assertEqual(result, expected, "Problem with test for access, 2011-2012")

        # Tests the contents of undated.csv.
        csv_path = os.path.join('test_data', 'script', 'undated.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Atlanta', 'GA', '30327-4346', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan', 'usmail',
                     'nan', 'OUTGOING', r'..\documents\formletters\30046.doc', '30046.doc', ' ', 'nan'],
                    ['Smyrna', 'GA', '30080-1944', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan', 'usmail',
                     'nan', 'OUTGOING', r'..\documents\formletters\Airline Passenger BOR Act2 1999.doc',
                     'Airline Passenger BOR Act2 1999', ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, undated")

    def test_error_argument(self):
        """Test for when the script exits due to an argument error."""
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path}", shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script and tests that it prints the correct error.
        output = subprocess.run(f"python {script_path}", shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Missing required arguments, input_directory and script_mode\r\n"
        self.assertEqual(result, expected, "Problem with test for error argument, printed error")

    def test_preservation(self):
        """Test for when the script runs correctly in preservation mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'preservation_test_copy'),
                        os.path.join('test_data', 'script', 'preservation_test'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'preservation_test')
        subprocess.run(f"python {script_path} {input_directory} preservation", shell=True)

        # Tests the contents of Preservation_Copy.csv.
        csv_path = os.path.join('test_data', 'script', 'Preservation_Copy.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Atlanta', 'GA', '30327-4346', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan', 'usmail',
                     'nan', 'OUTGOING', r'..\documents\formletters\30046.doc', '30046.doc', ' ', 'nan'],
                    ['Caseyville', 'GA', '30080-1944', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan',
                     'usmail', 'nan', 'OUTGOING', r'..\documents\formletters\Airline Passenger BOR Act2 1999.doc',
                     'Airline Passenger BOR Act2 1999', ' ', 'nan'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990315', '19990402', 'nan', '19990315',
                     'usmail', 'INTTAX', 'OUTGOING', r'..\documents\formletters\busintax.doc', 'busintax.doc',
                     ' ', 'nan'],
                    ['Washington', 'DC', '20420-0002', 'USA', 'nan', '513', 'C', '19990721', '19990721', 'nan',
                     '19990721', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\legal_case.html',
                     'legal_case.html', ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for preservation, Preservation_Copy.csv")

        # Tests the contents of the case remains log.
        csv_path = os.path.join('test_data', 'script', 'case_remains_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Caseyville', 'GA', '30080-1944', 'USA', 'usmail', 'nan', 'C', 'nan', 'nan', 'nan', 'nan',
                     'usmail', 'nan', 'OUTGOING', r'..\documents\formletters\Airline Passenger BOR Act2 1999.doc',
                     'Airline Passenger BOR Act2 1999', ' ', 'nan'],
                    ['Washington', 'DC', '20420-0002', 'USA', 'nan', '513', 'C', '19990721', '19990721', 'nan',
                     '19990721', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\legal_case.html',
                     'legal_case.html', ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for preservation, case remains log")

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        csv_path = os.path.join('test_data', 'script', f"file_deletion_log_{today}.csv")
        result = csv_to_list(csv_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\indivletters\00002.doc'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\indivletters\00001.doc'.replace('..', input_directory),
                     '26.6', today, today, '7FF68E7C773483286AE3FEBDF2554EF8', 'casework'],
                    [r'..\documents\objects\4007000.eml'.replace('..', input_directory),
                     '0.0', today, today, '49C13D076A41E65DBE137D695E22A6A7', 'casework'],
                    [r'..\documents\indivletters\casework_12345.doc'.replace('..', input_directory),
                     '26.6', today, today, 'A9C52FA2BA1A0E51AD59DA2E4DA08C9D', 'casework']]
        self.assertEqual(result, expected, "Problem with test for preservation, file deletion log")

        # Tests the contents of the metadata deletion log.
        csv_path = os.path.join('test_data', 'script', 'metadata_deletion_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Ellijay', 'GA', '30540', 'USA', 'usmail', 'nan', 'C', '20000427', '20000427', 'nan', '20000427',
                     'usmail', 'CASE2', 'OUTGOING', r'..\documents\indivletters\00002.doc', '00002.doc', ' ', 'nan'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990331', '19990402', 'nan', '19990331',
                     'usmail', 'CASE 1', 'OUTGOING', r'..\documents\indivletters\00001.doc', '00001.doc',
                     ' ', 'nan'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '513', 'C', '20120914', '20120914', 'nan',
                     '20120914', 'imail', 'CASE 3', 'OUTGOING', r'..\documents\formletters\2103422.html',
                     '2103422.html', ' ', 'nan'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '551', 'C', '19990315', '19990402', 'nan',
                     '19990315', 'imail', 'CASE4', 'INCOMING', r'..\documents\objects\4007000.eml', 'nan',
                     '1c8614bf01caf83e00010e44.eml', 'nan'],
                    ['Marietta', 'GA', '30067-8581', 'USA', 'nan', '513', 'C', '20000427', '20000427', 'nan',
                     '20000427', 'imail', 'nan', 'OUTGOING', r'..\documents\indivletters\casework_12345.doc',
                     'nan', ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for preservation, metadata deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = ['out_1B.dat', 'out_2A.dat', 'out_2C.dat', '2103422.html', '30046.doc', 'legal_case.html']
        self.assertEqual(result, expected, "Problem with test for preservation, input_directory contents")


if __name__ == '__main__':
    unittest.main()

