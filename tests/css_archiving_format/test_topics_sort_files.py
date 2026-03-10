import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import topics_sort_files
from test_read_metadata import df_to_list
from test_script import csv_to_list, make_dir_list


def make_df(row_list):
    """Make a dataframe from a list of rows with consistent columns, used for test input"""
    column_names = ['zip', 'out_topic', 'out_document_name', 'out_document_name_present', 'out_document_name_split']
    df = pd.DataFrame(row_list, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variables and directories used by every test, which are usually from topics_sort()"""
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort_files', 'name_export')
        self.output_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort_files', 'output')
        self.by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        self.folder_path = os.path.join(self.output_dir, 'correspondence_by_topic', 'ag', 'to_constituents')
        os.makedirs(self.folder_path)

    def tearDown(self):
        """Delete the script outputs, if made"""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_blank(self):
        """Test for when the document column has some blanks that should be skipped"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'ag', '..\\documents\\BlobExport\\forms\\ag.txt', 'TBD', 
                       '..\\documents\\BlobExport\\forms\\ag.txt'],
                      ['30601', 'ag', np.nan, 'TBD', np.nan],
                      ['30602', 'ag', '..\\documents\\BlobExport\\forms\\missing.txt', 'TBD',
                       '..\\documents\\BlobExport\\forms\\missing.txt'],
                      ['30603', 'ag', np.nan, 'TBD', np.nan],
                      ['30604', np.nan, np.nan, 'TBD', np.nan]])
        df_topic = topics_sort_files(df, 'out_document_name_split', self.input_dir, self.output_dir, self.folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['zip', 'out_topic', 'out_document_name', 'out_document_name_present', 'out_document_name_split'],
                    ['30600', 'ag', '..\\documents\\BlobExport\\forms\\ag.txt', True,
                     '..\\documents\\BlobExport\\forms\\ag.txt'],
                    ['30601', 'ag', 'BLANK', 'TBD', 'BLANK'],
                    ['30602', 'ag', '..\\documents\\BlobExport\\forms\\missing.txt', False,
                     '..\\documents\\BlobExport\\forms\\missing.txt'],
                    ['30603', 'ag', 'BLANK', 'TBD', 'BLANK'],
                    ['30604', 'BLANK', 'BLANK', 'TBD', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for blank, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.by_topic, 'ag'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'forms'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'forms', 'ag.txt')]
        self.assertEqual(expected, result, "Problem with test for blank, directory")

        # Verifies topics_sort_file_not_found.csv has the correct contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['ag', '..\\documents\\BlobExport\\forms\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for blank, not_found")

    def test_delimited(self):
        """Test for when the document column has more than one file"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'ag',
                       '..\\documents\\BlobExport\\objects\\001.txt^..\\documents\\BlobExport\\forms\\ag.txt',
                       'TBD', '..\\documents\\BlobExport\\objects\\001.txt'],
                      ['30600', 'ag',
                       '..\\documents\\BlobExport\\objects\\001.txt^..\\documents\\BlobExport\\forms\\ag.txt',
                       'TBD', '..\\documents\\BlobExport\\forms\\ag.txt'],
                      ['30601', 'ag',
                       'e:\\emailobj\\missing.txt^..\\documents\\BlobExport\\forms\\ag.txt',
                       'TBD', 'e:\\emailobj\\missing.txt'],
                      ['30601', 'ag',
                       'e:\\emailobj\\missing.txt^..\\documents\\BlobExport\\forms\\ag.txt',
                       'TBD', '..\\documents\\BlobExport\\forms\\ag.txt']])
        df_topic = topics_sort_files(df, 'out_document_name_split', self.input_dir, self.output_dir, self.folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['zip', 'out_topic', 'out_document_name', 'out_document_name_present', 'out_document_name_split'],
                    ['30600', 'ag',
                     '..\\documents\\BlobExport\\objects\\001.txt^..\\documents\\BlobExport\\forms\\ag.txt',
                     True, '..\\documents\\BlobExport\\objects\\001.txt'],
                    ['30600', 'ag',
                     '..\\documents\\BlobExport\\objects\\001.txt^..\\documents\\BlobExport\\forms\\ag.txt',
                     True, '..\\documents\\BlobExport\\forms\\ag.txt'],
                    ['30601', 'ag',
                     'e:\\emailobj\\missing.txt^..\\documents\\BlobExport\\forms\\ag.txt',
                     False, 'e:\\emailobj\\missing.txt'],
                    ['30601', 'ag',
                     'e:\\emailobj\\missing.txt^..\\documents\\BlobExport\\forms\\ag.txt',
                     True, '..\\documents\\BlobExport\\forms\\ag.txt']]
        self.assertEqual(expected, result, "Problem with test for duplicate, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.by_topic, 'ag'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'forms'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'objects'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'forms', 'ag.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'objects', '001.txt')]
        self.assertEqual(expected, result, "Problem with test for delimited, directory")

        # Verifies topics_sort_file_not_found.csv has the correct contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['ag', 'e:\\emailobj\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for delimited, not_found")
        
    def test_duplicate(self):
        """Test for when the document column has some files more than once"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'ag', '..\\documents\\BlobExport\\objects\\001.txt', 'TBD',
                       '..\\documents\\BlobExport\\objects\\001.txt'],
                      ['30601', 'ag', '..\\documents\\BlobExport\\forms\\ag.txt', 'TBD',
                       '..\\documents\\BlobExport\\forms\\ag.txt'],
                      ['30602', 'ag', '..\\documents\\BlobExport\\forms\\missing.txt', 'TBD',
                       '..\\documents\\BlobExport\\forms\\missing.txt'],
                      ['30603', 'ag', '..\\documents\\BlobExport\\objects\\001.txt', 'TBD',
                       '..\\documents\\BlobExport\\objects\\001.txt'],
                      ['30604', 'ag', '..\\documents\\BlobExport\\objects\\001.txt', 'TBD',
                       '..\\documents\\BlobExport\\objects\\001.txt'],
                      ['30605', 'ag', '..\\documents\\BlobExport\\objects\\missing.txt', 'TBD',
                       '..\\documents\\BlobExport\\objects\\missing.txt'],
                      ['30606', 'ag', '..\\documents\\BlobExport\\forms\\ag.txt', 'TBD',
                       '..\\documents\\BlobExport\\forms\\ag.txt'],
                      ['30607', 'ag', '..\\documents\\BlobExport\\objects\\001.txt', 'TBD',
                       '..\\documents\\BlobExport\\objects\\001.txt'],
                      ['30608', 'ag', '..\\documents\\BlobExport\\objects\\missing.txt', 'TBD',
                       '..\\documents\\BlobExport\\objects\\missing.txt']])
        df_topic = topics_sort_files(df, 'out_document_name_split', self.input_dir, self.output_dir, self.folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['zip', 'out_topic', 'out_document_name', 'out_document_name_present', 'out_document_name_split'],
                    ['30600', 'ag', '..\\documents\\BlobExport\\objects\\001.txt', True,
                     '..\\documents\\BlobExport\\objects\\001.txt'],
                    ['30601', 'ag', '..\\documents\\BlobExport\\forms\\ag.txt', True,
                     '..\\documents\\BlobExport\\forms\\ag.txt'],
                    ['30602', 'ag', '..\\documents\\BlobExport\\forms\\missing.txt', False,
                     '..\\documents\\BlobExport\\forms\\missing.txt'],
                    ['30603', 'ag', '..\\documents\\BlobExport\\objects\\001.txt', True,
                     '..\\documents\\BlobExport\\objects\\001.txt'],
                    ['30604', 'ag', '..\\documents\\BlobExport\\objects\\001.txt', True,
                     '..\\documents\\BlobExport\\objects\\001.txt'],
                    ['30605', 'ag', '..\\documents\\BlobExport\\objects\\missing.txt', False,
                     '..\\documents\\BlobExport\\objects\\missing.txt'],
                    ['30606', 'ag', '..\\documents\\BlobExport\\forms\\ag.txt', True,
                     '..\\documents\\BlobExport\\forms\\ag.txt'],
                    ['30607', 'ag', '..\\documents\\BlobExport\\objects\\001.txt', True,
                     '..\\documents\\BlobExport\\objects\\001.txt'],
                    ['30608', 'ag', '..\\documents\\BlobExport\\objects\\missing.txt', False,
                     '..\\documents\\BlobExport\\objects\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for duplicate, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.by_topic, 'ag'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'forms'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'objects'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'forms', 'ag.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'objects', '001.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate, directory")

        # Verifies topics_sort_file_not_found.csv has the correct contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['ag', '..\\documents\\BlobExport\\forms\\missing.txt'],
                    ['ag', '..\\documents\\BlobExport\\objects\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for duplicate, not_found")

    def test_unique(self):
        """Test for when each topic and file combination is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'ag', '..\\documents\\BlobExport\\forms\\bees.txt', 'TBD',
                       '..\\documents\\BlobExport\\forms\\bees.txt'],
                      ['30601', 'ag', '..\\documents\\BlobExport\\forms\\ag.txt', 'TBD',
                       '..\\documents\\BlobExport\\forms\\ag.txt'],
                      ['30602', 'ag', '..\\documents\\BlobExport\\forms\\missing.txt', 'TBD',
                       '..\\documents\\BlobExport\\forms\\missing.txt'],
                      ['30603', 'ag', '..\\documents\\BlobExport\\001.txt', 'TBD',
                       '..\\documents\\BlobExport\\001.txt'],
                      ['30604', 'ag', '..\\documents\\BlobExport\\objects\\001.txt', 'TBD',
                       '..\\documents\\BlobExport\\objects\\001.txt'],
                      ['30605', 'ag', '..\\documents\\BlobExport\\objects\\002.txt', 'TBD',
                       '..\\documents\\BlobExport\\objects\\002.txt'],
                      ['30606', 'ag', '..\\documents\\BlobExport\\objects\\missing.txt', 'TBD',
                       '..\\documents\\BlobExport\\objects\\missing.txt']])
        df_topic = topics_sort_files(df, 'out_document_name_split', self.input_dir, self.output_dir, self.folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['zip', 'out_topic', 'out_document_name', 'out_document_name_present', 'out_document_name_split'],
                    ['30600', 'ag', '..\\documents\\BlobExport\\forms\\bees.txt', True, 
                     '..\\documents\\BlobExport\\forms\\bees.txt'],
                    ['30601', 'ag', '..\\documents\\BlobExport\\forms\\ag.txt', True,
                     '..\\documents\\BlobExport\\forms\\ag.txt'],
                    ['30602', 'ag', '..\\documents\\BlobExport\\forms\\missing.txt', False,
                     '..\\documents\\BlobExport\\forms\\missing.txt'],
                    ['30603', 'ag', '..\\documents\\BlobExport\\001.txt', False,
                     '..\\documents\\BlobExport\\001.txt'],
                    ['30604', 'ag', '..\\documents\\BlobExport\\objects\\001.txt', True,
                     '..\\documents\\BlobExport\\objects\\001.txt'],
                    ['30605', 'ag', '..\\documents\\BlobExport\\objects\\002.txt', True,
                     '..\\documents\\BlobExport\\objects\\002.txt'],
                    ['30606', 'ag', '..\\documents\\BlobExport\\objects\\missing.txt', False,
                     '..\\documents\\BlobExport\\objects\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for blank, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.by_topic, 'ag'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'forms'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'objects'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'forms', 'ag.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'forms', 'bees.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'objects', '001.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'objects', '002.txt')]
        self.assertEqual(expected, result, "Problem with test for unique, directory")

        # Verifies topics_sort_file_not_found.csv has the correct contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['ag', '..\\documents\\BlobExport\\forms\\missing.txt'],
                    ['ag', '..\\documents\\BlobExport\\001.txt'],
                    ['ag', '..\\documents\\BlobExport\\objects\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for unique, not_found")


if __name__ == '__main__':
    unittest.main()
