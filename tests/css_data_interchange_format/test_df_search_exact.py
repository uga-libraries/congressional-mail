import numpy as np
import unittest
from css_data_interchange_format import df_search_exact
from test_df_search import make_df
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_one_column(self):
        """Test for when one of the searched columns matches a keyword exactly"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250201', 'case', '', '', ''],
                ['20250202', '', 'CASE', '', ''],
                ['20250203', 'x', 'x', 'x', 'x'],
                ['20250204', '', '', '', ''],
                ['20250205', np.nan, np.nan, np.nan, np.nan],
                ['20250206', '', '', 'case!', ''],
                ['20250207', '', '', '', 'CASE!']]
        df = make_df(rows)
        exact_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, exact_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250201', 'case', '', '', '', 'Casework'],
                    ['20250202', '', 'CASE', '', '', 'Casework'],
                    ['20250206', '', '', 'case!', '', 'Casework'],
                    ['20250207', '', '', '', 'CASE!', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for one_column, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'],
                    ['20250203', 'x', 'x', 'x', 'x'],
                    ['20250204', '', '', '', ''],
                    ['20250205', 'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for one_column, df_no_match")

    def test_multiple_columns(self):
        """Test for when one of the searched columns matches a keyword exactly"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250201', 'case', 'Case', 'CASE', 'case'],
                ['20250202', 'case!', 'Case!', 'CASE!', 'case!'],
                ['20250203', 'x', 'x', 'x', 'x'],
                ['20250204', 'Case', '', 'Case', ''],
                ['20250205', np.nan, np.nan, np.nan, np.nan],
                ['20250206', '', 'Case!', '', 'Case!'],
                ['20250207', '', '', '', '']]
        df = make_df(rows)
        exact_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, exact_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250201', 'case', 'Case', 'CASE', 'case', 'Casework'],
                    ['20250202', 'case!', 'Case!', 'CASE!', 'case!', 'Casework'],
                    ['20250204', 'Case', '', 'Case', '', 'Casework'],
                    ['20250206', '', 'Case!', '', 'Case!', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for multiple_columns, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'],
                    ['20250203', 'x', 'x', 'x', 'x'],
                    ['20250205', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['20250207', '', '', '', '']]
        self.assertEqual(expected, result, "Problem with test for multiple_columns, df_no_match")

    def test_none(self):
        """Test for when none of the searched columns matches a keyword exactly"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250201', np.nan, np.nan, np.nan, np.nan],
                ['20250202', '', '', '', ''],
                ['20250203', 'x', 'x', 'x', 'x']]
        df = make_df(rows)
        exact_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, exact_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'],
                    ['20250201', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['20250202', '', '', '', ''],
                    ['20250203', 'x', 'x', 'x', 'x']]
        self.assertEqual(expected, result, "Problem with test for none, df_no_match")

    def test_partial(self):
        """Test for when one of the searched columns partially equals a keyword, which is not enough for a match"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250201', 'a case', '', '', ''],
                ['20250202', '', 'Case!!', '', ''],
                ['20250203', 'x', 'x', 'x', 'x'],
                ['20250204', '', '', 'cAsE', ''],
                ['20250205', np.nan, np.nan, np.nan, np.nan],
                ['20250206', '', '', '', 'ENCASED']]
        df = make_df(rows)
        exact_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, exact_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for partial, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'],
                    ['20250201', 'a case', '', '', ''],
                    ['20250202', '', 'Case!!', '', ''],
                    ['20250203', 'x', 'x', 'x', 'x'],
                    ['20250204', '', '', 'cAsE', ''],
                    ['20250205', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['20250206', '', '', '', 'ENCASED']]
        self.assertEqual(expected, result, "Problem with test for partial, df_no_match")


if __name__ == '__main__':
    unittest.main()
