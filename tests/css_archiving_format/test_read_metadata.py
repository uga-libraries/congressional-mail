"""
Tests for the function read_metadata(), which reads the DAT file into a pandas dataframe.
To keep the inputs organized, the DAT file is named with the test condition rather than archiving_correspondence.dat
TODO find a character that causes the encoding error, so it can be tested.
"""
import os
import unittest
from css_archiving_format import read_metadata


def df_to_list(df):
    """Convert a dataframe to a list for easier comparison"""
    df.fillna('blank', inplace=True)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


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
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'blank', 'MD', 'blank', 'blank', '123 A St', 'blank', 'blank',
                     'blank', 'A city', 'AL', '12345', 'blank', 'a100', 'General', 'Email', '20240101', 'A1', 'blank',
                     'fileA100', 'blank', 'r100', 'General', 'Email', '20240111', 'formA', 'blank', 'replyA100',
                     'blank'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'blank', 'blank', 'blank', 'blank', '456 B St', 'Apt 7', 'blank',
                     'blank', 'B city', 'WY', '23456', 'blank', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     'fileB200', 'blank', 'r200', 'Case', 'Email', '20240212', 'formB', 'blank', 'replyB200', 'blank']]
        self.assertEqual(result, expected, "Problem with test for correct")

    def test_correct_blanks(self):
        """Test for when the DAT file can be read in its entirety but has blank rows to skip"""
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'correct.dat'))

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'blank', 'MD', 'blank', 'blank', '123 A St', 'blank', 'blank',
                     'blank', 'A city', 'AL', '12345', 'blank', 'a100', 'General', 'Email', '20240101', 'A1', 'blank',
                     'fileA100', 'blank', 'r100', 'General', 'Email', '20240111', 'formA', 'blank', 'replyA100',
                     'blank'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'blank', 'blank', 'blank', 'blank', '456 B St', 'Apt 7', 'blank',
                     'blank', 'B city', 'WY', '23456', 'blank', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     'fileB200', 'blank', 'r200', 'Case', 'Email', '20240212', 'formB', 'blank', 'replyB200', 'blank']]
        self.assertEqual(result, expected, "Problem with test for correct - blanks")

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
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'blank', 'MD', 'blank', 'blank', '123 A St', 'blank', 'blank',
                     'blank', 'A city', 'AL', '12345', 'blank', 'a100', 'General', 'Email', '20240101', 'A1', 'blank',
                     'fileA100', 'blank', 'r100', 'General', 'Email', '20240111', 'formA', 'blank', 'replyA100',
                     'blank'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'blank', 'blank', 'blank', 'blank', '456 B St', 'Apt 7', 'blank',
                     'blank', 'B city', 'WY', '23456', 'blank', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     'fileB200', 'blank', 'r200', 'Case', 'Email', '20240212', 'formB', 'blank', 'replyB200', 'blank'],
                    ['Ms.', 'Debbie', 'D.', 'Dunning', 'blank', 'blank', 'blank', 'blank', '789 D St', 'blank',
                     'blank', 'blank', 'D city', 'DE', '45678', 'blank', 'd400', 'General', 'Email', '20240404', 'D1',
                     'blank', 'fileD400', 'blank', 'r400', 'General', 'Email', '20240414', 'formD', 'blank',
                     'replyD400', 'blank']]
        self.assertEqual(result, expected, "Problem with test for ParserError")


if __name__ == '__main__':
    unittest.main()
