"""
Test for the function read_metadata(), which combines all metadata into a dataframe.
"""
import os
import unittest
from css_data_interchange_format import read_metadata


class MyTestCase(unittest.TestCase):
    def test_function(self):
        # Makes variable for the function and runs the function.
        paths_dict = {'out_1B': os.path.join('test_data', 'read', 'out_1B.dat'),
                      'out_2A': os.path.join('test_data', 'read', 'out_2A.dat')}
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        md_df.fillna('nan', inplace=True)
        result = [md_df.columns.tolist()] + md_df.values.tolist()
        expected = [['record_type_x', 'person_id', 'address_id_x', 'address_type', 'primary_flag',
                     'default_address_flag', 'title', 'organization_name', 'address_line_1', 'address_line_2',
                     'address_line_3', 'address_line_4', 'city', 'state_code', 'zip_code', 'carrier_route', 'county',
                     'country', 'district', 'precinct', 'no_mail_flag', 'deliverability', 'record_type_y',
                     'communication_id', 'workflow_id', 'workflow_person_id', 'communication_type', 'user_id',
                     'approved_by', 'status', 'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type',
                     'address_id_y', 'email_address', 'household_flag', 'household_id', 'group_name', 'salutation'],
                    ['1B', '1000001', '200001', 'HO', 'Y', 'Y', 'nan', 'nan', '100 St', 'nan', 'nan', 'nan', 'Kennesaw',
                     'GA', '30144-2248', 'R016', 'Cobb', 'USA', 'GA06', 'nan', 'nan', 'nan', '2A', '1100001', 'nan',
                     '11100011', 'imail', '8', 'nan', 'C', '19990301', '19990305', 'nan', '19990301', 'imail',
                     '200001', 'name@gmail.com', 'nan', 'nan', 'TAX1', 'Mr. and Mrs. Name'],
                    ['1B', '1000001', '200001', 'HO', 'Y', 'Y', 'nan', 'nan', '100 St', 'nan', 'nan', 'nan', 'Kennesaw',
                     'GA', '30144-2248', 'R016', 'Cobb', 'USA', 'GA06', 'nan', 'nan', 'nan', '2A', '1100002', 'nan',
                     '11100011', 'imail', '8', 'nan', 'C', '19990501', '19990507', 'nan', '19990501', 'imail',
                     '200001', 'name@gmail.com', 'nan', 'nan', 'HMO', 'Mr. and Mrs. Name'],
                    ['1B', '1000002', '200002', 'BU', 'Y', 'Y', 'Director', 'Business Name', 'P.O. Box 1A', '200 Main',
                     'nan', 'nan', 'Marietta', 'GA', '30062-5584', 'C085', 'Cobb', 'USA', 'GA06', 'nan', 'Y', 'nan',
                     'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                     'nan', 'nan', 'nan', 'nan', 'nan'],
                    ['1B', '1000003', '200003', 'HO', 'nan', 'nan', 'nan', 'nan', '300 Elm', 'Apt 3', 'nan', 'nan',
                     'Marietta', 'GA', '30062-1613', 'R026', 'Cobb', 'USA', 'GA06', 'nan', 'nan', 'D', '2A', '1100003',
                     'nan', '11100012', 'usmail', 'INTERN1', 'nan', 'C', '19990607', '19990617', 'nan', '19990607',
                     'usmail', '200003', 'nan', 'nan', 'nan', 'TAX1', 'nan'],
                    ['1B', '10000044', '200004', 'HO', 'Y', 'Y', 'nan', 'nan', '400 Rd', 'nan', 'nan', 'nan', 'Macon',
                     'GA', '31204-3904', 'C041', 'Bibb', 'USA', 'GA02', 'nan', 'nan', 'P',
                     'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                     'nan', 'nan', 'nan', 'nan', 'nan'],
                    ['nan', '1000005', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                     'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', '2A', '1100004', 'nan',
                     '11100011', 'imail', '2', 'nan', 'C', '20000315', '20000402', 'nan', '20000315', 'imail',
                     '200004', 'name@yahoo.com', 'Y', '1234567', 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for function read_metadata")


if __name__ == '__main__':
    unittest.main()