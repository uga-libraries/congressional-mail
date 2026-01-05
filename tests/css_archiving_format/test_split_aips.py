"""
Tests for the function split_aip(), which makes a folder for every 10,000 files and starts the metadata.csv
for transforming these folders into AIPs for the preservation system.
"""
import os
import shutil
import unittest
from css_archiving_format import split_aips
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    # def tearDown(self):
    #     """Delete the function input and output"""
    #     output_directory = os.path.join('test_data', 'split_aips')
    #     shutil.rmtree(output_directory)

    def test_function(self):
        # Starting test for initial development.
        output_directory = os.path.join(os.getcwd(), 'test_data', 'split_aips')
        os.mkdir(output_directory)

        input_directory = 'TBD - put in split_aips'
        split_aips(input_directory, output_directory)


if __name__ == '__main__':
    unittest.main()
