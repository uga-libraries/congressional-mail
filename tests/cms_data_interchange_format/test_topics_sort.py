import numpy as np
import os
import pandas as pd
import shutil
import unittest
from cms_data_interchange_format import topics_sort
from test_script import make_dir_list


def make_df(row_list):
    """Make a dataframe from a list of rows with consistent columns, used for test input"""
    df = pd.DataFrame(row_list, columns=['zip_code', 'code_description', 'correspondence_document_name'])
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
        self.by_topic = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'Correspondence_by_Topic')
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'cms_export')
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
        df = make_df([['30600', np.nan, r'in-email\file1.txt'],
                      ['30601', 'dogs', np.nan],
                      ['30602', 'farm', r'in-email\file3.txt'],
                      ['30603', np.nan, np.nan],
                      ['30604', np.nan, r'out-custom\Brown.txt'],
                      ['30605', 'farm', r'out-custom\Doe.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'farm'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents', 'Doe.txt')]
        self.assertEqual(expected, result, "Problem with test for blank")

    def test_duplicate_file(self):
        """Test for when a file is in the metadata with the same topic more than once"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', r'in-email\file1.txt'],
                      ['30601', 'dogs', r'in-email\file2.txt'],
                      ['30602', 'dogs', r'in-email\file2.txt'],
                      ['30603', 'dogs', r'in-email\file2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cats'),
                    os.path.join(self.by_topic, 'dogs'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'dogs', 'from_constituents'),
                    os.path.join(self.by_topic, 'dogs', 'from_constituents', 'file2.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate_file")

    def test_duplicate_topic(self):
        """Test for when a topic is in the metadata more than once"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', r'in-email\file1.txt'],
                      ['30601', 'dogs', r'in-email\file2.txt'],
                      ['30602', 'cats', r'in-email\file3.txt'],
                      ['30603', 'cats', r'in-email\file4.txt'],
                      ['30604', 'cats', r'out-custom\Jones.txt'],
                      ['30605', 'dogs', r'forms\Oppose.txt'],
                      ['30606', 'dogs', r'forms\Support.txt'],
                      ['30607', 'cats', r'attachments\scan1.txt'],
                      ['30608', 'dogs', r'attachments\scan2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cats'),
                    os.path.join(self.by_topic, 'dogs'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents'),
                    os.path.join(self.by_topic, 'cats', 'to_constituents'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'file4.txt'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'scan1.txt'),
                    os.path.join(self.by_topic, 'cats', 'to_constituents', 'Jones.txt'),
                    os.path.join(self.by_topic, 'dogs', 'from_constituents'),
                    os.path.join(self.by_topic, 'dogs', 'to_constituents'),
                    os.path.join(self.by_topic, 'dogs', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'dogs', 'from_constituents', 'scan2.txt'),
                    os.path.join(self.by_topic, 'dogs', 'to_constituents', 'Oppose.txt'),
                    os.path.join(self.by_topic, 'dogs', 'to_constituents', 'Support.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate_topic")

    def test_filenotfounderror(self):
        """Test for when a file is in the metadata but not the directory"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', r'in-email\file1.txt'],
                      ['30601', 'dogs', r'new\in-email\file2.txt'],
                      ['30602', 'farm', r'in-email\file3.txt'],
                      ['30603', 'park', r'\doc\in-email\file4.txt'],
                      ['30604', 'cats', r'out-custom\Brown.txt'],
                      ['30605', 'dogs', r'missing\out-custom\Doe.txt'],
                      ['30606', 'park', r'out-custom\missing.txt'],
                      ['30607', 'park', r'forms\not_present.txt'],
                      ['30608', 'park', r'attachments\missing.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cats'),
                    os.path.join(self.by_topic, 'farm'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents'),
                    os.path.join(self.by_topic, 'cats', 'to_constituents'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'cats', 'to_constituents', 'Brown.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt')]
        self.assertEqual(expected, result, "Problem with test for filenotfounderror, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['dogs', r'new\in-email\file2.txt'],
                    ['park', r'\doc\in-email\file4.txt'],
                    ['park', r'attachments\missing.txt'],
                    ['dogs', r'missing\out-custom\Doe.txt'],
                    ['park', r'out-custom\missing.txt'],
                    ['park', r'forms\not_present.txt']]
        self.assertEqual(expected, result, "Problem with test for filenotfounderror, log")

    def test_folder_empty(self):
        """Test for when no out files for a topic are in the directory, but some in are"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', r'in-email\file1.txt'],
                      ['30601', 'dogs', r'in-email\new\file2.txt'],
                      ['30604', 'cats', r'missing\out-custom\Doe.txt'],
                      ['30605', 'dogs', r'out-custom\missing.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folder was created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cats'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'file1.txt')]
        self.assertEqual(expected, result, "Problem with test for one folder empty, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['dogs', r'in-email\new\file2.txt'],
                    ['cats', r'missing\out-custom\Doe.txt'],
                    ['dogs', r'out-custom\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for one folder empty, log")

    def test_folders_empty(self):
        """Test for when no files (in or out) for a topic are in the directory and the topic folder is empty"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', r'in-email\file01.txt'],
                      ['30601', 'dogs', r'in-email\new\file2.txt'],
                      ['30602', 'farm', r'in-email\file3.txt'],
                      ['30603', 'park', r'in-email\file4.txt'],
                      ['30604', 'dogs', r'missing\out-custom\Doe.txt'],
                      ['30605', 'park', r'out-custom\missing.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'farm'),
                    os.path.join(self.by_topic, 'park'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'park', 'from_constituents'),
                    os.path.join(self.by_topic, 'park', 'from_constituents', 'file4.txt')]
        self.assertEqual(expected, result, "Problem with test for folders empty, topic folders")

        # Verifies the expected log was created and has the expected contents.
        result = make_log_list()
        expected = [['cats', r'in-email\file01.txt'],
                    ['dogs', r'in-email\new\file2.txt'],
                    ['dogs', r'missing\out-custom\Doe.txt'],
                    ['park', r'out-custom\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for folders empty, log")

    def test_unique(self):
        """Test for when topic and file is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'cats', r'in-email\file1.txt'],
                      ['30601', 'dogs', r'in-email\file2.txt'],
                      ['30602', 'farm', r'out-custom\Doe.txt'],
                      ['30603', 'park', r'out-custom\Jones.txt'],
                      ['30604', 'retire', r'forms\Thanks.txt'],
                      ['30605', 'water', r'attachments\scan1.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'cats'),
                    os.path.join(self.by_topic, 'dogs'),
                    os.path.join(self.by_topic, 'farm'),
                    os.path.join(self.by_topic, 'park'),
                    os.path.join(self.by_topic, 'retire'),
                    os.path.join(self.by_topic, 'weather'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents'),
                    os.path.join(self.by_topic, 'cats', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'dogs', 'from_constituents'),
                    os.path.join(self.by_topic, 'dogs', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents', 'Doe.txt'),
                    os.path.join(self.by_topic, 'park', 'to_constituents'),
                    os.path.join(self.by_topic, 'park', 'to_constituents', 'Jones.txt'),
                    os.path.join(self.by_topic, 'retire', 'to_constituents'),
                    os.path.join(self.by_topic, 'retire', 'to_constituents', 'Thanks.txt'),
                    os.path.join(self.by_topic, 'water', 'from_constituents'),
                    os.path.join(self.by_topic, 'water', 'from_constituents', 'scan1.txt')]
        self.assertEqual(expected, result, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
