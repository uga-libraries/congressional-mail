import numpy as np
import unittest
from cms_data_interchange_format import df_search_exact
from test_df_search import make_df
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_one_column(self):
        """Test for a single keyword that is in one of the searched columns per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', np.nan, np.nan, np.nan],
                ['30601', 'case', '', ''],
                ['30602', '', 'case!', ''],
                ['30603', '', '', 'CASE'],
                ['30604', '', 'CASE!', ''],
                ['30605', 'x', 'x', 'x'],
                ['30606', '', '', '']]
        df = make_df(rows)
        keyword_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, keyword_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30601', 'case', '', '', 'Casework'],
                    ['30602', '', 'case!', '', 'Casework'],
                    ['30603', '', '', 'CASE', 'Casework'],
                    ['30604', '', 'CASE!', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for one_column, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'],
                    ['30600', 'BLANK', 'BLANK', 'BLANK'],
                    ['30605', 'x', 'x', 'x'],
                    ['30606', '', '', '']]
        self.assertEqual(expected, result, "Problem with test for one_column, df_no_match")

    def test_multiple_columns(self):
        """Test for a single keyword that is in more than one searched column per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', np.nan, np.nan, np.nan],
                ['30601', 'case', 'case', 'case'],
                ['30602', 'CASE', 'Case!', ''],
                ['30603', 'Case', '', 'Case'],
                ['30604', '', 'Case!', 'Case!'],
                ['30605', 'x', 'x', 'x'],
                ['30606', '', '', '']]
        df = make_df(rows)
        keyword_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, keyword_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30601', 'case', 'case', 'case', 'Casework'],
                    ['30602', 'CASE', 'Case!', '', 'Casework'],
                    ['30603', 'Case', '', 'Case', 'Casework'],
                    ['30604', '', 'Case!', 'Case!', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for multiple_columns, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'],
                    ['30600', 'BLANK', 'BLANK', 'BLANK'],
                    ['30605', 'x', 'x', 'x'],
                    ['30606', '', '', '']]
        self.assertEqual(expected, result, "Problem with test for multiple_columns, df_no_match")

    def test_none(self):
        """Test for a single keyword that is not in any of the searched columns"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', np.nan, ''],
                ['30601-case', '', '', ''],
                ['30602', '', '', '']]
        df = make_df(rows)
        keyword_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, keyword_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'],
                    ['30600', '', 'BLANK', ''],
                    ['30601-case', '', '', ''],
                    ['30602', '', '', '']]
        self.assertEqual(expected, result, "Problem with test for none, df_no_match")

    def test_partial(self):
        """Test for a keyword that partially matches, but that isn't enough for a match"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'CASE.TXT', '', ''],
                ['30601', '', 'A Case!!', ''],
                ['30602', '', '', 'admin^case']]
        df = make_df(rows)
        keyword_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, keyword_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for partial, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'],
                    ['30600', 'CASE.TXT', '', ''],
                    ['30601', '', 'A Case!!', ''],
                    ['30602', '', '', 'admin^case']]
        self.assertEqual(expected, result, "Problem with test for partial, df_no_match")


if __name__ == '__main__':
    unittest.main()
