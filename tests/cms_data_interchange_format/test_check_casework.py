"""
Tests for the function check_casework(), which makes a log of rows that could pertain to casework.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from cms_data_interchange_format import check_casework
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the log, if made by the test"""
        log_path = os.path.join('test_data', 'case_remains_log.csv')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_case(self):
        """Test for when rows include 'case'"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'CASE', 'name.doc'],
                              ['30601', 'type1', 'legal case expert.doc'],
                              ['30602', 'type2', 'casey.doc'],
                              ['30603', 'type3', 'file.doc']],
                             columns=['zip_code', 'correspondence_type', 'correspondence_document_name'])
        check_casework(md_df, 'test_data')

        # Tests the values in the case remains log are correct.
        result = csv_to_list(os.path.join('test_data', 'case_remains_log.csv'))
        expected = [['zip_code', 'correspondence_type', 'correspondence_document_name'],
                    ['30600', 'CASE', 'name.doc'],
                    ['30601', 'type1', 'legal case expert.doc'],
                    ['30602', 'type2', 'casey.doc']]
        self.assertEqual(result, expected, "Problem with test for case")

    def test_no_case(self):
        """Test for when no rows include 'case'"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'type1', 'name.doc'],
                              ['30601', 'type2', 'file.doc']],
                             columns=['zip_code', 'correspondence_type', 'correspondence_document_name'])
        check_casework(md_df, 'test_data')

        # Tests the case remains log was not made.
        result = os.path.exists(os.path.join('test_data', 'case_remains_log.csv'))
        self.assertEqual(result, False, "Problem with test for no case")


if __name__ == '__main__':
    unittest.main()
