"""
Tests for the function remove_casework(), which removes rows that pertain to casework.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from archival_office_correspondence_data import remove_casework
from test_script import csv_to_list


def df_to_list(df):
    """Convert a dataframe to a list for easier comparison"""
    df.fillna('nan', inplace=True)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the deletion log, if made by the test"""
        log_path = os.path.join('test_data', 'metadata_deletion_log.csv')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_casework_all(self):
        """Test for when every row contains the word case and is deleted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'ITEM', 'PR', 'I AM ON THE CASE'],
                              ['30601', 'ITEM', 'CASE', ''],
                              ['30602', 'ITEM', ', CASE', ''],
                              ['30603', 'ITEM', 'OF-GEN, CASE', ''],
                              ['30604', 'ITEM', 'TR-RAL', 'SENT TO CASEWORK'],
                              ['30605', 'ITEM', 'TR-RAL', 'SENT TO CASE WORK, ATL'],
                              ['30606', 'ITEM', 'TR-RAL', 'CASE'],
                              ['30607', 'CASE WORK', '', ''],
                              ['CASEWORK', '', '', '']],
                             columns=['zip_code', 'correspondence_type', 'correspondence_topic', 'comments'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'comments']]
        self.assertEqual(result, expected, "Problem with test for casework - all, df")

        # Tests the values in the metadata deletion log are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_deletion_log.csv'))
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'comments'],
                    ['30600', 'ITEM', 'PR', 'I AM ON THE CASE'],
                    ['30601', 'ITEM', 'CASE', 'nan'],
                    ['30602', 'ITEM', ', CASE', 'nan'],
                    ['30603', 'ITEM', 'OF-GEN, CASE', 'nan'],
                    ['30604', 'ITEM', 'TR-RAL', 'SENT TO CASEWORK'],
                    ['30605', 'ITEM', 'TR-RAL', 'SENT TO CASE WORK, ATL'],
                    ['30606', 'ITEM', 'TR-RAL', 'CASE'],
                    ['30607', 'CASE WORK', 'nan', 'nan'],
                    ['CASEWORK', 'nan', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for casework - all, deletion log")

    def test_casework_some(self):
        """Test for when some rows contain the word case and is deleted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'ITEM', 'PR', 'I AM ON THE CASE'],
                              ['30601', 'ITEM', 'CASE', ''],
                              ['30602', 'ITEM', 'OF-GEN', 'NOTE'],
                              ['30603', 'ITEM', 'OF-GEN, CASE', ''],
                              ['30604', 'ITEM', 'TR-RAL', 'NOTE'],
                              ['30605', 'ITEM', 'TR-RAL', 'SENT TO CASE WORK, ATL']],
                             columns=['zip_code', 'correspondence_type', 'correspondence_topic', 'comments'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'comments'],
                    ['30602', 'ITEM', 'OF-GEN', 'NOTE'],
                    ['30604', 'ITEM', 'TR-RAL', 'NOTE']]
        self.assertEqual(result, expected, "Problem with test for casework - some, df")

        # Tests the values in the metadata deletion log are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_deletion_log.csv'))
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'comments'],
                    ['30600', 'ITEM', 'PR', 'I AM ON THE CASE'],
                    ['30601', 'ITEM', 'CASE', 'nan'],
                    ['30603', 'ITEM', 'OF-GEN, CASE', 'nan'],
                    ['30605', 'ITEM', 'TR-RAL', 'SENT TO CASE WORK, ATL']]
        self.assertEqual(result, expected, "Problem with test for casework - some, deletion log")

    def test_no_casework(self):
        """Test for when no rows contain the word case and nothing is deleted"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'ITEM', 'PR', 'I AM ON IT'],
                              ['30601', 'ITEM', 'OF-GEN', 'NOTE'],
                              ['30602', 'ITEM', 'TR-RAL', 'NOTE'],
                              ['30603', 'ITEM', 'TR-RAL', 'SENT TO ATL']],
                             columns=['zip_code', 'correspondence_type', 'correspondence_topic', 'comments'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'correspondence_type', 'correspondence_topic', 'comments'],
                    ['30600', 'ITEM', 'PR', 'I AM ON IT'],
                    ['30601', 'ITEM', 'OF-GEN', 'NOTE'],
                    ['30602', 'ITEM', 'TR-RAL', 'NOTE'],
                    ['30603', 'ITEM', 'TR-RAL', 'SENT TO ATL']]
        self.assertEqual(result, expected, "Problem with test for no casework, df")

        # Tests the metadata deletion log was not made.
        result = os.path.exists(os.path.join('test_data', 'metadata_deletion_log.csv'))
        self.assertEqual(result, False, "Problem with test for no casework, deletion log")


if __name__ == '__main__':
    unittest.main()
