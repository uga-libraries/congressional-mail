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
        self.to_folder_path = os.path.join(self.output_dir, 'correspondence_by_topic', 'pets', 'to_constituents')
        os.makedirs(self.to_folder_path)
        self.from_folder_path = os.path.join(self.output_dir, 'correspondence_by_topic', 'pets', 'from_constituents')
        os.makedirs(self.from_folder_path)

    def tearDown(self):
        """Delete the output folder and all its contents"""
        output_dir = os.path.join(os.getcwd(), 'test_data', 'topics_sort_files', 'output')
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

    def test_from_all(self):
        """Test for letters from constituents when all documents are present"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'forms\\Support.txt', 'TBD'],
                      ['30601', 'pets', 'attachments\\scan1.txt', 'TBD'],
                      ['30602', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30603', 'pets', 'in-email\\file2.txt', 'TBD']])
        df = topics_sort_files(df, 'attachments|in-email', self.input_dir, self.output_dir, self.from_folder_path)

        # Verifies df has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'forms\\Support.txt', 'TBD'],
                    ['30601', 'pets', 'attachments\\scan1.txt', True],
                    ['30602', 'pets', 'in-email\\file1.txt', True],
                    ['30603', 'pets', 'in-email\\file2.txt', True]]
        self.assertEqual(expected, result, "Problem with test for from_all, df")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(by_topic, 'pets'),
                    os.path.join(by_topic, 'pets', 'from_constituents'),
                    os.path.join(by_topic, 'pets', 'to_constituents'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'attachments'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'in-email'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'attachments', 'scan1.txt'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'in-email', 'file1.txt'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'in-email', 'file2.txt')]
        self.assertEqual(expected, result, "Problem with test for from_all, output_dir")

    def test_from_duplicates(self):
        """Test for letters from constituents when there are duplicates in the documents column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'forms\\Support.txt', 'TBD'],
                      ['30601', 'pets', 'attachments\\scan1.txt', 'TBD'],
                      ['30602', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30603', 'pets', 'in-email\\file2.txt', 'TBD'],
                      ['30604', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30605', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30606', 'pets', 'attachments\\scan_missing.txt', 'TBD'],
                      ['30607', 'pets', 'in-email\\file_missing.txt', 'TBD']])
        df = topics_sort_files(df, 'attachments|in-email', self.input_dir, self.output_dir, self.from_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'forms\\Support.txt', 'TBD'],
                    ['30601', 'pets', 'attachments\\scan1.txt', True],
                    ['30602', 'pets', 'in-email\\file1.txt', True],
                    ['30603', 'pets', 'in-email\\file2.txt', True],
                    ['30604', 'pets', 'in-email\\file1.txt', True],
                    ['30605', 'pets', 'in-email\\file1.txt', True],
                    ['30606', 'pets', 'attachments\\scan_missing.txt', False],
                    ['30607', 'pets', 'in-email\\file_missing.txt', False]]
        self.assertEqual(expected, result, "Problem with test for from_duplicates, df")

        # Verifies the contents of topics_sort_file_not_found.csv.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', 'attachments\\scan_missing.txt'],
                    ['pets', 'in-email\\file_missing.txt']]
        self.assertEqual(expected, result, "Problem with test for from_duplicates, not_found")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(by_topic, 'pets'),
                    os.path.join(by_topic, 'pets', 'from_constituents'),
                    os.path.join(by_topic, 'pets', 'to_constituents'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'attachments'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'in-email'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'attachments', 'scan1.txt'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'in-email', 'file1.txt'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'in-email', 'file2.txt')]
        self.assertEqual(expected, result, "Problem with test for from_duplicates, output_dir")

    def test_from_unique(self):
        """Test for letters from constituents when there are no duplicates in the documents column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'forms\\Support.txt', 'TBD'],
                      ['30601', 'pets', 'in-email\\file_missing.txt', 'TBD'],
                      ['30602', 'pets', 'attachments\\scan1.txt', 'TBD'],
                      ['30603', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30604', 'pets', 'attachments\\scan0.txt', 'TBD'],
                      ['30605', 'pets', 'attachments\\scan_missing.txt', 'TBD']])
        df = topics_sort_files(df, 'attachments|in-email', self.input_dir, self.output_dir, self.from_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'forms\\Support.txt', 'TBD'],
                    ['30601', 'pets', 'in-email\\file_missing.txt', False],
                    ['30602', 'pets', 'attachments\\scan1.txt', True],
                    ['30603', 'pets', 'in-email\\file1.txt', True],
                    ['30604', 'pets', 'attachments\\scan0.txt', False],
                    ['30605', 'pets', 'attachments\\scan_missing.txt', False]]
        self.assertEqual(expected, result, "Problem with test for from_unique, df")

        # Verifies the contents of topics_sort_file_not_found.csv.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', 'in-email\\file_missing.txt'],
                    ['pets', 'attachments\\scan0.txt'],
                    ['pets', 'attachments\\scan_missing.txt']]
        self.assertEqual(expected, result, "Problem with test for from_unique, not_found")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(by_topic, 'pets'),
                    os.path.join(by_topic, 'pets', 'from_constituents'),
                    os.path.join(by_topic, 'pets', 'to_constituents'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'attachments'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'in-email'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'attachments', 'scan1.txt'),
                    os.path.join(by_topic, 'pets', 'from_constituents', 'in-email', 'file1.txt')]
        self.assertEqual(expected, result, "Problem with test for from_unique, output_dir")

    def test_to_all(self):
        """Test for letters to constituents when all documents are present"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30601', 'pets', 'forms\\Support.txt', 'TBD'],
                      ['30602', 'pets', 'out-custom\\Doe.txt', 'TBD'],
                      ['30603', 'pets', 'out-custom\\Smith.txt', 'TBD']])
        df = topics_sort_files(df, 'forms|out-custom', self.input_dir, self.output_dir, self.to_folder_path)

        # Verifies df has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'in-email\\file1.txt', 'TBD'],
                    ['30601', 'pets', 'forms\\Support.txt', True],
                    ['30602', 'pets', 'out-custom\\Doe.txt', True],
                    ['30603', 'pets', 'out-custom\\Smith.txt', True]]
        self.assertEqual(expected, result, "Problem with test for to_all, df")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(by_topic, 'pets'),
                    os.path.join(by_topic, 'pets', 'from_constituents'),
                    os.path.join(by_topic, 'pets', 'to_constituents'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'forms'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'out-custom'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'forms', 'Support.txt'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'out-custom', 'Doe.txt'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'out-custom', 'Smith.txt')]
        self.assertEqual(expected, result, "Problem with test for to_all, output_dir")

    def test_to_duplicates(self):
        """Test for letters to constituents when there are duplicates in the documents column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30601', 'pets', 'forms\\Support.txt', 'TBD'],
                      ['30602', 'pets', 'forms\\missing.txt', 'TBD'],
                      ['30603', 'pets', 'out-custom\\Doe.txt', 'TBD'],
                      ['30604', 'pets', 'out-custom\\missing.txt', 'TBD'],
                      ['30605', 'pets', 'forms\\Support.txt', 'TBD'],
                      ['30606', 'pets', 'out-custom\\Smith.txt', 'TBD'],
                      ['30607', 'pets', 'forms\\missing.txt', 'TBD']])
        df = topics_sort_files(df, 'forms|out-custom', self.input_dir, self.output_dir, self.to_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'in-email\\file1.txt', 'TBD'],
                    ['30601', 'pets', 'forms\\Support.txt', True],
                    ['30602', 'pets', 'forms\\missing.txt', False],
                    ['30603', 'pets', 'out-custom\\Doe.txt', True],
                    ['30604', 'pets', 'out-custom\\missing.txt', False],
                    ['30605', 'pets', 'forms\\Support.txt', True],
                    ['30606', 'pets', 'out-custom\\Smith.txt', True],
                    ['30607', 'pets', 'forms\\missing.txt', False]]
        self.assertEqual(expected, result, "Problem with test for to_duplicates, df")

        # Verifies the contents of topics_sort_file_not_found.csv.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', 'forms\\missing.txt'],
                    ['pets', 'out-custom\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for to_duplicates, not_found")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(by_topic, 'pets'),
                    os.path.join(by_topic, 'pets', 'from_constituents'),
                    os.path.join(by_topic, 'pets', 'to_constituents'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'forms'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'out-custom'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'forms', 'Support.txt'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'out-custom', 'Doe.txt'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'out-custom', 'Smith.txt')]
        self.assertEqual(expected, result, "Problem with test for to_duplicates, output_dir")

    def test_to_unique(self):
        """Test for letters to constituents when there are no duplicates in the documents column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30600', 'pets', 'in-email\\file1.txt', 'TBD'],
                      ['30601', 'pets', 'out-custom\\Doe.txt', 'TBD'],
                      ['30602', 'pets', 'out-custom\\missing.txt', 'TBD'],
                      ['30603', 'pets', 'forms\\Support.txt', 'TBD'],
                      ['30604', 'pets', 'out-custom\\Smith.txt', 'TBD']])
        df = topics_sort_files(df, 'forms|out-custom', self.input_dir, self.output_dir, self.to_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df)
        expected = [['zip_code', 'code_description', 'correspondence_document_name',
                     'correspondence_document_name_present'],
                    ['30600', 'pets', 'in-email\\file1.txt', 'TBD'],
                    ['30601', 'pets', 'out-custom\\Doe.txt', True],
                    ['30602', 'pets', 'out-custom\\missing.txt', False],
                    ['30603', 'pets', 'forms\\Support.txt', True],
                    ['30604', 'pets', 'out-custom\\Smith.txt', True]]
        self.assertEqual(expected, result, "Problem with test for to_unique, df")

        # Verifies the contents of topics_sort_file_not_found.csv.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', 'out-custom\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for to_unique, not_found")

        # Verifies the contents of the output directory.
        result = make_dir_list(self.output_dir)
        by_topic = os.path.join(self.output_dir, 'correspondence_by_topic')
        expected = [os.path.join(by_topic),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(by_topic, 'pets'),
                    os.path.join(by_topic, 'pets', 'from_constituents'),
                    os.path.join(by_topic, 'pets', 'to_constituents'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'forms'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'out-custom'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'forms', 'Support.txt'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'out-custom', 'Doe.txt'),
                    os.path.join(by_topic, 'pets', 'to_constituents', 'out-custom', 'Smith.txt')]
        self.assertEqual(expected, result, "Problem with test for to_unique, output_dir")


if __name__ == '__main__':
    unittest.main()
