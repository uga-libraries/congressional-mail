import numpy as np
import pandas as pd
import unittest
from css_archiving_format import df_search
from test_read_metadata import df_to_list


def make_df(rows):
    """Make a df to use for test input"""
    column_names = ['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_topic', 'out_text', 'out_document_name', 'out_fillin']
    df = pd.DataFrame(rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def test_keyword_none(self):
        """Test for a single keyword that is not in any of the searched columns"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'abc', '', '', '', '', '', '', ''],
                ['30601', '', '', '', '', '', '', '', 'text'],
                ['30602-one', '', '', np.nan, '', '', np.nan, '', '']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one'], 'one_cat')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for keyword_none, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['30600', 'abc', '', '', '', '', '', '', ''],
                    ['30601', '', '', '', '', '', '', '', 'text'],
                    ['30602-one', '', '', 'blank', '', '', 'blank', '', '']]
        self.assertEqual(expected, result, "Problem with test for keyword_none, df_no_match")

    def test_keyword_one(self):
        """Test for a single keyword that is in one of the searched columns per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'ONE', '', '', '', '', '', '', ''],
                ['30601', '', 'one_text', '', '', '', '', '', ''],
                ['30602', '', '', 'path\\One.doc', '', '', '', '', ''],
                ['30603', '', '', '', 'fill one', '', '', '', ''],
                ['30604', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ['30605', '', '', '', '', '', '', '', ''],
                ['30606', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                ['30607', '', '', '', '', 'ONE', '', '', ''],
                ['30608', '', '', '', '', '', 'one_text', '', ''],
                ['30609', '', '', '', '', '', '', 'path\\One.doc', ''],
                ['30610', '', '', '', '', '', '', '', 'fill one']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one'], 'one_cat')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'ONE', '', '', '', '', '', '', '', 'one_cat'],
                    ['30601', '', 'one_text', '', '', '', '', '', '', 'one_cat'],
                    ['30602', '', '', 'path\\One.doc', '', '', '', '', '', 'one_cat'],
                    ['30603', '', '', '', 'fill one', '', '', '', '', 'one_cat'],
                    ['30607', '', '', '', '', 'ONE', '', '', '', 'one_cat'],
                    ['30608', '', '', '', '', '', 'one_text', '', '', 'one_cat'],
                    ['30609', '', '', '', '', '', '', 'path\\One.doc', '', 'one_cat'],
                    ['30610', '', '', '', '', '', '', '', 'fill one', 'one_cat']]
        self.assertEqual(expected, result, "Problem with test for keyword_one, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['30604', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank'],
                    ['30605', '', '', '', '', '', '', '', ''],
                    ['30606', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(expected, result, "Problem with test for keyword_one, df_no_match")

    def test_keyword_multiple(self):
        """Test for a single keyword that is in more than one searched column per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'ONE', 'one_text', '', np.nan, '', '', '', np.nan],
                ['30601', '', '', 'path\\One.doc', 'fill one', 'ONE', '', '', ''],
                ['30602', '', '', '', '', '', '', '', ''],
                ['30603', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ['30604', '', 'ONE ONE', '', '', '', 'one_text', 'path\\One.doc', 'fill one'],
                ['30605', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                ['30606', 'one', 'one', 'one', 'one', 'one', 'one', 'one', 'one']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one'], 'one_cat')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'ONE', 'one_text', '', 'blank', '', '', '', 'blank', 'one_cat'],
                    ['30601', '', '', 'path\\One.doc', 'fill one', 'ONE', '', '', '', 'one_cat'],
                    ['30604', '', 'ONE ONE', '', '', '', 'one_text', 'path\\One.doc', 'fill one', 'one_cat'],
                    ['30606', 'one', 'one', 'one', 'one', 'one', 'one', 'one', 'one', 'one_cat']]
        self.assertEqual(expected, result, "Problem with test for keyword_multiple, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['30602', '', '', '', '', '', '', '', ''],
                    ['30603', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank'],
                    ['30605', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(expected, result, "Problem with test for keyword_multiple, df_no_match")

    def test_keywords_none(self):
        """Test for multiple keywords that are not in any of the searched columns"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600-one', 'abc', '', '', '', '', '', '', ''],
                ['30601-onetwo', '', '', '', '', '', '', '', 'text'],
                ['30602-three', '', '', np.nan, '', '', np.nan, '', '']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one', 'two', 'three'], 'cats')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for keywords_none, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['30600-one', 'abc', '', '', '', '', '', '', ''],
                    ['30601-onetwo', '', '', '', '', '', '', '', 'text'],
                    ['30602-three', '', '', 'blank', '', '', 'blank', '', '']]
        self.assertEqual(expected, result, "Problem with test for keywords_none, df_no_match")

    def test_keywords_one(self):
        """Test for multiple keywords that are in one of the searched columns per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'ONE', '', '', '', '', '', '', ''],
                ['30601', '', 'two_text', '', '', '', '', '', ''],
                ['30602', '', '', 'path\\Three.doc', '', '', '', '', ''],
                ['30603', '', '', '', 'fill one two', '', '', '', ''],
                ['30604', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ['30605', '', '', '', '', '', '', '', ''],
                ['30606', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                ['30607', '', '', '', '', 'ONE', '', '', ''],
                ['30608', '', '', '', '', '', 'two_text', '', ''],
                ['30609', '', '', '', '', '', '', 'path\\Three.doc', ''],
                ['30610', '', '', '', '', '', '', '', 'fill one two']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one', 'two', 'three'], 'cats')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'ONE', '', '', '', '', '', '', '', 'cats'],
                    ['30601', '', 'two_text', '', '', '', '', '', '', 'cats'],
                    ['30602', '', '', 'path\\Three.doc', '', '', '', '', '', 'cats'],
                    ['30603', '', '', '', 'fill one two', '', '', '', '', 'cats'],
                    ['30607', '', '', '', '', 'ONE', '', '', '', 'cats'],
                    ['30608', '', '', '', '', '', 'two_text', '', '', 'cats'],
                    ['30609', '', '', '', '', '', '', 'path\\Three.doc', '', 'cats'],
                    ['30610', '', '', '', '', '', '', '', 'fill one two', 'cats']]
        self.assertEqual(expected, result, "Problem with test for keywords_one, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['30604', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank'],
                    ['30605', '', '', '', '', '', '', '', ''],
                    ['30606', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(expected, result, "Problem with test for keywords_one, df_no_match")

    def test_keywords_multiple(self):
        """Test for multiple keywords that are in more than one searched column per row"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'ONE', 'one_text', '', np.nan, '', '', '', np.nan],
                ['30601', '', '', 'path\\Two.doc', 'fill two', 'TWO', '', '', ''],
                ['30602', '', '', '', '', '', '', '', ''],
                ['30603', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ['30604', '', 'THREE THREE', '', '', '', 'three_text', 'path\\Three.doc', 'fill three'],
                ['30605', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                ['30606', 'one', 'two', 'three', 'one two three', 'one', 'two', 'three', 'one']]
        df = make_df(rows)
        df_match, df_no_match = df_search(df, ['one', 'two', 'three'], 'cats')

        # Tests the values in df_match are correct.
        result = df_to_list(df_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'ONE', 'one_text', '', 'blank', '', '', '', 'blank', 'cats'],
                    ['30601', '', '', 'path\\Two.doc', 'fill two', 'TWO', '', '', '', 'cats'],
                    ['30604', '', 'THREE THREE', '', '', '', 'three_text', 'path\\Three.doc', 'fill three', 'cats'],
                    ['30606', 'one', 'two', 'three', 'one two three', 'one', 'two', 'three', 'one', 'cats']]
        self.assertEqual(expected, result, "Problem with test for keywords_multiple, df_match")

        # Tests the values in df_no_match are correct.
        result = df_to_list(df_no_match)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['30602', '', '', '', '', '', '', '', ''],
                    ['30603', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank'],
                    ['30605', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(expected, result, "Problem with test for keywords_multiple, df_no_match")


if __name__ == '__main__':
    unittest.main()
