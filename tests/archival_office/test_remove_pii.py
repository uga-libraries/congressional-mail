"""
Test for the function remove_pii(), which removes columns that contain personally identifiable information.
To simplify input, the content is just numbers instead of reasonable data for the column types.
Since the code assigns the columns, rather than relying on the input data, all columns will always be present
or there would have already been an error.
"""
import pandas as pd
import unittest
from archival_office_correspondence_data import remove_pii


class MyTestCase(unittest.TestCase):

    def test_function(self):
        """Test for when the function runs correctly."""
        # Makes a dataframe to use as test input.
        md_df = pd.DataFrame([['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']],
                             columns=['name', 'title', 'organization', 'address_line_1', 'address_line_2', 'city',
                                      'state_code', 'zip_code', 'correspondence_type', 'correspondence_topic',
                                      'correspondence_subtopic', 'letter_date', 'staffer_initials', 'document_number',
                                      'comments'])
        md_df = remove_pii(md_df)

        # Tests the columns of the returned dataframe are correct.
        expected = ['city', 'state_code', 'zip_code', 'correspondence_type', 'correspondence_topic',
                    'correspondence_subtopic', 'letter_date', 'staffer_initials', 'document_number', 'comments']
        self.assertEqual(md_df.columns.tolist(), expected, "Problem with test for function, columns")

        # Tests the values in the returned dataframe are correct.
        expected = [['6', '7', '8', '9', '10', '11', '12', '13', '14', '15']]
        self.assertEqual(md_df.values.tolist(), expected, "Problem with test for function, values")


if __name__ == '__main__':
    unittest.main()
