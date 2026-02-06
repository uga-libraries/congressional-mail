import numpy as np
import unittest
from cms_data_interchange_format import find_recommendation_rows
from test_df_search import make_df
from test_read_metadata_file import df_to_list


class MyTestCase(unittest.TestCase):

    def test_code_desc(self):
        """Test for when the column code_description indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', 'intern rec yes'],
                ['30601', '', '', 'DC Page Rec'],
                ['30602', '', '', 'jan rec for doe'],
                ['30603', '', '', 'RECOMMENDATION'],
                ['30604', '', '', ''],
                ['30605', '', '', 'parks'],
                ['30607', '', '', np.nan]]
        df = make_df(rows)
        df_recommendation, df_recommendation_check = find_recommendation_rows(df)

        # Tests the values in df_recommendation are correct.
        result = df_to_list(df_recommendation)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', '', 'intern rec yes', 'Recommendation'],
                    ['30601', '', '', 'DC Page Rec', 'Recommendation'],
                    ['30602', '', '', 'jan rec for doe', 'Recommendation'],
                    ['30603', '', '', 'RECOMMENDATION', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_recommendation")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendation_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_recommendation_check")

    def test_corr_doc(self):
        """Test for when the column correspondence_document_name indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'intern rec.doc', '', ''],
                ['30601', 'path\\Page Rec', '', ''],
                ['30602', 'path\\rec for doe.txt', '', ''],
                ['30603', 'RECOMMENDATION', '', ''],
                ['30604', '', '', ''],
                ['30605', 'parks', '', ''],
                ['30606', np.nan, '', '']]
        df = make_df(rows)
        df_recommendation, df_recommendation_check = find_recommendation_rows(df)

        # Tests the values in df_recommendation are correct.
        result = df_to_list(df_recommendation)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', 'intern rec.doc', '', '', 'Recommendation'],
                    ['30601', 'path\\Page Rec', '', '', 'Recommendation'],
                    ['30602', 'path\\rec for doe.txt', '', '', 'Recommendation'],
                    ['30603', 'RECOMMENDATION', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_recommendation")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendation_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_recommendation_check")

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', 'intern rec yes', ''],
                ['30601', '', 'DC Page Rec', ''],
                ['30602', '', 'jan rec for doe', ''],
                ['30603', '', 'RECOMMENDATION', ''],
                ['30604', '', '', ''],
                ['30605', '', 'parks', ''],
                ['30606', '', np.nan, '']]
        df = make_df(rows)
        df_recommendation, df_recommendation_check = find_recommendation_rows(df)

        # Tests the values in df_recommendation are correct.
        result = df_to_list(df_recommendation)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30600', '', 'intern rec yes', '', 'Recommendation'],
                    ['30601', '', 'DC Page Rec', '', 'Recommendation'],
                    ['30602', '', 'jan rec for doe', '', 'Recommendation'],
                    ['30603', '', 'RECOMMENDATION', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_recommendation")

        # Tests the values in df_recommendations_check are correct.
        result = df_to_list(df_recommendation_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_recommendation_check")

    def test_none(self):
        """Test for when no rows have recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'doc.doc', 'one', 'a'],
                ['30601', np.nan, 'two', 'b'],
                ['30602', '', 'three', 'c']]
        df = make_df(rows)
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
