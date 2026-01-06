import os
import shutil
import unittest
from aip_prep import metadata_csv, type_aip, type_files
from test_script import csv_to_list, files_per_dir, make_input_folder


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the script input and output"""
        shutil.rmtree(os.path.join(os.getcwd(), 'test_data'))

    def test_no_sub_multi(self):
        """Test for when the type folder has no subfolders and enough files to be multiple AIPs"""
        # Makes test data, folders, and metadata.csv and runs the function.
        aips_dir = os.path.join(os.getcwd(), 'test_data', 'aips_dir')
        input_dir = os.path.join(os.getcwd(), 'test_data', 'export')
        metadata_path = os.path.join(aips_dir, 'metadata.csv')
        output_dir = os.path.join(os.getcwd(), 'test_data')
        type_path = os.path.join(input_dir, 'documents', 'Form')
        make_input_folder(type_path, 20001)
        os.mkdir(aips_dir)
        metadata_csv(metadata_path, 'header')
        paths_list = type_files(output_dir, type_path)
        type_aip(aips_dir, metadata_path, paths_list, type_path)

        # Tests the aips_dir has the correct contents.
        result = files_per_dir(aips_dir)
        expected = [[aips_dir, 1],
                    [os.path.join(aips_dir, 'form_1'), 10000],
                    [os.path.join(aips_dir, 'form_2'), 10000],
                    [os.path.join(aips_dir, 'form_3'), 1]]
        self.assertEqual(expected, result, "Problem with test for no_sub_multi, aips_dir")

        # Tests the metadata.csv has the correct values.
        result = csv_to_list(metadata_path)
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'],
                    ['BLANK', 'BLANK', 'form_1', 'BLANK', 'Constituent Mail Form 1', 1],
                    ['BLANK', 'BLANK', 'form_2', 'BLANK', 'Constituent Mail Form 2', 1],
                    ['BLANK', 'BLANK', 'form_3', 'BLANK', 'Constituent Mail Form 3', 1]]
        self.assertEqual(expected, result, "Problem with test for no_sub_multi, metadata.csv")

    def test_no_sub_one(self):
        """Test for when the type folder has no subfolders and few enough files to be a single AIP"""
        # Makes test data, folders, and metadata.csv and runs the function.
        aips_dir = os.path.join(os.getcwd(), 'test_data', 'aips_dir')
        input_dir = os.path.join(os.getcwd(), 'test_data', 'export')
        metadata_path = os.path.join(aips_dir, 'metadata.csv')
        output_dir = os.path.join(os.getcwd(), 'test_data')
        type_path = os.path.join(input_dir, 'documents', 'FORM')
        make_input_folder(type_path, 25)
        os.mkdir(aips_dir)
        metadata_csv(metadata_path, 'header')
        paths_list = type_files(output_dir, type_path)
        type_aip(aips_dir, metadata_path, paths_list, type_path)

        # Tests the aips_dir has the correct contents.
        result = files_per_dir(aips_dir)
        expected = [[aips_dir, 1],
                    [os.path.join(aips_dir, 'form_1'), 25]]
        self.assertEqual(expected, result, "Problem with test for no_sub_one, aips_dir")

        # Tests the metadata.csv has the correct values.
        result = csv_to_list(metadata_path)
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'],
                    ['BLANK', 'BLANK', 'form_1', 'BLANK', 'Constituent Mail FORM 1', 1]]
        self.assertEqual(expected, result, "Problem with test for no_sub_one, metadata.csv")

    def test_sub_combo(self):
        """Test for when the type folder has subfolders, each with few enough files to be combined in an AIP"""
        # Makes test data, folders, and metadata.csv and runs the function.
        aips_dir = os.path.join(os.getcwd(), 'test_data', 'aips_dir')
        input_dir = os.path.join(os.getcwd(), 'test_data', 'export')
        metadata_path = os.path.join(aips_dir, 'metadata.csv')
        output_dir = os.path.join(os.getcwd(), 'test_data')
        type_path = os.path.join(input_dir, 'documents', 'form')
        make_input_folder(type_path, 5000)
        make_input_folder(os.path.join(type_path, 'cats'), 5000)
        make_input_folder(os.path.join(type_path, 'cows'), 10)
        make_input_folder(os.path.join(type_path, 'dogs'), 20)
        make_input_folder(os.path.join(type_path, 'fish'), 30)
        os.mkdir(aips_dir)
        metadata_csv(metadata_path, 'header')
        paths_list = type_files(output_dir, type_path)
        type_aip(aips_dir, metadata_path, paths_list, type_path)

        # Tests the aips_dir has the correct contents.
        result = files_per_dir(aips_dir)
        expected = [[aips_dir, 1],
                    [os.path.join(aips_dir, 'form_1'), 5000],
                    [os.path.join(aips_dir, 'form_1', 'cats'), 5000],
                    [os.path.join(aips_dir, 'form_2'), 0],
                    [os.path.join(aips_dir, 'form_2', 'cows'), 10],
                    [os.path.join(aips_dir, 'form_2', 'dogs'), 20],
                    [os.path.join(aips_dir, 'form_2', 'fish'), 30]]
        self.assertEqual(expected, result, "Problem with test for sub_combo, aips_dir")

        # Tests the metadata.csv has the correct values.
        result = csv_to_list(metadata_path)
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'],
                    ['BLANK', 'BLANK', 'form_1', 'BLANK', 'Constituent Mail form 1', 1],
                    ['BLANK', 'BLANK', 'form_2', 'BLANK', 'Constituent Mail form 2', 1]]
        self.assertEqual(expected, result, "Problem with test for sub_combo, metadata.csv")

    def test_sub_one(self):
        """Test for when the type folder has subfolders, each with enough files to be a separate AIP"""
        # Makes test data, folders, and metadata.csv and runs the function.
        aips_dir = os.path.join(os.getcwd(), 'test_data', 'aips_dir')
        input_dir = os.path.join(os.getcwd(), 'test_data', 'export')
        metadata_path = os.path.join(aips_dir, 'metadata.csv')
        output_dir = os.path.join(os.getcwd(), 'test_data')
        type_path = os.path.join(input_dir, 'documents', 'form')
        make_input_folder(type_path, 10000)
        make_input_folder(os.path.join(type_path, 'cats'), 10000)
        make_input_folder(os.path.join(type_path, 'dogs'), 10)
        os.mkdir(aips_dir)
        metadata_csv(metadata_path, 'header')
        paths_list = type_files(output_dir, type_path)
        type_aip(aips_dir, metadata_path, paths_list, type_path)

        # Tests the aips_dir has the correct contents.
        result = files_per_dir(aips_dir)
        expected = [[aips_dir, 1],
                    [os.path.join(aips_dir, 'form_1'), 10000],
                    [os.path.join(aips_dir, 'form_2'), 0],
                    [os.path.join(aips_dir, 'form_2', 'cats'), 10000],
                    [os.path.join(aips_dir, 'form_3'), 0],
                    [os.path.join(aips_dir, 'form_3', 'dogs'), 10]]
        self.assertEqual(expected, result, "Problem with test for sub_one, aips_dir")

        # Tests the metadata.csv has the correct values.
        result = csv_to_list(metadata_path)
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'],
                    ['BLANK', 'BLANK', 'form_1', 'BLANK', 'Constituent Mail form 1', 1],
                    ['BLANK', 'BLANK', 'form_2', 'BLANK', 'Constituent Mail form 2', 1],
                    ['BLANK', 'BLANK', 'form_3', 'BLANK', 'Constituent Mail form 3', 1]]
        self.assertEqual(expected, result, "Problem with test for sub_one, metadata.csv")

    def test_sub_split(self):
        """Test for when the type folder has subfolders, each with enough files to be spit across AIPs"""
        # Makes test data, folders, and metadata.csv and runs the function.
        aips_dir = os.path.join(os.getcwd(), 'test_data', 'aips_dir')
        input_dir = os.path.join(os.getcwd(), 'test_data', 'export')
        metadata_path = os.path.join(aips_dir, 'metadata.csv')
        output_dir = os.path.join(os.getcwd(), 'test_data')
        type_path = os.path.join(input_dir, 'documents', 'form')
        make_input_folder(type_path, 10001)
        make_input_folder(os.path.join(type_path, 'cats'), 10004)
        make_input_folder(os.path.join(type_path, 'fish'), 10000)
        os.mkdir(aips_dir)
        metadata_csv(metadata_path, 'header')
        paths_list = type_files(output_dir, type_path)
        type_aip(aips_dir, metadata_path, paths_list, type_path)

        # Tests the aips_dir has the correct contents.
        result = files_per_dir(aips_dir)
        expected = [[aips_dir, 1],
                    [os.path.join(aips_dir, 'form_1'), 10000],
                    [os.path.join(aips_dir, 'form_2'), 1],
                    [os.path.join(aips_dir, 'form_2', 'cats'), 9999],
                    [os.path.join(aips_dir, 'form_3'), 0],
                    [os.path.join(aips_dir, 'form_3', 'cats'), 5],
                    [os.path.join(aips_dir, 'form_3', 'fish'), 9995],
                    [os.path.join(aips_dir, 'form_4'), 0],
                    [os.path.join(aips_dir, 'form_4', 'fish'), 5]]
        self.assertEqual(expected, result, "Problem with test for sub_split, aips_dir")

        # Tests the metadata.csv has the correct values.
        result = csv_to_list(metadata_path)
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'],
                    ['BLANK', 'BLANK', 'form_1', 'BLANK', 'Constituent Mail form 1', 1],
                    ['BLANK', 'BLANK', 'form_2', 'BLANK', 'Constituent Mail form 2', 1],
                    ['BLANK', 'BLANK', 'form_3', 'BLANK', 'Constituent Mail form 3', 1],
                    ['BLANK', 'BLANK', 'form_4', 'BLANK', 'Constituent Mail form 4', 1]]
        self.assertEqual(expected, result, "Problem with test for sub_spit, metadata.csv")


if __name__ == '__main__':
    unittest.main()
