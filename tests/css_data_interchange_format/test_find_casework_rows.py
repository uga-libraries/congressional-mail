import pandas as pd
import unittest
from css_data_interchange_format import find_casework_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_doc_name(self):
        """Test for when the column communication_document_name indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', 'doc\\Buck Letter - Casework.doc', '', ''],
                           ['20250402', '', 'doc\\Casework - Initial Reply.doc', '', ''],
                           ['20250403', '', 'doc\\Close Favorably - Case work.doc', '', ''],
                           ['20250404', '', 'doc\\Initial Reply - Casework.doc', '', ''],
                           ['20250405', '', 'doc\\Interim - Casework.doc', '', ''],
                           ['20250406', '', 'doc\\Open Sixth District Casework.doc', '', ''],
                           ['20250407', '', 'doc\\Napster Case.doc', '', ''],
                           ['20250408', '', 'doc\\initialssacase.doc', '', ''],
                           ['20250409', '', 'doc\\Open Sixth District Cases.doc', '', ''],
                           ['20250410', '', 'doc\\Antitrust Case.doc', '', ''],
                           ['20250411', '', 'doc\\doc.txt', '', ''],
                           ['20250412', '', 'case', '', ''],
                           ['20250413', '', 'doc\\issue.txt', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250412', '', 'case', '', '', 'Casework'],
                    ['20250401', '', 'doc\\Buck Letter - Casework.doc', '', '', 'Casework'],
                    ['20250402', '', 'doc\\Casework - Initial Reply.doc', '', '', 'Casework'],
                    ['20250403', '', 'doc\\Close Favorably - Case work.doc', '', '', 'Casework'],
                    ['20250404', '', 'doc\\Initial Reply - Casework.doc', '', '', 'Casework'],
                    ['20250405', '', 'doc\\Interim - Casework.doc', '', '', 'Casework'],
                    ['20250406', '', 'doc\\Open Sixth District Casework.doc', '', '', 'Casework'],
                    ['20250408', '', 'doc\\initialssacase.doc', '', '', 'Casework'],
                    ['20250409', '', 'doc\\Open Sixth District Cases.doc', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250407', '', 'doc\\Napster Case.doc', '', '', 'Casework'],
                    ['20250410', '', 'doc\\Antitrust Case.doc', '', '', 'Casework'],
                    ['20250413', '', 'doc\\issue.txt', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for doc_name, df_casework_check")

    def test_file_name(self):
        """Test for when the column file_name indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', 'Buck Letter - Casework.doc', ''],
                           ['20250402', '', '', 'Casework - Initial Reply.doc', ''],
                           ['20250403', '', '', 'Close Favorably - Case work.doc', ''],
                           ['20250404', '', '', 'Initial Reply - Casework.doc', ''],
                           ['20250405', '', '', 'Interim - Casework.doc', ''],
                           ['20250406', '', '', 'Open Sixth District Casework.doc', ''],
                           ['20250407', '', '', 'Napster Case.doc', ''],
                           ['20250408', '', '', 'initialssacase.doc', ''],
                           ['20250409', '', '', 'Open Sixth District Cases.doc', ''],
                           ['20250410', '', '', 'Antitrust Case.doc', ''],
                           ['20250411', '', '', 'doc.txt', ''],
                           ['20250412', '', '', 'case', ''],
                           ['20250413', '', '', 'issue', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250412', '', '', 'case', '', 'Casework'],
                    ['20250401', '', '', 'Buck Letter - Casework.doc', '', 'Casework'],
                    ['20250402', '', '', 'Casework - Initial Reply.doc', '', 'Casework'],
                    ['20250403', '', '', 'Close Favorably - Case work.doc', '', 'Casework'],
                    ['20250404', '', '', 'Initial Reply - Casework.doc', '', 'Casework'],
                    ['20250405', '', '', 'Interim - Casework.doc', '', 'Casework'],
                    ['20250406', '', '', 'Open Sixth District Casework.doc', '', 'Casework'],
                    ['20250408', '', '', 'initialssacase.doc', '', 'Casework'],
                    ['20250409', '', '', 'Open Sixth District Cases.doc', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for file_name, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250407', '', '', 'Napster Case.doc', '', 'Casework'],
                    ['20250410', '', '', 'Antitrust Case.doc', '', 'Casework'],
                    ['20250413', '', '', 'issue', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for file_name, df_casework_check")

    def test_group_name(self):
        """Test for when the column group_name indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', 'casework12', '', '', ''],
                           ['20250402', 'CASE 1', '', '', ''],
                           ['20250403', 'legal case concern', '', '', ''],
                           ['20250404', 'Smith Case', '', '', ''],
                           ['20250405', 'case!', '', '', ''],
                           ['20250406', 'ISSUE', '', '', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250401', 'casework12', '', '', '', 'Casework'],
                    ['20250402', 'CASE 1', '', '', '', 'Casework'],
                    ['20250405', 'case!', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250403', 'legal case concern', '', '', '', 'Casework'],
                    ['20250404', 'Smith Case', '', '', '', 'Casework'],
                    ['20250406', 'ISSUE', '', '', '', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for group_name, df_casework_check")

    def test_none(self):
        """Test for when no patterns indicating casework are present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', '', ''],
                           ['20250402', '', 'doc\\doc.txt', '', ''],
                           ['20250403', '', 'doc\\doc.txt', 'doc.txt', ''],
                           ['20250404-case', '', '', 'doc.txt', '']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none, df_casework_check")

    def test_text(self):
        """Test for when the column text indicates casework is present"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['20250401', '', '', '', 'might be casework'],
                           ['20250402', '', '', '', 'CASE99'],
                           ['20250403', '', '', '', 'Could be Case Work.'],
                           ['20250404', '', '', '', ''],
                           ['20250405', '', '', '', 'check for case'],
                           ['20250406', '', '', '', 'initialssacase'],
                           ['20250407', '', '', '', 'Add to open sixth district cases'],
                           ['20250408', '', '', '', 'CASE'],
                           ['20250409', '', '', '', 'SSN Issue']],
                          columns=['date_in', 'group_name', 'communication_document_name', 'file_name', 'text'])
        df_casework, df_casework_check = find_casework_rows(df)

        # Tests the values in df_casework are correct.
        result = df_to_list(df_casework)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250408', '', '', '', 'CASE', 'Casework'],
                    ['20250401', '', '', '', 'might be casework', 'Casework'],
                    ['20250403', '', '', '', 'Could be Case Work.', 'Casework'],
                    ['20250406', '', '', '', 'initialssacase', 'Casework'],
                    ['20250407', '', '', '', 'Add to open sixth district cases', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for text, df_casework")

        # Tests the values in df_casework_check are correct.
        result = df_to_list(df_casework_check)
        expected = [['date_in', 'group_name', 'communication_document_name', 'file_name', 'text', 'Appraisal_Category'],
                    ['20250402', '', '', '', 'CASE99', 'Casework'],
                    ['20250405', '', '', '', 'check for case', 'Casework'],
                    ['20250409', '', '', '', 'SSN Issue', 'Casework']]
        self.assertEqual(expected, result, "Problem with test for text, df_casework_check")


if __name__ == '__main__':
    unittest.main()
