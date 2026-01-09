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

    def test_in_topic(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'CASEWORK', '', '', '', '', '', '', ''],
                              ['30601', 'Misc', '', '', '', '', '', '', ''],
                              ['30602', 'Casework Issues', '', '', '', '', '', '', ''],
                              ['30603', 'Prison Case', '', '', '', '', '', '', ''],
                              ['30604', 'Healthcare^Casework', '', '', '', '', '', '', ''],
                              ['30605', 'case work^Social Security', '', '', '', '', '', '', ''],
                              ['30606', 'Prison Case^No Reply', '', '', '', '', '', '', ''],
                              ['30607', 'KEEP CASE', '', '', '', '', '', '', ''],
                              ['30608', 'Casework^Casework Issues', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'CASEWORK', '', '', '', '', '', '', '', 'Casework'],
                    ['30602', 'Casework Issues', '', '', '', '', '', '', '', 'Casework'],
                    ['30603', 'Prison Case', '', '', '', '', '', '', '', 'Casework'],
                    ['30604', 'Healthcare^Casework', '', '', '', '', '', '', '', 'Casework'],
                    ['30605', 'case work^Social Security', '', '', '', '', '', '', '', 'Casework'],
                    ['30606', 'Prison Case^No Reply', '', '', '', '', '', '', '', 'Casework'],
                    ['30608', 'Casework^Casework Issues', '', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30607', 'KEEP CASE', '', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_casework_check")

    def test_none(self):
        """Test for when there are no indicators of casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Keep', '', '', '', '', 'Keep', '', ''],
                              ['30601', 'Healthcare', '', '', '', 'Healthcare', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched), df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched), df_casework_check")

    def test_out_text(self):
        """Test for when the column out_text is equal to a keyword that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30601', '', '', '', '', '', 'Case!', '', ''],
                              ['30602', '', '', '', '', '', 'CASE', '', ''],
                              ['30603', '', '', '', '', '', 'Not case', '', ''],
                              ['30604', '', '', '', '', '', 'case!', '', ''],
                              ['30605', '', '', '', '', '', 'Just in case', '', ''],
                              ['30606', '', '', '', '', '', 'case', '', ''],
                              ['30607', '', '', '', '', '', 'CASEWORK', '', ''],
                              ['30608', '', '', '', '', '', 'Possibly case work', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', '', '', '', '', '', 'Case!', '', '', 'Casework'],
                    ['30602', '', '', '', '', '', 'CASE', '', '', 'Casework'],
                    ['30604', '', '', '', '', '', 'case!', '', '', 'Casework'],
                    ['30606', '', '', '', '', '', 'case', '', '', 'Casework'],
                    ['30607', '', '', '', '', '', 'CASEWORK', '', '', 'Casework'],
                    ['30608', '', '', '', '', '', 'Possibly case work', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', 'Not case', '', '', 'Casework'],
                    ['30605', '', '', '', '', '', 'Just in case', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_casework_check")

    def test_out_topic(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', 'Case Work', '', '', ''],
                              ['30601', '', '', '', '', 'Healthcare^CASEWORK', '', '', ''],
                              ['30602', '', '', '', '', 'Casework Issues^Social Security', '', '', ''],
                              ['30603', '', '', '', '', 'Prison Case', '', '', ''],
                              ['30604', '', '', '', '', 'casework^casework Issues', '', '', ''],
                              ['30605', '', '', '', '', '', '', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', 'Case Work', '', '', '', 'Casework'],
                    ['30601', '', '', '', '', 'Healthcare^CASEWORK', '', '', '', 'Casework'],
                    ['30602', '', '', '', '', 'Casework Issues^Social Security', '', '', '', 'Casework'],
                    ['30603', '', '', '', '', 'Prison Case', '', '', '', 'Casework'],
                    ['30604', '', '', '', '', 'casework^casework Issues', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_casework_check")

    def test_phase(self):
        """Test for when a column contains a phrase that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', '', '', '', '', '', 'I added to case', '', ''],
                              ['30601', '', '', '', '', '', 'Already opened a case', '', ''],
                              ['30602', '', '', '', '', '', 'CASE CLOSED', '', ''],
                              ['30603', '', '', '', '', '', 'Case for doe', '', ''],
                              ['30604', '', '', '', '', '', 'A case has been opened', '', ''],
                              ['30605', '', '', '', '', '', 'Maybe case issue', '', ''],
                              ['30606', '', '', '', '', '', 'case work', '', ''],
                              ['30607', '', '', '', '', '', 'For casework', '', ''],
                              ['30608', '', '', '', '', '', 'For case work', '', ''],
                              ['30609', 'Closed Case', '', '', '', '', '', '', ''],
                              ['30610', 'Open Case', '', '', '', '', '', '', ''],
                              ['30611', '', '', '', '', '', 'Mary started case yesterday', '', ''],
                              ['30612', 'Roads', '', '', '', '', 'Not a case', '', '']],
                             columns=['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                                      'out_topic', 'out_text', 'out_document_name', 'out_fillin'])
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30606', '', '', '', '', '', 'case work', '', '', 'Casework'],
                    ['30600', '', '', '', '', '', 'I added to case', '', '', 'Casework'],
                    ['30601', '', '', '', '', '', 'Already opened a case', '', '', 'Casework'],
                    ['30602', '', '', '', '', '', 'CASE CLOSED', '', '', 'Casework'],
                    ['30603', '', '', '', '', '', 'Case for doe', '', '', 'Casework'],
                    ['30604', '', '', '', '', '', 'A case has been opened', '', '', 'Casework'],
                    ['30605', '', '', '', '', '', 'Maybe case issue', '', '', 'Casework'],
                    ['30607', '', '', '', '', '', 'For casework', '', '', 'Casework'],
                    ['30608', '', '', '', '', '', 'For case work', '', '', 'Casework'],
                    ['30609', 'Closed Case', '', '', '', '', '', '', '', 'Casework'],
                    ['30610', 'Open Case', '', '', '', '', '', '', '', 'Casework'],
                    ['30611', '', '', '', '', '', 'Mary started case yesterday', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for phrase, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30612', 'Roads', '', '', '', '', 'Not a case', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for phrase, df_casework_check")


if __name__ == '__main__':
    unittest.main()
