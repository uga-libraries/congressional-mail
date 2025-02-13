"""
Test for the function remove_casework_rows(), which metadata rows for letters that pertain to casework.
"""
import os
import pandas as pd
import unittest
from css_archiving_format import remove_casework_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_function(self):
        """Test for the function, which will remove some rows from mdf_df"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['Ms.', 'Anna', 'A.', 'Anderson', '', '', '', '', '123 A St', '', '', '',
                               'A city', 'AL', '12345', '', 'a100', 'Casework', 'Email', '20210101', 'Casework', '',
                               r'..\documents\BlobExport\objects\111111.txt', '', '100', 'Casework', 'Email',
                               '20210111', 'formA', '', r'..\documents\BlobExport\formletters\test.txt', ''],
                              ['Mr.', 'Bill', 'B.', 'Blue', '', '', '', '', '234 B St', '', '', '', 'B city', 'WY',
                               '23456', '', 'b200', 'Issue', 'Email', '20230202', 'Issue', '',
                               r'..\documents\BlobExport\objects\222222.txt', '', '200', 'Issue', 'Email', '20230212',
                               'formB', '', '', ''],
                              ['Mr.', 'Clive', 'C.', 'Cooper', '', '', '', '', '345 C St', '', '', '', 'C city', 'CO',
                               '34567', '', 'c300', 'Casework', 'Letter', '20240303', 'Casework', '', '', '', '300',
                               'Casework', 'Email', '20240313', 'formC', '',
                               r'..\documents\BlobExport\formletters\test.txt', ''],
                              ['Ms.', 'Diane', 'D.', 'Dudly', '', '', '', '', '456 D St', '', '', '', 'D city', 'DE',
                               '45678', '', 'd100', 'Issue', 'Email', '20210101', 'Issue', '', '', '', '400', 'Issue',
                               'Email', '20210111', 'formD', '', r'..\documents\BlobExport\indivletters\400.txt', ''],
                              ['Ms.', 'Emma', 'E.', 'Evans', '', '', '', '', '567 E St', '', '', '', 'E city', 'ME',
                               '56789', '', 'e100', 'Casework', 'Email', '20210101', 'Casework', '',
                               r'..\documents\BlobExport\objects\333333.txt', '', '500', 'Casework', 'Email',
                               '20210111', 'formE', '', r'..\documents\BlobExport\indivletters\500.txt', '']],
                             columns=['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org',
                                      'addr1', 'addr2', 'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id',
                                      'in_type', 'in_method', 'in_date', 'in_topic', 'in_text', 'in_document_name',
                                      'in_fillin', 'out_id', 'out_type', 'out_method', 'out_date', 'out_topic',
                                      'out_text', 'out_document_name', 'out_fillin'])
        output_directory = os.path.join('test_data', 'remove_casework_metadata')
        md_df = remove_casework_rows(md_df, output_directory)

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['prefix', 'first', 'middle', 'last', 'suffix', 'appellation', 'title', 'org', 'addr1', 'addr2',
                     'addr3', 'addr4', 'city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date',
                     'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_id', 'out_type', 'out_method',
                     'out_date', 'out_topic', 'out_text', 'out_document_name', 'out_fillin'],
                    ['Mr.', 'Bill', 'B.', 'Blue', '', '', '', '', '234 B St', '', '', '', 'B city', 'WY', '23456', '',
                     'b200', 'Issue', 'Email', '20230202', 'Issue', '', r'..\documents\BlobExport\objects\222222.txt',
                     '', '200', 'Issue', 'Email', '20230212', 'formB', '', '', ''],
                    ['Ms.', 'Diane', 'D.', 'Dudly', '', '', '', '', '456 D St', '', '', '', 'D city', 'DE',
                     '45678', '', 'd100', 'Issue', 'Email', '20210101', 'Issue', '', '', '', '400', 'Issue',
                     'Email', '20210111', 'formD', '', r'..\documents\BlobExport\indivletters\400.txt', '']]
        self.assertEqual(result, expected, "Problem with test for function")


if __name__ == '__main__':
    unittest.main()
