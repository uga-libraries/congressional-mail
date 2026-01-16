import numpy as np
import os
import pandas as pd
import unittest
from css_archiving_format import check_metadata_formatting_multi
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the reports, if made by the test"""
        columns = ['in_document_name', 'out_document_name']
        for column in columns:
            report_path = os.path.join('test_data', f'metadata_formatting_errors_{column}.csv')
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_blob(self):
        """Test for the BlobExport pattern, including correct cells, formatting errors, and blanks"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30601', '..\\documents\\BlobExport\\folder1\\file1.txt'],
                           ['30602', 'root\\documents\\BlobExport\\foldera\\filea.txt'],
                           ['30603', '..\\documents\\BlobExport\\folder1\\folder2\\file2.txt'],
                           ['30604', np.nan],
                           ['30605', '..\\documents\\BlobExport\\file3.txt'],
                           ['30606', 'dir\\..\\documents\\BlobExport\\folder1\\file1.txt'],
                           ['30607', 'fileb.txt']],
                          columns=['zip', 'in_document_name'])
        in_document_name_mismatch = check_metadata_formatting_multi('in_document_name', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(3, in_document_name_mismatch, "Problem with test for blob, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_in_document_name.csv'))
        expected = [['zip', 'in_document_name'],
                    ['30602', 'root\\documents\\BlobExport\\foldera\\filea.txt'],
                    ['30606', 'dir\\..\\documents\\BlobExport\\folder1\\file1.txt'],
                    ['30607', 'fileb.txt']]
        self.assertEqual(expected, result, "Problem with test for blob, report")

    def test_dos(self):
        """Test for the dos pattern, including correct cells, formatting errors, and blanks"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30601', '\\\\smith-atlanta\\dos\\public\\folder1\\file1.txt'],
                           ['30602', 'root\\\\smith-atlanta\\dos\\public\\foldera\\filea.txt'],
                           ['30603', '\\\\smith-atlanta\\dos\\public\\folder1\\folder2\\file2.txt'],
                           ['30604', np.nan],
                           ['30605', '\\\\smith-atlanta\\dos\\public\\file3.txt'],
                           ['30606', 'dir\\\\smith-atlanta\\dos\\public\\folder1\\file1.txt'],
                           ['30607', np.nan]],
                          columns=['zip', 'out_document_name'])
        out_document_name_mismatch = check_metadata_formatting_multi('out_document_name', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(2, out_document_name_mismatch, "Problem with test for dos, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_out_document_name.csv'))
        expected = [['zip', 'out_document_name'],
                    ['30602', 'root\\\\smith-atlanta\\dos\\public\\foldera\\filea.txt'],
                    ['30606', 'dir\\\\smith-atlanta\\dos\\public\\folder1\\file1.txt']]
        self.assertEqual(expected, result, "Problem with test for dos, report")

    def test_e(self):
        """Test for the e\\: pattern, including correct cells, formatting errors, and blanks"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30601', 'e:\\emailobj\\200101\\416120451.txt'],
                           ['30602', 'root\\e:\\emailobj\\200202\\416120451.txt'],
                           ['30603', 'e:\\emailobj\\200303\\416120451.txt'],
                           ['30604', np.nan]],
                          columns=['zip', 'out_document_name'])
        out_document_name_mismatch = check_metadata_formatting_multi('out_document_name', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(1, out_document_name_mismatch, "Problem with test for e, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_out_document_name.csv'))
        expected = [['zip', 'out_document_name'],
                    ['30602', 'root\\e:\\emailobj\\200202\\416120451.txt']]
        self.assertEqual(expected, result, "Problem with test for e, report")

    def test_column_blank(self):
        """Test for when the column is blank"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30601', np.nan],
                           ['30602', np.nan],
                           ['30603', np.nan],
                           ['30604', np.nan],
                           ['30605', np.nan]],
                          columns=['zip', 'out_document_name'])
        out_document_name_mismatch = check_metadata_formatting_multi('out_document_name', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual('column_blank', out_document_name_mismatch, "Problem with test for 'column_blank', count")

        # Tests the report was not made
        result = os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_out_document_name.csv'))
        expected = False
        self.assertEqual(expected, result, "Problem with test for 'column_blank', report")

    def test_column_missing(self):
        """Test for when the column is missing"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30601', '..\\documents\\BlobExport\\folder1\\file1.txt'],
                           ['30602', '..\\documents\\BlobExport\\folder2\\file2.txt'],
                           ['30603', '\\\\smith-atlanta\\dos\\public\\folder1\\folder2\\file1.txt'],
                           ['30604', '\\\\smith-atlanta\\dos\\public\\folder1\\folder2\\file2.txt'],
                           ['30605', '..\\documents\\BlobExport\\folder2\\file3.txt']],
                          columns=['zip', 'in_document_name'])
        out_document_name_mismatch = check_metadata_formatting_multi('out_document_name', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual('column_missing', out_document_name_mismatch, "Problem with test for column_missing, count")

        # Tests the report was not made
        result = os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_out_document_name.csv'))
        expected = False
        self.assertEqual(expected, result, "Problem with test for column_missing, report")

    def test_no_errors(self):
        """Test for both patterns when there are no errors or blanks"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30601', '..\\documents\\BlobExport\\folder1\\file1.txt'],
                           ['30602', '..\\documents\\BlobExport\\folder2\\file2.txt'],
                           ['30603', '\\\\smith-atlanta\\dos\\public\\folder1\\folder2\\file1.txt'],
                           ['30604', '\\\\smith-atlanta\\dos\\public\\folder1\\folder2\\file2.txt'],
                           ['30605', '..\\documents\\BlobExport\\folder2\\file3.txt']],
                          columns=['zip', 'out_document_name'])
        out_document_name_mismatch = check_metadata_formatting_multi('out_document_name', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(0, out_document_name_mismatch, "Problem with test for no errors, count")

        # Tests the report was not made
        result = os.path.exists(os.path.join('test_data', 'metadata_formatting_errors_out_document_name.csv'))
        expected = False
        self.assertEqual(expected, result, "Problem with test for no errors, report")

    def test_only_errors(self):
        """Test for when there are only errors, no correct or blanks"""
        # Makes a dataframe to use as test input and runs the function.
        df = pd.DataFrame([['30601', '..\\documents\\folder1\\file1.txt'],
                           ['30602', '..\\documents\\file2.txt'],
                           ['30603', '\\public\\file1.txt'],
                           ['30604', 'file2.txt']],
                          columns=['zip', 'out_document_name'])
        out_document_name_mismatch = check_metadata_formatting_multi('out_document_name', df, 'test_data')

        # Tests the returned row count is correct.
        self.assertEqual(4, out_document_name_mismatch, "Problem with test for only errors, count")

        # Tests the values in the report are correct.
        result = csv_to_list(os.path.join('test_data', 'metadata_formatting_errors_out_document_name.csv'))
        expected = [['zip', 'out_document_name'],
                    ['30601', '..\\documents\\folder1\\file1.txt'],
                    ['30602', '..\\documents\\file2.txt'],
                    ['30603', '\\public\\file1.txt'],
                    ['30604', 'file2.txt']]
        self.assertEqual(expected, result, "Problem with test for only, report")


if __name__ == '__main__':
    unittest.main()
