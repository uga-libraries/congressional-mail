"""
Tests for the function remove_pii(), which removes columns that contain personally identifiable information.
To simplify input, the content is just numbers instead of reasonable data for the column types.
"""
import pandas as pd
import unittest
from cms_data_interchange_format import remove_pii


class MyTestCase(unittest.TestCase):

    def test_1b(self):
        """Test for columns in table 1B."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                               '17', '18', '19', '20', '21', '22']],
                             columns=['record_type', 'constituent_id', 'address_id', 'address_type', 'primary_flag',
                                      'default_address_flag', 'title', 'organization_name', 'address_line_1',
                                      'address_line_2', 'address_line_3', 'address_line_4', 'city', 'state',
                                      'zip_code', 'carrier_route', 'county', 'country', 'district', 'precinct',
                                      'no_mail_flag', 'agency_code'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['constituent_id', 'city', 'state', 'zip_code', 'country']
        self.assertEqual(expected, md_df.columns.tolist(), "Problem with test for 1B, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['2', '13', '14', '15', '18']]
        self.assertEqual(expected, md_df.values.tolist(), "Problem with test for 1B, values")

    def test_2a(self):
        """Test for columns in table 2A."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']],
                             columns=['record_type', 'constituent_id', 'correspondence_id', 'correspondence_type',
                                      'staff', 'date_in', 'date_out', 'tickler_date', 'update_date', 'response_type',
                                      'address_id', 'household_flag', 'household_id', 'extra1', 'extra2'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['constituent_id', 'correspondence_id', 'correspondence_type', 'staff', 'date_in', 'date_out',
                    'tickler_date', 'update_date', 'response_type']
        self.assertEqual(expected, md_df.columns.tolist(), "Problem with test for 2A, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['2', '3', '4', '5', '6', '7', '8', '9', '10']]
        self.assertEqual(expected, md_df.values.tolist(), "Problem with test for 2A, values")

    def test_2b(self):
        """Test for columns in table 2B."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5']],
                             columns=['record_type', 'constituent_id', 'correspondence_id', 'correspondence_code',
                                      'position'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['constituent_id', 'correspondence_id', 'correspondence_code', 'position']
        self.assertEqual(expected, md_df.columns.tolist(), "Problem with test for 2B, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['2', '3', '4', '5']]
        self.assertEqual(expected, md_df.values.tolist(), "Problem with test for 2B, values")

    def test_2c(self):
        """Test for columns in table 2C."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7']],
                             columns=['record_type', 'constituent_id', 'correspondence_id', '2C_sequence_number',
                                      'document_type', 'correspondence_document_name', 'file_location'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['constituent_id', 'correspondence_id', '2C_sequence_number', 'document_type',
                    'correspondence_document_name', 'file_location']
        self.assertEqual(expected, md_df.columns.tolist(), "Problem with test for 2C, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['2', '3', '4', '5', '6', '7']]
        self.assertEqual(expected, md_df.values.tolist(), "Problem with test for 2C, values")


if __name__ == '__main__':
    unittest.main()
