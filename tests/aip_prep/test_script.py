"""
Tests for the function split_aip(), which makes a folder for every 10,000 files and starts the metadata.csv
for transforming these folders into AIPs for the preservation system.
"""
from datetime import datetime
import os
import pandas as pd
import shutil
import subprocess
import unittest


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path)
    df = df.fillna('BLANK')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


def files_per_dir(dir_path):
    """Make a list of lists with the path for every folder and the number of files in that folder to test results,
    since there are too many test files used to check each file path"""
    file_count = []
    for root, dirs, files in os.walk(dir_path):
        file_count.append([root, len(files)])
    return file_count


def make_input_folder(folder_path, file_count):
    """Make a folder with the specified name and number of files for test input,
    since the needed number of files is larger than we want to store in a GitHub repo"""
    os.makedirs(folder_path)
    for i in range(1, file_count + 1):
        file_path = os.path.join(folder_path, f'file_{i}.txt')
        with open(file_path, 'w') as file:
            file.write("Test input")


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the script input and output"""
        shutil.rmtree(os.path.join(os.getcwd(), 'test_data'))

    def test_no_subfolders(self):
        """Test for when the type folders have no subfolders, with a mix of 1 and multiple AIPs per type"""
        # Makes the input directory with test data.
        input_directory = os.path.join(os.getcwd(), 'test_data', 'export')
        make_input_folder(input_directory, 3)  # act as metadata files
        make_input_folder(os.path.join(input_directory, 'documents', 'CASE'), 2500)
        make_input_folder(os.path.join(input_directory, 'documents', 'Indivletters'), 10001)
        make_input_folder(os.path.join(input_directory, 'documents', 'Objects'), 20123)
        
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'aip_prep.py')
        subprocess.run(f"python {script_path} {input_directory}", shell=True, capture_output=True, text=True)

        # Tests the aips_dir has the correct contents.
        aips_dir = os.path.join(os.getcwd(), 'test_data', 'aips_dir')
        result = files_per_dir(aips_dir)
        expected = [[aips_dir, 1],
                    [os.path.join(aips_dir, 'case_1'), 2500],
                    [os.path.join(aips_dir, 'indivletters_1'), 10000],
                    [os.path.join(aips_dir, 'indivletters_2'), 1],
                    [os.path.join(aips_dir, 'metadata'), 3],
                    [os.path.join(aips_dir, 'objects_1'), 10000],
                    [os.path.join(aips_dir, 'objects_2'), 10000],
                    [os.path.join(aips_dir, 'objects_3'), 123]]
        self.assertEqual(expected, result, "Problem with test for no_subfolders, aips_dir")

        # Tests the metadata.csv has the correct values.
        result = csv_to_list(os.path.join(aips_dir, 'metadata.csv'))
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'],
                    ['BLANK', 'BLANK', 'metadata', 'BLANK', 'CSS Metadata', 1],
                    ['BLANK', 'BLANK', 'case_1', 'BLANK', 'CSS CASE 1', 1],
                    ['BLANK', 'BLANK', 'indivletters_1', 'BLANK', 'CSS Indivletters 1', 1],
                    ['BLANK', 'BLANK', 'indivletters_2', 'BLANK', 'CSS Indivletters 2', 1],
                    ['BLANK', 'BLANK', 'objects_1', 'BLANK', 'CSS Objects 1', 1],
                    ['BLANK', 'BLANK', 'objects_2', 'BLANK', 'CSS Objects 2', 1],
                    ['BLANK', 'BLANK', 'objects_3', 'BLANK', 'CSS Objects 3', 1]]
        self.assertEqual(expected, result, "Problem with test for no_subfolders, metadata.csv")

    def test_subfolders(self):
        """Test for when the type folders have subfolders, with a mix of 1 and multiple AIPs per type"""
        # Makes the input directory with test data.
        input_directory = os.path.join(os.getcwd(), 'test_data', 'export')
        make_input_folder(input_directory, 3)
        make_input_folder(os.path.join(input_directory, 'documents', 'form', 'a'), 1)
        make_input_folder(os.path.join(input_directory, 'documents', 'form', 'a', 'aa'), 2)
        make_input_folder(os.path.join(input_directory, 'documents', 'form', 'a', 'ab'), 10000)
        make_input_folder(os.path.join(input_directory, 'documents', 'indivletters', 'cats'), 20)
        make_input_folder(os.path.join(input_directory, 'documents', 'indivletters', 'dogs'), 10)
        make_input_folder(os.path.join(input_directory, 'documents', 'objects', 'apples'), 10001)
        make_input_folder(os.path.join(input_directory, 'documents', 'objects', 'bananas'), 20002)

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'aip_prep.py')
        subprocess.run(f"python {script_path} {input_directory}", shell=True, capture_output=True, text=True)

        # Tests the aips_dir has the correct contents.
        aips_dir = os.path.join(os.getcwd(), 'test_data', 'aips_dir')
        result = files_per_dir(aips_dir)
        expected = [[aips_dir, 1],
                    [os.path.join(aips_dir, 'form_1'), 0],
                    [os.path.join(aips_dir, 'form_1', 'a'), 1],
                    [os.path.join(aips_dir, 'form_1', 'a', 'aa'), 2],
                    [os.path.join(aips_dir, 'form_1', 'a', 'ab'), 9997],
                    [os.path.join(aips_dir, 'form_2'), 0],
                    [os.path.join(aips_dir, 'form_2', 'a', ), 0],
                    [os.path.join(aips_dir, 'form_2', 'a', 'ab'), 3],
                    [os.path.join(aips_dir, 'indivletters_1'), 0],
                    [os.path.join(aips_dir, 'indivletters_1', 'cats'), 20],
                    [os.path.join(aips_dir, 'indivletters_1', 'dogs'), 10],
                    [os.path.join(aips_dir, 'metadata'), 3],
                    [os.path.join(aips_dir, 'objects_1'), 0],
                    [os.path.join(aips_dir, 'objects_1', 'apples'), 10000],
                    [os.path.join(aips_dir, 'objects_2'), 0],
                    [os.path.join(aips_dir, 'objects_2', 'apples'), 1],
                    [os.path.join(aips_dir, 'objects_2', 'bananas'), 9999],
                    [os.path.join(aips_dir, 'objects_3'), 0],
                    [os.path.join(aips_dir, 'objects_3', 'bananas'), 10000],
                    [os.path.join(aips_dir, 'objects_4'), 0],
                    [os.path.join(aips_dir, 'objects_4', 'bananas'), 3]]
        self.assertEqual(expected, result, "Problem with test for subfolders, aips_dir")

        # Tests the metadata.csv has the correct values.
        result = csv_to_list(os.path.join(aips_dir, 'metadata.csv'))
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'],
                    ['BLANK', 'BLANK', 'metadata', 'BLANK', 'CSS Metadata', 1],
                    ['BLANK', 'BLANK', 'form_1', 'BLANK', 'CSS form 1', 1],
                    ['BLANK', 'BLANK', 'form_2', 'BLANK', 'CSS form 2', 1],
                    ['BLANK', 'BLANK', 'indivletters_1', 'BLANK', 'CSS indivletters 1', 1],
                    ['BLANK', 'BLANK', 'objects_1', 'BLANK', 'CSS objects 1', 1],
                    ['BLANK', 'BLANK', 'objects_2', 'BLANK', 'CSS objects 2', 1],
                    ['BLANK', 'BLANK', 'objects_3', 'BLANK', 'CSS objects 3', 1],
                    ['BLANK', 'BLANK', 'objects_4', 'BLANK', 'CSS objects 4', 1]]
        self.assertEqual(expected, result, "Problem with test for subfolders, metadata.csv")

    def test_subfolders_empty(self):
        """Test for when the type folder includes empty subfolders"""
        # Makes the input directory with test data.
        input_directory = os.path.join(os.getcwd(), 'test_data', 'export')
        make_input_folder(input_directory, 1)
        make_input_folder(os.path.join(input_directory, 'documents', 'indivletters'), 2)
        make_input_folder(os.path.join(input_directory, 'documents', 'indivletters', 'lions'), 3)
        make_input_folder(os.path.join(input_directory, 'documents', 'indivletters', 'bears'), 0),
        make_input_folder(os.path.join(input_directory, 'documents', 'indivletters', 'tigers'), 0)

        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'aip_prep.py')
        subprocess.run(f"python {script_path} {input_directory}", shell=True, capture_output=True, text=True)

        # Tests the aips_dir has the correct contents.
        aips_dir = os.path.join(os.getcwd(), 'test_data', 'aips_dir')
        result = files_per_dir(aips_dir)
        expected = [[aips_dir, 1],
                    [os.path.join(aips_dir, 'indivletters_1'), 2],
                    [os.path.join(aips_dir, 'indivletters_1', 'lions'), 3],
                    [os.path.join(aips_dir, 'metadata'), 1]]
        self.assertEqual(expected, result, "Problem with test for subfolders, aips_dir")

        # Tests the metadata.csv has the correct values.
        result = csv_to_list(os.path.join(aips_dir, 'metadata.csv'))
        expected = [['Department', 'Collection', 'Folder', 'AIP_ID', 'Title', 'Version'],
                    ['BLANK', 'BLANK', 'metadata', 'BLANK', 'CSS Metadata', 1],
                    ['BLANK', 'BLANK', 'indivletters_1', 'BLANK', 'CSS indivletters 1', 1]]
        self.assertEqual(expected, result, "Problem with test for subfolders, metadata.csv")

        # Tests the empty_subfolders_log.txt has the correct values.
        result = []
        with open(os.path.join(os.getcwd(), 'test_data', 'empty_subfolders_log.txt'), newline='\n') as log:
            rows = log.readlines()
            for row in rows:
                result.append(row)
        today = datetime.now().strftime("%Y-%m-%d")
        expected = [f"{os.path.join(input_directory, 'documents', 'indivletters', 'bears')} "
                    f"was empty on {today} when this export was split into smaller folders for AIP creation\r\n",
                    f"{os.path.join(input_directory, 'documents', 'indivletters', 'tigers')} "
                    f"was empty on {today} when this export was split into smaller folders for AIP creation\r\n"]
        self.assertEqual(expected, result, "Problem with test for subfolders_empty, empty_subfolders_log.txt")


if __name__ == '__main__':
    unittest.main()
