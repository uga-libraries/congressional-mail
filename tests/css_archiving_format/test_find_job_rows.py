"""
Tests for the function find_job_rows(),
which finds metadata rows with topics or text that indicate they are job applications and returns as a df.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_archiving_format import find_job_rows
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_all(self):
        """Test for when all patterns indicating job applications are present"""

        self.assertEqual(True, False, "Problem with test for all patterns")

    def test_in_text(self):
        """Test for when all patterns indicating job applications are present"""

        self.assertEqual(True, False, "Problem with test for all patterns")

    def test_in_topic(self):
        """Test for when all patterns indicating job applications are present"""

        self.assertEqual(True, False, "Problem with test for all patterns")

    def test_none(self):
        """Test for when all patterns indicating job applications are present"""

        self.assertEqual(True, False, "Problem with test for all patterns")

    def test_out_document_name(self):
        """Test for when all patterns indicating job applications are present"""

        self.assertEqual(True, False, "Problem with test for all patterns")

    def test_out_text(self):
        """Test for when all patterns indicating job applications are present"""

        self.assertEqual(True, False, "Problem with test for all patterns")

    def test_out_topic(self):
        """Test for when all patterns indicating job applications are present"""

        self.assertEqual(True, False, "Problem with test for all patterns")

        
if __name__ == '__main__':
    unittest.main()
