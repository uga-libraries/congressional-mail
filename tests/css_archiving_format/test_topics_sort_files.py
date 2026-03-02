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
    column_names = ['zip', 'in_topic', 'in_document_name', 'out_topic',
                    'out_document_name', 'out_document_name_present']
    df = pd.DataFrame(row_list, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variables and directories used by every test, which are usually from topics_sort()"""
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort_files', 'name_export')
        self.output_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort_files', 'output')
        self.folder_path = os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents')
        os.makedirs(self.folder_path)

    def tearDown(self):
        """Delete the script outputs, if made"""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_blank(self):
        """Test for when the document column has some blanks that should be skipped"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Ag', 'a.txt', 'farming', r'..\documents\BlobExport\forms\ag.txt', 'TBD'],
                      ['30601', 'Ag', 'b.txt', 'farming', np.nan, 'TBD'],
                      ['30602', 'Ag', 'c.txt', 'farming', r'..\documents\BlobExport\forms\missing.txt', 'TBD'],
                      ['30603', 'Ag', 'd.txt', 'farming', np.nan, 'TBD'],
                      ['30604', np.nan, np.nan, np.nan, np.nan, 'TBD']])
        df_topic = topics_sort_files(df, 'out_document_name', self.input_dir, self.output_dir, self.folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['zip', 'in_topic', 'in_document_name', 'out_topic', 'out_document_name',
                     'out_document_name_present'],
                    ['30600', 'Ag', 'a.txt', 'farming', r'..\documents\BlobExport\forms\ag.txt', True],
                    ['30601', 'Ag', 'b.txt', 'farming', 'BLANK', 'TBD'],
                    ['30602', 'Ag', 'c.txt', 'farming', r'..\documents\BlobExport\forms\missing.txt', False],
                    ['30603', 'Ag', 'd.txt', 'farming', 'BLANK', 'TBD'],
                    ['30604', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'TBD']]
        self.assertEqual(expected, result, "Problem with test for blank, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents', 'ag.txt')]
        self.assertEqual(expected, result, "Problem with test for blank, directory")

        # Verifies topics_sort_file_not_found.csv has the correct contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['farming', r'..\documents\BlobExport\forms\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for blank, not_found")

    def test_duplicate(self):
        """Test for when the document column has some files more than once"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Ag', 'a.txt', 'farming', r'..\documents\BlobExport\objects\001.txt', 'TBD'],
                      ['30601', 'Ag', 'b.txt', 'farming', r'..\documents\BlobExport\forms\ag.txt', 'TBD'],
                      ['30602', 'Ag', 'c.txt', 'farming', r'..\documents\BlobExport\forms\missing.txt', 'TBD'],
                      ['30603', 'Ag', 'd.txt', 'farming', r'..\documents\BlobExport\objects\001.txt', 'TBD'],
                      ['30604', 'Ag', 'e.txt', 'farming', r'..\documents\BlobExport\objects\001.txt', 'TBD'],
                      ['30605', 'Ag', 'f.txt', 'farming', r'..\documents\BlobExport\objects\missing.txt', 'TBD'],
                      ['30606', 'Ag', 'g.txt', 'farming', r'..\documents\BlobExport\forms\ag.txt', 'TBD'],
                      ['30607', 'Ag', 'h.txt', 'farming', r'..\documents\BlobExport\objects\001.txt', 'TBD'],
                      ['30608', 'Ag', 'i.txt', 'farming', r'..\documents\BlobExport\objects\missing.txt', 'TBD']])
        df_topic = topics_sort_files(df, 'out_document_name', self.input_dir, self.output_dir, self.folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['zip', 'in_topic', 'in_document_name', 'out_topic', 'out_document_name',
                     'out_document_name_present'],
                    ['30600', 'Ag', 'a.txt', 'farming', r'..\documents\BlobExport\objects\001.txt', True],
                    ['30601', 'Ag', 'b.txt', 'farming', r'..\documents\BlobExport\forms\ag.txt', True],
                    ['30602', 'Ag', 'c.txt', 'farming', r'..\documents\BlobExport\forms\missing.txt', False],
                    ['30603', 'Ag', 'd.txt', 'farming', r'..\documents\BlobExport\objects\001.txt', True],
                    ['30604', 'Ag', 'e.txt', 'farming', r'..\documents\BlobExport\objects\001.txt', True],
                    ['30605', 'Ag', 'f.txt', 'farming', r'..\documents\BlobExport\objects\missing.txt', False],
                    ['30606', 'Ag', 'g.txt', 'farming', r'..\documents\BlobExport\forms\ag.txt', True],
                    ['30607', 'Ag', 'h.txt', 'farming', r'..\documents\BlobExport\objects\001.txt', True],
                    ['30608', 'Ag', 'i.txt', 'farming', r'..\documents\BlobExport\objects\missing.txt', False]]
        self.assertEqual(expected, result, "Problem with test for blank, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents', '001.txt'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents', 'ag.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate, directory")

        # Verifies topics_sort_file_not_found.csv has the correct contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['farming', r'..\documents\BlobExport\forms\missing.txt'],
                    ['farming', r'..\documents\BlobExport\objects\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for duplicate, not_found")

    def test_unique(self):
        """Test for when each topic and file combination is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'Ag', 'a.txt', 'farming', r'..\documents\BlobExport\forms\bees.txt', 'TBD'],
                      ['30601', 'Ag', 'b.txt', 'farming', r'..\documents\BlobExport\forms\ag.txt', 'TBD'],
                      ['30602', 'Ag', 'c.txt', 'farming', r'..\documents\BlobExport\forms\missing.txt', 'TBD'],
                      ['30603', 'Ag', 'd.txt', 'farming', r'..\documents\BlobExport\001.txt', 'TBD'],
                      ['30604', 'Ag', 'e.txt', 'farming', r'..\documents\BlobExport\objects\001.txt', 'TBD'],
                      ['30605', 'Ag', 'f.txt', 'farming', r'..\documents\BlobExport\objects\002.txt', 'TBD'],
                      ['30606', 'Ag', 'g.txt', 'farming', r'..\documents\BlobExport\objects\missing.txt', 'TBD']])
        df_topic = topics_sort_files(df, 'out_document_name', self.input_dir, self.output_dir, self.folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['zip', 'in_topic', 'in_document_name', 'out_topic', 'out_document_name',
                     'out_document_name_present'],
                    ['30600', 'Ag', 'a.txt', 'farming', r'..\documents\BlobExport\forms\bees.txt', True],
                    ['30601', 'Ag', 'b.txt', 'farming', r'..\documents\BlobExport\forms\ag.txt', True],
                    ['30602', 'Ag', 'c.txt', 'farming', r'..\documents\BlobExport\forms\missing.txt', False],
                    ['30603', 'Ag', 'd.txt', 'farming', r'..\documents\BlobExport\001.txt', False],
                    ['30604', 'Ag', 'e.txt', 'farming', r'..\documents\BlobExport\objects\001.txt', True],
                    ['30605', 'Ag', 'f.txt', 'farming', r'..\documents\BlobExport\objects\002.txt', True],
                    ['30606', 'Ag', 'g.txt', 'farming', r'..\documents\BlobExport\objects\missing.txt', False]]
        self.assertEqual(expected, result, "Problem with test for blank, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents', '001.txt'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents', '002.txt'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents', 'ag.txt'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'farming', 'to_constituents', 'bees.txt')]
        self.assertEqual(expected, result, "Problem with test for unique, directory")

        # Verifies topics_sort_file_not_found.csv has the correct contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['farming', r'..\documents\BlobExport\forms\missing.txt'],
                    ['farming', r'..\documents\BlobExport\001.txt'],
                    ['farming', r'..\documents\BlobExport\objects\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for unique, not_found")


if __name__ == '__main__':
    unittest.main()
