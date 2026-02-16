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
                    os.path.join(self.by_topic, 'ag', 'ag_metadata.csv'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents'),
                    os.path.join(self.by_topic, 'farm', 'farm_metadata.csv'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'farm', 'to_constituents', 'ag.txt')]
        self.assertEqual(expected, result, "Problem with test for doc_both, directory")

        # Verifies the file not found log has the expected contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['farm', '..\\documents\\BlobExport\\responses\\farm_missing.txt']]
        self.assertEqual(expected, result, "Problem with test for doc_both, file not found log")

        # Verifies ag_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'ag', 'ag_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*',
                     'ag', '..\\documents\\BlobExport\\objects\\file1.txt', 'True', '*', '*', '*', '*',
                     'ag^farm', '..\\documents\\BlobExport\\responses\\ag.txt', 'True'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'ag^farm', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'ag', '..\\documents\\BlobExport\\responses\\ag.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for doc_both, ag_metadata.csv")

        # Verifies farm_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'farm', 'farm_metadata.csv'))
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
        self.assertEqual(expected, result, "Problem with test for doc_both, farm_metadata.csv")

    def test_doc_in(self):
        """Test for when only in_document_name has paths matching the export"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'ag.', '..\\documents\\BlobExport\\objects\\file1.txt', np.nan, np.nan],
                      ['30602', 'ag.^farm', '..\\documents\\BlobExport\\objects\\file2.txt', np.nan, np.nan],
                      ['30603', 'farm', '..\\documents\\BlobExport\\objects\\file3.txt', np.nan, np.nan]])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies correspondence_by_topic has the expected contents:
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.by_topic, 'ag'),
                    os.path.join(self.by_topic, 'farm'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents'),
                    os.path.join(self.by_topic, 'ag', 'ag_metadata.csv'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'ag', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents'),
                    os.path.join(self.by_topic, 'farm', 'farm_metadata.csv'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'farm', 'from_constituents', 'file3.txt')]
        self.assertEqual(expected, result, "Problem with test for doc_in, directory")

        # Verifies ag_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'ag', 'ag_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*',
                     'ag.', '..\\documents\\BlobExport\\objects\\file1.txt', 'True', '*', '*', '*', '*',
                     'BLANK', 'BLANK', 'no_path_provided'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'ag.^farm', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'BLANK', 'BLANK', 'no_path_provided']]
        self.assertEqual(expected, result, "Problem with test for doc_in, ag_metadata.csv")

        # Verifies farm_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'farm', 'farm_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'ag.^farm', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'BLANK', 'BLANK', 'no_path_provided'],
                    ['*', '*', '30603', '*', '*', '*', '*', '*',
                     'farm', '..\\documents\\BlobExport\\objects\\file3.txt', 'True', '*', '*', '*', '*',
                     'BLANK', 'BLANK', 'no_path_provided']]
        self.assertEqual(expected, result, "Problem with test for doc_in, farm_metadata.csv")

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

        # Verifies the file not found log has the expected contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['ag', '..\\documents\\BlobExport\\objects\\missing.txt'],
                    ['ag', '..\\documents\\BlobExport\\responses\\missing.txt'],
                    ['farm', '..\\documents\\BlobExport\\objects\\missing.txt'],
                    ['farm', '..\\documents\\BlobExport\\responses\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for doc_neither, file not found log")

    def test_doc_out(self):
        """Test for when only out_document_name has paths matching the export"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', np.nan, np.nan, 'ag', '..\\documents\\BlobExport\\responses\\answer1.txt'],
                      ['30602', np.nan, np.nan, 'ag^farm/family', '..\\documents\\BlobExport\\responses\\ag.txt'],
                      ['30603', np.nan, np.nan, 'ag', '..\\documents\\BlobExport\\responses\\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies correspondence_by_topic has the expected contents:
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.by_topic, 'ag'),
                    os.path.join(self.by_topic, 'farm_family'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents'),
                    os.path.join(self.by_topic, 'ag', 'ag_metadata.csv'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'ag.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'ag', 'to_constituents', 'answer2.txt'),
                    os.path.join(self.by_topic, 'farm_family', 'to_constituents'),
                    os.path.join(self.by_topic, 'farm_family', 'farm_family_metadata.csv'),
                    os.path.join(self.by_topic, 'farm_family', 'to_constituents', 'ag.txt')]
        self.assertEqual(expected, result, "Problem with test for doc_out, directory")

        # Verifies ag_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'ag', 'ag_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*', 'BLANK', 'BLANK', 'no_path_provided',
                     '*', '*', '*', '*', 'ag', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*', 'BLANK', 'BLANK', 'no_path_provided',
                     '*', '*', '*', '*', 'ag^farm/family', '..\\documents\\BlobExport\\responses\\ag.txt', 'True'],
                    ['*', '*', '30603', '*', '*', '*', '*', '*', 'BLANK', 'BLANK', 'no_path_provided',
                     '*', '*', '*', '*', 'ag', '..\\documents\\BlobExport\\responses\\answer2.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for doc_out, ag_metadata.csv")

        # Verifies farm_family_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'farm_family', 'farm_family_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*', 'BLANK', 'BLANK', 'no_path_provided',
                     '*', '*', '*', '*', 'ag^farm/family', '..\\documents\\BlobExport\\responses\\ag.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for doc_out, farm_metadata.csv")

    def test_topic_both(self):
        """Test for when a topic is in both in_topic and out_topic"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'cat', '..\\documents\\BlobExport\\objects\\file1.txt',
                       'pet', '..\\documents\\BlobExport\\responses\\answer1.txt'],
                      ['30602', 'dog', '..\\documents\\BlobExport\\objects\\file2.txt',
                       'dog^pet', '..\\documents\\BlobExport\\responses\\answer1.txt'],
                      ['30603', 'pet', '..\\documents\\BlobExport\\objects\\file3.txt',
                       'cat^dog', '..\\documents\\BlobExport\\responses\\missing.txt'],
                      ['30604', 'pet', '..\\documents\\BlobExport\\objects\\missing.txt',
                       'cat^dog', '..\\documents\\BlobExport\\responses\\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.by_topic, 'cat'),
                    os.path.join(self.by_topic, 'dog'),
                    os.path.join(self.by_topic, 'pet'),
                    os.path.join(self.by_topic, 'cat', 'from_constituents'),
                    os.path.join(self.by_topic, 'cat', 'to_constituents'),
                    os.path.join(self.by_topic, 'cat', 'cat_metadata.csv'),
                    os.path.join(self.by_topic, 'cat', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'cat', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'cat', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'cat', 'to_constituents', 'answer2.txt'),
                    os.path.join(self.by_topic, 'dog', 'from_constituents'),
                    os.path.join(self.by_topic, 'dog', 'to_constituents'),
                    os.path.join(self.by_topic, 'dog', 'dog_metadata.csv'),
                    os.path.join(self.by_topic, 'dog', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'dog', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'dog', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'dog', 'to_constituents', 'answer2.txt'),
                    os.path.join(self.by_topic, 'pet', 'from_constituents'),
                    os.path.join(self.by_topic, 'pet', 'to_constituents'),
                    os.path.join(self.by_topic, 'pet', 'pet_metadata.csv'),
                    os.path.join(self.by_topic, 'pet', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'pet', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'pet', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'pet', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'pet', 'to_constituents', 'answer2.txt')]
        self.assertEqual(expected, result, "Problem with test for topic_both, directory")

        # Verifies the file not found log has the expected contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['cat', '..\\documents\\BlobExport\\objects\\missing.txt'],
                    ['cat', '..\\documents\\BlobExport\\responses\\missing.txt'],
                    ['dog', '..\\documents\\BlobExport\\objects\\missing.txt'],
                    ['dog', '..\\documents\\BlobExport\\responses\\missing.txt'],
                    ['pet', '..\\documents\\BlobExport\\objects\\missing.txt'],
                    ['pet', '..\\documents\\BlobExport\\responses\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for topic_both, file not found log")

        # Verifies cat_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'cat', 'cat_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*',
                     'cat', '..\\documents\\BlobExport\\objects\\file1.txt', 'True', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True'],
                    ['*', '*', '30603', '*', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\objects\\file3.txt', 'True', '*', '*', '*', '*',
                     'cat^dog', '..\\documents\\BlobExport\\responses\\missing.txt', 'False'],
                    ['*', '*', '30604', '*', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\objects\\missing.txt', 'False', '*', '*', '*', '*',
                     'cat^dog', '..\\documents\\BlobExport\\responses\\answer2.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for topic_both, cat_metadata.csv")

        # Verifies dog_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'dog', 'dog_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'dog', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'dog^pet', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True'],
                    ['*', '*', '30603', '*', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\objects\\file3.txt', 'True', '*', '*', '*', '*',
                     'cat^dog', '..\\documents\\BlobExport\\responses\\missing.txt', 'False'],
                    ['*', '*', '30604', '*', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\objects\\missing.txt', 'False', '*', '*', '*', '*',
                     'cat^dog', '..\\documents\\BlobExport\\responses\\answer2.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for topic_both, dog_metadata.csv")

        # Verifies pet_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'pet', 'pet_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*',
                     'cat', '..\\documents\\BlobExport\\objects\\file1.txt', 'True', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'dog', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'dog^pet', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True'],
                    ['*', '*', '30603', '*', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\objects\\file3.txt', 'True', '*', '*', '*', '*',
                     'cat^dog', '..\\documents\\BlobExport\\responses\\missing.txt', 'False'],
                    ['*', '*', '30604', '*', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\objects\\missing.txt', 'False', '*', '*', '*', '*',
                     'cat^dog', '..\\documents\\BlobExport\\responses\\answer2.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for topic_both, pet_metadata.csv")

    def test_topic_one(self):
        """Test for when a topic is either in in_topic or out_topic, but not the other column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'cat', '..\\documents\\BlobExport\\objects\\file1.txt',
                       'pet', '..\\documents\\BlobExport\\responses\\answer1.txt'],
                      ['30602', 'cat^dog', '..\\documents\\BlobExport\\objects\\file2.txt',
                       'pet', '..\\documents\\BlobExport\\responses\\answer1.txt'],
                      ['30603', np.nan, '..\\documents\\BlobExport\\objects\\file3.txt',
                       'pet^toy', '..\\documents\\BlobExport\\responses\\missing.txt'],
                      ['30604', 'cat', '..\\documents\\BlobExport\\objects\\missing.txt',
                       'pet', '..\\documents\\BlobExport\\responses\\answer2.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the expected topic folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.by_topic, 'cat'),
                    os.path.join(self.by_topic, 'dog'),
                    os.path.join(self.by_topic, 'pet'),
                    os.path.join(self.by_topic, 'toy'),
                    os.path.join(self.by_topic, 'cat', 'from_constituents'),
                    os.path.join(self.by_topic, 'cat', 'to_constituents'),
                    os.path.join(self.by_topic, 'cat', 'cat_metadata.csv'),
                    os.path.join(self.by_topic, 'cat', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'cat', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'cat', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'cat', 'to_constituents', 'answer2.txt'),
                    os.path.join(self.by_topic, 'dog', 'from_constituents'),
                    os.path.join(self.by_topic, 'dog', 'to_constituents'),
                    os.path.join(self.by_topic, 'dog', 'dog_metadata.csv'),
                    os.path.join(self.by_topic, 'dog', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'dog', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'pet', 'from_constituents'),
                    os.path.join(self.by_topic, 'pet', 'to_constituents'),
                    os.path.join(self.by_topic, 'pet', 'pet_metadata.csv'),
                    os.path.join(self.by_topic, 'pet', 'from_constituents', 'file1.txt'),
                    os.path.join(self.by_topic, 'pet', 'from_constituents', 'file2.txt'),
                    os.path.join(self.by_topic, 'pet', 'from_constituents', 'file3.txt'),
                    os.path.join(self.by_topic, 'pet', 'to_constituents', 'answer1.txt'),
                    os.path.join(self.by_topic, 'pet', 'to_constituents', 'answer2.txt'),
                    os.path.join(self.by_topic, 'toy', 'from_constituents'),
                    os.path.join(self.by_topic, 'toy', 'toy_metadata.csv'),
                    os.path.join(self.by_topic, 'toy', 'from_constituents', 'file3.txt')]
        self.assertEqual(expected, result, "Problem with test for topic_one, directory")

        # Verifies the file not found log has the expected contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['cat', '..\\documents\\BlobExport\\objects\\missing.txt'],
                    ['pet', '..\\documents\\BlobExport\\objects\\missing.txt'],
                    ['pet', '..\\documents\\BlobExport\\responses\\missing.txt'],
                    ['toy', '..\\documents\\BlobExport\\responses\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for topic_one, file not found log")

        # Verifies cat_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'cat', 'cat_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*',
                     'cat', '..\\documents\\BlobExport\\objects\\file1.txt', 'True', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'cat^dog', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True'],
                    ['*', '*', '30604', '*', '*', '*', '*', '*',
                     'cat', '..\\documents\\BlobExport\\objects\\missing.txt', 'False', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\responses\\answer2.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for topic_one, pet_metadata.csv")

        # Verifies dog_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'dog', 'dog_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'cat^dog', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for topic_one, pet_metadata.csv")

        # Verifies pet_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'pet', 'pet_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30601', '*', '*', '*', '*', '*',
                     'cat', '..\\documents\\BlobExport\\objects\\file1.txt', 'True', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True'],
                    ['*', '*', '30602', '*', '*', '*', '*', '*',
                     'cat^dog', '..\\documents\\BlobExport\\objects\\file2.txt', 'True', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\responses\\answer1.txt', 'True'],
                    ['*', '*', '30603', '*', '*', '*', '*', '*',
                     'BLANK', '..\\documents\\BlobExport\\objects\\file3.txt', 'True', '*', '*', '*', '*',
                     'pet^toy', '..\\documents\\BlobExport\\responses\\missing.txt', 'False'],
                    ['*', '*', '30604', '*', '*', '*', '*', '*',
                     'cat', '..\\documents\\BlobExport\\objects\\missing.txt', 'False', '*', '*', '*', '*',
                     'pet', '..\\documents\\BlobExport\\responses\\answer2.txt', 'True']]
        self.assertEqual(expected, result, "Problem with test for topic_one, pet_metadata.csv")

        # Verifies toy_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'toy', 'toy_metadata.csv'))
        expected = [['city', 'state', 'zip', 'country', 'in_id', 'in_type', 'in_method', 'in_date', 'in_topic',
                     'in_document_name', 'in_document_name_present', 'out_id', 'out_type', 'out_method', 'out_date',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['*', '*', '30603', '*', '*', '*', '*', '*',
                     'BLANK', '..\\documents\\BlobExport\\objects\\file3.txt', 'True', '*', '*', '*', '*',
                     'pet^toy', '..\\documents\\BlobExport\\responses\\missing.txt', 'False']]
        self.assertEqual(expected, result, "Problem with test for topic_one, toy_metadata.csv")


if __name__ == '__main__':
    unittest.main()
