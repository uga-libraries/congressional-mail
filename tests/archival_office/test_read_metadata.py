"""
Test for the function read_metadata(), which reads the dat file into a dataframe.
"""
import os
import unittest
from archival_office_correspondence_data import read_metadata


class MyTestCase(unittest.TestCase):

    def test_function(self):
        """Test for when the function works correctly"""
        # Runs the function being tested.
        md_df = read_metadata(os.path.join('test_data', 'read_md.dat'))

        # Tests the dataframe has the expected columns and values.
        # First converts the resulting dataframe into a list, with blanks filled with '', for easier comparison.
        result = [md_df.columns.tolist()] + md_df.values.tolist()
        expected = [['name', 'title', 'organization', 'address_line_1', 'address_line_2', 'city', 'state_code',
                     'zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic',
                     'letter_date', 'staffer_initials', 'document_number', 'comments'],
                    ['', '', 'COMPANY ABC', '123 MAIN', '', 'CITY A', 'GA', '30000', 'ISSUE', 'CO-OLD',
                     '', '971002', 'ABC', '123XYZ456', ''],
                    [',  ,', 'EDITOR', 'NEWSPAPER GAZETTE', 'PO BOX 456', '999 BLVD', 'CITY B', 'FL', '70000', 'ISSUE',
                     'PR-GEN', '', '971003', 'ABC', '', 'NOTE'],
                    ['LAST A, FIRST A, MR.', '', '', '1001 1ST STREET', '', 'CITY A', 'GA', '30000-1234',
                     'CASE', 'TR-HWY', '', '', 'RA', '555QRS667', 'ANOTHER NOTE'],
                    ['LAST B, FIRST B MIDDLE, JR.', '', '', '200 ROAD', 'APT 5B', 'CITY A', 'GA', '30001',
                     'ISSUE', 'TR-RAL', '', '980104', 'NOP', '', '']]
        self.assertEqual(result, expected, "Problem with test for function")


if __name__ == '__main__':
    unittest.main()
