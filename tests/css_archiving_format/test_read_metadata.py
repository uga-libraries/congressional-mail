"""
To keep the inputs organized, the DAT file is named with the test condition rather than archiving_correspondence.dat
TODO find a character that causes the encoding error, so it can be tested.
"""
import os
import unittest
from css_archiving_format import read_metadata


def df_to_list(df):
    """Convert a dataframe to a list for easier comparison"""
    df.fillna('BLANK', inplace=True)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the DAT file has no errors, no blank rows, and no delimited doc columns"""
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'correct.dat'))

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin',
                     'in_document_name_split', 'out_document_name_split'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'BLANK', 'MD', 'BLANK', 'BLANK', '123 A St', 'BLANK',
                     'BLANK', 'BLANK', 'A city', 'AL', '12345', 'BLANK', 'a100', 'General', 'Email', '20240101',
                     'A1', 'BLANK', 'path\\A100.doc', 'BLANK', 'r100', 'General', 'Email', '20240111', 'T1',
                     'note', 'path\\formA.doc', 'replyA100', 'path\\A100.doc', 'path\\formA.doc'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7',
                     'BLANK', 'BLANK', 'B city', 'WY', '23456', 'BLANK', 'b200', 'Case', 'Email', '20240202',
                     'B1^B2', 'Note', 'path\\B200.doc', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2',
                     'BLANK', 'path\\formB.doc', 'replyB200', 'path\\B200.doc', 'path\\formB.doc']]
        self.assertEqual(expected, result, "Problem with test for correct")

    def test_correct_blanks(self):
        """Test for when the DAT file has blank rows to skip"""
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'correct_blank_rows.dat'))

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin',
                     'in_document_name_split', 'out_document_name_split'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'BLANK', 'MD', 'BLANK', 'BLANK', '123 A St', 'BLANK',
                     'BLANK', 'BLANK', 'A city', 'AL', '12345', 'BLANK', 'a100', 'General', 'Email', '20240101',
                     'A1', 'BLANK', 'path\\fileA100.doc', 'BLANK', 'r100', 'General', 'Email', '20240111', 'T1',
                     'BLANK', 'path\\formA.doc', 'replyA100', 'path\\fileA100.doc', 'path\\formA.doc'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7',
                     'BLANK', 'BLANK', 'B city', 'WY', '23456', 'BLANK', 'b200', 'Case', 'Email', '20240202',
                     'B1^B2', 'Note', 'path\\fileB200.doc', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2',
                     'BLANK', 'path\\formB.doc', 'replyB200', 'path\\fileB200.doc', 'path\\formB.doc']]
        self.assertEqual(expected, result, "Problem with test for correct - blanks")

    def test_correct_multiple_in(self):
        """Test for when the DAT file has delimiters within in_document_name"""
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'correct_multiple_in.dat'))

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin',
                     'in_document_name_split', 'out_document_name_split'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'BLANK', 'MD', 'BLANK', 'BLANK', '123 A St', 'BLANK', 'BLANK',
                     'BLANK', 'A city', 'AL', '12345', 'US', 'a100', 'General', 'Email', '20240101', 'A1', 'BLANK',
                     'objects\\fileA100.txt^objects\\fileA200.txt^objects\\fileA300.txt', 'BLANK', 'r100', 'General',
                     'Email', '20240111', 'T1', 'BLANK', 'forms\\formA.doc', 'replyA1', 'objects\\fileA100.txt',
                     'forms\\formA.doc'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'BLANK', 'MD', 'BLANK', 'BLANK', '123 A St', 'BLANK', 'BLANK',
                     'BLANK', 'A city', 'AL', '12345', 'US', 'a100', 'General', 'Email', '20240101', 'A1', 'BLANK',
                     'objects\\fileA100.txt^objects\\fileA200.txt^objects\\fileA300.txt', 'BLANK', 'r100', 'General',
                     'Email', '20240111', 'T1', 'BLANK', 'forms\\formA.doc', 'replyA1', 'objects\\fileA200.txt',
                     'forms\\formA.doc'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'BLANK', 'MD', 'BLANK', 'BLANK', '123 A St', 'BLANK', 'BLANK',
                     'BLANK', 'A city', 'AL', '12345', 'US', 'a100', 'General', 'Email', '20240101', 'A1', 'BLANK',
                     'objects\\fileA100.txt^objects\\fileA200.txt^objects\\fileA300.txt', 'BLANK', 'r100', 'General',
                     'Email', '20240111', 'T1', 'BLANK', 'forms\\formA.doc', 'replyA1', 'objects\\fileA300.txt',
                     'forms\\formA.doc'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7', 'BLANK',
                     'BLANK', 'B city', 'WY', '23456', 'US', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     'objects\\fileB100.txt', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2', 'note',
                     'forms\\formB.doc', 'replyB200',  'objects\\fileB100.txt', 'forms\\formB.doc'],
                    ['Ms.', 'CeCe', 'C.', 'Cleese', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 C St', 'Apt C', 'BLANK',
                     'BLANK', 'C city', 'CA', '78911', 'US', 'c300', 'General', 'Email', '20240303', 'C1', 'Note',
                     'objects\\FileC1.txt^objects\\FileC2.txt', 'BLANK', 'r300', 'General', 'Email', '20240313',
                     'T3', 'BLANK', 'forms\\formC.doc', 'replyC2', 'objects\\FileC1.txt', 'forms\\formC.doc'],
                    ['Ms.', 'CeCe', 'C.', 'Cleese', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 C St', 'Apt C', 'BLANK',
                     'BLANK', 'C city', 'CA', '78911', 'US', 'c300', 'General', 'Email', '20240303', 'C1', 'Note',
                     'objects\\FileC1.txt^objects\\FileC2.txt', 'BLANK', 'r300', 'General', 'Email', '20240313',
                     'T3', 'BLANK', 'forms\\formC.doc', 'replyC2', 'objects\\FileC2.txt', 'forms\\formC.doc']]
        self.assertEqual(expected, result, "Problem with test for correct_multiple_in")

    def test_correct_multiple_in_out(self):
        """Test for when the DAT file has delimiters within in_document_name and out_document_name"""
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'correct_multiple_in_out.dat'))

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin',
                     'in_document_name_split', 'out_document_name_split'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'BLANK', 'MD', 'BLANK', 'BLANK', '123 A St', 'BLANK', 'BLANK',
                     'BLANK', 'A city', 'AL', '12345', 'US', 'a100', 'General', 'Email', '20240101', 'A1', 'Note',
                     '\\objects\\A.doc', 'text', 'r100', 'General', 'Email', '20240111', 'T1', 'note',
                     '\\form\\A1.txt', 'replyA1', '\\objects\\A.doc', '\\form\\A1.txt'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7', 'BLANK',
                     'BLANK', 'B city', 'WY', '23456', 'US', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     '\\objects\\B.doc^\\objects\\BB.doc', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2', 'note',
                     '\\form\\B1.txt^\\form\\B2.txt', 'replyB200', '\\objects\\B.doc', '\\form\\B1.txt'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7', 'BLANK',
                     'BLANK', 'B city', 'WY', '23456', 'US', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     '\\objects\\B.doc^\\objects\\BB.doc', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2', 'note',
                     '\\form\\B1.txt^\\form\\B2.txt', 'replyB200', '\\objects\\B.doc', '\\form\\B2.txt'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7', 'BLANK',
                     'BLANK', 'B city', 'WY', '23456', 'US', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     '\\objects\\B.doc^\\objects\\BB.doc', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2', 'note',
                     '\\form\\B1.txt^\\form\\B2.txt', 'replyB200', '\\objects\\BB.doc', '\\form\\B1.txt'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7', 'BLANK',
                     'BLANK', 'B city', 'WY', '23456', 'US', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     '\\objects\\B.doc^\\objects\\BB.doc', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2', 'note',
                     '\\form\\B1.txt^\\form\\B2.txt', 'replyB200', '\\objects\\BB.doc', '\\form\\B2.txt'],
                    ['Ms.', 'CeCe', 'C.', 'Cleese', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 C St', 'Apt C', 'BLANK',
                     'BLANK', 'C city', 'CA', '78911', 'US', 'c300', 'General', 'Email', '20240303', 'C1', 'Note',
                     '\\objects\\C.doc^\\objects\\CC.doc^\\objects\\CCC.doc', 'text', 'r300', 'General', 'Email',
                     '20240313', 'T3', 'note', '\\form\\C1.txt^\\form\\C2.txt', 'replyC2', '\\objects\\C.doc',
                     '\\form\\C1.txt'],
                    ['Ms.', 'CeCe', 'C.', 'Cleese', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 C St', 'Apt C', 'BLANK',
                     'BLANK', 'C city', 'CA', '78911', 'US', 'c300', 'General', 'Email', '20240303', 'C1', 'Note',
                     '\\objects\\C.doc^\\objects\\CC.doc^\\objects\\CCC.doc', 'text', 'r300', 'General', 'Email',
                     '20240313', 'T3', 'note', '\\form\\C1.txt^\\form\\C2.txt', 'replyC2', '\\objects\\C.doc',
                     '\\form\\C2.txt'],
                    ['Ms.', 'CeCe', 'C.', 'Cleese', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 C St', 'Apt C', 'BLANK',
                     'BLANK', 'C city', 'CA', '78911', 'US', 'c300', 'General', 'Email', '20240303', 'C1', 'Note',
                     '\\objects\\C.doc^\\objects\\CC.doc^\\objects\\CCC.doc', 'text', 'r300', 'General', 'Email',
                     '20240313', 'T3', 'note', '\\form\\C1.txt^\\form\\C2.txt', 'replyC2', '\\objects\\CC.doc',
                     '\\form\\C1.txt'],
                    ['Ms.', 'CeCe', 'C.', 'Cleese', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 C St', 'Apt C', 'BLANK',
                     'BLANK', 'C city', 'CA', '78911', 'US', 'c300', 'General', 'Email', '20240303', 'C1', 'Note',
                     '\\objects\\C.doc^\\objects\\CC.doc^\\objects\\CCC.doc', 'text', 'r300', 'General', 'Email',
                     '20240313', 'T3', 'note', '\\form\\C1.txt^\\form\\C2.txt', 'replyC2', '\\objects\\CC.doc',
                     '\\form\\C2.txt'],
                    ['Ms.', 'CeCe', 'C.', 'Cleese', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 C St', 'Apt C', 'BLANK',
                     'BLANK', 'C city', 'CA', '78911', 'US', 'c300', 'General', 'Email', '20240303', 'C1', 'Note',
                     '\\objects\\C.doc^\\objects\\CC.doc^\\objects\\CCC.doc', 'text', 'r300', 'General', 'Email',
                     '20240313', 'T3', 'note', '\\form\\C1.txt^\\form\\C2.txt', 'replyC2', '\\objects\\CCC.doc',
                     '\\form\\C1.txt'],
                    ['Ms.', 'CeCe', 'C.', 'Cleese', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 C St', 'Apt C', 'BLANK',
                     'BLANK', 'C city', 'CA', '78911', 'US', 'c300', 'General', 'Email', '20240303', 'C1', 'Note',
                     '\\objects\\C.doc^\\objects\\CC.doc^\\objects\\CCC.doc', 'text', 'r300', 'General', 'Email',
                     '20240313', 'T3', 'note', '\\form\\C1.txt^\\form\\C2.txt', 'replyC2', '\\objects\\CCC.doc',
                     '\\form\\C2.txt']]
        self.assertEqual(expected, result, "Problem with test for correct_multiple_in_out")

    def test_correct_multiple_out(self):
        """Test for when the DAT file has delimiters within out_document_name"""
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'correct_multiple_out.dat'))

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin',
                     'in_document_name_split', 'out_document_name_split'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'BLANK', 'MD', 'BLANK', 'BLANK', '123 A St', 'BLANK', 'BLANK',
                     'BLANK', 'A city', 'AL', '12345', 'US', 'a100', 'General', 'Email', '20240101', 'A1', 'Note',
                     'path\\A.doc', 'text', 'r100', 'General', 'Email', '20240111', 'T1', 'note',
                     '\\form\\A1.txt^\\indiv\\A2.txt', 'replyA1', 'path\\A.doc', '\\form\\A1.txt'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'BLANK', 'MD', 'BLANK', 'BLANK', '123 A St', 'BLANK', 'BLANK',
                     'BLANK', 'A city', 'AL', '12345', 'US', 'a100', 'General', 'Email', '20240101', 'A1', 'Note',
                     'path\\A.doc', 'text', 'r100', 'General', 'Email', '20240111', 'T1', 'note',
                     '\\form\\A1.txt^\\indiv\\A2.txt', 'replyA1', 'path\\A.doc', '\\indiv\\A2.txt'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7', 'BLANK',
                     'BLANK', 'B city', 'WY', '23456', 'US', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     'path\\B.doc', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2', 'note',
                     '\\form\\B1.txt^\\form\\B2.txt^\\form\\B3.txt', 'replyB200', 'path\\B.doc', '\\form\\B1.txt'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7', 'BLANK',
                     'BLANK', 'B city', 'WY', '23456', 'US', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     'path\\B.doc', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2', 'note',
                     '\\form\\B1.txt^\\form\\B2.txt^\\form\\B3.txt', 'replyB200', 'path\\B.doc', '\\form\\B2.txt'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7', 'BLANK',
                     'BLANK', 'B city', 'WY', '23456', 'US', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     'path\\B.doc', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2', 'note',
                     '\\form\\B1.txt^\\form\\B2.txt^\\form\\B3.txt', 'replyB200', 'path\\B.doc', '\\form\\B3.txt'],
                    ['Ms.', 'CeCe', 'C.', 'Cleese', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 C St', 'Apt C', 'BLANK',
                     'BLANK', 'C city', 'CA', '78911', 'US', 'c300', 'General', 'Email', '20240303', 'C1', 'Note',
                     'path\\C.doc', 'text', 'r300', 'General', 'Email', '20240313', 'T3', 'note',
                     'e:\\\\eobj\\C1.eml', 'replyC2', 'path\\C.doc', 'e:\\\\eobj\\C1.eml']]
        self.assertEqual(expected, result, "Problem with test for correct_multiple_out")

    def test_parser_error(self):
        """Test for when the DAT file has content with tabs, resulting in a ParserError
        It should also print ParserWarning: Skipping line 4: expected 32 fields, saw 36"""
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'parser_error.dat'))

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin',
                     'in_document_name_split', 'out_document_name_split'],
                    ['Ms.', 'Anna', 'A.', 'Anderson', 'BLANK', 'MD', 'BLANK', 'BLANK', '123 A St', 'BLANK', 'BLANK',
                     'BLANK', 'A city', 'AL', '12345', 'BLANK', 'a100', 'General', 'Email', '20240101', 'A1', 'BLANK',
                     'fileA100.txt', 'BLANK', 'r100', 'General', 'Email', '20240111', 'T1', 'BLANK', 'formA.txt',
                     'replyA100', 'fileA100.txt', 'formA.txt'],
                    ['Mr.', 'Bill', 'B.', 'Blue', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '456 B St', 'Apt 7', 'BLANK',
                     'BLANK', 'B city', 'WY', '23456', 'BLANK', 'b200', 'Case', 'Email', '20240202', 'B1^B2', 'Note',
                     'fileB200.txt', 'BLANK', 'r200', 'Case', 'Email', '20240212', 'T2', 'BLANK', 'formB.txt',
                     'replyB200', 'fileB200.txt', 'formB.txt'],
                    ['Ms.', 'Debbie', 'D.', 'Dunning', 'BLANK', 'BLANK', 'BLANK', 'BLANK', '789 D St', 'BLANK',
                     'BLANK', 'BLANK', 'D city', 'DE', '45678', 'BLANK', 'd400', 'General', 'Email', '20240404', 'D1',
                     'BLANK', 'fileD400.txt', 'BLANK', 'r400', 'General', 'Email', '20240414', 'T4', 'note',
                     'formD.txt', 'replyD400', 'fileD400.txt', 'formD.txt']]
        self.assertEqual(expected, result, "Problem with test for ParserError")


if __name__ == '__main__':
    unittest.main()
