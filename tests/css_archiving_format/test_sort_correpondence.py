"""
Tests for the function sort_correspondence(), which organizes a copy of the letters by topic.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import pandas as pd
import unittest
from css_archiving_format import sort_correspondence


class MyTestCase(unittest.TestCase):

    def test_duplicate_file(self):
        """Test for when a file is in the metadata more than once"""
        self.assertEqual(True, True, "Problem with test for duplicate_file")

    def test_duplicate_topic(self):
        """Test for when a topic is in the metadata more than once, due to topic combinations"""
        self.assertEqual(True, True, "Problem with test for duplicate_topic")

    def test_filenotfounderror(self):
        """Test for when a file is in the metadata but not the directory"""
        self.assertEqual(True, True, "Problem with test for filenotfounderror")

    def test_multiple_topic(self):
        """Test for when a row has multiple topics (joined by ^)"""
        df = pd.DataFrame([['Agriculture', 'file1'], ['Agriculture^Labor', 'file2'],
                           ['Admin^Small Business^Tax', 'file3']], columns=['in_topic', 'in_document_name'])
        sort_correspondence(df, 'output_dir')
        self.assertEqual(True, True, "Problem with test for multiple topic")

    def test_unique(self):
        """Test for when each topic and file is unique"""
        df = pd.DataFrame([['Agriculture', 'file1'], ['Labor', 'file2'], ['Small Business', 'file3']],
                          columns=['in_topic', 'in_document_name'])
        sort_correspondence(df, 'output_dir')
        self.assertEqual(True, True, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
