"""
Tests for the script archival_office_correspondence_data.py
"""
import os
import pandas as pd
import subprocess
import unittest


def csv_to_list(csv_path):
    """Convert the contents of a CSV to a list which contains one list per row for easier comparison"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('nan')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Remove script outputs, if they were made"""
        filenames = ['CSS_Access_Copy.csv', '1997-1998.csv', 'undated.csv']
        for filename in filenames:
            file_path = os.path.join('test_data', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_correct(self):
        """Test for when the script runs correctly."""
        # Runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'archival_office_correspondence_data.py')
        md_path = os.path.join('test_data', 'script_md.dat')
        output = subprocess.run(f"python {script_path} {md_path}", shell=True, stdout=subprocess.PIPE)

        # Tests that it prints the correct message.
        result = output.stdout.decode('utf-8')
        expected = ()
        self.assertEqual(result, expected, "Problem with test for correct, printed message")

        # Tests the contents of CSS_Access_Copy.csv.
        csv_path = os.path.join('test_data', 'CSS_Access_Copy.csv')
        result = csv_to_list(csv_path)
        expected = []
        self.assertEqual(result, expected, "Problem with test for correct, CSS_Access_Copy.csv")

        # Tests the contents of 1997-1998.csv.
        csv_path = os.path.join('test_data', '1997-1998.csv')
        result = csv_to_list(csv_path)
        expected = []
        self.assertEqual(result, expected, "Problem with test for correct, 1997-1998")

        # Tests the contents of undated.csv.
        csv_path = os.path.join('test_data', 'undated.csv')
        result = csv_to_list(csv_path)
        expected = []
        self.assertEqual(result, expected, "Problem with test for correct, undated")

        
if __name__ == '__main__':
    unittest.main()
