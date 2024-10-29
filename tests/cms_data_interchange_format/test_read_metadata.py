"""
Test for the function read_metadata(), which combines all metadata into a dataframe.
"""
import os
import unittest
from cms_data_interchange_format import read_metadata


class MyTestCase(unittest.TestCase):
    def test_function(self):
        # Makes variable for the function and runs the function.
        paths_dict = {'1B': os.path.join('test_data', 'read', '1B.out'),
                      '2A': os.path.join('test_data', 'read', '2A.out'),
                      '2B': os.path.join('test_data', 'read', '2B.out'),
                      '2C': os.path.join('test_data', 'read', '2C.out')}
        md_df = read_metadata(paths_dict)

        # # Tests the value of md_df
        # md_df.fillna('nan', inplace=True)
        # result = [md_df.columns.tolist()] + md_df.values.tolist()
        # expected = [['constituent_id', 'correspondence_id', 'correspondence_type', 'staff', 'date_in', 'date_out',
        #             'tickler_date', 'update_date', 'response_type'],
        #             ['1', '1001', 'LETTER', 'Staffer_1', '20220110', '20220110', 'nan', '20220110', 'LETTER'],
        #             ['2', '2002', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'nan', '20220220', 'EMAIL'],
        #             ['3', '3003', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'nan', '20220330', 'EMAIL']]
        # self.assertEqual(result, expected, "Problem with test for function read_metadata")

        # Tests the value of md_df
        md_df.fillna('nan', inplace=True)
        result = [md_df.columns.tolist()] + md_df.values.tolist()
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20220110', '20220110', 'nan',
                     '20220110', 'LETTER', 'TAXES', 'CON', '1', 'main', 'taxes_con.docx', 'nan'],
                    ['City Two', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'nan',
                     '20220220', 'EMAIL', 'MINWAGE', 'PRO', '1', 'main', 'min_wage_pro.docx', 'nan'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'nan',
                     '20220330', 'EMAIL', 'RIGHTS', 'PRO', '1', 'main', 'rights_pro.docx', 'nan']]
        self.assertEqual(result, expected, "Problem with test for function read_metadata")


if __name__ == '__main__':
    unittest.main()
