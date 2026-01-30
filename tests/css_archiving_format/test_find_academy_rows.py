import numpy as np
import unittest
from css_archiving_format import find_academy_rows
from test_df_search import make_df
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_in_document_name(self):
        """Test for when column in_document_name contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', 'ACADEMY', '', '', '', '', ''],
                ['30601', '', '', 'path\\academy_app.doc', '', '', '', '', ''],
                ['30602', '', '', 'academy-application.doc', '', '', '', '', ''],
                ['30603', '', '', 'path\\sports_academy.doc', '', '', '', '', ''],
                ['30604', '', '', '', '', '', '', '', ''],
                ['30605', '', '', 'path\\Academy', '', '', '', '', ''],
                ['30606', '', '', 'path\\academy_nom.doc', '', '', '', '', ''],
                ['30607', '', '', 'academy', '', '', '', '', ''],
                ['30608', '', '', np.nan, '', '', '', '', ''],
                ['30609', '', '', 'no_match.doc', '', '', '', '', '']]
        md_df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', 'ACADEMY', '', '', '', '', '', 'Academy_Application'],
                    ['30601', '', '', 'path\\academy_app.doc', '', '', '', '', '', 'Academy_Application'],
                    ['30602', '', '', 'academy-application.doc', '', '', '', '', '', 'Academy_Application'],
                    ['30603', '', '', 'path\\sports_academy.doc', '', '', '', '', '', 'Academy_Application'],
                    ['30605', '', '', 'path\\Academy', '', '', '', '', '', 'Academy_Application'],
                    ['30606', '', '', 'path\\academy_nom.doc', '', '', '', '', '', 'Academy_Application'],
                    ['30607', '', '', 'academy', '', '', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_academy_check")

    def test_in_text(self):
        """Test for when column in_text contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', 'For Academy Application', '', '', '', '', '', ''],
                ['30601', '', 'academy_application', '', '', '', '', '', ''],
                ['30602', '', np.nan, '', '', '', '', '', ''],
                ['30603', '', '', '', '', '', '', '', ''],
                ['30604', '', 'Arts academy', '', '', '', '', '', ''],
                ['30605', '', 'academy', '', '', '', '', '', ''],
                ['30606', '', 'no_match', '', '', '', '', '', ''],
                ['30607', '', 'ACADEMY', '', '', '', '', '', '']]
        md_df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', 'For Academy Application', '', '', '', '', '', '', 'Academy_Application'],
                    ['30601', '', 'academy_application', '', '', '', '', '', '', 'Academy_Application'],
                    ['30604', '', 'Arts academy', '', '', '', '', '', '', 'Academy_Application'],
                    ['30605', '', 'academy', '', '', '', '', '', '', 'Academy_Application'],
                    ['30607', '', 'ACADEMY', '', '', '', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_academy_check")

    def test_in_topic(self):
        """Test for when column in_topic contains one of the topics indicating academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'Science Academy', '', '', '', '', '', '', ''],
                ['30601', 'academy', '', '', '', '', '', '', ''],
                ['30602', 'Military^Academy Applicant', '', '', '', '', '', '', ''],
                ['30603', 'Arts', '', '', '', '', '', '', ''],
                ['30604', '', '', '', '', '', '', '', ''],
                ['30605', 'ACADEMY^ADMIN', '', '', '', '', '', '', ''],
                ['30606', np.nan, '', '', '', '', '', '', '']]
        md_df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Science Academy', '', '', '', '', '', '', '', 'Academy_Application'],
                    ['30601', 'academy', '', '', '', '', '', '', '', 'Academy_Application'],
                    ['30602', 'Military^Academy Applicant', '', '', '', '', '', '', '', 'Academy_Application'],
                    ['30605', 'ACADEMY^ADMIN', '', '', '', '', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_academy_check")

    def test_none(self):
        """Test for when no patterns indicating academy applications are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'Arts', np.nan, 'Arts', '', '', '', '', ''],
                ['30601', 'Water', '', '', '', '', '', '', '']]
        md_df = make_df(rows)
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
        rows = [['30600', '', '', '', '', '', '', '', ''],
                ['30601', '', '', '', '', '', '', 'path\\academy app info.pdf', ''],
                ['30602', '', '', '', '', '', '', 'path\\academy', ''],
                ['30603', '', '', '', '', '', '', 'space', ''],
                ['30604', '', '', '', '', '', '', np.nan, ''],
                ['30605', '', '', '', '', '', '', 'academy_noms.pdf', ''],
                ['30606', '', '', '', '', '', '', 'academy', ''],
                ['30607', '', '', '', '', '', '', 'ACADEMY-NOM.doc', '']]
        md_df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', '', 'path\\academy app info.pdf', '', 'Academy_Application'],
                    ['30602', '', '', '', '', '', '', 'path\\academy', '', 'Academy_Application'],
                    ['30605', '', '', '', '', '', '', 'academy_noms.pdf', '', 'Academy_Application'],
                    ['30606', '', '', '', '', '', '', 'academy', '', 'Academy_Application'],
                    ['30607', '', '', '', '', '', '', 'ACADEMY-NOM.doc', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_academy_check")

    def test_out_fillin(self):
        """Test for when column out_fillin contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', '', '', '', 'info'],
                ['30601', '', '', '', '', '', '', '', ''],
                ['30602', '', '', '', '', '', '', '', 'academy nomination info'],
                ['30603', '', '', '', '', '', '', '', 'ACADEMY'],
                ['30604', '', '', '', '', '', '', '', np.nan],
                ['30605', '', '', '', '', '', '', '', 'NEW_ACADEMY_NOMS'],
                ['30606', '', '', '', '', '', '', '', 'academy'],
                ['30607', '', '', '', '', '', '', '', 'Nominations for academy']]
        md_df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30602', '', '', '', '', '', '', '', 'academy nomination info', 'Academy_Application'],
                    ['30603', '', '', '', '', '', '', '', 'ACADEMY', 'Academy_Application'],
                    ['30605', '', '', '', '', '', '', '', 'NEW_ACADEMY_NOMS', 'Academy_Application'],
                    ['30606', '', '', '', '', '', '', '', 'academy', 'Academy_Application'],
                    ['30607', '', '', '', '', '', '', '', 'Nominations for academy', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_academy_check")

    def test_out_text(self):
        """Test for when column out_text contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', '', 'for academy applications', '', ''],
                ['30601', '', '', '', '', '', 'Academy_Application info', '', ''],
                ['30602', '', '', '', '', '', 'ACADEMY', '', ''],
                ['30603', '', '', '', '', '', 'Note', '', ''],
                ['30604', '', '', '', '', '', 'Intl Sci Academy', '', ''],
                ['30605', '', '', '', '', '', 'academy', '', ''],
                ['30606', '', '', '', '', '', '', '', ''],
                ['30607', '', '', '', '', '', np.nan, '', '']]
        md_df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', 'for academy applications', '', '', 'Academy_Application'],
                    ['30601', '', '', '', '', '', 'Academy_Application info', '', '', 'Academy_Application'],
                    ['30602', '', '', '', '', '', 'ACADEMY', '', '', 'Academy_Application'],
                    ['30604', '', '', '', '', '', 'Intl Sci Academy', '', '', 'Academy_Application'],
                    ['30605', '', '', '', '', '', 'academy', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_academy_check")

    def test_out_topic(self):
        """Test for when column out_topic contains one of the topics indicating academy applications"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', 'Academy', '', '', ''],
                ['30601', '', '', '', '', 'General^military service academy', '', '', ''],
                ['30602', '', '', '', '', 'Science Academy Inst', '', '', ''],
                ['30603', '', '', '', '', 'Military', '', '', ''],
                ['30604', '', '', '', '', '', '', '', ''],
                ['30605', '', '', '', '', 'academy', '', '', ''],
                ['30606', '', '', '', '', np.nan, '', '', '']]
        md_df = make_df(rows)
        df_academy, df_academy_check = find_academy_rows(md_df)

        # Tests the values in df_academy are correct.
        result = df_to_list(df_academy)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', 'Academy', '', '', '', 'Academy_Application'],
                    ['30601', '', '', '', '', 'General^military service academy', '', '', '', 'Academy_Application'],
                    ['30602', '', '', '', '', 'Science Academy Inst', '', '', '', 'Academy_Application'],
                    ['30605', '', '', '', '', 'academy', '', '', '', 'Academy_Application']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_academy")

        # Tests the values in df_academy_check are correct.
        result = df_to_list(df_academy_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_academy_check")


if __name__ == '__main__':
    unittest.main()
