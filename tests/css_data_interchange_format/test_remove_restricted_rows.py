import os
import pandas as pd
import unittest
from css_data_interchange_format import remove_restricted_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_function(self):
        """Test for removing rows"""
        # Makes dataframes to use as test input and runs the function.
        md_df = pd.DataFrame([['30001', '19990101', 'imail', 'court'],
                              ['30002', '19990202', 'imail', 'sports court'],
                              ['30003', '19990303', 'usmail', 'migrant'],
                              ['30004', '19990404', 'usmail', 'refugee'],
                              ['30005', '19990505', 'usmail', 'FUN2']],
                             columns=['zip_code', 'date_in', 'response_type', 'group_name'])
        restrict_df = pd.DataFrame([['30001', '19990101', 'imail', 'court'],
                                    ['30003', '19990303', 'usmail', 'migrant'],
                                    ['30004', '19990404', 'usmail', 'refugee']],
                                   columns=['zip_code', 'date_in', 'response_type', 'group_name'])
        md_df = remove_restricted_rows(md_df, restrict_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'date_in', 'response_type', 'group_name'],
                    ['30002', '19990202', 'imail', 'sports court'],
                    ['30005', '19990505', 'usmail', 'FUN2']]
        self.assertEqual(expected, result, "Problem with test for type_same")


if __name__ == '__main__':
    unittest.main()

