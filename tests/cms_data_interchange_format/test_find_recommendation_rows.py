import pandas as pd
import unittest
from cms_data_interchange_format import find_recommendation_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_code_desc(self):
        """Test for when the column code_description indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', '', 'Send generic recommendation'],
                           ['30601', '', '', 'Letter of Recommendation'],
                           ['30602', '', '', 'letters of recommendation for girl scouts'],
                           ['30603', '', '', 'Recommendation for policy'],
                           ['30604', '', '', 'RECOMMENDATION LETTER'],
                           ['30605', '', '', 'recommendation letters']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text',
                                   'code_description'])
        df_recommendation, df_recommendation_check = find_recommendation_rows(df)

        # Tests the values in df_recommendation are correct.
        result = df_to_list(df_recommendation)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', '', 'Send generic recommendation', 'Recommendation'],
                    ['30601', '', '', 'Letter of Recommendation', 'Recommendation'],
                    ['30602', '', '', 'letters of recommendation for girl scouts', 'Recommendation'],
                    ['30604', '', '', 'RECOMMENDATION LETTER', 'Recommendation'],
                    ['30605', '', '', 'recommendation letters', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_recommendation")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendation_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30603', '', '', 'Recommendation for policy', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_recommendation_check")

    def test_corr_doc(self):
        """Test for when the column correspondence_document_name indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', 'path\\Send generic recommendation.txt', '', ''],
                           ['30601', 'path\\Letter of Recommendation.txt', '', ''],
                           ['30602', 'path\\letters of recommendation for girl scouts.txt', '', ''],
                           ['30603', 'path\\Recommendation for policy.txt', '', ''],
                           ['30604', 'path\\RECOMMENDATION LETTER.txt', '', ''],
                           ['30605', 'path\\recommendation letters.txt', '', '']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text',
                                   'code_description'])
        df_recommendation, df_recommendation_check = find_recommendation_rows(df)

        # Tests the values in df_recommendation are correct.
        result = df_to_list(df_recommendation)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', 'path\\Send generic recommendation.txt', '', '', 'Recommendation'],
                    ['30601', 'path\\Letter of Recommendation.txt', '', '', 'Recommendation'],
                    ['30602', 'path\\letters of recommendation for girl scouts.txt', '', '', 'Recommendation'],
                    ['30604', 'path\\RECOMMENDATION LETTER.txt', '', '', 'Recommendation'],
                    ['30605', 'path\\recommendation letters.txt', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_recommendation")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendation_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30603', 'path\\Recommendation for policy.txt', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_recommendation_check")

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', 'Send generic recommendation', ''],
                           ['30601', '', 'Letter of Recommendation', ''],
                           ['30602', '', 'letters of recommendation for girl scouts', ''],
                           ['30603', '', 'Recommendation for policy', ''],
                           ['30604', '', 'RECOMMENDATION LETTER', ''],
                           ['30605', '', 'recommendation letters', '']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_recommendation, df_recommendation_check = find_recommendation_rows(df)

        # Tests the values in df_recommendation are correct.
        result = df_to_list(df_recommendation)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', 'Send generic recommendation', '', 'Recommendation'],
                    ['30601', '', 'Letter of Recommendation', '', 'Recommendation'],
                    ['30602', '', 'letters of recommendation for girl scouts', '', 'Recommendation'],
                    ['30604', '', 'RECOMMENDATION LETTER', '', 'Recommendation'],
                    ['30605', '', 'recommendation letters', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_recommendation")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendation_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30603', '', 'Recommendation for policy', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_recommendation_check")

    def test_none(self):
        """Test for when no rows have recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', 'doc.doc', 'one', 'a'],
                           ['30601', '', 'two', 'b'],
                           ['30602', '', 'three', 'c']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_recommendation, df_recommendation_check = find_recommendation_rows(df)

        # Tests the values in df_recommendation are correct.
        result = df_to_list(df_recommendation)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_recommendation")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendation_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_recommendation_check")


if __name__ == '__main__':
    unittest.main()
