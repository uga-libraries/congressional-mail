import pandas as pd
import unittest
from css_archiving_format import find_recommendation_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_in_document_name(self):
        """Test for when column in_document_name contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', r'path/check if recommendation.txt', '', '', '', '', ''],
                              ['30601', '', '', r'path/letter of recommendation', '', '', '', '', ''],
                              ['30602', '', '', r'policy for recommendation.pdf', '', '', '', '', ''],
                              ['30603', '', '', '', '', '', '', '', ''],
                              ['30604', '', '', r'REC FOR', '', '', '', '', ''],
                              ['30605', '', '', r'wrote recommendation', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', r'path/letter of recommendation', '', '', '', '', '', 'Recommendation'],
                    ['30602', '', '', r'policy for recommendation.pdf', '', '', '', '', '', 'Recommendation'],
                    ['30604', '', '', r'REC FOR', '', '', '', '', '', 'Recommendation'],
                    ['30605', '', '', r'wrote recommendation', '', '', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', r'path/check if recommendation.txt', '', '', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_recommendations_check")

    def test_in_text(self):
        """Test for when column in_text contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'Senator wrote recommendation', '', '', '', '', '', ''],
                              ['30601', '', 'policy for recommendations sent', '', '', '', '', '', ''],
                              ['30602', '', 'Program recommendation', '', '', '', '', '', ''],
                              ['30603', '', 'Letter of Recommendation', '', '', '', '', '', ''],
                              ['30604', '', 'Requested rec for JD', '', '', '', '', '', ''],
                              ['30605', '', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', 'Senator wrote recommendation', '', '', '', '', '', '', 'Recommendation'],
                    ['30601', '', 'policy for recommendations sent', '', '', '', '', '', '', 'Recommendation'],
                    ['30603', '', 'Letter of Recommendation', '', '', '', '', '', '', 'Recommendation'],
                    ['30604', '', 'Requested rec for JD', '', '', '', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30602', '', 'Program recommendation', '', '', '', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_recommendations_check")

    def test_in_topic(self):
        """Test for when column in_topic contains Recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Recommendations', '', '', '', '', '', '', ''],
                              ['30601', 'Admin^recommendations', '', '', '', '', '', '', ''],
                              ['30602', 'RECOMMENDATIONS^Admin', '', '', '', '', '', '', ''],
                              ['30603', 'Policy Recommendation', '', '', '', '', '', '', ''],
                              ['30604', '', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Recommendations', '', '', '', '', '', '', '', 'Recommendation'],
                    ['30601', 'Admin^recommendations', '', '', '', '', '', '', '', 'Recommendation'],
                    ['30602', 'RECOMMENDATIONS^Admin', '', '', '', '', '', '', '', 'Recommendation'],
                    ['30603', 'Policy Recommendation', '', '', '', '', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_recommendations_check")

    def test_none(self):
        """Test for when no patterns indicating recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Farm', '', 'Animals', '', '', ''],
                              ['30601', 'Water', 'note', '', '', 'Rights', 'note', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched), df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched), df_recommendations_check")

    def test_out_document_name(self):
        """Test for when column out_document_name contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', r'path/check if recommendation.txt', ''],
                              ['30601', '', '', '', '', '', '', r'path/letter of recommendation', ''],
                              ['30602', '', '', '', '', '', '', r'policy for recommendation.pdf', ''],
                              ['30603', '', '', '', '', '', '', '', ''],
                              ['30604', '', '', '', '', '', '', r'REC FOR', ''],
                              ['30605', '', '', '', '', '', '', r'wrote recommendation', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', '', r'path/letter of recommendation', '', 'Recommendation'],
                    ['30602', '', '', '', '', '', '', r'policy for recommendation.pdf', '', 'Recommendation'],
                    ['30604', '', '', '', '', '', '', r'REC FOR', '', 'Recommendation'],
                    ['30605', '', '', '', '', '', '', r'wrote recommendation', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', '', r'path/check if recommendation.txt', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_recommendations_check")

    def test_out_fillin(self):
        """Test for when column out_fillin contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', '', 'Doe letter of recommendation'],
                              ['30601', '', '', '', '', '', '', '', 'Policy for recommendations sent'],
                              ['30602', '', '', '', '', '', '', '', 'REC FOR JD'],
                              ['30603', '', '', '', '', '', '', '', 'not a recommendation'],
                              ['30604', '', '', '', '', '', '', '', 'recommendation to support'],
                              ['30605', '', '', '', '', '', '', '', 'Wrote Recommendation']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', '', '', 'Doe letter of recommendation', 'Recommendation'],
                    ['30601', '', '', '', '', '', '', '', 'Policy for recommendations sent', 'Recommendation'],
                    ['30602', '', '', '', '', '', '', '', 'REC FOR JD', 'Recommendation'],
                    ['30605', '', '', '', '', '', '', '', 'Wrote Recommendation', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', '', '', 'not a recommendation', 'Recommendation'],
                    ['30604', '', '', '', '', '', '', '', 'recommendation to support', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_recommendations_check")

    def test_out_text(self):
        """Test for when column out_text contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', 'Doe letter of recommendation', '', ''],
                              ['30601', '', '', '', '', '', 'Policy for recommendations sent', '', ''],
                              ['30602', '', '', '', '', '', 'REC FOR JD', '', ''],
                              ['30603', '', '', '', '', '', 'not a recommendation', '', ''],
                              ['30604', '', '', '', '', '', 'recommendation to support', '', ''],
                              ['30605', '', '', '', '', '', 'Wrote Recommendation', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', 'Doe letter of recommendation', '', '', 'Recommendation'],
                    ['30601', '', '', '', '', '', 'Policy for recommendations sent', '', '', 'Recommendation'],
                    ['30602', '', '', '', '', '', 'REC FOR JD', '', '', 'Recommendation'],
                    ['30605', '', '', '', '', '', 'Wrote Recommendation', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', 'not a recommendation', '', '', 'Recommendation'],
                    ['30604', '', '', '', '', '', 'recommendation to support', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_recommendations_check")

    def test_out_topic(self):
        """Test for when column out_topic contains Recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', 'Policy Recommendation', '', '', ''],
                              ['30601', '', '', '', '', 'General^recommendations', '', '', ''],
                              ['30602', '', '', '', '', 'Rec', '', '', ''],
                              ['30603', '', '', '', '', '', '', '', ''],
                              ['30604', '', '', '', '', 'Recommendations^Admin', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', 'Policy Recommendation', '', '', '', 'Recommendation'],
                    ['30601', '', '', '', '', 'General^recommendations', '', '', '', 'Recommendation'],
                    ['30604', '', '', '', '', 'Recommendations^Admin', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_recommendations_check")


if __name__ == '__main__':
    unittest.main()
