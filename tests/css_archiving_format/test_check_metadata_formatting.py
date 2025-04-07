"""
Tests for the function check_metadata_formatting(),
which finds all rows in a column that don't match the expected formatting,
saves them to a csv and returns the count.
This is for columns with a single pattern. There is a separate function for multiple patterns.
To simplify testing, only a few columns are used.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_archiving_format import check_metadata_formatting
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the reports, if made by the test"""
        columns = ['in_date', 'out_date', 'state', 'zip']
        for column in columns:
            report_path = os.path.join('test_data', f'metadata_formatting_errors_{column}.csv')
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_in_date(self):
        """Test for the in_date column, including correct cells, formatting errors, and blanks"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30601', np.nan], ['30602', '20001212.0600'], ['30603', '20001212'], ['30604', '2000'],
                           ['30605', '2000-12-12'], ['30606', 'Dec 12, 2000'], ['30606', 'rcvd 20001212']],
                          columns=['zip', 'in_date'])
        state_mismatch = check_metadata_formatting('in_date', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(state_mismatch, 5, "Problem with test for in_date, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_in_date.csv'))
        expected = [['zip', 'in_date'], [30602, '20001212.0600'], [30604, '2000'], [30605, '2000-12-12'],
                    [30606, 'Dec 12, 2000'], [30606, 'rcvd 20001212']]
        self.assertEqual(result, expected, "Problem with test for in_date, report")

    def test_out_date(self):
        """Test for the out_date column, including correct cells, formatting errors, and blanks"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30601', np.nan], ['30602', '20001212.0600'], ['30603', '20001212'], ['30604', '2000'],
                           ['30605', '2000-12-12'], ['30606', 'Dec 12, 2000'], ['30606', 'rcvd 20001212']],
                          columns=['zip', 'out_date'])
        state_mismatch = check_metadata_formatting('out_date', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(state_mismatch, 5, "Problem with test for out_date, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_out_date.csv'))
        expected = [['zip', 'out_date'], [30602, '20001212.0600'], [30604, '2000'], [30605, '2000-12-12'],
                    [30606, 'Dec 12, 2000'], [30606, 'rcvd 20001212']]
        self.assertEqual(result, expected, "Problem with test for out_date, report")

    def test_state(self):
        """Test for the state column, including correct cells, formatting errors, and blanks"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['GA', '30601'], [np.nan, '30602'], ['ga', '30603'],
                           ['GEORGIA', '30604'], ['AL', '30605'], ['NDK', '30606'], ['D.C.', '30607']],
                          columns=['state', 'zip'])
        state_mismatch = check_metadata_formatting('state', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(state_mismatch, 3, "Problem with test for state, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_state.csv'))
        expected = [['state', 'zip'], ['ga', 30603], ['GEORGIA', 30604], ['NDK', 30606]]
        self.assertEqual(result, expected, "Problem with test for state, report")

    def test_zip(self):
        """Test for the zip column, including correct cells, formatting errors, and blanks"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['GA', '30601'], ['MS', '306024444'], ['GA', '30603-0001'], ['TX', 'no zip'],
                           ['GA', np.nan], ['DC', 'no zip'], ['GA', np.nan], ['MO', '3060'], ['GA', '30603-XXXX']],
                          columns=['state', 'zip'])
        state_mismatch = check_metadata_formatting('zip', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(state_mismatch, 4, "Problem with test for zip, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_zip.csv'))
        expected = [['state', 'zip'], ['MS', '306024444'], ['TX', 'no zip'], ['DC', 'no zip'], ['MO', '3060']]
        self.assertEqual(result, expected, "Problem with test for zip, report")

    def test_no_errors(self):
        """Test for the column has no formatting errors, which would be the same for any column"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['GA', '30601'], ['MS', '38602'], ['GA', '30603-0001'], ['TX', '76621']],
                          columns=['state', 'zip'])
        state_mismatch = check_metadata_formatting('zip', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(state_mismatch, 0, "Problem with test for no errors, count")

        # Tests the report was not made.
        result = os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_zip.csv'))
        expected = False
        self.assertEqual(result, expected, "Problem with test for no errors, report")


if __name__ == '__main__':
    unittest.main()
