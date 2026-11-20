import pandas as pd
import numpy as np
import unittest
from cms_data_interchange_format import find_routine_office_rows
from test_read_metadata_file import df_to_list

# Before running these tests, change the topics_list in the function 
# to the standard test values ['Flag Request', 'congrats^scouts']

def make_df(rows):
    """Make a df to use for test input"""
    column_names = ['zip_code', 'code_description']
    df = pd.DataFrame(rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def test_match(self):
        """Test for when every topic matches one of the topics for routine office"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'Flag Request'],
                ['30601', 'congrats^scouts'],
                ['30602', 'Flag Request']]
        df = make_df(rows)
        df_routine = find_routine_office_rows(df)

        # Tests the values in df_routine are correct.
        result = df_to_list(df_routine)
        expected = [['zip_code', 'code_description', 'Appraisal_Category'],
                    ['30600', 'Flag Request', 'Routine_Office'],
                    ['30601', 'congrats^scouts', 'Routine_Office'],
                    ['30602', 'Flag Request', 'Routine_Office']]
        self.assertEqual(expected, result, "Problem with test for match")

    def test_match_partial(self):
        """Test for when some topics match one of the topics for routine office"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'Flag Request'],
                ['30601', 'CranFlag Request'],
                ['30602', ''],
                ['30603', 'congrats^scouts'],
                ['30604', 'OTHER']]
        df = make_df(rows)
        df_routine = find_routine_office_rows(df)

        # Tests the values in df_routine are correct.
        result = df_to_list(df_routine)
        expected = [['zip_code', 'code_description', 'Appraisal_Category'],
                    ['30600', 'Flag Request', 'Routine_Office'],
                    ['30603', 'congrats^scouts', 'Routine_Office']]
        self.assertEqual(expected, result, "Problem with test for match_partial")

    def test_no_match(self):
        """Test for when no topic matches one of the topics for routine office, including partial matches and blanks"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'pear'],
                ['30601', ''],
                ['30602', 'Flag Requestsauce'],
                ['30603', np.nan],
                ['30604', 'fruit'],
                ['30605', 'Flag Request Brand']]
        df = make_df(rows)
        df_routine = find_routine_office_rows(df)

        # Tests the values in df_routine are correct.
        result = df_to_list(df_routine)
        expected = [['zip_code', 'code_description', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for no_match")


if __name__ == '__main__':
    unittest.main()
