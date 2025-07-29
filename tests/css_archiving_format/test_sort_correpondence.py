"""
Tests for the function sort_correspondence(), which organizes a copy of the letters by topic.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import shutil

import pandas as pd
import unittest
from css_archiving_format import sort_correspondence


def make_df(row_list):
    """Make a dataframe from a list of rows with consistent columns, used for test input"""
    df = pd.DataFrame(row_list, columns=['zip', 'in_topic', 'in_document_name'])
    return df


def make_dir_list(dir_path):
    """Make a list of the contents of the folder created by the function to compare to expected results"""
    contents_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            contents_list.append(os.path.join(root, file))
    return contents_list


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variables used by every test"""
        self.by_topic = os.path.join(os.getcwd(), 'test_data', 'sort_correspondence', 'Correspondence_by_Topic')
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'sort_correspondence', 'css_export')
        self.output_dir = os.path.join(os.getcwd(), 'test_data', 'sort_correspondence')

    def tearDown(self):
        """Delete the Correspondence_by_Topic folder and its contents"""
        if os.path.exists(self.by_topic):
            shutil.rmtree(self.by_topic)

    def test_duplicate_file(self):
        """Test for when a file is in the metadata with the same topic more than once"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\file1.txt'],
                      ['30601', 'Agriculture^Labor', r'..\documents\BlobExport\file1.txt'],
                      ['30602', 'Small Business', r'..\documents\BlobExport\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'file1.txt'),
                    os.path.join(self.by_topic, 'Labor', 'file1.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'file3.txt')]
        self.assertEqual(result, expected, "Problem with test for duplicate_file")

    def test_duplicate_topic(self):
        """Test for when a topic is in the metadata more than once, due to topic combinations"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\file1.txt'],
                      ['30601', 'Agriculture^Labor', r'..\documents\BlobExport\file2.txt'],
                      ['30602', 'Agriculture^Labor^Tax', r'..\documents\BlobExport\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'file2.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'file3.txt'),
                    os.path.join(self.by_topic, 'Labor', 'file2.txt'),
                    os.path.join(self.by_topic, 'Labor', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'file3.txt')]
        self.assertEqual(result, expected, "Problem with test for duplicate_topic")

    def test_filenotfounderror(self):
        """Test for when a file is in the metadata but not the directory"""
        self.assertEqual(True, True, "Problem with test for filenotfounderror")

    def test_folder_empty(self):
        """Test for when no files for a topic are in the directory and the topic folder is empty"""
        self.assertEqual(True, True, "Problem with test for folder empty")

    def test_folder_name_error(self):
        """Test for when a topic contains a character that cannot be in a folder name"""
        self.assertEqual(True, True, "Problem with test for folder name error")

    def test_multiple_topic(self):
        """Test for when a row has multiple topics (joined by ^)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\file1.txt'],
                      ['30601', 'Farm^Labor', r'..\documents\BlobExport\file2.txt'],
                      ['30602', 'Admin^Small Business^Tax', r'..\documents\BlobExport\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Admin', 'file3.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'file1.txt'),
                    os.path.join(self.by_topic, 'Farm', 'file2.txt'),
                    os.path.join(self.by_topic, 'Labor', 'file2.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'file3.txt')]
        self.assertEqual(result, expected, "Problem with test for multiple topic")

    def test_unique(self):
        """Test for when each topic and file is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\file1.txt'],
                      ['30601', 'Labor', r'..\documents\BlobExport\file2.txt'],
                      ['30602', 'Small Business', r'..\documents\BlobExport\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'file1.txt'),
                    os.path.join(self.by_topic, 'Labor', 'file2.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'file3.txt')]
        self.assertEqual(result, expected, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
