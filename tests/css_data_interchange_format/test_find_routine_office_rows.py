import numpy as np
import unittest
from css_data_interchange_format import find_routine_office_rows
from test_df_search import make_df
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_match(self):
        """Test for when all topics indicate routine office"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'congrats^scouts', 'x', 'y', 'z'],
                ['20250402', 'congrats^scouts', 'x', 'y', 'z'],
                ['20250403', 'Flag Request', 'x', 'y', 'z']]
        df = make_df(rows)
        df_routine = find_routine_office_rows(df)

        # Tests the values in df_routine are correct.
        result = df_to_list(df_routine)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'congrats^scouts', 'x', 'y', 'z', 'Routine_Office'],
                    ['20250402', 'congrats^scouts', 'x', 'y', 'z', 'Routine_Office'],
                    ['20250403', 'Flag Request', 'x', 'y', 'z', 'Routine_Office']]
        self.assertEqual(expected, result, "Problem with test for match")

    def test_match_partial(self):
        """Test for when some topics indicate routine office"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'Farm', 'x', 'y', 'z'],
                ['20250402', 'Flag Request', 'x', 'y', 'z'],
                ['20250403', 'Flag', 'x', 'y', 'z'],
                ['20250404', 'congrats^scouts', '', '', ''],
                ['20250405', 'Peanuts', 'x', 'y', 'z'],
                ['20250406', 'scouts', 'x', 'y', 'z']]
        df = make_df(rows)
        df_routine = find_routine_office_rows(df)

        # Tests the values in df_routine are correct.
        result = df_to_list(df_routine)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250402', 'Flag Request', 'x', 'y', 'z', 'Routine_Office'],
                    ['20250404', 'congrats^scouts', '', '', '', 'Routine_Office']]
        self.assertEqual(expected, result, "Problem with test for match_partial")

    def test_no_match(self):
        """Test for when no topics indicate routine office"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'congrats^election', 'x', 'y', 'z'],
                ['20250401', np.nan, 'x', 'y', 'z'],
                ['20250402', 'Admin', 'x', 'y', 'z'],
                ['20250401', '', 'x', 'y', 'z'],
                ['20250403', 'Apples', 'x', 'y', 'z']]
        df = make_df(rows)
        df_routine = find_routine_office_rows(df)

        # Tests the values in df_routine are correct.
        result = df_to_list(df_routine)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for no_match")


if __name__ == '__main__':
    unittest.main()
