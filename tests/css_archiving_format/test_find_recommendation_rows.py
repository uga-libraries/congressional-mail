"""
Tests for the function find_recommendation_rows(),
which finds metadata rows with topics or text that indicate they are job applications and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_archiving_format import find_recommendation_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_all(self):
        """Test for when all patterns indicating recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Recommendations^General', 'my recommendation', '', '', 'Recommendations',
                               '', '', ''],
                              ['30601', '', 'rec for john doe', '', '', '', 'policy for recommendations sent', '', ''],
                              ['30602', 'Recommendations', 'letter of recommendation for smith', '', '', '', '', '',
                               'decline_recommendation'],
                              ['30603', 'Recommendations', 'rec for green', '', '', 'Recommendations',
                               'wrote recommendation', '', ''],
                              ['30604', '', '', '', '', 'Admin^Recommendations', 'wrote recommendation', '', ''],
                              ['30605', 'Admin', 'my recommendation is x', '', '', 'Admin', '', '', ''],
                              ['30606', 'Admin', 'note', '', '', 'Admin', 'recommendation', r'doc\recommendation.txt',
                               'name_date']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Recommendations^General', 'my recommendation', '', '', 'Recommendations', '', '', '',
                     'Recommendation'],
                    ['30602', 'Recommendations', 'letter of recommendation for smith', '', '', '', '', '',
                     'decline_recommendation', 'Recommendation'],
                    ['30603', 'Recommendations', 'rec for green', '', '', 'Recommendations', 'wrote recommendation',
                     '', '', 'Recommendation'],
                    ['30604', '', '', '', '', 'Admin^Recommendations', 'wrote recommendation', '', '', 'Recommendation'],
                    ['30601', '', 'rec for john doe', '', '', '', 'policy for recommendations sent', '', '',
                     'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for all patterns, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30605', 'Admin', 'my recommendation is x', '', '', 'Admin', '', '', '', 'Recommendation'],
                    ['30606', 'Admin', 'note', '', '', 'Admin', 'recommendation', r'doc\recommendation.txt',
                     'name_date', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for all patterns, df_recommendations_check")

    def test_in_text(self):
        """Test for when column in_text contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Admin', 'Senator wrote recommendation', '', '', '', '', '', ''],
                              ['30601', 'Admin', 'policy for recommendations sent', '', '', 'Admin', '', '', ''],
                              ['30602', 'Arts', 'Program recommendation', '', '', '', '', '', ''],
                              ['30603', 'General', 'Letter of Recommendation', '', '', '', '', '', ''],
                              ['30604', '', 'Requested rec for JD', '', '', '', '', '', ''],
                              ['30605', 'Water', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Admin', 'Senator wrote recommendation', '', '', '', '', '', '', 'Recommendation'],
                    ['30601', 'Admin', 'policy for recommendations sent', '', '', 'Admin', '', '', '', 'Recommendation'],
                    ['30603', 'General', 'Letter of Recommendation', '', '', '', '', '', '', 'Recommendation'],
                    ['30604', '', 'Requested rec for JD', '', '', '', '', '', '', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for in_text, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30602', 'Arts', 'Program recommendation', '', '', '', '', '', '', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for in_text, df_recommendations_check")

    def test_in_topic(self):
        """Test for when column in_topic contains Recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Recommendations', 'note', '', '', '', '', '', ''],
                              ['30601', 'Admin^recommendations', '', '', '', '', '', '', ''],
                              ['30602', 'RECOMMENDATIONS^Admin', '', '', '', '', '', '', ''],
                              ['30603', 'Policy Recommendation', '', '', '', 'Water', 'Reply note', '', ''],
                              ['30604', '', '', '', '', 'Gen', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Recommendations', 'note', '', '', '', '', '', '', 'Recommendation'],
                    ['30601', 'Admin^recommendations', '', '', '', '', '', '', '', 'Recommendation'],
                    ['30602', 'RECOMMENDATIONS^Admin', '', '', '', '', '', '', '', 'Recommendation'],
                    ['30603', 'Policy Recommendation', '', '', '', 'Water', 'Reply note', '', '', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for in_topic, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for in_topic, df_recommendations_check")

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
        self.assertEqual(result, expected, "Problem with test for none (no patterns matched), df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no patterns matched), df_recommendations_check")

    def test_out_text(self):
        """Test for when column out_text contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Admin', 'note', '', '', '', 'Doe letter of recommendation', '', ''],
                              ['30601', 'Admin', 'note', '', '', '', 'Policy for recommendations sent', '', ''],
                              ['30602', 'Admin', 'note', '', '', '', 'REC FOR JD', '', ''],
                              ['30603', 'Admin', '', '', '', '', 'not a recommendation', '', ''],
                              ['30604', 'Admin', '', '', '', '', 'recommendation to support', '', ''],
                              ['30605', 'Admin', '', '', '', '', 'Wrote Recommendation', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Admin', 'note', '', '', '', 'Doe letter of recommendation', '', '', 'Recommendation'],
                    ['30601', 'Admin', 'note', '', '', '', 'Policy for recommendations sent', '', '', 'Recommendation'],
                    ['30602', 'Admin', 'note', '', '', '', 'REC FOR JD', '', '', 'Recommendation'],
                    ['30605', 'Admin', '', '', '', '', 'Wrote Recommendation', '', '', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for out_text, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', 'Admin', '', '', '', '', 'not a recommendation', '', '', 'Recommendation'],
                    ['30604', 'Admin', '', '', '', '', 'recommendation to support', '', '', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for out_text, df_recommendations_check")

    def test_out_topic(self):
        """Test for when column out_topic contains Recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', 'Water', 'Policy Recommendation', '', ''],
                              ['30601', 'General', '', '', '', 'General^recommendations', '', '', ''],
                              ['30602', 'Water', '', '', '', '', 'Recommendation', '', ''],
                              ['30603', '', 'note', '', '', 'RECOMMENDATIONS', '', '', ''],
                              ['30604', 'Admin', '', '', '', 'Recommendations^Admin', 'note', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', 'General', '', '', '', 'General^recommendations', '', '', '', 'Recommendation'],
                    ['30603', '', 'note', '', '', 'RECOMMENDATIONS', '', '', '', 'Recommendation'],
                    ['30604', 'Admin', '', '', '', 'Recommendations^Admin', 'note', '', '', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for out_topic, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', 'Water', 'Policy Recommendation', '', '', 'Recommendation'],
                    ['30602', 'Water', '', '', '', '', 'Recommendation', '', '', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for out_topic, df_recommendations_check")


if __name__ == '__main__':
    unittest.main()
