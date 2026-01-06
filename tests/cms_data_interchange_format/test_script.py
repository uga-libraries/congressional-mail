"""
Tests for the script cms_data_interchange_format.py
"""
from datetime import date
import os
import pandas as pd
import shutil
import subprocess
import unittest
from test_sort_correspondence import make_dir_list


def csv_to_list(csv_path, sort=False):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison
    With the option to sort for ones with inconsistent order in the output"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('BLANK')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    if sort:
        csv_list.sort()
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
                     'metadata_formatting_errors_date_out.csv', 'metadata_formatting_errors_state.csv',
                     f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv", 'topics_report.csv',
                     'usability_report_matching.csv', 'usability_report_matching_details.csv',
                     'usability_report_metadata.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', 'script', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Metadata split by congress year, in own directory.
        folder_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year')
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # Incoming letters organized by topic, in own directory.
        file_path = os.path.join('test_data', 'script', 'Correspondence_by_Topic')
        if os.path.exists(file_path):
            shutil.rmtree(file_path)

        # Copy of test data for appraisal mode, which is altered by the script (files are deleted)).
        copy_path = os.path.join('test_data', 'script', 'appraisal_copy')
        if os.path.exists(copy_path):
            shutil.rmtree(copy_path)

    def test_access(self):
        """Test for when the script runs correctly in access mode."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'cms_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'access')
        output = subprocess.run(f"python {script_path} {input_directory} access",
                                shell=True, capture_output=True, text=True)

        # Tests the print statement.
        result = output.stdout
        expected = ('\nThe script is running in access mode.\nIt will remove rows for deleted letters '
                    'and columns with PII, make copies of the metadata split by congress year, '
                    'and make a copy of the constituent letters organized by topic\n')
        self.assertEqual(expected, result, "Problem with test for access, printed statement")

        # Tests the contents of the appraisal_check_log.csv.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag',
                     'Appraisal_Category'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', '11111', 'CON', '1', 'main', r'in-email\1.txt', 'BLANK', 'note text 1',
                     'COR', '11111', 'LEGAL CASE', 'Y', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for access, appraisal_check_log.csv")

        # Tests the contents of the appraisal_delete_log.csv.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for access, appraisal_delete_log.csv")

        # Tests the contents of archiving_correspondence_redacted.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_redacted.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', '11111', 'CON', '1', 'main', r'in-email\1.txt', 'BLANK',
                     'COR', '11111', 'LEGAL CASE', 'Y'],
                    ['Caseyville', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK',
                     '20220220', 'EMAIL', '22222', 'PRO', '1', 'main', r'in-email\2.txt', 'BLANK',
                     'COR', '22222', 'MINWAGE', 'Y'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK',
                     '20220330', 'EMAIL', '33333', 'PRO', '1', 'main', r'in-email\3.txt', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'EMAIL', '33333', 'PRO', '1', 'main', r'in-email\33.txt', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', '20230330', '20230330', 'BLANK',
                     '20230330', 'EMAIL', '33333', 'PRO', '1', 'main', r'in-email\333.txt', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y']]
        self.assertEqual(expected, result, "Problem with test for access, archiving_correspondence_redacted.csv")

        # Tests the contents of 2021-2022.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year', '2021-2022.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', '11111', 'CON', '1', 'main', r'in-email\1.txt', 'BLANK',
                     'COR', '11111', 'LEGAL CASE', 'Y'],
                    ['Caseyville', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK',
                     '20220220', 'EMAIL', '22222', 'PRO', '1', 'main', r'in-email\2.txt', 'BLANK',
                     'COR', '22222', 'MINWAGE', 'Y'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK',
                     '20220330', 'EMAIL', '33333', 'PRO', '1', 'main', r'in-email\3.txt', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y']]
        self.assertEqual(expected, result, "Problem with test for access, 2021-2022")

        # Tests the contents of 2023-2024.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year', '2023-2024.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', '20230330', '20230330', 'BLANK',
                     '20230330', 'EMAIL', '33333', 'PRO', '1', 'main', r'in-email\333.txt', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y']]
        self.assertEqual(expected, result, "Problem with test for access, 2023-2024")

        # Tests the contents of undated.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year', 'undated.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'EMAIL', '33333', 'PRO', '1', 'main', r'in-email\33.txt', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y']]
        self.assertEqual(expected, result, "Problem with test for access, undated")

        # Tests that Correspondence_by_Topic has the expected files.
        by_topic = os.path.join(os.getcwd(), 'test_data', 'script', 'Correspondence_by_Topic')
        result = make_dir_list(by_topic)
        expected = [os.path.join(by_topic, 'LEGAL CASE', '1.txt'),
                    os.path.join(by_topic, 'MINWAGE', '2.txt'),
                    os.path.join(by_topic, 'RIGHTS', '3.txt'),
                    os.path.join(by_topic, 'RIGHTS', '33.txt'),
                    os.path.join(by_topic, 'RIGHTS', '333.txt')]
        self.assertEqual(expected, result, "Problem with test for access, Correspondence_by_Topic")

    def test_accession(self):
        """Test for when the script runs correctly in accession mode"""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'cms_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'accession')
        output = subprocess.run(f"python {script_path} {input_directory} accession",
                                shell=True, capture_output=True, text=True)

        # Tests the print statement.
        result = output.stdout
        expected = ('\nThe script is running in accession mode.\n'
                    'It will produce usability and appraisal reports and not change the export.\n')
        self.assertEqual(expected, result, "Problem with test for accession, printed statement")

        # Tests the contents of the appraisal check log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag',
                     'Appraisal_Category'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', '11111', 'CON', '1', 'main', 'in-email\\case_name.txt', 'BLANK',
                     'note text 1', 'COR', '11111', 'LEGAL CASE', 'Y', 'Casework'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', '11111', 'CON', '1', 'main', 'out-custom\\1001.txt', 'BLANK',
                     'note text 1', 'COR', '11111', 'LEGAL CASE', 'Y', 'Casework'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', '20230330', '20230330', 'BLANK',
                     '20230330', 'EMAIL', '33333', 'PRO', '1', 'main', 'out-custom\\100X.txt', 'BLANK',
                     'Recommendation for legislation', 'COR', '33333', 'RIGHTS', 'Y', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for appraisal, appraisal_check_log.csv")

        # Tests the contents of the appraisal_delete_log.csv.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag',
                     'Appraisal_Category'],
                    ['Caseyville', 'Georgia', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '2022 Feb', 'BLANK',
                     '20220220', 'EMAIL', '22222', 'PRO', '1', 'main', 'in-email\\2.txt', 'BLANK',
                     'Letter of Recommendation', 'COR', '22222', 'MINWAGE', 'Y', 'Recommendation'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'EMAIL', '33333', 'PRO', '1', 'main', 'in-email\\3.txt', 'BLANK', 'Add to case file',
                     'COR', '33333', 'RIGHTS', 'Y', 'Casework'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '2022-03-30', 'BLANK',
                     '20220330', 'EMAIL', '33333', 'PRO', '1', 'main', 'forms\\1.txt', 'BLANK', 'CASEWORK',
                     'COR', '33333', 'RIGHTS', 'Y', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for appraisal, appraisal_delete_log.csv")

        # Tests the contents of the metadata_formatting_errors_date_out.csv.
        csv_path = os.path.join('test_data', 'script', 'metadata_formatting_errors_date_out.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['Caseyville', 'Georgia', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '2022 Feb', 'BLANK',
                     '20220220', 'EMAIL', '22222', 'PRO', '1', 'main', 'in-email\\2.txt', 'BLANK', 'COR', '22222',
                     'MINWAGE', 'Y'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '2022-03-30', 'BLANK',
                     '20220330', 'EMAIL', '33333', 'PRO', '1', 'main', 'forms\\1.txt', 'BLANK', 'COR', '33333',
                     'RIGHTS', 'Y']]
        self.assertEqual(expected, result, "Problem with test for accession, metadata_formatting_errors_date_out.csv")

        # Tests the contents of the metadata_formatting_errors_state.csv.
        csv_path = os.path.join('test_data', 'script', 'metadata_formatting_errors_state.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['Caseyville', 'Georgia', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '2022 Feb', 'BLANK',
                     '20220220', 'EMAIL', '22222', 'PRO', '1', 'main', 'in-email\\2.txt', 'BLANK', 'COR', '22222',
                     'MINWAGE', 'Y']]
        self.assertEqual(expected, result, "Problem with test for accession, metadata_formatting_errors_state.csv")

        # Tests the contents of the topics_report.csv.
        csv_path = os.path.join('test_data', 'script', 'topics_report.csv')
        result = csv_to_list(csv_path)
        expected = [['Topic', 'Topic_Count'],
                    ['RIGHTS', '3'],
                    ['LEGAL CASE', '2'],
                    ['MINWAGE', '1']]
        self.assertEqual(expected, result, "Problem with test for accession, topics_report.csv")

        # Tests the contents of the usability_report_matching.csv.
        csv_path = os.path.join('test_data', 'script', 'usability_report_matching.csv')
        result = csv_to_list(csv_path)
        expected = [['Category', 'Row/File_Count', 'Row_Percent'],
                    ['Match', '4', '67%'],
                    ['Metadata_Only', '2', '33%'],
                    ['Metadata_Blank', '0', '0%'],
                    ['Directory_Only', '1', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for accession, usability_report_matching.csv")

        # Tests the contents of the usability_report_matching_details.csv.
        csv_path = os.path.join('test_data', 'script', 'usability_report_matching_details.csv')
        result = csv_to_list(csv_path, sort=True)
        expected = [['Category', 'Path'],
                    ['Directory Only', f'{input_directory.lower()}\\documents\\out-custom\\1002.txt'],
                    ['Metadata Only', f'{input_directory.lower()}\\documents\\in-email\\3.txt'],
                    ['Metadata Only', f'{input_directory.lower()}\\documents\\out-custom\\100x.txt']]
        self.assertEqual(expected, result, "Problem with test for accession, usability_report_matching_details.csv")

        # Tests the contents of the usability_report_metadata.csv.
        csv_path = os.path.join('test_data', 'script', 'usability_report_metadata.csv')
        result = csv_to_list(csv_path)
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '0', '0.0', 'uncheckable'],
                    ['state', 'True', '0', '0.0', '1'],
                    ['zip_code', 'True', '0', '0.0', '0'],
                    ['country', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_type', 'True', '0', '0.0', 'uncheckable'],
                    ['staff', 'True', '0', '0.0', 'uncheckable'],
                    ['date_in', 'True', '1', '16.67', '0'],
                    ['date_out', 'True', '1', '16.67', '2'],
                    ['tickler_date', 'True', '6', '100.0', '0'],
                    ['update_date', 'True', '1', '16.67', '0'],
                    ['response_type', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_code', 'True', '0', '0.0', 'uncheckable'],
                    ['position', 'True', '0', '0.0', 'uncheckable'],
                    ['2C_sequence_number', 'True', '0', '0.0', 'uncheckable'],
                    ['document_type', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_document_name', 'True', '0', '0.0', '0'],
                    ['file_location', 'True', '6', '100.0', 'uncheckable'],
                    ['code_type', 'True', '0', '0.0', 'uncheckable'],
                    ['code', 'True', '0', '0.0', 'uncheckable'],
                    ['code_description', 'True', '0', '0.0', 'uncheckable'],
                    ['inactive_flag', 'True', '0', '0.0', 'uncheckable']]
        self.assertEqual(expected, result, "Problem with test for accession, usability_report_metadata.csv")

    def test_appraisal(self):
        """Test for when the script runs correctly in appraisal mode."""
        # Makes a copy of the test data in the repo, since the script alters the data by deleting files.
        shutil.copytree(os.path.join('test_data', 'script', 'appraisal'),
                        os.path.join('test_data', 'script', 'appraisal_copy'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'cms_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'appraisal_copy')
        output = subprocess.run(f"python {script_path} {input_directory} appraisal",
                                shell=True, capture_output=True, text=True)

        # Tests the print statement.
        result = output.stdout
        expected = ('\nThe script is running in appraisal mode.\n'
                    'It will delete letters due to appraisal but not change the metadata file.\n')
        self.assertEqual(expected, result, "Problem with test for appraisal, printed statement")

        # Tests the contents of the appraisal check log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag',
                     'Appraisal_Category'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', '11111', 'CON', '1', 'main', 'in-email\\case_name.txt', 'BLANK',
                     'note text 1', 'COR', '11111', 'LEGAL CASE', 'Y', 'Casework'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', '11111', 'CON', '1', 'main', 'out-custom\\1001.txt', 'BLANK',
                     'note text 1', 'COR', '11111', 'LEGAL CASE', 'Y', 'Casework'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', '20230330', '20230330', 'BLANK',
                     '20230330', 'EMAIL', '33333', 'PRO', '1', 'main', 'out-custom\\1002.txt', 'BLANK',
                     'Recommendation for legislation', 'COR', '33333', 'RIGHTS', 'Y', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for appraisal, appraisal_check_log.csv")

        # Tests the contents of the appraisal_delete_log.csv.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag',
                    'Appraisal_Category'],
                    ['Caseyville', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK',
                     '20220220', 'EMAIL', '22222', 'PRO', '1', 'main', 'in-email\\2.txt', 'BLANK',
                     'Letter of Recommendation', 'COR', '22222', 'MINWAGE', 'Y', 'Recommendation'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'EMAIL', '33333', 'PRO', '1', 'main', 'in-email\\3.txt', 'BLANK', 'Add to case file',
                     'COR', '33333', 'RIGHTS', 'Y', 'Casework'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK',
                     '20220330', 'EMAIL', '33333', 'PRO', '1', 'main', 'forms\\1.txt', 'BLANK', 'CASEWORK',
                     'COR', '33333', 'RIGHTS', 'Y', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for appraisal, appraisal_delete_log.csv")

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        csv_path = os.path.join('test_data', 'script', f"file_deletion_log_{today}.csv")
        result = csv_to_list(csv_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [os.path.join('test_data', 'script', 'appraisal_copy', 'documents', 'in-email', '2.txt'),
                     '0.1', today, today, 'BFC30C1C407A46A42D322B493E783D8A', 'Recommendation'],
                    [os.path.join('test_data', 'script', 'appraisal_copy', 'documents', 'in-email', '3.txt'),
                     '0.2', today, today, '3372E0A98AEBE7DB66A368010DB78AF3', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for appraisal, file_delete_log.csv")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = ['1B.out', '2A.out', '2B.out', '2C.out', '2D.out', '8A.out',
                    '1.txt', 'case_name.txt', '1001.txt', '1002.txt']
        self.assertEqual(expected, result, "Problem with test for appraisal, input_directory contents")

    def test_error_argument(self):
        """Test for when the script exits due to an argument error."""
        script_path = os.path.join(os.getcwd(), '..', '..', 'cms_data_interchange_format.py')

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

