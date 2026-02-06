import numpy as np
import pandas as pd
import unittest
from css_archiving_format import find_casework_rows
from test_read_metadata import df_to_list


def make_df(rows):
    """Make a df to use for test input"""
    column_names = ['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                    'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin']
    df = pd.DataFrame(rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def test_in_document_name(self):
        """Test for when the column in_document_name contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', 'ADDED TO CASE LOG', '', '', '', '', '', ''],
                ['30601', '', '', '', '\\Form\\Already Open', '', '', '', '', '', ''],
                ['30602', '', '', '', '', '', '', '', '', '', ''],
                ['30603', '', '', '', '\\doc\\case.doc', '', '', '', '', '', ''],
                ['30604', '', '', '', '\\Form\\Case.doc', '', '', '', '', '', ''],
                ['30605', '', '', '', '\\Form\\Thanks.doc', '', '', '', '', '', ''],
                ['30606', '', '', '', np.nan, '', '', '', '', '', ''],
                ['30607', '', '', '', 'case closed', '', '', '', '', '', ''],
                ['30608', '', '', '', '\\doc\\case file.doc', '', '', '', '', '', ''],
                ['30609', '', '', '', 'case', '', '', '', '', '', '']]
        md_df = make_df(rows)
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30609', '', '', '', 'case', '', '', '', '', '', '', 'Casework'],
                    ['30600', '', '', '', 'ADDED TO CASE LOG', '', '', '', '', '', '', 'Casework'],
                    ['30601', '', '', '', '\\Form\\Already Open', '', '', '', '', '', '', 'Casework'],
                    ['30607', '', '', '', 'case closed', '', '', '', '', '', '', 'Casework'],
                    ['30608', '', '', '', '\\doc\\case file.doc', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '\\doc\\case.doc', '', '', '', '', '', '', 'Casework'],
                    ['30604', '', '', '', '\\Form\\Case.doc', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_document_name, df_casework_check")

    def test_in_fillin(self):
        """Test for when the column in_fillin contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', 'INITIALSSACASE RESPOND', '', '', '', '', ''],
                ['30601', '', '', '', '', 'Still Open Case', '', '', '', '', ''],
                ['30602', '', '', '', '', '', '', '', '', '', ''],
                ['30603', '', '', '', '', 'maybe case', '', '', '', '', ''],
                ['30604', '', '', '', '', 'Not Case', '', '', '', '', ''],
                ['30605', '', '', '', '', 'thanks', '', '', '', '', ''],
                ['30606', '', '', '', '', np.nan, '', '', '', '', ''],
                ['30607', '', '', '', '', 'open sixth district cases', '', '', '', '', ''],
                ['30608', '', '', '', '', 'jv prison case help', '', '', '', '', ''],
                ['30609', '', '', '', '', 'CASE', '', '', '', '', '']]
        md_df = make_df(rows)
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30609', '', '', '', '', 'CASE', '', '', '', '', '', 'Casework'],
                    ['30600', '', '', '', '', 'INITIALSSACASE RESPOND', '', '', '', '', '', 'Casework'],
                    ['30601', '', '', '', '', 'Still Open Case', '', '', '', '', '', 'Casework'],
                    ['30607', '', '', '', '', 'open sixth district cases', '', '', '', '', '', 'Casework'],
                    ['30608', '', '', '', '', 'jv prison case help', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_fillin, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', 'maybe case', '', '', '', '', '', 'Casework'],
                    ['30604', '', '', '', '', 'Not Case', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_fillin, df_casework_check")

    def test_in_text(self):
        """Test for when the column in_text contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', 'CASE FOR JD', '', '', '', '', '', '', ''],
                ['30601', '', '', 'Check Case Has', '', '', '', '', '', '', ''],
                ['30602', '', '', '', '', '', '', '', '', '', ''],
                ['30603', '', '', 'probably case', '', '', '', '', '', '', ''],
                ['30604', '', '', 'In Case', '', '', '', '', '', '', ''],
                ['30605', '', '', 'thanks', '', '', '', '', '', '', ''],
                ['30606', '', '', np.nan, '', '', '', '', '', '', ''],
                ['30607', '', '', 'case issue', '', '', '', '', '', '', ''],
                ['30608', '', '', 'is case open still?', '', '', '', '', '', '', ''],
                ['30609', '', '', 'Case', '', '', '', '', '', '', '']]
        md_df = make_df(rows)
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30609', '', '', 'Case', '', '', '', '', '', '', '', 'Casework'],
                    ['30600', '', '', 'CASE FOR JD', '', '', '', '', '', '', '', 'Casework'],
                    ['30601', '', '', 'Check Case Has', '', '', '', '', '', '', '', 'Casework'],
                    ['30607', '', '', 'case issue', '', '', '', '', '', '', '', 'Casework'],
                    ['30608', '', '', 'is case open still?', '', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', 'probably case', '', '', '', '', '', '', '', 'Casework'],
                    ['30604', '', '', 'In Case', '', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_text, df_casework_check")

    def test_in_topic(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', 'CASE WORK TODO', '', '', '', '', '', '', '', ''],
                ['30601', '', 'Urgent Casework', '', '', '', '', '', '', '', ''],
                ['30602', '', '', '', '', '', '', '', '', '', ''],
                ['30603', '', 'maybe case', '', '', '', '', '', '', '', ''],
                ['30604', '', 'Not Case', '', '', '', '', '', '', '', ''],
                ['30605', '', 'Admin', '', '', '', '', '', '', '', ''],
                ['30606', '', np.nan, '', '', '', '', '', '', '', ''],
                ['30607', '', 'closed case', '', '', '', '', '', '', '', ''],
                ['30608', '', 'dc forwarded to me for reply', '', '', '', '', '', '', '', ''],
                ['30609', '', 'case', '', '', '', '', '', '', '', '']]
        md_df = make_df(rows)
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30609', '', 'case', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30600', '', 'CASE WORK TODO', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30601', '', 'Urgent Casework', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30607', '', 'closed case', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30608', '', 'dc forwarded to me for reply', '', '', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', 'maybe case', '', '', '', '', '', '', '', '', 'Casework'],
                    ['30604', '', 'Not Case', '', '', '', '', '', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for in_topic, df_casework_check")

    def test_none(self):
        """Test for when there are no indicators of casework"""
        # Makes a dataframe to use as test input and runs the function.
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'text', '', np.nan, '', 'text', '', '', '', '', ''],
                ['30601', 'text', '', np.nan, '', '', '', '', '', '', ''],
                ['30602', 'text', '', np.nan, '', np.nan, '', '', '', '', ''],
                ['30603-case', 'text', '', np.nan, '', '', '', '', '', '', '']]
        md_df = make_df(rows)
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
        rows = [['30600', '', '', '', '', '', '', '', '', 'STARTED CASE LOG', ''],
                ['30601', '', '', '', '', '', '', '', '', '\\Doc\\Added To Case.txt', ''],
                ['30602', '', '', '', '', '', '', '', '', '', ''],
                ['30603', '', '', '', '', '', '', '', '', '\\form\\case.txt', ''],
                ['30604', '', '', '', '', '', '', '', '', '\\Doc\\Case12.txt', ''],
                ['30605', '', '', '', '', '', '', '', '', '\\form\\thanks.txt', ''],
                ['30606', '', '', '', '', '', '', '', '', np.nan, ''],
                ['30607', '', '', '', '', '', '', '', '', 'already open', ''],
                ['30608', '', '', '', '', '', '', '', '', '\\form\\case closed.txt', ''],
                ['30609', '', '', '', '', '', '', '', '', 'case!', '']]
        md_df = make_df(rows)
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30609', '', '', '', '', '', '', '', '', 'case!', '', 'Casework'],
                    ['30600', '', '', '', '', '', '', '', '', 'STARTED CASE LOG', '', 'Casework'],
                    ['30601', '', '', '', '', '', '', '', '', '\\Doc\\Added To Case.txt', '', 'Casework'],
                    ['30607', '', '', '', '', '', '', '', '', 'already open', '', 'Casework'],
                    ['30608', '', '', '', '', '', '', '', '', '\\form\\case closed.txt', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', '', '', '', '\\form\\case.txt', '', 'Casework'],
                    ['30604', '', '', '', '', '', '', '', '', '\\Doc\\Case12.txt', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_document_name, df_casework_check")

    def test_out_fillin(self):
        """Test for when the column out_fillin contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', '', '', '', '', '', 'CASE FILE_ABC'],
                ['30601', '', '', '', '', '', '', '', '', '', 'New Case For'],
                ['30602', '', '', '', '', '', '', '', '', '', ''],
                ['30603', '', '', '', '', '', '', '', '', '', 'not case'],
                ['30604', '', '', '', '', '', '', '', '', '', 'Possible Case'],
                ['30605', '', '', '', '', '', '', '', '', '', 'Thanks'],
                ['30606', '', '', '', '', '', '', '', '', '', np.nan],
                ['30607', '', '', '', '', '', '', '', '', '', 'case has'],
                ['30608', '', '', '', '', '', '', '', '', '', 'potential case issue - review'],
                ['30609', '', '', '', '', '', '', '', '', '', 'CASE!']]
        md_df = make_df(rows)
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30609', '', '', '', '', '', '', '', '', '', 'CASE!', 'Casework'],
                    ['30600', '', '', '', '', '', '', '', '', '', 'CASE FILE_ABC', 'Casework'],
                    ['30601', '', '', '', '', '', '', '', '', '', 'New Case For', 'Casework'],
                    ['30607', '', '', '', '', '', '', '', '', '', 'case has', 'Casework'],
                    ['30608', '', '', '', '', '', '', '', '', '', 'potential case issue - review', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', '', '', '', '', 'not case', 'Casework'],
                    ['30604', '', '', '', '', '', '', '', '', '', 'Possible Case', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_fillin, df_casework_check")

    def test_out_text(self):
        """Test for when the column out_text contains one of the keywords"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', '', '', '', 'CASE OPEN ABC', '', ''],
                ['30601', '', '', '', '', '', '', '', 'New Case Work', '', ''],
                ['30602', '', '', '', '', '', '', '', '', '', ''],
                ['30603', '', '', '', '', '', '', '', 'maybe case', '', ''],
                ['30604', '', '', '', '', '', '', '', 'Just In Case', '', ''],
                ['30605', '', '', '', '', '', '', '', 'thanks', '', ''],
                ['30606', '', '', '', '', '', '', '', np.nan, '', ''],
                ['30607', '', '', '', '', '', '', '', 'casework', '', ''],
                ['30608', '', '', '', '', '', '', '', 'I closed case.', '', ''],
                ['30609', '', '', '', '', '', '', '', 'Case!', '', '']]
        md_df = make_df(rows)
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30609', '', '', '', '', '', '', '', 'Case!', '', '', 'Casework'],
                    ['30600', '', '', '', '', '', '', '', 'CASE OPEN ABC', '', '', 'Casework'],
                    ['30601', '', '', '', '', '', '', '', 'New Case Work', '', '', 'Casework'],
                    ['30607', '', '', '', '', '', '', '', 'casework', '', '', 'Casework'],
                    ['30608', '', '', '', '', '', '', '', 'I closed case.', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', '', '', 'maybe case', '', '', 'Casework'],
                    ['30604', '', '', '', '', '', '', '', 'Just In Case', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_text, df_casework_check")

    def test_out_topic(self):
        """Test for when the column in_topic contains a topic that indicates casework"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', '', '', 'FORWARDED TO ME^ADMIN', '', '', ''],
                ['30601', '', '', '', '', '', '', 'Admin^InitialSSACase', '', '', ''],
                ['30602', '', '', '', '', '', '', '', '', '', ''],
                ['30603', '', '', '', '', '', '', 'admin^case', '', '', ''],
                ['30604', '', '', '', '', '', '', 'Case^IP', '', '', ''],
                ['30605', '', '', '', '', '', '', 'Thanks', '', '', ''],
                ['30606', '', '', '', '', '', '', np.nan, '', '', ''],
                ['30607', '', '', '', '', '', '', 'open case', '', '', ''],
                ['30608', '', '', '', '', '', '', 'admin^open sixth district cases^help', '', '', ''],
                ['30609', '', '', '', '', '', '', 'case!', '', '', '']]
        md_df = make_df(rows)
        df_casework, df_casework_check = find_casework_rows(md_df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30609', '', '', '', '', '', '', 'case!', '', '', '', 'Casework'],
                    ['30600', '', '', '', '', '', '', 'FORWARDED TO ME^ADMIN', '', '', '', 'Casework'],
                    ['30601', '', '', '', '', '', '', 'Admin^InitialSSACase', '', '', '', 'Casework'],
                    ['30607', '', '', '', '', '', '', 'open case', '', '', '', 'Casework'],
                    ['30608', '', '', '', '', '', '', 'admin^open sixth district cases^help', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin',
                     'out_type', 'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30603', '', '', '', '', '', '', 'admin^case', '', '', '', 'Casework'],
                    ['30604', '', '', '', '', '', '', 'Case^IP', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for out_topic, df_casework_check")


if __name__ == '__main__':
    unittest.main()
