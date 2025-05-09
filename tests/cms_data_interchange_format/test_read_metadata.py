"""
Test for the function read_metadata(), which combines all metadata into a dataframe.
"""
import os
import unittest
from cms_data_interchange_format import read_metadata
from test_read_metadata_file import df_to_list


class MyTestCase(unittest.TestCase):
    
    def test_function(self):
        # Makes variable for the function and runs the function.
        paths_dict = {'1B': os.path.join('test_data', 'read', '1B.out'),
                      '2A': os.path.join('test_data', 'read', '2A.out'),
                      '2B': os.path.join('test_data', 'read', '2B.out'),
                      '2C': os.path.join('test_data', 'read', '2C.out'),
                      '2D': os.path.join('test_data', 'read', '2D.out'),
                      '8A': os.path.join('test_data', 'read', '8A.out')}
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        result = df_to_list(md_df)
        expected = [['city', 'state', 'zip_code', 'country', 'correspondence_type', 'staff', 'date_in', 'date_out',
                     'tickler_date', 'update_date', 'response_type', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['City One', 'GA', '30001', 'USA', 'LETTER', 'Staffer_1', '20220110', '20220110', 'BLANK',
                     '20220110', 'LETTER', '15001', 'CON', '1', 'main', 'taxes_con.docx', 'BLANK', 'text1',
                     'COR', '15001', 'Taxes', 'Y'],
                    ['City Two', 'GA', '30002', 'USA', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK',
                     '20220220', 'EMAIL', '15002', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK', 'text2',
                     'COR', '15002', 'Minimum Wage', 'BLANK'],
                    ['City Three', 'GA', '30003', 'USA', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK',
                     '20220330', 'EMAIL', '15003', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK', 'text3',
                     'COR', '15003', 'Rights > Workers', 'Y']]
        self.assertEqual(result, expected, "Problem with test for function read_metadata")


if __name__ == '__main__':
    unittest.main()
