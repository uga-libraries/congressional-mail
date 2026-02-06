import numpy as np
import pandas as pd
import unittest
from css_data_interchange_format import df_search
from test_read_metadata import df_to_list


def make_df(rows):
    """Make a df to use for test input"""
    column_names = ['date_in', 'group_name', 'communication_document_name', 'file_name', 'text']
    df = pd.DataFrame(rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def test_keyword_none(self):
        """Test for a single keyword that is not in any of the searched columns"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'Agriculture', '..\\documents\\farms.txt', 'farms.txt', ''],
                ['20250402-one', 'Legal', '..\\documents\\legal.txt', 'legal.txt', np.nan]]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one'], 'one_cat')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for keyword_none, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'],
                    ['20250401', 'Agriculture', '..\\documents\\farms.txt', 'farms.txt', ''],
                    ['20250402-one', 'Legal', '..\\documents\\legal.txt', 'legal.txt', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for keyword_none, df_no_match")

    def test_keyword_one(self):
        """Test for a single keyword that is in one of the searched columns per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'ONE', '', '', ''],
                ['20250402', '', 'one thing', '', ''],
                ['20250403', '', '', 'thing one', ''],
                ['20250404', '', '', '', 'thing one thing'],
                ['20240405', np.nan, np.nan, np.nan, 'one'],
                ['20240406', 'x', 'x', 'x', 'x'],
                ['20240407', '', '', '', ''],
                ['20240408', np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one'], 'one_cat')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'ONE', '', '', '', 'one_cat'],
                    ['20250402', '', 'one thing', '', '', 'one_cat'],
                    ['20250403', '', '', 'thing one', '', 'one_cat'],
                    ['20250404', '', '', '', 'thing one thing', 'one_cat'],
                    ['20240405', 'BLANK', 'BLANK', 'BLANK', 'one', 'one_cat']]
        self.assertEqual(expected, result, "Problem with test for keyword_one, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'],
                    ['20240406', 'x', 'x', 'x', 'x'],
                    ['20240407', '', '', '', ''],
                    ['20240408', 'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for keyword_one, df_no_match")

    def test_keyword_multiple(self):
        """Test for a single keyword that is in more than one searched column per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'one', 'one thing', '', ''],
                ['20250402', '', '', 'thing one', 'ONE'],
                ['20250403', 'thing one thing', 'oner', 'One', ''],
                ['20250404', 'one', 'one', 'one', 'one'],
                ['20240405', '', 'one one', '', 'one'],
                ['20240406', 'x', 'x', 'x', 'x'],
                ['20240407', '', '', '', ''],
                ['20240408', np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one'], 'one_cat')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'one', 'one thing', '', '', 'one_cat'],
                    ['20250402', '', '', 'thing one', 'ONE', 'one_cat'],
                    ['20250403', 'thing one thing', 'oner', 'One', '', 'one_cat'],
                    ['20250404', 'one', 'one', 'one', 'one', 'one_cat'],
                    ['20240405', '', 'one one', '', 'one', 'one_cat']]
        self.assertEqual(expected, result, "Problem with test for keyword_multiple, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'],
                    ['20240406', 'x', 'x', 'x', 'x'],
                    ['20240407', '', '', '', ''],
                    ['20240408', 'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for keyword_multiple, df_no_match")

    def test_keywords_none(self):
        """Test for multiple keywords that are not in any of the searched columns"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['one', 'abc', '', '', ''],
                ['onetwo', '', '', '', 'text'],
                ['three', '', '', np.nan, np.nan]]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one', 'two', 'three'], 'cats')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for keywords_none, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'],
                    ['one', 'abc', '', '', ''],
                    ['onetwo', '', '', '', 'text'],
                    ['three', '', '', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for keywords_none, df_no_match")

    def test_keywords_one(self):
        """Test for multiple keywords that are in one of the searched columns per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'ONE', '', '', ''],
                ['20250402', '', 'two thing', '', ''],
                ['20250403', '', '', 'thing_three', ''],
                ['20250404', '', '', '', 'Two'],
                ['20240405', '', '', '', 'THREE'],
                ['20240406', 'x', 'x', 'x', 'x'],
                ['20240407', '', '', '', ''],
                ['20240408', np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one', 'two', 'three'], 'cats')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'ONE', '', '', '', 'cats'],
                    ['20250402', '', 'two thing', '', '', 'cats'],
                    ['20250403', '', '', 'thing_three', '', 'cats'],
                    ['20250404', '', '', '', 'Two', 'cats'],
                    ['20240405', '', '', '', 'THREE', 'cats']]
        self.assertEqual(expected, result, "Problem with test for keywords_one, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'],
                    ['20240406', 'x', 'x', 'x', 'x'],
                    ['20240407', '', '', '', ''],
                    ['20240408', 'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for keywords_one, df_no_match")

    def test_keywords_multiple(self):
        """Test for multiple keywords that are in more than one searched column per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'one', 'two', 'three', ''],
                ['20250402', '', 'One Two', '', 'and Three'],
                ['20250403', 'ONE', 'TWO', '', 'THREE'],
                ['20250404', '', 'and one', '', 'and one thing'],
                ['20240405', '', 'OneTwoThree', '', 'three'],
                ['20240406', 'x', 'x', 'x', 'x'],
                ['20240407', '', '', '', ''],
                ['20240408', np.nan, np.nan, np.nan, np.nan]]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one', 'two', 'three'], 'cats')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'one', 'two', 'three', '', 'cats'],
                    ['20250402', '', 'One Two', '', 'and Three', 'cats'],
                    ['20250403', 'ONE', 'TWO', '', 'THREE', 'cats'],
                    ['20250404', '', 'and one', '', 'and one thing', 'cats'],
                    ['20240405', '', 'OneTwoThree', '', 'three', 'cats']]
        self.assertEqual(expected, result, "Problem with test for keywords_multiple, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'],
                    ['20240406', 'x', 'x', 'x', 'x'],
                    ['20240407', '', '', '', ''],
                    ['20240408', 'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for keywords_multiple, df_no_match")


if __name__ == '__main__':
    unittest.main()
