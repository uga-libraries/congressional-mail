import datetime
import os
import unittest
from aip_prep import type_files
from test_script import text_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the log, if made"""
        log_path = os.path.join(os.getcwd(), 'type_files', 'empty_subfolders_log.txt')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_empty_subfolder(self):
        """Test for when the type folder includes an empty subfolder"""
        # Makes variables needed as function input and runs the function.
        output_dir = os.path.join(os.getcwd(), 'type_files')
        type_path = os.path.join(output_dir, 'empty_subfolder')
        result = type_files(output_dir, type_path)

        # Tests the file_paths_list returned by the function.
        expected = [os.path.join(type_path, 'Document.txt'),
                    os.path.join(type_path, 'folder_a', 'folder_aa', 'Document.txt')]
        self.assertEqual(expected, result, "Problem with test for empty_subfolder, list")

        # Tests the contents of the empty_subfolders_log.txt.
        result = text_to_list(os.path.join(output_dir, 'empty_subfolders_log.txt'))
        today = datetime.date.today()
        expected = [f'The following folders were empty on {today} when this export was split into smaller folders '
                    f'for AIP creation and were not included in the final AIPs:\r\n', '\r\n',
                    f"{os.path.join(type_path, 'folder_empty')}\r\n"]
        self.assertEqual(result, expected, "Problem with test for empty_subfolder, log")

    def test_files_only(self):
        """Test for when the type folder has no subfolder"""
        # Makes variables needed as function input and runs the function.
        output_dir = os.path.join(os.getcwd(), 'type_files')
        type_path = os.path.join(output_dir, 'files_only')
        result = type_files(output_dir, type_path)

        # Tests the file_paths_list returned by the function.
        expected = [os.path.join(type_path, 'Document.txt'),
                    os.path.join(type_path, 'Document2.txt')]
        self.assertEqual(expected, result, "Problem with test for files_only")

    def test_subfolders(self):
        """Test for when the type folder includes subfolders"""
        # Makes variables needed as function input and runs the function.
        output_dir = os.path.join(os.getcwd(), 'type_files')
        type_path = os.path.join(output_dir, 'subfolders')
        result = type_files(output_dir, type_path)

        # Tests the file_paths_list returned by the function.
        expected = [os.path.join(type_path, 'Document.txt'),
                    os.path.join(type_path, 'folder_a', 'Document.txt'),
                    os.path.join(type_path, 'folder_b', 'Document.txt'),
                    os.path.join(type_path, 'folder_b', 'folder_bb', 'folder_bbb', 'Document2.txt')]
        self.assertEqual(expected, result, "Problem with test for subfolders")


if __name__ == '__main__':
    unittest.main()
