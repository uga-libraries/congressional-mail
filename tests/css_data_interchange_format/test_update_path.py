"""
Tests for the function update_path(), which converts the path in the metadata to the file path in the export.
"""
import unittest
from css_data_interchange_format import update_path


class MyTestCase(unittest.TestCase):

    def test_pattern_match(self):
        """Test for the pattern ..\\documents\\folder\\..\\file.ext"""
        file_path = update_path(r'..\documents\formletters\form_a.txt', 'input_dir')
        expected = r'input_dir\documents\formletters\form_a.txt'
        self.assertEqual(file_path, expected, "Problem with test for pattern match")

    def test_new(self):
        """Test for a new pattern"""
        file_path = update_path(r'\folder\folder\letter\111111.txt', 'input_dir')
        expected = 'error_new'
        self.assertEqual(file_path, expected, "Problem with test for new")

    def test_new_doc(self):
        """Test for a new pattern that starts with ..\\ still but not documents"""
        file_path = update_path(r'..\folder\111111.txt', 'input_dir')
        expected = 'error_new'
        self.assertEqual(file_path, expected, "Problem with test for new")


if __name__ == '__main__':
    unittest.main()
