"""
Tests for the function check_metadata_usability(),
which tests the usability of the metadata and generates a report of the results.
To simplify testing, column values are numbers when the cell content formatting isn't important for the test.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_archiving_format import check_metadata_usability
from test_script import csv_to_list


def make_df(rows_list):
    """Makes md_df for testing. In production, this is made by reading the export csv."""
    column_names = ['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                    'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                    'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                    'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin']
    df = pd.DataFrame(rows_list, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the reports, if made by the test"""
        reports = ['metadata_formatting_errors_in_date.csv', 'metadata_formatting_errors_in_document_name.csv',
                   'metadata_formatting_errors_out_date.csv', 'metadata_formatting_errors_out_document_name.csv',
                   'metadata_formatting_errors_state.csv', 'metadata_formatting_errors_zip.csv',
                   'usability_report_metadata.csv']
        for report in reports:
            report_path = os.path.join('test_data', report)
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_columns_correct(self):
        """Test for when every aspect of column testing is fully correct"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'GA', '30601', '16', '17', 
                      '18', '19', '20010401', '21', '22', r'..\documents\BlobExport\folder.txt', '24', '25', '26', 
                      '27', '20010415', '29', '30', r'..\documents\BlobExport\folder.txt', '32']]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['prefix', True, 0, 0.0, 'uncheckable'],
                    ['first', True, 0, 0.0, 'uncheckable'],
                    ['middle', True, 0, 0.0, 'uncheckable'],
                    ['last', True, 0, 0.0, 'uncheckable'],
                    ['suffix', True, 0, 0.0, 'uncheckable'],
                    ['appellation', True, 0, 0.0, 'uncheckable'],
                    ['title', True, 0, 0.0, 'uncheckable'],
                    ['org', True, 0, 0.0, 'uncheckable'],
                    ['addr1', True, 0, 0.0, 'uncheckable'],
                    ['addr2', True, 0, 0.0, 'uncheckable'],
                    ['addr3', True, 0, 0.0, 'uncheckable'],
                    ['addr4', True, 0, 0.0, 'uncheckable'],
                    ['city', True, 0, 0.0, 'uncheckable'],
                    ['state', True, 0, 0, '0'],
                    ['zip', True, 0, 0, '0'],
                    ['country', True, 0, 0.0, 'uncheckable'],
                    ['in_id', True, 0, 0.0, 'uncheckable'],
                    ['in_type', True, 0, 0.0, 'uncheckable'],
                    ['in_method', True, 0, 0.0, 'uncheckable'],
                    ['in_date', True, 0, 0, '0'],
                    ['in_topic', True, 0, 0.0, 'uncheckable'],
                    ['in_text', True, 0, 0.0, 'uncheckable'],
                    ['in_document_name', True, 0, 0, '0'],
                    ['in_fillin', True, 0, 0.0, 'uncheckable'],
                    ['out_id', True, 0, 0.0, 'uncheckable'],
                    ['out_type', True, 0, 0.0, 'uncheckable'],
                    ['out_method', True, 0, 0.0, 'uncheckable'],
                    ['out_date', True, 0, 0, '0'],
                    ['out_topic', True, 0, 0.0, 'uncheckable'],
                    ['out_text', True, 0, 0.0, 'uncheckable'],
                    ['out_document_name', True, 0, 0, '0'],
                    ['out_fillin', True, 0, 0.0, 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for correct")

    def test_columns_blanks(self):
        """Test for when some columns have blank cells"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'GA', '30601', '16', '17', 
                      '18', '19', '20010401', '21', '22', r'..\documents\BlobExport\folder.txt', '24', '25', '26', '27', 
                      '20010415', '29', '30', r'..\documents\BlobExport\folder.txt', np.nan],
                     ['1', '2', '3', '4', '5', '6', '7', '8', '9', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 
                      np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 
                      np.nan, np.nan, np.nan, np.nan, np.nan],
                     ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'GA', '30601', '16', '17', 
                      '18', '19', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                      np.nan, np.nan, np.nan],
                     ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'GA', '30601', '16', '17', 
                      '18', '19', '20010401', '21', '22', r'..\documents\BlobExport\folder.txt', '24', '25', '26', 
                      '27', '20010415', '29', np.nan, np.nan, np.nan]]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['prefix', True, 0, 0.0, 'uncheckable'],
                    ['first', True, 0, 0.0, 'uncheckable'],
                    ['middle', True, 0, 0.0, 'uncheckable'],
                    ['last', True, 0, 0.0, 'uncheckable'],
                    ['suffix', True, 0, 0.0, 'uncheckable'],
                    ['appellation', True, 0, 0.0, 'uncheckable'],
                    ['title', True, 0, 0.0, 'uncheckable'],
                    ['org', True, 0, 0.0, 'uncheckable'],
                    ['addr1', True, 0, 0.0, 'uncheckable'],
                    ['addr2', True, 1, 25.0, 'uncheckable'],
                    ['addr3', True, 1, 25.0, 'uncheckable'],
                    ['addr4', True, 1, 25.0, 'uncheckable'],
                    ['city', True, 1, 25.0, 'uncheckable'],
                    ['state', True, 1, 25.0, '0'],
                    ['zip', True, 1, 25.0, '0'],
                    ['country', True, 1, 25.0, 'uncheckable'],
                    ['in_id', True, 1, 25.0, 'uncheckable'],
                    ['in_type', True, 1, 25.0, 'uncheckable'],
                    ['in_method', True, 1, 25.0, 'uncheckable'],
                    ['in_date', True, 2, 50.0, '0'],
                    ['in_topic', True, 2, 50.0, 'uncheckable'],
                    ['in_text', True, 2, 50.0, 'uncheckable'],
                    ['in_document_name', True, 2, 50.0, '0'],
                    ['in_fillin', True, 2, 50.0, 'uncheckable'],
                    ['out_id', True, 2, 50.0, 'uncheckable'],
                    ['out_type', True, 2, 50.0, 'uncheckable'],
                    ['out_method', True, 2, 50.0, 'uncheckable'],
                    ['out_date', True, 2, 50.0, '0'],
                    ['out_topic', True, 2, 50.0, 'uncheckable'],
                    ['out_text', True, 3, 75.0, 'uncheckable'],
                    ['out_document_name', True, 3, 75.0, '0'],
                    ['out_fillin', True, 4, 100.0, 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for blanks")

    def test_columns_extra(self):
        """Test for when some columns are not expected"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'GA', '30601', '16', '17', 
                      '18', '19', '20010401', '21', '22', r'..\documents\BlobExport\folder.txt', '24', '25', '26', 
                      '27', '20010415', '29', '30', r'..\documents\BlobExport\folder.txt', '32']]
        md_df = make_df(rows_list)
        md_df['extra'] = '33'
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['prefix', 'True', 0, 0.0, 'uncheckable'],
                    ['first', 'True', 0, 0.0, 'uncheckable'],
                    ['middle', 'True', 0, 0.0, 'uncheckable'],
                    ['last', 'True', 0, 0.0, 'uncheckable'],
                    ['suffix', 'True', 0, 0.0, 'uncheckable'],
                    ['appellation', 'True', 0, 0.0, 'uncheckable'],
                    ['title', 'True', 0, 0.0, 'uncheckable'],
                    ['org', 'True', 0, 0.0, 'uncheckable'],
                    ['addr1', 'True', 0, 0.0, 'uncheckable'],
                    ['addr2', 'True', 0, 0.0, 'uncheckable'],
                    ['addr3', 'True', 0, 0.0, 'uncheckable'],
                    ['addr4', 'True', 0, 0.0, 'uncheckable'],
                    ['city', 'True', 0, 0.0, 'uncheckable'],
                    ['state', 'True', 0, 0.0, '0'],
                    ['zip', 'True', 0, 0.0, '0'],
                    ['country', 'True', 0, 0.0, 'uncheckable'],
                    ['in_id', 'True', 0, 0.0, 'uncheckable'],
                    ['in_type', 'True', 0, 0.0, 'uncheckable'],
                    ['in_method', 'True', 0, 0.0, 'uncheckable'],
                    ['in_date', 'True', 0, 0.0, '0'],
                    ['in_topic', 'True', 0, 0.0, 'uncheckable'],
                    ['in_text', 'True', 0, 0.0, 'uncheckable'],
                    ['in_document_name', 'True', 0, 0.0, '0'],
                    ['in_fillin', 'True', 0, 0.0, 'uncheckable'],
                    ['out_id', 'True', 0, 0.0, 'uncheckable'],
                    ['out_type', 'True', 0, 0.0, 'uncheckable'],
                    ['out_method', 'True', 0, 0.0, 'uncheckable'],
                    ['out_date', 'True', 0, 0.0, '0'],
                    ['out_topic', 'True', 0, 0.0, 'uncheckable'],
                    ['out_text', 'True', 0, 0.0, 'uncheckable'],
                    ['out_document_name', 'True', 0, 0.0, '0'],
                    ['out_fillin', 'True', 0, 0.0, 'uncheckable'],
                    ['extra', 'Error: unexpected column', 0, 0.0, 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for extra")

    def test_columns_format(self):
        """Test for when some cells in the six tested columns do not match the expected formats"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'ga', '30601', '16', '17', 
                      '18', '19', '19991201', '21', '22', r'..\documents\BlobExport\folder\file.txt', '24', '25', 
                      '26', '27', '1999-12-17', '29', '30', r'..\documents\BlobExport\folder\file.txt', '32'],
                     ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', np.nan, np.nan, '16', '17', 
                      '18', '19', np.nan, '21', '22', np.nan, '24', '25', '26', '27', '1999', '29', '30', np.nan, '32'],
                     ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'GA', 'zipcode', '16', '17', 
                      '18', '19', '20000101', '21', '22', r'\new\file.txt', '24', '25', '26', '27', 'July 1, 2001', 
                      '29', '30', r'..\documents\BlobExport\folder\file.txt', '32'],
                     ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'Georgia', '30601-0000', 
                      '16', '17', '18', '19', np.nan, '21', '22', r'\\smith-dc\dos\public\folder\file.txt', '24', 
                      '25', '26', '27', 'undated', '29', '30', r'\\new\file.txt', '32'],
                     ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'NDA', '3060', '16', '17', 
                      '18', '19', '2000 Jan 3', '21', '22', 'file.txt', '24', '25', '26', '27', '19990101.12.12', 
                      '29', '30', r'\\smith-atl\dos\public\folder\file.txt', '32']]
        md_df = make_df(rows_list)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['prefix', True, 0, 0.0, 'uncheckable'],
                    ['first', True, 0, 0.0, 'uncheckable'],
                    ['middle', True, 0, 0.0, 'uncheckable'],
                    ['last', True, 0, 0.0, 'uncheckable'],
                    ['suffix', True, 0, 0.0, 'uncheckable'],
                    ['appellation', True, 0, 0.0, 'uncheckable'],
                    ['title', True, 0, 0.0, 'uncheckable'],
                    ['org', True, 0, 0.0, 'uncheckable'],
                    ['addr1', True, 0, 0.0, 'uncheckable'],
                    ['addr2', True, 0, 0.0, 'uncheckable'],
                    ['addr3', True, 0, 0.0, 'uncheckable'],
                    ['addr4', True, 0, 0.0, 'uncheckable'],
                    ['city', True, 0, 0.0, 'uncheckable'],
                    ['state', True, 1, 20.0, '3'],
                    ['zip', True, 1, 20.0, '2'],
                    ['country', True, 0, 0.0, 'uncheckable'],
                    ['in_id', True, 0, 0.0, 'uncheckable'],
                    ['in_type', True, 0, 0.0, 'uncheckable'],
                    ['in_method', True, 0, 0.0, 'uncheckable'],
                    ['in_date', True, 2, 40.0, '1'],
                    ['in_topic', True, 0, 0.0, 'uncheckable'],
                    ['in_text', True, 0, 0.0, 'uncheckable'],
                    ['in_document_name', True, 1, 20.0, '2'],
                    ['in_fillin', True, 0, 0.0, 'uncheckable'],
                    ['out_id', True, 0, 0.0, 'uncheckable'],
                    ['out_type', True, 0, 0.0, 'uncheckable'],
                    ['out_method', True, 0, 0.0, 'uncheckable'],
                    ['out_date', True, 0, 0.0, '5'],
                    ['out_topic', True, 0, 0.0, 'uncheckable'],
                    ['out_text', True, 0, 0.0, 'uncheckable'],
                    ['out_document_name', True, 1, 20.0, '1'],
                    ['out_fillin', True, 0, 0.0, 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for formatting")

    def test_columns_missing(self):
        """Test for when some columns are missing"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 'GA', '30601', '16', '17', 
                      '18', '19', '20010401', '21', '22', r'..\documents\BlobExport\folder.txt', '24', '25', '26', 
                      '27', '20010415', '29', '30', r'..\documents\BlobExport\folder.txt', '32']]
        md_df = make_df(rows_list)
        md_df.drop(['prefix', 'first', 'addr2', 'addr3', 'in_method', 'in_topic', 'out_text', 'out_fillin'],
                   axis=1, inplace=True)
        check_metadata_usability(md_df, 'test_data')

        # Tests the values in the metadata usability report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_metadata.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent', 'Formatting_Errors'],
                    ['prefix', False, 'BLANK', 'BLANK', 'uncheckable'],
                    ['first', False, 'BLANK', 'BLANK', 'uncheckable'],
                    ['middle', True, 0.0, 0.0, 'uncheckable'],
                    ['last', True, 0.0, 0.0, 'uncheckable'],
                    ['suffix', True, 0.0, 0.0, 'uncheckable'],
                    ['appellation', True, 0.0, 0.0, 'uncheckable'],
                    ['title', True, 0.0, 0.0, 'uncheckable'],
                    ['org', True, 0.0, 0.0, 'uncheckable'],
                    ['addr1', True, 0.0, 0.0, 'uncheckable'],
                    ['addr2', False, 'BLANK', 'BLANK', 'uncheckable'],
                    ['addr3', False, 'BLANK', 'BLANK', 'uncheckable'],
                    ['addr4', True, 0.0, 0.0, 'uncheckable'],
                    ['city', True, 0.0, 0.0, 'uncheckable'],
                    ['state', True, 0.0, 0.0, '0'],
                    ['zip', True, 0.0, 0.0, '0'],
                    ['country', True, 0.0, 0.0, 'uncheckable'],
                    ['in_id', True, 0.0, 0.0, 'uncheckable'],
                    ['in_type', True, 0.0, 0.0, 'uncheckable'],
                    ['in_method', False, 'BLANK', 'BLANK', 'uncheckable'],
                    ['in_date', True, 0.0, 0.0, '0'],
                    ['in_topic', False, 'BLANK', 'BLANK', 'uncheckable'],
                    ['in_text', True, 0.0, 0.0, 'uncheckable'],
                    ['in_document_name', True, 0.0, 0.0, '0'],
                    ['in_fillin', True, 0.0, 0.0, 'uncheckable'],
                    ['out_id', True, 0.0, 0.0, 'uncheckable'],
                    ['out_type', True, 0.0, 0.0, 'uncheckable'],
                    ['out_method', True, 0.0, 0.0, 'uncheckable'],
                    ['out_date', True, 0.0, 0.0, '0'],
                    ['out_topic', True, 0.0, 0.0, 'uncheckable'],
                    ['out_text', False, 'BLANK', 'BLANK', 'uncheckable'],
                    ['out_document_name', True, 0.0, 0.0, '0'],
                    ['out_fillin', False, 'BLANK', 'BLANK', 'uncheckable']]
        self.assertEqual(result, expected, "Problem with test for missing")


if __name__ == '__main__':
    unittest.main()
