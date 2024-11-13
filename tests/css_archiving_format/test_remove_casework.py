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
        paths = [os.path.join('test_data', 'text_deletion_log.csv'),
                 os.path.join('test_data', 'topic_deletion_log.csv')]
        for path in paths:
            if os.path.exists(path):
                os.remove(path)

    def test_in_text(self):
        """Test for when the column in_text contains a phrase that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'Letter case.prison'],
                              ['30601', '', 'Outgoing Info: casework, letter is x'],
                              ['30602', '', 'Outgoing Info: case work, letter is y'],
                              ['30603', '', 'Answer topic x, forwarded original on to case work'],
                              ['30604', '', 'Send down for casework'],
                              ['30605', '', 'This is not casework']],
                             columns=['zip', 'in_topic', 'in_text'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30605', '', 'This is not casework']]
        self.assertEqual(result, expected, "Problem with test for in_text, df")

        # Tests the values in the deletion log are correct.
        result = csv_to_list(os.path.join('test_data', 'text_deletion_log.csv'))
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'nan', 'Letter case.prison'],
                    ['30601', 'nan', 'Outgoing Info: casework, letter is x'],
                    ['30602', 'nan', 'Outgoing Info: case work, letter is y'],
                    ['30603', 'nan', 'Answer topic x, forwarded original on to case work'],
                    ['30604', 'nan', 'Send down for casework']]
        self.assertEqual(result, expected, "Problem with test for in_text, log")

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
        result = csv_to_list(os.path.join('test_data', 'topic_deletion_log.csv'))
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'Casework', 'nan'],
                    ['30602', 'Casework Issues', 'nan'],
                    ['30604', 'Prison Case', 'note']]
        self.assertEqual(result, expected, "Problem with test for in_topic, exact match, log")

    def test_in_topic_partial(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Keep', ''],
                              ['30601', 'Healthcare^Casework', ''],
                              ['30602', 'Casework Issues^Social Security', 'note'],
                              ['30603', 'Prison Case^No Reply', ''],
                              ['30604', 'Casework^Casework Issues', '']],
                             columns=['zip', 'in_topic', 'in_text'])
        md_df = remove_casework(md_df, 'test_data')

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30600', 'Keep', '']]
        self.assertEqual(result, expected, "Problem with test for in_topic, partial match, df")

        # Tests the values in the deletion log are correct.
        result = csv_to_list(os.path.join('test_data', 'topic_deletion_log.csv'))
        expected = [['zip', 'in_topic', 'in_text'],
                    ['30601', 'Healthcare^Casework', 'nan'],
                    ['30602', 'Casework Issues^Social Security', 'note'],
                    ['30603', 'Prison Case^No Reply', 'nan'],
                    ['30604', 'Casework^Casework Issues', 'nan']]
        self.assertEqual(result, expected, "Problem with test for in_topic, partial match, log")


if __name__ == '__main__':
    unittest.main()
