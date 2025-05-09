"""
Tests for the function find_recommendations_rows(), which finds metadata rows that are or might be recommendations
To simplify testing, a small subset of the columns from an export are used
"""
import pandas as pd
import unittest
from cms_data_interchange_format import find_recommendation_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['file_1.doc', 'Send generic recommendation', 'x'],
                           ['file_2.doc', 'Letter of Recommendation', 'x'],
                           ['file_3.doc', 'letters of recommendation for girl scouts', 'x'],
                           ['file_4.doc', 'Recommendation for policy', 'x'],
                           ['file_5.doc', 'RECOMMENDATION LETTER', 'x'],
                           ['file_6.doc', 'recommendation letters', 'x']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_recommendation, df_recommendation_check = find_recommendation_rows(df)

        # Tests the values in df_recommendation are correct.
        result = df_to_list(df_recommendation)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_1.doc', 'Send generic recommendation', 'x', 'Recommendation'],
                    ['file_2.doc', 'Letter of Recommendation', 'x', 'Recommendation'],
                    ['file_3.doc', 'letters of recommendation for girl scouts', 'x', 'Recommendation'],
                    ['file_5.doc', 'RECOMMENDATION LETTER', 'x', 'Recommendation'],
                    ['file_6.doc', 'recommendation letters', 'x', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for corr_text, df_recommendation")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendation_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category'],
                    ['file_4.doc', 'Recommendation for policy', 'x', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for corr_text, df_recommendation_check")

    def test_none(self):
        """Test for when no rows have recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['file_1.doc', 'one', 'a'],
                           ['file_2.doc', 'two', 'b'],
                           ['file_3.doc', 'three', 'c']],
                          columns=['correspondence_document_name', 'correspondence_text', 'code_description'])
        df_recommendation, df_recommendation_check = find_recommendation_rows(df)

        # Tests the values in df_recommendation are correct.
        result = df_to_list(df_recommendation)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none, df_recommendation")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendation_check)
        expected = [['correspondence_document_name', 'correspondence_text', 'code_description', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none, df_recommendation_check")


if __name__ == '__main__':
    unittest.main()
