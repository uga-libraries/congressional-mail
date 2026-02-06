import numpy as np
import pandas as pd
import unittest
from css_archiving_format import df_search_exact
from test_read_metadata import df_to_list


def make_df(rows):
    """Make a df to use for test input"""
    column_names = ['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin']
    df = pd.DataFrame(rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def test_one_column(self):
        """Test for when one of the searched columns matches a keyword exactly"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                ['30601', 'case', '', '', '', '', '', '', '', '', ''],
                ['30602', '', 'case!', '', '', '', '', '', '', '', ''],
                ['30603', '', '', 'CASE', '', '', '', '', '', '', ''],
                ['30604', '', '', '', 'CASE!', '', '', '', '', '', ''],
                ['30605', '', '', '', '', 'Case', '', '', '', '', ''],
                ['30606', '', '', '', '', '', '', '', '', '', ''],
                ['30607', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ['30608', '', '', '', '', '', 'case', '', '', '', ''],
                ['30609', '', '', '', '', '', '', 'case!', '', '', ''],
                ['30610', '', '', '', '', '', '', '', 'CASE', '', ''],
                ['30611', '', '', '', '', '', '', '', '', 'CASE!', ''],
                ['30612', '', '', '', '', '', '', '', '', '', 'Case!']]
        df = make_df(rows)
        keyword_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, keyword_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', 'case', '', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30602', '', 'case!', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30603', '', '', 'CASE', '', '', '', '', '', '', '', 'Casework'],
                    ['30604', '', '', '', 'CASE!', '', '', '', '', '', '', 'Casework'],
                    ['30605', '', '', '', '', 'Case', '', '', '', '', '', 'Casework'],
                    ['30608', '', '', '', '', '', 'case', '', '', '', '', 'Casework'],
                    ['30609', '', '', '', '', '', '', 'case!', '', '', '', 'Casework'],
                    ['30610', '', '', '', '', '', '', '', 'CASE', '', '', 'Casework'],
                    ['30611', '', '', '', '', '', '', '', '', 'CASE!', '', 'Casework'],
                    ['30612', '', '', '', '', '', '', '', '', '', 'Case!', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for one_column, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['30600', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['30606', '', '', '', '', '', '', '', '', '', ''],
                    ['30607', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank']]
        self.assertEqual(expected, result, "Problem with test for one_column, df_no_match")

    def test_multiple_columns(self):
        """Test for when more than one of the searched columns matches a keyword exactly"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                ['30601', 'case', 'case', 'CASE', 'CASE!', 'Case', '', '', '', '', ''],
                ['30602', '', 'case!', '', '', '', '', 'case!', '', '', ''],
                ['30603', '', '', 'CASE', np.nan, np.nan, 'case', '', '', '', 'case'],
                ['30604', '', '', '', '', '', '', '', '', '', ''],
                ['30605', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows)
        keyword_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, keyword_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', 'case', 'case', 'CASE', 'CASE!', 'Case', '', '', '', '', '', 'Casework'],
                    ['30602', '', 'case!', '', '', '', '', 'case!', '', '', '', 'Casework'],
                    ['30603', '', '', 'CASE', 'blank', 'blank', 'case', '', '', '', 'case', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for multiple_columns, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['30600', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['30604', '', '', '', '', '', '', '', '', '', ''],
                    ['30605', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank']]
        self.assertEqual(expected, result, "Problem with test for multiple_columns, df_no_match")

    def test_none(self):
        """Test for when none of the searched columns matches a keyword exactly"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                ['30601', '', '', '', '', '', '', '', '', '', ''],
                ['30602', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows)
        keyword_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, keyword_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['30600', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['30601', '', '', '', '', '', '', '', '', '', ''],
                    ['30602', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank']]
        self.assertEqual(expected, result, "Problem with test for none, df_no_match")

    def test_partial(self):
        """Test for when one of the searched columns partially equals a keyword, which is not enough for a match"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                ['30601', 'a case', '', '', '', '', '', '', '', '', ''],
                ['30602', '', 'Case!!', '', '', '', '', '', '', '', ''],
                ['30603', '', '', 'cAsE', '', '', '', '', '', '', ''],
                ['30604', '', '', '', 'ENCASED', '', '', '', '', '', ''],
                ['30605', '', '', '', '', '', '', '', '', '', ''],
                ['30606', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows)
        keyword_list = ['CASE', 'Case', 'case', 'CASE!', 'Case!', 'case!']
        df_match, df_no_match = df_search_exact(df, keyword_list, 'Casework')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for partial, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['30600', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['30601', 'a case', '', '', '', '', '', '', '', '', ''],
                    ['30602', '', 'Case!!', '', '', '', '', '', '', '', ''],
                    ['30603', '', '', 'cAsE', '', '', '', '', '', '', ''],
                    ['30604', '', '', '', 'ENCASED', '', '', '', '', '', ''],
                    ['30605', '', '', '', '', '', '', '', '', '', ''],
                    ['30606', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank']]
        self.assertEqual(expected, result, "Problem with test for partial, df_no_match")


if __name__ == '__main__':
    unittest.main()
