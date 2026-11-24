import numpy as np
import os
import pandas as pd
import shutil
import unittest
from cms_data_interchange_format import topics_sort
from test_script import csv_to_list, make_dir_list, text_to_list
from test_topics_sort_df import make_df


def make_log_list():
    """Makes a list of the contents of the log created when files in the metadata are not in the directory"""
    log_path = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'topics_sort_file_not_found.csv')
    log_df = pd.read_csv(log_path)
    log_list = [log_df.columns.tolist()] + log_df.values.tolist()
    return log_list


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variables used by every test"""
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'name_export')
        self.output_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'output')
        self.by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')

    def tearDown(self):
        """Delete the script outputs, if made"""
        # Output for most tests
        output_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort', 'output')
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

        # Files for restart
        restart_dir = os.path.join(os.getcwd(), 'test_data', 'restart')
        if os.path.exists(restart_dir):
            shutil.rmtree(restart_dir)

    def test_empty_blank(self):
        """Test for when all rows have no topic and/or no document and should be skipped"""
        # Makes a dataframe to use as test input and runs the function being tested.
        os.mkdir(self.output_dir)
        df = make_df([['30600', np.nan, 'cats'],
                      ['30600', 'attachments\\scan1.txt', np.nan],
                      ['30601', np.nan, np.nan],])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        expected = [self.by_topic, os.path.join(self.output_dir, 'topics_sort_metadata.csv')]
        self.assertEqual(expected, result, "Problem with test for empty_blank, directory")

        # Verifies the contents of topics_sort_metadata.csv
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_metadata.csv'))
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date', 'response_type',
                     'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position', '2C_sequence_number',
                     'document_type', 'correspondence_document_name', 'correspondence_document_name_present',
                     'file_location', 'code_type', 'code', 'code_description', 'inactive_flag']]
        self.assertEqual(expected, result, "Problem with test for empty_missing, metadata")

    def test_empty_missing(self):
        """Test for when all files are only in the metadata and not the directory"""
        # Makes a dataframe to use as test input and runs the function being tested.
        os.mkdir(self.output_dir)
        df = make_df([['30600', 'attachments\\scan0.txt', 'cats'],
                      ['30601', 'forms\\con.txt', 'dogs'],
                      ['30602', 'in-email\\file0.txt', 'cats'],
                      ['30603', 'in-email\\file_missing.txt', 'dogs'],
                      ['30604', 'out-custom\\Smith.doc', 'dogs']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        expected = [self.by_topic,
                    os.path.join(self.output_dir, 'topics_sort_complete.txt'),
                    os.path.join(self.output_dir, 'topics_sort_expected_file_count.csv'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'topics_sort_metadata.csv')]
        self.assertEqual(expected, result, "Problem with test for empty_missing, directory")

        # Verifies the contents of topics_sort_complete.txt
        result = text_to_list(os.path.join(self.output_dir, 'topics_sort_complete.txt'))
        expected = ['cats', 'dogs']
        self.assertEqual(expected, result, "Problem with test for empty_missing, complete")

        # Verifies the contents of topics_sort_expected_file_count.csv
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_expected_file_count.csv'))
        expected = [['cats', '2'],
                    ['dogs', '3']]
        self.assertEqual(expected, result, "Problem with test for empty_missing, expected_file_count")

        # Verifies the contents of topics_sort_file_not_found.csv
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['cats', 'attachments\\scan0.txt'],
                    ['cats', 'in-email\\file0.txt'],
                    ['dogs', 'forms\\con.txt'],
                    ['dogs', 'in-email\\file_missing.txt'],
                    ['dogs', 'out-custom\\Smith.doc']]
        self.assertEqual(expected, result, "Problem with test for empty_missing, not_found")

        # Verifies the contents of topics_sort_metadata.csv
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_metadata.csv'))
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date', 'response_type',
                     'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position', '2C_sequence_number',
                     'document_type', 'correspondence_document_name', 'correspondence_document_name_present',
                     'file_location', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30600', '*', '*', '*', '*', '*',
                     'attachments\\scan0.txt', 'TBD', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30601', '*', '*', '*', '*', '*',
                     'forms\\con.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30602', '*', '*', '*', '*', '*',
                     'in-email\\file0.txt', 'TBD', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30603', '*', '*', '*', '*', '*',
                     'in-email\\file_missing.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30604', '*', '*', '*', '*', '*',
                     'out-custom\\Smith.doc', 'TBD', '*', '*', '*', 'dogs', '*']]
        self.assertEqual(expected, result, "Problem with test for empty_missing, metadata")

    def test_duplicate(self):
        """Test for duplicate topics after normalizing"""
        # Makes a dataframe to use as test input and runs the function being tested.
        os.mkdir(self.output_dir)
        df = make_df([['30600', 'out-custom\\Brown.txt', '/dogs'],
                      ['30601', 'forms\\Support.txt', '/dogs'],
                      ['30602', 'forms\\Thanks.txt', '<dogs']])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        expected = [self.by_topic,
                    os.path.join(self.output_dir, 'topics_sort_complete.txt'),
                    os.path.join(self.output_dir, 'topics_sort_expected_file_count.csv'),
                    os.path.join(self.output_dir, 'topics_sort_metadata.csv'),
                    os.path.join(self.by_topic, '_dogs'),
                    os.path.join(self.by_topic, '_dogs', 'forms'),
                    os.path.join(self.by_topic, '_dogs', 'out-custom'),
                    os.path.join(self.by_topic, '_dogs', '_dogs_metadata.csv'),
                    os.path.join(self.by_topic, '_dogs', 'forms', 'Support.txt'),
                    os.path.join(self.by_topic, '_dogs', 'forms', 'Thanks.txt'),
                    os.path.join(self.by_topic, '_dogs', 'out-custom', 'Brown.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicate, directory")

        # Verifies the contents of topics_sort_complete.txt
        result = text_to_list(os.path.join(self.output_dir, 'topics_sort_complete.txt'))
        expected = ['/dogs', '<dogs']
        self.assertEqual(expected, result, "Problem with test for duplicate, complete")

        # Verifies the contents of topics_sort_expected_file_count.csv
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_expected_file_count.csv'))
        expected = [['_dogs', '2'],
                    ['_dogs', '1']]
        self.assertEqual(expected, result, "Problem with test for duplicate, expected_file_count")

        # Verifies the contents of dogs_metadata.csv
        result = csv_to_list(os.path.join(self.by_topic, '_dogs', '_dogs_metadata.csv'))
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name',
                     'file_location', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30600', '*', '*', '*', '*', '*',
                     'out-custom\\Brown.txt', '*', '*', '*', '/dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30601', '*', '*', '*', '*', '*',
                     'forms\\Support.txt', '*', '*', '*', '/dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30602', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', '*', '*', '*', '<dogs', '*']]
        self.assertEqual(expected, result, "Problem with test for duplicate, dogs_metadata.csv")

        # Verifies the contents of topics_sort_metadata.csv
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_metadata.csv'))
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date', 'response_type',
                     'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position', '2C_sequence_number',
                     'document_type', 'correspondence_document_name', 'correspondence_document_name_present',
                     'file_location', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30600', '*', '*', '*', '*', '*',
                     'out-custom\\Brown.txt', 'TBD', '*', '*', '*', '/dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30601', '*', '*', '*', '*', '*',
                     'forms\\Support.txt', 'TBD', '*', '*', '*', '/dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30602', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', 'TBD', '*', '*', '*', '<dogs', '*']]
        self.assertEqual(expected, result, "Problem with test for empty_missing, metadata")

    def test_restart(self):
        """Test for when topic sorting is interrupted and restarted"""
        # Makes a copy of the test data, since it is altered by the test,
        # makes path variables since different from the other tests,
        # and reads the csv into a df
        output_dir = os.path.join(os.getcwd(), 'test_data', 'restart', 'output')
        input_dir = os.path.join(os.getcwd(), 'test_data', 'restart', 'name_export')
        by_topic = os.path.join(output_dir, 'correspondence_by_topic')
        shutil.copytree(os.path.join(os.getcwd(), 'test_data', 'topics_sort_restart'),
                        os.path.join(os.getcwd(), 'test_data', 'restart'))
        df = pd.read_csv(os.path.join(output_dir, 'topics_sort_metadata.csv'))
        topics_sort(df, input_dir, output_dir, restart=True)

        # Verifies the contents of the output directory.
        result = make_dir_list(output_dir)
        expected = [by_topic,
                    os.path.join(output_dir, 'topics_sort_complete.txt'),
                    os.path.join(output_dir, 'topics_sort_expected_file_count.csv'),
                    os.path.join(output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(output_dir, 'topics_sort_metadata.csv'),
                    os.path.join(by_topic, 'cats'),
                    os.path.join(by_topic, 'dogs'),
                    os.path.join(by_topic, 'cats', 'attachments'),
                    os.path.join(by_topic, 'cats', 'forms'),
                    os.path.join(by_topic, 'cats', 'in-email'),
                    os.path.join(by_topic, 'cats', 'out-custom'),
                    os.path.join(by_topic, 'cats', 'cats_metadata.csv'),
                    os.path.join(by_topic, 'cats', 'attachments', 'scan1.txt'),
                    os.path.join(by_topic, 'cats', 'forms', 'Support.txt'),
                    os.path.join(by_topic, 'cats', 'forms', 'Thanks.txt'),
                    os.path.join(by_topic, 'cats', 'in-email', 'file1.txt'),
                    os.path.join(by_topic, 'cats', 'out-custom', 'Doe.txt'),
                    os.path.join(by_topic, 'dogs', 'attachments'),
                    os.path.join(by_topic, 'dogs', 'forms'),
                    os.path.join(by_topic, 'dogs', 'in-email'),
                    os.path.join(by_topic, 'dogs', 'out-custom'),
                    os.path.join(by_topic, 'dogs', 'dogs_metadata.csv'),
                    os.path.join(by_topic, 'dogs', 'attachments', 'scan2.txt'),
                    os.path.join(by_topic, 'dogs', 'forms', 'Thanks.txt'),
                    os.path.join(by_topic, 'dogs', 'in-email', 'file2.txt'),
                    os.path.join(by_topic, 'dogs', 'out-custom', 'Jones.txt')]
        self.assertEqual(expected, result, "Problem with test for restart, directory")

        # Verifies the contents of cats_metadata.csv
        result = csv_to_list(os.path.join(by_topic, 'cats', 'cats_metadata.csv'))
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name',
                     'file_location', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30604', '*', '*', '*', '*', '*',
                     'out-custom\\Doe.txt', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30605', '*', '*', '*', '*', '*',
                     'in-email\\file1.txt', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30610', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30611', '*', '*', '*', '*', '*',
                     'forms\\Support.txt', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30614', '*', '*', '*', '*', '*',
                     'attachments\\scan1.txt', '*', '*', '*', 'cats', '*']]
        self.assertEqual(expected, result, "Problem with test for restart, cats_metadata.csv")

        # Verifies the contents of dogs_metadata.csv
        result = csv_to_list(os.path.join(by_topic, 'dogs', 'dogs_metadata.csv'))
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name',
                     'file_location', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30602', '*', '*', '*', '*', '*',
                     'out-custom\\Jones.txt', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30603', '*', '*', '*', '*', '*',
                     'in-email\\file2.txt', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30607', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30612', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30616', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30617', '*', '*', '*', '*', '*',
                     'attachments\\scan2.txt', '*', '*', '*', 'dogs', '*']]
        self.assertEqual(expected, result, "Problem with test for restart, dogs_metadata.csv")

        # Verifies the contents of topics_sort_complete.txt
        result = text_to_list(os.path.join(output_dir, 'topics_sort_complete.txt'))
        expected = ['dogs', 'cats']
        self.assertEqual(expected, result, "Problem with test for restart, complete")

        # Verifies the contents of topics_sort_expected_file_count.csv
        result = csv_to_list(os.path.join(output_dir, 'topics_sort_expected_file_count.csv'))
        expected = [['dogs', '6'],
                    ['cats', '7']]
        self.assertEqual(expected, result, "Problem with test for restart, expected_file_count")

        # Verifies the contents of topics_sort_file_not_found.csv
        result = csv_to_list(os.path.join(output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['dogs', 'forms\\missing.txt'],
                    ['dogs', 'in-email\\file0.txt'],
                    ['cats', 'out-custom\\missing.txt'],
                    ['cats', 'forms\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for restart, not_found")

        # Verifies the contents of topics_sort_metadata.csv
        result = csv_to_list(os.path.join(output_dir, 'topics_sort_metadata.csv'))
        expected = [
            ['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date', 'response_type',
             'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position', '2C_sequence_number',
             'document_type', 'correspondence_document_name', 'correspondence_document_name_present',
             'file_location', 'code_type', 'code', 'code_description', 'inactive_flag'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30602', '*', '*', '*', '*', '*',
             'out-custom\\Jones.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30603', '*', '*', '*', '*', '*',
             'in-email\\file2.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30604', '*', '*', '*', '*', '*',
             'out-custom\\Doe.txt', 'TBD', '*', '*', '*', 'cats', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30605', '*', '*', '*', '*', '*',
             'in-email\\file1.txt', 'TBD', '*', '*', '*', 'cats', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30607', '*', '*', '*', '*', '*',
             'forms\\Thanks.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30608', '*', '*', '*', '*', '*',
             'out-custom\\missing.txt', 'TBD', '*', '*', '*', 'cats', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30609', '*', '*', '*', '*', '*',
             'forms\\missing.txt', 'TBD', '*', '*', '*', 'cats', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30610', '*', '*', '*', '*', '*',
             'forms\\Thanks.txt', 'TBD', '*', '*', '*', 'cats', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30611', '*', '*', '*', '*', '*',
             'forms\\Support.txt', 'TBD', '*', '*', '*', 'cats', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30612', '*', '*', '*', '*', '*',
             'forms\\Thanks.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30614', '*', '*', '*', '*', '*',
             'attachments\\scan1.txt', 'TBD', '*', '*', '*', 'cats', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30615', '*', '*', '*', '*', '*',
             'forms\\missing.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30616', '*', '*', '*', '*', '*',
             'forms\\Thanks.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30617', '*', '*', '*', '*', '*',
             'attachments\\scan2.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30618', '*', '*', '*', '*', '*',
             'in-email\\file0.txt', 'TBD', '*', '*', '*', 'dogs', '*']]
        self.assertEqual(expected, result, "Problem with test for restart, metadata")

    def test_unique(self):
        """Test for when all topics are unique"""
        # Makes a dataframe to use as test input and runs the function being tested.
        os.mkdir(self.output_dir)
        df = make_df([['30601', 'out-custom\\Brown.txt', np.nan],
                      ['30602', 'out-custom\\Jones.txt', 'dogs'],
                      ['30603', 'in-email\\file2.txt', 'dogs'],
                      ['30604', 'out-custom\\Doe.txt', 'cats'],
                      ['30605', 'in-email\\file1.txt', 'cats'],
                      ['30606', np.nan, 'cats'],
                      ['30607', 'forms\\Thanks.txt', 'dogs'],
                      ['30608', 'out-custom\\missing.txt', 'cats'],
                      ['30609', 'forms\\missing.txt', 'cats'],
                      ['30610', 'forms\\Thanks.txt', 'cats'],
                      ['30611', 'forms\\Support.txt', 'cats'],
                      ['30612', 'forms\\Thanks.txt', 'dogs'],
                      ['30613', np.nan, 'dogs'],
                      ['30614', 'attachments\\scan1.txt', 'cats'],
                      ['30615', 'forms\\missing.txt', 'dogs'],
                      ['30616', 'forms\\Thanks.txt', 'dogs'],
                      ['30617', 'attachments\\scan2.txt', 'dogs'],
                      ['30618', 'in-email\\file0.txt', 'dogs'],
                      ['30619', 'in-email\\file4.txt', np.nan],
                      ['30620', np.nan, np.nan]])
        topics_sort(df, self.input_dir, self.output_dir)

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        expected = [self.by_topic,
                    os.path.join(self.output_dir, 'topics_sort_complete.txt'),
                    os.path.join(self.output_dir, 'topics_sort_expected_file_count.csv'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'topics_sort_metadata.csv'),
                    os.path.join(self.by_topic, 'cats'),
                    os.path.join(self.by_topic, 'dogs'),
                    os.path.join(self.by_topic, 'cats', 'attachments'),
                    os.path.join(self.by_topic, 'cats', 'forms'),
                    os.path.join(self.by_topic, 'cats', 'in-email'),
                    os.path.join(self.by_topic, 'cats', 'out-custom'),
                    os.path.join(self.by_topic, 'cats', 'cats_metadata.csv'),
                    os.path.join(self.by_topic, 'cats', 'attachments', 'scan1.txt'),
                    os.path.join(self.by_topic, 'cats', 'forms', 'Support.txt'),
                    os.path.join(self.by_topic, 'cats', 'forms', 'Thanks.txt'),
                    os.path.join(self.by_topic, 'cats', 'in-email', 'file1.txt'),
                    os.path.join(self.by_topic, 'cats', 'out-custom', 'Doe.txt'),
                    os.path.join(self.by_topic, 'dogs', 'attachments'),
                    os.path.join(self.by_topic, 'dogs', 'forms'),
                    os.path.join(self.by_topic, 'dogs', 'in-email'),
                    os.path.join(self.by_topic, 'dogs', 'out-custom'),
                    os.path.join(self.by_topic, 'dogs', 'dogs_metadata.csv'),
                    os.path.join(self.by_topic, 'dogs', 'attachments', 'scan2.txt'),
                    os.path.join(self.by_topic, 'dogs', 'forms', 'Thanks.txt'),
                    os.path.join(self.by_topic, 'dogs', 'in-email', 'file2.txt'),
                    os.path.join(self.by_topic, 'dogs', 'out-custom', 'Jones.txt')]
        self.assertEqual(expected, result, "Problem with test for unique, directory")

        # Verifies the contents of cats_metadata.csv
        result = csv_to_list(os.path.join(self.by_topic, 'cats', 'cats_metadata.csv'))
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name',
                     'file_location', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30604', '*', '*', '*', '*', '*',
                     'out-custom\\Doe.txt', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30605', '*', '*', '*', '*', '*',
                     'in-email\\file1.txt', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30610', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30611', '*', '*', '*', '*', '*',
                    'forms\\Support.txt', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30614', '*', '*', '*', '*', '*',
                     'attachments\\scan1.txt', '*', '*', '*', 'cats', '*']]
        self.assertEqual(expected, result, "Problem with test for unique, cats_metadata.csv")

        # Verifies the contents of dogs_metadata.csv
        result = csv_to_list(os.path.join(self.by_topic, 'dogs', 'dogs_metadata.csv'))
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name',
                     'file_location', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30602', '*', '*', '*', '*', '*',
                     'out-custom\\Jones.txt', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30603', '*', '*', '*', '*', '*',
                     'in-email\\file2.txt', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30607', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30612', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30616', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30617', '*', '*', '*', '*', '*',
                     'attachments\\scan2.txt', '*', '*', '*', 'dogs', '*']]
        self.assertEqual(expected, result, "Problem with test for unique, dogs_metadata.csv")

        # Verifies the contents of topics_sort_complete.txt
        result = text_to_list(os.path.join(self.output_dir, 'topics_sort_complete.txt'))
        expected = ['dogs', 'cats']
        self.assertEqual(expected, result, "Problem with test for unique, complete")

        # Verifies the contents of topics_sort_expected_file_count.csv
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_expected_file_count.csv'))
        expected = [['dogs', '6'],
                    ['cats', '7']]
        self.assertEqual(expected, result, "Problem with test for unique, expected_file_count")

        # Verifies the contents of topics_sort_file_not_found.csv
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['dogs', 'forms\\missing.txt'],
                    ['dogs', 'in-email\\file0.txt'],
                    ['cats', 'out-custom\\missing.txt'],
                    ['cats', 'forms\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for unique, not_found")

        # Verifies the contents of topics_sort_metadata.csv
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_metadata.csv'))
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date', 'response_type',
                     'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position', '2C_sequence_number',
                     'document_type', 'correspondence_document_name', 'correspondence_document_name_present',
                     'file_location', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30602', '*', '*', '*', '*', '*',
                     'out-custom\\Jones.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30603', '*', '*', '*', '*', '*',
                     'in-email\\file2.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30604', '*', '*', '*', '*', '*',
                     'out-custom\\Doe.txt', 'TBD', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30605', '*', '*', '*', '*', '*',
                     'in-email\\file1.txt', 'TBD', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30607', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30608', '*', '*', '*', '*', '*',
                     'out-custom\\missing.txt', 'TBD', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30609', '*', '*', '*', '*', '*',
                     'forms\\missing.txt', 'TBD', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30610', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', 'TBD', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30611', '*', '*', '*', '*', '*',
                     'forms\\Support.txt', 'TBD', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30612', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30614', '*', '*', '*', '*', '*',
                     'attachments\\scan1.txt', 'TBD', '*', '*', '*', 'cats', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30615', '*', '*', '*', '*', '*',
                     'forms\\missing.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30616', '*', '*', '*', '*', '*',
                     'forms\\Thanks.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30617', '*', '*', '*', '*', '*',
                     'attachments\\scan2.txt', 'TBD', '*', '*', '*', 'dogs', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30618', '*', '*', '*', '*', '*',
                     'in-email\\file0.txt', 'TBD', '*', '*', '*', 'dogs', '*']]
        self.assertEqual(expected, result, "Problem with test for unique, metadata")


if __name__ == '__main__':
    unittest.main()
