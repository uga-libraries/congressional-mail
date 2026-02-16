import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import topics_sort
from test_script import csv_to_list, make_dir_list


def make_df(rows):
    """Make a df for test input with all columns in the export, where rows just has the values that change"""
    full_rows = []
    for row in rows:
        new_row = ['*', '*', row[0], '*', '*', '*', '*', '*', row[1], row[2], '*', '*', '*', '*', row[3], row[4]]
        full_rows.append(new_row)
    columns = ['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
               'in_document_name', 'out_id', 'out_type', 'out_method', 'out_date', 'out_topic', 'out_document_name']
    df = pd.DataFrame(full_rows, columns=columns)
    return df


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variables and output_dir directory used by every test"""
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'css_export')
        self.output_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'access_copy')
        os.mkdir(self.output_dir)
        self.by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')

    def tearDown(self):
        """Delete the output_dir and all its contents, if made"""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_doc_both(self):
        """Test for when in_document_name and out_document_name have paths matching the export"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'ag', '..\\documents\\BlobExport\\objects\\file1.txt',
                       'ag^farm', '..\\documents\\BlobExport\\responses\\ag.txt'],
                      ['30602', 'ag^farm', '..\\documents\\BlobExport\\objects\\file2.txt',
                       'ag', '..\\documents\\BlobExport\\responses\\ag.txt'],
                      ['30603', 'farm', '..\\documents\\BlobExport\\objects\\file3.txt',
                       'farm', '..\\documents\\BlobExport\\responses\\farm_missing.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies correspondence_by_topic has the expected contents:
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.by_topic, 'ag'),
                    os.path.join(self.by_topic, 'farm'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents'),
                    os.path.join(self.by_topic, 'ag', 'ag_description.csv'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents'),
                    os.path.join(self.by_topic, 'farm', 'farm_description.csv'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents', 'ag.txt')]
        self.assertEqual(expected, result, "Problem with test for doc_both, directory")

        # Verifies the deletion log has the expected contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['farm', '..\\documents\\BlobExport\\responses\\farm_missing.txt']]
        self.assertEqual(expected, result, "Problem with test for doc_both, deletion log")

        # Verifies ag_description.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'ag', 'ag_description.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*',
                     'ag', '..\\documents\\BlobExport\\objects\\file1.txt', 'True', '*', '*', '*', '*',
                     'ag^farm', '..\\documents\\BlobExport\\responses\\ag.txt', 'True'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'ag^farm', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'ag', '..\\documents\\BlobExport\\responses\\ag.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for doc_both, ag_description.csv")

        # Verifies farm_description.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'farm', 'farm_description.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*',
                     'ag', '..\\documents\\BlobExport\\objects\\file1.txt', 'True', '*', '*', '*', '*',
                     'ag^farm', '..\\documents\\BlobExport\\responses\\ag.txt', 'True'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'ag^farm', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'ag', '..\\documents\\BlobExport\\responses\\ag.txt', 'True'],
                    ['*', '*', '30603', '*', '*', '*', '*', '*',
                     'farm', '..\\documents\\BlobExport\\objects\\file3.txt', 'True', '*', '*', '*', '*',
                     'farm', '..\\documents\\BlobExport\\responses\\farm_missing.txt', 'False']]
        self.assertEqual(expected, result, "Problem with test for doc_both, farm_description.csv")

    def test_doc_in(self):
        """Test for when only in_document_name has paths matching the export"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'ag', '..\\documents\\BlobExport\\objects\\file1.txt', np.nan, np.nan],
                      ['30602', 'ag^farm', '..\\documents\\BlobExport\\objects\\file2.txt', np.nan, np.nan],
                      ['30603', 'farm', '..\\documents\\BlobExport\\objects\\file3.txt', np.nan, np.nan]])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies correspondence_by_topic has the expected contents:
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.by_topic, 'ag'),
                    os.path.join(self.by_topic, 'farm'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents'),
                    os.path.join(self.by_topic, 'ag', 'ag_description.csv'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents'),
                    os.path.join(self.by_topic, 'farm', 'farm_description.csv'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt')]
        self.assertEqual(expected, result, "Problem with test for doc_in, directory")

        # Verifies ag_description.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'ag', 'ag_description.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*',
                     'ag', '..\\documents\\BlobExport\\objects\\file1.txt', 'True', '*', '*', '*', '*',
                     'BLANK', 'BLANK', 'no_path_provided'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'ag^farm', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'BLANK', 'BLANK', 'no_path_provided']]
        self.assertEqual(expected, result, "Problem with test for doc_in, ag_description.csv")

        # Verifies farm_description.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'farm', 'farm_description.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'ag^farm', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'BLANK', 'BLANK', 'no_path_provided'],
                    ['*', '*', '30603', '*', '*', '*', '*', '*',
                     'farm', '..\\documents\\BlobExport\\objects\\file3.txt', 'True', '*', '*', '*', '*',
                     'BLANK', 'BLANK', 'no_path_provided']]
        self.assertEqual(expected, result, "Problem with test for doc_in, farm_description.csv")

    def test_doc_neither(self):
        """Test for when neither in_document_name nor out_document_name have paths matching the export"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'ag', '..\\documents\\BlobExport\\objects\\missing.txt', np.nan, np.nan],
                      ['30602', np.nan, np.nan, 'ag', '..\\documents\\BlobExport\\responses\\missing.txt'],
                      ['30603', 'ag', np.nan, 'ag', '..\\documents\\BlobExport\\responses\\missing.txt'],
                      ['30604', 'farm', '..\\documents\\BlobExport\\objects\\missing.txt',
                       'farm', '..\\documents\\BlobExport\\responses\\missing.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies correspondence_by_topic has the expected contents:
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv')]
        self.assertEqual(expected, result, "Problem with test for doc_neither, directory")

        # Verifies the deletion log has the expected contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['ag', '..\\documents\\BlobExport\\objects\\missing.txt'],
                    ['ag', '..\\documents\\BlobExport\\responses\\missing.txt'],
                    ['farm', '..\\documents\\BlobExport\\objects\\missing.txt'],
                    ['farm', '..\\documents\\BlobExport\\responses\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for doc_neither, deletion log")

    def test_doc_out(self):
        """Test for when only out_document_name has paths matching the export"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', np.nan, np.nan, 'ag', '..\\documents\\BlobExport\\responses\\answer1.txt'],
                      ['30602', np.nan, np.nan, 'ag^farm', '..\\documents\\BlobExport\\responses\\ag.txt'],
                      ['30603', np.nan, np.nan, 'ag', '..\\documents\\BlobExport\\responses\\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies correspondence_by_topic has the expected contents:
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.by_topic, 'ag'),
                    os.path.join(self.by_topic, 'farm'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents'),
                    os.path.join(self.by_topic, 'ag', 'ag_description.csv'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'answer2.txt'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents'),
                    os.path.join(self.by_topic, 'farm', 'farm_description.csv'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents', 'ag.txt')]
        self.assertEqual(expected, result, "Problem with test for doc_out, directory")

        # Verifies ag_description.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'ag', 'ag_description.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*', 'BLANK', 'BLANK', 'no_path_provided',
                     '*', '*', '*', '*', 'ag', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*', 'BLANK', 'BLANK', 'no_path_provided',
                     '*', '*', '*', '*', 'ag^farm', '..\\documents\\BlobExport\\responses\\ag.txt', 'True'],
                    ['*', '*', '30603', '*', '*', '*', '*', '*', 'BLANK', 'BLANK', 'no_path_provided',
                     '*', '*', '*', '*', 'ag', '..\\documents\\BlobExport\\responses\\answer2.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for doc_out, ag_description.csv")

        # Verifies farm_description.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'farm', 'farm_description.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*', 'BLANK', 'BLANK', 'no_path_provided',
                     '*', '*', '*', '*', 'ag^farm', '..\\documents\\BlobExport\\responses\\ag.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for doc_out, farm_description.csv")

    def test_topic_both(self):
        """Test for when a topic is in the metadata more than once, due to topic combinations"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'ag', '..\\documents\\BlobExport\\objects\\file1.txt',
                       'ag', '..\\documents\\BlobExport\\responses\\ag.txt'],
                      ['30601', 'ag^farm', '..\\documents\\BlobExport\\objects\\file2.txt',
                       'Tax', '..\\documents\\BlobExport\\responses\\answer1.txt'],
                      ['30602', 'ag^farm^Tax', '..\\documents\\BlobExport\\objects\\file3.txt',
                       'ag^Tax', '..\\documents\\BlobExport\\responses\\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'ag', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'answer2.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'Tax', 'to_constituents', 'answer2.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate_topic")

    def test_topic_in(self):
        """Test for when each topic and file combination is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'ag', '..\\documents\\BlobExport\\objects\\file1.txt',
                       'ag', '..\\documents\\BlobExport\\responses\\ag.txt'],
                      ['30602', 'farm', '..\\documents\\BlobExport\\objects\\file2.txt',
                       'farm', '..\\documents\\BlobExport\\responses\\answer1.txt'],
                      ['30603', 'Small Business', '..\\documents\\BlobExport\\objects\\file3.txt',
                       'Tax', '..\\documents\\BlobExport\\responses\\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'ag', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'to_constituents', 'answer2.txt')]
        self.assertEqual(expected, result, "Problem with test for unique")

    def test_topic_out(self):
        """Test for when each topic and file combination is unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'ag', '..\\documents\\BlobExport\\objects\\file1.txt',
                       'ag', '..\\documents\\BlobExport\\responses\\ag.txt'],
                      ['30602', 'farm', '..\\documents\\BlobExport\\objects\\file2.txt',
                       'farm', '..\\documents\\BlobExport\\responses\\answer1.txt'],
                      ['30603', 'Small Business', '..\\documents\\BlobExport\\objects\\file3.txt',
                       'Tax', '..\\documents\\BlobExport\\responses\\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.by_topic)
        expected = [os.path.join(self.by_topic, 'ag', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'Small Business', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'Tax', 'to_constituents', 'answer2.txt')]
        self.assertEqual(expected, result, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
