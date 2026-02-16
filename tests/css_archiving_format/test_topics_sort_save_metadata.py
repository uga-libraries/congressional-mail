import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import topics_sort_save_metadata
from test_script import csv_to_list


def make_df(rows):
    """Make a df for test input"""
    columns = ['zip', 'in_topic', 'in_document_name', 'in_document_name_present', 'out_topic', 'out_document_name',
               'out_document_name_present', 'in_topic_split', 'out_topic_split']
    df = pd.DataFrame(rows, columns=columns)
    return df


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test folder and its contents (the topic folder and metadata csv), if made"""
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata')
        if os.path.exists(topic_path):
            shutil.rmtree(topic_path)

    def test_basic(self):
        """Test for when the df meets no cleanup criteria other than having topic_split columns before saving"""
        # Makes test input (topic folder, df, and path variables) and runs the function.
        rows = [['30601', 'apples', '1.txt', True, 'Apples', 'Apples.doc', True, 'apples', 'Apples'],
                ['30602', 'apples', '2.txt', True, 'ag', 'ag.doc', False, 'apples', 'ag'],
                ['30603', 'apples', '3.txt', False, 'Apples', 'Apples.doc', True, 'apples', 'Apples'],
                ['30603', 'apples', '4.txt', False, 'ag', 'ag.doc', False, 'apples', 'ag']]
        df = make_df(rows)
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'apples')
        os.makedirs(topic_path)
        topic_norm = 'apples'
        topics_sort_save_metadata(df, topic_path, topic_norm)

        # Verifies the metadata csv has the correct contents.
        result = csv_to_list(os.path.join(topic_path, 'apples_description.csv'))
        expected = [['zip', 'in_topic', 'in_document_name', 'in_document_name_present',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['30601', 'apples', '1.txt', 'True', 'Apples', 'Apples.doc', 'True'],
                    ['30602', 'apples', '2.txt', 'True', 'ag', 'ag.doc', 'False'],
                    ['30603', 'apples', '3.txt', 'False', 'Apples', 'Apples.doc', 'True'],
                    ['30603', 'apples', '4.txt', 'False', 'ag', 'ag.doc', 'False']]
        self.assertEqual(expected, result, "Problem with test for basic")

    def test_duplicate(self):
        """Test for when the df includes duplicate rows once the topic_split columns are removed"""
        # Makes test input (topic folder, df, and path variables) and runs the function.
        rows = [['30601', 'ag^apples', '1.txt', True, 'Apples', 'Apples.doc', True, 'ag', 'Apples'],
                ['30601', 'ag^apples', '1.txt', True, 'Apples', 'Apples.doc', True, 'apples', 'Apples'],
                ['30602', 'ag^apples', '2.txt', True, 'apples^reg', 'Apples.doc', True, 'ag', 'apples'],
                ['30602', 'ag^apples', '2.txt', True, 'apples^reg', 'Apples.doc', True, 'apples', 'apples'],
                ['30602', 'ag^apples', '2.txt', True, 'apples^reg', 'Apples.doc', True, 'apples', 'reg'],
                ['30603', 'apples', '3.txt', False, 'ag', 'Ag.doc', False, 'apples', 'ag']]
        df = make_df(rows)
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'apples')
        os.makedirs(topic_path)
        topic_norm = 'apples'
        topics_sort_save_metadata(df, topic_path, topic_norm)

        # Verifies the metadata csv has the correct contents.
        result = csv_to_list(os.path.join(topic_path, 'apples_description.csv'))
        expected = [['zip', 'in_topic', 'in_document_name', 'in_document_name_present',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['30601', 'ag^apples', '1.txt', 'True', 'Apples', 'Apples.doc', 'True'],
                    ['30602', 'ag^apples', '2.txt', 'True', 'apples^reg', 'Apples.doc', 'True'],
                    ['30603', 'apples', '3.txt', 'False', 'ag', 'Ag.doc', 'False']]
        self.assertEqual(expected, result, "Problem with test for duplicate")

    def test_tbd(self):
        """Test for when the df includes TBD to be updated"""
        # Makes test input (topic folder, df, and path variables) and runs the function.
        rows = [['30601', 'ag', '1.txt', True, 'Apples', 'Apples.doc', True, 'ag', 'Apples'],
                ['30602', 'apples', np.nan, 'TBD', 'Apples', 'Apples.doc', True, 'apples', 'Apples'],
                ['30603', 'apples', '3.txt', False, 'ag', np.nan, 'TBD', 'apples', 'ag'],
                ['30604', 'apples', np.nan, 'TBD', 'ag', np.nan, 'TBD', 'apples', 'ag']]
        df = make_df(rows)
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'apples')
        os.makedirs(topic_path)
        topic_norm = 'apples'
        topics_sort_save_metadata(df, topic_path, topic_norm)

        # Verifies the metadata csv has the correct contents.
        result = csv_to_list(os.path.join(topic_path, 'apples_description.csv'))
        expected = [['zip', 'in_topic', 'in_document_name', 'in_document_name_present',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['30601', 'ag', '1.txt', 'True', 'Apples', 'Apples.doc', 'True'],
                    ['30602', 'apples', 'BLANK', 'no_path_provided', 'Apples', 'Apples.doc', 'True'],
                    ['30603', 'apples', '3.txt', 'False', 'ag', 'BLANK', 'no_path_provided'],
                    ['30604', 'apples', 'BLANK', 'no_path_provided', 'ag', 'BLANK', 'no_path_provided']]
        self.assertEqual(expected, result, "Problem with test for TBD")


if __name__ == '__main__':
    unittest.main()
