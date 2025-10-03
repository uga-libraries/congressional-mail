"""
Tests for the function read_metadata(), which reads the dat file into a dataframe.
"""
import os
import unittest
from archival_office_correspondence_data import read_metadata


class MyTestCase(unittest.TestCase):

    def test_blank(self):
        """Test for when the metadata file has blank rows, which are not included"""
        # Runs the function being tested.
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'archive_blank.dat'))

        # Tests the dataframe has the expected columns and values.
        result = [md_df.columns.tolist()] + md_df.values.tolist()
        expected = [['name', 'title', 'organization', 'address_line_1', 'address_line_2', 'city', 'state_code',
                     'zip_code', 'correspondence_type', 'correspondence_topic', 'correspondence_subtopic',
                     'letter_date', 'staffer_initials', 'document_number', 'comments'],
                    ['LAST A, FIRST A, MR.', '', '', '1001 1ST STREET', '', 'CITY A', 'GA', '30000-1234',
                     'CASE', 'TR-HWY', '', '', 'RA', '555QRS667', 'ANOTHER NOTE'],
                    ['LAST B, FIRST B MIDDLE, JR.', '', '', '200 ROAD', 'APT 5B', 'CITY A', 'GA', '30001',
                     'ISSUE', 'TR-RAL', '', '980104', 'NOP', '', '']]
        self.assertEqual(expected, result, "Problem with test for blank rows")

    def test_no_blank(self):
        """Test for when the metadata file has no blank rows"""
        # Runs the function being tested.
        md_df = read_metadata(os.path.join('test_data', 'read_metadata', 'archive.dat'))

        # Tests the dataframe has the expected columns and values.
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
        self.assertEqual(expected, result, "Problem with test for no blank rows")


if __name__ == '__main__':
    unittest.main()
