"""
Test for the function remove_appraisal_rows(), which metadata rows for letters deleted during appraisal.
To simplify input, the test uses dataframes with only a few of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_data_interchange_format import remove_appraisal_rows
from test_find_casework_rows import df_to_list


class MyTestCase(unittest.TestCase):

    def test_function(self):
        """Test for the function, which will remove some rows from md_df"""
        # Makes dataframes to use as test input and runs the function.
        md_df = pd.DataFrame([['30144-2248', '19990301', 'imail', 'TAX1'],
                              ['30144-2248', '19990501', 'imail', 'Casework - HMO'],
                              ['30062-1613', '19990607', 'usmail', 'TAX1'],
                              ['', '20000315', 'imail', 'Casework']],
                             columns=['zip_code', 'date_in', 'response_type', 'group_name'])
        appraisal_df = pd.DataFrame([['30144-2248', '19990501', 'imail', 'Casework - HMO', 'Casework'],
                                    ['', '20000315', 'imail', 'Casework', 'Casework']],
                                    columns=['zip_code', 'date_in', 'response_type', 'group_name', 'Appraisal_Category'])
        md_df = remove_appraisal_rows(md_df, appraisal_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip_code', 'date_in', 'response_type', 'group_name'],
                    ['30144-2248', '19990301', 'imail', 'TAX1'],
                    ['30062-1613', '19990607', 'usmail', 'TAX1']]
        self.assertEqual(expected, result, "Problem with test for function")


if __name__ == '__main__':
    unittest.main()

