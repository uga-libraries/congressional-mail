import os
import pandas as pd
import shutil
import unittest
from css_data_interchange_format import topics_sort_save_metadata
from test_script import csv_to_list


def make_df(rows):
    """Make a df for test input"""
    column_names = ['group_name', 'zip_code', 'communication_document_name', 'communication_document_name_present']
    df = pd.DataFrame(rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test folder and its contents (the topic folder and metadata csv), if made"""
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata')
        if os.path.exists(topic_path):
            shutil.rmtree(topic_path)

    def test_duplicate(self):
        """Test for when there are duplicate rows"""
        # Makes test input and runs the function.
        df = make_df([['rivers', '30601', 'path\\file2.txt', True],
                      ['rivers', '30602', 'path\\file2.txt', True],
                      ['rivers', '30602', 'path\\file2.txt', True]])
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'rivers')
        os.makedirs(topic_path)
        topics_sort_save_metadata(df, topic_path, 'rivers')

        # Verifies the contents of rivers_metadata.csv
        result = csv_to_list(os.path.join(topic_path, 'rivers_metadata.csv'))
        expected = [['group_name', 'zip_code', 'communication_document_name'],
                    ['rivers', '30601', 'path\\file2.txt'],
                    ['rivers', '30602', 'path\\file2.txt']]
        self.assertEqual(expected, result, "Problem with test for duplicate")

    def test_found_all(self):
        """Test for when all documents were found"""
        # Makes test input and runs the function.
        df = make_df([['rivers', '30601', 'path\\file1.txt', True],
                      ['rivers', '30602', 'path\\file2.txt', True],
                      ['rivers', '30603', 'path\\file3.txt', True]])
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'rivers')
        os.makedirs(topic_path)
        topics_sort_save_metadata(df, topic_path, 'rivers')

        # Verifies the contents of rivers_metadata.csv
        result = csv_to_list(os.path.join(topic_path, 'rivers_metadata.csv'))
        expected = [['group_name', 'zip_code', 'communication_document_name'],
                    ['rivers', '30601', 'path\\file1.txt'],
                    ['rivers', '30602', 'path\\file2.txt'],
                    ['rivers', '30603', 'path\\file3.txt']]
        self.assertEqual(expected, result, "Problem with test for found_all")

    def test_found_some(self):
        """Test for when some documents were found and others not"""
        # Makes test input and runs the function.
        df = make_df([['rivers', '30601', 'path\\file1.txt', False],
                      ['rivers', '30602', 'path\\file2.txt', True],
                      ['rivers', '30603', 'path\\file3.txt', False],
                      ['rivers', '30604', 'path\\file4.txt', True],
                      ['rivers', '30605', 'path\\file5.txt', False]])
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'rivers')
        os.makedirs(topic_path)
        topics_sort_save_metadata(df, topic_path, 'rivers')

        # Verifies the contents of rivers_metadata.csv
        result = csv_to_list(os.path.join(topic_path, 'rivers_metadata.csv'))
        expected = [['group_name', 'zip_code', 'communication_document_name'],
                    ['rivers', '30602', 'path\\file2.txt'],
                    ['rivers', '30604', 'path\\file4.txt']]
        self.assertEqual(expected, result, "Problem with test for found_some")

    def test_update_csv(self):
        """Test for when the metadata.csv already exists"""
        # Makes test input and runs the function to make the metadata.csv.
        df = make_df([['rivers*', '30601', 'path\\file1.txt', True],
                      ['rivers*', '30602', 'path\\file2.txt', True],
                      ['rivers*', '30603', 'path\\file3.txt', False]])
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'rivers_')
        os.makedirs(topic_path)
        topics_sort_save_metadata(df, topic_path, 'rivers_')

        # Makes another df for test input and runs the function to add to the metadata.csv.
        df = make_df([['rivers:', '30604', 'path\\file4.txt', True],
                      ['rivers:', '30605', 'path\\file5.txt', True]])
        topics_sort_save_metadata(df, topic_path, 'rivers_')

        # Verifies the contents of rivers__metadata.csv
        result = csv_to_list(os.path.join(topic_path, 'rivers__metadata.csv'))
        expected = [['group_name', 'zip_code', 'communication_document_name'],
                    ['rivers*', '30601', 'path\\file1.txt'],
                    ['rivers*', '30602', 'path\\file2.txt'],
                    ['rivers:', '30604', 'path\\file4.txt'],
                    ['rivers:', '30605', 'path\\file5.txt']]
        self.assertEqual(expected, result, "Problem with test for update_csv")


if __name__ == '__main__':
    unittest.main()
