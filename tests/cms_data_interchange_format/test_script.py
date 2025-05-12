"""
Tests for the script cms_data_interchange_format.py
"""
import os
import pandas as pd
import subprocess
import unittest


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('BLANK')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Remove script outputs, if they were made"""
        filenames = ['Access_Copy.csv', '2021-2022.csv', '2023-2024.csv', 'undated.csv', 'case_remains_log.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_access(self):
        """Test for when the script runs correctly in access mode."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'cms_data_interchange_format.py')
        input_directory = os.path.join('test_data', 'script')
        subprocess.run(f"python {script_path} {input_directory} access", shell=True)

        # Tests the contents of case_remains_log.csv.
        csv_path = os.path.join('test_data', 'case_remains_log.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', 'LEGAL CASE', 'CON', '1', 'main', 'legal_con.docx', 'BLANK'],
                    ['Caseyville', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK',
                     '20220220', 'EMAIL', 'MINWAGE', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for access, case_remains_log.csv")

        # Tests the contents of Access_Copy.csv.
        csv_path = os.path.join('test_data', 'Access_Copy.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', 'LEGAL CASE', 'CON', '1', 'main', 'legal_con.docx', 'BLANK'],
                    ['Caseyville', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK',
                     '20220220', 'EMAIL', 'MINWAGE', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK',
                     '20220330', 'EMAIL', 'RIGHTS', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'EMAIL', 'RIGHTS', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', '20230330', '20230330', 'BLANK',
                     '20230330', 'EMAIL', 'RIGHTS', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for correct, Access_Copy.csv")

        # Tests the contents of 2021-2022.csv.
        csv_path = os.path.join('test_data', '2021-2022.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20210110', '20210110', 'BLANK',
                     '20210110', 'LETTER', 'LEGAL CASE', 'CON', '1', 'main', 'legal_con.docx', 'BLANK'],
                    ['Caseyville', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK',
                     '20220220', 'EMAIL', 'MINWAGE', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK',
                     '20220330', 'EMAIL', 'RIGHTS', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for correct, 2021-2022")

        # Tests the contents of 2023-2024.csv.
        csv_path = os.path.join('test_data', '2023-2024.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', '20230330', '20230330', 'BLANK',
                     '20230330', 'EMAIL', 'RIGHTS', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for correct, 2023-2024")

        # Tests the contents of undated.csv.
        csv_path = os.path.join('test_data', 'undated.csv')
        result = csv_to_list(csv_path)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location'],
                    ['City One', 'GA', '30001', 'USA', 'EMAIL', 'Staffer_3', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'EMAIL', 'RIGHTS', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for correct, undated")

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

