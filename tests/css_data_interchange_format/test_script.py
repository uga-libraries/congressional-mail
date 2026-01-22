from datetime import date
import os
import pandas as pd
import shutil
import subprocess
import unittest
from test_topics_sort import make_dir_list


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('BLANK')
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
        # Metadata file and logs in the output directory.
        filenames = ['appraisal_check_log.csv', 'appraisal_delete_log.csv', 'archiving_correspondence_redacted.csv',
                     f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv",
                     'metadata_formatting_errors_state_code.csv', 'metadata_formatting_errors_update_date.csv',
                     'restriction_review.csv', 'topics_report.csv', 'topics_sort_file_not_found.csv',
                     'usability_report_matching.csv', 'usability_report_matching_details.csv',
                     'usability_report_metadata.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', 'script', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Copy of test data, and for access all the script outputs.
        test_folders = ['access_test', 'appraisal_test']
        for test_folder in test_folders:
            test_path = os.path.join('test_data', 'script', test_folder)
            if os.path.exists(test_path):
                shutil.rmtree(test_path)

        # Once all tests are updated, the only thing to delete is output_dir
        output_dir = os.path.join('test_data', 'script', 'output_dir')
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

    def test_access(self):
        """Test for when the script runs correctly in access mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'access_test_copy'),
                        os.path.join('test_data', 'script', 'access_test'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'access_test', 'export')
        output = subprocess.run(f"python {script_path} {input_directory} access",
                                shell=True, capture_output=True, text=True)

        # Tests the print statement.
        result = output.stdout
        expected = ('\nThe script is running in access mode.\nIt will remove rows for deleted or restricted letters '
                    'and columns with PII, make copies of the metadata split by calendar year, '
                    'and make a copy of the letters to and from constituents organized by topic\n')
        self.assertEqual(expected, result, "Problem with test for access, printed statement")

        # Tests the contents of the appraisal_check_log.csv.
        csv_path = os.path.join('test_data', 'script', 'access_test', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for access, appraisal_check_log.csv")

        # Tests the contents of the appraisal_delete_log.csv.
        csv_path = os.path.join('test_data', 'script', 'access_test', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'text', 'Appraisal_Category'],
                    ['usmail', 'BLANK', 'C', '19990315', '19990402', 'BLANK', '19990315', 'usmail', 'CASEWORK', ' ',
                     ' ', 'BLANK', 'POLAND', 'OUTGOING', r'..\documents\indivletters\2070078.doc', '2070078.doc',
                     ' ', 'BLANK', 'Neutral', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for access, appraisal_delete_log.csv")

        # Tests the contents of archiving_correspondence_redacted.csv.
        csv_path = os.path.join('test_data', 'script', 'access_test', 'archiving_correspondence_redacted.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['usmail', 'BLANK', 'C', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'usmail', 'BLANK', 'Smyrna', 'GA',
                     '30080-1944', 'USA', 'OUTGOING', r'..\documents\formletters\Airline Passenger BOR Act2 1999.doc',
                     'Airline Passenger BOR Act2 1999', ' ', 'BLANK'],
                    ['usmail', 'BLANK', 'C', '19990331', '19990402', 'BLANK', '19990331', 'usmail', 'INTTAX', ' ', ' ',
                     'BLANK', 'POLAND', 'OUTGOING', r'..\documents\formletters\inttax.doc', 'inttax.doc', ' ', 'BLANK'],
                    ['usmail', 'BLANK', 'C', '20000427', '20000427', 'BLANK', '20000427', 'usmail', 'TOUR5', 'Ellijay',
                     'GA', '30540', 'USA', 'OUTGOING', r'..\documents\formletters\flag.doc', 'flag.doc', ' ', 'BLANK'],
                    ['usmail', 'BLANK', 'C', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'usmail', 'BLANK', 'Atlanta', 'GA',
                     '30327-4346', 'USA', 'OUTGOING', r'..\documents\formletters\30046.doc', '30046.doc', ' ', 'BLANK'],
                    ['BLANK', '551', 'C', '19990315', '19990402', 'BLANK', '19990315', 'imail', 'FARMING', 'Marietta',
                     'GA', '30062-1668', 'USA', 'INCOMING', r'..\documents\objects\4007000.eml', 'BLANK',
                     '1c8614bf01caf83e00010e44.eml', 'BLANK'],
                    ['BLANK', '513', 'C', '20000427', '20000427', 'BLANK', '20000427', 'imail', 'BLANK', 'Marietta',
                     'GA', '30067-8581', 'USA', 'OUTGOING', r'..\documents\indivletters\2076104.doc', 'BLANK',
                     ' ', 'BLANK'],
                    ['BLANK', '513', 'C', '20120914', '20120914', 'BLANK', '20120914', 'imail', 'BLANK', 'Marietta',
                     'GA', '30062-1668', 'USA', 'OUTGOING', r'..\documents\formletters\2103422.html', '2103422',
                     ' ', 'BLANK'],
                    ['BLANK', '513', 'C', '19990721', '19990721', 'BLANK', '19990721', 'imail', 'BLANK', 'Washington',
                     'DC', '20420-0002', 'USA', 'OUTGOING', r'..\documents\formletters\208956.html', '208956',
                     ' ', 'BLANK'],
                    ['usmail', 'BLANK', 'C', '19990415', '19990502', 'BLANK', '19990415', 'usmail', 'AG',
                     'Marietta', 'GA', '30067-8582', 'USA', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['usmail', 'BLANK', 'C', '19990515', '19990602', 'BLANK', '19990515', 'usmail', 'OC',
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for access, archiving_correspondence_redacted.csv")

        # Tests the contents of form_letter_metadata.csv.
        csv_path = os.path.join('test_data', 'script', 'access_test', 'form_letter_metadata.csv')
        result = csv_to_list(csv_path)
        expected = [['document_id', 'version', 'document_grouping_id', 'document_type', 'document_display_name',
                     'document_description', 'document_name_x', 'created_by', 'revised_by', 'approved_by',
                     'creation_date', 'revision_date', 'last_used_date', 'status', 'inactive_flag',
                     'virtual_directory', 'fill-in_field_name', 'label', 'code', 'code_type', 'document_name_y',
                     'user_id', 'attached_date', 'text', 'form_letter_attachment_flag', 'file_name', 'owned_by'],
                    ['000001', '1', '123456', 'Form', 'Economy', 'BLANK', r'..\doc\formletter\econ.pdf', '17',
                     'JSmith', '17', '20101212', '20110101', '20150101', 'Approved', 'BLANK', 'Form Letters',
                     'position', 'BLANK', 'LABOR', 'DOC', r'..\doc\formletter\econ.pdf', '17', '20120101', 'text',
                     'Y', 'econ.pdf', '17'],
                    ['000001', '1', '123456', 'Form', 'Economy', 'BLANK', r'..\doc\formletter\econ.pdf', '17',
                     'JSmith', '17', '20101212', '20110101', '20150101', 'Approved', 'BLANK', 'Form Letters',
                     'position', 'BLANK', 'TRADE', 'DOC', r'..\doc\formletter\econ.pdf', '17', '20120101', 'text',
                     'Y', 'econ.pdf', '17'],
                    ['000002', '1', '123456', 'Form', 'Courts', 'Basic info on justice system',
                     r'..\doc\formletter\court.pdf', 'JSmith', '17', 'JSmith', '20101212', '20110101', '20150101',
                     'Inactive', 'Y', 'Form Letters', 'staff_member', 'Full Name:', 'COURT', 'COM',
                     r'..\doc\formletter\court.pdf', 'JSmith', '20120101', 'text', 'Y', 'court.pdf', 'JSmith']]
        self.assertEqual(expected, result, "Problem with test for access, form_letter_metadata.csv")

        # Tests the contents of 1999.csv.
        csv_path = os.path.join('test_data', 'script', 'access_test', 'correspondence_metadata_by_year', '1999.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['usmail', 'BLANK', 'C', '19990331', '19990402', 'BLANK', '19990331', 'usmail', 'INTTAX', ' ', ' ',
                     'BLANK', 'POLAND', 'OUTGOING', r'..\documents\formletters\inttax.doc', 'inttax.doc',
                     ' ', 'BLANK'],
                    ['BLANK', '551', 'C', '19990315', '19990402', 'BLANK', '19990315', 'imail', 'FARMING', 'Marietta',
                     'GA', '30062-1668', 'USA', 'INCOMING', r'..\documents\objects\4007000.eml', 'BLANK',
                     '1c8614bf01caf83e00010e44.eml', 'BLANK'],
                    ['BLANK', '513', 'C', '19990721', '19990721', 'BLANK', '19990721', 'imail', 'BLANK', 'Washington',
                     'DC', '20420-0002', 'USA', 'OUTGOING', r'..\documents\formletters\208956.html', '208956',
                     ' ', 'BLANK'],
                    ['usmail', 'BLANK', 'C', '19990415', '19990502', 'BLANK', '19990415', 'usmail', 'AG',
                     'Marietta', 'GA', '30067-8582', 'USA', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['usmail', 'BLANK', 'C', '19990515', '19990602', 'BLANK', '19990515', 'usmail', 'OC',
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for access, 1999.csv")

        # Tests the contents of 2000.csv.
        csv_path = os.path.join('test_data', 'script', 'access_test', 'correspondence_metadata_by_year', '2000.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['usmail', 'BLANK', 'C', '20000427', '20000427', 'BLANK', '20000427', 'usmail', 'TOUR5', 'Ellijay',
                     'GA', '30540', 'USA', 'OUTGOING', r'..\documents\formletters\flag.doc', 'flag.doc', ' ', 'BLANK'],
                    ['BLANK', '513', 'C', '20000427', '20000427', 'BLANK', '20000427', 'imail', 'BLANK', 'Marietta',
                     'GA', '30067-8581', 'USA', 'OUTGOING', r'..\documents\indivletters\2076104.doc',
                     'BLANK', ' ', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for access, 2000.csv")

        # Tests the contents of 2012.csv.
        csv_path = os.path.join('test_data', 'script', 'access_test', 'correspondence_metadata_by_year', '2012.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['BLANK', '513', 'C', '20120914', '20120914', 'BLANK', '20120914', 'imail', 'BLANK', 'Marietta',
                     'GA', '30062-1668', 'USA', 'OUTGOING', r'..\documents\formletters\2103422.html',
                     '2103422', ' ', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for access, 2012.csv")

        # Tests the contents of undated.csv.
        csv_path = os.path.join('test_data', 'script', 'access_test', 'correspondence_metadata_by_year', 'undated.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['usmail', 'BLANK', 'C', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'usmail', 'BLANK', 'Smyrna', 'GA',
                     '30080-1944', 'USA', 'OUTGOING', r'..\documents\formletters\Airline Passenger BOR Act2 1999.doc',
                     'Airline Passenger BOR Act2 1999', ' ', 'BLANK'],
                    ['usmail', 'BLANK', 'C', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'usmail', 'BLANK', 'Atlanta', 'GA',
                     '30327-4346', 'USA', 'OUTGOING', r'..\documents\formletters\30046.doc', '30046.doc', ' ', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for access, undated.csv")

        # Tests that Correspondence_by_Topic has the expected files.
        by_topic = os.path.join(os.getcwd(), 'test_data', 'script', 'access_test', 'Correspondence_by_Topic')
        result = make_dir_list(by_topic)
        expected = [os.path.join(by_topic, 'FARMING', 'from_constituents', '4007000.eml'),
                    os.path.join(by_topic, 'INTTAX', 'to_constituents', 'inttax.doc')]
        self.assertEqual(expected, result, "Problem with test for access, Correspondence_by_Topic")

        # Tests the contents of topics_sort_file_not_found.csv.
        csv_path = os.path.join('test_data', 'script', 'access_test', 'topics_sort_file_not_found.csv')
        result = csv_to_list(csv_path)
        expected = [['TOUR5', r'..\documents\formletters\flag.doc']]
        self.assertEqual(expected, result, "Problem with test for access, topics_sort_file_not_found.csv")

    def test_accession(self):
        """Test for when the script runs correctly in accession mode."""
        # Makes copy of test data for easier deletion of script output.
        shutil.copytree(os.path.join('test_data', 'script', 'accession'),
                        os.path.join('test_data', 'script', 'output_dir'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'output_dir', 'constituent_mail_export')
        output = subprocess.run(f"python {script_path} {input_directory} accession",
                                shell=True, capture_output=True, text=True)

        # Tests the print statement.
        result = output.stdout
        expected = ('\nThe script is running in accession mode.\n'
                    'It will produce usability and appraisal reports and not change the export.\n')
        self.assertEqual(expected, result, "Problem with test for accession, printed statement")

        # Tests the contents of the appraisal_check_log.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'text', 'Appraisal_Category'],
                    ['BLANK', '513', 'C', '19990721', '19990721', 'BLANK', '19990721', 'imail', 'BLANK', 'Washington',
                     'DC', '20420-0002', 'USA', 'OUTGOING', r'..\documents\formletters\legal_case.html',
                     'legal_case.html', ' ', 'BLANK', 'text8', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for accession, appraisal_check_log.csv")

        # Tests the contents of the appraisal_delete_log.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'text', 'Appraisal_Category'],
                    ['BLANK', '513', 'C', '20000427', '20000427', 'BLANK', '2000 April 27', 'imail', 'BLANK',
                     'Marietta', 'GA', '30067-8581', 'USA', 'OUTGOING',
                     r'..\documents\indivletters\casework_12345.doc', 'BLANK', ' ', 'BLANK', 'text5', 'Casework'],
                    ['BLANK', '513', 'C', '20120914', '20120914', 'BLANK', '20120914', 'imail', 'CASEWORK2',
                     'Marietta', 'Georgia', '30062-1668', 'USA', 'OUTGOING', r'..\documents\formletters\2103422.html',
                     '2103422.html', ' ', 'BLANK', 'text9', 'Casework'],
                    ['BLANK', '551', 'C', '19990315', '19990402', 'BLANK', '19990315', 'imail', 'CASEWORK2',
                     'Marietta', 'Georgia', '30062-1668', 'USA', 'INCOMING', r'..\documents\objects\4007000.eml',
                     'BLANK', '1c8614bf01caf83e00010e44.eml', 'BLANK', 'text7', 'Casework'],
                    ['usmail', 'BLANK', 'C', '19990331', '19990402', 'BLANK', '19990331', 'usmail', 'C1', ' ', ' ',
                     'BLANK', 'POLAND', 'OUTGOING', r'..\documents\indivletters\case work\00001.doc', '00001.doc',
                     ' ', 'BLANK', 'text3', 'Casework'],
                    ['usmail', 'BLANK', 'C', '20000427', '20000427', 'BLANK', '2000-04-27', 'usmail', 'CASEWORK2',
                     'Ellijay', 'GA', '30540', 'USA', 'OUTGOING', r'..\documents\indivletters\00002.doc',
                     '00002.doc', ' ', 'BLANK', 'text1', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for accession, appraisal_delete_log.csv")

        # Tests the contents of the metadata_formatting_errors_update_date.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'metadata_formatting_errors_update_date.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['usmail', 'BLANK', 'C', '20000427', '20000427', 'BLANK', '2000-04-27', 'usmail', 'CASEWORK2',
                     'Ellijay', 'GA', '30540', 'USA', 'OUTGOING', r'..\documents\indivletters\00002.doc',
                     '00002.doc', ' ', 'BLANK'],
                    ['BLANK', '513', 'C', '20000427', '20000427', 'BLANK', '2000 April 27', 'imail', 'BLANK',
                     'Marietta', 'GA', '30067-8581', 'USA', 'OUTGOING',
                     r'..\documents\indivletters\casework_12345.doc', 'BLANK', ' ', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for accession, metadata_formatting_errors_update_date.csv")

        # Tests the contents of the metadata_formatting_errors_state_code.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'metadata_formatting_errors_state_code.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['usmail', 'BLANK', 'C', '19990331', '19990402', 'BLANK', '19990331', 'usmail', 'C1', ' ', ' ',
                     'BLANK', 'POLAND', 'OUTGOING', r'..\documents\indivletters\case work\00001.doc', '00001.doc',
                     ' ', 'BLANK'],
                    ['BLANK', '551', 'C', '19990315', '19990402', 'BLANK', '19990315', 'imail', 'CASEWORK2',
                     'Marietta', 'Georgia', '30062-1668', 'USA', 'INCOMING', r'..\documents\objects\4007000.eml',
                     'BLANK', '1c8614bf01caf83e00010e44.eml', 'BLANK'],
                    ['BLANK', '513', 'C', '20120914', '20120914', 'BLANK', '20120914', 'imail', 'CASEWORK2',
                     'Marietta', 'Georgia', '30062-1668', 'USA', 'OUTGOING', r'..\documents\formletters\2103422.html',
                     '2103422.html', ' ', 'BLANK'],
                    ['usmail', 'BLANK', 'C', '19990315', '19990402', 'BLANK', '19990315', 'usmail', 'INTTAX',
                     ' ', ' ', 'BLANK', 'POLAND', 'OUTGOING', r'..\documents\formletters\busintax.doc',
                     'busintax.doc', ' ', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for accession, metadata_formatting_errors_state_code.csv")

        # Tests the contents of the topics_report.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'topics_report.csv')
        result = csv_to_list(csv_path)
        expected = [['Topic', 'Topic_Count'],
                    ['BLANK', '4'],
                    ['CASEWORK2', '3'],
                    ['C1', '1'],
                    ['INTTAX', '1']]
        self.assertEqual(expected, result, "Problem with test for accession, topics_report.csv")

        # Tests the contents of the usability_report_matching.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'usability_report_matching.csv')
        result = csv_to_list(csv_path)
        expected = [['Category', 'Row/File_Count', 'Row_Percent'],
                    ['Match', '6', '67%'],
                    ['Metadata_Only', '3', '33%'],
                    ['Metadata_Blank', '0', '0%'],
                    ['Directory_Only', '1', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for accession, usability_report_matching.csv")

        # Tests the contents of the usability_report_matching_details.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'usability_report_matching_details.csv')
        result = csv_to_list(csv_path)
        result.sort()
        expected = [['Category', 'Path'],
                    ['Directory Only', os.path.join(input_directory, 'documents', 'indivletters', 'casework_999999.doc')],
                    ['Metadata Only', os.path.join(input_directory, 'documents', 'formletters', 'airline act2.doc')],
                    ['Metadata Only', os.path.join(input_directory, 'documents', 'formletters', 'busintax.doc')],
                    ['Metadata Only', os.path.join(input_directory, 'documents', 'indivletters', '00002.doc')]]
        self.assertEqual(expected, result, "Problem with test for accession, usability_report_matching_details.csv")

        # Tests the contents of the usability_report_metadata.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'usability_report_metadata.csv')
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
                    ['update_date', 'True', '2', '22.22', '2'],
                    ['response_type', 'True', '0', '0.0', 'uncheckable'],
                    ['group_name', 'True', '4', '44.44', 'uncheckable'],
                    ['document_type', 'True', '0', '0.0', 'uncheckable'],
                    ['communication_document_name', 'True', '0', '0.0', '0'],
                    ['communication_document_id', 'True', '2', '22.22', 'uncheckable'],
                    ['file_location', 'True', '0', '0.0', 'uncheckable'],
                    ['file_name', 'True', '9', '100.0', 'uncheckable']]
        self.assertEqual(expected, result, "Problem with test for accession, usability_report_metadata.csv")

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
                    'It will delete letters due to appraisal and make a report of metadata to review for restrictions,'
                    'but not change the metadata file.\n')
        self.assertEqual(expected, result, "Problem with test for appraisal, printed statement")

        # Tests the contents of the appraisal check log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'text', 'Appraisal_Category'],
                    ['BLANK', '513', 'C', '19990721', '19990721', 'BLANK', '19990721', 'imail', 'BLANK', 'Washington',
                     'DC', '20420-0002', 'USA', 'OUTGOING', r'..\documents\formletters\legal_case.html',
                     'legal_case.html', ' ', 'BLANK', 'text8', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for appraisal check log")

        # Tests the contents of the appraisal delete log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'text', 'Appraisal_Category'],
                    ['BLANK', '513', 'C', '20000427', '20000427', 'BLANK', '20000427', 'imail', 'BLANK', 'Marietta',
                     'GA', '30067-8581', 'USA', 'OUTGOING', r'..\documents\indivletters\casework_12345.doc',
                     'BLANK', ' ', 'BLANK', 'text5', 'Casework'],
                    ['BLANK', '513', 'C', '20120914', '20120914', 'BLANK', '20120914', 'imail', 'CASE 3', 'Marietta',
                     'GA', '30062-1668', 'USA', 'OUTGOING', r'..\documents\formletters\2103422.html',
                     '2103422.html', ' ', 'BLANK', 'text9', 'Casework'],
                    ['BLANK', '551', 'C', '19990315', '19990402', 'BLANK', '19990315', 'imail', 'CASE4', 'Marietta',
                     'GA', '30062-1668', 'USA', 'INCOMING', r'..\documents\objects\4007000.eml', 'BLANK',
                     '1c8614bf01caf83e00010e44.eml', 'BLANK', 'text7', 'Casework'],
                    ['usmail', 'BLANK', 'C', '19990331', '19990402', 'BLANK', '19990331', 'usmail', 'C1', ' ', ' ',
                     'BLANK', 'POLAND', 'OUTGOING', r'..\documents\indivletters\case work\00001.doc', '00001.doc',
                     ' ', 'BLANK', 'text3', 'Casework'],
                    ['usmail', 'BLANK', 'C', '20000427', '20000427', 'BLANK', '20000427', 'usmail', 'CASEWORK2',
                     'Ellijay', 'GA', '30540', 'USA', 'OUTGOING', r'..\documents\indivletters\00002.doc',
                     '00002.doc', ' ', 'BLANK', 'text1', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for appraisal, appraisal delete log")

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        csv_path = os.path.join('test_data', 'script', f"file_deletion_log_{today}.csv")
        result = csv_to_list(csv_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\indivletters\casework_12345.doc'.replace('..', input_directory),
                     '26.6', today, today, 'A9C52FA2BA1A0E51AD59DA2E4DA08C9D', 'Casework'],
                    [r'..\documents\objects\4007000.eml'.replace('..', input_directory),
                     '0.0', today, today, '49C13D076A41E65DBE137D695E22A6A7', 'Casework'],
                    [r'..\documents\indivletters\case work\00001.doc'.replace('..', input_directory),
                     '26.6', today, today, '7FF68E7C773483286AE3FEBDF2554EF8', 'Casework'],
                    [r'..\documents\indivletters\00002.doc'.replace('..', input_directory),
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Cannot delete: FileNotFoundError']]
        self.assertEqual(expected, result, "Problem with test for appraisal, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = ['out_1B.dat', 'out_2A.dat', 'out_2C.dat', 'out_2D.dat',
                    '2103422.html', '30046.doc', 'legal_case.html']
        self.assertEqual(expected, result, "Problem with test for appraisal, input_directory contents")

        # Tests the contents of restriction_review.csv.
        csv_path = os.path.join('test_data', 'script', 'restriction_review.csv')
        result = csv_to_list(csv_path)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['usmail', 'BLANK', 'X', '20010101', '20010102', 'BLANK', '20010103', 'usmail', 'court',
                     'Atlanta', 'GA', '30327', 'USA', 'INCOMING', '..\\documents\\objects\\1.txt', '1.txt',
                     'BLANK', 'BLANK'],
                    ['usmail', 'BLANK', 'X', '20020101', '20020102', 'BLANK', '20020103', 'usmail', 'refugee',
                     'Atlanta', 'GA', '30327', 'USA', 'INCOMING', '..\\documents\\objects\\4.txt', '4.txt',
                     'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for appraisal, restriction_review.csv")

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
        self.assertEqual(expected, result, "Problem with test for error argument, printed error")


if __name__ == '__main__':
    unittest.main()

