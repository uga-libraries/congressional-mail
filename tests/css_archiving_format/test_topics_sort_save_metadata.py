import numpy as np
import os
import pandas as pd
import shutil
import unittest
from css_archiving_format import topics_sort_save_metadata
from test_script import csv_to_list


def make_df(rows):
    """Make a df for test input"""
    column_names = ['in_topic', 'in_document_name', 'in_document_name_present', 'out_topic', 
                    'out_document_name', 'out_document_name_present', 'in_document_name_split', 
                    'out_document_name_split', 'in_topic_split', 'out_topic_split']
    df = pd.DataFrame(rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test folder and its contents (the topic folder and metadata csv), if made"""
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata')
        if os.path.exists(topic_path):
            shutil.rmtree(topic_path)

    def test_basic(self):
        """Test for when the df meets no cleanup criteria other than having topic_split columns before saving"""
        # Makes test input and runs the function.
        rows = [['apples', '1.txt', True, 'Apples', 'Apples.doc', True, '1.txt', 'Apples.doc', 'apples', 'Apples'],
                ['apples', '2.txt', True, 'ag', 'ag.doc', False, '2.txt', 'ag.doc', 'apples', 'ag'],
                ['apples', '3.txt', False, 'Apples', 'Apples.doc', True, '3.txt', 'Apples.doc', 'apples', 'Apples'],
                ['apples', '4.txt', True, 'ag', 'ag.doc', False, '4.txt', 'ag.doc', 'apples', 'ag']]
        df = make_df(rows)
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'apples')
        os.makedirs(topic_path)
        topics_sort_save_metadata(df, topic_path, 'apples')

        # Verifies the metadata csv has the correct contents.
        result = csv_to_list(os.path.join(topic_path, 'apples_metadata.csv'))
        expected = [['in_topic', 'in_document_name', 'in_document_name_present',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['apples', '1.txt', 'True', 'Apples', 'Apples.doc', 'True'],
                    ['apples', '2.txt', 'True', 'ag', 'ag.doc', 'False'],
                    ['apples', '3.txt', 'False', 'Apples', 'Apples.doc', 'True'],
                    ['apples', '4.txt', 'True', 'ag', 'ag.doc', 'False']]
        self.assertEqual(expected, result, "Problem with test for basic")

    def test_duplicate_doc(self):
        """Test for when the df includes duplicate rows once the document_name_split columns are removed"""
        # Makes test input and runs the function.
        rows = [['ag', '1.txt^2.txt', True, 'ag', 'Apples.doc', True, '1.txt', 'Apples.doc', 'ag', 'ag'],
                ['ag', '1.txt^2.txt', True, 'ag', 'Apples.doc', True, '2.txt', 'Apples.doc', 'ag', 'ag'],
                ['ag', '2.txt^3.txt^4.txt', True, 'ag', 'A.doc^B.doc', True, '2.txt', 'A.doc', 'ag', 'ag'],
                ['ag', '2.txt^3.txt^4.txt', True, 'ag', 'A.doc^B.doc', True, '2.txt', 'B.doc', 'ag', 'ag'],
                ['ag', '2.txt^3.txt^4.txt', True, 'ag', 'A.doc^B.doc', True, '3.txt', 'A.doc', 'ag', 'ag'],
                ['ag', '2.txt^3.txt^4.txt', True, 'ag', 'A.doc^B.doc', True, '3.txt', 'B.doc', 'ag', 'ag'],
                ['ag', '2.txt^3.txt^4.txt', True, 'ag', 'A.doc^B.doc', True, '4.txt', 'A.doc', 'ag', 'ag'],
                ['ag', '2.txt^3.txt^4.txt', True, 'ag', 'A.doc^B.doc', True, '4.txt', 'B.doc', 'ag', 'ag']]
        df = make_df(rows)
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'apples')
        os.makedirs(topic_path)
        topics_sort_save_metadata(df, topic_path, 'apples')

        # Verifies the metadata csv has the correct contents.
        result = csv_to_list(os.path.join(topic_path, 'apples_metadata.csv'))
        expected = [['in_topic', 'in_document_name', 'in_document_name_present',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['ag', '1.txt^2.txt', 'True', 'ag', 'Apples.doc', 'True'],
                    ['ag', '2.txt^3.txt^4.txt', 'True', 'ag', 'A.doc^B.doc', 'True']]
        self.assertEqual(expected, result, "Problem with test for duplicate_doc")

    def test_duplicate_topic(self):
        """Test for when the df includes duplicate rows once the topic_split columns are removed"""
        # Makes test input and runs the function.
        rows = [['ag^apples', '1.txt', False, 'Apples', 'Apples.doc', True, '1.txt', 'Apples.doc', 'ag', 'Apples'],
                ['ag^apples', '1.txt', False, 'Apples', 'Apples.doc', True, '1.txt', 'Apples.doc', 'apples', 'Apples'],
                ['ag^apples', '2.txt', True, 'apples^reg', 'Ag.doc', True, '2.txt', 'Ag.doc', 'ag', 'apples'],
                ['ag^apples', '2.txt', True, 'apples^reg', 'Ag.doc', True, '2.txt', 'Ag.doc', 'apples', 'apples'],
                ['ag^apples', '2.txt', True, 'apples^reg', 'Ag.doc', True, '2.txt', 'Ag.doc', 'apples', 'reg'],
                ['apples', '3.txt', True, 'ag', 'Ag.doc', False, '3.txt', 'Ag.doc', 'apples', 'ag']]
        df = make_df(rows)
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'apples')
        os.makedirs(topic_path)
        topics_sort_save_metadata(df, topic_path, 'apples')

        # Verifies the metadata csv has the correct contents.
        result = csv_to_list(os.path.join(topic_path, 'apples_metadata.csv'))
        expected = [['in_topic', 'in_document_name', 'in_document_name_present',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['ag^apples', '1.txt', 'False', 'Apples', 'Apples.doc', 'True'],
                    ['ag^apples', '2.txt', 'True', 'apples^reg', 'Ag.doc', 'True'],
                    ['apples', '3.txt', 'True', 'ag', 'Ag.doc', 'False']]
        self.assertEqual(expected, result, "Problem with test for duplicate_topic")

    def test_not_found(self):
        """Test for when the df includes rows where neither document was found"""
        # Makes test input and runs the function.
        rows = [['apples', '1.txt', True, 'ag', 'Apples.doc', True, '1.txt', 'Apples.doc', 'apples', 'ag'],
                ['apples', '2.txt', False, 'ag', 'XApples.doc', False, '2.txt', 'XApples.doc', 'apples', 'ag'],
                ['apples', '3.txt', True, 'ag', 'XApple.doc', False, '3.txt', 'XApple.doc', 'apples', 'ag'],
                ['apples', '4.txt', False, 'ag', np.nan, 'TBD', '4.txt', np.nan, 'apples', 'ag'],
                ['apples', '5.txt', True, 'ag', np.nan, 'TBD', '5.txt', np.nan, 'apples', 'ag'],
                ['apples', np.nan, 'TBD', 'ag', 'XApples.doc', False, np.nan, 'XApples.doc', 'apples', 'ag'],
                ['apples', '7.txt', False, 'ag', 'Apples.doc', True, '7.txt', 'Apples.doc', 'apples', 'ag'],
                ['apples', np.nan, 'TBD', 'ag', 'Apples.doc', 'TBD', np.nan, 'Apples.doc', np.nan, 'ag'],
                ['apples', np.nan, 'TBD', 'ag', 'Apples.doc', True, np.nan, 'Apples.doc', 'apples', 'ag']]
        df = make_df(rows)
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'apples')
        os.makedirs(topic_path)
        topics_sort_save_metadata(df, topic_path, 'apples')

        # Verifies the metadata csv has the correct contents.
        result = csv_to_list(os.path.join(topic_path, 'apples_metadata.csv'))
        expected = [['in_topic', 'in_document_name', 'in_document_name_present',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['apples', '1.txt', 'True', 'ag', 'Apples.doc', 'True'],
                    ['apples', '3.txt', 'True', 'ag', 'XApple.doc', 'False'],
                    ['apples', '5.txt', 'True', 'ag', 'BLANK', 'no_path_provided'],
                    ['apples', '7.txt', 'False', 'ag', 'Apples.doc', 'True'],
                    ['apples', 'BLANK', 'no_path_provided', 'ag', 'Apples.doc', 'True']]
        self.assertEqual(expected, result, "Problem with test for not_found")

    def test_tbd(self):
        """Test for when the df includes TBD to be updated"""
        # Makes test input and runs the function.
        rows = [['ag', '1.txt', True, 'Apples', 'Apples.doc', True, '1.txt', 'Apples.doc', 'ag', 'Apples'],
                ['apples', np.nan, 'TBD', 'Apples', 'Apples.doc', True, np.nan, 'Apples.doc', 'apples', 'Apples'],
                ['apples', '3.txt', True, 'ag', np.nan, 'TBD', '3.txt', np.nan, 'apples', 'ag'],
                ['apples', np.nan, 'TBD', 'ag', 'Apples.doc', True, np.nan, 'Apples.doc', 'apples', 'ag']]
        df = make_df(rows)
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', 'apples')
        os.makedirs(topic_path)
        topics_sort_save_metadata(df, topic_path, 'apples')

        # Verifies the metadata csv has the correct contents.
        result = csv_to_list(os.path.join(topic_path, 'apples_metadata.csv'))
        expected = [['in_topic', 'in_document_name', 'in_document_name_present',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['ag', '1.txt', 'True', 'Apples', 'Apples.doc', 'True'],
                    ['apples', 'BLANK', 'no_path_provided', 'Apples', 'Apples.doc', 'True'],
                    ['apples', '3.txt', 'True', 'ag', 'BLANK', 'no_path_provided'],
                    ['apples', 'BLANK', 'no_path_provided', 'ag', 'Apples.doc', 'True']]
        self.assertEqual(expected, result, "Problem with test for TBD")
        
    def test_update_csv(self):
        """Test for when multiple topics normalize to the same topic folder and metadata.csv"""
        # Makes test input and runs the function to make the metadata.csv.
        rows = [['ag', '1.txt', True, '|apples|', 'Apples.doc', True, '1.txt', 'Apples.doc', 'ag', '|apples|']]
        df = make_df(rows)
        topic_path = os.path.join('test_data', 'topics_sort_save_metadata', '_apples_')
        os.makedirs(topic_path)
        topics_sort_save_metadata(df, topic_path, '_apples_')

        # Makes another df and runs the function to add to the metadata.csv.
        rows = [['<apples>', '2.txt', True, 'Apples', 'Apples.doc', True, '2.txt', 'Apples.doc', '<apples>', 'Apples'],
                ['<apples>', '3.txt', True, 'ag', 'Apples.doc', True, '3.txt', 'Apples.doc', '<apples>', 'ag'],
                ['<apples>', '4.txt', False, 'ag', 'Apples.doc', True, '4.txt', 'Apples.doc', '<apples>', 'ag']]
        df = make_df(rows)
        topics_sort_save_metadata(df, topic_path, '_apples_')

        # Verifies the metadata csv has the correct contents.
        result = csv_to_list(os.path.join(topic_path, '_apples__metadata.csv'))
        expected = [['in_topic', 'in_document_name', 'in_document_name_present',
                     'out_topic', 'out_document_name', 'out_document_name_present'],
                    ['ag', '1.txt', 'True', '|apples|', 'Apples.doc', 'True'],
                    ['<apples>', '2.txt', 'True', 'Apples', 'Apples.doc', 'True'],
                    ['<apples>', '3.txt', 'True', 'ag', 'Apples.doc', 'True'],
                    ['<apples>', '4.txt', 'False', 'ag', 'Apples.doc', 'True']]
        self.assertEqual(expected, result, "Problem with test for update_csv")


if __name__ == '__main__':
    unittest.main()
