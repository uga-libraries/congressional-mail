"""
Tests for the function check_metadata_formatting(),
which finds all rows in a column that don't match the expected formatting,
saves them to a csv and returns the count.

All column tests include correct cells, formatting errors, and blank cells.
To simplify testing, only the columns with expected formatting are included and
columns that are not part of a test are blank.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_data_interchange_format import check_metadata_formatting
from test_script import csv_to_list


def make_df(rows_list):
    """Makes md_df for testing"""
    column_names = ['state_code', 'zip_code', 'date_in', 'date_out', 'reminder_date', 'update_date',
                    'communication_document_name']
    df = pd.DataFrame(rows_list, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the reports, if made by the test"""
        columns = ['communication_document_name', 'date_in', 'date_out', 'reminder_date', 'state_code',
                   'update_date', 'zip_code']
        for column in columns:
            report_path = os.path.join('test_data', f'metadata_formatting_errors_{column}.csv')
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_column_blank(self):
        """Test for a column that is entirely blank, which would be the same for any column"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['GA', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     ['GA', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     ['GA', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows_list)
        zip_mismatch = check_metadata_formatting('zip_code', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(zip_mismatch, 'column_blank', "Problem with test for column_blank, count")

        # Tests the report was not created.
        result = os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))
        self.assertEqual(result, False, "Problem with test for column_blank, report")

    def test_column_missing(self):
        """Test for a column that is missing, which would be the same for any column"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, '30601', np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, '30601', np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, '30601', np.nan, np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows_list)
        df.drop(columns=['zip_code'], axis=1, inplace=True)
        zip_mismatch = check_metadata_formatting('zip_code', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(zip_mismatch, 'column_missing', "Problem with test for column_missing, count")

        # Tests the report was not created.
        result = os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))
        self.assertEqual(result, False, "Problem with test for column_missing, report")

    def test_column_no_errors(self):
        """Test for a column with no formatting errors, which would be the same for any column"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, '30601', np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, '30601', np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, '30601', np.nan, np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows_list)
        zip_mismatch = check_metadata_formatting('zip_code', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(zip_mismatch, 0, "Problem with test for column_no_errors, count")

        # Tests the report was not created.
        result = os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))
        self.assertEqual(result, False, "Problem with test for column_no_errors, report")

    def test_communication_document_name(self):
        """Test for the communication_document_name column"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, '7'],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, '..\\documents\\objects\\1.txt'],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 'documents\\objects\\2.txt'],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 'objects\\3.txt'],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, '4.txt']]
        df = make_df(rows_list)
        cdm_mismatch = check_metadata_formatting('communication_document_name', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(cdm_mismatch, 4, "Problem with test for communication_document_name, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_communication_document_name.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'date_out', 'reminder_date', 'update_date',
                     'communication_document_name'],
                    ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', '7'],
                    ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'documents\\objects\\2.txt'],
                    ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'objects\\3.txt'],
                    ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', '4.txt']]
        self.assertEqual(result, expected, "Problem with test for communication_document_name, report")

    def test_date_in(self):
        """Test for the date_in column"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, np.nan, '2005', np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, '2005-01-02', np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, '20050304', np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, 'January 2005', np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows_list)
        date_in_mismatch = check_metadata_formatting('date_in', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(date_in_mismatch, 3, "Problem with test for date_in, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_date_in.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'date_out', 'reminder_date', 'update_date',
                     'communication_document_name'],
                    ['nan', 'nan', '2005', 'nan', 'nan', 'nan', 'nan'],
                    ['nan', 'nan', '2005-01-02', 'nan', 'nan', 'nan', 'nan'],
                    ['nan', 'nan', 'January 2005', 'nan', 'nan', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for date_in, report")

    def test_date_out(self):
        """Test for the date_out column"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, '20251201', np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, '2025/12/01', np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, '2025-12-01', np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows_list)
        date_out_mismatch = check_metadata_formatting('date_out', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(date_out_mismatch, 2, "Problem with test for date_out, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_date_out.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'date_out', 'reminder_date', 'update_date',
                     'communication_document_name'],
                    ['nan', 'nan', 'nan', '2025/12/01', 'nan', 'nan', 'nan'],
                    ['nan', 'nan', 'nan', '2025-12-01', 'nan', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for date_out, report")

    def test_reminder_date(self):
        """Test for the reminder_date column"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, np.nan, np.nan, np.nan, '20230101', np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, '20230102', np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, '20230103', np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, '2023', np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, '20230104', np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows_list)
        reminder_mismatch = check_metadata_formatting('reminder_date', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(reminder_mismatch, 1, "Problem with test for reminder_date, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_reminder_date.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'date_out', 'reminder_date', 'update_date',
                     'communication_document_name'],
                    ['nan', 'nan', 'nan', 'nan', '2023', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for reminder_date, report")

    def test_state_code(self):
        """Test for the state_code column"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['VA', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     ['ga', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     ['Georgia', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     ['X', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows_list)
        state_mismatch = check_metadata_formatting('state_code', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(state_mismatch, 3, "Problem with test for state_code, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_state_code.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'date_out', 'reminder_date', 'update_date',
                     'communication_document_name'],
                    ['ga', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan'],
                    ['Georgia', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan'],
                    ['X', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for state_code, report")

    def test_update_date(self):
        """Test for the update_date column"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, '202101212', np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, '20210102', np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, '20210103', np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, 'no date', np.nan]]
        df = make_df(rows_list)
        update_mismatch = check_metadata_formatting('update_date', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(update_mismatch, 2, "Problem with test for update_date, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_update_date.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'date_out', 'reminder_date', 'update_date',
                     'communication_document_name'],
                    ['nan', 'nan', 'nan', 'nan', 'nan', '202101212', 'nan'],
                    ['nan', 'nan', 'nan', 'nan', 'nan', 'no date', 'nan']]
        self.assertEqual(result, expected, "Problem with test for update_date, report")

    def test_zip_code(self):
        """Test for the zip_code column"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, '30601', np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, '30601 1234', np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, '30601-1234', np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, '3060', np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, 'XXXXX', np.nan, np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows_list)
        zip_mismatch = check_metadata_formatting('zip_code', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(zip_mismatch, 3, "Problem with test for zip_code, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))
        expected = [['state_code', 'zip_code', 'date_in', 'date_out', 'reminder_date', 'update_date',
                     'communication_document_name'],
                    ['nan', '30601 1234', 'nan', 'nan', 'nan', 'nan', 'nan'],
                    ['nan', '3060', 'nan', 'nan', 'nan', 'nan', 'nan'],
                    ['nan', 'XXXXX', 'nan', 'nan', 'nan', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for zip_code, report")


if __name__ == '__main__':
    unittest.main()
