"""
Tests for the function sort_correspondence(), which organizes a copy of the letters by topic.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import sort_correspondence


def make_df(row_list):
    """Make a dataframe from a list of rows with consistent columns, used for test input"""
    df = pd.DataFrame(row_list, columns=['zip', 'in_topic', 'in_document_name'])
    return df


def make_dir_list(dir_path):
    """Make a list of the files in the folder created by the function to compare to expected results"""
    contents_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            contents_list.append(os.path.join(root, file))
    return contents_list


def make_log_list():
    """Makes a list of the contents of the log created when files in the metadata are not in the directory"""
    log_path = os.path.join(os.getcwd(), 'test_data', 'sort_correspondence', 'topic_sort_file_not_found.csv')
    log_df = pd.read_csv(log_path)
    log_list = [log_df.columns.tolist()] + log_df.values.tolist()
    return log_list


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variables used by every test"""
        self.by_topic = os.path.join(os.getcwd(), 'test_data', 'sort_correspondence', 'Correspondence_by_Topic')
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'sort_correspondence', 'css_export')
        self.output_dir = os.path.join(os.getcwd(), 'test_data', 'sort_correspondence')

    def tearDown(self):
        """Delete the script outputs, if made"""
        # Correspondence_by_Topic folder.
        if os.path.exists(self.by_topic):
            shutil.rmtree(self.by_topic)

        # Log for FileNotFoundError.
        log_path = os.path.join(os.getcwd(), 'test_data', 'sort_correspondence', 'topic_sort_file_not_found.csv')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_blank(self):
        """Test for when some rows have no topic and/or no document and should be skipped"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'nan', r'..\documents\BlobExport\file3.txt'],
                      ['30601', 'Agriculture', r'..\documents\BlobExport\file1.txt'],
                      ['30602', 'Agriculture^Peanuts', r'..\documents\BlobExport\file2.txt'],
                      ['30603', 'Agriculture^Peanuts', 'nan'],
                      ['30604', 'nan', 'nan']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'file2.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'file2.txt')]
        self.assertEqual(result, expected, "Problem with test for blank")

    def test_duplicate_file(self):
        """Test for when a file is in the metadata with the same topic more than once"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\file1.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\file1.txt'],
                      ['30602', 'Small Business', r'..\documents\BlobExport\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'file1.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'file1.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'file3.txt')]
        self.assertEqual(result, expected, "Problem with test for duplicate_file")

    def test_duplicate_topic(self):
        """Test for when a topic is in the metadata more than once, due to topic combinations"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\file1.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\file2.txt'],
                      ['30602', 'Agriculture^Peanuts^Tax', r'..\documents\BlobExport\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'file2.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'file3.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'file2.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'file3.txt')]
        self.assertEqual(result, expected, "Problem with test for duplicate_topic")

    def test_filenotfounderror(self):
        """Test for when a file is in the metadata but not the directory"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\file1.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\file_missing.txt'],
                      ['30602', 'Peanuts', r'..\documents\BlobExport\file2.txt'],
                      ['30603', 'Peanuts', r'..\documents\BlobExport\folder_missing\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'file1.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'file2.txt')]
        self.assertEqual(result, expected, "Problem with test for filenotfounderror, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['Agriculture', r'..\documents\BlobExport\file_missing.txt'],
                    ['Peanuts', r'..\documents\BlobExport\file_missing.txt'],
                    ['Peanuts', r'..\documents\BlobExport\folder_missing\file3.txt']]
        self.assertEqual(result, expected, "Problem with test for filenotfounderror, log")

    def test_folder_empty(self):
        """Test for when no files for a topic are in the directory and the topic folder is empty"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\missing\file1.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\missing\file2.txt'],
                      ['30602', 'Peanuts', r'..\documents\BlobExport\missing\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the topic folders are not in Correspondence_by_Topic:
        result = [os.path.exists(os.path.join(self.by_topic, 'Agriculture')),
                  os.path.exists(os.path.join(self.by_topic, 'Peanuts'))]
        expected = [False, False]
        self.assertEqual(result, expected, "Problem with test for folder empty, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['Agriculture', r'..\documents\BlobExport\missing\file1.txt'],
                    ['Agriculture', r'..\documents\BlobExport\missing\file2.txt'],
                    ['Peanuts', r'..\documents\BlobExport\missing\file2.txt'],
                    ['Peanuts', r'..\documents\BlobExport\missing\file3.txt']]
        self.assertEqual(result, expected, "Problem with test for folder empty, log")

        # Verifies folders without a file are not still present.
        result = [os.path.exists(os.path.join(self.by_topic, 'Agriculture')),
                  os.path.exists(os.path.join(self.by_topic, 'Peanuts'))]
        expected = [False, False]
        self.assertEqual(result, expected, "Problem with test for folder empty, folders not deleted")

    def test_folder_name_error(self):
        """Test for when a topic contains a character that cannot be in a folder name"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'A\\B^C/D^E:F^***', r'..\documents\BlobExport\file1.txt'],
                      ['30601', 'G?^"H"', r'..\documents\BlobExport\file2.txt'],
                      ['30602', '<I|J>', r'..\documents\BlobExport\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'A_B', 'file1.txt'),
                    os.path.join(self.by_topic, 'C_D', 'file1.txt'),
                    os.path.join(self.by_topic, 'E_F', 'file1.txt'),
                    os.path.join(self.by_topic, 'G_', 'file2.txt'),
                    os.path.join(self.by_topic, '_H_', 'file2.txt'),
                    os.path.join(self.by_topic, '_I_J_', 'file3.txt'),
                    os.path.join(self.by_topic, '___', 'file1.txt')]
        self.assertEqual(result, expected, "Problem with test for folder name error")

    def test_multiple_topic(self):
        """Test for when a row has multiple topics (joined by ^)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\file1.txt'],
                      ['30601', 'Farm^Peanuts', r'..\documents\BlobExport\file2.txt'],
                      ['30602', 'Admin^Small Business^Tax', r'..\documents\BlobExport\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Admin', 'file3.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'file1.txt'),
                    os.path.join(self.by_topic, 'Farm', 'file2.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'file2.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'file3.txt')]
        self.assertEqual(result, expected, "Problem with test for multiple topic")

    def test_unique(self):
        """Test for when each topic and file is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\file1.txt'],
                      ['30601', 'Peanuts', r'..\documents\BlobExport\file2.txt'],
                      ['30602', 'Small Business', r'..\documents\BlobExport\file3.txt']])
        sort_correspondence(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'file1.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'file2.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'file3.txt')]
        self.assertEqual(result, expected, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
