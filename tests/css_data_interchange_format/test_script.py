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
        # Metadata file and logs in the input directory.
        filenames = ['appraisal_check_log.csv', 'appraisal_delete_log.csv', 'archiving_correspondence_redacted.csv'
                     f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv",
                     'metadata_formatting_errors_state_code.csv',
                     'topics_report.csv', 'usability_report_matching.csv', 'usability_report_matching_details.csv',
                     'usability_report_metadata.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', 'script', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Metadata split by congress year, in own directory.
        file_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year')
        if os.path.exists(file_path):
            shutil.rmtree(file_path)

        # Copy of test data.
        test_folders = ['access_test', 'appraisal_test']
        for test_folder in test_folders:
            test_path = os.path.join('test_data', 'script', test_folder)
            if os.path.exists(test_path):
                shutil.rmtree(test_path)

    def test_access(self):
        """Test for when the script runs correctly in access mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'access_test_copy'),
                        os.path.join('test_data', 'script', 'access_test'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'access_test')
        output = subprocess.run(f"python {script_path} {input_directory} access",
                                shell=True, capture_output=True, text=True)

        # Tests the print statement.
        result = output.stdout
        expected = ('\nThe script is running in access mode.\nIt will remove rows for deleted letters and columns with '
                    'PII from the merged metadata tables, and make copies of the metadata split by congress year\n')
        self.assertEqual(result, expected, "Problem with test for access, printed statement")

        # Tests the contents of the appraisal_check_log.csv.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for access, appraisal_check_log.csv")

        # Tests the contents of the appraisal_delete_log.csv.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'Appraisal_Category'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990315', '19990402', 'nan', '19990315',
                     'usmail', 'CASEWORK', 'OUTGOING', r'..\documents\indivletters\2070078.doc', '2070078.doc',
                     ' ', 'nan', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for access, appraisal_delete_log.csv")

        # Tests the contents of archiving_correspondence_redacted.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_redacted.csv')
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
        self.assertEqual(result, expected, "Problem with test for access, archiving_correspondence_redacted.csv")

        # Tests the contents of 1999-2000.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year', '1999-2000.csv')
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
        self.assertEqual(result, expected, "Problem with test for access, 1999-2000.csv")

        # Tests the contents of 2011-2012.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year', '2011-2012.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '513', 'C', '20120914', '20120914', 'nan',
                     '20120914', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\2103422.html',
                     '2103422', ' ', 'nan']]
        self.assertEqual(result, expected, "Problem with test for access, 2011-2012.csv")

        # Tests the contents of undated.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year', 'undated.csv')
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
        self.assertEqual(result, expected, "Problem with test for access, undated.csv")

    def test_accession(self):
        """Test for when the script runs correctly in accession mode."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'accession_test')
        output = subprocess.run(f"python {script_path} {input_directory} accession",
                                shell=True, capture_output=True, text=True)

        # Tests the print statement.
        result = output.stdout
        expected = ('\nThe script is running in accession mode.\n'
                    'It will produce usability and appraisal reports and not change the export.\n')
        self.assertEqual(result, expected, "Problem with test for accession, printed statement")

        # Tests the contents of the appraisal_check_log.csv.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'Appraisal_Category'],
                    ['Washington', 'DC', '20420-0002', 'USA', 'nan', '513', 'C', '19990721', '19990721', 'nan',
                     '19990721', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\legal_case.html',
                     'legal_case.html', ' ', 'nan', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for accession, appraisal_check_log.csv")

        # Tests the contents of the appraisal_delete_log.csv.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'Appraisal_Category'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990331', '19990402', 'nan', '19990331',
                     'usmail', 'CASE 1', 'OUTGOING', r'..\documents\indivletters\00001.doc', '00001.doc',
                     ' ', 'nan', 'Casework'],
                    ['Ellijay', 'GA', '30540', 'USA', 'usmail', 'nan', 'C', '20000427', '20000427', 'nan', '20000427',
                     'usmail', 'CASE2', 'OUTGOING', r'..\documents\indivletters\00002.doc', '00002.doc', ' ', 'nan',
                     'Casework'],
                    ['Marietta', 'GA', '30067-8581', 'USA', 'nan', '513', 'C', '20000427', '20000427', 'nan',
                     '20000427', 'imail', 'nan', 'OUTGOING', r'..\documents\indivletters\casework_12345.doc',
                     'nan', ' ', 'nan', 'Casework'],
                    ['Marietta', 'Georgia', '30062-1668', 'USA', 'nan', '513', 'C', '20120914', '20120914', 'nan',
                     '20120914', 'imail', 'CASE 3', 'OUTGOING', r'..\documents\formletters\2103422.html',
                     '2103422.html', ' ', 'nan', 'Casework'],
                    ['Marietta', 'Georgia', '30062-1668', 'USA', 'nan', '551', 'C', '19990315', '19990402', 'nan',
                     '19990315', 'imail', 'CASE4', 'INCOMING', r'..\documents\objects\4007000.eml', 'nan',
                     '1c8614bf01caf83e00010e44.eml', 'nan', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for accession, appraisal_delete_log.csv")

        # # Tests the contents of the metadata_1.csv.
        # csv_path = os.path.join('test_data', 'script', 'name.csv')
        # result = csv_to_list(csv_path)
        # expected = []
        # self.assertEqual(result, expected, "Problem with test for accession, name.csv")
        #
        # Tests the contents of the metadata_formatting_errors_state_code.csv.
        csv_path = os.path.join('test_data', 'script', 'metadata_formatting_errors_state_code.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990331', '19990402', 'nan', '19990331',
                     'usmail', 'CASE 1', 'OUTGOING', r'..\documents\indivletters\00001.doc', '00001.doc', ' ', 'nan'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990315', '19990402', 'nan', '19990315',
                     'usmail', 'INTTAX', 'OUTGOING', r'..\documents\formletters\busintax.doc', 'busintax.doc', ' ',
                     'nan'],
                    ['Marietta', 'Georgia', '30062-1668', 'USA', 'nan', '513', 'C', '20120914', '20120914', 'nan',
                     '20120914', 'imail', 'CASE 3', 'OUTGOING', r'..\documents\formletters\2103422.html',
                     '2103422.html', ' ', 'nan'],
                    ['Marietta', 'Georgia', '30062-1668', 'USA', 'nan', '551', 'C', '19990315', '19990402', 'nan',
                     '19990315', 'imail', 'CASE4', 'INCOMING', r'..\documents\objects\4007000.eml', 'nan',
                     '1c8614bf01caf83e00010e44.eml', 'nan']]
        self.assertEqual(result, expected, "Problem with test for accession, metadata_formatting_errors_state_code.csv")

        # Tests the contents of the topics_report.csv.
        csv_path = os.path.join('test_data', 'script', 'topics_report.csv')
        result = csv_to_list(csv_path)
        expected = [['Topic', 'Topic_Count'],
                    ['BLANK', '4'],
                    ['CASE2', '1'],
                    ['CASE 1', '1'],
                    ['INTTAX', '1'],
                    ['CASE 3', '1'],
                    ['CASE4', '1']]
        self.assertEqual(result, expected, "Problem with test for accession, topics_report.csv")

        # Tests the contents of the usability_report_matching.csv.
        csv_path = os.path.join('test_data', 'script', 'usability_report_matching.csv')
        result = csv_to_list(csv_path)
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '3'],
                    ['Directory_Only', '1'],
                    ['Match', '6'],
                    ['Metadata_Blank', '0']]
        self.assertEqual(result, expected, "Problem with test for accession, usability_report_matching.csv")

        # Tests the contents of the usability_report_matching_details.csv.
        csv_path = os.path.join('test_data', 'script', 'usability_report_matching_details.csv')
        result = csv_to_list(csv_path)
        result.sort()
        expected = [['Category', 'Path'],
                    ['Directory Only', r'test_data\script\accession_test\documents\indivletters\casework_999999.doc'],
                    ['Metadata Only', r'test_data\script\accession_test\documents\formletters\Airline Act2.doc'],
                    ['Metadata Only', r'test_data\script\accession_test\documents\formletters\busintax.doc'],
                    ['Metadata Only', r'test_data\script\accession_test\documents\indivletters\00002.doc']]
        self.assertEqual(result, expected, "Problem with test for accession, usability_report_matching_details.csv")

        # Tests the contents of the usability_report_metadata.csv.
        csv_path = os.path.join('test_data', 'script', 'usability_report_metadata.csv')
        result = csv_to_list(csv_path)
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '0', '0.0', 'uncheckable'],
                    ['state_code', 'True', '0', '0.0', '4'],
                    ['zip_code', 'True', '2', '22.22', '0'],
                    ['country', 'True', '0', '0.0', 'uncheckable'],
                    ['communication_type', 'True', '4', '44.44', 'uncheckable'],
                    ['approved_by', 'True', '5', '55.56', 'uncheckable'],
                    ['status', 'True', '0', '0.0', 'uncheckable'],
                    ['date_in', 'True', '2', '22.22', '0'],
                    ['date_out', 'True', '2', '22.22', '0'],
                    ['reminder_date', 'True', '9', '100.0', '0'],
                    ['update_date', 'True', '2', '22.22', '0'],
                    ['response_type', 'True', '0', '0.0', 'uncheckable'],
                    ['group_name', 'True', '4', '44.44', 'uncheckable'],
                    ['document_type', 'True', '0', '0.0', 'uncheckable'],
                    ['communication_document_name', 'True', '0', '0.0', '0'],
                    ['communication_document_id', 'True', '2', '22.22', 'uncheckable'],
                    ['file_location', 'True', '0', '0.0', 'uncheckable'],
                    ['file_name', 'True', '9', '100.0', 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for accession, usability_report_metadata.csv")

    def test_appraisal(self):
        """Test for when the script runs correctly in appraisal mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'appraisal_test_copy'),
                        os.path.join('test_data', 'script', 'appraisal_test'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'appraisal_test')
        output = subprocess.run(f"python {script_path} {input_directory} appraisal",
                                shell=True, capture_output=True, text=True)

        # Tests the print statement.
        result = output.stdout
        expected = ('\nThe script is running in appraisal mode.\n'
                    'It will delete letters due to appraisal but not change the metadata file.\n')
        self.assertEqual(result, expected, "Problem with test for appraisal, printed statement")

        # Tests the contents of the appraisal check log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'Appraisal_Category'],
                    ['Washington', 'DC', '20420-0002', 'USA', 'nan', '513', 'C', '19990721', '19990721', 'nan',
                     '19990721', 'imail', 'nan', 'OUTGOING', r'..\documents\formletters\legal_case.html',
                     'legal_case.html', ' ', 'nan', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for appraisal check log")

        # Tests the contents of the appraisal delete log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'Appraisal_Category'],
                    [' ', ' ', 'nan', 'POLAND', 'usmail', 'nan', 'C', '19990331', '19990402', 'nan', '19990331',
                     'usmail', 'CASE 1', 'OUTGOING', r'..\documents\indivletters\00001.doc', '00001.doc',
                     ' ', 'nan', 'Casework'],
                    ['Ellijay', 'GA', '30540', 'USA', 'usmail', 'nan', 'C', '20000427', '20000427', 'nan', '20000427',
                     'usmail', 'CASE2', 'OUTGOING', r'..\documents\indivletters\00002.doc', '00002.doc', ' ', 'nan',
                     'Casework'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '513', 'C', '20120914', '20120914', 'nan',
                     '20120914', 'imail', 'CASE 3', 'OUTGOING', r'..\documents\formletters\2103422.html',
                     '2103422.html', ' ', 'nan', 'Casework'],
                    ['Marietta', 'GA', '30062-1668', 'USA', 'nan', '551', 'C', '19990315', '19990402', 'nan',
                     '19990315', 'imail', 'CASE4', 'INCOMING', r'..\documents\objects\4007000.eml', 'nan',
                     '1c8614bf01caf83e00010e44.eml', 'nan', 'Casework'],
                    ['Marietta', 'GA', '30067-8581', 'USA', 'nan', '513', 'C', '20000427', '20000427', 'nan',
                     '20000427', 'imail', 'nan', 'OUTGOING', r'..\documents\indivletters\casework_12345.doc',
                     'nan', ' ', 'nan', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for appraisal, appraisal delete log")

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        csv_path = os.path.join('test_data', 'script', f"file_deletion_log_{today}.csv")
        result = csv_to_list(csv_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\indivletters\00001.doc'.replace('..', input_directory),
                     '26.6', today, today, '7FF68E7C773483286AE3FEBDF2554EF8', 'Casework'],
                    [r'..\documents\indivletters\00002.doc'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\objects\4007000.eml'.replace('..', input_directory),
                     '0.0', today, today, '49C13D076A41E65DBE137D695E22A6A7', 'Casework'],
                    [r'..\documents\indivletters\casework_12345.doc'.replace('..', input_directory),
                     '26.6', today, today, 'A9C52FA2BA1A0E51AD59DA2E4DA08C9D', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for appraisal, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = ['out_1B.dat', 'out_2A.dat', 'out_2C.dat', '2103422.html', '30046.doc', 'legal_case.html']
        self.assertEqual(result, expected, "Problem with test for appraisal, input_directory contents")

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
        # Runs the script.
        # Since just testing printing right now, using a folder for input_directory that is not an export.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'preservation_test')
        output = subprocess.run(f"python {script_path} {input_directory} preservation",
                                shell=True, capture_output=True, text=True)

        # Tests the print statement.
        result = output.stdout
        expected = '\nThe script is running in preservation mode.\nThe steps are TBD.\n'
        self.assertEqual(result, expected, "Problem with test for preservation, printed statement")


if __name__ == '__main__':
    unittest.main()

