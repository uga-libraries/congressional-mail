"""
Test for the function read_metadata(), which combines all metadata into a dataframe.
"""
import os
import unittest
from css_data_interchange_format import read_metadata


class MyTestCase(unittest.TestCase):
    def test_function(self):
        # Makes variable for the function and runs the function.
        paths_dict = {'1B': os.path.join('test_data', 'read', 'out_1B.dat'),
                      '2A': os.path.join('test_data', 'read', 'out_2A.dat'),
                      '2C': os.path.join('test_data', 'read', 'out_2C.dat')}
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        md_df.fillna('nan', inplace=True)
        result = [md_df.columns.tolist()] + md_df.values.tolist()
        expected = [['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                     'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name'],
                    ['Kennesaw', 'GA', '30144-2248', 'USA', 'imail', 'nan', 'C', '19990301', '19990305', 'nan',
                     '19990301', 'imail', 'TAX1', 'OUTGOING', r'..\documents\formletters\taxes.doc',
                     'nan', 'nan', 'taxes.doc'],
                    ['Kennesaw', 'GA', '30144-2248', 'USA', 'imail', 'nan', 'C', '19990501', '19990507', 'nan',
                     '19990501', 'imail', 'HMO', 'OUTGOING', r'..\documents\formletters\insurance.doc',
                     'nan', 'nan', 'insurance.doc'],
                    ['Marietta', 'GA', '30062-1613', 'USA', 'usmail', 'nan', 'C', '19990607', '19990617', 'nan',
                     '19990607', 'usmail', 'TAX1', 'OUTGOING', r'..\documents\formletters\taxes.doc',
                     'nan', 'nan', 'taxes.doc'],
                    ['nan', 'nan', 'nan', 'nan', 'imail', 'nan', 'C', '20000315', '20000402', 'nan', '20000315',
                     'imail', 'nan', 'OUTGOING', r'..\documents\indivletters\12345.doc', 'nan', 'nan', '12345.doc'],
                    ['Marietta', 'GA', '30062-5584', 'USA', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                     'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan'],
                    ['Macon', 'GA', '31204-3904', 'USA', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                     'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for function read_metadata")


if __name__ == '__main__':
    unittest.main()
