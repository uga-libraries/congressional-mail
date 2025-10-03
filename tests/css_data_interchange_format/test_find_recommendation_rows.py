"""
Tests for the function find_recommendation_rows(), 
which finds metadata rows that indicate they are recommendations and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_data_interchange_format import find_recommendation_rows
from test_appraisal_check_df import df_to_list


class MyTestCase(unittest.TestCase):
    
    def test_doc_name(self):
        """Test for when the column communication_document_name indicates recommendations are present
        This is the only column so far that indicate recommendations"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'Admin', 'docs\\Intern Rec.txt', '', ''],
                           ['20250402', 'Admin', 'docs\\PAGE REC.txt', '', ''],
                           ['20250403', 'Admin', 'docs\\intern rec-no', '', ''],
                           ['20250404', 'Admin', 'docs\\doc.txt', 'page recommendation', ''],
                           ['20250405', 'Admin', 'docs\\doc.txt', '', ''],
                           ['20250406', 'Admin', 'docs\\doc.txt', 'intern recommendation', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_rec, df_rec_check = find_recommendation_rows(df)

        # Tests the values in df_rec are correct.
        result = df_to_list(df_rec)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'Admin', 'docs\\Intern Rec.txt', '', '', 'Recommendation'],
                    ['20250402', 'Admin', 'docs\\PAGE REC.txt', '', '', 'Recommendation'],
                    ['20250403', 'Admin', 'docs\\intern rec-no', '', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_rec")

        # Tests the values in df_rec_check are correct.
        result = df_to_list(df_rec_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250404', 'Admin', 'docs\\doc.txt', 'page recommendation', '', 'Recommendation'],
                    ['20250406', 'Admin', 'docs\\doc.txt', 'intern recommendation', '', 'Recommendation']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_rec_check")

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
        
        
if __name__ == '__main__':
    unittest.main()
