"""
Tests for the function remove_pii(), which removes columns that contain personally identifiable information.
To simplify input, tests use dataframes with only some of the columns present in a real css/cms export
and the content is just numbers instead of reasonable data for the column types.
"""
import pandas as pd
import unittest
from metadata_update import remove_pii


class MyTestCase(unittest.TestCase):

    def test_all_present(self):
        """Test for when all PII columns are present."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]],
                             columns=['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
                                      'addr1', 'addr2', 'addr3', 'addr4', 'city', 'state', 'zip', 'in_id', 'out_id'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['zip', 'in_id', 'out_id']
        self.assertEqual(md_df.columns.tolist(), expected, "Problem with test for all present, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [[15, 16, 17]]
        self.assertEqual(md_df.values.tolist(), expected, "Problem with test for all present, values")

    def test_some_present(self):
        """Test for when some PII columns are present."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([[1, 2, 3, 4, 5, 6]],
                             columns=['in_type', 'first', 'last', 'title', 'country', 'addr1'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['in_type', 'country']
        self.assertEqual(md_df.columns.tolist(), expected, "Problem with test for some present, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [[1, 5]]
        self.assertEqual(md_df.values.tolist(), expected, "Problem with test for some present, values")

    def test_none_present(self):
        """Test for when no PII columns are present."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([[1, 2, 3, 4], [11, 12, 13, 14]],
                             columns=['zip', 'country', 'in_id', 'out_id'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['zip', 'country', 'in_id', 'out_id']
        self.assertEqual(md_df.columns.tolist(), expected, "Problem with test for none present, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [[1, 2, 3, 4], [11, 12, 13, 14]]
        self.assertEqual(md_df.values.tolist(), expected, "Problem with test for none present, values")


if __name__ == '__main__':
    unittest.main()
