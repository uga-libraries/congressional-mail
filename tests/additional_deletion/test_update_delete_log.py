import csv
from datetime import date
import os
import pandas as pd
import unittest
from additional_deletion import update_delete_log


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path, dtype=str)
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the log, which needs to be made fresh for each test"""
        os.remove(self.deletion_log_path)

    def setUp(self):
        """Makes a log with a header, which is done before this function is run"""
        self.deletion_log_path = os.path.join('test_data', 'update_delete_log', 'file_deletion_log_addition.csv')
        with open(self.deletion_log_path, 'w', newline='') as deletion_log:
            deletion_log_writer = csv.writer(deletion_log)
            deletion_log_writer.writerow(['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'])

    def test_one_file(self):
        """Test for when the first file is added to the log"""
        # Runs the function being tested.
        delete_file_path = os.path.join('test_data', 'update_delete_log', 'first.txt')
        update_delete_log(self.deletion_log_path, delete_file_path)

        # Verifies the contents of the log.
        result = csv_to_list(self.deletion_log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [delete_file_path, '0.9', '2026-11-25', date.today().strftime('%Y-%m-%d'),
                     '03AEF5F2106BF4BF76686FE2A1990403', 'Additional deletion: ADD REASON']]
        self.assertEqual(expected, result, "Problem with test for one_file")

    def test_two_file(self):
        """Test for when two files are added to the log"""
        # Adds the first file.
        delete_file_path_1 = os.path.join('test_data', 'update_delete_log', 'first.txt')
        update_delete_log(self.deletion_log_path, delete_file_path_1)

        # Adds the second file.
        delete_file_path_2 = os.path.join('test_data', 'update_delete_log', 'second.txt')
        update_delete_log(self.deletion_log_path, delete_file_path_2)

        # Verifies the contents of the log.
        result = csv_to_list(self.deletion_log_path)
        expected = [['File', 'SizeKB', 'DateCreated', 'DateDeleted', 'MD5', 'Notes'],
                    [delete_file_path_1, '0.9', '2026-11-25', date.today().strftime('%Y-%m-%d'),
                     '03AEF5F2106BF4BF76686FE2A1990403', 'Additional deletion: ADD REASON'],
                    [delete_file_path_2, '3.1', '2026-11-25', date.today().strftime('%Y-%m-%d'),
                     'D27A6FB5D63CDF6E66890E7658E89FD7', 'Additional deletion: ADD REASON']]
        self.assertEqual(expected, result, "Problem with test for two_files")


if __name__ == '__main__':
    unittest.main()
