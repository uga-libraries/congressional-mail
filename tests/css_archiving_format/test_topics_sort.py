import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import topics_sort
from test_script import make_dir_list


def make_df(rows):
    """Make a df for test input"""
    columns = ['zip', 'in_topic', 'in_document_name', 'out_topic', 'out_document_name',
               'in_topic_split', 'out_topic_split']
    df = pd.DataFrame(rows, columns=columns)
    return df


def make_log_list():
    """Makes a list of the contents of the log created when files in the metadata are not in the directory"""
    log_path = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'topics_sort_file_not_found.csv')
    log_df = pd.read_csv(log_path)
    log_list = [log_df.columns.tolist()] + log_df.values.tolist()
    return log_list


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variables used by every test"""
        self.by_topic = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'correspondence_by_topic')
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'css_export')
        self.output_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort')

    def tearDown(self):
        """Delete the script outputs, if made"""
        # correspondence_by_topic folder.
        if os.path.exists(self.by_topic):
            shutil.rmtree(self.by_topic)

        # Log for FileNotFoundError.
        log_path = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'topics_sort_file_not_found.csv')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_folder_in(self):
        """Test for when no out files for a topic are in the directory, but some in are"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\missing.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\objects\missing\file2.txt',
                       'Agriculture^Peanuts', r'..\documents\BlobExport\responses\missing.txt'],
                      ['30602', 'Peanuts', r'..\documents\BlobExport\objects\missing\file3.txt',
                       'Peanuts', r'..\documents\BlobExport\responses\missing.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the empty topic folder and empty from_constituents folder are not in correspondence_by_topic:
        result = [os.path.exists(os.path.join(self.by_topic, 'Agriculture', 'from_constituents')),
                  os.path.exists(os.path.join(self.by_topic, 'Agriculture', 'to_constituents')),
                  os.path.exists(os.path.join(self.by_topic, 'Peanuts'))]
        expected = [True, False, False]
        self.assertEqual(expected, result, "Problem with test for one folder empty, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['Agriculture', r'..\documents\BlobExport\objects\missing\file2.txt'],
                    ['Peanuts', r'..\documents\BlobExport\objects\missing\file2.txt'],
                    ['Peanuts', r'..\documents\BlobExport\objects\missing\file3.txt'],
                    ['Agriculture', r'..\documents\BlobExport\responses\missing.txt'],
                    ['Peanuts', r'..\documents\BlobExport\responses\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for one folder empty, log")

    def test_folder_neither(self):
        """Test for when no files (in or out) for a topic are in the directory and the topic folder is empty"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\objects\missing\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\missing.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\objects\missing\file2.txt',
                       'Agriculture^Peanuts', r'..\documents\BlobExport\responses\missing.txt'],
                      ['30602', 'Peanuts', r'..\documents\BlobExport\objects\missing\file3.txt',
                       'Peanuts', r'..\documents\BlobExport\responses\missing.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the empty topic folders are not in correspondence_by_topic:
        result = [os.path.exists(os.path.join(self.by_topic, 'Agriculture')),
                  os.path.exists(os.path.join(self.by_topic, 'Peanuts'))]
        expected = [False, False]
        self.assertEqual(expected, result, "Problem with test for folders empty, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['Agriculture', r'..\documents\BlobExport\objects\missing\file1.txt'],
                    ['Agriculture', r'..\documents\BlobExport\objects\missing\file2.txt'],
                    ['Peanuts', r'..\documents\BlobExport\objects\missing\file2.txt'],
                    ['Peanuts', r'..\documents\BlobExport\objects\missing\file3.txt'],
                    ['Agriculture', r'..\documents\BlobExport\responses\missing.txt'],
                    ['Peanuts', r'..\documents\BlobExport\responses\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for folders empty, log")

    def test_topic_both(self):
        """Test for when a topic is in the metadata more than once, due to topic combinations"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\objects\file2.txt',
                       'Tax', r'..\documents\BlobExport\responses\answer1.txt'],
                      ['30602', 'Agriculture^Peanuts^Tax', r'..\documents\BlobExport\objects\file3.txt',
                       'Agriculture^Tax', r'..\documents\BlobExport\responses\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'answer2.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'Tax', 'to_constituents', 'answer2.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate_topic")

    def test_topic_in(self):
        """Test for when each topic and file combination is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'Agriculture', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30602', 'Peanuts', r'..\documents\BlobExport\objects\file2.txt',
                       'Peanuts', r'..\documents\BlobExport\responses\answer1.txt'],
                      ['30603', 'Small Business', r'..\documents\BlobExport\objects\file3.txt',
                       'Tax', r'..\documents\BlobExport\responses\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'to_constituents', 'answer2.txt')]
        self.assertEqual(expected, result, "Problem with test for unique")

    def test_topic_out(self):
        """Test for when each topic and file combination is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'Agriculture', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30602', 'Peanuts', r'..\documents\BlobExport\objects\file2.txt',
                       'Peanuts', r'..\documents\BlobExport\responses\answer1.txt'],
                      ['30603', 'Small Business', r'..\documents\BlobExport\objects\file3.txt',
                       'Tax', r'..\documents\BlobExport\responses\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'to_constituents', 'answer2.txt')]
        self.assertEqual(expected, result, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
