from datetime import date
import os
import pandas as pd
import shutil
import subprocess
import unittest


def csv_to_list(csv_path, sort=False):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison
    with the option to sort for the report with inconsistent row order"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('BLANK')
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


def make_dir_list(dir_path):
    """Make a list of the files in the folder created by the function to compare to expected results"""
    contents_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            contents_list.append(os.path.join(root, file))
    return contents_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Remove script outputs and copies of test data, if they were made"""
        # These same folder name is used for the copied input, regardless of mode, to simplify deletion.
        folder_path = os.path.join('test_data', 'script', 'output_dir')
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

    def test_correct_access(self):
        """Test for when the script runs correctly and is in access mode."""
        # Makes a copy of the test data in the repo, to simplify deleting script outputs.
        shutil.copytree(os.path.join('test_data', 'script', 'Access'),
                        os.path.join('test_data', 'script', 'output_dir'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join(os.getcwd(), 'test_data', 'script', 'output_dir', 'Constituent_Mail_Export')
        printed = subprocess.run(f"python {script_path} {input_directory} access",
                                 shell=True, capture_output=True, text=True)

        # Tests the printed statement.
        result = printed.stdout
        expected = ("\nThe script is running in access mode.\nIt will remove rows for deleted or restricted letters "
                    "and columns with PII, make copies of the metadata split by calendar year, and make a copy "
                    "of the letters to and from constituents organized by topic\n")
        self.assertEqual(expected, result, "Problem with test for access, printed statement")

        # Tests the contents of the appraisal check log.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for access, appraisal check log")

        # Tests the contents of the appraisal delete log.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['Ms.', 'Diane', 'D.', 'Dudly', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 D St', 'BLANK', 'BLANK', 
                     'BLANK', 'D city', 'DE', '45678', 'BLANK', 'd100', 'General', 'Email', '20210101', 'Resumes',
                     'BLANK', r'..\documents\BlobExport\objects\444444.txt', 'BLANK', 'r400', 'General', 'Email',
                     '20210111', 'D', 'academy nomination', r'..\documents\BlobExport\indivletters\000004.txt', 'BLANK',
                     'Academy_Application|Job_Application'],
                    ['Ms.', 'Emma', 'E.', 'Evans', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '567 E St', 'BLANK', 'BLANK', 
                     'BLANK', 'E city', 'ME', '56789', 'BLANK', 'e100', 'General', 'Email', '20210101',
                     'Casework Issues', 'BLANK', r'..\documents\BlobExport\objects\555555.txt', 'BLANK', 'r500',
                     'General', 'Email', '20210111', 'E', 'BLANK', r'..\documents\BlobExport\formletters\B.txt',
                     'BLANK', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for access, appraisal delete log")

        # Tests the contents of archiving_correspondence_redacted.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'archiving_correspondence_redacted.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_document_name', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name'],
                    ['A city', 'AL', '12345', 'BLANK', 'a100', 'General', 'Email', '20210101', 'A1',
                     r'..\documents\BlobExport\objects\111111.txt', 'r100', 'General', 'Email', '20210111',
                     'A', r'..\documents\BlobExport\indivletters\000001.txt'],
                    ['A city', 'AL', '12345', 'BLANK', 'a100', 'General', 'Email', '20210101', 'A1',
                     r'..\documents\BlobExport\objects\111111_add.txt', 'r100', 'General', 'Email', '20210111',
                     'A', r'..\documents\BlobExport\indivletters\000001.txt'],
                    ['B city', 'WY', '23456', 'BLANK', 'b200', 'General', 'Email', '20230202', 'B1^B2',
                     r'..\documents\BlobExport\objects\222222.txt', 'r200', 'General', 'Email', '20230212',
                     'B1^B2', r'..\documents\BlobExport\indivletters\000002.txt'],
                    ['C city', 'CO', '34567', 'BLANK', 'c300', 'General', 'Letter', '20240303', 'A1',
                     r'..\documents\BlobExport\objects\333333.txt', 'r300', 'General', 'Email', '20240313',
                     'A', r'..\documents\BlobExport\formletters\A.txt'],
                    ['C city', 'CO', '34567', 'BLANK', 'c300', 'General', 'Letter', '20240303', 'A1',
                     r'..\documents\BlobExport\objects\333333.txt', 'r300', 'General', 'Email', '20240313',
                     'A', r'..\documents\BlobExport\indivletters\000003.txt'],
                    ['F city', 'FL', '10234', 'BLANK', 'f600', 'General', 'Email', '20230202', 'B1',
                     r'..\documents\BlobExport\objects\xxxxxx.txt', 'r600', 'General', 'Email', '20230212',
                     'B', r'..\documents\BlobExport\indivletters\00000Z.txt']]
        self.assertEqual(expected, result, "Problem with test for access, archiving_correspondence_redacted.csv")

        # Tests the contents of 2021.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'correspondence_metadata_by_year', '2021.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_document_name', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_document_name'],
                    ['A city', 'AL', '12345', 'BLANK', 'a100', 'General', 'Email', '20210101', 'A1',
                     r'..\documents\BlobExport\objects\111111.txt', 'r100', 'General', 'Email', '20210111',
                     'A', r'..\documents\BlobExport\indivletters\000001.txt'],
                    ['A city', 'AL', '12345', 'BLANK', 'a100', 'General', 'Email', '20210101', 'A1',
                     r'..\documents\BlobExport\objects\111111_add.txt', 'r100', 'General', 'Email', '20210111',
                     'A', r'..\documents\BlobExport\indivletters\000001.txt']]
        self.assertEqual(expected, result, "Problem with test for access, 2021.csv")

        # Tests the contents of 2023.csv.
        csv_path = os.path.join(os.getcwd(), 'test_data', 'script', 'output_dir', 'correspondence_metadata_by_year', '2023.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_document_name', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_document_name'],
                    ['B city', 'WY', '23456', 'BLANK', 'b200', 'General', 'Email', '20230202', 'B1^B2',
                     r'..\documents\BlobExport\objects\222222.txt', 'r200', 'General', 'Email', '20230212',
                     'B1^B2', r'..\documents\BlobExport\indivletters\000002.txt'],
                    ['F city', 'FL', '10234', 'BLANK', 'f600', 'General', 'Email', '20230202', 'B1',
                     r'..\documents\BlobExport\objects\xxxxxx.txt', 'r600', 'General', 'Email', '20230212',
                     'B', r'..\documents\BlobExport\indivletters\00000Z.txt']]
        self.assertEqual(expected, result, "Problem with test for access, 2023.csv")

        # Tests the contents of 2024.csv.
        csv_path = os.path.join(os.getcwd(), 'test_data', 'script', 'output_dir', 'correspondence_metadata_by_year', '2024.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_document_name', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_document_name'],
                    ['C city', 'CO', '34567', 'BLANK', 'c300', 'General', 'Letter', '20240303', 'A1',
                     r'..\documents\BlobExport\objects\333333.txt', 'r300', 'General', 'Email', '20240313',
                     'A', r'..\documents\BlobExport\formletters\A.txt'],
                    ['C city', 'CO', '34567', 'BLANK', 'c300', 'General', 'Letter', '20240303', 'A1',
                     r'..\documents\BlobExport\objects\333333.txt', 'r300', 'General', 'Email', '20240313',
                     'A', r'..\documents\BlobExport\indivletters\000003.txt']]
        self.assertEqual(expected, result, "Problem with test for access, 2024.csv")

        # Tests that no undated.csv was made.
        result = os.path.exists(os.path.join(os.getcwd(), 'test_data', 'script', 'output_dir'
                                             'correspondence_metadata_by_year', 'undated.csv'))
        self.assertEqual(False, result, "Problem with test for access, undated.csv")

        # Tests that Correspondence_by_Topic has the expected files.
        by_topic = os.path.join(os.getcwd(), 'test_data', 'script', 'output_dir', 'Correspondence_by_Topic')
        result = make_dir_list(by_topic)
        expected = [os.path.join(by_topic, 'A', 'to_constituents', '000001.txt'),
                    os.path.join(by_topic, 'A', 'to_constituents', '000003.txt'),
                    os.path.join(by_topic, 'A', 'to_constituents', 'A.txt'),
                    os.path.join(by_topic, 'A1', 'from_constituents', '111111.txt'),
                    os.path.join(by_topic, 'A1', 'from_constituents', '111111_add.txt'),
                    os.path.join(by_topic, 'A1', 'from_constituents', '333333.txt'),
                    os.path.join(by_topic, 'B1', 'from_constituents', '222222.txt'),
                    os.path.join(by_topic, 'B1', 'to_constituents', '000002.txt'),
                    os.path.join(by_topic, 'B2', 'from_constituents', '222222.txt'),
                    os.path.join(by_topic, 'B2', 'to_constituents', '000002.txt'),]
        self.assertEqual(expected, result, "Problem with test for access, Correspondence_by_Topic")

        # Tests the contents of topics_sort_file_not_found.csv
        csv_path = os.path.join(os.getcwd(), 'test_data', 'script', 'output_dir', 'topics_sort_file_not_found.csv')
        result = csv_to_list(csv_path)
        expected = [['B1', r'..\documents\BlobExport\objects\xxxxxx.txt'],
                    ['B', r'..\documents\BlobExport\indivletters\00000Z.txt']]
        self.assertEqual(expected, result, "Problem with test for access, topics_sort_file_not_found.csv")

    def test_correct_accession(self):
        """Test for when the script runs correctly and is in accession mode."""
        # Makes a copy of the test data in the repo, to simplify deleting script outputs.
        shutil.copytree(os.path.join('test_data', 'script', 'Accession'),
                        os.path.join('test_data', 'script', 'output_dir'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'output_dir', 'Constituent_Mail_Export')
        printed = subprocess.run(f"python {script_path} {input_directory} accession",
                                 shell=True, capture_output=True, text=True)

        # Tests the printed statement.
        result = printed.stdout
        expected = ("\nThe script is running in accession mode.\n"
                    "It will produce usability and appraisal reports and not change the export.\n")
        self.assertEqual(expected, result, "Problem with test for accession, printed statement")

        # Tests the contents of the appraisal check log.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['Ms.', 'Gretel', 'G.', 'Green', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 G St', 'BLANK', 'BLANK', 
                     'BLANK', 'G city', 'GA', '78901', 'BLANK', 'g100', 'General', 'Email', '20210101', 'E', 'BLANK',
                     r'..\documents\BlobExport\objects\777777.txt', 'BLANK', 'r700', 'General', 'Email', '20210111',
                     'BLANK', 'BLANK', r'..\documents\BlobExport\indivletters\000007.txt', 'Court case', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for accession, appraisal check log")

        # Tests the contents of the appraisal delete log.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['Mr.', 'Clive', 'C.', 'Cooper', 'Jr.', 'BLANK', 'CEO', 'Company', 'Attn: C', 'Division', 'POBox',
                     '345 C St', 'C city', 'CO', '34567', 'BLANK', 'c300', 'General', 'Letter', '20240303', 'Misc',
                     'Maybe case work', r'..\documents\BlobExport\objects\333333.txt', 'BLANK', 'r300', 'General',
                     'Email', '2024-03-13', 'B1^B2', 'BLANK', r'..\documents\BlobExport\indivletters\000003.txt',
                     'BLANK', 'Casework'],
                    ['Ms.', 'Ann', 'A.', 'Anderson', 'BLANK', 'MD', 'BLANK', 'BLANK', '123 A St', 'BLANK', 'BLANK',
                     'BLANK', 'A city', 'AL', '12345', 'BLANK', 'a100', 'General', 'Email', '20210101', 'Misc',
                     'academy nomination', r'..\documents\BlobExport\objects\111111.txt', 'BLANK', 'r100', 'General',
                     'Email', '20210111', 'BLANK', 'BLANK', r'..\documents\BlobExport\indivletters\000001.txt',
                     'BLANK', 'Academy_Application'],
                    ['Ms.', 'Diane', 'D.', 'Dudly', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 D St', 'BLANK', 'BLANK',
                     'BLANK', 'D city', 'DEL', '45678', 'BLANK', 'd100', 'General', 'Email', '20210101', 'Casework',
                     'BLANK', r'..\documents\BlobExport\objects\444444.txt', 'BLANK', 'r400', 'General', 'Email',
                     '20210111', 'Recommendations', 'BLANK', r'..\documents\BlobExport\formletters\D.txt', 'BLANK',
                     'Casework|Recommendation'],
                    ['Ms.', 'Emma', 'E.', 'Evans', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '567 E St', 'BLANK', 'BLANK',
                     'BLANK', 'E city', 'ME', '56789', 'BLANK', 'e100', 'General', 'Email', '20210101', 
                     'Recommendations', 'BLANK', r'..\documents\BlobExport\objects\555555.txt', 'BLANK', 'r500', 
                     'General', 'Email', '20210111', 'E', 'BLANK', r'..\documents\BlobExport\indivletters\000005.txt', 
                     'BLANK', 'Recommendation'],
                    ['Ms.', 'Fiona', 'F.', 'Fowler', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '678 F St', 'BLANK', 'BLANK',
                     'BLANK', 'F city', 'fl', '67890', 'BLANK', 'f100', 'General', 'Email', '20210101',
                     'Social Security^Casework', 'BLANK', 'BLANK', 'BLANK', 'r600', 'General', 'Email', '20210111',
                     'E', 'BLANK', r'..\documents\BlobExport\formletters\F.txt', 'BLANK', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for accession, appraisal delete log")

        # Tests the contents of metadata_formatting_errors_state.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'metadata_formatting_errors_state.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Ms.', 'Diane', 'D.', 'Dudly', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 D St', 'BLANK', 'BLANK', 
                     'BLANK', 'D city', 'DEL', '45678', 'BLANK', 'd100', 'General', 'Email', '20210101', 'Casework', 
                     'BLANK', r'..\documents\BlobExport\objects\444444.txt', 'BLANK', 'r400', 'General', 'Email', 
                     '20210111', 'Recommendations', 'BLANK', r'..\documents\BlobExport\formletters\D.txt', 'BLANK'],
                    ['Ms.', 'Fiona', 'F.', 'Fowler', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '678 F St', 'BLANK', 'BLANK', 
                     'BLANK', 'F city', 'fl', '67890', 'BLANK', 'f100', 'General', 'Email', '20210101',
                     'Social Security^Casework', 'BLANK', 'BLANK', 'BLANK', 'r600', 'General', 'Email', '20210111', 
                     'E', 'BLANK', r'..\documents\BlobExport\formletters\F.txt', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for accession, metadata_formatting_errors_state.csv")

        # Tests the contents of metadata_formatting_errors_out_date.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'metadata_formatting_errors_out_date.csv')
        result = csv_to_list(csv_path)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Mr.', 'Clive', 'C.', 'Cooper', 'Jr.', 'BLANK', 'CEO', 'Company', 'Attn: C', 'Division', 'POBox',
                     '345 C St', 'C city', 'CO', '34567', 'BLANK', 'c300', 'General', 'Letter', '20240303', 'Misc',
                     'Maybe case work', r'..\documents\BlobExport\objects\333333.txt', 'BLANK', 'r300', 'General',
                     'Email', '2024-03-13', 'B1^B2', 'BLANK', r'..\documents\BlobExport\indivletters\000003.txt', 
                     'BLANK']]
        self.assertEqual(expected, result, "Problem with test for accession, metadata_formatting_errors_out_date.csv")

        # Tests the other metadata formatting reports were not made.
        output_directory = os.path.join('test_data', 'script', 'output_dir')
        result = [os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_zip.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_in_date.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_in_doc.csv')),
                  os.path.exists(os.path.join(output_directory, 'metadata_formatting_errors_out_doc.csv'))]
        expected = [False, False, False, False]
        self.assertEqual(expected, result, "Problem with test for accession, other metadata formatting reports")

        # Tests the contents of topics_report.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'topics_report.csv')
        result = csv_to_list(csv_path)
        expected = [['Topic', 'In_Topic_Count', 'Out_Topic_Count', 'Total'],
                    ['B1^B2', '1', '2', '3'],
                    ['BLANK', '0', '2', '2'],
                    ['Casework', '1', '0', '1'],
                    ['E', '1', '2', '3'],
                    ['Misc', '2', '0', '2'],
                    ['Recommendations', '1', '1', '2'],
                    ['Social Security^Casework', '1', '0', '1']]
        self.assertEqual(expected, result, "Problem with test for accession, topics_report.csv")

        # Tests the contents of usability_report_matching.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'usability_report_matching.csv')
        result = csv_to_list(csv_path)
        expected = [['Category', 'Row/File_Count', 'Row_Percent'],
                    ['Match', '10', '71%'],
                    ['Metadata_Only', '3', '21%'],
                    ['Metadata_Blank', '1', '7%'],
                    ['Directory_Only', '2', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for accession, usability_report_matching.csv")

        # Tests the contents of usability_report_matching_details.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'usability_report_matching_details.csv')
        result = csv_to_list(csv_path, sort=True)
        expected = [['Category', 'Path'],
                    ['Directory Only', r'test_data\script\output_dir\constituent_mail_export\documents\formletters\b.txt'],
                    ['Directory Only', r'test_data\script\output_dir\constituent_mail_export\documents\objects\666666.txt'],
                    ['Metadata Only', r'test_data\script\output_dir\constituent_mail_export\documents\objects\444444.txt'],
                    ['Metadata Only', r'test_data\script\output_dir\constituent_mail_export\documents\objects\555555.txt'],
                    ['Metadata Only', r'test_data\script\output_dir\constituent_mail_export\documents\objects\b.txt']]
        self.assertEqual(expected, result, "Problem with test for accession, usability_report_matching_details.csv")

        # Tests the contents of usability_report_metadata.csv.
        csv_path = os.path.join('test_data', 'script', 'output_dir', 'usability_report_metadata.csv')
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
        self.assertEqual(expected, result, "Problem with test for accession, usability_report_metadata.csv")

    def test_correct_appraisal(self):
        """Test for when the script runs correctly and is in appraisal mode."""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'script', 'Appraisal'),
                        os.path.join('test_data', 'script', 'output_dir'))

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'output_dir', 'Constituent_Mail_Export')
        printed = subprocess.run(f"python {script_path} {input_directory} appraisal",
                                 shell=True, capture_output=True, text=True)

        # Tests the printed statement.
        result = printed.stdout
        expected = ("\nThe script is running in appraisal mode.\n"
                    "It will delete letters due to appraisal and make a report of metadata to review for restrictions,"
                    "but not change the metadata file.\n")
        self.assertEqual(expected, result, "Problem with test for appraisal, printed statement")

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        csv_path = os.path.join('test_data', 'script', 'output_dir', f"file_deletion_log_{today}.csv")
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
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\objects\555555.txt'.replace('..', input_directory),
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Cannot delete: FileNotFoundError'],
                    [r'..\documents\indivletters\000005.txt'.replace('..', input_directory),
                     '1.2', today, today, 'EFBB58E35027F2382E2C58F22B895B7C', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for appraisal, file deletion log")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = ['archiving_correspondence.dat', 'B.txt', 'D.txt', 'F.txt', '000007.txt',
                    '222222.txt', '666666.txt', '777777.txt']
        self.assertEqual(expected, result, "Problem with test for appraisal, input_directory contents")

        # Tests the contents of restriction_review.csv
        result = csv_to_list(os.path.join('test_data', 'script', 'output_dir', 'restriction_review.csv'))
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1',
                     'addr2', 'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method',
                     'in_date', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type',
                     'out_method', 'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin',
                     'in_topic_split', 'out_topic_split'],
                    ['Mx.', 'Harry', 'H.', 'Hills', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '111 H St', 'BLANK',
                     'BLANK', 'BLANK', 'H city', 'HI', '11111', 'BLANK', 'h100', 'General', 'Email', '20210101',
                     'refugee', 'note', r'..\documents\BlobExport\objects\888888.txt', 'fill', 'r800', 'General',
                     'Email', '20210111', 'BLANK', 'note', r'..\documents\BlobExport\formletters\H.txt', 'fill',
                     'refugee', 'BLANK'],
                    ['Mx.', 'Ionia', 'I.', 'Invern', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '222 I St', 'BLANK',
                     'BLANK', 'BLANK', 'I city', 'IA', '22222', 'BLANK', 'i100', 'General', 'Email', '20210101',
                     'Admin', 'note', r'..\documents\BlobExport\objects\999999.txt', 'fill', 'r900', 'General',
                     'Email', '20210111', 'citizenship', 'note', r'..\documents\BlobExport\formletters\I.txt',
                     'fill', 'Admin', 'citizenship'],
                    ['Mx.', 'Janey', 'J.', 'James', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '333 J St', 'BLANK',
                     'BLANK', 'BLANK', 'J city', 'GA', '33333', 'BLANK', 'j100', 'General', 'Email', '20210101',
                     'immigrant', 'note', r'..\documents\BlobExport\objects\101010.txt', 'fill', 'r110', 'General',
                     'Email', '20210111', 'citizen^citizenship', 'note', r'..\documents\BlobExport\formletters\J.txt',
                     'fill', 'immigrant', 'citizen'],
                    ['Mx.', 'Janey', 'J.', 'James', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '333 J St', 'BLANK',
                     'BLANK', 'BLANK', 'J city', 'GA', '33333', 'BLANK', 'j100', 'General', 'Email', '20210101',
                     'immigrant', 'note', r'..\documents\BlobExport\objects\101010.txt', 'fill', 'r110', 'General',
                     'Email', '20210111', 'citizen^citizenship', 'note', r'..\documents\BlobExport\formletters\J.txt',
                     'fill', 'immigrant', 'citizenship']]
        self.assertEqual(expected, result, "Problem with test for appraisal, restriction_review.csv")

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
        self.assertEqual(expected, result, "Problem with test for error argument, printed error")

    def test_error_appraisal_no_delete(self):
        """Test for when the script exits due to a missing appraisal_delete_log."""
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        input_directory = os.path.join('test_data', 'script', 'Incomplete_Export')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path} {input_directory} appraisal",
                           shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script and tests that it prints the correct error.
        output = subprocess.run(f"python {script_path} {input_directory} appraisal", shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = ("\r\nThe script is running in appraisal mode.\r\n"
                    "It will delete letters due to appraisal and make a report of metadata to review for restrictions,"
                    "but not change the metadata file.\r\n"
                    "No appraisal_delete_log.csv in the output directory. Cannot do appraisal without it.\r\n")
        self.assertEqual(expected, result, "Problem with test for error argument, printed error")


if __name__ == '__main__':
    unittest.main()
