"""
Tests for the function check_metadata_usability(),
which tests the usability of the metadata and generates a report of the results.
To simply testing, column values are letters when the cell content formatting isn't important for the test.
"""
import numpy as np
import os
import pandas as pd
import unittest
from cms_data_interchange_format import check_metadata_usability
from test_script import csv_to_list


def make_df(rows_list):
    """Makes md_df for testing. In production, this is made by reading the export csv.
    This can only be used for making test input with all the columns present.
    """
    column_names = ['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                    'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                    '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                    'code_type', 'code', 'code_description', 'inactive_flag']
    df = pd.DataFrame(rows_list, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the reports, if made by the test"""
        reports = ['metadata_formatting_errors_correspondence_document_name.csv',
                   'metadata_formatting_errors_date_in.csv', 'metadata_formatting_errors_date_out.csv',
                   'metadata_formatting_errors_state.csv', 'metadata_formatting_errors_tickler_date.csv',
                   'metadata_formatting_errors_update_date.csv', 'metadata_formatting_errors_zip_code.csv',
                   'usability_report_metadata.csv']
        for report in reports:
            report_path = os.path.join('test_data', report)
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_all_correct(self):
        """Test for when all aspects of column testing are fully correct and there are no blanks"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['a', 'GA', '30600', 'b', 'c', 'd', '20240810', '20240811', '20240812', '20240813',
                      'e', 'f', 'g', 'h', 'i', 'forms\\1.txt', 'j', 'k', 'l', 'm', 'n'],
                     ['a', 'GA', '30601', 'b', 'c', 'd', '20240910', '20240911', '20240912', '20240913',
                      'e', 'f', 'g', 'h', 'i', 'forms\\2.txt', 'j', 'k', 'l', 'm', 'n'],
                     ['a', 'GA', '30602', 'b', 'c', 'd', '20241010', '20241011', '20241012', '20241013',
                      'e', 'f', 'g', 'h', 'i', 'forms\\3.txt', 'j', 'k', 'l', 'm', 'n']]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '0', '0.0', 'uncheckable'],
                    ['state', 'True', '0', '0.0', '0'],
                    ['zip_code', 'True', '0', '0.0', '0'],
                    ['country', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_type', 'True', '0', '0.0', 'uncheckable'],
                    ['staff', 'True', '0', '0.0', 'uncheckable'],
                    ['date_in', 'True', '0', '0.0', '0'],
                    ['date_out', 'True', '0', '0.0', '0'],
                    ['tickler_date', 'True', '0', '0.0', '0'],
                    ['update_date', 'True', '0', '0.0', '0'],
                    ['response_type', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_code', 'True', '0', '0.0', 'uncheckable'],
                    ['position', 'True', '0', '0.0', 'uncheckable'],
                    ['2C_sequence_number', 'True', '0', '0.0', 'uncheckable'],
                    ['document_type', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_document_name', 'True', '0', '0.0', '0'],
                    ['file_location', 'True', '0', '0.0', 'uncheckable'],
                    ['code_type', 'True', '0', '0.0', 'uncheckable'],
                    ['code', 'True', '0', '0.0', 'uncheckable'],
                    ['code_description', 'True', '0', '0.0', 'uncheckable'],
                    ['inactive_flag', 'True', '0', '0.0', 'uncheckable']]
        self.assertEqual(expected, result, "Problem with test for all correct, usability_report_metadata.csv")

        # Tests which formatting reports were made, if any.
        result = [os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_correspondence_document_name.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_in.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_out.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_state.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_tickler_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_update_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))]
        expected = [False, False, False, False, False, False, False]
        self.assertEqual(expected, result, "Problem with test for all correct, metadata_formatting_errors csvs")

    def test_blank(self):
        """Test for when every row is blank"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                      np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                      np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '2', '100.0', 'uncheckable'],
                    ['state', 'True', '2', '100.0', 'column_blank'],
                    ['zip_code', 'True', '2', '100.0', 'column_blank'],
                    ['country', 'True', '2', '100.0', 'uncheckable'],
                    ['correspondence_type', 'True', '2', '100.0', 'uncheckable'],
                    ['staff', 'True', '2', '100.0', 'uncheckable'],
                    ['date_in', 'True', '2', '100.0', 'column_blank'],
                    ['date_out', 'True', '2', '100.0', 'column_blank'],
                    ['tickler_date', 'True', '2', '100.0', 'column_blank'],
                    ['update_date', 'True', '2', '100.0', 'column_blank'],
                    ['response_type', 'True', '2', '100.0', 'uncheckable'],
                    ['correspondence_code', 'True', '2', '100.0', 'uncheckable'],
                    ['position', 'True', '2', '100.0', 'uncheckable'],
                    ['2C_sequence_number', 'True', '2', '100.0', 'uncheckable'],
                    ['document_type', 'True', '2', '100.0', 'uncheckable'],
                    ['correspondence_document_name', 'True', '2', '100.0', 'column_blank'],
                    ['file_location', 'True', '2', '100.0', 'uncheckable'],
                    ['code_type', 'True', '2', '100.0', 'uncheckable'],
                    ['code', 'True', '2', '100.0', 'uncheckable'],
                    ['code_description', 'True', '2', '100.0', 'uncheckable'],
                    ['inactive_flag', 'True', '2', '100.0', 'uncheckable']]
        self.assertEqual(expected, result, "Problem with test for blank, usability_report_metadata.csv")

        # Tests which formatting reports were made, if any.
        result = [os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_correspondence_document_name.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_in.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_out.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_state.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_tickler_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_update_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))]
        expected = [False, False, False, False, False, False, False]
        self.assertEqual(expected, result, "Problem with test for all blank, metadata_formatting_errors csvs")

    def test_blank_partial(self):
        """Test for some rows of each column have blanks but no column is entirely blank"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                      np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                     ['a', np.nan, np.nan, np.nan, 'c', np.nan, np.nan, np.nan, '20241012', np.nan,
                      np.nan, np.nan, 'g', np.nan, np.nan, np.nan, 'j', np.nan, np.nan, np.nan, 'n'],
                     ['a', 'GA', np.nan, np.nan, 'c', 'd', np.nan, np.nan, '20241012', '20241013',
                      np.nan, np.nan, 'g', 'h', np.nan, np.nan, 'j', 'k', np.nan, np.nan, 'n'],
                     ['a', 'GA', '30602', np.nan, 'c', 'd', '20241010', np.nan, '20241012', '20241013',
                      'e', np.nan, 'g', 'h', 'i', np.nan, 'j', 'k', 'l', np.nan, 'n'],
                     ['a', 'GA', '30602', 'b', 'c', 'd', '20241010', '20241011', '20241012', '20241013',
                     'e', 'f', 'g', 'h', 'i', 'forms\\3.txt', 'j', 'k', 'l', 'm', 'n']]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '1', '20.0', 'uncheckable'],
                    ['state', 'True', '2', '40.0', '0'],
                    ['zip_code', 'True', '3', '60.0', '0'],
                    ['country', 'True', '4', '80.0', 'uncheckable'],
                    ['correspondence_type', 'True', '1', '20.0', 'uncheckable'],
                    ['staff', 'True', '2', '40.0', 'uncheckable'],
                    ['date_in', 'True', '3', '60.0', '0'],
                    ['date_out', 'True', '4', '80.0', '0'],
                    ['tickler_date', 'True', '1', '20.0', '0'],
                    ['update_date', 'True', '2', '40.0', '0'],
                    ['response_type', 'True', '3', '60.0', 'uncheckable'],
                    ['correspondence_code', 'True', '4', '80.0', 'uncheckable'],
                    ['position', 'True', '1', '20.0', 'uncheckable'],
                    ['2C_sequence_number', 'True', '2', '40.0', 'uncheckable'],
                    ['document_type', 'True', '3', '60.0', 'uncheckable'],
                    ['correspondence_document_name', 'True', '4', '80.0', '0'],
                    ['file_location', 'True', '1', '20.0', 'uncheckable'],
                    ['code_type', 'True', '2', '40.0', 'uncheckable'],
                    ['code', 'True', '3', '60.0', 'uncheckable'],
                    ['code_description', 'True', '4', '80.0', 'uncheckable'],
                    ['inactive_flag', 'True', '1', '20.0', 'uncheckable']]
        self.assertEqual(expected, result, "Problem with test for blank_partial, usability_report_metadata.csv")

        # Tests which formatting reports were made, if any.
        result = [os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_correspondence_document_name.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_in.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_out.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_state.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_tickler_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_update_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))]
        expected = [False, False, False, False, False, False, False]
        self.assertEqual(expected, result, "Problem with test for blank_partial, metadata_formatting_errors csvs")

    def test_columns_extra(self):
        """Test for when there are additional columns beyond what is expected"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['a', 'GA', '30600', 'b', 'c', 'd', '20240810', '20240811', '20240812', '20240813',
                      'e', 'f', 'g', 'h', 'i', 'forms\\1.txt', 'j', 'k', 'l', 'm', 'n'],
                     ['a', 'GA', '30601', 'b', 'c', 'd', '20240910', '20240911', '20240912', '20240913',
                      'e', 'f', 'g', 'h', 'i', 'forms\\2.txt', 'j', 'k', 'l', 'm', 'n']]
        md_df = make_df(rows_list)
        md_df.insert(0, 'extra_beginning', 'x')
        md_df.insert(10, 'extra_middle', 'y')
        md_df['extra_end'] = 'z'
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'), sort=True)
        expected = [['2C_sequence_number', 'True', '0', '0.0', 'uncheckable'],
                    ['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '0', '0.0', 'uncheckable'],
                    ['code', 'True', '0', '0.0', 'uncheckable'],
                    ['code_description', 'True', '0', '0.0', 'uncheckable'],
                    ['code_type', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_code', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_document_name', 'True', '0', '0.0', '0'],
                    ['correspondence_type', 'True', '0', '0.0', 'uncheckable'],
                    ['country', 'True', '0', '0.0', 'uncheckable'],
                    ['date_in', 'True', '0', '0.0', '0'],
                    ['date_out', 'True', '0', '0.0', '0'],
                    ['document_type', 'True', '0', '0.0', 'uncheckable'],
                    ['extra_beginning', 'Error: unexpected column', '0', '0.0', 'BLANK'],
                    ['extra_end', 'Error: unexpected column', '0', '0.0', 'BLANK'],
                    ['extra_middle', 'Error: unexpected column', '0', '0.0', 'BLANK'],
                    ['file_location', 'True', '0', '0.0', 'uncheckable'],
                    ['inactive_flag', 'True', '0', '0.0', 'uncheckable'],
                    ['position', 'True', '0', '0.0', 'uncheckable'],
                    ['response_type', 'True', '0', '0.0', 'uncheckable'],
                    ['staff', 'True', '0', '0.0', 'uncheckable'],
                    ['state', 'True', '0', '0.0', '0'],
                    ['tickler_date', 'True', '0', '0.0', '0'],
                    ['update_date', 'True', '0', '0.0', '0'],
                    ['zip_code', 'True', '0', '0.0', '0']]
        self.assertEqual(expected, result, "Problem with test for columns_extra, usability_report_metadata.csv")

        # Tests which formatting reports were made, if any.
        result = [os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_correspondence_document_name.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_in.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_out.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_state.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_tickler_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_update_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))]
        expected = [False, False, False, False, False, False, False]
        self.assertEqual(expected, result, "Problem with test for columns_metadata, metadata_formatting_errors csvs")

    def test_columns_missing(self):
        """Test for when every column except dates is missing
        Can't test for all missing at once without mixing it with a test for extra columns"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['20240810', '20240811', '20240812', '20240813'],
                     ['20240910', '20240911', '20240912', '20240913'],
                     ['20241010', '20241011', '20241012', '20241013']]
        md_df = pd.DataFrame(rows_list, columns=['date_in', 'date_out', 'tickler_date', 'update_date'])
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['state', 'False', 'BLANK', 'BLANK', 'column_missing'],
                    ['zip_code', 'False', 'BLANK', 'BLANK', 'column_missing'],
                    ['country', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['correspondence_type', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['staff', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['date_in', 'True', '0.0', '0.0', '0'],
                    ['date_out', 'True', '0.0', '0.0', '0'],
                    ['tickler_date', 'True', '0.0', '0.0', '0'],
                    ['update_date', 'True', '0.0', '0.0', '0'],
                    ['response_type', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['correspondence_code', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['position', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['2C_sequence_number', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['document_type', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['correspondence_document_name', 'False', 'BLANK', 'BLANK', 'column_missing'],
                    ['file_location', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['code_type', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['code', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['code_description', 'False', 'BLANK', 'BLANK', 'uncheckable'],
                    ['inactive_flag', 'False', 'BLANK', 'BLANK', 'uncheckable']]
        self.assertEqual(expected, result, "Problem with test for columns_missing, usability_report_metadata.csv")

        # Tests which formatting reports were made, if any.
        result = [os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_correspondence_document_name.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_in.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_out.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_state.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_tickler_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_update_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))]
        expected = [False, False, False, False, False, False, False]
        self.assertEqual(expected, result, "Problem with test for columns_missing, metadata_formatting_errors csvs")

    def test_columns_missing_dates(self):
        """Test for when the date columns are missing
        Can't test for all missing at once without mixing it with a test for extra columns"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['a', 'GA', '30600', 'b', 'c', 'd', '20240810', '20240811', '20240812', '20240813',
                     'e', 'f', 'g', 'h', 'i', 'forms\\1.txt', 'j', 'k', 'l', 'm', 'n'],
                    ['a', 'GA', '30601', 'b', 'c', 'd', '20240910', '20240911', '20240912', '20240913',
                     'e', 'f', 'g', 'h', 'i', 'forms\\2.txt', 'j', 'k', 'l', 'm', 'n'],
                    ['a', 'GA', '30602', 'b', 'c', 'd', '20241010', '20241011', '20241012', '20241013',
                     'e', 'f', 'g', 'h', 'i', 'forms\\3.txt', 'j', 'k', 'l', 'm', 'n']]
        md_df = make_df(rows_list)
        md_df.drop(['date_in', 'date_out', 'tickler_date', 'update_date'], axis=1, inplace=True)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '0.0', '0.0', 'uncheckable'],
                    ['state', 'True', '0.0', '0.0', '0'],
                    ['zip_code', 'True', '0.0', '0.0', '0'],
                    ['country', 'True', '0.0', '0.0', 'uncheckable'],
                    ['correspondence_type', 'True', '0.0', '0.0', 'uncheckable'],
                    ['staff', 'True', '0.0', '0.0', 'uncheckable'],
                    ['date_in', 'False', 'BLANK', 'BLANK', 'column_missing'],
                    ['date_out', 'False', 'BLANK', 'BLANK', 'column_missing'],
                    ['tickler_date', 'False', 'BLANK', 'BLANK', 'column_missing'],
                    ['update_date', 'False', 'BLANK', 'BLANK', 'column_missing'],
                    ['response_type', 'True', '0.0', '0.0', 'uncheckable'],
                    ['correspondence_code', 'True', '0.0', '0.0', 'uncheckable'],
                    ['position', 'True', '0.0', '0.0', 'uncheckable'],
                    ['2C_sequence_number', 'True', '0.0', '0.0', 'uncheckable'],
                    ['document_type', 'True', '0.0', '0.0', 'uncheckable'],
                    ['correspondence_document_name', 'True', '0.0', '0.0', '0'],
                    ['file_location', 'True', '0.0', '0.0', 'uncheckable'],
                    ['code_type', 'True', '0.0', '0.0', 'uncheckable'],
                    ['code', 'True', '0.0', '0.0', 'uncheckable'],
                    ['code_description', 'True', '0.0', '0.0', 'uncheckable'],
                    ['inactive_flag', 'True', '0.0', '0.0', 'uncheckable']]
        self.assertEqual(expected, result, "Problem with test for columns_missing_dates, usability_report_metadata.csv")

        # Tests which formatting reports were made, if any.
        result = [os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_correspondence_document_name.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_in.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_out.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_state.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_tickler_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_update_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))]
        expected = [False, False, False, False, False, False, False]
        self.assertEqual(expected, result, "Problem with test for columns_missing_datest, metadata_formatting_errors csvs")

    def test_formatting(self):
        """Test for when each column with formatting tests has errors"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['a', 'Georgia', '3', 'b', 'c', 'd', '2024-08-10', '2024-08-11', '2024-08-12', 'Aug 24',
                      'e', 'f', 'g', 'h', 'i', '1.txt', 'j', 'k', 'l', 'm', 'n'],
                     ['a', 'GA', '306011', 'b', 'c', 'd', '2024', '20240911', '2024', 'Sept 24',
                      'e', 'f', 'g', 'h', 'i', 'forms\\2.txt', 'j', 'k', 'l', 'm', 'n'],
                     ['a', 'GA', '30602', 'b', 'c', 'd', 'October 10', '20241011', '20241012', 'Oct 24',
                      'e', 'f', 'g', 'h', 'i', 'forms\\3.txt', 'j', 'k', 'l', 'm', 'n']]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['city', 'True', '0', '0.0', 'uncheckable'],
                    ['state', 'True', '0', '0.0', '1'],
                    ['zip_code', 'True', '0', '0.0', '2'],
                    ['country', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_type', 'True', '0', '0.0', 'uncheckable'],
                    ['staff', 'True', '0', '0.0', 'uncheckable'],
                    ['date_in', 'True', '0', '0.0', '3'],
                    ['date_out', 'True', '0', '0.0', '1'],
                    ['tickler_date', 'True', '0', '0.0', '2'],
                    ['update_date', 'True', '0', '0.0', '3'],
                    ['response_type', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_code', 'True', '0', '0.0', 'uncheckable'],
                    ['position', 'True', '0', '0.0', 'uncheckable'],
                    ['2C_sequence_number', 'True', '0', '0.0', 'uncheckable'],
                    ['document_type', 'True', '0', '0.0', 'uncheckable'],
                    ['correspondence_document_name', 'True', '0', '0.0', '1'],
                    ['file_location', 'True', '0', '0.0', 'uncheckable'],
                    ['code_type', 'True', '0', '0.0', 'uncheckable'],
                    ['code', 'True', '0', '0.0', 'uncheckable'],
                    ['code_description', 'True', '0', '0.0', 'uncheckable'],
                    ['inactive_flag', 'True', '0', '0.0', 'uncheckable']]
        self.assertEqual(expected, result, "Problem with test for formatting, usability_report_metadata.csv")

        # Tests which formatting reports were made, if any.
        result = [os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_correspondence_document_name.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_in.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_date_out.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_state.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_tickler_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_update_date.csv')),
                  os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip_code.csv'))]
        expected = [True, True, True, True, True, True, True]
        self.assertEqual(expected, result, "Problem with test for formatting, metadata_formatting_errors csvs")


if __name__ == '__main__':
    unittest.main()
