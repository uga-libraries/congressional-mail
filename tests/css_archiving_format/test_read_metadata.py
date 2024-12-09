"""
Tests for the function read_metadata(), which reads the DAT file into a pandas dataframe.
To keep the inputs organized, the DAT file is named with the test condition rather than archiving_correspondence.dat
"""
import os
import unittest
from css_archiving_format import read_metadata
from test_remove_casework import df_to_list


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the DAT file can be read in its entirety"""
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'correct.dat'))

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'nan', 'MD', 'nan', 'nan', '123 A St', 'nan', 'nan', 'nan',
                     'A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20240101', 'A1', 'nan', 'fileA100',
                     'nan', 'r100', 'General', 'Email', '20240111', 'formA', 'nan', 'replyA100', 'nan'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'nan', 'nan', 'nan', 'nan', '456 B St', 'Apt 7', 'nan', 'nan',
                     'B city', 'WY', '23456', 'nan', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note', 'fileB200',
                     'nan', 'r200', 'Case', 'Email', '20240212', 'formB', 'nan', 'replyB200', 'nan']]
        self.assertEqual(result, expected, "Problem with test for correct")

    def test_parser_error(self):
        """Test for when the DAT file has content with tabs, resulting in a ParserError
        It should also print ParserWarning: Skipping line 4: expected 32 fields, saw 34"""
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'parser_error.dat'))

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'nan', 'MD', 'nan', 'nan', '123 A St', 'nan', 'nan', 'nan',
                     'A city', 'AL', '12345', 'nan', 'a100', 'General', 'Email', '20240101', 'A1', 'nan', 'fileA100',
                     'nan', 'r100', 'General', 'Email', '20240111', 'formA', 'nan', 'replyA100', 'nan'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'nan', 'nan', 'nan', 'nan', '456 B St', 'Apt 7', 'nan', 'nan',
                     'B city', 'WY', '23456', 'nan', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note', 'fileB200',
                     'nan', 'r200', 'Case', 'Email', '20240212', 'formB', 'nan', 'replyB200', 'nan'],
                    ['Ms.', 'Debbie', 'D.', 'Dunning', 'nan', 'nan', 'nan', 'nan', '789 D St', 'nan', 'nan', 'nan',
                     'D city', 'DE', '45678', 'nan', 'd400', 'General', 'Email', '20240404', 'D1', 'nan', 'fileD400',
                     'nan', 'r400', 'General', 'Email', '20240414', 'formD', 'nan', 'replyD400', 'nan']]
        self.assertEqual(result, expected, "Problem with test for ParserError")


if __name__ == '__main__':
    unittest.main()
