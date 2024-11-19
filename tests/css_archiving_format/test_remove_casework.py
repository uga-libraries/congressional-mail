"""
Tests for the function remove_casework(), which removes rows that pertain to casework.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import unittest
from css_archiving_format import remove_casework
from test_script import csv_to_list


def df_to_list(df):
    """Convert a dataframe to a list for easier comparison"""
    df.fillna('nan', inplace=True)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the deletion log, if made by the test"""
        paths = [os.path.join('test_data', 'deletion_log.csv'),
                 os.path.join('test_data', 'row_includes_case_log.csv')]
        for path in paths:
            if os.path.exists(path):
                os.remove(path)

    def test_all_casework(self):
        """Test for when every row is casework (all deleted)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Casework Issues', ''],
                              ['30601', 'Health', 'This is casework'],
                              ['30602', 'Prison Case', '']],
                             columns=['zip', 'in_topic', 'in_text'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the returned dataframe is empty (columns only).
        result = df_to_list(md_df)
        expected = [['zip', 'in_topic', 'in_text']]
        self.assertEqual(result, expected, "Problem with test for all casework, df")

        # Tests the values in the deletion log are correct.
        result = csv_to_list(os.path.join('test_data', 'deletion_log.csv'))
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'Casework Issues', 'nan'],
                    ['30602', 'Prison Case', 'nan'],
                    ['30601', 'Health', 'This is casework']]
        self.assertEqual(result, expected, "Problem with test for all casework, deletion log")

        # Tests that no case log was made.
        result = os.path.exists(os.path.join('test_data', 'row_includes_case_log.csv'))
        self.assertEqual(result, False, "Problem with test for in_topic, exact match, case log")

    def test_casework_keyword(self):
        """Test for when a column contains the word casework (is deleted)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'Just in case'],
                              ['30601', '', 'Outgoing Info: casework, letter is x'],
                              ['30602', '', 'Outgoing Info: letter is y'],
                              ['30603', '', 'Answer topic x, forwarded original on to case work'],
                              ['30604', '', 'Send down for casework'],
                              ['30605', '', 'This is not casework'],
                              ['casework', '', '']],
                             columns=['zip', 'in_topic', 'in_text'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', '', 'Just in case'],
                    ['30602', '', 'Outgoing Info: letter is y'],
                    ['30603', '', 'Answer topic x, forwarded original on to case work']]
        self.assertEqual(result, expected, "Problem with test for casework keyword, df")

        # Tests the values in the deletion log are correct.
        result = csv_to_list(os.path.join('test_data', 'deletion_log.csv'))
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30601', 'nan', 'Outgoing Info: casework, letter is x'],
                    ['30604', 'nan', 'Send down for casework'],
                    ['30605', 'nan', 'This is not casework'],
                    ['casework', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for casework keyword, deletion log")

        # Tests the values of the row includes case log are correct.
        result = csv_to_list(os.path.join('test_data', 'row_includes_case_log.csv'))
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'nan', 'Just in case'],
                    ['30603', 'nan', 'Answer topic x, forwarded original on to case work']]
        self.assertEqual(result, expected, "Problem with test for casework keyword, case log")

    def test_in_topic_exact(self):
        """Test for when the column in_topic exactly matches a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Casework', ''],
                              ['30601', 'Keep', 'note'],
                              ['30602', 'Casework Issues', ''],
                              ['30604', 'Prison Case', 'note']],
                             columns=['zip', 'in_topic', 'in_text'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30601', 'Keep', 'note']]
        self.assertEqual(result, expected, "Problem with test for in_topic, exact match, df")

        # Tests the values in the deletion log are correct.
        result = csv_to_list(os.path.join('test_data', 'deletion_log.csv'))
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'Casework', 'nan'],
                    ['30602', 'Casework Issues', 'nan'],
                    ['30604', 'Prison Case', 'note']]
        self.assertEqual(result, expected, "Problem with test for in_topic, exact match, deletion log")

        # Tests that no case log was made.
        result = os.path.exists(os.path.join('test_data', 'row_includes_case_log.csv'))
        self.assertEqual(result, False, "Problem with test for in_topic, exact match, case log")

    def test_in_topic_partial(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Keep', 'CASE OF THE CENTURY'],
                              ['30601', 'Healthcare^Casework', ''],
                              ['30602', 'Casework Issues^Social Security', 'note'],
                              ['30603', 'Prison Case^No Reply', ''],
                              ['30604', 'Casework^Casework Issues', '']],
                             columns=['zip', 'in_topic', 'in_text'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'Keep', 'CASE OF THE CENTURY']]
        self.assertEqual(result, expected, "Problem with test for in_topic, partial match, df")

        # Tests the values in the deletion log are correct.
        result = csv_to_list(os.path.join('test_data', 'deletion_log.csv'))
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30601', 'Healthcare^Casework', 'nan'],
                    ['30602', 'Casework Issues^Social Security', 'note'],
                    ['30603', 'Prison Case^No Reply', 'nan'],
                    ['30604', 'Casework^Casework Issues', 'nan']]
        self.assertEqual(result, expected, "Problem with test for in_topic, partial match, deletion log")

        # Tests the values of the row includes case log are correct.
        result = csv_to_list(os.path.join('test_data', 'row_includes_case_log.csv'))
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'Keep', 'CASE OF THE CENTURY']]
        self.assertEqual(result, expected, "Problem with test for in_topic, partial match, case log")

    def test_no_casework(self):
        """Test for when there are no indicators of casework, so the logs are not made"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Keep', ''],
                              ['30601', 'Healthcare', '']],
                             columns=['zip', 'in_topic', 'in_text'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'Keep', ''],
                    ['30601', 'Healthcare', '']]
        self.assertEqual(result, expected, "Problem with test for no casework, df")

        # Tests that no deletion log was made.
        result = os.path.exists(os.path.join('test_data', 'deletion_log.csv'))
        self.assertEqual(result, False, "Problem with test for no casework, deletion log")

        # Tests that no case log was made.
        result = os.path.exists(os.path.join('test_data', 'row_includes_case_log.csv'))
        self.assertEqual(result, False, "Problem with test for no casework, case log")


if __name__ == '__main__':
    unittest.main()
