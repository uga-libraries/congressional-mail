import numpy as np
import unittest
from css_archiving_format import find_recommendation_rows
from test_df_search import make_df
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_in_document_name(self):
        """Test for when column in_document_name contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', 'path\\letter.txt', '', '', '', '', ''],
                ['30601', '', '', 'path\\Intern rec', '', '', '', '', ''],
                ['30602', '', '', 'page rec.doc', '', '', '', '', ''],
                ['30603', '', '', '', '', '', '', '', ''],
                ['30604', '', '', 'path\\REC FOR JD.doc', '', '', '', '', ''],
                ['30605', '', '', 'recommendation', '', '', '', '', ''],
                ['30606', '', '', np.nan, '', '', '', '', '']]
        md_df = make_df(rows)
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', 'path\\Intern rec', '', '', '', '', '', 'Recommendation'],
                    ['30602', '', '', 'page rec.doc', '', '', '', '', '', 'Recommendation'],
                    ['30604', '', '', 'path\\REC FOR JD.doc', '', '', '', '', '', 'Recommendation'],
                    ['30605', '', '', 'recommendation', '', '', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_recommendations_check")

    def test_in_fillin(self):
        """Test for when column in_fillin contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', 'letter', '', '', '', ''],
                ['30601', '', '', '', 'New intern rec', '', '', '', ''],
                ['30602', '', '', '', 'Page Recommendation', '', '', '', ''],
                ['30603', '', '', '', '', '', '', '', ''],
                ['30604', '', '', '', 'URGENT REC FOR JD', '', '', '', ''],
                ['30605', '', '', '', 'recommendation', '', '', '', ''],
                ['30606', '', '', '', np.nan, '', '', '', '']]
        md_df = make_df(rows)
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', 'New intern rec', '', '', '', '', 'Recommendation'],
                    ['30602', '', '', '', 'Page Recommendation', '', '', '', '', 'Recommendation'],
                    ['30604', '', '', '', 'URGENT REC FOR JD', '', '', '', '', 'Recommendation'],
                    ['30605', '', '', '', 'recommendation', '', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for in_fillin, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for in_fillin, df_recommendations_check")

    def test_in_text(self):
        """Test for when column in_text contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', 'letter', '', '', '', '', '', ''],
                ['30601', '', 'Intern Rec 2', '', '', '', '', '', ''],
                ['30602', '', 'New page rec', '', '', '', '', '', ''],
                ['30603', '', '', '', '', '', '', '', ''],
                ['30604', '', 'URGENT REC FOR JD', '', '', '', '', '', ''],
                ['30605', '', 'recommendation', '', '', '', '', '', ''],
                ['30606', '', np.nan, '', '', '', '', '', '']]
        md_df = make_df(rows)
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', 'Intern Rec 2', '', '', '', '', '', '', 'Recommendation'],
                    ['30602', '', 'New page rec', '', '', '', '', '', '', 'Recommendation'],
                    ['30604', '', 'URGENT REC FOR JD', '', '', '', '', '', '', 'Recommendation'],
                    ['30605', '', 'recommendation', '', '', '', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_recommendations_check")

    def test_in_topic(self):
        """Test for when column in_topic contains Recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'Admin', '', '', '', '', '', '', ''],
                ['30601', 'Intern rec25', '', '', '', '', '', '', ''],
                ['30602', '25 page rec', '', '', '', '', '', '', ''],
                ['30603', '', '', '', '', '', '', '', ''],
                ['30604', 'URGENT REC FOR X', '', '', '', '', '', '', ''],
                ['30605', 'recommendation', '', '', '', '', '', '', ''],
                ['30606', np.nan, '', '', '', '', '', '', '']]
        md_df = make_df(rows)
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', 'Intern rec25', '', '', '', '', '', '', '', 'Recommendation'],
                    ['30602', '25 page rec', '', '', '', '', '', '', '', 'Recommendation'],
                    ['30604', 'URGENT REC FOR X', '', '', '', '', '', '', '', 'Recommendation'],
                    ['30605', 'recommendation', '', '', '', '', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_recommendations_check")

    def test_none(self):
        """Test for when no patterns indicating recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'Farm', np.nan, 'Animals', np.nan, np.nan, np.nan, np.nan, np.nan],
                ['30601-recommendation', 'Water', 'note', '', '', 'Rights', 'note', '', '']]
        md_df = make_df(rows)
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
        rows = [['30600', '', '', '', '', '', '', 'path\\letter.txt', ''],
                ['30601', '', '', '', '', '', '', 'path\\Intern rec', ''],
                ['30602', '', '', '', '', '', '', 'page rec.doc', ''],
                ['30603', '', '', '', '', '', '', '', ''],
                ['30604', '', '', '', '', '', '', 'path\\REC FOR JD.doc', ''],
                ['30605', '', '', '', '', '', '', 'recommendation', ''],
                ['30606', '', '', '', '', '', '', np.nan, '']]
        md_df = make_df(rows)
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', '', 'path\\Intern rec', '', 'Recommendation'],
                    ['30602', '', '', '', '', '', '', 'page rec.doc', '', 'Recommendation'],
                    ['30604', '', '', '', '', '', '', 'path\\REC FOR JD.doc', '', 'Recommendation'],
                    ['30605', '', '', '', '', '', '', 'recommendation', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_recommendations_check")

    def test_out_fillin(self):
        """Test for when column out_fillin contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', '', '', '', 'letter'],
                ['30601', '', '', '', '', '', '', '', 'Intern rec2'],
                ['30602', '', '', '', '', '', '', '', 'new page rec'],
                ['30603', '', '', '', '', '', '', '', ''],
                ['30604', '', '', '', '', '', '', '', 'URGENT REC FOR JD'],
                ['30605', '', '', '', '', '', '', '', 'recommendation'],
                ['30606', '', '', '', '', '', '', '', np.nan]]
        md_df = make_df(rows)
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', '', '', 'Intern rec2', 'Recommendation'],
                    ['30602', '', '', '', '', '', '', '', 'new page rec', 'Recommendation'],
                    ['30604', '', '', '', '', '', '', '', 'URGENT REC FOR JD', 'Recommendation'],
                    ['30605', '', '', '', '', '', '', '', 'recommendation', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_recommendations_check")

    def test_out_text(self):
        """Test for when column out_text contains a phrase indicating recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', '', 'letter', '', ''],
                ['30601', '', '', '', '', '', 'Intern rec2', '', ''],
                ['30602', '', '', '', '', '', 'WA page rec', '', ''],
                ['30603', '', '', '', '', '', '', '', ''],
                ['30604', '', '', '', '', '', 'URGENT REC FOR JD', '', ''],
                ['30605', '', '', '', '', '', 'recommendation', '', ''],
                ['30606', '', '', '', '', '', np.nan, '', '']]
        md_df = make_df(rows)
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', 'Intern rec2', '', '', 'Recommendation'],
                    ['30602', '', '', '', '', '', 'WA page rec', '', '', 'Recommendation'],
                    ['30604', '', '', '', '', '', 'URGENT REC FOR JD', '', '', 'Recommendation'],
                    ['30605', '', '', '', '', '', 'recommendation', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_recommendations_check")

    def test_out_topic(self):
        """Test for when column out_topic contains Recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', 'letter', '', '', ''],
                ['30601', '', '', '', '', 'Intern Rec_2', '', '', ''],
                ['30602', '', '', '', '', 'new page rec', '', '', ''],
                ['30603', '', '', '', '', '', '', '', ''],
                ['30604', '', '', '', '', 'URGENT REC FOR X', '', '', ''],
                ['30605', '', '', '', '', 'recommendation', '', '', ''],
                ['30606', '', '', '', '', np.nan, '', '', '']]
        md_df = make_df(rows)
        df_recommendations, df_recommendations_check = find_recommendation_rows(md_df)

        # Tests the values in df_recommendations are correct.
        result = df_to_list(df_recommendations)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', 'Intern Rec_2', '', '', '', 'Recommendation'],
                    ['30602', '', '', '', '', 'new page rec', '', '', '', 'Recommendation'],
                    ['30604', '', '', '', '', 'URGENT REC FOR X', '', '', '', 'Recommendation'],
                    ['30605', '', '', '', '', 'recommendation', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_recommendations")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendations_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_recommendations_check")


if __name__ == '__main__':
    unittest.main()
