"""
Tests for the function usability_check(),
which tests the usability of the metadata and generates reports of the results.
To simplify testing, column values are numbers when the cell content formatting isn't important for the test.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_archiving_format import usability_check


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path)
    df = df.fillna('blank')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


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
        report_paths = [os.path.join('test_data', 'usability_report.csv'),
                        os.path.join('test_data', 'usability_report_columns.csv'),
                        os.path.join('test_data', 'usability_report_letter_matches.csv')]
        for report_path in report_paths:
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_columns_correct(self):
        """Test for when every aspect of column testing is fully correct"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                      20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]]
        md_df = make_df(rows_list)
        usability_check(md_df, 'test_data')

        # Tests the values in the columns report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_columns.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent'],
                    ['prefix', True, 0, 0],
                    ['first', True, 0, 0],
                    ['middle', True, 0, 0],
                    ['last', True, 0, 0],
                    ['suffix', True, 0, 0],
                    ['appellation', True, 0, 0],
                    ['title', True, 0, 0],
                    ['org', True, 0, 0],
                    ['addr1', True, 0, 0],
                    ['addr2', True, 0, 0],
                    ['addr3', True, 0, 0],
                    ['addr4', True, 0, 0],
                    ['city', True, 0, 0],
                    ['state', True, 0, 0],
                    ['zip', True, 0, 0],
                    ['country', True, 0, 0],
                    ['in_id', True, 0, 0],
                    ['in_type', True, 0, 0],
                    ['in_method', True, 0, 0],
                    ['in_date', True, 0, 0],
                    ['in_topic', True, 0, 0],
                    ['in_text', True, 0, 0],
                    ['in_document_name', True, 0, 0],
                    ['in_fillin', True, 0, 0],
                    ['out_id', True, 0, 0],
                    ['out_type', True, 0, 0],
                    ['out_method', True, 0, 0],
                    ['out_date', True, 0, 0],
                    ['out_topic', True, 0, 0],
                    ['out_text', True, 0, 0],
                    ['out_document_name', True, 0, 0],
                    ['out_fillin', True, 0, 0]]
        self.assertEqual(result, expected, "Problem with test for columns - correct, columns report")

    def test_columns_blanks(self):
        """Test for when some columns have blank cells"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                      20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, np.nan],
                     [1, 2, 3, 4, 5, 6, 7, 8, 9,
                      np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                      np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                      np.nan, np.nan, np.nan],
                     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                      np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                      np.nan, np.nan, np.nan],
                     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                     20, 21, 22, 23, 24, 25, 26, 27, 28, 29, np.nan, np.nan, np.nan]]
        md_df = make_df(rows_list)
        usability_check(md_df, 'test_data')

        # Tests the values in the columns report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_columns.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent'],
                    ['prefix', True, 0, 0],
                    ['first', True, 0, 0],
                    ['middle', True, 0, 0],
                    ['last', True, 0, 0],
                    ['suffix', True, 0, 0],
                    ['appellation', True, 0, 0],
                    ['title', True, 0, 0],
                    ['org', True, 0, 0],
                    ['addr1', True, 0, 0],
                    ['addr2', True, 1, 25.0],
                    ['addr3', True, 1, 25.0],
                    ['addr4', True, 1, 25.0],
                    ['city', True, 1, 25.0],
                    ['state', True, 1, 25.0],
                    ['zip', True, 1, 25.0],
                    ['country', True, 1, 25.0],
                    ['in_id', True, 1, 25.0],
                    ['in_type', True, 1, 25.0],
                    ['in_method', True, 1, 25.0],
                    ['in_date', True, 2, 50.0],
                    ['in_topic', True, 2, 50.0],
                    ['in_text', True, 2, 50.0],
                    ['in_document_name', True, 2, 50.0],
                    ['in_fillin', True, 2, 50.0],
                    ['out_id', True, 2, 50.0],
                    ['out_type', True, 2, 50.0],
                    ['out_method', True, 2, 50.0],
                    ['out_date', True, 2, 50.0],
                    ['out_topic', True, 2, 50.0],
                    ['out_text', True, 3, 75.0],
                    ['out_document_name', True, 3, 75.0],
                    ['out_fillin', True, 4, 100.0]]
        self.assertEqual(result, expected, "Problem with test for columns - blanks, columns report")

    def test_columns_extra(self):
        """Test for when some columns are not expected"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                      20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]]
        md_df = make_df(rows_list)
        md_df['extra'] = 33
        usability_check(md_df, 'test_data')

        # Tests the values in the columns report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_columns.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent'],
                    ['prefix', 'True', 0, 0],
                    ['first', 'True', 0, 0],
                    ['middle', 'True', 0, 0],
                    ['last', 'True', 0, 0],
                    ['suffix', 'True', 0, 0],
                    ['appellation', 'True', 0, 0],
                    ['title', 'True', 0, 0],
                    ['org', 'True', 0, 0],
                    ['addr1', 'True', 0, 0],
                    ['addr2', 'True', 0, 0],
                    ['addr3', 'True', 0, 0],
                    ['addr4', 'True', 0, 0],
                    ['city', 'True', 0, 0],
                    ['state', 'True', 0, 0],
                    ['zip', 'True', 0, 0],
                    ['country', 'True', 0, 0],
                    ['in_id', 'True', 0, 0],
                    ['in_type', 'True', 0, 0],
                    ['in_method', 'True', 0, 0],
                    ['in_date', 'True', 0, 0],
                    ['in_topic', 'True', 0, 0],
                    ['in_text', 'True', 0, 0],
                    ['in_document_name', 'True', 0, 0],
                    ['in_fillin', 'True', 0, 0],
                    ['out_id', 'True', 0, 0],
                    ['out_type', 'True', 0, 0],
                    ['out_method', 'True', 0, 0],
                    ['out_date', 'True', 0, 0],
                    ['out_topic', 'True', 0, 0],
                    ['out_text', 'True', 0, 0],
                    ['out_document_name', 'True', 0, 0],
                    ['out_fillin', 'True', 0, 0],
                    ['extra', 'Error: unexpected column', 0, 0]]
        self.assertEqual(result, expected, "Problem with test for columns - missing, columns report")

    def test_columns_missing(self):
        """Test for when some columns are missing"""
        # Makes a dataframe to use as test input and runs the function.
        rows_list = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                      20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]]
        md_df = make_df(rows_list)
        md_df.drop(['prefix', 'first', 'addr2', 'addr3', 'in_date', 'in_topic', 'out_text', 'out_document_name'],
                   axis=1, inplace=True)
        usability_check(md_df, 'test_data')

        # Tests the values in the columns report are correct.
        result = csv_to_list(os.path.join('test_data', 'usability_report_columns.csv'))
        expected = [['Column_Name', 'Present', 'Blank_Count', 'Blank_Percent'],
                    ['prefix', False, 'blank', 'blank'],
                    ['first', False, 'blank', 'blank'],
                    ['middle', True, 0.0, 0.0],
                    ['last', True, 0.0, 0.0],
                    ['suffix', True, 0.0, 0.0],
                    ['appellation', True, 0.0, 0.0],
                    ['title', True, 0.0, 0.0],
                    ['org', True, 0.0, 0.0],
                    ['addr1', True, 0.0, 0.0],
                    ['addr2', False, 'blank', 'blank'],
                    ['addr3', False, 'blank', 'blank'],
                    ['addr4', True, 0.0, 0.0],
                    ['city', True, 0.0, 0.0],
                    ['state', True, 0.0, 0.0],
                    ['zip', True, 0.0, 0.0],
                    ['country', True, 0.0, 0.0],
                    ['in_id', True, 0.0, 0.0],
                    ['in_type', True, 0.0, 0.0],
                    ['in_method', True, 0.0, 0.0],
                    ['in_date', False, 'blank', 'blank'],
                    ['in_topic', False, 'blank', 'blank'],
                    ['in_text', True, 0.0, 0.0],
                    ['in_document_name', True, 0.0, 0.0],
                    ['in_fillin', True, 0.0, 0.0],
                    ['out_id', True, 0.0, 0.0],
                    ['out_type', True, 0.0, 0.0],
                    ['out_method', True, 0.0, 0.0],
                    ['out_date', True, 0.0, 0.0],
                    ['out_topic', True, 0.0, 0.0],
                    ['out_text', False, 'blank', 'blank'],
                    ['out_document_name', False, 'blank', 'blank'],
                    ['out_fillin', True, 0.0, 0.0]]
        self.assertEqual(result, expected, "Problem with test for columns - missing, columns report")


if __name__ == '__main__':
    unittest.main()
