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
        """Test for when the column in_text contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', 'I added to case.', '', '', '', '', '', '', ''],
                              ['30601', '', '', 'already opened', '', '', '', '', '', '', ''],
                              ['30602', '', '', 'Doe case closed', '', '', '', '', '', '', ''],
                              ['30603', '', '', 'Case for Doe', '', '', '', '', '', '', ''],
                              ['30604', '', '', 'case has been opened', '', '', '', '', '', '', ''],
                              ['30605', '', '', '', '', '', '', '', '', '', ''],
                              ['30606', '', '', 'check if case', '', '', '', '', '', '', ''],
                              ['30607', '', '', 'case issue', '', '', '', '', '', '', ''],
                              ['30608', '', '', 'case work', '', '', '', '', '', '', ''],
                              ['30609', '', '', 'CASEWORK', '', '', '', '', '', '', ''],
                              ['30610', '', '', 'closed case', '', '', '', '', '', '', ''],
                              ['30611', '', '', 'open case', '', '', '', '', '', '', ''],
                              ['30612', '', '', 'started case', '', '', '', '', '', '', ''],
                              ['30613', '', '', 'keep', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', 'I added to case.', '', '', '', '', '', '', '', 'Casework'],
                    ['30601', '', '', 'already opened', '', '', '', '', '', '', '', 'Casework'],
                    ['30602', '', '', 'Doe case closed', '', '', '', '', '', '', '', 'Casework'],
                    ['30603', '', '', 'Case for Doe', '', '', '', '', '', '', '', 'Casework'],
                    ['30604', '', '', 'case has been opened', '', '', '', '', '', '', '', 'Casework'],
                    ['30607', '', '', 'case issue', '', '', '', '', '', '', '', 'Casework'],
                    ['30608', '', '', 'case work', '', '', '', '', '', '', '', 'Casework'],
                    ['30609', '', '', 'CASEWORK', '', '', '', '', '', '', '', 'Casework'],
                    ['30610', '', '', 'closed case', '', '', '', '', '', '', '', 'Casework'],
                    ['30611', '', '', 'open case', '', '', '', '', '', '', '', 'Casework'],
                    ['30612', '', '', 'started case', '', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30606', '', '', 'check if case', '', '', '', '', '', '', '', 'Casework'],]
        self.assertEqual(expected, result, "Problem with test for in_text, df_casework_check")

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
        """Test for when the column out_fillin contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', '', '', '', 'check for case'],
                              ['30601', '', '', '', '', '', '', '', '', '', 'Added to case.'],
                              ['30602', '', '', '', '', '', '', '', '', '', 'Case is already open'],
                              ['30603', '', '', '', '', '', '', '', '', '', 'case closed'],
                              ['30604', '', '', '', '', '', '', '', '', '', 'case for doe'],
                              ['30605', '', '', '', '', '', '', '', '', '', 'case has been opened'],
                              ['30606', '', '', '', '', '', '', '', '', '', ''],
                              ['30607', '', '', '', '', '', '', '', '', '', 'check for case 2'],
                              ['30608', '', '', '', '', '', '', '', '', '', 'keep'],
                              ['30609', '', '', '', '', '', '', '', '', '', 'CASE ISSUE'],
                              ['30610', '', '', '', '', '', '', '', '', '', 'case work'],
                              ['30611', '', '', '', '', '', '', '', '', '', 'casework'],
                              ['30612', '', '', '', '', '', '', '', '', '', 'closed case'],
                              ['30613', '', '', '', '', '', '', '', '', '', 'open case'],
                              ['30614', '', '', '', '', '', '', '', '', '', 'started case']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', '', '', '', '', 'Added to case.', 'Casework'],
                    ['30602', '', '', '', '', '', '', '', '', '', 'Case is already open', 'Casework'],
                    ['30603', '', '', '', '', '', '', '', '', '', 'case closed', 'Casework'],
                    ['30604', '', '', '', '', '', '', '', '', '', 'case for doe', 'Casework'],
                    ['30605', '', '', '', '', '', '', '', '', '', 'case has been opened', 'Casework'],
                    ['30609', '', '', '', '', '', '', '', '', '', 'CASE ISSUE', 'Casework'],
                    ['30610', '', '', '', '', '', '', '', '', '', 'case work', 'Casework'],
                    ['30611', '', '', '', '', '', '', '', '', '', 'casework', 'Casework'],
                    ['30612', '', '', '', '', '', '', '', '', '', 'closed case', 'Casework'],
                    ['30613', '', '', '', '', '', '', '', '', '', 'open case', 'Casework'],
                    ['30614', '', '', '', '', '', '', '', '', '', 'started case', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', '', '', '', '', '', 'check for case', 'Casework'],
                    ['30607', '', '', '', '', '', '', '', '', '', 'check for case 2', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_casework_check")

    def test_out_text(self):
        """Test for when the column out_text contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', '', '', 'keep', '', ''],
                              ['30601', '', '', '', '', '', '', '', 'added to case', '', ''],
                              ['30602', '', '', '', '', '', '', '', 'already open', '', ''],
                              ['30603', '', '', '', '', '', '', '', 'case closed', '', ''],
                              ['30604', '', '', '', '', '', '', '', 'case for', '', ''],
                              ['30605', '', '', '', '', '', '', '', 'case has been opened', '', ''],
                              ['30606', '', '', '', '', '', '', '', '', '', ''],
                              ['30607', '', '', '', '', '', '', '', 'Check if case', '', ''],
                              ['30608', '', '', '', '', '', '', '', 'Case Issue', '', ''],
                              ['30609', '', '', '', '', '', '', '', 'Possible case work.', '', ''],
                              ['30610', '', '', '', '', '', '', '', 'new casework', '', ''],
                              ['30611', '', '', '', '', '', '', '', 'closed case yesterday', '', ''],
                              ['30612', '', '', '', '', '', '', '', 'open case', '', ''],
                              ['30612', '', '', '', '', '', '', '', 'started case', '', '']],
                             columns=['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', '', '', 'added to case', '', '', 'Casework'],
                    ['30602', '', '', '', '', '', '', '', 'already open', '', '', 'Casework'],
                    ['30603', '', '', '', '', '', '', '', 'case closed', '', '', 'Casework'],
                    ['30604', '', '', '', '', '', '', '', 'case for', '', '', 'Casework'],
                    ['30605', '', '', '', '', '', '', '', 'case has been opened', '', '', 'Casework'],
                    ['30608', '', '', '', '', '', '', '', 'Case Issue', '', '', 'Casework'],
                    ['30609', '', '', '', '', '', '', '', 'Possible case work.', '', '', 'Casework'],
                    ['30610', '', '', '', '', '', '', '', 'new casework', '', '', 'Casework'],
                    ['30611', '', '', '', '', '', '', '', 'closed case yesterday', '', '', 'Casework'],
                    ['30612', '', '', '', '', '', '', '', 'open case', '', '', 'Casework'],
                    ['30612', '', '', '', '', '', '', '', 'started case', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30607', '', '', '', '', '', '', '', 'Check if case', '', '', 'Casework']]
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
