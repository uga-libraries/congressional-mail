import numpy as np
import unittest
from css_data_interchange_format import find_recommendation_rows
from test_df_search import make_df
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_doc_name(self):
        """Test for when the column communication_document_name indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', '', 'Intern Rec.txt', '', ''],
                ['20250402', '', 'docs\\PAGE REC', '', ''],
                ['20250403', '', 'docs\\rec for jd.doc', '', ''],
                ['20250404', '', 'recommendation', '', ''],
                ['20250405', '', 'docs\\doc.txt', '', ''],
                ['20250406', '', '', '', ''],
                ['20250407', '', np.nan, '', ''],
                ['20250408', '', 'docs\\rec.txt', '', ''],
                ['20250409', '', 'docs\\rec_yes.txt', '', '']]
        df = make_df(rows)
        df_rec, df_rec_check = find_recommendation_rows(df)

        # Tests the values in df_rec are correct.
        result = df_to_list(df_rec)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', 'Intern Rec.txt', '', '', 'Recommendation'],
                    ['20250402', '', 'docs\\PAGE REC', '', '', 'Recommendation'],
                    ['20250403', '', 'docs\\rec for jd.doc', '', '', 'Recommendation'],
                    ['20250404', '', 'recommendation', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_rec")

        # Tests the values in df_rec_check are correct.
        result = df_to_list(df_rec_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250408', '', 'docs\\rec.txt', '', '', 'Recommendation'],
                    ['20250409', '', 'docs\\rec_yes.txt', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_rec_check")

    def test_file_name(self):
        """Test for when the column file_name indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'intern rec.doc', '', '', ''],
                ['20250402', 'NEW PAGE REC', '', '', ''],
                ['20250403', 'art rec for jd.doc', '', '', ''],
                ['20250404', 'recommendation', '', '', ''],
                ['20250405', '', '', '', ''],
                ['20250406', 'keep', '', '', ''],
                ['20250407', np.nan, '', '', ''],
                ['20250406', 'rec.doc', '', '', ''],
                ['20250406', 'record.doc', '', '', '']]
        df = make_df(rows)
        df_rec, df_rec_check = find_recommendation_rows(df)

        # Tests the values in df_rec are correct.
        result = df_to_list(df_rec)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'intern rec.doc', '', '', '', 'Recommendation'],
                    ['20250402', 'NEW PAGE REC', '', '', '', 'Recommendation'],
                    ['20250403', 'art rec for jd.doc', '', '', '', 'Recommendation'],
                    ['20250404', 'recommendation', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for group, df_rec")

        # Tests the values in df_rec_check are correct.
        result = df_to_list(df_rec_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250406', 'rec.doc', '', '', '', 'Recommendation'],
                    ['20250406', 'record.doc', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for group, df_rec_check")

    def test_group(self):
        """Test for when the column group indicates recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'intern rec2', '', '', ''],
                ['20250402', 'DC PAGE REC', '', '', ''],
                ['20250403', 'art rec for jd', '', '', ''],
                ['20250404', 'recommendation', '', '', ''],
                ['20250405', '', '', '', ''],
                ['20250406', 'keep', '', '', ''],
                ['20250407', np.nan, '', '', ''],
                ['20250408', 'REC', '', '', ''],
                ['20250409', 'REC1', '', '', '']]
        df = make_df(rows)
        df_rec, df_rec_check = find_recommendation_rows(df)

        # Tests the values in df_rec are correct.
        result = df_to_list(df_rec)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'intern rec2', '', '', '', 'Recommendation'],
                    ['20250402', 'DC PAGE REC', '', '', '', 'Recommendation'],
                    ['20250403', 'art rec for jd', '', '', '', 'Recommendation'],
                    ['20250404', 'recommendation', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for group, df_rec")

        # Tests the values in df_rec_check are correct.
        result = df_to_list(df_rec_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250408', 'REC', '', '', '', 'Recommendation'],
                    ['20250409', 'REC1', '', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for group, df_rec_check")

    def test_none(self):
        """Test for no patterns indicating recommendations are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['20250401', 'Admin', 'docs\\doc.txt', 'file.txt', ''],
                ['20250402', 'Admin', 'docs\\doc.txt', np.nan, np.nan],
                ['20250403', 'Interviews', 'docs\\doc.txt', '', '']]
        df = make_df(rows)
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
        rows = [['20250401', '', '', '', 'intern rec2'],
                ['20250402', '', '', '', 'DCPAGE REC'],
                ['20250403', '', '', '', 'art rec for jd'],
                ['20250404', '', '', '', 'recommendation'],
                ['20250405', '', '', '', ''],
                ['20250406', '', '', '', 'keep'],
                ['20250407', '', '', '', np.nan],
                ['20250408', '', '', '', 'Rec'],
                ['20250409', '', '', '', 'Update_Rec']]
        df = make_df(rows)
        df_rec, df_rec_check = find_recommendation_rows(df)

        # Tests the values in df_rec are correct.
        result = df_to_list(df_rec)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', '', '', '', 'intern rec2', 'Recommendation'],
                    ['20250402', '', '', '', 'DCPAGE REC', 'Recommendation'],
                    ['20250403', '', '', '', 'art rec for jd', 'Recommendation'],
                    ['20250404', '', '', '', 'recommendation', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for text, df_rec")

        # Tests the values in df_rec_check are correct.
        result = df_to_list(df_rec_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250408', '', '', '', 'Rec', 'Recommendation'],
                    ['20250409', '', '', '', 'Update_Rec', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for text, df_rec_check")


if __name__ == '__main__':
    unittest.main()
