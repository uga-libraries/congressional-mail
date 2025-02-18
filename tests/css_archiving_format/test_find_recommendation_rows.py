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
        md_df = pd.DataFrame([['30600', 'Recommendations^General', '', 'Recommendations', ''],
                              ['30601', '', 'rec for john doe', '', 'policy for recommendations sent'],
                              ['30602', 'Recommendations', 'rec for smith', '', ''],
                              ['30603', 'Recommendations', 'rec for green', 'Recommendations', 'wrote recommendation'],
                              ['30604', '', '', 'Admin^Recommendations', 'wrote recommendation']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_recommendations = find_recommendation_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30600', 'Recommendations^General', '', 'Recommendations', '', 'Recommendation'],
                    ['30602', 'Recommendations', 'rec for smith', '', '', 'Recommendation'],
                    ['30603', 'Recommendations', 'rec for green', 'Recommendations', 'wrote recommendation',
                     'Recommendation'],
                    ['30604', '', '', 'Admin^Recommendations', 'wrote recommendation', 'Recommendation'],
                    ['30601', '', 'rec for john doe', '', 'policy for recommendations sent', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for all patterns")

    def test_in_text(self):
        """Test for when column in_text contains a phrase indicating recommendations (case-insensitive)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Admin', 'Senator wrote recommendation', '', ''],
                              ['30601', 'Admin', 'policy for recommendations sent', 'Admin', ''],
                              ['30602', 'Arts', '', '', ''],
                              ['30603', 'General', 'Letter of Recommendation', '', ''],
                              ['30604', '', 'Requested rec for JD', '', ''],
                              ['30605', 'Water', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_recommendations = find_recommendation_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30600', 'Admin', 'Senator wrote recommendation', '', '', 'Recommendation'],
                    ['30601', 'Admin', 'policy for recommendations sent', 'Admin', '', 'Recommendation'],
                    ['30603', 'General', 'Letter of Recommendation', '', '', 'Recommendation'],
                    ['30604', '', 'Requested rec for JD', '', '', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for in_text")

    def test_in_topic(self):
        """Test for when column in_topic contains Recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Recommendations', 'note', '', ''],
                              ['30601', 'Admin^Recommendations', '', '', ''],
                              ['30602', 'Recommendations^Admin', '', '', ''],
                              ['30603', 'Water', '', 'Water', 'Reply note'],
                              ['30604', '', '', 'Gen', '']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_recommendations = find_recommendation_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30600', 'Recommendations', 'note', '', '', 'Recommendation'],
                    ['30601', 'Admin^Recommendations', '', '', '', 'Recommendation'],
                    ['30602', 'Recommendations^Admin', '', '', '', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for in_topic")

    def test_none(self):
        """Test for when no patterns indicating recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Farm', '', 'Animals', ''],
                              ['30601', 'Water', 'note', 'Rights', 'note']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_recommendations = find_recommendation_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category']]
        self.assertEqual(result, expected, "Problem with test for none (no patterns matched)")

    def test_out_text(self):
        """Test for when column out_text contains a phrase indicating recommendations (case-insensitive)"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Admin', 'note', '', 'Doe letter of recommendation'],
                              ['30601', 'Admin', 'note', '', 'Policy for recommendations sent'],
                              ['30602', 'Admin', 'note', '', 'REC FOR JD'],
                              ['30603', 'Admin', '', '', 'note'],
                              ['30604', 'Admin', '', '', 'support'],
                              ['30605', 'Admin', '', '', 'Wrote Recommendation']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_recommendations = find_recommendation_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30600', 'Admin', 'note', '', 'Doe letter of recommendation', 'Recommendation'],
                    ['30601', 'Admin', 'note', '', 'Policy for recommendations sent', 'Recommendation'],
                    ['30602', 'Admin', 'note', '', 'REC FOR JD', 'Recommendation'],
                    ['30605', 'Admin', '', '', 'Wrote Recommendation', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for out_text")

    def test_out_topic(self):
        """Test for when column out_topic contains Recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', 'Water', ''],
                              ['30601', 'General', '', 'General^Recommendations', ''],
                              ['30602', 'Water', '', '', ''],
                              ['30603', '', 'note', 'Recommendations', ''],
                              ['30604', 'Admin', '', 'Recommendations^Admin', 'note']],
                             columns=['zip', 'in_topic', 'in_text', 'out_topic', 'out_text'])
        df_recommendations = find_recommendation_rows(md_df)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'out_topic', 'out_text', 'Appraisal_Category'],
                    ['30601', 'General', '', 'General^Recommendations', '', 'Recommendation'],
                    ['30603', '', 'note', 'Recommendations', '', 'Recommendation'],
                    ['30604', 'Admin', '', 'Recommendations^Admin', 'note', 'Recommendation']]
        self.assertEqual(result, expected, "Problem with test for out_topic")


if __name__ == '__main__':
    unittest.main()
