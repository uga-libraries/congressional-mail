"""
Test for the function remove_appraisals_rows(), which removes metadata rows for letters deleted during appraisal.
To simplify input, the test uses dataframes with only a few of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_archiving_format import remove_appraisal_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_type_different(self):
        """Test for when columns in md_df have a different datatype, but otherwise the same value, as appraisal_df"""
        # Makes dataframes to use as test input and runs the function.
        md_df = pd.DataFrame([['Anderson', '', 12345, 'Casework', r'..\objects\111111.txt'],
                              ['Blue', '', 23456, 'Issue', r'..\objects\222222.txt'],
                              ['Clive', '', 34567, 'Casework', ''],
                              ['Dudley', '', 45678, 'Issue', ''],
                              ['Evans', '', 56789, 'Casework', r'..\objects\333333.txt']],
                             columns=['last', 'title', 'zip', 'in_type', 'in_document_name'])
        appraisal_df = pd.DataFrame([['Anderson', '', '12345', 'Casework', r'..\objects\111111.txt', 'Casework'],
                                    ['Clive', '', '34567', 'Casework', '', 'Casework'],
                                    ['Evans', '', '56789', 'Casework', r'..\objects\333333.txt', 'Casework']],
                                    columns=['last', 'title', 'zip', 'in_type', 'in_document_name', 'Appraisal_Category'])
        md_df = remove_appraisal_rows(md_df, appraisal_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'title', 'zip', 'in_type', 'in_document_name'],
                    ['Blue', '', '23456', 'Issue', r'..\objects\222222.txt'],
                    ['Dudley', '', '45678', 'Issue', '']]
        self.assertEqual(expected, result, "Problem with test for type different")

    def test_type_same(self):
        """Test for when columns in md_df have the same datatype and value as appraisal_df"""
        # Makes dataframes to use as test input and runs the function.
        md_df = pd.DataFrame([['Anderson', '', '12345', 'Casework', r'..\objects\111111.txt'],
                              ['Blue', '', '23456', 'Issue', r'..\objects\222222.txt'],
                              ['Clive', '', '34567', 'Casework', ''],
                              ['Dudley', '', '45678', 'Issue', ''],
                              ['Evans', '', '56789', 'Casework', r'..\objects\333333.txt']],
                             columns=['last', 'title', 'zip', 'in_type', 'in_document_name'])
        appraisal_df = pd.DataFrame([['Anderson', '', '12345', 'Casework', r'..\objects\111111.txt', 'Casework'],
                                    ['Clive', '', '34567', 'Casework', '', 'Casework'],
                                    ['Evans', '', '56789', 'Casework', r'..\objects\333333.txt', 'Casework']],
                                    columns=['last', 'title', 'zip', 'in_type', 'in_document_name', 'Appraisal_Category'])
        md_df = remove_appraisal_rows(md_df, appraisal_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['last', 'title', 'zip', 'in_type', 'in_document_name'],
                    ['Blue', '', '23456', 'Issue', r'..\objects\222222.txt'],
                    ['Dudley', '', '45678', 'Issue', '']]
        self.assertEqual(expected, result, "Problem with test for same type")


if __name__ == '__main__':
    unittest.main()
