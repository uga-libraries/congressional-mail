import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_data_interchange_format import topics_sort
from test_script import csv_to_list, make_dir_list


def make_df(rows):
    """Make a df for test input with all columns, where rows just has the values that change for each test"""
    full_rows = []
    for row in rows:
        new_row = ['*', '*', '*', '*', '*', '*', '*', '*', row[0], '*', '*', row[1], '*', row[2], row[3], '*', '*', '*']
        full_rows.append(new_row)
    columns = ['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date', 'update_date',
               'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country', 'document_type',
               'communication_document_name', 'communication_document_id', 'file_location', 'file_name']
    df = pd.DataFrame(full_rows, columns=columns)
    return df


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variables and directory used by every test"""
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'name_export')
        self.output_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'output_directory')
        os.mkdir(self.output_dir)
        self.by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')

    def tearDown(self):
        """Delete the script outputs, if made"""
        output_directory = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'output_directory')
        if os.path.exists(output_directory):
            shutil.rmtree(output_directory)

    def test_duplicate_norm(self):
        """Test for when there are duplicate topics after normalization"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([[np.nan, '30600', 'IN', np.nan],
                      ['*kittens*', '30601', 'OUTGOING', '..\\documents\\forms\\cat.txt'],
                      ['<kittens>', '30602', 'AT_OUT2', '..\\documents\\indivletters\\toA.txt'],
                      ['puppies?', '30603', 'AT_OUT', '..\\documents\\indivletters\\toB.txt'],
                      [':kittens:', '30604', 'AT_IN2', '..\\documents\\objects\\file3.txt'],
                      ['puppies', '30605', 'AT_IN', '..\\documents\\objects\\file1.txt'],
                      ['puppies/', '30606', 'OUT', '..\\documents\\forms\\dog.txt'],
                      ['|kittens|', '30607', 'OUT', '..\\documents\\forms\\cat.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the contents of the output_directory.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.by_topic, 'puppies'),
                    os.path.join(self.by_topic, 'puppies_'),
                    os.path.join(self.by_topic, '_kittens_'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents'),
                    os.path.join(self.by_topic, 'puppies', 'puppies_metadata.csv'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents', 'objects'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents', 'objects', 'file1.txt'),
                    os.path.join(self.by_topic, 'puppies_', 'to_constituents'),
                    os.path.join(self.by_topic, 'puppies_', 'puppies__metadata.csv'),
                    os.path.join(self.by_topic, 'puppies_', 'to_constituents', 'forms'),
                    os.path.join(self.by_topic, 'puppies_', 'to_constituents', 'indivletters'),
                    os.path.join(self.by_topic, 'puppies_', 'to_constituents', 'forms', 'dog.txt'),
                    os.path.join(self.by_topic, 'puppies_', 'to_constituents', 'indivletters', 'toB.txt'),
                    os.path.join(self.by_topic, '_kittens_', 'from_constituents'),
                    os.path.join(self.by_topic, '_kittens_', 'to_constituents'),
                    os.path.join(self.by_topic, '_kittens_', '_kittens__metadata.csv'),
                    os.path.join(self.by_topic, '_kittens_', 'from_constituents', 'objects'),
                    os.path.join(self.by_topic, '_kittens_', 'from_constituents', 'objects', 'file3.txt'),
                    os.path.join(self.by_topic, '_kittens_', 'to_constituents', 'forms'),
                    os.path.join(self.by_topic, '_kittens_', 'to_constituents', 'indivletters'),
                    os.path.join(self.by_topic, '_kittens_', 'to_constituents', 'forms', 'cat.txt'),
                    os.path.join(self.by_topic, '_kittens_', 'to_constituents', 'indivletters', 'toA.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate_norm, output_directory")

        # Verifies puppies_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'puppies', 'puppies_metadata.csv'))
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies', '*', '*', '30605', '*',
                     'AT_IN', '..\\documents\\objects\\file1.txt', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for duplicate_norm, puppies_metadata.csv")

        # # Verifies puppies__metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'puppies_', 'puppies__metadata.csv'))
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies?', '*', '*', '30603', '*',
                     'AT_OUT', '..\\documents\\indivletters\\toB.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies/', '*', '*', '30606', '*',
                     'OUT', '..\\documents\\forms\\dog.txt', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for duplicate_norm, puppies__metadata.csv")

        # Verifies _kittens__metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, '_kittens_', '_kittens__metadata.csv'))
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*kittens*', '*', '*', '30601', '*',
                     'OUTGOING', '..\\documents\\forms\\cat.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '<kittens>', '*', '*', '30602', '*',
                     'AT_OUT2', '..\\documents\\indivletters\\toA.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', ':kittens:', '*', '*', '30604', '*',
                     'AT_IN2', '..\\documents\\objects\\file3.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '|kittens|', '*', '*', '30607', '*',
                     'OUT', '..\\documents\\forms\\cat.txt', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for duplicate_norm, _kittens__metadata.csv")

    def test_empty_blank(self):
        """Test for when no letters are sorted because the group and/or document name are blank for all"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['kittens', '30601', 'INCOMING', np.nan],
                      [np.nan, '30602', 'AT_OUT', np.nan],
                      ['kittens', '30603', 'AT_IN2', np.nan],
                      [np.nan, '30604', 'OUT', '..\\documents\\objects\\file1.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the contents of the output_directory.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic')]
        self.assertEqual(expected, result, "Problem with test for empty_blank, output_directory")

    def test_empty_missing(self):
        """Test for when no letters are sorted because none of the letters are in the export"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['kittens', '30601', 'INCOMING', '..\\documents\\ima\\from_0.txt'],
                      ['pets', '30602', 'AT_IN1', '..\\documents\\ima\\missing.txt'],
                      ['kittens', '30603', 'AT_OUT', '..\\documents\\form\\missing.txt'],
                      ['puppies', '30604', 'OUT', '..\\documents\\objects\\file0.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the contents of the output_directory.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv')]
        self.assertEqual(expected, result, "Problem with test for empty_missing, output_directory")

        # Verifies the file_not_found log has the expected contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['kittens', '..\\documents\\ima\\from_0.txt'],
                    ['kittens', '..\\documents\\form\\missing.txt'],
                    ['pets', '..\\documents\\ima\\missing.txt'],
                    ['puppies', '..\\documents\\objects\\file0.txt']]
        self.assertEqual(expected, result, "Problem with test for empty_missing, file_not_found")

    def test_in(self):
        """Test for when all letters are from constituents"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['kittens', '30601', 'INCOMING', '..\\documents\\ima\\from_01.txt'],
                      ['pets', '30602', 'AT_IN1', '..\\documents\\ima\\missing.txt'],
                      ['kittens', '30603', 'AT_IN2', '..\\documents\\ima\\from_01.txt'],
                      ['puppies', '30604', 'AT_IN', '..\\documents\\objects\\file1.txt'],
                      ['puppies', '30605', 'IN', '..\\documents\\objects\\file2.txt'],
                      [np.nan, '30606', 'IN', '..\\documents\\objects\\file3.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the contents of the output_directory.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.by_topic, 'kittens'),
                    os.path.join(self.by_topic, 'puppies'),
                    os.path.join(self.by_topic, 'kittens', 'from_constituents'),
                    os.path.join(self.by_topic, 'kittens', 'kittens_metadata.csv'),
                    os.path.join(self.by_topic, 'kittens', 'from_constituents', 'ima'),
                    os.path.join(self.by_topic, 'kittens', 'from_constituents', 'ima', 'from_01.txt'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents'),
                    os.path.join(self.by_topic, 'puppies', 'puppies_metadata.csv'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents', 'objects'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents', 'objects', 'file1.txt'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents', 'objects', 'file2.txt')]
        self.assertEqual(expected, result, "Problem with test for in, output_directory")

        # Verifies kittens_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'kittens', 'kittens_metadata.csv'))
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'kittens', '*', '*', '30601', '*',
                     'INCOMING', '..\\documents\\ima\\from_01.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'kittens', '*', '*', '30603', '*',
                     'AT_IN2', '..\\documents\\ima\\from_01.txt', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for in, kittens_metadata.csv")

        # Verifies puppies_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'puppies', 'puppies_metadata.csv'))
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies', '*', '*', '30604', '*', 
                     'AT_IN', '..\\documents\\objects\\file1.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies', '*', '*', '30605', '*', 
                     'IN', '..\\documents\\objects\\file2.txt', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for in, puppies_metadata.csv")

        # Verifies the file_not_found log has the expected contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', '..\\documents\\ima\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for in, file_not_found")

    def test_in_out(self):
        """Test for when letters are from and to constituents"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([[np.nan, '30600', 'IN', np.nan],
                      ['kittens', '30601', 'OUTGOING', '..\\documents\\forms\\cat.txt'],
                      ['bunnies', '30602', 'AT_OUT1', '..\\documents\\forms\\missing.txt'],
                      ['kittens', '30603', 'AT_OUT2', '..\\documents\\indivletters\\toA.txt'],
                      ['puppies', '30604', 'AT_OUT', '..\\documents\\indivletters\\toB.txt'],
                      ['kittens', '30605', 'AT_IN2', '..\\documents\\objects\\file3.txt'],
                      ['puppies', '30606', 'AT_IN', '..\\documents\\objects\\file1.txt'],
                      ['puppies', '30607', 'OUT', '..\\documents\\forms\\dog.txt'],
                      ['puppies', '30608', 'OUT', np.nan],
                      ['puppies', '30609', 'AT_IN', '..\\documents\\objects\\file1.txt'],
                      ['kittens', '30610', 'OUT', '..\\documents\\missing.txt'],
                      ['kittens', '30611', 'OUT', '..\\documents\\forms\\missing.txt'],
                      ['kittens', '30612', 'INCOMING', '..\\documents\\ima\\from_01.txt'],
                      ['bunnies', '30613', 'AT_IN1', '..\\documents\\ima\\missing.txt'],
                      ['puppies', '30614', 'IN', '..\\documents\\objects\\file2.txt'],
                      ['bunnies', '30615', 'OUT_JD', '..\\documents\\indivletters\\toD.txt'],
                      ['kittens', '30616', 'OUT', '..\\documents\\forms\\cat.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the contents of the output_directory.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.by_topic, 'bunnies'),
                    os.path.join(self.by_topic, 'kittens'),
                    os.path.join(self.by_topic, 'puppies'),
                    os.path.join(self.by_topic, 'bunnies', 'to_constituents'),
                    os.path.join(self.by_topic, 'bunnies', 'bunnies_metadata.csv'),
                    os.path.join(self.by_topic, 'bunnies', 'to_constituents', 'indivletters'),
                    os.path.join(self.by_topic, 'bunnies', 'to_constituents', 'indivletters', 'toD.txt'),
                    os.path.join(self.by_topic, 'kittens', 'from_constituents'),
                    os.path.join(self.by_topic, 'kittens', 'to_constituents'),
                    os.path.join(self.by_topic, 'kittens', 'kittens_metadata.csv'),
                    os.path.join(self.by_topic, 'kittens', 'from_constituents', 'ima'),
                    os.path.join(self.by_topic, 'kittens', 'from_constituents', 'objects'),
                    os.path.join(self.by_topic, 'kittens', 'from_constituents', 'ima', 'from_01.txt'),
                    os.path.join(self.by_topic, 'kittens', 'from_constituents', 'objects', 'file3.txt'),
                    os.path.join(self.by_topic, 'kittens', 'to_constituents', 'forms'),
                    os.path.join(self.by_topic, 'kittens', 'to_constituents', 'indivletters'),
                    os.path.join(self.by_topic, 'kittens', 'to_constituents', 'forms', 'cat.txt'),
                    os.path.join(self.by_topic, 'kittens', 'to_constituents', 'indivletters', 'toA.txt'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents'),
                    os.path.join(self.by_topic, 'puppies', 'to_constituents'),
                    os.path.join(self.by_topic, 'puppies', 'puppies_metadata.csv'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents', 'objects'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents', 'objects', 'file1.txt'),
                    os.path.join(self.by_topic, 'puppies', 'from_constituents', 'objects', 'file2.txt'),
                    os.path.join(self.by_topic, 'puppies', 'to_constituents', 'forms'),
                    os.path.join(self.by_topic, 'puppies', 'to_constituents', 'indivletters'),
                    os.path.join(self.by_topic, 'puppies', 'to_constituents', 'forms', 'dog.txt'),
                    os.path.join(self.by_topic, 'puppies', 'to_constituents', 'indivletters', 'toB.txt')]
        self.assertEqual(expected, result, "Problem with test for in_out, output_directory")

        # Verifies bunnies_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'bunnies', 'bunnies_metadata.csv'))
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'bunnies', '*', '*', '30615', '*',
                     'OUT_JD', '..\\documents\\indivletters\\toD.txt', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for in_out, bunnies_metadata.csv")

        # Verifies kittens_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'kittens', 'kittens_metadata.csv'))
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'kittens', '*', '*', '30601', '*',
                     'OUTGOING', '..\\documents\\forms\\cat.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'kittens', '*', '*', '30603', '*',
                     'AT_OUT2', '..\\documents\\indivletters\\toA.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'kittens', '*', '*', '30605', '*',
                     'AT_IN2', '..\\documents\\objects\\file3.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'kittens', '*', '*', '30612', '*',
                     'INCOMING', '..\\documents\\ima\\from_01.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'kittens', '*', '*', '30616', '*',
                     'OUT', '..\\documents\\forms\\cat.txt', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for in_out, kittens_metadata.csv")

        # Verifies puppies_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'puppies', 'puppies_metadata.csv'))
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies', '*', '*', '30604', '*',
                     'AT_OUT', '..\\documents\\indivletters\\toB.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies', '*', '*', '30606', '*',
                     'AT_IN', '..\\documents\\objects\\file1.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies', '*', '*', '30607', '*',
                     'OUT', '..\\documents\\forms\\dog.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies', '*', '*', '30609', '*',
                     'AT_IN', '..\\documents\\objects\\file1.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies', '*', '*', '30614', '*',
                     'IN', '..\\documents\\objects\\file2.txt', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for in_out, puppies_metadata.csv")

        # Verifies the file_not_found log has the expected contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['kittens', '..\\documents\\missing.txt'],
                    ['kittens', '..\\documents\\forms\\missing.txt'],
                    ['bunnies', '..\\documents\\ima\\missing.txt'],
                    ['bunnies', '..\\documents\\forms\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for in_out, file_not_found")

    def test_out(self):
        """Test for when all letters are to constituents"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['kittens', '30601', 'OUTGOING', '..\\documents\\forms\\cat.txt'],
                      ['pets', '30602', 'AT_OUT1', '..\\documents\\forms\\missing.txt'],
                      ['kittens', '30603', 'AT_OUT2', '..\\documents\\indivletters\\toA.txt'],
                      ['puppies', '30604', 'AT_OUT', '..\\documents\\indivletters\\toB.txt'],
                      ['puppies', '30605', 'OUT', '..\\documents\\forms\\dog.txt'],
                      ['puppies', '30606', 'OUT', np.nan],
                      ['kittens', '30607', 'OUT', '..\\documents\\missing.txt']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the contents of the output_directory.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.by_topic, 'kittens'),
                    os.path.join(self.by_topic, 'puppies'),
                    os.path.join(self.by_topic, 'kittens', 'to_constituents'),
                    os.path.join(self.by_topic, 'kittens', 'kittens_metadata.csv'),
                    os.path.join(self.by_topic, 'kittens', 'to_constituents', 'forms'),
                    os.path.join(self.by_topic, 'kittens', 'to_constituents', 'indivletters'),
                    os.path.join(self.by_topic, 'kittens', 'to_constituents', 'forms', 'cat.txt'),
                    os.path.join(self.by_topic, 'kittens', 'to_constituents', 'indivletters', 'toA.txt'),
                    os.path.join(self.by_topic, 'puppies', 'to_constituents'),
                    os.path.join(self.by_topic, 'puppies', 'puppies_metadata.csv'),
                    os.path.join(self.by_topic, 'puppies', 'to_constituents', 'forms'),
                    os.path.join(self.by_topic, 'puppies', 'to_constituents', 'indivletters'),
                    os.path.join(self.by_topic, 'puppies', 'to_constituents', 'forms', 'dog.txt'),
                    os.path.join(self.by_topic, 'puppies', 'to_constituents', 'indivletters', 'toB.txt')]
        self.assertEqual(expected, result, "Problem with test for out, output_directory")

        # Verifies kittens_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'kittens', 'kittens_metadata.csv'))
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'kittens', '*', '*', '30601', '*',
                     'OUTGOING', '..\\documents\\forms\\cat.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'kittens', '*', '*', '30603', '*',
                     'AT_OUT2', '..\\documents\\indivletters\\toA.txt', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for out, kittens_metadata.csv")

        # Verifies puppies_metadata.csv has the expected contents.
        result = csv_to_list(os.path.join(self.by_topic, 'puppies', 'puppies_metadata.csv'))
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_id',
                     'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies', '*', '*', '30604', '*',
                     'AT_OUT', '..\\documents\\indivletters\\toB.txt', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'puppies', '*', '*', '30605', '*',
                     'OUT', '..\\documents\\forms\\dog.txt', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for out, puppies_metadata.csv")

        # Verifies the file_not_found log has the expected contents.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['kittens', '..\\documents\\missing.txt'],
                    ['pets', '..\\documents\\forms\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for out, file_not_found")


if __name__ == '__main__':
    unittest.main()
