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
        md_df = pd.DataFrame([['30600', 'Casework Issues', '', ''],
                              ['30601', 'Health', 'This is casework', 'Medical'],
                              ['30602', 'Prison Case', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category'],
                    ['30600', 'Casework Issues', '', '', 'Casework'],
                    ['30602', 'Prison Case', '', '', 'Casework'],
                    ['30601', 'Health', 'This is casework', 'Medical', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for all casework, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for all casework, df_casework_check")

    def test_casework(self):
        """Test for when a column contains the word casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'Just in case', ''],
                              ['30601', '', 'Outgoing Info: casework, letter is x', ''],
                              ['30602', '', 'Outgoing Info: letter is y', ''],
                              ['30603', '', 'Answer topic x, forwarded original on to case work', ''],
                              ['30604', '', 'Send down for casework', ''],
                              ['30605', '', 'This is not casework', ''],
                              ['casework', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category'],
                    ['30601', '', 'Outgoing Info: casework, letter is x', '', 'Casework'],
                    ['30604', '', 'Send down for casework', '', 'Casework'],
                    ['30605', '', 'This is not casework', '', 'Casework'],
                    ['casework', '', '', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for casework, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category'],
                    ['30600', '', 'Just in case', '', 'Casework'],
                    ['30603', '', 'Answer topic x, forwarded original on to case work', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for casework, df_casework_check")

    def test_in_topic(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Casework', '', 'Admin'],
                              ['30601', 'Keep', 'note', ''],
                              ['30602', 'Casework Issues', '', 'Admin'],
                              ['30603', 'Prison Case', 'note', 'Justice'],
                              ['30604', 'Healthcare^Casework', '', 'Health'],
                              ['30605', 'Casework Issues^Social Security', 'note', 'SSA'],
                              ['30606', 'Prison Case^No Reply', '', 'Justice'],
                              ['30607', 'Keep', 'CASE OF THE CENTURY', 'Legal'],
                              ['30608', 'Casework^Casework Issues', '', 'Admin']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category'],
                    ['30600', 'Casework', '', 'Admin', 'Casework'],
                    ['30602', 'Casework Issues', '', 'Admin', 'Casework'],
                    ['30603', 'Prison Case', 'note', 'Justice', 'Casework'],
                    ['30604', 'Healthcare^Casework', '', 'Health', 'Casework'],
                    ['30605', 'Casework Issues^Social Security', 'note', 'SSA', 'Casework'],
                    ['30606', 'Prison Case^No Reply', '', 'Justice', 'Casework'],
                    ['30608', 'Casework^Casework Issues', '', 'Admin', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for in_topic, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category'],
                    ['30607', 'Keep', 'CASE OF THE CENTURY', 'Legal', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for in_topic, df_casework_check")

    def test_none(self):
        """Test for when there are no indicators of casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Keep', '', 'Keep'],
                              ['30601', 'Healthcare', '', 'Healthcare']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no patterns matched), df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no patterns matched), df_casework_check")

    def test_out_topic(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Admin', '', 'Casework'],
                              ['30601', 'Admin', '', 'Healthcare^Casework'],
                              ['30602', 'SSA', 'note', 'Casework Issues^Social Security'],
                              ['30603', '', '', 'Prison Case'],
                              ['30604', '', '', 'Casework^Casework Issues'],
                              ['30605', 'Admin', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category'],
                    ['30600', 'Admin', '', 'Casework', 'Casework'],
                    ['30601', 'Admin', '', 'Healthcare^Casework', 'Casework'],
                    ['30602', 'SSA', 'note', 'Casework Issues^Social Security', 'Casework'],
                    ['30603', '', '', 'Prison Case', 'Casework'],
                    ['30604', '', '', 'Casework^Casework Issues', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for out_topic, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for out_topic, df_casework_check")

    def test_phase(self):
        """Test for when a column contains a phrase that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'I added to case', ''],
                              ['30601', '', 'Already opened a case', ''],
                              ['30602', 'Closed Case', '', ''],
                              ['30603', 'Open Case', '', ''],
                              ['30604', '', 'Mary started case yesterday', 'Admin'],
                              ['30605', 'Roads', 'Not a case', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category'],
                    ['30600', '', 'I added to case', '', 'Casework'],
                    ['30601', '', 'Already opened a case', '', 'Casework'],
                    ['30602', 'Closed Case', '', '', 'Casework'],
                    ['30603', 'Open Case', '', '', 'Casework'],
                    ['30604', '', 'Mary started case yesterday', 'Admin', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for phrase, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'Appraisal_Category'],
                    ['30605', 'Roads', 'Not a case', '', 'Casework']]
        self.assertEqual(result, expected, "Problem with test for phrase, df_casework_check")


if __name__ == '__main__':
    unittest.main()
