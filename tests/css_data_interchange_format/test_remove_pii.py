"""
Tests for the function remove_pii(), which removes columns that contain personally identifiable information.
To simplify input, tests use dataframes with only some of the columns present in a real export
and the content is just numbers instead of reasonable data for the column types.
"""
import pandas as pd
import unittest
from css_data_interchange_format import remove_pii


class MyTestCase(unittest.TestCase):

    def test_all_present(self):
        """Test for when all PII columns are present."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7', '8', '9',
                               '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                               '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                               '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
                               '40', '41', '42', '43', '44', '45', '46', '47', '48']],
                             columns=['record_type_x', 'person_id_x', 'address_id_x', 'address_type', 'primary_flag',
                                      'default_address_flag', 'title', 'organization_name', 'address_line_1',
                                      'address_line_2', 'address_line_3', 'address_line_4', 'city', 'state_code',
                                      'zip_code', 'carrier_route', 'county', 'country', 'district', 'precinct',
                                      'no_mail_flag', 'deliverability', 'record_type_y', 'communication_id',
                                      'workflow_id', 'workflow_person_id', 'communication_type', 'user_id',
                                      'approved_by', 'status', 'date_in', 'date_out', 'reminder_date', 'update_date',
                                      'response_type', 'address_id_y', 'email_address', 'household_flag',
                                      'household_id', 'group_name', 'salutation', 'record_type', 'person_id_y',
                                      'document_type', 'communication_document_name', 'communication_document_id',
                                      'file_location', 'file_name'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['city', 'state_code', 'zip_code', 'country', 'communication_type', 'approved_by', 'status',
                    'date_in', 'date_out', 'reminder_date', 'update_date', 'response_type', 'group_name',
                    'document_type', 'communication_document_name', 'file_location', 'file_name']
        self.assertEqual(md_df.columns.tolist(), expected, "Problem with test for all present, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['13', '14', '15', '18', '27', '29', '30', '31', '32', '33', '34', '35',
                     '40', '44', '45', '47', '48']]
        self.assertEqual(md_df.values.tolist(), expected, "Problem with test for all present, values")

    def test_some_present(self):
        """Test for when some PII columns are present."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7', '8', '9',
                               '10', '11', '12', '13', '14', '15', '16', '17']],
                             columns=['record_type_x', 'person_id_x', 'address_id_x', 'address_type', 'primary_flag',
                                      'default_address_flag', 'title', 'organization_name', 'address_line_1',
                                      'address_line_2', 'city', 'state_code', 'email_address', 'household_flag',
                                      'household_id', 'group_name', 'salutation'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['city', 'state_code', 'group_name']
        self.assertEqual(md_df.columns.tolist(), expected, "Problem with test for some present, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['11', '12', '16']]
        self.assertEqual(md_df.values.tolist(), expected, "Problem with test for some present, values")

    def test_none_present(self):
        """Test for when no PII columns are present."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5'], ['11', '12', '13', '14', '15']],
                             columns=['status', 'date_in', 'date_out', 'reminder_date', 'update_date'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['status', 'date_in', 'date_out', 'reminder_date', 'update_date']
        self.assertEqual(md_df.columns.tolist(), expected, "Problem with test for none present, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['1', '2', '3', '4', '5'], ['11', '12', '13', '14', '15']]
        self.assertEqual(md_df.values.tolist(), expected, "Problem with test for none present, values")


if __name__ == '__main__':
    unittest.main()
