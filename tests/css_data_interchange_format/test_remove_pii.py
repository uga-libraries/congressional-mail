import pandas as pd
import unittest
from css_data_interchange_format import remove_pii


class MyTestCase(unittest.TestCase):

    def test_1b(self):
        """Test for columns in table 1B."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                               '17', '18', '19', '20', '21', '22', '23', '24', '25', '26']],
                             columns=['record_type', 'person_id', 'address_id', 'address_type', 'primary_flag',
                                      'default_address_flag', 'title', 'organization_name', 'address_line_1',
                                      'address_line_2', 'address_line_3', 'address_line_4', 'city', 'state_code',
                                      'zip_code', 'carrier_route', 'county', 'country', 'district', 'precinct',
                                      'no_mail_flag', 'deliverability', 'extra1', 'extra2', 'extra3', 'extra4'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['person_id', 'city', 'state_code', 'zip_code', 'country']
        self.assertEqual(expected, md_df.columns.tolist(), "Problem with test for 1B, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['2', '13', '14', '15', '18']]
        self.assertEqual(expected, md_df.values.tolist(), "Problem with test for 1B, values")

    def test_2a(self):
        """Test for columns in table 2A."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                               '17', '18', '19', '20', '21']],
                             columns=['record_type', 'person_id', 'communication_id', 'workflow_id',
                                      'workflow_person_id', 'communication_type', 'user_id', 'approved_by', 'status',
                                      'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type',
                                      'address_id', 'email_address', 'household_flag', 'household_id', 'group_name',
                                      'salutation', 'extra'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['person_id', 'communication_id', 'communication_type', 'approved_by', 'status', 'date_in',
                    'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name']
        self.assertEqual(expected, md_df.columns.tolist(), "Problem with test for 2A, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['2', '3', '6', '8', '9', '10', '11', '12', '13', '14', '19']]
        self.assertEqual(expected, md_df.values.tolist(), "Problem with test for 2A, values")

    def test_2c(self):
        """Test for columns in table 2C."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7', '8']],
                             columns=['record_type', 'person_id', 'communication_id', 'document_type',
                                      'communication_document_name', 'communication_document_id',
                                      'file_location', 'file_name'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['person_id', 'communication_id', 'document_type', 'communication_document_name',
                    'communication_document_id', 'file_location', 'file_name']
        self.assertEqual(expected, md_df.columns.tolist(), "Problem with test for 2C, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['2', '3', '4', '5', '6', '7', '8']]
        self.assertEqual(expected, md_df.values.tolist(), "Problem with test for 2C, values")


if __name__ == '__main__':
    unittest.main()
