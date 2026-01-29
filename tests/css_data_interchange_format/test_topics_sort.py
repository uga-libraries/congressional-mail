import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_data_interchange_format import topics_sort


def make_df(row_list):
    """Make a dataframe from a list of rows with consistent columns, used for test input"""
    df = pd.DataFrame(row_list, columns=['zip_code', 'group_name', 'document_type', 'communication_document_name'])
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
    log_path = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'topics_sort_file_not_found.csv')
    log_df = pd.read_csv(log_path)
    log_list = [log_df.columns.tolist()] + log_df.values.tolist()
    return log_list


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variables used by every test"""
        self.by_topic = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'Correspondence_by_Topic')
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'css_export')
        self.output_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort')

    def tearDown(self):
        """Delete the script outputs, if made"""
        # Correspondence_by_Topic folder.
        if os.path.exists(self.by_topic):
            shutil.rmtree(self.by_topic)

        # Log for FileNotFoundError.
        log_path = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'topics_sort_file_not_found.csv')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_blank(self):
        """Test for when some rows have no topic and/or no document and should be skipped"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', np.nan, 'INCOMING', r'..\documents\ima\file1.txt'],
                      ['30601', 'dogs', 'INCOMING', np.nan],
                      ['30602', 'farm', 'AT_IN1', r'..\documents\objects\file3.txt'],
                      ['30603', np.nan, 'AT_IN2', np.nan],
                      ['30604', np.nan, 'OUTGOING', np.nan],
                      ['30605', 'dogs', 'AT_OUT2', np.nan],
                      ['30606', np.nan, 'AT_OUT2', r'..\documents\indivletters\toA.txt'],
                      ['30607', 'farm', 'AT_OUT2', r'..\documents\indivletters\toB.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents', 'toB.txt')]
        self.assertEqual(expected, result, "Problem with test for blank")

    def test_duplicate_file(self):
        """Test for when a file is in the metadata with the same topic more than once"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', 'INCOMING', r'..\documents\ima\file1.txt'],
                      ['30601', 'dogs', 'INCOMING', r'..\documents\objects\file2.txt'],
                      ['30602', 'dogs', 'AT_IN1', r'..\documents\objects\file2.txt'],
                      ['30603', 'dogs', 'AT_IN2', r'..\documents\objects\file2.txt'],
                      ['30604', 'dogs', 'OUTGOING', r'..\documents\indivletters\toA.txt'],
                      ['30605', 'dogs', 'AT_OUT2', r'..\documents\indivletters\toA.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cats', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'dogs', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'dogs', 'to_constituents', 'toA.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate_file")

    def test_duplicate_topic(self):
        """Test for when a topic is in the metadata more than once"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', 'INCOMING', r'..\documents\ima\file1.txt'],
                      ['30601', 'dogs', 'INCOMING', r'..\documents\objects\file2.txt'],
                      ['30602', 'cats', 'AT_IN1', r'..\documents\objects\file3.txt'],
                      ['30603', 'cats', 'AT_IN2', r'..\documents\objects\file4.txt'],
                      ['30604', 'cats', 'AT_OUT2', r'..\documents\indivletters\toB.txt'],
                      ['30605', 'cats', 'OUTGOING', r'..\documents\indivletters\toD.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cats', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'file4.txt'),
                    os.path.join(self.by_topic, 'cats', 'to_constituents', 'toB.txt'),
                    os.path.join(self.by_topic, 'cats', 'to_constituents', 'toD.txt'),
                    os.path.join(self.by_topic, 'dogs', 'from_constituents', 'file2.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate_topic")

    def test_filenotfounderror(self):
        """Test for when a file is in the metadata but not the directory"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', 'INCOMING', r'..\documents\ima\file1.txt'],
                      ['30601', 'dogs', 'INCOMING', r'..\documents\ima\file2.txt'],
                      ['30602', 'farm', 'AT_IN1', r'..\documents\objects\file3.txt'],
                      ['30603', 'park', 'AT_IN2', r'\doc\objects\file4.txt'],
                      ['30604', 'park', 'OUT_IN2', r'\doc\indivletter\toX.txt'],
                      ['30605', 'park', 'OUT_IN2', r'\doc\missing\toA.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cats', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt')]
        self.assertEqual(expected, result, "Problem with test for filenotfounderror, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['dogs', r'..\documents\ima\file2.txt'],
                    ['park', r'\doc\objects\file4.txt'],
                    ['park', r'\doc\indivletter\toX.txt'],
                    ['park', r'\doc\missing\toA.txt']]
        self.assertEqual(expected, result, "Problem with test for filenotfounderror, log")

    def test_folder_empty(self):
        """Test for when no outgoing files for a topic are in the directory, but some incoming are"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', 'INCOMING', r'..\documents\file1.txt'],
                      ['30601', 'dogs', 'INCOMING', r'..\documents\file2.txt'],
                      ['30602', 'cats', 'AT_IN1', r'..\documents\objects\file3.txt'],
                      ['30603', 'cats', 'AT_IN2', r'..\documents\objects\file4.txt'],
                      ['30604', 'cats', 'OUTGOING', r'..\documents\toX.txt'],
                      ['30605', 'cats', 'AT_OUT3', r'..\documents\toY.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cats', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'file4.txt')]
        self.assertEqual(expected, result, "Problem with test for one folder empty, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['cats', r'..\documents\file1.txt'],
                    ['dogs', r'..\documents\file2.txt'],
                    ['cats', r'..\documents\toX.txt'],
                    ['cats', r'..\documents\toY.txt']]
        self.assertEqual(expected, result, "Problem with test for one folder empty, log")

        # Verifies folder without a file is not still present.
        result = os.path.exists(os.path.join(self.by_topic, 'dogs'))
        expected = False
        self.assertEqual(expected, result, "Problem with test for one folder empty, folders not deleted")

    def test_folders_empty(self):
        """Test for when no files (incoming or outgoing) for a topic are in the directory and the topic folder is empty"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', 'INCOMING', r'..\documents\file1.txt'],
                      ['30601', 'dogs', 'INCOMING', r'..\documents\file2.txt'],
                      ['30602', 'farm', 'AT_IN1', r'..\documents\objects\file3.txt'],
                      ['30603', 'park', 'AT_IN2', r'..\documents\objects\file4.txt'],
                      ['30604', 'cats', 'OUTGOING', r'..\documents\toX.txt'],
                      ['30605', 'cats', 'AT_OUT3', r'..\documents\toY.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'park', 'from_constituents', 'file4.txt')]
        self.assertEqual(expected, result, "Problem with test for folders empty, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['cats', r'..\documents\file1.txt'],
                    ['dogs', r'..\documents\file2.txt'],
                    ['cats', r'..\documents\toX.txt'],
                    ['cats', r'..\documents\toY.txt']]
        self.assertEqual(expected, result, "Problem with test for folders empty, log")

        # Verifies folders without a file are not still present.
        result = [os.path.exists(os.path.join(self.by_topic, 'cats')),
                  os.path.exists(os.path.join(self.by_topic, 'dogs'))]
        expected = [False, False]
        self.assertEqual(expected, result, "Problem with test for folders empty, folders not deleted")

    def test_folder_name_error(self):
        """Test for when a topic contains a character that cannot be in a folder name"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'A\\BC/DE:***', 'INCOMING', r'..\documents\ima\file1.txt'],
                      ['30601', 'Ga?', 'OUTGOMING', r'..\documents\indivletters\toB.txt'],
                      ['30602', '"H"', 'AT_IN1', r'..\documents\objects\file3.txt'],
                      ['30603', '<pa|rk>', 'OUT_IN2', r'..\documents\indivletters\toC.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'A_BC_DE____', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Ga_', 'to_constituents', 'toB.txt'),
                    os.path.join(self.by_topic, '_H_', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, '_pa_rk_', 'to_constituents', 'toC.txt')]
        self.assertEqual(expected, result, "Problem with test for folder name error")

    def test_folder_name_trailing(self):
        """Test for when a topic ends with a space or period, which cannot be in the folder name"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', ' apple.com', 'INCOMING', r'..\documents\ima\file1.txt'],
                      ['30601', 'cat ', 'OUTGOING', r'..\documents\indivletters\toA.txt'],
                      ['30601', 'dog', 'INCOMING', r'..\documents\objects\file2.txt'],
                      ['30602', 'dog.', 'OUT_IN1', r'..\documents\indivletters\toC.txt'],
                      ['30603', 'park and rec. ', 'AT_IN2', r'..\documents\objects\file4.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, ' apple.com', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'cat', 'to_constituents', 'toA.txt'),
                    os.path.join(self.by_topic, 'dog', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'dog', 'to_constituents', 'toC.txt'),
                    os.path.join(self.by_topic, 'park and rec', 'from_constituents', 'file4.txt')]
        self.assertEqual(expected, result, "Problem with test for folder name trailing")

    def test_unique(self):
        """Test for when topic and file is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', 'INCOMING', r'..\documents\ima\file1.txt'],
                      ['30601', 'dogs', 'INCOMING', r'..\documents\objects\file2.txt'],
                      ['30602', 'farm', 'AT_IN1', r'..\documents\objects\file3.txt'],
                      ['30603', 'park', 'AT_IN2', r'..\documents\objects\file4.txt'],
                      ['30604', 'tree', 'OUTGOING', r'..\documents\indivletters\toA.txt'],
                      ['30605', 'zoo', 'AT_OUT2', r'..\documents\indivletters\toB.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cats', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'dogs', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'park', 'from_constituents', 'file4.txt'),
                    os.path.join(self.by_topic, 'tree', 'to_constituents', 'toA.txt'),
                    os.path.join(self.by_topic, 'zoo', 'to_constituents', 'toB.txt')]
        self.assertEqual(expected, result, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
