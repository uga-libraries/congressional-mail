"""
Tests for the script css_archiving_format.py
"""
from datetime import date
import os
import pandas as pd
import shutil
import subprocess
import unittest


def csv_to_list(csv_path, sort=False):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison
    with the option to sort for the match details report with inconsistent row order"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('nan')
    if sort:
        df = df.sort_values(by=['Category', 'Path'])
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
        # Files saved in the parent of input_directory.
        filenames = ['archiving_correspondence_redacted.csv', '2021-2022.csv', '2023-2024.csv',
                     'appraisal_check_log.csv', 'appraisal_delete_log.csv',
                     f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv",
                     'metadata_formatting_errors_state.csv', 'metadata_formatting_errors_zip.csv',
                     'metadata_formatting_errors_in_date.csv', 'metadata_formatting_errors_in_doc.csv',
                     'metadata_formatting_errors_out_date.csv', 'metadata_formatting_errors_out_doc.csv',
                     'topics_report.csv', 'usability_report_matching.csv', 'usability_report_matching_details.csv',
                     'usability_report_metadata.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', 'script', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Copy of input_directory made for some test modes.
        for mode in ('Accession', 'Appraisal', 'Preservation'):
            copy_path = os.path.join('test_data', 'script', f'{mode}_Constituent_Mail_Export')
            if os.path.exists(copy_path):
                shutil.rmtree(copy_path)

    def test_correct_access(self):
        """Test for when the script runs correctly and is in access mode."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'Access_Constituent_Mail_Export')
        printed = subprocess.run(f"python {script_path} {input_directory} access",
                                 shell=True, capture_output=True, text=True)

        # Tests the printed statement.
        result = printed.stdout
        expected = ("\nThe script is running in access mode.\nIt will remove rows for deleted letters and columns with "
                    "PII, and make copies of the metadata split by congress year\n")
        self.assertEqual(result, expected, "Problem with test for access, printed statement")

        # Tests the contents of the appraisal check log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for access, appraisal check log")

        # Tests the contents of the appraisal delete log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['Ms.', 'Diane', 'D.', 'Dudly', 'nan', 'nan', 'nan', 'nan', '456 D St', 'nan', 'nan', 'nan',
                     'D city', 'DE', '45678', 'nan', 'd100', 'General', 'Email', '20210101', 'Resumes',
                     'nan', r'..\documents\BlobExport\objects\444444.txt', 'nan', 'r400', 'General', 'Email',
                     '20210111', 'D', 'academy nomination', r'..\documents\BlobExport\indivletters\000004.txt', 'nan',
                     'Academy_Application|Job_Application'],
                    ['Ms.', 'Emma', 'E.', 'Evans', 'nan', 'nan', 'nan', 'nan', '567 E St', 'nan', 'nan', 'nan',
                     'E city', 'ME', '56789', 'nan', 'e100', 'General', 'Email', '20210101', 'Casework Issues',
                     'nan', r'..\documents\BlobExport\objects\555555.txt', 'nan', 'r500', 'General', 'Email',
                     '20210111', 'E', 'nan', r'..\documents\BlobExport\indivletters\000005.txt', 'nan', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for access, appraisal delete log")

        # Tests the contents of archiving_correspondence_redacted.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_redacted.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_document_name', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name'],
                    ['A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'A1',
                     r'..\documents\BlobExport\objects\111111.txt', 'r100', 'General', 'Email', '20210111',
                     'A', r'..\documents\BlobExport\formletters\A'],
                    ['B city', 'WY', '23456', 'nan', 'b200', 'General', 'Email', '20230202', 'B1^B2',
                     r'..\documents\BlobExport\objects\222222.txt', 'r200', 'General', 'Email', '20230212',
                     'B', r'..\documents\BlobExport\formletters\B'],
                    ['C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'A1',
                     r'..\documents\BlobExport\objects\333333.txt', 'r300', 'General', 'Email', '20240313',
                     'A', r'..\documents\BlobExport\formletters\A']]
        self.assertEqual(result, expected, "Problem with test for access, archiving_correspondence_redacted.csv")

        # Tests the contents of 2021-2022.csv.
        csv_path = os.path.join('test_data', 'script', '2021-2022.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_document_name', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_document_name'],
                    ['A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'A1',
                     r'..\documents\BlobExport\objects\111111.txt', 'r100', 'General', 'Email', '20210111',
                     'A', r'..\documents\BlobExport\formletters\A']]
        self.assertEqual(result, expected, "Problem with test for access, 2021-2022.csv")

        # Tests the contents of 2023-2024.csv.
        csv_path = os.path.join(os.getcwd(), 'test_data', 'script', '2023-2024.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_document_name', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_document_name'],
                    ['B city', 'WY', '23456', 'nan', 'b200', 'General', 'Email', '20230202', 'B1^B2',
                     r'..\documents\BlobExport\objects\222222.txt', 'r200', 'General', 'Email', '20230212',
                     'B', r'..\documents\BlobExport\formletters\B'],
                    ['C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'A1',
                     r'..\documents\BlobExport\objects\333333.txt', 'r300', 'General', 'Email', '20240313',
                     'A', r'..\documents\BlobExport\formletters\A']]
        self.assertEqual(result, expected, "Problem with test for access, 2023-2024.csv")

        # Tests that no undated.csv was made.
        result = os.path.exists(os.path.join(os.getcwd(), 'test_data', 'script', 'undated.csv'))
        self.assertEqual(result, False, "Problem with test for access, undated.csv")

        # Tests the other script mode outputs were not made.
        output_directory = os.path.join('test_data', 'script')
        result = [os.path.exists(os.path.join(output_directory, 'usability_report_metadata.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_state.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_zip.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_in_date.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_in_doc.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_out_date.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_out_doc.csv')),
                  os.path.exists(os.path.join(output_directory, 'usability_report_matching.csv')),
                  os.path.exists(os.path.join(output_directory, 'usability_report_matching_details.csv')),
                  os.path.exists(os.path.join(output_directory, 'topics_report.csv'))]
        expected = [False, False, False, False, False, False, False, False, False, False]
        self.assertEqual(result, expected, "Problem with test for access, other script mode outputs")

    def test_correct_accession(self):
        """Test for when the script runs correctly and is in accession mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'Accession_Constituent_Mail_Export_copy'),
                        os.path.join('test_data', 'script', 'Accession_Constituent_Mail_Export'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'Accession_Constituent_Mail_Export')
        printed = subprocess.run(f"python {script_path} {input_directory} accession",
                                 shell=True, capture_output=True, text=True)

        # Tests the printed statement.
        result = printed.stdout
        expected = ("\nThe script is running in accession mode.\n"
                    "It will produce usability and appraisal reports and not change the export.\n")
        self.assertEqual(result, expected, "Problem with test for accession, printed statement")

        # Tests the contents of the appraisal check log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['Ms.', 'Gretel', 'G.', 'Green', 'nan', 'nan', 'nan', 'nan', '789 G St', 'nan', 'nan', 'nan',
                     'G city', 'GA', '78901', 'nan', 'g100', 'General', 'Email', '20210101', 'E', 'nan',
                     r'..\documents\BlobExport\objects\777777.txt', 'nan', 'r700', 'General', 'Email', '20210111',
                     'nan', 'nan', r'..\documents\BlobExport\indivletters\000007.txt', 'Court case', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for accession, appraisal check log")

        # Tests the contents of the appraisal delete log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['Mr.', 'Clive', 'C.', 'Cooper', 'Jr.', 'nan', 'CEO', 'Company', 'Attn: C', 'Division', 'POBox',
                     '345 C St', 'C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'Misc',
                     'Maybe casework', r'..\documents\BlobExport\objects\333333.txt', 'nan', 'r300', 'General',
                     'Email', '2024-03-13', 'B1^B2', 'nan', r'..\documents\BlobExport\indivletters\000003.txt', 'nan',
                     'Casework'],
                    ['Ms.', 'Ann', 'A.', 'Anderson', 'nan', 'MD', 'nan', 'nan', '123 A St', 'nan', 'nan', 'nan',
                     'A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'Misc',
                     'academy nomination',
                     r'..\documents\BlobExport\objects\111111.txt', 'nan', 'r100', 'General', 'Email', '20210111',
                     'nan', 'nan', r'..\documents\BlobExport\indivletters\000001.txt', 'nan', 'Academy_Application'],
                    ['Ms.', 'Diane', 'D.', 'Dudly', 'nan', 'nan', 'nan', 'nan', '456 D St', 'nan', 'nan', 'nan',
                     'D city', 'DEL', '45678', 'nan', 'd100', 'General', 'Email', '20210101', 'Casework', 'nan',
                     r'..\documents\BlobExport\objects\444444.txt', 'nan', 'r400', 'General', 'Email', '20210111',
                     'Recommendations', 'nan', r'..\documents\BlobExport\formletters\D.txt', 'nan',
                     'Casework|Recommendation'],
                    ['Ms.', 'Emma', 'E.', 'Evans', 'nan', 'nan', 'nan', 'nan', '567 E St', 'nan', 'nan', 'nan',
                     'E city', 'ME', '56789', 'nan', 'e100', 'General', 'Email', '20210101', 'Recommendations', 'nan',
                     r'..\documents\BlobExport\objects\555555.txt', 'nan', 'r500', 'General', 'Email', '20210111',
                     'E', 'nan', r'..\documents\BlobExport\indivletters\000005.txt', 'nan', 'Recommendation'],
                    ['Ms.', 'Fiona', 'F.', 'Fowler', 'nan', 'nan', 'nan', 'nan', '678 F St', 'nan', 'nan', 'nan',
                     'F city', 'fl', '67890', 'nan', 'f100', 'General', 'Email', '20210101',
                     'Social Security^Casework', 'nan', 'nan', 'nan', 'r600',
                     'General', 'Email', '20210111', 'E', 'nan', r'..\documents\BlobExport\formletters\F.txt', 'nan',
                     'Casework']]
        self.assertEqual(result, expected, "Problem with test for accession, appraisal delete log")

        # Tests the contents of metadata_formatting_errors_state.csv.
        csv_path = os.path.join('test_data', 'script', 'metadata_formatting_errors_state.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Ms.', 'Diane', 'D.', 'Dudly', 'nan', 'nan', 'nan', 'nan', '456 D St', 'nan', 'nan', 'nan',
                     'D city', 'DEL', '45678', 'nan', 'd100', 'General', 'Email', '20210101', 'Casework', 'nan',
                     r'..\documents\BlobExport\objects\444444.txt', 'nan', 'r400', 'General', 'Email', '20210111',
                     'Recommendations', 'nan', r'..\documents\BlobExport\formletters\D.txt', 'nan'],
                    ['Ms.', 'Fiona', 'F.', 'Fowler', 'nan', 'nan', 'nan', 'nan', '678 F St', 'nan', 'nan', 'nan',
                     'F city', 'fl', '67890', 'nan', 'f100', 'General', 'Email', '20210101',
                     'Social Security^Casework', 'nan', 'nan', 'nan', 'r600', 'General', 'Email', '20210111', 'E',
                     'nan', r'..\documents\BlobExport\formletters\F.txt', 'nan']]
        self.assertEqual(result, expected, "Problem with test for accession, metadata_formatting_errors_state.csv")

        # Tests the contents of metadata_formatting_errors_out_date.csv.
        csv_path = os.path.join('test_data', 'script', 'metadata_formatting_errors_out_date.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Mr.', 'Clive', 'C.', 'Cooper', 'Jr.', 'nan', 'CEO', 'Company', 'Attn: C', 'Division', 'POBox',
                     '345 C St', 'C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'Misc',
                     'Maybe casework', r'..\documents\BlobExport\objects\333333.txt', 'nan', 'r300', 'General',
                     'Email', '2024-03-13', 'B1^B2', 'nan', r'..\documents\BlobExport\indivletters\000003.txt', 'nan']]
        self.assertEqual(result, expected,
                         "Problem with test for accession, metadata_formatting_errors_out_date.csv")

        # Tests the other metadata formatting reports were not made.
        output_directory = os.path.join('test_data', 'script')
        result = [os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_zip.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_in_date.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_in_doc.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_out_doc.csv'))]
        expected = [False, False, False, False]
        self.assertEqual(result, expected, "Problem with test for accession, other metadata formatting reports")

        # Tests the contents of topics_report.csv.
        csv_path = os.path.join('test_data', 'script', 'topics_report.csv')
        result = csv_to_list(csv_path)
        expected = [['Topic', 'In_Topic_Count', 'Out_Topic_Count', 'Total'],
                    ['B1^B2', '1', '2', '3'],
                    ['BLANK', '0', '2', '2'],
                    ['Casework', '1', '0', '1'],
                    ['E', '1', '2', '3'],
                    ['Misc', '2', '0', '2'],
                    ['Recommendations', '1', '1', '2'],
                    ['Social Security^Casework', '1', '0', '1']]
        self.assertEqual(result, expected, "Problem with test for accession, topics_report.csv")

        # Tests the contents of usability_report_matching.csv.
        csv_path = os.path.join('test_data', 'script', 'usability_report_matching.csv')
        result = csv_to_list(csv_path)
        expected = [['Category', 'Count'],
                    ['Metadata_Only', '3'],
                    ['Directory_Only', '2'],
                    ['Match', '10'],
                    ['Metadata_Blank', '1']]
        self.assertEqual(result, expected, "Problem with test for accession, usability_report_matching.csv")

        # Tests the contents of usability_report_matching_details.csv.
        csv_path = os.path.join('test_data', 'script', 'usability_report_matching_details.csv')
        result = csv_to_list(csv_path, sort=True)
        expected = [['Category', 'Path'],
                    ['Directory Only', r'test_data\script\Accession_Constituent_Mail_Export\documents\formletters\B.txt'],
                    ['Directory Only', r'test_data\script\Accession_Constituent_Mail_Export\documents\objects\666666.txt'],
                    ['Metadata Only', r'test_data\script\Accession_Constituent_Mail_Export\documents\objects\444444.txt'],
                    ['Metadata Only', r'test_data\script\Accession_Constituent_Mail_Export\documents\objects\555555.txt'],
                    ['Metadata Only', r'test_data\script\Accession_Constituent_Mail_Export\documents\objects\B.txt']]
        self.assertEqual(result, expected, "Problem with test for accession, usability_report_matching_details.csv")

        # Tests the contents of usability_report_metadata.csv.
        csv_path = os.path.join('test_data', 'script', 'usability_report_metadata.csv')
        result = csv_to_list(csv_path)
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['prefix', 'True', '0', '0.0', 'uncheckable'],
                    ['first', 'True', '0', '0.0', 'uncheckable'],
                    ['middle', 'True', '0', '0.0', 'uncheckable'],
                    ['last', 'True', '0', '0.0', 'uncheckable'],
                    ['suffix', 'True', '6', '85.71', 'uncheckable'],
                    ['appellation', 'True', '6', '85.71', 'uncheckable'],
                    ['title', 'True', '6', '85.71', 'uncheckable'],
                    ['org', 'True', '6', '85.71', 'uncheckable'],
                    ['addr1', 'True', '0', '0.0', 'uncheckable'],
                    ['addr2', 'True', '5', '71.43', 'uncheckable'],
                    ['addr3', 'True', '6', '85.71', 'uncheckable'],
                    ['addr4', 'True', '6', '85.71', 'uncheckable'],
                    ['city', 'True', '0', '0.0', 'uncheckable'],
                    ['state', 'True', '0', '0.0', '2'],
                    ['zip', 'True', '0', '0.0', '0'],
                    ['country', 'True', '7', '100.0', 'uncheckable'],
                    ['in_id', 'True', '0', '0.0', 'uncheckable'],
                    ['in_type', 'True', '0', '0.0', 'uncheckable'],
                    ['in_method', 'True', '0', '0.0', 'uncheckable'],
                    ['in_date', 'True', '0', '0.0', '0'],
                    ['in_topic', 'True', '0', '0.0', 'uncheckable'],
                    ['in_text', 'True', '4', '57.14', 'uncheckable'],
                    ['in_document_name', 'True', '1', '14.29', '0'],
                    ['in_fillin', 'True', '7', '100.0', 'uncheckable'],
                    ['out_id', 'True', '0', '0.0', 'uncheckable'],
                    ['out_type', 'True', '0', '0.0', 'uncheckable'],
                    ['out_method', 'True', '0', '0.0', 'uncheckable'],
                    ['out_date', 'True', '0', '0.0', '1'],
                    ['out_topic', 'True', '2', '28.57', 'uncheckable'],
                    ['out_text', 'True', '7', '100.0', 'uncheckable'],
                    ['out_document_name', 'True', '0', '0.0', '0'],
                    ['out_fillin', 'True', '6', '85.71', 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for accession, usability_report_metadata.csv")

        # Tests the other script mode outputs were not made.
        output_directory = os.path.join('test_data', 'script')
        today = date.today().strftime('%Y-%m-%d')
        result = [os.path.exists(os.path.join(output_directory, '2021-2022.csv')),
                  os.path.exists(os.path.join(output_directory, '2023-2024.csv')),
                  os.path.exists(os.path.join(output_directory, 'archiving_correspondence_redacted.csv')),
                  os.path.exists(os.path.join('test_data', 'script', f"file_deletion_log_{today}.csv"))]
        expected = [False, False, False, False]
        self.assertEqual(result, expected, "Problem with test for accession, other script mode outputs")

    def test_correct_appraisal(self):
        """Test for when the script runs correctly and is in appraisal mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'Appraisal_Constituent_Mail_Export_copy'),
                        os.path.join('test_data', 'script', 'Appraisal_Constituent_Mail_Export'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'Appraisal_Constituent_Mail_Export')
        printed = subprocess.run(f"python {script_path} {input_directory} appraisal",
                                 shell=True, capture_output=True, text=True)

        # Tests the printed statement.
        result = printed.stdout
        expected = ("\nThe script is running in appraisal mode.\n"
                    "It will delete letters due to appraisal but not change the metadata file.\n")
        self.assertEqual(result, expected, "Problem with test for appraisal, printed statement")

        # Tests the contents of the appraisal check log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['Ms.', 'Gretel', 'G.', 'Green', 'nan', 'nan', 'nan', 'nan', '789 G St', 'nan', 'nan', 'nan',
                     'G city', 'GA', '78901', 'nan', 'g100', 'General', 'Email', '20210101', 'E', 'nan',
                     r'..\documents\BlobExport\objects\777777.txt', 'nan', 'r700', 'General', 'Email', '20210111',
                     'nan', 'nan', r'..\documents\BlobExport\indivletters\000007.txt', 'Court case', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for appraisal, appraisal check log")

        # Tests the contents of the appraisal delete log.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['Mr.', 'Clive', 'C.', 'Cooper', 'Jr.', 'nan', 'CEO', 'Company', 'Attn: C', 'Division', 'POBox',
                     '345 C St', 'C city', 'CO', '34567', 'nan', 'c300', 'General', 'Letter', '20240303', 'Misc',
                     'Maybe casework', r'..\documents\BlobExport\objects\333333.txt', 'nan', 'r300', 'General',
                     'Email', '2024-03-13', 'B1^B2', 'nan', r'..\documents\BlobExport\indivletters\000003.txt', 'nan',
                     'Casework'],
                    ['Ms.', 'Ann', 'A.', 'Anderson', 'nan', 'MD', 'nan', 'nan', '123 A St', 'nan', 'nan', 'nan',
                     'A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20210101', 'Misc',
                     'academy nomination',
                     r'..\documents\BlobExport\objects\111111.txt', 'nan', 'r100', 'General', 'Email', '20210111',
                     'nan', 'nan', r'..\documents\BlobExport\indivletters\000001.txt', 'nan', 'Academy_Application'],
                    ['Ms.', 'Diane', 'D.', 'Dudly', 'nan', 'nan', 'nan', 'nan', '456 D St', 'nan', 'nan', 'nan',
                     'D city', 'DEL', '45678', 'nan', 'd100', 'General', 'Email', '20210101', 'Casework', 'nan',
                     r'..\documents\BlobExport\objects\444444.txt', 'nan', 'r400', 'General', 'Email', '20210111',
                     'Recommendations', 'nan', r'..\documents\BlobExport\formletters\D.txt', 'nan',
                     'Casework|Recommendation'],
                    ['Ms.', 'Emma', 'E.', 'Evans', 'nan', 'nan', 'nan', 'nan', '567 E St', 'nan', 'nan', 'nan',
                     'E city', 'ME', '56789', 'nan', 'e100', 'General', 'Email', '20210101', 'Recommendations', 'nan',
                     r'..\documents\BlobExport\objects\555555.txt', 'nan', 'r500', 'General', 'Email', '20210111',
                     'E', 'nan', r'..\documents\BlobExport\indivletters\000005.txt', 'nan', 'Recommendation'],
                    ['Ms.', 'Fiona', 'F.', 'Fowler', 'nan', 'nan', 'nan', 'nan', '678 F St', 'nan', 'nan', 'nan',
                     'F city', 'fl', '67890', 'nan', 'f100', 'General', 'Email', '20210101',
                     'Social Security^Casework', 'nan', 'nan', 'nan', 'r600',
                     'General', 'Email', '20210111', 'E', 'nan', r'..\documents\BlobExport\formletters\F.txt', 'nan',
                     'Casework']]
        self.assertEqual(result, expected, "Problem with test for appraisal, appraisal delete log")

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        csv_path = os.path.join('test_data', 'script', f"file_deletion_log_{today}.csv")
        result = csv_to_list(csv_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [r'..\documents\objects\333333.txt'.replace('..', input_directory),
                     '0.8', today, today, '09F83C9A1604F2DBCB8471DACCB99A49', 'Casework'],
                    [r'..\documents\indivletters\000003.txt'.replace('..', input_directory),
                     '3.5', today, today, '3E273CCDD4D24DBFCD55B519999BABC7', 'Casework'],
                    [r'..\documents\objects\111111.txt'.replace('..', input_directory),
                     '0.0', today, today, 'C53D3BB354B533DE159BB7C89E0433D5', 'Academy_Application'],
                    [r'..\documents\indivletters\000001.txt'.replace('..', input_directory),
                     '0.1', today, today, '21E65C7B733959A8B3E6071EB0748BF6', 'Academy_Application'],
                    [r'..\documents\objects\444444.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\objects\555555.txt'.replace('..', input_directory),
                     'nan', 'nan', 'nan', 'nan', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\indivletters\000005.txt'.replace('..', input_directory),
                     '1.2', today, today, 'EFBB58E35027F2382E2C58F22B895B7C', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for appraisal, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = ['archiving_correspondence.dat', 'B.txt', 'D.txt', 'F.txt', '000007.txt',
                    '222222.txt', '666666.txt', '777777.txt']
        self.assertEqual(result, expected, "Problem with test for appraisal, input_directory contents")

        # Tests the other script mode outputs were not made.
        output_directory = os.path.join('test_data', 'script')
        result = [os.path.exists(os.path.join(output_directory, 'archiving_correspondence_redacted.csv')),
                  os.path.exists(os.path.join(output_directory, '2021-2022.csv')),
                  os.path.exists(os.path.join(output_directory, '2023-2024.csv')),
                  os.path.exists(os.path.join(output_directory, 'usability_report_metadata.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_state.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_zip.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_in_date.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_in_doc.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_out_date.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_out_doc.csv')),
                  os.path.exists(os.path.join(output_directory, 'usability_report_matching.csv')),
                  os.path.exists(os.path.join(output_directory, 'usability_report_matching_details.csv')),
                  os.path.exists(os.path.join(output_directory, 'topics_report.csv'))]
        expected = [False, False, False, False, False, False, False, False, False, False, False, False, False]
        self.assertEqual(result, expected, "Problem with test for appraisal, other script mode outputs")

    def test_correct_preservation(self):
        """Test for when the script runs correctly and is in preservation mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'Preservation_Constituent_Mail_Export_copy'),
                        os.path.join('test_data', 'script', 'Preservation_Constituent_Mail_Export'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'Preservation_Constituent_Mail_Export')
        printed = subprocess.run(f"python {script_path} {input_directory} preservation",
                                 shell=True, capture_output=True, text=True)

        # Tests the printed statement.
        result = printed.stdout
        expected = "\nThe script is running in preservation mode.\nThe steps are TBD.\n"
        self.assertEqual(result, expected, "Problem with test for preservation, printed statement")

        # Tests the other script mode outputs were not made.
        output_directory = os.path.join('test_data', 'script')
        today = date.today().strftime('%Y-%m-%d')
        result = [os.path.exists(os.path.join(output_directory, '2021-2022.csv')),
                  os.path.exists(os.path.join(output_directory, '2023-2024.csv')),
                  os.path.exists(os.path.join(output_directory, 'archiving_correspondence_redacted.csv')),
                  os.path.exists(os.path.join(output_directory, f'file_deletion_log_{today}.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_state.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_zip.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_in_date.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_in_doc.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_out_date.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_out_doc.csv')),
                  os.path.exists(os.path.join(output_directory, 'topics_report.csv')),
                  os.path.exists(os.path.join(output_directory, 'usability_report_matching.csv')),
                  os.path.exists(os.path.join(output_directory, 'usability_report_matching_details.csv')),
                  os.path.exists(os.path.join(output_directory, 'usability_report_metadata.csv'))]
        expected = [False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        self.assertEqual(result, expected, "Problem with test for preservation, other script mode outputs")

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
