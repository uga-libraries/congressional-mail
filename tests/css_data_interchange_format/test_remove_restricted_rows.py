import numpy as np
import os
import pandas as pd
import unittest
from css_data_interchange_format import remove_restricted_rows
from test_find_casework_rows import df_to_list


class MyTestCase(unittest.TestCase):

    def test_no_report(self):
        """Test for when there is no restriction_review.csv"""
        # Makes dataframes to use as test input and runs the function.
        md_df = pd.DataFrame([['30144-2248', '19990301', 'imail', 'FUN1'],
                              ['30144-2248', '19990501', 'imail', 'ASST - ADOPT'],
                              ['30062-1613', '19990607', 'usmail', 'FUN1'],
                              [np.nan, '20000315', np.nan, 'FUN2']],
                             columns=['zip_code', 'date_in', 'response_type', 'group_name'])
        output_directory = os.getcwd()
        md_df = remove_restricted_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'date_in', 'response_type', 'group_name'],
                    ['30144-2248', '19990301', 'imail', 'FUN1'],
                    ['30144-2248', '19990501', 'imail', 'ASST - ADOPT'],
                    ['30062-1613', '19990607', 'usmail', 'FUN1'],
                    ['blank', '20000315', 'blank', 'FUN2']]
        self.assertEqual(expected, result, "Problem with test for no_report")

    def test_type_different(self):
        """Test for when the rows to remove have a different type in some columns"""
        # Makes dataframes to use as test input and runs the function.
        md_df = pd.DataFrame([[30001, 19990101, 'imail', 'court'],
                              [30002, 19990202, 'imail', 'sports court'],
                              [30003, 19990303, 'usmail', 'migrant'],
                              [30004, 19990404, 'usmail', 'refugee'],
                              [30005, 19990505, 'usmail', 'FUN2']],
                             columns=['zip_code', 'date_in', 'response_type', 'group_name'])
        output_directory = os.path.join('test_data', 'remove_restricted_rows')
        md_df = remove_restricted_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'date_in', 'response_type', 'group_name'],
                    ['30002', '19990202', 'imail', 'sports court'],
                    ['30005', '19990505', 'usmail', 'FUN2']]
        self.assertEqual(expected, result, "Problem with test for type_same")

    def test_type_same(self):
        """Test for when the rows to remove have the same type"""
        # Makes dataframes to use as test input and runs the function.
        md_df = pd.DataFrame([['30001', '19990101', 'imail', 'court'],
                              ['30002', '19990202', 'imail', 'sports court'],
                              ['30003', '19990303', 'usmail', 'migrant'],
                              ['30004', '19990404', 'usmail', 'refugee'],
                              ['30005', '19990505', 'usmail', 'FUN2']],
                             columns=['zip_code', 'date_in', 'response_type', 'group_name'])
        output_directory = os.path.join('test_data', 'remove_restricted_rows')
        md_df = remove_restricted_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'date_in', 'response_type', 'group_name'],
                    ['30002', '19990202', 'imail', 'sports court'],
                    ['30005', '19990505', 'usmail', 'FUN2']]
        self.assertEqual(expected, result, "Problem with test for type_same")


if __name__ == '__main__':
    unittest.main()

