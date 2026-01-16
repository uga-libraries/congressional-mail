import pandas as pd
import unittest
from css_data_interchange_format import find_recommendation_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):

    def test_doc_name(self):
        """Test for when the column communication_document_name indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', 'docs\\Intern Rec.txt', '', ''],
                           ['20250402', '', 'docs\\PAGE REC.txt', '', ''],
                           ['20250403', '', 'docs\\intern rec-no', '', ''],
                           ['20250404', '', 'docs\\recommendation.txt', '', ''],
                           ['20250405', '', 'docs\\doc.txt', '', ''],
                           ['20250406', '', 'docs\\recommendation_request.txt', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_rec, df_rec_check = find_recommendation_rows(df)

        # Tests the values in df_rec are correct.
        result = df_to_list(df_rec)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', 'docs\\Intern Rec.txt', '', '', 'Recommendation'],
                    ['20250402', '', 'docs\\PAGE REC.txt', '', '', 'Recommendation'],
                    ['20250403', '', 'docs\\intern rec-no', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_rec")

        # Tests the values in df_rec_check are correct.
        result = df_to_list(df_rec_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250404', '', 'docs\\recommendation.txt', '', '', 'Recommendation'],
                    ['20250406', '', 'docs\\recommendation_request.txt', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_rec_check")

    def test_group(self):
        """Test for when the column group indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'intern_returning', '', '', ''],
                           ['20250402', 'new_intern', '', '', ''],
                           ['20250403', 'PAGE', '', '', ''],
                           ['20250404', '', '', '', ''],
                           ['20250405', 'recommendation', '', '', ''],
                           ['20250406', 'keep', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_rec, df_rec_check = find_recommendation_rows(df)

        # Tests the values in df_rec are correct.
        result = df_to_list(df_rec)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'intern_returning', '', '', '', 'Recommendation'],
                    ['20250402', 'new_intern', '', '', '', 'Recommendation'],
                    ['20250403', 'PAGE', '', '', '', 'Recommendation'],
                    ['20250405', 'recommendation', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for group, df_rec")

        # Tests the values in df_rec_check are correct.
        result = df_to_list(df_rec_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for group, df_rec_check")

    def test_none(self):
        """Test for no patterns indicating recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'Admin', 'docs\\doc.txt', 'file.txt', ''],
                           ['20250402', 'Admin', 'docs\\doc.txt', '', ''],
                           ['20250403', 'Interviews', 'docs\\doc.txt', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_rec, df_rec_check = find_recommendation_rows(df)

        # Tests the values in df_rec are correct.
        result = df_to_list(df_rec)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_rec")

        # Tests the values in df_rec_check are correct.
        result = df_to_list(df_rec_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_rec_check")
        
    def test_text(self):
        """Test for when the column text indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', '', 'intern recommendation'],
                           ['20250402', '', '', '', 'donor page rec'],
                           ['20250403', '', '', '', 'check for recommendation'],
                           ['20250404', '', '', '', ''],
                           ['20250405', '', '', '', 'INTERN REC'],
                           ['20250406', '', '', '', 'policy recommendation']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_rec, df_rec_check = find_recommendation_rows(df)

        # Tests the values in df_rec are correct.
        result = df_to_list(df_rec)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', '', '', 'intern recommendation', 'Recommendation'],
                    ['20250402', '', '', '', 'donor page rec', 'Recommendation'],
                    ['20250405', '', '', '', 'INTERN REC', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for text, df_rec")

        # Tests the values in df_rec_check are correct.
        result = df_to_list(df_rec_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250403', '', '', '', 'check for recommendation', 'Recommendation'],
                    ['20250406', '', '', '', 'policy recommendation', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for text, df_rec_check")


if __name__ == '__main__':
    unittest.main()
