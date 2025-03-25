"""
Tests for the function update_path(), which converts the path in the metadata to the file path in the export.
"""
import unittest
from css_archiving_format import update_path


class MyTestCase(unittest.TestCase):

    def test_blobexport(self):
        """Test for the pattern ..\\documents\\BlobExport\\folder\\..\\file.ext"""
        file_path = update_path(r'..\documents\BlobExport\formletters\form_a.txt', 'input_dir')
        expected = r'input_dir\documents\formletters\form_a.txt'
        self.assertEqual(file_path, expected, "Problem with test for BlobExport")

    def test_dos(self):
        """Test for the pattern \\\\name-office\\dos\\public\\folder\\..\\file.ext"""
        file_path = update_path(r'\\office-dc\dos\public\letter\111111.txt', 'input_dir')
        expected = r'input_dir\documents\letter\111111.txt'
        self.assertEqual(file_path, expected, "Problem with test for Dos")

    def test_new(self):
        """Test for a new pattern"""
        file_path = update_path(r'\folder\folder\letter\111111.txt', 'input_dir')
        expected = 'error_new'
        self.assertEqual(file_path, expected, "Problem with test for new")


if __name__ == '__main__':
    unittest.main()
