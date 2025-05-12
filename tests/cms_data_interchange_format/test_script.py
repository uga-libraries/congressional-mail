"""
Tests for the script cms_data_interchange_format.py
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
                     f"file_deletion_log_{date.today().strftime('%Y-%m-%d')}.csv"]
        for filename in filenames:
            file_path = os.path.join('test_data', 'script', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Metadata split by congress year, in own directory.
        folder_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year')
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

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
        expected = ('\nThe script is running in access mode.\nIt will remove rows for deleted letters, '
                    'save the merged metadata tables without columns with PII,'
                    ' and make copies of the metadata split by congress year\n')
        self.assertEqual(result, expected, "Problem with test for access, printed statement")

        # Tests the contents of the appraisal_check_log.csv.
        csv_path = os.path.join('test_data', 'script', 'appraisal_check_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag',
                     'Appraisal_Category'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', '11111', 'CON', '1', 'main', 'legal_con.docx', 'BLANK', 'note text 1',
                     'COR', '11111', 'LEGAL CASE', 'Y', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for access, appraisal_check_log.csv")

        # Tests the contents of the appraisal_delete_log.csv.
        csv_path = os.path.join('test_data', 'script', 'appraisal_delete_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag',
                     'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for access, appraisal_delete_log.csv")

        # Tests the contents of archiving_correspondence_redacted.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_redacted.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', '11111', 'CON', '1', 'main', 'legal_con.docx', 'BLANK',
                     'COR', '11111', 'LEGAL CASE', 'Y'],
                    ['Caseyville', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK',
                     '20220220', 'EMAIL', '22222', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK',
                     'COR', '22222', 'MINWAGE', 'Y'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK',
                     '20220330', 'EMAIL', '33333', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'EMAIL', '33333', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', '20230330', '20230330', 'BLANK',
                     '20230330', 'EMAIL', '33333', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y']]
        self.assertEqual(result, expected, "Problem with test for access, archiving_correspondence_redacted.csv")

        # Tests the contents of 2021-2022.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year', '2021-2022.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', '11111', 'CON', '1', 'main', 'legal_con.docx', 'BLANK',
                     'COR', '11111', 'LEGAL CASE', 'Y'],
                    ['Caseyville', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK',
                     '20220220', 'EMAIL', '22222', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK',
                     'COR', '22222', 'MINWAGE', 'Y'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK',
                     '20220330', 'EMAIL', '33333', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y']]
        self.assertEqual(result, expected, "Problem with test for access, 2021-2022")

        # Tests the contents of 2023-2024.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year', '2023-2024.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', '20230330', '20230330', 'BLANK',
                     '20230330', 'EMAIL', '33333', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y']]
        self.assertEqual(result, expected, "Problem with test for access, 2023-2024")

        # Tests the contents of undated.csv.
        csv_path = os.path.join('test_data', 'script', 'archiving_correspondence_by_congress_year', 'undated.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'EMAIL', '33333', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK',
                     'COR', '33333', 'RIGHTS', 'Y']]
        self.assertEqual(result, expected, "Problem with test for access, undated")

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
        self.assertEqual(result, expected, "Problem with test for appraisal, printed statement")

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
        self.assertEqual(result, expected, "Problem with test for appraisal, appraisal_check_log.csv")

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
        self.assertEqual(result, expected, "Problem with test for appraisal, appraisal_delete_log.csv")

        # Tests the contents of the file deletion log.
        today = date.today().strftime('%Y-%m-%d')
        csv_path = os.path.join('test_data', 'script', f"file_deletion_log_{today}.csv")
        result = csv_to_list(csv_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [os.path.join('test_data', 'script', 'appraisal_copy', 'documents', 'in-email', '2.txt'),
                     '0.1', today, today, 'BFC30C1C407A46A42D322B493E783D8A', 'Recommendation'],
                    [os.path.join('test_data', 'script', 'appraisal_copy', 'documents', 'in-email', '3.txt'),
                     '0.2', today, today, '3372E0A98AEBE7DB66A368010DB78AF3', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for appraisal, file_delete_log.csv")

        # Tests the contents of the input_directory, that all files that should be deleted are gone.
        result = files_in_dir(input_directory)
        expected = ['1B.out', '2A.out', '2B.out', '2C.out', '2D.out', '8A.out',
                    '1.txt', 'case_name.txt', '1001.txt', '1002.txt']
        self.assertEqual(result, expected, "Problem with test for appraisal, input_directory contents")

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
        self.assertEqual(result, expected, "Problem with test for error argument, printed error")

    # def test_accession(self):
    #     """Test for when the script runs correctly in accession mode."""
    #     # Runs the script.
    #     script_path = os.path.join(os.getcwd(), '..', '..', 'cms_data_interchange_format.py')
    #     input_directory = os.path.join('test_data', 'script')
    #     subprocess.run(f"python {script_path} {input_directory} preservation", shell=True)
    #
    #     # Tests the contents of case_remains_log.csv.
    #     csv_path = os.path.join('test_data', 'case_remains_log.csv')
    #     result = csv_to_list(csv_path)
    #     expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
    #                  'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
    #                  '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location'],
    #                 ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
    #                  '20210110', 'LETTER', 'LEGAL CASE', 'CON', '1', 'main', 'legal_con.docx', 'BLANK'],
    #                 ['Caseyville', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK',
    #                  '20220220', 'EMAIL', 'MINWAGE', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK']]
    #     self.assertEqual(result, expected, "Problem with test for preservation, case_remains_log.csv")

    def test_preservation(self):
        """Test for when the script runs correctly in preservation mode."""
        # Runs the script.
        # Since just testing printing right now, using a folder for input_directory that is not an export.
        script_path = os.path.join(os.getcwd(), '..', '..', 'cms_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script', 'preservation')
        output = subprocess.run(f"python {script_path} {input_directory} preservation",
                                shell=True, capture_output=True, text=True)

        # Tests the print statement.
        result = output.stdout
        expected = '\nThe script is running in preservation mode.\nThe steps are TBD.\n'
        self.assertEqual(result, expected, "Problem with test for preservation, printed statement")


if __name__ == '__main__':
    unittest.main()

