"""
Tests for the function check_metadata_usability(),
which tests the usability of the metadata and generates a report of the results.
To simply testing, column values are letters when the cell content formatting isn't important for the test.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_data_interchange_format import check_metadata_usability
from test_script import csv_to_list


def make_df(rows_list):
    """Makes md_df for testing. In production, this is made by reading the export csv.
    This can only be used for making test input with all the columns present.
    """
    column_names = ['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                    'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                    'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                    'file_name']
    df = pd.DataFrame(rows_list, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the reports, if made by the test"""
        reports = ['metadata_formatting_errors_in_date.csv', 'metadata_formatting_errors_in_document_name.csv',
                   'metadata_formatting_errors_out_date.csv', 'metadata_formatting_errors_out_document_name.csv',
                   'metadata_formatting_errors_state_code.csv', 'metadata_formatting_errors_zip_code.csv',
                   'usability_report_metadata.csv']
        for report in reports:
            report_path = os.path.join('test_data', report)
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_all_correct(self):
        """Test for when all aspects of column testing are fully correct, including no blanks"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['a', 'GA', '11111', 'd', 'e', 'f', 'g', '20010101', '20010102', '20010103', '20010104',
                      'l', 'm', 'n', '..\\documents\\file1.txt', 'p', 'q', 'r'],
                     ['a', 'GA', '22222', 'd', 'e', 'f', 'g', '20020101', '20020102', '20020103', '20020104',
                      'l', 'm', 'n', '..\\documents\\file2.txt', 'p', 'q', 'r'],
                     ['a', 'GA', '33333', 'd', 'e', 'f', 'g', '20030101', '20030102', '20030103', '20030104',
                     'l', 'm', 'n', '..\\documents\\file3.txt', 'p', 'q', 'r']]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '0', '0.0', 'uncheckable'],
                    ['state_code', 'True', '0', '0.0', '0'],
                    ['zip_code', 'True', '0', '0.0', '0'],
                    ['country', 'True', '0', '0.0', 'uncheckable'],
                    ['communication_type', 'True', '0', '0.0', 'uncheckable'],
                    ['approved_by', 'True', '0', '0.0', 'uncheckable'],
                    ['status', 'True', '0', '0.0', 'uncheckable'],
                    ['date_in', 'True', '0', '0.0', '0'],
                    ['date_out', 'True', '0', '0.0', '0'],
                    ['reminder_date', 'True', '0', '0.0', '0'],
                    ['update_date', 'True', '0', '0.0', '0'],
                    ['response_type', 'True', '0', '0.0', 'uncheckable'],
                    ['group_name', 'True', '0', '0.0', 'uncheckable'],
                    ['document_type', 'True', '0', '0.0', 'uncheckable'],
                    ['communication_document_name', 'True', '0', '0.0', '0'],
                    ['communication_document_id', 'True', '0', '0.0', 'uncheckable'],
                    ['file_location', 'True', '0', '0.0', 'uncheckable'],
                    ['file_name', 'True', '0', '0.0', 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for all correct")

    def test_blank(self):
        """Test for when every row in is blank"""
        # TODO test fails because not string, which breaks function
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                      np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                      np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '2', '100.0', 'uncheckable'],
                    ['state_code', 'True', '2', '100.0', '0'],
                    ['zip_code', 'True', '2', '100.0', '0'],
                    ['country', 'True', '2', '100.0', 'uncheckable'],
                    ['communication_type', 'True', '2', '100.0', 'uncheckable'],
                    ['approved_by', 'True', '2', '100.0', 'uncheckable'],
                    ['status', 'True', '2', '100.0', 'uncheckable'],
                    ['date_in', 'True', '2', '100.0', '0'],
                    ['date_out', 'True', '2', '100.0', '0'],
                    ['reminder_date', 'True', '2', '100.0', '0'],
                    ['update_date', 'True', '2', '100.0', '0'],
                    ['response_type', 'True', '2', '100.0', 'uncheckable'],
                    ['group_name', 'True', '2', '100.0', 'uncheckable'],
                    ['document_type', 'True', '2', '100.0', 'uncheckable'],
                    ['communication_document_name', 'True', '2', '100.0', '0'],
                    ['communication_document_id', 'True', '2', '100.0', 'uncheckable'],
                    ['file_location', 'True', '2', '100.0', 'uncheckable'],
                    ['file_name', 'True', '2', '100.0', 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for blank")

    def test_blank_partial(self):
        """Test for when some rows of each column have blanks but no columns are all blank"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, 'GA', '11111', np.nan, 'e', 'f', np.nan, np.nan, '20010102', '20010103', '20010104',
                      np.nan, np.nan, 'n', '..\\documents\\file1.txt', np.nan, 'q', 'r'],
                     ['a', np.nan, '22222', np.nan, np.nan, np.nan, 'g', '20020101', np.nan, np.nan, '20020104',
                      np.nan, np.nan, np.nan, np.nan, 'p', np.nan, 'r'],
                     ['a', 'GA', np.nan, 'd', np.nan, np.nan, np.nan, '20030101', '20030102', '20030103', np.nan,
                      'l', 'm', np.nan, np.nan, 'p',  'q', np.nan]]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '1', '33.33', 'uncheckable'],
                    ['state_code', 'True', '1', '33.33', '0'],
                    ['zip_code', 'True', '1', '33.33', '0'],
                    ['country', 'True', '2', '66.67', 'uncheckable'],
                    ['communication_type', 'True', '2', '66.67', 'uncheckable'],
                    ['approved_by', 'True', '2', '66.67', 'uncheckable'],
                    ['status', 'True', '2', '66.67', 'uncheckable'],
                    ['date_in', 'True', '1', '33.33', '0'],
                    ['date_out', 'True', '1', '33.33', '0'],
                    ['reminder_date', 'True', '1', '33.33', '0'],
                    ['update_date', 'True', '1', '33.33', '0'],
                    ['response_type', 'True', '2', '66.67', 'uncheckable'],
                    ['group_name', 'True', '2', '66.67', 'uncheckable'],
                    ['document_type', 'True', '2', '66.67', 'uncheckable'],
                    ['communication_document_name', 'True', '2', '66.67', '0'],
                    ['communication_document_id', 'True', '1', '33.33', 'uncheckable'],
                    ['file_location', 'True', '1', '33.33', 'uncheckable'],
                    ['file_name', 'True', '1', '33.33', 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for blank, partial")

    def test_columns_extra(self):
        """Test for when there are additional columns beyond what is expected"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['a', 'GA', '11111', 'd', 'e', 'f', 'g', '20010101', '20010102', '20010103', '20010104',
                      'l', 'm', 'n', '..\\documents\\file1.txt', 'p', 'q', 'r']]
        md_df = make_df(rows_list)
        md_df.insert(0, 'extra_beginning', 'x')
        md_df.insert(7, 'extra_middle', 'y')
        md_df['extra_end'] = 'z'
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        # Added sorting since this is the only test I observed with inconsistent column order,
        # but will watch for it elsewhere and add to csv_to_list() if needed.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        result.sort()
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['approved_by', 'True', '0', '0.0', 'uncheckable'],
                    ['city', 'True', '0', '0.0', 'uncheckable'],
                    ['communication_document_id', 'True', '0', '0.0', 'uncheckable'],
                    ['communication_document_name', 'True', '0', '0.0', '0'],
                    ['communication_type', 'True', '0', '0.0', 'uncheckable'],
                    ['country', 'True', '0', '0.0', 'uncheckable'],
                    ['date_in', 'True', '0', '0.0', '0'],
                    ['date_out', 'True', '0', '0.0', '0'],
                    ['document_type', 'True', '0', '0.0', 'uncheckable'],
                    ['extra_beginning', 'Error: unexpected column', '0', '0.0', 'nan'],
                    ['extra_end', 'Error: unexpected column', '0', '0.0', 'nan'],
                    ['extra_middle', 'Error: unexpected column', '0', '0.0', 'nan'],
                    ['file_location', 'True', '0', '0.0', 'uncheckable'],
                    ['file_name', 'True', '0', '0.0', 'uncheckable'],
                    ['group_name', 'True', '0', '0.0', 'uncheckable'],
                    ['reminder_date', 'True', '0', '0.0', '0'],
                    ['response_type', 'True', '0', '0.0', 'uncheckable'],
                    ['state_code', 'True', '0', '0.0', '0'],
                    ['status', 'True', '0', '0.0', 'uncheckable'],
                    ['update_date', 'True', '0', '0.0', '0'],
                    ['zip_code', 'True', '0', '0.0', '0']]
        self.assertEqual(result, expected, "Problem with test for columns extra")

    def test_formatting(self):
        """Test for when each column with formatting tests has errors"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['a', 'Georgia', '1', 'd', 'e', 'f', 'g', '2001', '2001-01-02', 'n.d.', '010104',
                      'l', 'm', 'n', 'documents\\file1.txt', 'p', 'q', 'r'],
                     ['a', 'GA', 'unknown', 'd', 'e', 'f', 'g', '2002', '2002-01-02', 'n.d.', '020104',
                      'l', 'm', 'n', '..\\docs\\file2.txt', 'p', 'q', 'r'],
                     ['a', 'GA', '33333', 'd', 'e', 'f', 'g', '20030101', '20030102', '20030103', '20030104',
                      'l', 'm', 'n', 'file3.txt', 'p', 'q', 'r']]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '0', '0.0', 'uncheckable'],
                    ['state_code', 'True', '0', '0.0', '1'],
                    ['zip_code', 'True', '0', '0.0', '2'],
                    ['country', 'True', '0', '0.0', 'uncheckable'],
                    ['communication_type', 'True', '0', '0.0', 'uncheckable'],
                    ['approved_by', 'True', '0', '0.0', 'uncheckable'],
                    ['status', 'True', '0', '0.0', 'uncheckable'],
                    ['date_in', 'True', '0', '0.0', '2'],
                    ['date_out', 'True', '0', '0.0', '2'],
                    ['reminder_date', 'True', '0', '0.0', '2'],
                    ['update_date', 'True', '0', '0.0', '2'],
                    ['response_type', 'True', '0', '0.0', 'uncheckable'],
                    ['group_name', 'True', '0', '0.0', 'uncheckable'],
                    ['document_type', 'True', '0', '0.0', 'uncheckable'],
                    ['communication_document_name', 'True', '0', '0.0', '3'],
                    ['communication_document_id', 'True', '0', '0.0', 'uncheckable'],
                    ['file_location', 'True', '0', '0.0', 'uncheckable'],
                    ['file_name', 'True', '0', '0.0', 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for formatting")

    def test_columns_missing(self):
        """Test for when every column except dates is missing
        Can't test for all missing at once without mixing it with a test for extra columns"""
        # TODO test fails because some of missing columns are required for formatting
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['20010101', '20010102', '20010103', '20010104']]
        md_df = pd.DataFrame(rows_list, columns=['date_in', 'date_out', 'reminder_date', 'update_date'])
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'False', 'nan', 'nan', 'uncheckable'],
                    ['state_code', 'False', 'nan', 'nan', 'nan'],
                    ['zip_code', 'False', 'nan', 'nan', 'nan'],
                    ['country', 'False', 'nan', 'nan', 'uncheckable'],
                    ['communication_type', 'False', 'nan', 'nan', 'uncheckable'],
                    ['approved_by', 'False', 'nan', 'nan', 'uncheckable'],
                    ['status', 'False', 'nan', 'nan', 'uncheckable'],
                    ['date_in', 'True', '0.0', '0.0', '0'],
                    ['date_out', 'True', '0.0', '0.0', '0'],
                    ['reminder_date', 'True', '0.0', '0.0', '0'],
                    ['update_date', 'True', '0.0', '0.0', '0'],
                    ['response_type', 'False', 'nan', 'nan', 'uncheckable'],
                    ['group_name', 'False', 'nan', 'nan', 'uncheckable'],
                    ['document_type', 'False', 'nan', 'nan', 'uncheckable'],
                    ['communication_document_name', 'False', 'nan', 'nan'],
                    ['communication_document_id', 'False', 'nan', 'nan', 'uncheckable'],
                    ['file_location', 'False', 'nan', 'nan', 'uncheckable'],
                    ['file_name', 'False', 'nan', 'nan', 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for columns missing")

    def test_columns_missing_dates(self):
        """Test for when the date columns are missing
        Can't test for all missing at once without mixing it with a test for extra columns"""
        # Makes a dataframe to use as test input and runs the function.
        # TODO test fails because some of missing columns are required for formatting
        rows_list = [['a', 'GA', '11111', 'd', 'e', 'f', 'g', 'l', 'm', 'n', '..\\documents\\file1.txt', 'p', 'q', 'r']]
        columns_list = ['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                        'response_type', 'group_name', 'document_type', 'communication_document_name',
                        'communication_document_id', 'file_location', 'file_name']
        md_df = pd.DataFrame(rows_list, columns=columns_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '0.0', '0.0', 'uncheckable'],
                    ['state_code', 'True', '0.0', '0.0', '0'],
                    ['zip_code', 'True', '0.0', '0.0', '0'],
                    ['country', 'True', '0.0', '0.0', 'uncheckable'],
                    ['communication_type', 'True', '0.0', '0.0', 'uncheckable'],
                    ['approved_by', 'True', '0.0', '0.0', 'uncheckable'],
                    ['status', 'True', '0.0', '0.0', 'uncheckable'],
                    ['date_in', 'False', 'nan', 'nan', 'nan'],
                    ['date_out', 'False', 'nan', 'nan', 'nan'],
                    ['reminder_date', 'False', 'nan', 'nan', 'nan'],
                    ['update_date', 'False', 'nan', 'nan', 'nan'],
                    ['response_type', 'True', '0.0', '0.0', '0'],
                    ['group_name', 'True', '0.0', '0.0', 'uncheckable'],
                    ['document_type', 'True', '0.0', '0.0', 'uncheckable'],
                    ['communication_document_name', 'True', '0.0', '0.0', '0'],
                    ['communication_document_id', 'True', '0.0', '0.0', 'uncheckable'],
                    ['file_location', 'True', '0.0', '0.0', 'uncheckable'],
                    ['file_name', 'True', '0.0', '0.0', 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for columns missing dates")


if __name__ == '__main__':
    unittest.main()
