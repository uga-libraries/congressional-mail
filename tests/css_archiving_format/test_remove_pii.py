import pandas as pd
import unittest
from css_archiving_format import remove_pii


class MyTestCase(unittest.TestCase):

    def test_all_present(self):
        """Test for when all PII columns are present."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                               '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']],
                             columns=['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
                                      'addr1', 'addr2', 'addr3', 'addr4', 'city', 'state', 'zip', 'in_id', 'in_text',
                                      'in_fillin', 'out_id', 'out_text', 'out_fillin'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['city', 'state', 'zip', 'in_id', 'out_id']
        self.assertEqual(expected, md_df.columns.tolist(), "Problem with test for all present, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['13', '14', '15', '16', '19']]
        self.assertEqual(expected, md_df.values.tolist(), "Problem with test for all present, values")

    def test_some_present(self):
        """Test for when some PII columns are present."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6']],
                             columns=['in_type', 'first', 'last', 'title', 'country', 'addr1'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['in_type', 'country']
        self.assertEqual(expected, md_df.columns.tolist(), "Problem with test for some present, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['1', '5']]
        self.assertEqual(expected, md_df.values.tolist(), "Problem with test for some present, values")

    def test_none_present(self):
        """Test for when no PII columns are present."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4'], ['11', '12', '13', '14']],
                             columns=['zip', 'country', 'in_id', 'out_id'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['zip', 'country', 'in_id', 'out_id']
        self.assertEqual(expected, md_df.columns.tolist(), "Problem with test for none present, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['1', '2', '3', '4'], ['11', '12', '13', '14']]
        self.assertEqual(expected, md_df.values.tolist(), "Problem with test for none present, values")


if __name__ == '__main__':
    unittest.main()
