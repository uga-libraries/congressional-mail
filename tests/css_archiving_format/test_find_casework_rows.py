"""
Tests for the function find_casework_rows(), 
which finds metadata rows with topics or text that indicate they are casework and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_archiving_format import find_casework_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_in_document_name(self):
        """Test for when the column in_document_name contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', r'path\added to case.txt', '', '', '', '', '', ''],
                              ['30601', '', '', '', r'path\already open.txt', '', '', '', '', '', ''],
                              ['30602', '', '', '', r'path\case closed.txt', '', '', '', '', '', ''],
                              ['30603', '', '', '', r'path\case for.txt', '', '', '', '', '', ''],
                              ['30604', '', '', '', r'path\case has been opened.txt', '', '', '', '', '', ''],
                              ['30605', '', '', '', '', '', '', '', '', '', ''],
                              ['30606', '', '', '', r'path\check for case.txt', '', '', '', '', '', ''],
                              ['30607', '', '', '', r'path\case issue.txt', '', '', '', '', '', ''],
                              ['30608', '', '', '', r'path\case work.txt', '', '', '', '', '', ''],
                              ['30609', '', '', '', r'path\casework.txt', '', '', '', '', '', ''],
                              ['30610', '', '', '', r'path\closed case.txt', '', '', '', '', '', ''],
                              ['30611', '', '', '', r'path\open case.txt', '', '', '', '', '', ''],
                              ['30612', '', '', '', r'path\started case.txt', '', '', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', r'path\added to case.txt', '', '', '', '', '', '', 'Casework'],
                    ['30601', '', '', '', r'path\already open.txt', '', '', '', '', '', '', 'Casework'],
                    ['30602', '', '', '', r'path\case closed.txt', '', '', '', '', '', '', 'Casework'],
                    ['30603', '', '', '', r'path\case for.txt', '', '', '', '', '', '', 'Casework'],
                    ['30604', '', '', '', r'path\case has been opened.txt', '', '', '', '', '', '', 'Casework'],
                    ['30607', '', '', '', r'path\case issue.txt', '', '', '', '', '', '', 'Casework'],
                    ['30608', '', '', '', r'path\case work.txt', '', '', '', '', '', '', 'Casework'],
                    ['30609', '', '', '', r'path\casework.txt', '', '', '', '', '', '', 'Casework'],
                    ['30610', '', '', '', r'path\closed case.txt', '', '', '', '', '', '', 'Casework'],
                    ['30611', '', '', '', r'path\open case.txt', '', '', '', '', '', '', 'Casework'],
                    ['30612', '', '', '', r'path\started case.txt', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30606', '', '', '', r'path\check for case.txt', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_casework_check")

    def test_in_text(self):
        """Test for when the column NAME contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', '', '', '', ''],
                              ['30601', '', '', '', '', '', '', '', '', '', ''],
                              ['30602', '', '', '', '', '', '', '', '', '', ''],
                              ['30603', '', '', '', '', '', '', '', '', '', ''],
                              ['30604', '', '', '', '', '', '', '', '', '', ''],
                              ['30605', '', '', '', '', '', '', '', '', '', ''],
                              ['30606', '', '', '', '', '', '', '', '', '', ''],
                              ['30607', '', '', '', '', '', '', '', '', '', ''],
                              ['30608', '', '', '', '', '', '', '', '', '', ''],
                              ['30609', '', '', '', '', '', '', '', '', '', ''],
                              ['30610', '', '', '', '', '', '', '', '', '', ''],
                              ['30611', '', '', '', '', '', '', '', '', '', ''],
                              ['30612', '', '', '', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for COLUMN, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for COLUMN, df_casework_check")

    def test_in_topic(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'CASEWORK', '', '', '', '', '', '', '', ''],
                              ['30601', '', 'Misc', '', '', '', '', '', '', '', ''],
                              ['30602', '', 'Casework Issues', '', '', '', '', '', '', '', ''],
                              ['30603', '', 'Prison Case', '', '', '', '', '', '', '', ''],
                              ['30604', '', 'Healthcare^Casework', '', '', '', '', '', '', '', ''],
                              ['30605', '', 'case work^Social Security', '', '', '', '', '', '', '', ''],
                              ['30606', '', 'Prison Case^No Reply', '', '', '', '', '', '', '', ''],
                              ['30607', '', 'KEEP CASE', '', '', '', '', '', '', '', ''],
                              ['30608', '', 'Casework^Casework Issues', '', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', 'CASEWORK', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30602', '', 'Casework Issues', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30603', '', 'Prison Case', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30604', '', 'Healthcare^Casework', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30605', '', 'case work^Social Security', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30606', '', 'Prison Case^No Reply', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30608', '', 'Casework^Casework Issues', '', '', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30607', '', 'KEEP CASE', '', '', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_casework_check")

    def test_in_type(self):
        """Test for when the column in_type is equal to CASE"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'CASE', '', '', '', '', '', '', '', '', ''],
                              ['30601', 'GENERAL', '', '', '', '', '', '', '', '', ''],
                              ['30602', '', '', '', '', '', '', '', '', '', ''],
                              ['30603', 'CASE', '', '', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'CASE', '', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30603', 'CASE', '', '', '', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_type, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for in_type, df_casework_check")

    def test_none(self):
        """Test for when there are no indicators of casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', 'Keep', '', '', '', '', '', 'Keep', '', ''],
                              ['30601', '', 'Healthcare', '', '', '', '', 'Healthcare', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched), df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched), df_casework_check")

    def test_out_document_name(self):
        """Test for when the column out_document_name contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', '', '', '', ''],
                              ['30601', '', '', '', '', '', '', '', '', r'path\added to case.txt', ''],
                              ['30602', '', '', '', '', '', '', '', '', r'path\already open.txt', ''],
                              ['30603', '', '', '', '', '', '', '', '', r'path\case closed.txt', ''],
                              ['30604', '', '', '', '', '', '', '', '', r'path\case for.txt', ''],
                              ['30605', '', '', '', '', '', '', '', '', r'path\case has been opened.txt', ''],
                              ['30606', '', '', '', '', '', '', '', '', r'path\check for case.txt', ''],
                              ['30607', '', '', '', '', '', '', '', '', r'path\case issue.txt', ''],
                              ['30608', '', '', '', '', '', '', '', '', r'path\case work.txt', ''],
                              ['30609', '', '', '', '', '', '', '', '', r'path\casework.txt', ''],
                              ['30610', '', '', '', '', '', '', '', '', r'path\closed case.txt', ''],
                              ['30611', '', '', '', '', '', '', '', '', r'path\open case.txt', ''],
                              ['30612', '', '', '', '', '', '', '', '', r'path\started case.txt', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', '', '', '', r'path\added to case.txt', '', 'Casework'],
                    ['30602', '', '', '', '', '', '', '', '', r'path\already open.txt', '', 'Casework'],
                    ['30603', '', '', '', '', '', '', '', '', r'path\case closed.txt', '', 'Casework'],
                    ['30604', '', '', '', '', '', '', '', '', r'path\case for.txt', '', 'Casework'],
                    ['30605', '', '', '', '', '', '', '', '', r'path\case has been opened.txt', '', 'Casework'],
                    ['30607', '', '', '', '', '', '', '', '', r'path\case issue.txt', '', 'Casework'],
                    ['30608', '', '', '', '', '', '', '', '', r'path\case work.txt', '', 'Casework'],
                    ['30609', '', '', '', '', '', '', '', '', r'path\casework.txt', '', 'Casework'],
                    ['30610', '', '', '', '', '', '', '', '', r'path\closed case.txt', '', 'Casework'],
                    ['30611', '', '', '', '', '', '', '', '', r'path\open case.txt', '', 'Casework'],
                    ['30612', '', '', '', '', '', '', '', '', r'path\started case.txt', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30606', '', '', '', '', '', '', '', '', r'path\check for case.txt', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_casework_check")

    def test_out_fillin(self):
        """Test for when the column NAME contains one of the keywords"""
        # TODO
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', '', '', '', ''],
                              ['30601', '', '', '', '', '', '', '', '', '', ''],
                              ['30602', '', '', '', '', '', '', '', '', '', ''],
                              ['30603', '', '', '', '', '', '', '', '', '', ''],
                              ['30604', '', '', '', '', '', '', '', '', '', ''],
                              ['30605', '', '', '', '', '', '', '', '', '', ''],
                              ['30606', '', '', '', '', '', '', '', '', '', ''],
                              ['30607', '', '', '', '', '', '', '', '', '', ''],
                              ['30608', '', '', '', '', '', '', '', '', '', ''],
                              ['30609', '', '', '', '', '', '', '', '', '', ''],
                              ['30610', '', '', '', '', '', '', '', '', '', ''],
                              ['30611', '', '', '', '', '', '', '', '', '', ''],
                              ['30612', '', '', '', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for COLUMN, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for COLUMN, df_casework_check")

    def test_out_text(self):
        """Test for when the column NAME contains one of the keywords"""
        # TODO
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', '', '', '', ''],
                              ['30601', '', '', '', '', '', '', '', '', '', ''],
                              ['30602', '', '', '', '', '', '', '', '', '', ''],
                              ['30603', '', '', '', '', '', '', '', '', '', ''],
                              ['30604', '', '', '', '', '', '', '', '', '', ''],
                              ['30605', '', '', '', '', '', '', '', '', '', ''],
                              ['30606', '', '', '', '', '', '', '', '', '', ''],
                              ['30607', '', '', '', '', '', '', '', '', '', ''],
                              ['30608', '', '', '', '', '', '', '', '', '', ''],
                              ['30609', '', '', '', '', '', '', '', '', '', ''],
                              ['30610', '', '', '', '', '', '', '', '', '', ''],
                              ['30611', '', '', '', '', '', '', '', '', '', ''],
                              ['30612', '', '', '', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for COLUMN, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for COLUMN, df_casework_check")

    def test_out_text_exact(self):
        """Test for when the column out_text is equal to a keyword that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', '', '', '', '', '', '', '', 'Case!', '', ''],
                              ['30602', '', '', '', '', '', '', '', 'CASE', '', ''],
                              ['30603', '', '', '', '', '', '', '', 'Just in case', '', ''],
                              ['30604', '', '', '', '', '', '', '', 'case', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', '', '', 'Case!', '', '', 'Casework'],
                    ['30602', '', '', '', '', '', '', '', 'CASE', '', '', 'Casework'],
                    ['30604', '', '', '', '', '', '', '', 'case', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_text_exact, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', '', '', 'Just in case', '', '', 'Casework'],]
        self.assertEqual(expected, result, "Problem with test for out_text_exact, df_casework_check")

    def test_out_topic(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', 'Case Work', '', '', ''],
                              ['30601', '', '', '', '', '', '', 'Healthcare^CASEWORK', '', '', ''],
                              ['30602', '', '', '', '', '', '', 'Casework Issues^Social Security', '', '', ''],
                              ['30603', '', '', '', '', '', '', 'Prison Case', '', '', ''],
                              ['30604', '', '', '', '', '', '', 'casework^casework Issues', '', '', ''],
                              ['30605', '', '', '', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', '', 'Case Work', '', '', '', 'Casework'],
                    ['30601', '', '', '', '', '', '', 'Healthcare^CASEWORK', '', '', '', 'Casework'],
                    ['30602', '', '', '', '', '', '', 'Casework Issues^Social Security', '', '', '', 'Casework'],
                    ['30603', '', '', '', '', '', '', 'Prison Case', '', '', '', 'Casework'],
                    ['30604', '', '', '', '', '', '', 'casework^casework Issues', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_casework_check")

    def test_out_type(self):
        """Test for when the column out_type is equal to CASE"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', 'CASE', '', '', '', ''],
                              ['30601', '', '', '', '', '', 'GENERAL', '', '', '', ''],
                              ['30602', '', '', '', '', '', '', '', '', '', ''],
                              ['30603', '', '', '', '', '', 'CASE', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', 'CASE', '', '', '', '', 'Casework'],
                    ['30603', '', '', '', '', '', 'CASE', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_type, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_type, df_casework_check")


if __name__ == '__main__':
    unittest.main()
