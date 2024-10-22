"""
Tests for the function split_congress_year(), which makes one CSV for letters received in each Congress Year.
To simplify input, tests use dataframes with only some of the columns present in a real css/cms export
"""
import os
import pandas as pd
import unittest
from archival_office_correspondence_data import split_congress_year
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function output, if it was created"""
        filenames = ['1959-1960.csv', '1997-1998.csv', '1999-2000.csv', '2001-2002.csv', '2003-2004.csv',
                     '2059-2060.csv', 'undated.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_all(self):
        """Test for a combination of all date values: even, odd, 1900s, 2000s, and blank"""
        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['ATLANTA', 'TX-GEN', '970102', 'AC'],
                              ['RIVERDALE', 'FR-GEN', '980505', 'AC'],
                              ['ATLANTA', 'EV-WAT', '990719', 'VT'],
                              ['LAWRENCEVILLE', 'FR-GEN', '', 'AC'],
                              ['ROSWELL', '', '001031', 'TGO'],
                              ['COLUMBUS', 'TX-GEN', '030315', ''],
                              ['LAWRENCEVILLE', 'CO-OLD', '', 'VT']],
                             columns=['city', 'correspondence_topic', 'letter_date', 'staffer_initials'])
        split_congress_year(md_df, 'test_data')

        # Tests that 1997-1998.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '1997-1998.csv'))
        expected = [['city', 'correspondence_topic', 'letter_date', 'staffer_initials'],
                    ['ATLANTA', 'TX-GEN', '970102', 'AC'],
                    ['RIVERDALE', 'FR-GEN', '980505', 'AC']]
        self.assertEqual(result, expected, "Problem with test for all years, 1997-1998")

        # Tests that 1999-2000.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '1999-2000.csv'))
        expected = [['city', 'correspondence_topic', 'letter_date', 'staffer_initials'],
                    ['ATLANTA', 'EV-WAT', '990719', 'VT'],
                    ['ROSWELL', 'nan', '001031', 'TGO']]
        self.assertEqual(result, expected, "Problem with test for all years, 1999-2000")

        # Tests that 2003-2004.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '2003-2004.csv'))
        expected = [['city', 'correspondence_topic', 'letter_date', 'staffer_initials'],
                    ['COLUMBUS', 'TX-GEN', '030315', 'nan']]
        self.assertEqual(result, expected, "Problem with test for all years, 2003-2004")

        # Tests that undated.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'undated.csv'))
        expected = [['city', 'correspondence_topic', 'letter_date', 'staffer_initials'],
                    ['LAWRENCEVILLE', 'FR-GEN', 'nan', 'AC'],
                    ['LAWRENCEVILLE', 'CO-OLD', 'nan', 'VT']]
        self.assertEqual(result, expected, "Problem with test for all years, undated")

    def test_blank(self):
        """Test for when some of the letters do not have a date (letter_date column is empty string)"""

        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['ROSWELL', '', '', 'TGO'],
                              ['COLUMBUS', 'TX-GEN', '', ''],
                              ['LAWRENCEVILLE', 'CO-OLD', '', 'VT']],
                             columns=['city', 'correspondence_topic', 'letter_date', 'staffer_initials'])
        split_congress_year(md_df, 'test_data')

        # Tests that undated.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', 'undated.csv'))
        expected = [['city', 'correspondence_topic', 'letter_date', 'staffer_initials'],
                    ['ROSWELL', 'nan', 'nan', 'TGO'],
                    ['COLUMBUS', 'TX-GEN', 'nan', 'nan'],
                    ['LAWRENCEVILLE', 'CO-OLD', 'nan', 'VT']]
        self.assertEqual(result, expected, "Problem with test for blank, undated")

    def test_1900s(self):
        """Test for when the years are from the 1900s (two-digit year is 60 or later)"""

        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['ATLANTA', 'TX-GEN', '970102', 'AC'],
                              ['RIVERDALE', 'FR-GEN', '980505', 'AC'],
                              ['ATLANTA', 'EV-WAT', '600719', 'VT']],
                             columns=['city', 'correspondence_topic', 'letter_date', 'staffer_initials'])
        split_congress_year(md_df, 'test_data')

        # Tests that 1959-1960.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '1959-1960.csv'))
        expected = [['city', 'correspondence_topic', 'letter_date', 'staffer_initials'],
                    ['ATLANTA', 'EV-WAT', '600719', 'VT']]
        self.assertEqual(result, expected, "Problem with test for 1900S, 1959-1960")

        # Tests that 1997-1998.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '1997-1998.csv'))
        expected = [['city', 'correspondence_topic', 'letter_date', 'staffer_initials'],
                    ['ATLANTA', 'TX-GEN', '970102', 'AC'],
                    ['RIVERDALE', 'FR-GEN', '980505', 'AC']]
        self.assertEqual(result, expected, "Problem with test for 1900S, 1997-1998")

    def test_2000s(self):
        """Test for when the years are from the 2000s (two-digit year is 59 or earlier"""

        # Makes a dataframe to use as test input and runs the function being tested.
        md_df = pd.DataFrame([['ATLANTA', 'TX-GEN', '590102', 'AC'],
                              ['ROSWELL', '', '001031', 'TGO'],
                              ['COLUMBUS', 'TX-GEN', '010315', '']],
                             columns=['city', 'correspondence_topic', 'letter_date', 'staffer_initials'])
        split_congress_year(md_df, 'test_data')

        # Tests that 1999-2000.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '1999-2000.csv'))
        expected = [['city', 'correspondence_topic', 'letter_date', 'staffer_initials'],
                    ['ROSWELL', 'nan', '001031', 'TGO']]
        self.assertEqual(result, expected, "Problem with test for 2000s, 1999-2000")

        # Tests that 2001-2002.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '2001-2002.csv'))
        expected = [['city', 'correspondence_topic', 'letter_date', 'staffer_initials'],
                    ['COLUMBUS', 'TX-GEN', '010315', 'nan']]
        self.assertEqual(result, expected, "Problem with test for 2000s, 2001-2002")

        # Tests that 2059-2060.csv has the correct values.
        result = csv_to_list(os.path.join('test_data', '2059-2060.csv'))
        expected = [['city', 'correspondence_topic', 'letter_date', 'staffer_initials'],
                    ['ATLANTA', 'TX-GEN', '590102', 'AC']]
        self.assertEqual(result, expected, "Problem with test for 2000s, 2059-2060")


if __name__ == '__main__':
    unittest.main()
