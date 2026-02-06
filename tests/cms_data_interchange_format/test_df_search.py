import numpy as np
import pandas as pd
import unittest
from cms_data_interchange_format import df_search
from test_read_metadata import df_to_list


def make_df(rows):
    """Make a df to use for test input"""
    column_names = ['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description']
    df = pd.DataFrame(rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def test_keyword_none(self):
        """Test for a single keyword that is not in any of the searched columns"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', np.nan, ''],
                ['30601-one', '', '', ''],
                ['30602', '', '', '']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one'], 'one_cat')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for keyword_none, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'],
                    ['30600', '', 'BLANK', ''],
                    ['30601-one', '', '', ''],
                    ['30602', '', '', '']]
        self.assertEqual(expected, result, "Problem with test for keyword_none, df_no_match")

    def test_keyword_one(self):
        """Test for a single keyword that is in one of the searched columns per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', np.nan, np.nan, np.nan],
                ['30601', 'ONE', '', ''],
                ['30602', '', 'OneA', ''],
                ['30603', '', '', 'b-one'],
                ['30604', '', 'XoneX', ''],
                ['30605', 'x', 'x', 'x'],
                ['30606', '', '', '']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one'], 'one_cat')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30601', 'ONE', '', '', 'one_cat'],
                    ['30602', '', 'OneA', '', 'one_cat'],
                    ['30603', '', '', 'b-one', 'one_cat'],
                    ['30604', '', 'XoneX', '', 'one_cat']]
        self.assertEqual(expected, result, "Problem with test for keyword_one, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'],
                    ['30600', 'BLANK', 'BLANK', 'BLANK'],
                    ['30605', 'x', 'x', 'x'],
                    ['30606', '', '', '']]
        self.assertEqual(expected, result, "Problem with test for keyword_one, df_no_match")

    def test_keyword_multiple(self):
        """Test for a single keyword that is in more than one searched column per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', np.nan, np.nan, np.nan],
                ['30601', 'ONE', 'OneA', ''],
                ['30602', '', 'OneA', 'XoneX'],
                ['30603', 'one', '', 'one'],
                ['30604', 'oner', 'onet', 'onex'],
                ['30605', 'x', 'x', 'x'],
                ['30606', '', '', '']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one'], 'one_cat')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30601', 'ONE', 'OneA', '', 'one_cat'],
                    ['30602', '', 'OneA', 'XoneX', 'one_cat'],
                    ['30603', 'one', '', 'one', 'one_cat'],
                    ['30604', 'oner', 'onet', 'onex', 'one_cat']]
        self.assertEqual(expected, result, "Problem with test for keyword_multiple, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'],
                    ['30600', 'BLANK', 'BLANK', 'BLANK'],
                    ['30605', 'x', 'x', 'x'],
                    ['30606', '', '', '']]
        self.assertEqual(expected, result, "Problem with test for keyword_multiple, df_no_match")

    def test_keywords_none(self):
        """Test for multiple keywords that are not in any of the searched columns"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', np.nan, np.nan, np.nan],
                ['30605_one', 'x', 'x', 'x'],
                ['30606', '', '', '']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one', 'two', 'three'], 'cats')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for keywords_none, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'],
                    ['30600', 'BLANK', 'BLANK', 'BLANK'],
                    ['30605_one', 'x', 'x', 'x'],
                    ['30606', '', '', '']]
        self.assertEqual(expected, result, "Problem with test for keywords_none, df_no_match")

    def test_keywords_one(self):
        """Test for multiple keywords that are in one of the searched columns per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', np.nan, np.nan, np.nan],
                ['30601', 'ONE', '', ''],
                ['30602', '', 'Two B', ''],
                ['30603', '', '', 'XthreeX'],
                ['30604', '', 'one', ''],
                ['30605', 'x', 'x', 'x'],
                ['30606', '', '', '']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one', 'two', 'three'], 'cats')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30601', 'ONE', '', '', 'cats'],
                    ['30602', '', 'Two B', '', 'cats'],
                    ['30603', '', '', 'XthreeX', 'cats'],
                    ['30604', '', 'one', '', 'cats']]
        self.assertEqual(expected, result, "Problem with test for keywords_one, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'],
                    ['30600', 'BLANK', 'BLANK', 'BLANK'],
                    ['30605', 'x', 'x', 'x'],
                    ['30606', '', '', '']]
        self.assertEqual(expected, result, "Problem with test for keywords_one, df_no_match")

    def test_keywords_multiple(self):
        """Test for multiple keywords that are in more than one searched column per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', np.nan, np.nan, np.nan],
                ['30601', 'ONE', 'TWO', ''],
                ['30602', 'oneA', 'Atwo', ''],
                ['30603', '', 'xtwox', 'xthreex'],
                ['30604', 'one one', 'two two', 'three'],
                ['30605', 'x', 'x', 'x'],
                ['30606', '', '', '']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one', 'two', 'three'], 'cats')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30601', 'ONE', 'TWO', '', 'cats'],
                    ['30602', 'oneA', 'Atwo', '', 'cats'],
                    ['30603', '', 'xtwox', 'xthreex', 'cats'],
                    ['30604', 'one one', 'two two', 'three', 'cats']]
        self.assertEqual(expected, result, "Problem with test for keywords_multiple, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'],
                    ['30600', 'BLANK', 'BLANK', 'BLANK'],
                    ['30605', 'x', 'x', 'x'],
                    ['30606', '', '', '']]
        self.assertEqual(expected, result, "Problem with test for keywords_multiple, df_no_match")


if __name__ == '__main__':
    unittest.main()
