"""
Tests for the function remove_casework_letters(), which removes letters received or sent that pertain to casework.
"""
import os
import shutil
import unittest
from css_archiving_format import remove_casework_letters


def files_in_dir(dir_path):
    """Make a list of every file in a directory, for testing the result of the function"""
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_list.append(file)
    return file_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(os.path.join('test_data', 'remove_casework_letters', 'css_export')):
            shutil.rmtree(os.path.join('test_data', 'remove_casework_letters', 'css_export'))

    def test_function(self):
        """Initial test for the development of the function"""
        # Makes a copy of the test data in the repo, since the script alters the data.
        shutil.copytree(os.path.join('test_data', 'remove_casework_letters', 'css_export_copy'),
                        os.path.join('test_data', 'remove_casework_letters', 'css_export'))

        input_directory = os.path.join('test_data', 'remove_casework_letters', 'css_export')
        remove_casework_letters(input_directory)

        result = files_in_dir(input_directory)
        expected = ['form_a.txt', 'test.txt', '100.txt']
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
