import pandas as pd
import unittest
from cms_data_interchange_format import find_casework_rows
from test_read_metadata_file import df_to_list


class MyTestCase(unittest.TestCase):

    def test_code_desc(self):
        """Test for when the column code_scription indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', '', 'New case file'],
                           ['30601', '', '', 'case has been closed'],
                           ['30602', '', '', 'Case Open'],
                           ['30603', '', '', 'CASEWORK'],
                           ['30604', '', '', ''],
                           ['30605', '', '', 'Maybe not case work'],
                           ['30606', '', '', 'Forwarded to me for a response'],
                           ['30607', '', '', 'Add to open case'],
                           ['30608', '', '', 'Potential case'],
                           ['30609', '', '', 'case_01'],
                           ['30610', '', '', 'case'],
                           ['30611', '', '', 'issue']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30610', '', '', 'case', 'Casework'],
                    ['30600', '', '', 'New case file', 'Casework'],
                    ['30601', '', '', 'case has been closed', 'Casework'],
                    ['30602', '', '', 'Case Open', 'Casework'],
                    ['30603', '', '', 'CASEWORK', 'Casework'],
                    ['30605', '', '', 'Maybe not case work', 'Casework'],
                    ['30606', '', '', 'Forwarded to me for a response', 'Casework'],
                    ['30607', '', '', 'Add to open case', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30608', '', '', 'Potential case', 'Casework'],
                    ['30609', '', '', 'case_01', 'Casework'],
                    ['30611', '', '', 'issue', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for code_desc, df_casework_check")

    def test_corr_doc_name(self):
        """Test for when the column correspondence_document_name indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', 'path\\case file.txt', '', ''],
                           ['30601', 'path\\case has.txt', '', ''],
                           ['30602', 'path\\Case Open.txt', '', ''],
                           ['30603', 'path\\CASEWORK.txt', '', ''],
                           ['30604', '', '', ''],
                           ['30605', 'path\\case work.txt', '', ''],
                           ['30606', 'path\\Forwarded to me.txt', '', ''],
                           ['30607', 'path\\open case.txt', '', ''],
                           ['30608', 'path\\potential case.txt', '', ''],
                           ['30609', 'path\\case.txt', '', ''],
                           ['30610', 'CASE', '', ''],
                           ['30611', 'path\\Water_Issue.txt', '', '']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30610', 'CASE', '', '', 'Casework'],
                    ['30600', 'path\\case file.txt', '', '', 'Casework'],
                    ['30601', 'path\\case has.txt', '', '', 'Casework'],
                    ['30602', 'path\\Case Open.txt', '', '', 'Casework'],
                    ['30603', 'path\\CASEWORK.txt', '', '', 'Casework'],
                    ['30605', 'path\\case work.txt', '', '', 'Casework'],
                    ['30606', 'path\\Forwarded to me.txt', '', '', 'Casework'],
                    ['30607', 'path\\open case.txt', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30608', 'path\\potential case.txt', '', '', 'Casework'],
                    ['30609', 'path\\case.txt', '', '', 'Casework'],
                    ['30611', 'path\\Water_Issue.txt', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for corr_doc, df_casework_check")

    def test_corr_text(self):
        """Test for when the column correspondence_text indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', '', 'New case file', ''],
                           ['30601', '', 'case has been closed', ''],
                           ['30602', '', 'Case Open', ''],
                           ['30603', '', 'CASEWORK', ''],
                           ['30604', '', 'Forwarded to me for a response', ''],
                           ['30605', '', 'Add to open case', ''],
                           ['30606', '', 'Potential case', ''],
                           ['30607', '', 'Maybe not case work', ''],
                           ['30608', '', 'Case!', ''],
                           ['30609', '', 'ISSUE ABC', '']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30608', '', 'Case!', '', 'Casework'],
                    ['30600', '', 'New case file', '', 'Casework'],
                    ['30601', '', 'case has been closed', '', 'Casework'],
                    ['30602', '', 'Case Open', '', 'Casework'],
                    ['30603', '', 'CASEWORK', '', 'Casework'],
                    ['30604', '', 'Forwarded to me for a response', '', 'Casework'],
                    ['30605', '', 'Add to open case', '', 'Casework'],
                    ['30607', '', 'Maybe not case work', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category'],
                    ['30606', '', 'Potential case', '', 'Casework'],
                    ['30609', '', 'ISSUE ABC', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for corr_text, df_casework_check")

    def test_none(self):
        """Test for when no rows have casework"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30600', 'file_1.doc', 'one', 'a'],
                           ['30601', 'file_2.doc', 'two', 'b'],
                           ['30602-case', 'file_3.doc', 'three', 'c']],
                          columns=['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['zip_code', 'correspondence_document_name', 'correspondence_text', 'code_description',
                     'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_casework_check")


if __name__ == '__main__':
    unittest.main()
