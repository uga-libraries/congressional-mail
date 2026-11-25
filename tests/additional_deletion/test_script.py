import os
import pandas as pd
import shutil
import subprocess
import unittest


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path, dtype=str)
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the script output"""
        log_path = os.path.join('test_data', 'script', 'file_deletion_log_addition.csv')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_css_arch(self):
        """Test for the css_archiving format, which has deletion data in folders"""
        # Runs the script.
        script_path = os.path.join('..', '..', 'additional_deletion.py')
        delete_directory = os.path.join('test_data', 'script', 'css_archiving', 'delete')
        input_directory = os.path.join('test_data', 'script', 'css_archiving', 'export')
        output_directory = os.path.join('test_data', 'script')
        subprocess.run(f"python css_arch {script_path} {delete_directory} {input_directory} {output_directory}", shell=True)

        # Verifies the contents of the log.
        result = csv_to_list()
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes']]
        self.assertEqual(expected, result, "Problem with test for one_file")


if __name__ == '__main__':
    unittest.main()
