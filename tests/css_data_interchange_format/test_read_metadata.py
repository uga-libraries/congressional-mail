import os
import unittest
from css_data_interchange_format import read_metadata


def df_to_list(df):
    """Fill blanks in a df and convert to a list for easier comparison"""
    df.fillna('BLANK', inplace=True)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def test_match(self):
        """Test for when both IDs for all rows match 2A once"""
        # Makes variable for the function and runs the function.
        paths_dict = {'1B': os.path.join('test_data', 'read', 'match', '1B.dat'),
                      '2A': os.path.join('test_data', 'read', 'match', '2A.dat'),
                      '2C': os.path.join('test_data', 'read', 'match', '2C.dat'),
                      '2D': os.path.join('test_data', 'read', 'match', '2D.dat')}
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        result = df_to_list(md_df)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'text'],
                    ['imail', 'BLANK', 'C', '19990301', '19990305', 'BLANK', '19990301', 'imail', 'TAX1',
                     'Kennesaw', 'GA', '30144-2248', 'USA', 'OUTGOING', r'..\documents\formletters\taxes.doc',
                     'BLANK', 'BLANK', 'taxes.doc', 'Support for 1'],
                    ['imail', 'BLANK', 'C', '19990501', '19990507', 'BLANK', '19990501', 'imail', 'HMO',
                     'Marietta', 'GA', '30062-5584', 'USA', 'OUTGOING', r'..\documents\formletters\insurance.doc',
                     'BLANK', 'BLANK', 'insurance.doc', 'Against 2'],
                    ['usmail', 'BLANK', 'C', '19990607', '19990617', 'BLANK', '19990607', 'usmail', 'TAX1',
                     'Marietta', 'GA', '30062-1613', 'USA', 'OUTGOING', r'..\documents\formletters\taxes.doc',
                     'BLANK', 'BLANK', 'taxes.doc', 'Support for 3'],
                    ['imail', 'BLANK', 'C', '20000315', '20000402', 'BLANK', '20000315', 'imail', 'BLANK',
                     'Macon', 'GA', '31204-3904', 'USA', 'OUTGOING', r'..\documents\indivletters\12345.doc',
                     'BLANK', 'BLANK', '12345.doc', 'Neutral re 4']]
        self.assertEqual(expected, result, "Problem with test for match")

    def test_match_multiple(self):
        """Test for when at least one row for both IDs matches 2A more than once"""
        # Makes variable for the function and runs the function.
        paths_dict = {'1B': os.path.join('test_data', 'read', 'match_multiple', '1B.dat'),
                      '2A': os.path.join('test_data', 'read', 'match_multiple', '2A.dat'),
                      '2C': os.path.join('test_data', 'read', 'match_multiple', '2C.dat'),
                      '2D': os.path.join('test_data', 'read', 'match_multiple', '2D.dat')}
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        result = df_to_list(md_df)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'text'],
                    ['imail', 'BLANK', 'C', '19990301', '19990305', 'BLANK', '19990301', 'imail', 'TAX1',
                     'Kennesaw', 'GA', '30144-2248', 'USA', 'OUTGOING', r'..\documents\formletters\taxes.doc',
                     'BLANK', 'BLANK', 'taxes.doc', 'Support for 1'],
                    ['imail', 'BLANK', 'C', '19990501', '19990507', 'BLANK', '19990501', 'imail', 'HMO',
                     'Kennesaw', 'GA', '30144-2248', 'USA', 'OUTGOING', r'..\documents\formletters\taxes.doc',
                     'BLANK', 'BLANK', 'taxes.doc', 'Support for 1'],
                    ['usmail', 'BLANK', 'C', '19990607', '19990617', 'BLANK', '19990607', 'usmail', 'TAX1',
                     'Marietta', 'GA', '30062-5584', 'USA', 'OUTGOING', r'..\documents\formletters\taxes.doc',
                     'BLANK', 'BLANK', 'taxes.doc', 'Support for 3'],
                    ['usmail', 'BLANK', 'C', '19990607', '19990617', 'BLANK', '19990607', 'usmail', 'TAX1',
                     'Marietta', 'GA', '30062-1613', 'USA', 'OUTGOING', r'..\documents\formletters\taxes.doc',
                     'BLANK', 'BLANK', 'taxes.doc', 'Support for 3'],
                    ['imail', 'BLANK', 'C', '20000315', '20000402', 'BLANK', '20000315', 'imail', 'BLANK',
                     'Macon', 'GA', '31204-3904', 'USA', 'OUTGOING', r'..\documents\indivletters\12345.doc',
                     'BLANK', 'BLANK', '12345.doc', 'Neutral re 4'],
                    ['imail', 'BLANK', 'C', '20000315', '20000402', 'BLANK', '20000315', 'imail', 'BLANK',
                     'Macon', 'GA', '31204-3904', 'USA', 'OUTGOING', r'..\documents\indivletters\12345.doc',
                     'BLANK', 'BLANK', '12345.doc', 'Against 4'],
                    ['imail', 'BLANK', 'C', '20000315', '20000402', 'BLANK', '20000315', 'imail', 'BLANK',
                     'Macon', 'GA', '31204-3904', 'USA', 'OUTGOING', r'..\documents\formletters\gifts.doc',
                     'BLANK', 'BLANK', 'gifts.doc', 'Neutral re 4'],
                    ['imail', 'BLANK', 'C', '20000315', '20000402', 'BLANK', '20000315', 'imail', 'BLANK',
                     'Macon', 'GA', '31204-3904', 'USA', 'OUTGOING', r'..\documents\formletters\gifts.doc',
                     'BLANK', 'BLANK', 'gifts.doc', 'Against 4']]
        self.assertEqual(expected, result, "Problem with test for match_multiple")

    def test_no_match_communication_id(self):
        """Test for when the communication_id in 2C and/or 2D does not match 2A"""
        # Makes variable for the function and runs the function.
        paths_dict = {'1B': os.path.join('test_data', 'read', 'no_match_communication_id', '1B.dat'),
                      '2A': os.path.join('test_data', 'read', 'no_match_communication_id', '2A.dat'),
                      '2C': os.path.join('test_data', 'read', 'no_match_communication_id', '2C.dat'),
                      '2D': os.path.join('test_data', 'read', 'no_match_communication_id', '2D.dat')}
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        result = df_to_list(md_df)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'text'],
                    ['imail', 'BLANK', 'C', '19990301', '19990305', 'BLANK', '19990301', 'imail', 'TAX1',
                     'Kennesaw', 'GA', '30144-2248', 'USA', 'OUTGOING', r'..\documents\formletters\taxes.doc',
                     'BLANK', 'BLANK', 'taxes.doc', 'BLANK'],
                    ['imail', 'BLANK', 'C', '19990501', '19990507', 'BLANK', '19990501', 'imail', 'HMO',
                     'Marietta', 'GA', '30062-5584', 'USA', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'Against 2'],
                    ['usmail', 'BLANK', 'C', '19990607', '19990617', 'BLANK', '19990607', 'usmail', 'TAX1',
                     'Marietta', 'GA', '30062-1613', 'USA', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for no_match_communication_id")

    def test_no_match_person_id(self):
        """Test for when the person_id in 1B does not match 2A"""
        # Makes variable for the function and runs the function.
        paths_dict = {'1B': os.path.join('test_data', 'read', 'no_match_person_id', '1B.dat'),
                      '2A': os.path.join('test_data', 'read', 'no_match_person_id', '2A.dat'),
                      '2C': os.path.join('test_data', 'read', 'no_match_person_id', '2C.dat'),
                      '2D': os.path.join('test_data', 'read', 'no_match_person_id', '2D.dat')}
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        result = df_to_list(md_df)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id', 'file_location',
                     'file_name', 'text'],
                    ['imail', 'BLANK', 'C', '19990301', '19990305', 'BLANK', '19990301', 'imail', 'TAX1',
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'OUTGOING', r'..\documents\formletters\taxes.doc',
                     'BLANK', 'BLANK', 'taxes.doc', 'Support for 1'],
                    ['imail', 'BLANK', 'C', '20000315', '20000402', 'BLANK', '20000315', 'imail', 'BLANK',
                     'BLANK', 'BLANK', 'BLANK', 'BLANK', 'OUTGOING', r'..\documents\indivletters\12345.doc',
                     'BLANK', 'BLANK', '12345.doc', 'Neutral re 4']]
        self.assertEqual(expected, result, "Problem with test for no_match_person_id")


if __name__ == '__main__':
    unittest.main()
