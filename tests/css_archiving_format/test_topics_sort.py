"""
Tests for the function topics_sort(), which organizes a copy of the letters by topic.
To simplify input, tests use dataframes with only some of the columns present in a real export.
"""
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import topics_sort


def make_df(row_list):
    """Make a dataframe from a list of rows with consistent columns, used for test input"""
    df = pd.DataFrame(row_list, columns=['zip', 'in_topic', 'in_document_name', 'out_topic', 'out_document_name'])
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
        df = make_df([['30600', 'nan', r'..\documents\BlobExport\objects\file3.txt',
                       'nan', r'..\documents\BlobExport\responses\answer1.txt'],
                      ['30601', 'Agriculture', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30602', 'Agriculture^Peanuts', r'..\documents\BlobExport\objects\file2.txt',
                       'Peanuts', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30603', 'Agriculture^Peanuts', 'nan', 'Peanuts', 'nan'],
                      ['30604', 'nan', 'nan', 'nan', 'nan']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'to_constituents', 'ag.txt')]
        self.assertEqual(expected, result, "Problem with test for blank")

    def test_duplicate_file(self):
        """Test for when a file is in the metadata with the same topic more than once"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture^Peanuts', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30602', 'Small Business', r'..\documents\BlobExport\objects\file3.txt',
                       'Small Business', r'..\documents\BlobExport\responses\ag.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'to_constituents', 'ag.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate_file")

    def test_duplicate_topic(self):
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

    def test_filenotfounderror(self):
        """Test for when a file is in the metadata but not the directory"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\objects\file_missing.txt',
                       'Agriculture^Peanuts', r'..\documents\BlobExport\responses\answer_missing.txt'],
                      ['30602', 'Peanuts', r'..\documents\BlobExport\objects\file2.txt',
                       'Peanuts', r'..\documents\BlobExport\responses\answer2_missing.txt'],
                      ['30603', 'Peanuts', r'..\documents\BlobExport\objects\folder_missing\file3.txt',
                       'Peanuts', r'..\documents\BlobExport\responses\folder_missing\ag.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'from_constituents', 'file2.txt')]
        self.assertEqual(expected, result, "Problem with test for filenotfounderror, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['Agriculture', r'..\documents\BlobExport\objects\file_missing.txt'],
                    ['Peanuts', r'..\documents\BlobExport\objects\file_missing.txt'],
                    ['Peanuts', r'..\documents\BlobExport\objects\folder_missing\file3.txt'],
                    ['Agriculture', r'..\documents\BlobExport\responses\answer_missing.txt'],
                    ['Peanuts', r'..\documents\BlobExport\responses\answer_missing.txt'],
                    ['Peanuts', r'..\documents\BlobExport\responses\answer2_missing.txt'],
                    ['Peanuts', r'..\documents\BlobExport\responses\folder_missing\ag.txt']]
        self.assertEqual(expected, result, "Problem with test for filenotfounderror, log")

    def test_folder_empty(self):
        """Test for when no out files for a topic are in the directory, but some in are"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\missing.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\objects\missing\file2.txt',
                       'Agriculture^Peanuts', r'..\documents\BlobExport\responses\missing.txt'],
                      ['30602', 'Peanuts', r'..\documents\BlobExport\objects\missing\file3.txt',
                       'Peanuts', r'..\documents\BlobExport\responses\missing.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the empty topic folder and empty from_constituents folder are not in Correspondence_by_Topic:
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

    def test_folders_empty(self):
        """Test for when no files (in or out) for a topic are in the directory and the topic folder is empty"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\objects\missing\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\missing.txt'],
                      ['30601', 'Agriculture^Peanuts', r'..\documents\BlobExport\objects\missing\file2.txt',
                       'Agriculture^Peanuts', r'..\documents\BlobExport\responses\missing.txt'],
                      ['30602', 'Peanuts', r'..\documents\BlobExport\objects\missing\file3.txt',
                       'Peanuts', r'..\documents\BlobExport\responses\missing.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the empty topic folders are not in Correspondence_by_Topic:
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

    def test_folder_name_error(self):
        """Test for when a topic contains a character that cannot be in a folder name"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'A\\B^C/D^E:F^***', r'..\documents\BlobExport\objects\file1.txt',
                       'A\\B^C/D^E:F^***', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30601', 'G?^"H"', r'..\documents\BlobExport\objects\file2.txt',
                       'G?^"H"', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30602', '<I|J>', r'..\documents\BlobExport\objects\file3.txt',
                       '<I|J>', r'..\documents\BlobExport\responses\ag.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'A_B', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'A_B', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'C_D', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'C_D', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'E_F', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'E_F', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'G_', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'G_', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, '_H_', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, '_H_', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, '_I_J_', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, '_I_J_', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, '___', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, '___', 'to_constituents', 'ag.txt'),]
        self.assertEqual(expected, result, "Problem with test for folder name error")

    def test_folder_name_trailing(self):
        """Test for when a topic ends with a space or period, which cannot be in the folder name"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'park and rec. ', r'..\documents\BlobExport\objects\file1.txt',
                       'park and rec. ', r'..\documents\BlobExport\responses\answer1.txt'],
                      ['30601', 'cat ', r'..\documents\BlobExport\objects\file2.txt',
                       'cat ', r'..\documents\BlobExport\responses\answer2.txt'],
                      ['30601', 'dog. ', r'..\documents\BlobExport\objects\file2.txt',
                       'dog. ', r'..\documents\BlobExport\responses\answer2.txt'],
                      ['30602', 'dog', r'..\documents\BlobExport\objects\file3.txt',
                       'dog', r'..\documents\BlobExport\responses\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cat', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'cat', 'to_constituents', 'answer2.txt'),
                    os.path.join(self.by_topic, 'dog', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'dog', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'dog', 'to_constituents', 'answer2.txt'),
                    os.path.join(self.by_topic, 'park and rec', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'park and rec', 'to_constituents', 'answer1.txt'),]
        self.assertEqual(expected, result, "Problem with test for folder name trailing")

    def test_multiple_doc(self):
        """Test for when a row has multiple documents (joined by ^)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture^Farm',
                       '..\\documents\\BlobExport\\objects\\file1.txt^..\\documents\\BlobExport\\objects\\file2.txt',
                       'Agriculture',
                       '..\\documents\\BlobExport\\responses\\ag.txt^..\\documents\\BlobExport\\responses\\answer1.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'Farm', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Farm', 'from_constituents', 'file2.txt')]
        self.assertEqual(expected, result, "Problem with test for multiple doc")

    def test_multiple_topic(self):
        """Test for when a row has multiple topics (joined by ^)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30601', 'Farm^Peanuts', r'..\documents\BlobExport\objects\file2.txt',
                       'Farm^Peanuts', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30602', 'Admin^Small Business^Tax', r'..\documents\BlobExport\objects\file3.txt',
                       'Admin^Small Business^Tax', r'..\documents\BlobExport\responses\answer1.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Admin', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Admin', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Farm', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'Farm', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'Tax', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'to_constituents', 'answer1.txt')]
        self.assertEqual(expected, result, "Problem with test for multiple topic")

    def test_unique(self):
        """Test for when each topic and file is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Agriculture', r'..\documents\BlobExport\objects\file1.txt',
                       'Agriculture', r'..\documents\BlobExport\responses\ag.txt'],
                      ['30601', 'Peanuts', r'..\documents\BlobExport\objects\file2.txt',
                       'Peanuts', r'..\documents\BlobExport\responses\answer1.txt'],
                      ['30602', 'Small Business', r'..\documents\BlobExport\objects\file3.txt',
                       'Small Business', r'..\documents\BlobExport\responses\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'Agriculture', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'Agriculture', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'Peanuts', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'to_constituents', 'answer2.txt')]
        self.assertEqual(expected, result, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
