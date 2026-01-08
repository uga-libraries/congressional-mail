"""
Test for the function read_metadata_file(), which reads the metadata from one file into a dataframe.
"""
import os
import unittest
from cms_data_interchange_format import read_metadata_file


def df_to_list(df):
    """Convert a dataframe to a list for easier comparison"""
    df.fillna('BLANK', inplace=True)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def test_1b(self):
        """Test for the metadata file 1B.out"""
        df_1b = read_metadata_file('1B', os.path.join('test_data', 'read', 'match', '1B.out'))

        result = df_to_list(df_1b)
        expected = [['record_type', 'constituent_id', 'address_id', 'address_type', 'primary_flag',
                     'default_address_flag', 'title', 'organization_name', 'address_line_1', 'address_line_2',
                     'address_line_3', 'address_line_4', 'city', 'state', 'zip_code', 'carrier_route',
                     'county', 'country', 'district', 'precinct', 'no_mail_flag', 'agency_code'],
                    ['1B', '1', '11', 'HO', 'Y', 'Y', 'BLANK', 'BLANK', '10 Oak St', 'Apt 2', 'BLANK', 'BLANK',
                     'City One', 'GA', '30001', 'C1', 'Clarke', 'USA', 'D1', 'P1', 'BLANK', 'BLANK'],
                    ['1B', '2', '22', 'BU', 'BLANK', 'Y', 'CEO', 'Org', '20 Pine Rd', 'BLANK', 'BLANK', 'BLANK',
                     'City Two', 'GA', '30002', 'C2', 'Clarke', 'USA', 'D2', 'P2', 'Y', 'BLANK'],
                    ['1B', '3', '33', 'HO', 'Y', 'Y', 'BLANK', 'BLANK', '30 Elm Ave', 'BLANK', 'BLANK', 'BLANK',
                     'City Three', 'GA', '30003', 'C3', 'Clarke', 'USA', 'D3', 'P3', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for 1B")

    def test_2a(self):
        """Test for the metadata file 2A.out"""
        df_2a = read_metadata_file('2A', os.path.join('test_data', 'read', 'match', '2A.out'))

        result = df_to_list(df_2a)
        expected = [['record_type', 'constituent_id', 'correspondence_id', 'correspondence_type', 'staff',
                     'date_in', 'date_out', 'tickler_date', 'update_date', 'response_type', 'address_id',
                     'household_flag', 'household_id', 'extra1', 'extra2'],
                    ['2A', '1', '1001', 'LETTER', 'Staffer_1', '20220110', '20220110', 'BLANK', '20220110',
                     'LETTER', '11', 'Y', '111', 'BLANK', 'BLANK'],
                    ['2A', '2', '2002', 'EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK', '20220220',
                     'EMAIL', '22', 'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['2A', '3', '3003', 'EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK', '20220330',
                     'EMAIL', '33', 'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for 2A")

    def test_2b(self):
        """Test for the metadata file 2B.out"""
        df_2b = read_metadata_file('2B', os.path.join('test_data', 'read', 'match', '2B.out'))

        result = df_to_list(df_2b)
        expected = [['record_type', 'constituent_id', 'correspondence_id', 'correspondence_code', 'position'],
                    ['2B', '1', '1001', '15001', 'CON'],
                    ['2B', '2', '2002', '15002', 'PRO'],
                    ['2B', '3', '3003', '15003', 'NEU']]
        self.assertEqual(expected, result, "Problem with test for 2B")

    def test_2c(self):
        """Test for the metadata file 2C.out"""
        df_2c = read_metadata_file('2C', os.path.join('test_data', 'read', 'match', '2C.out'))

        result = df_to_list(df_2c)
        expected = [['record_type', 'constituent_id', 'correspondence_id', '2C_sequence_number',
                     'document_type', 'correspondence_document_name', 'file_location'],
                    ['2C', '1', '1001', '1', 'main', 'taxes_con.docx', 'BLANK'],
                    ['2C', '2', '2002', '1', 'main', 'min_wage_pro.docx', 'BLANK'],
                    ['2C', '3', '3003', '1', 'main', 'rights_pro.docx', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for 2C")

    def test_2d(self):
        """Test for the metadata file 2D.out"""
        df_2d = read_metadata_file('2D', os.path.join('test_data', 'read', 'match', '2D.out'))

        result = df_to_list(df_2d)
        expected = [['record_type', 'constituent_id', 'correspondence_id', '2D_sequence_number', 'text_type',
                     'correspondence_text'],
                    ['2D', '1', '1001', '1', 'CM', 'text1'],
                    ['2D', '2', '2002', '1', 'CM', 'text2'],
                    ['2D', '2', '3003', '1', 'CM', 'text3']]
        self.assertEqual(expected, result, "Problem with test for 2D")

    def test_8a(self):
        """Test for the metadata file 8A.out"""
        df_8a = read_metadata_file('8A', os.path.join('test_data', 'read', 'match', '8A.out'))

        result = df_to_list(df_8a)
        expected = [['record_type', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['8A', 'COR', '15001', 'Taxes', 'Y'],
                    ['8A', 'COR', '15002', 'Minimum Wage', 'BLANK'],
                    ['8A', 'COR', '15003', 'Rights > Workers', 'Y']]
        self.assertEqual(expected, result, "Problem with test for 8A")


if __name__ == '__main__':
    unittest.main()
