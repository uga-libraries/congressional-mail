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

    def test_in_document_name(self):
        """Test for when column in_document_name contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', 'academy app.doc', '', '', '', '', ''],
                              ['30601', '', '', 'path/academy_app.doc', '', '', '', '', ''],
                              ['30602', '', '', 'academy-application.doc', '', '', '', '', ''],
                              ['30603', '', '', 'path/sports_academy.doc', '', '', '', '', ''],
                              ['30604', '', '', '', '', '', '', '', ''],
                              ['30605', '', '', 'academy nom.doc', '', '', '', '', ''],
                              ['30606', '', '', 'path/academy_nom.doc', '', '', '', '', ''],
                              ['30607', '', '', 'academy_nomination.doc', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', 'academy app.doc', '', '', '', '', '', 'Academy_Application'],
                    ['30601', '', '', 'path/academy_app.doc', '', '', '', '', '', 'Academy_Application'],
                    ['30602', '', '', 'academy-application.doc', '', '', '', '', '', 'Academy_Application'],
                    ['30605', '', '', 'academy nom.doc', '', '', '', '', '', 'Academy_Application'],
                    ['30606', '', '', 'path/academy_nom.doc', '', '', '', '', '', 'Academy_Application'],
                    ['30607', '', '', 'academy_nomination.doc', '', '', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', 'path/sports_academy.doc', '', '', '', '', '', 'Academy_Application'],]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_academy_check")

    def test_in_text(self):
        """Test for when column in_text contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'For Academy Application', '', '', '', '', '', ''],
                              ['30601', '', 'academy_application', '', '', '', '', '', ''],
                              ['30602', '', 'academy-applications', '', '', '', '', '', ''],
                              ['30603', '', '', '', '', '', '', '', ''],
                              ['30604', '', 'Arts academy', '', '', '', '', '', ''],
                              ['30605', '', 'Academy Nom Notification', '', '', '', '', '', ''],
                              ['30606', '', 'academy_nom 2025', '', '', '', '', '', ''],
                              ['30607', '', 'academy-nominations', '', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', 'For Academy Application', '', '', '', '', '', '', 'Academy_Application'],
                    ['30601', '', 'academy_application', '', '', '', '', '', '', 'Academy_Application'],
                    ['30602', '', 'academy-applications', '', '', '', '', '', '', 'Academy_Application'],
                    ['30605', '', 'Academy Nom Notification', '', '', '', '', '', '', 'Academy_Application'],
                    ['30606', '', 'academy_nom 2025', '', '', '', '', '', '', 'Academy_Application'],
                    ['30607', '', 'academy-nominations', '', '', '', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30604', '', 'Arts academy', '', '', '', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_academy_check")

    def test_in_topic(self):
        """Test for when column in_topic contains one of the topics indicating academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Science Academy', '', '', '', '', '', '', ''],
                              ['30601', 'military service academy', '', '', '', '', '', '', ''],
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
                    ['30601', 'military service academy', '', '', '', '', '', '', '', 'Academy_Application'],
                    ['30602', 'Military^Academy Applicant', '', '', '', '', '', '', '', 'Academy_Application'],
                    ['30604', 'MILITARY SERVICE ACADEMY^ADMIN', '', '', '', '', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Science Academy', '', '', '', '', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_academy_check")

    def test_none(self):
        """Test for when no patterns indicating academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Arts', '', 'Arts', ''],
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

    def test_out_document_name(self):
        """Test for when column out_document_name contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', '', ''],
                              ['30601', '', '', '', '', '', '', 'path/academy application info.pdf', ''],
                              ['30602', '', '', '', '', '', '', 'path/academy nomination info.pdf', ''],
                              ['30603', '', '', '', '', '', '', 'space academy', ''],
                              ['30604', '', '', '', '', '', '', 'academy_apps.pdf', ''],
                              ['30605', '', '', '', '', '', '', 'academy_noms.pdf', ''],
                              ['30606', '', '', '', '', '', '', 'ACADEMY-APP', ''],
                              ['30607', '', '', '', '', '', '', 'ACADEMY-NOM', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', '', 'path/academy application info.pdf', '', 'Academy_Application'],
                    ['30602', '', '', '', '', '', '', 'path/academy nomination info.pdf', '', 'Academy_Application'],
                    ['30604', '', '', '', '', '', '', 'academy_apps.pdf', '', 'Academy_Application'],
                    ['30605', '', '', '', '', '', '', 'academy_noms.pdf', '', 'Academy_Application'],
                    ['30606', '', '', '', '', '', '', 'ACADEMY-APP', '', 'Academy_Application'],
                    ['30607', '', '', '', '', '', '', 'ACADEMY-NOM', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', '', 'space academy', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_academy_check")

    def test_out_fillin(self):
        """Test for when column out_fillin contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', '', 'academy application info'],
                              ['30601', '', '', '', '', '', '', '', ''],
                              ['30602', '', '', '', '', '', '', '', 'academy nomination info'],
                              ['30603', '', '', '', '', '', '', '', 'ACADEMY_APPS'],
                              ['30604', '', '', '', '', '', '', '', 'academy_info'],
                              ['30605', '', '', '', '', '', '', '', 'ACADEMY_NOMS'],
                              ['30606', '', '', '', '', '', '', '', 'academy-app'],
                              ['30607', '', '', '', '', '', '', '', 'academy-nom']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', '', '', 'academy application info', 'Academy_Application'],
                    ['30602', '', '', '', '', '', '', '', 'academy nomination info', 'Academy_Application'],
                    ['30603', '', '', '', '', '', '', '', 'ACADEMY_APPS', 'Academy_Application'],
                    ['30605', '', '', '', '', '', '', '', 'ACADEMY_NOMS', 'Academy_Application'],
                    ['30606', '', '', '', '', '', '', '', 'academy-app', 'Academy_Application'],
                    ['30607', '', '', '', '', '', '', '', 'academy-nom', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30604', '', '', '', '', '', '', '', 'academy_info', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_academy_check")

    def test_out_text(self):
        """Test for when column out_text contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', 'for academy applications', '', ''],
                              ['30601', '', '', '', '', '', 'Academy_Application info', '', ''],
                              ['30602', '', '', '', '', '', 'ACADEMY-APP', '', ''],
                              ['30603', '', '', '', '', '', 'Academy Note', '', ''],
                              ['30604', '', '', '', '', '', 'Intl Sci Academy', '', ''],
                              ['30605', '', '', '', '', '', 'for academy nomination', '', ''],
                              ['30606', '', '', '', '', '', 'Academy-Nomination acceptance', '', ''],
                              ['30607', '', '', '', '', '', 'ACADEMY-NOM-YES', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', 'for academy applications', '', '', 'Academy_Application'],
                    ['30601', '', '', '', '', '', 'Academy_Application info', '', '', 'Academy_Application'],
                    ['30602', '', '', '', '', '', 'ACADEMY-APP', '', '', 'Academy_Application'],
                    ['30605', '', '', '', '', '', 'for academy nomination', '', '', 'Academy_Application'],
                    ['30606', '', '', '', '', '', 'Academy-Nomination acceptance', '', '', 'Academy_Application'],
                    ['30607', '', '', '', '', '', 'ACADEMY-NOM-YES', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', 'Academy Note', '', '', 'Academy_Application'],
                    ['30604', '', '', '', '', '', 'Intl Sci Academy', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_academy_check")

    def test_out_topic(self):
        """Test for when column out_topic contains one of the topics indicating academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', 'Academy', '', '', ''],
                              ['30601', '', '', '', '', 'General^military service academy', '', '', ''],
                              ['30602', '', '', '', '', 'Science Academy', '', '', ''],
                              ['30603', '', '', '', '', 'Academy APPLICANT^Military', '', '', ''],
                              ['30604', '', '', '', '', 'Academy Applicant', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', 'General^military service academy', '', '', '', 'Academy_Application'],
                    ['30603', '', '', '', '', 'Academy APPLICANT^Military', '', '', '', 'Academy_Application'],
                    ['30604', '', '', '', '', 'Academy Applicant', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', 'Academy', '', '', '', 'Academy_Application'],
                    ['30602', '', '', '', '', 'Science Academy', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_academy_check")


if __name__ == '__main__':
    unittest.main()
