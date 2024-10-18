"""
Tests for the function read_metadata(), which reads the DAT file into a pandas dataframe.
"""
import os
import unittest
from css_archiving_format import read_metadata


class MyTestCase(unittest.TestCase):

    def test_parsererror(self):
        """Test for when the DAT file has content with tabs, resulting in a ParserError without correction"""
        md_df = read_metadata(os.path.join('test_data', 'read_parsererror_md.dat'))

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
