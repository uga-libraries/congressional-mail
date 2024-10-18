"""
Tests for the script css_archiving_format.py
"""
import os
import pandas as pd
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the script runs correctly."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')
        md_path = os.path.join('test_data', 'script_md.dat')
        output = subprocess.run(f"python {script_path} {md_path}", shell=True, stdout=subprocess.PIPE)

        # Tests that it prints the correct message.
        result = output.stdout.decode('utf-8')
        expected = ("\r\nColumns remaining in the constituent mail metadata after removing personal identifiers "
                    "are listed below.\r\nTo remove any of these columns from the metadata, add them to the 'remove' "
                    "list and run the script again.\r\n\tzip\r\n\tcountry\r\n\tin_id\r\n\tin_type\r\n\tin_method\r\n"
                    "\tin_date\r\n\tin_topic\r\n\tin_text\r\n\tin_document_name\r\n\tin_fillin\r\n\tout_id\r\n"
                    "\tout_type\r\n\tout_method\r\n\tout_date\r\n\tout_topic\r\n\tout_text\r\n\tout_document_name\r\n"
                    "\tout_fillin\r\n")
        self.assertEqual(result, expected, "Problem with test for correct, printed message")

    def test_error_argument(self):
        """Test for when the script exits due to an argument error."""
        script_path = os.path.join(os.getcwd(), '..', '..', 'css_archiving_format.py')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path}", shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script and tests that it prints the correct error.
        output = subprocess.run(f"python {script_path}", shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Missing required argument: path to the metadata file\r\n"
        self.assertEqual(result, expected, "Problem with test for error argument, printed error")


if __name__ == '__main__':
    unittest.main()
