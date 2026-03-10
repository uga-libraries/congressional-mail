import os
import pandas as pd
import shutil
import unittest
from css_data_interchange_format import topics_sort_files
from test_read_metadata import df_to_list
from test_script import csv_to_list, make_dir_list


def make_df(row_list):
    """Make a dataframe from a list of rows with consistent columns, used for test input"""
    column_names = ['group_name', 'zip_code', 'document_type', 'communication_document_name',
                    'communication_document_name_present']
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
        """Delete the script outputs, if made"""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_from_all_found(self):
        """Test for when all files in the in_document column are present"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['pets', '30600', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                      ['pets', '30601', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                      ['pets', '30602', 'AT_IN', '..\\documents\\objects\\from2.txt', 'TBD'],
                      ['pets', '30603', 'IN', '..\\documents\\objects\\from3.txt', 'TBD']])
        df_topic = topics_sort_files(df, 'IN', self.input_dir, self.output_dir, self.from_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['group_name', 'zip_code', 'document_type', 'communication_document_name',
                    'communication_document_name_present'],
                    ['pets', '30600', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                    ['pets', '30601', 'IN', '..\\documents\\objects\\from1.txt', True],
                    ['pets', '30602', 'AT_IN', '..\\documents\\objects\\from2.txt', True],
                    ['pets', '30603', 'IN', '..\\documents\\objects\\from3.txt', True]]
        self.assertEqual(expected, result, "Problem with test for from_all_found, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'pets'),
                    self.from_folder_path,
                    self.to_folder_path,
                    os.path.join(self.from_folder_path, 'objects'),
                    os.path.join(self.from_folder_path, 'objects', 'from1.txt'),
                    os.path.join(self.from_folder_path, 'objects', 'from2.txt'),
                    os.path.join(self.from_folder_path, 'objects', 'from3.txt')]
        self.assertEqual(expected, result, "Problem with test for from_all_found, directory")

    def test_from_duplicates(self):
        """Test for when there are duplicates in the in_document column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['pets', '30600', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                      ['pets', '30601', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                      ['pets', '30602', 'AT_IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                      ['pets', '30603', 'IN', '..\\documents\\missing\\from3.txt', 'TBD']])
        df_topic = topics_sort_files(df, 'IN', self.input_dir, self.output_dir, self.from_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['group_name', 'zip_code', 'document_type', 'communication_document_name',
                     'communication_document_name_present'],
                    ['pets', '30600', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                    ['pets', '30601', 'IN', '..\\documents\\objects\\from1.txt', True],
                    ['pets', '30602', 'AT_IN', '..\\documents\\objects\\from1.txt', True],
                    ['pets', '30603', 'IN', '..\\documents\\missing\\from3.txt', False]]
        self.assertEqual(expected, result, "Problem with test for from_duplicates, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'pets'),
                    self.from_folder_path,
                    self.to_folder_path,
                    os.path.join(self.from_folder_path, 'objects'),
                    os.path.join(self.from_folder_path, 'objects', 'from1.txt')]
        self.assertEqual(expected, result, "Problem with test for from_duplicates, directory")

        # Verifies topics_sort_file_not_found.csv was not created.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', '..\\documents\\missing\\from3.txt']]
        self.assertEqual(expected, result, "Problem with test for from_duplicates, not_found")

    def test_from_subfolders(self):
        """Test for when there are multiple levels of subfolders in the in_document column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['pets', '30600', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                      ['pets', '30601', 'IN', '..\\documents\\forms\\campaign_a\\a1.txt', 'TBD'],
                      ['pets', '30602', 'IN', '..\\documents\\forms\\campaign_a\\missing.txt', 'TBD'],
                      ['pets', '30603', 'AT_IN', '..\\documents\\forms\\campaign_b\\b1.txt', 'TBD'],
                      ['pets', '30604', 'IN', '..\\documents\\forms\\campaign_b\\b2.txt', 'TBD']])
        df_topic = topics_sort_files(df, 'IN', self.input_dir, self.output_dir, self.from_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['group_name', 'zip_code', 'document_type', 'communication_document_name',
                     'communication_document_name_present'],
                    ['pets', '30600', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                    ['pets', '30601', 'IN', '..\\documents\\forms\\campaign_a\\a1.txt', True],
                    ['pets', '30602', 'IN', '..\\documents\\forms\\campaign_a\\missing.txt', False],
                    ['pets', '30603', 'AT_IN', '..\\documents\\forms\\campaign_b\\b1.txt', True],
                    ['pets', '30604', 'IN', '..\\documents\\forms\\campaign_b\\b2.txt', True]]
        self.assertEqual(expected, result, "Problem with test for from_subfolders, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'pets'),
                    self.from_folder_path,
                    self.to_folder_path,
                    os.path.join(self.from_folder_path, 'forms'),
                    os.path.join(self.from_folder_path, 'forms', 'campaign_a'),
                    os.path.join(self.from_folder_path, 'forms', 'campaign_b'),
                    os.path.join(self.from_folder_path, 'forms', 'campaign_a', 'a1.txt'),
                    os.path.join(self.from_folder_path, 'forms', 'campaign_b', 'b1.txt'),
                    os.path.join(self.from_folder_path, 'forms', 'campaign_b', 'b2.txt')]
        self.assertEqual(expected, result, "Problem with test for from_subfolders, directory")

        # Verifies topics_sort_file_not_found.csv was not created.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', '..\\documents\\forms\\campaign_a\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for from_subfolders, not_found")

    def test_from_unique(self):
        """Test for when there are no duplicates in the in_document column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['pets', '30600', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                      ['pets', '30601', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                      ['pets', '30602', 'AT_IN', '..\\documents\\objects\\from2.txt', 'TBD'],
                      ['pets', '30603', 'IN', '..\\documents\\missing\\from3.txt', 'TBD'],
                      ['pets', '30604', 'IN', '..\\documents\\objects\\missing.txt', 'TBD']])
        df_topic = topics_sort_files(df, 'IN', self.input_dir, self.output_dir, self.from_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['group_name', 'zip_code', 'document_type', 'communication_document_name',
                    'communication_document_name_present'],
                    ['pets', '30600', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                    ['pets', '30601', 'IN', '..\\documents\\objects\\from1.txt', True],
                    ['pets', '30602', 'AT_IN', '..\\documents\\objects\\from2.txt', True],
                    ['pets', '30603', 'IN', '..\\documents\\missing\\from3.txt', False],
                    ['pets', '30604', 'IN', '..\\documents\\objects\\missing.txt', False]]
        self.assertEqual(expected, result, "Problem with test for from_unique, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'pets'),
                    self.from_folder_path,
                    self.to_folder_path,
                    os.path.join(self.from_folder_path, 'objects'),
                    os.path.join(self.from_folder_path, 'objects', 'from1.txt'),
                    os.path.join(self.from_folder_path, 'objects', 'from2.txt')]
        self.assertEqual(expected, result, "Problem with test for from_unique, directory")

        # Verifies topics_sort_file_not_found.csv was not created.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', '..\\documents\\missing\\from3.txt'],
                    ['pets', '..\\documents\\objects\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for from_unique, not_found")

    def test_to_all_found(self):
        """Test for when all files in the out_document column are present"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['pets', '30600', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                      ['pets', '30601', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                      ['pets', '30602', 'AT_OUT', '..\\documents\\indivletters\\toB.txt', 'TBD'],
                      ['pets', '30603', 'OUT', '..\\documents\\indivletters\\toC.txt', 'TBD']])
        df_topic = topics_sort_files(df, 'OUT', self.input_dir, self.output_dir, self.to_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['group_name', 'zip_code', 'document_type', 'communication_document_name',
                    'communication_document_name_present'],
                    ['pets', '30600', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                    ['pets', '30601', 'OUT', '..\\documents\\indivletters\\toA.txt', True],
                    ['pets', '30602', 'AT_OUT', '..\\documents\\indivletters\\toB.txt', True],
                    ['pets', '30603', 'OUT', '..\\documents\\indivletters\\toC.txt', True]]
        self.assertEqual(expected, result, "Problem with test for to_all_found, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'pets'),
                    self.from_folder_path,
                    self.to_folder_path,
                    os.path.join(self.to_folder_path, 'indivletters'),
                    os.path.join(self.to_folder_path, 'indivletters', 'toA.txt'),
                    os.path.join(self.to_folder_path, 'indivletters', 'toB.txt'),
                    os.path.join(self.to_folder_path, 'indivletters', 'toC.txt')]
        self.assertEqual(expected, result, "Problem with test for to_all_found, directory")

    def test_to_duplicates(self):
        """Test for when there are duplicates in the out_document column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['pets', '30600', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                      ['pets', '30601', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                      ['pets', '30602', 'AT_OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                      ['pets', '30603', 'OUT', '..\\documents\\missing\\toC.txt', 'TBD']])
        df_topic = topics_sort_files(df, 'OUT', self.input_dir, self.output_dir, self.to_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['group_name', 'zip_code', 'document_type', 'communication_document_name',
                     'communication_document_name_present'],
                    ['pets', '30600', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                    ['pets', '30601', 'OUT', '..\\documents\\indivletters\\toA.txt', True],
                    ['pets', '30602', 'AT_OUT', '..\\documents\\indivletters\\toA.txt', True],
                    ['pets', '30603', 'OUT', '..\\documents\\missing\\toC.txt', False]]
        self.assertEqual(expected, result, "Problem with test for to_duplicates, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'pets'),
                    self.from_folder_path,
                    self.to_folder_path,
                    os.path.join(self.to_folder_path, 'indivletters'),
                    os.path.join(self.to_folder_path, 'indivletters', 'toA.txt')]
        self.assertEqual(expected, result, "Problem with test for to_duplicates, directory")

        # Verifies topics_sort_file_not_found.csv was not created.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', '..\\documents\\missing\\toC.txt']]
        self.assertEqual(expected, result, "Problem with test for to_duplicates, not_found")

    def test_to_subfolders(self):
        """Test for when there are multiple levels of subfolders in the out_document column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['pets', '30600', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                      ['pets', '30601', 'OUT', '..\\documents\\formletters\\parks.txt', 'TBD'],
                      ['pets', '30602', 'OUT', '..\\documents\\formletters\\pets\\dogs.txt', 'TBD'],
                      ['pets', '30603', 'OUT', '..\\documents\\formletters\\pets\\treats\\dog_treat.txt', 'TBD'],
                      ['pets', '30604', 'AT_OUT', '..\\documents\\formletters\\pets\\cats.txt', 'TBD'],
                      ['pets', '30605', 'OUT', '..\\documents\\formletters\\missing.txt', 'TBD'],
                      ['pets', '30606', 'OUT', '..\\documents\\formletters\\pets\\missing\\dogs.txt', 'TBD']])
        df_topic = topics_sort_files(df, 'OUT', self.input_dir, self.output_dir, self.from_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['group_name', 'zip_code', 'document_type', 'communication_document_name',
                     'communication_document_name_present'],
                    ['pets', '30600', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                    ['pets', '30601', 'OUT', '..\\documents\\formletters\\parks.txt', True],
                    ['pets', '30602', 'OUT', '..\\documents\\formletters\\pets\\dogs.txt', True],
                    ['pets', '30603', 'OUT', '..\\documents\\formletters\\pets\\treats\\dog_treat.txt', True],
                    ['pets', '30604', 'AT_OUT', '..\\documents\\formletters\\pets\\cats.txt', True],
                    ['pets', '30605', 'OUT', '..\\documents\\formletters\\missing.txt', False],
                    ['pets', '30606', 'OUT', '..\\documents\\formletters\\pets\\missing\\dogs.txt', False]]
        self.assertEqual(expected, result, "Problem with test for to_subfolders, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'pets'),
                    self.from_folder_path,
                    self.to_folder_path,
                    os.path.join(self.from_folder_path, 'formletters'),
                    os.path.join(self.from_folder_path, 'formletters', 'pets'),
                    os.path.join(self.from_folder_path, 'formletters', 'parks.txt'),
                    os.path.join(self.from_folder_path, 'formletters', 'pets', 'treats'),
                    os.path.join(self.from_folder_path, 'formletters', 'pets', 'cats.txt'),
                    os.path.join(self.from_folder_path, 'formletters', 'pets', 'dogs.txt'),
                    os.path.join(self.from_folder_path, 'formletters', 'pets', 'treats', 'dog_treat.txt')]
        self.assertEqual(expected, result, "Problem with test for to_subfolders, directory")

        # Verifies topics_sort_file_not_found.csv was not created.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', '..\\documents\\formletters\\missing.txt'],
                    ['pets', '..\\documents\\formletters\\pets\\missing\\dogs.txt']]
        self.assertEqual(expected, result, "Problem with test for to_subfolders, not_found")

    def test_to_unique(self):
        """Test for when there are no duplicates in the out_document column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['pets', '30600', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                      ['pets', '30601', 'OUT', '..\\documents\\indivletters\\toA.txt', 'TBD'],
                      ['pets', '30602', 'AT_OUT', '..\\documents\\indivletters\\toB.txt', 'TBD'],
                      ['pets', '30603', 'OUT', '..\\documents\\missing\\toC.txt', 'TBD'],
                      ['pets', '30604', 'OUT', '..\\documents\\indivletters\\missing.txt', 'TBD']])
        df_topic = topics_sort_files(df, 'OUT', self.input_dir, self.output_dir, self.to_folder_path)

        # Verifies df_topic has the correct values.
        result = df_to_list(df_topic)
        expected = [['group_name', 'zip_code', 'document_type', 'communication_document_name',
                    'communication_document_name_present'],
                    ['pets', '30600', 'IN', '..\\documents\\objects\\from1.txt', 'TBD'],
                    ['pets', '30601', 'OUT', '..\\documents\\indivletters\\toA.txt', True],
                    ['pets', '30602', 'AT_OUT', '..\\documents\\indivletters\\toB.txt', True],
                    ['pets', '30603', 'OUT', '..\\documents\\missing\\toC.txt', False],
                    ['pets', '30604', 'OUT', '..\\documents\\indivletters\\missing.txt', False]]
        self.assertEqual(expected, result, "Problem with test for from_unique, df_topic")

        # Verifies the expected folders were created and have the expected files in them.
        result = make_dir_list(self.output_dir)
        expected = [os.path.join(self.output_dir, 'correspondence_by_topic'),
                    os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'),
                    os.path.join(self.output_dir, 'correspondence_by_topic', 'pets'),
                    self.from_folder_path,
                    self.to_folder_path,
                    os.path.join(self.to_folder_path, 'indivletters'),
                    os.path.join(self.to_folder_path, 'indivletters', 'toA.txt'),
                    os.path.join(self.to_folder_path, 'indivletters', 'toB.txt')]
        self.assertEqual(expected, result, "Problem with test for from_unique, directory")

        # Verifies topics_sort_file_not_found.csv was not created.
        result = csv_to_list(os.path.join(self.output_dir, 'topics_sort_file_not_found.csv'))
        expected = [['pets', '..\\documents\\missing\\toC.txt'],
                    ['pets', '..\\documents\\indivletters\\missing.txt']]
        self.assertEqual(expected, result, "Problem with test for from_unique, not_found")


if __name__ == '__main__':
    unittest.main()
