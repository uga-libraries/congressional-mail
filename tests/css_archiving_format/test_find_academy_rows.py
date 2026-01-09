"""
Tests for the function find_academy_rows(), 
which finds metadata rows with topics or text that indicate they are academy applications and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_archiving_format import find_academy_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):
    
    def test_in_text(self):
        """Test for when column in_text contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Military', 'For Academy Application', '', '', 'Mil', '', '', ''],
                              ['30601', 'Admin', 'academy_application', '', '', '', 'note', '', ''],
                              ['30602', 'Admin', 'academy-applications', '', '', '', 'note', '', ''],
                              ['30603', 'Economy', '', '', '', 'Economy', '', '', ''],
                              ['30604', 'Arts', 'Arts academy', '', '', 'Arts', '', '', ''],
                              ['30605', 'Admin', 'Academy Nom Notification', '', '', '', 'note', '', ''],
                              ['30606', 'Admin', 'academy_nom 2025', '', '', '', 'note', '', ''],
                              ['30607', 'Admin', 'academy-nominations', '', '', '', 'note', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Military', 'For Academy Application', '', '', 'Mil', '', '', '', 'Academy_Application'],
                    ['30601', 'Admin', 'academy_application', '', '', '', 'note', '', '', 'Academy_Application'],
                    ['30602', 'Admin', 'academy-applications', '', '', '', 'note', '', '', 'Academy_Application'],
                    ['30605', 'Admin', 'Academy Nom Notification', '', '', '', 'note', '', '', 'Academy_Application'],
                    ['30606', 'Admin', 'academy_nom 2025', '', '', '', 'note', '', '', 'Academy_Application'],
                    ['30607', 'Admin', 'academy-nominations', '', '', '', 'note', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30604', 'Arts', 'Arts academy', '', '', 'Arts', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_academy_check")

    def test_in_topic(self):
        """Test for when column in_topic contains one of the topics indicating academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Science Academy', '', '', '', 'Water', '', '', ''],
                              ['30601', 'military service academy', '', '', '', 'Admin', '', '', ''],
                              ['30602', 'Military^Academy Applicant', '', '', '', '', '', '', ''],
                              ['30603', 'Arts', '', '', '', '', '', '', ''],
                              ['30604', 'MILITARY SERVICE ACADEMY^ADMIN', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', 'military service academy', '', '', '', 'Admin', '', '', '', 'Academy_Application'],
                    ['30602', 'Military^Academy Applicant', '', '', '', '', '', '', '', 'Academy_Application'],
                    ['30604', 'MILITARY SERVICE ACADEMY^ADMIN', '', '', '', '', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Science Academy', '', '', '', 'Water', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_academy_check")

    def test_none(self):
        """Test for when no patterns indicating academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Arts', 'Note', 'Arts', 'Note'],
                              ['30601', 'Water', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched), df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text', 
                     'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched), df_academy_check")

    def test_out_text(self):
        """Test for when column out_text contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', 'for academy applications', '', ''],
                              ['30601', '', 'note', '', '', '', 'Academy_Application info', '', ''],
                              ['30602', 'Military', '', '', '', '', 'ACADEMY-APP', '', ''],
                              ['30603', 'Arts', 'Note', '', '', 'Arts', 'Academy Note', '', ''],
                              ['30604', 'Science', '', '', '', 'Science', 'Intl Sci Academy', '', ''],
                              ['30605', '', 'note', '', '', '', 'for academy nomination', '', ''],
                              ['30606', '', 'note', '', '', '', 'Academy-Nomination acceptance', '', ''],
                              ['30607', '', 'note', '', '', '', 'ACADEMY-NOM-YES', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', 'for academy applications', '', '', 'Academy_Application'],
                    ['30601', '', 'note', '', '', '', 'Academy_Application info', '', '', 'Academy_Application'],
                    ['30602', 'Military', '', '', '', '', 'ACADEMY-APP', '', '', 'Academy_Application'],
                    ['30605', '', 'note', '', '', '', 'for academy nomination', '', '', 'Academy_Application'],
                    ['30606', '', 'note', '', '', '', 'Academy-Nomination acceptance', '', '', 'Academy_Application'],
                    ['30607', '', 'note', '', '', '', 'ACADEMY-NOM-YES', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', 'Arts', 'Note', '', '', 'Arts', 'Academy Note', '', '', 'Academy_Application'],
                    ['30604', 'Science', '', '', '', 'Science', 'Intl Sci Academy', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_academy_check")

    def test_out_topic(self):
        """Test for when column out_topic contains one of the topics indicating academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Transportation', '', '', '', 'Academy', '', '', ''],
                              ['30601', 'General', '', '', '', 'General^military service academy', '', '', ''],
                              ['30602', 'General', '', '', '', 'Science Academy', 'Note', '', ''],
                              ['30603', '', '', '', '', 'Academy APPLICANT^Military', '', '', ''],
                              ['30604', '', '', '', '', 'Academy Applicant', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', 'General', '', '', '', 'General^military service academy', '', '', '',
                     'Academy_Application'],
                    ['30603', '', '', '', '', 'Academy APPLICANT^Military', '', '', '', 'Academy_Application'],
                    ['30604', '', '', '', '', 'Academy Applicant', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Transportation', '', '', '', 'Academy', '', '', '', 'Academy_Application'],
                    ['30602', 'General', '', '', '', 'Science Academy', 'Note', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_academy_check")


if __name__ == '__main__':
    unittest.main()
