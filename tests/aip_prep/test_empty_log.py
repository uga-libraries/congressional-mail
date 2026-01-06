import datetime
import os
import unittest
from aip_prep import empty_log
from test_script import text_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the log, if made"""
        log_path = os.path.join(os.getcwd(), 'empty_subfolders_log.txt')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_new(self):
        """Test for making the log for the first time"""
        # Runs the function.
        output_dir = os.getcwd()
        empty_log(output_dir, 'C:/test/folder_empty')

        # Tests the contents of the empty subfolder log.
        result = text_to_list(os.path.join(output_dir, 'empty_subfolders_log.txt'))
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        expected = [f"The following folders were empty on {today} "
                    f"when this export was split into smaller folders for AIP creation and were not included "
                    f"in the final AIPs:\r\n", '\r\n',
                    "C:/test/folder_empty\r\n"]
        self.assertEqual(expected, result, "Problem with test for new log")

    def test_addition(self):
        """Test for adding a row to an existing log"""
        # Runs the function twice, once to make the log and once to add to the existing log.
        output_dir = os.getcwd()
        empty_log(output_dir, 'C:/test/empty_one')
        empty_log(output_dir, 'C:/test/empty_two')

        # Tests the contents of the empty subfolder log.
        result = text_to_list(os.path.join(output_dir, 'empty_subfolders_log.txt'))
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        expected = [f"The following folders were empty on {today} "
                    f"when this export was split into smaller folders for AIP creation and were not included "
                    f"in the final AIPs:\r\n", '\r\n',
                    "C:/test/empty_one\r\n",
                    "C:/test/empty_two\r\n"]
        self.assertEqual(expected, result, "Problem with test for addition to log")


if __name__ == '__main__':
    unittest.main()
