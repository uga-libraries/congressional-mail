"""
Tests for the function find_casework_rows(), 
which finds metadata rows with topics or text that indicate they are casework and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_archiving_format import find_casework_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_all_casework(self):
        """Test for when every row is casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Casework Issues', ''],
                              ['30601', 'Health', 'This is casework'],
                              ['30602', 'Prison Case', '']],
                             columns=['zip', 'in_topic', 'in_text'])
        df_casework = find_casework_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'Appraisal_Category'],
                    ['30600', 'Casework Issues', '', 'Casework'],
                    ['30602', 'Prison Case', '', 'Casework'],
                    ['30601', 'Health', 'This is casework', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for all casework")

    def test_case_phase(self):
        """Test for when a column contains a phrase that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'I added to case'],
                              ['30601', '', 'Already opened a case'],
                              ['30602', 'Closed Case', ''],
                              ['30603', 'Open Case', ''],
                              ['30604', '', 'Mary started case yesterday'],
                              ['30605', 'Roads', 'Not a case']],
                             columns=['zip', 'in_topic', 'in_text'])
        df_casework = find_casework_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'Appraisal_Category'],
                    ['30600', '', 'I added to case', 'Casework'],
                    ['30601', '', 'Already opened a case', 'Casework'],
                    ['30602', 'Closed Case', '', 'Casework'],
                    ['30603', 'Open Case', '', 'Casework'],
                    ['30604', '', 'Mary started case yesterday', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for case phrase")

    def test_casework_keyword(self):
        """Test for when a column contains the word casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'Just in case'],
                              ['30601', '', 'Outgoing Info: casework, letter is x'],
                              ['30602', '', 'Outgoing Info: letter is y'],
                              ['30603', '', 'Answer topic x, forwarded original on to case work'],
                              ['30604', '', 'Send down for casework'],
                              ['30605', '', 'This is not casework'],
                              ['casework', '', '']],
                             columns=['zip', 'in_topic', 'in_text'])
        df_casework = find_casework_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'Appraisal_Category'],
                    ['30601', '', 'Outgoing Info: casework, letter is x', 'Casework'],
                    ['30604', '', 'Send down for casework', 'Casework'],
                    ['30605', '', 'This is not casework', 'Casework'],
                    ['casework', '', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for casework keyword")

    def test_in_topic_exact(self):
        """Test for when the column in_topic exactly matches a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Casework', ''],
                              ['30601', 'Keep', 'note'],
                              ['30602', 'Casework Issues', ''],
                              ['30604', 'Prison Case', 'note']],
                             columns=['zip', 'in_topic', 'in_text'])
        df_casework = find_casework_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'Appraisal_Category'],
                    ['30600', 'Casework', '', 'Casework'],
                    ['30602', 'Casework Issues', '', 'Casework'],
                    ['30604', 'Prison Case', 'note', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for in_topic, exact match")

    def test_in_topic_partial(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Keep', 'CASE OF THE CENTURY'],
                              ['30601', 'Healthcare^Casework', ''],
                              ['30602', 'Casework Issues^Social Security', 'note'],
                              ['30603', 'Prison Case^No Reply', ''],
                              ['30604', 'Casework^Casework Issues', '']],
                             columns=['zip', 'in_topic', 'in_text'])
        df_casework = find_casework_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'Appraisal_Category'],
                    ['30601', 'Healthcare^Casework', '', 'Casework'],
                    ['30602', 'Casework Issues^Social Security', 'note', 'Casework'],
                    ['30603', 'Prison Case^No Reply', '', 'Casework'],
                    ['30604', 'Casework^Casework Issues', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for in topic, partial match")

    def test_no_casework(self):
        """Test for when there are no indicators of casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Keep', ''],
                              ['30601', 'Healthcare', '']],
                             columns=['zip', 'in_topic', 'in_text'])
        df_casework = find_casework_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for no casework")


if __name__ == '__main__':
    unittest.main()
