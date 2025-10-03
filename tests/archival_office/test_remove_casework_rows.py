"""
Test for the function remove_casework_rows(), which removes metadata rows for letters that pertain to casework.
To simplify the input the test uses dataframes with only a few of the columns present in a real export.
"""
import pandas as pd
import unittest
from archival_office_correspondence_data import remove_casework_rows
from test_find_casework_rows import df_to_list


class MyTestCase(unittest.TestCase):

    def test_function(self):
        """Test for the function, which will return some rows from md_df"""
        # Makes dataframes to use as test input and runs the function.
        md_df = pd.DataFrame([['GA', 30601, 'info'],
                              ['GA', 30602, 'casework'],
                              ['GA', 30603, 'other info'],
                              ['VA', 20101, 'for casework']],
                             columns=['state_code', 'zip_code', 'comments'])
        casework_df = pd.DataFrame([['GA', 30602, 'casework'],
                                    ['VA', 20101, 'for casework']],
                                   columns=['state_code', 'zip_code', 'comments'])
        md_df = remove_casework_rows(md_df, casework_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['state_code', 'zip_code', 'comments'],
                    ['GA', 30601, 'info'],
                    ['GA', 30603, 'other info']]
        self.assertEqual(expected, result, "Problem with test for function")


if __name__ == '__main__':
    unittest.main()
