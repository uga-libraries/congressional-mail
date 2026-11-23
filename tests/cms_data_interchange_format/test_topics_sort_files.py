import os
import pandas as pd
import shutil
import unittest
from cms_data_interchange_format import topics_sort_files
from test_read_metadata import df_to_list
from test_script import csv_to_list, make_dir_list


def make_df(row_list):
    """Make a dataframe from a list of rows with consistent columns, used for test input"""
    column_names = ['zip_code', 'code_description', 'correspondence_document_name',
                    'correspondence_document_name_present']
    df = pd.DataFrame(row_list, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variables and directories used by every test, which are usually from topics_sort()"""
        self.input_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort_files', 'name_export')
        self.output_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort_files', 'output')
        self.by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        self.topic_path = os.path.join(self.output_dir, 'correspondence_by_topic', 'pets')
        os.makedirs(self.topic_path)

    def tearDown(self):
        """Delete the output folder and all its contents"""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_all(self):
        """Test for when all documents are present"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'forms\\Support.txt', 'TBD'],
                      ['30601', 'pets', 'attachments\\scan1.txt', 'TBD'],
                      ['30602', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30603', 'pets', 'in-email\\file2.txt', 'TBD']])
        df = topics_sort_files(df, self.input_dir, self.output_dir, self.topic_path)

        # Verifies df has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'forms\\Support.txt', True],
                    ['30601', 'pets', 'attachments\\scan1.txt', True],
                    ['30602', 'pets', 'in-email\\file1.txt', True],
                    ['30603', 'pets', 'in-email\\file2.txt', True]]
        self.assertEqual(expected, result, "Problem with test for all, df")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(by_topic, 'pets'),
                    os.path.join(by_topic, 'pets', 'attachments'),
                    os.path.join(by_topic, 'pets', 'forms'),
                    os.path.join(by_topic, 'pets', 'in-email'),
                    os.path.join(by_topic, 'pets', 'attachments', 'scan1.txt'),
                    os.path.join(by_topic, 'pets', 'forms', 'Support.txt'),
                    os.path.join(by_topic, 'pets', 'in-email', 'file1.txt'),
                    os.path.join(by_topic, 'pets', 'in-email', 'file2.txt')]
        self.assertEqual(expected, result, "Problem with test for all, output_dir")

    def test_duplicates(self):
        """Test for when there are duplicates in the documents column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'forms\\Support.txt', 'TBD'],
                      ['30601', 'pets', 'attachments\\scan1.txt', 'TBD'],
                      ['30602', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30603', 'pets', 'in-email\\file2.txt', 'TBD'],
                      ['30604', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30605', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30606', 'pets', 'attachments\\scan_missing.txt', 'TBD'],
                      ['30607', 'pets', 'in-email\\file_missing.txt', 'TBD']])
        df = topics_sort_files(df, self.input_dir, self.output_dir, self.topic_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'forms\\Support.txt', True],
                    ['30601', 'pets', 'attachments\\scan1.txt', True],
                    ['30602', 'pets', 'in-email\\file1.txt', True],
                    ['30603', 'pets', 'in-email\\file2.txt', True],
                    ['30604', 'pets', 'in-email\\file1.txt', True],
                    ['30605', 'pets', 'in-email\\file1.txt', True],
                    ['30606', 'pets', 'attachments\\scan_missing.txt', False],
                    ['30607', 'pets', 'in-email\\file_missing.txt', False]]
        self.assertEqual(expected, result, "Problem with test for duplicates, df")

        # Verifies the contents of topics_sort_file_not_found.csv.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', 'attachments\\scan_missing.txt'],
                    ['pets', 'in-email\\file_missing.txt']]
        self.assertEqual(expected, result, "Problem with test for duplicates, not_found")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(by_topic, 'pets'),
                    os.path.join(by_topic, 'pets', 'attachments'),
                    os.path.join(by_topic, 'pets', 'forms'),
                    os.path.join(by_topic, 'pets', 'in-email'),
                    os.path.join(by_topic, 'pets', 'attachments', 'scan1.txt'),
                    os.path.join(by_topic, 'pets', 'forms', 'Support.txt'),
                    os.path.join(by_topic, 'pets', 'in-email', 'file1.txt'),
                    os.path.join(by_topic, 'pets', 'in-email', 'file2.txt')]
        self.assertEqual(expected, result, "Problem with test for duplicates, output_dir")

    def test_path_error(self):
        """Test for when the path is error_new or for a folder instead of a file (just logged)"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'error_new', 'TBD'],
                      ['30601', 'pets', 'out-custom', 'TBD']])
        df = topics_sort_files(df, self.input_dir, self.output_dir, self.topic_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'error_new', False],
                    ['30601', 'pets', 'out-custom', False]]
        self.assertEqual(expected, result, "Problem with test for path_error, df")

        # Verifies the contents of topics_sort_file_not_found.csv.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', 'error_new'],
                    ['pets', 'out-custom']]
        self.assertEqual(expected, result, "Problem with test for path_error, not_found")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(by_topic, 'pets')]
        self.assertEqual(expected, result, "Problem with test for path_error, output_dir")

    def test_subfolders(self):
        """Test for when there are multiple levels of subfolders"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30601', 'pets', 'documents\\1.txt', 'TBD'],
                      ['30602', 'pets', 'documents\\A\\2.txt', 'TBD'],
                      ['30603', 'pets', 'documents\\A\\missing\\1.txt', 'TBD'],
                      ['30604', 'pets', 'documents\\B\\BB\\4.txt', 'TBD'],
                      ['30605', 'pets', 'documents\\B\\BB\\missing.txt', 'TBD'],
                      ['30606', 'pets', 'documents\\C\\6.txt', 'TBD']])
        df = topics_sort_files(df, self.input_dir, self.output_dir, self.topic_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'in-email\\file1.txt', True],
                    ['30601', 'pets', 'documents\\1.txt', True],
                    ['30602', 'pets', 'documents\\A\\2.txt', True],
                    ['30603', 'pets', 'documents\\A\\missing\\1.txt', False],
                    ['30604', 'pets', 'documents\\B\\BB\\4.txt', True],
                    ['30605', 'pets', 'documents\\B\\BB\\missing.txt', False],
                    ['30606', 'pets', 'documents\\C\\6.txt', True]]
        self.assertEqual(expected, result, "Problem with test for subfolders, df")

        # Verifies the contents of topics_sort_file_not_found.csv.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', 'documents\\A\\missing\\1.txt'],
                    ['pets', 'documents\\B\\BB\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for subfolders, not_found")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(by_topic, 'pets'),
                    os.path.join(by_topic, 'pets', 'documents'),
                    os.path.join(by_topic, 'pets', 'in-email'),
                    os.path.join(by_topic, 'pets', 'documents', 'A'),
                    os.path.join(by_topic, 'pets', 'documents', 'B'),
                    os.path.join(by_topic, 'pets', 'documents', 'C'),
                    os.path.join(by_topic, 'pets', 'documents', '1.txt'),
                    os.path.join(by_topic, 'pets', 'documents', 'A', 'missing'),
                    os.path.join(by_topic, 'pets', 'documents', 'A', '2.txt'),
                    os.path.join(by_topic, 'pets', 'documents', 'B', 'BB'),
                    os.path.join(by_topic, 'pets', 'documents', 'B', 'BB', '4.txt'),
                    os.path.join(by_topic, 'pets', 'documents', 'C', '6.txt'),
                    os.path.join(by_topic, 'pets', 'in-email', 'file1.txt')]
        self.assertEqual(expected, result, "Problem with test for subfolders, output_dir")

    def test_unique(self):
        """Test for when there are no duplicates in the documents column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30601', 'pets', 'out-custom\\Doe.txt', 'TBD'],
                      ['30602', 'pets', 'out-custom\\missing.txt', 'TBD'],
                      ['30603', 'pets', 'forms\\Support.txt', 'TBD'],
                      ['30604', 'pets', 'out-custom\\Smith.txt', 'TBD']])
        df = topics_sort_files(df, self.input_dir, self.output_dir, self.topic_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'in-email\\file1.txt', True],
                    ['30601', 'pets', 'out-custom\\Doe.txt', True],
                    ['30602', 'pets', 'out-custom\\missing.txt', False],
                    ['30603', 'pets', 'forms\\Support.txt', True],
                    ['30604', 'pets', 'out-custom\\Smith.txt', True]]
        self.assertEqual(expected, result, "Problem with test for unique, df")

        # Verifies the contents of topics_sort_file_not_found.csv.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', 'out-custom\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for unique, not_found")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(by_topic, 'pets'),
                    os.path.join(by_topic, 'pets', 'forms'),
                    os.path.join(by_topic, 'pets', 'in-email'),
                    os.path.join(by_topic, 'pets', 'out-custom'),
                    os.path.join(by_topic, 'pets', 'forms', 'Support.txt'),
                    os.path.join(by_topic, 'pets', 'in-email', 'file1.txt'),
                    os.path.join(by_topic, 'pets', 'out-custom', 'Doe.txt'),
                    os.path.join(by_topic, 'pets', 'out-custom', 'Smith.txt')]
        self.assertEqual(expected, result, "Problem with test for unique, output_dir")


if __name__ == '__main__':
    unittest.main()
