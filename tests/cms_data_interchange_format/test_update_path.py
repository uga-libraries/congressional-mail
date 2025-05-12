"""
Tests for the function update_path(), which converts the path in the metadata to the file path in the export.
"""
import unittest
from cms_data_interchange_format import update_path


class MyTestCase(unittest.TestCase):

    def test_error(self):
        """Test for a new pattern"""
        file_path = update_path(r'new\folder\file.txt', 'input_dir')
        expected = 'error_new'
        self.assertEqual(file_path, expected, "Problem with test for error")

    def test_error_partial(self):
        """Test for a new pattern that is a partial match to an existing pattern (still an error)"""
        file_path = update_path(r'enews\folder\file.txt', 'input_dir')
        expected = 'error_new'
        self.assertEqual(file_path, expected, "Problem with test for error partial")

    def test_match_attachments(self):
        """Test for the pattern attachments\\..\\file.ext"""
        file_path = update_path(r'attachments\folder\file.txt', 'input_dir')
        expected = r'input_dir\documents\attachments\folder\file.txt'
        self.assertEqual(file_path, expected, "Problem with test for match attachments")

    def test_match_case_custom(self):
        """Test for the pattern case-custom\\..\\file.ext"""
        file_path = update_path(r'case-custom\folder\file.txt', 'input_dir')
        expected = r'input_dir\documents\case-custom\folder\file.txt'
        self.assertEqual(file_path, expected, "Problem with test for match case-custom")

    def test_match_case_files(self):
        """Test for the pattern case-files\\..\\file.ext"""
        file_path = update_path(r'case-files\folder\file.txt', 'input_dir')
        expected = r'input_dir\documents\case-files\folder\file.txt'
        self.assertEqual(file_path, expected, "Problem with test for match case-files")

    def test_match_documents(self):
        """Test for the pattern documents\\..\\file.ext"""
        file_path = update_path(r'documents\folder\file.txt', 'input_dir')
        expected = r'input_dir\documents\documents\folder\file.txt'
        self.assertEqual(file_path, expected, "Problem with test for match documents")

    def test_match_enewsletters(self):
        """Test for the pattern enewsletters\\..\\file.ext"""
        file_path = update_path(r'enewsletters\folder\file.txt', 'input_dir')
        expected = r'input_dir\documents\enewsletters\folder\file.txt'
        self.assertEqual(file_path, expected, "Problem with test for match enewsletters")

    def test_match_form_attachments(self):
        """Test for the pattern form-attachments\\..\\file.ext"""
        file_path = update_path(r'form-attachments\folder\file.txt', 'input_dir')
        expected = r'input_dir\documents\form-attachments\folder\file.txt'
        self.assertEqual(file_path, expected, "Problem with test for match form-attachments")

    def test_match_forms(self):
        """Test for the pattern forms\\..\\file.ext"""
        file_path = update_path(r'forms\folder\file.txt', 'input_dir')
        expected = r'input_dir\documents\forms\folder\file.txt'
        self.assertEqual(file_path, expected, "Problem with test for match forms")

    def test_match_in_email(self):
        """Test for the pattern in-email\\..\\file.ext"""
        file_path = update_path(r'in-email\folder\file.txt', 'input_dir')
        expected = r'input_dir\documents\in-email\folder\file.txt'
        self.assertEqual(file_path, expected, "Problem with test for match in-email")

    def test_match_out_custom(self):
        """Test for the pattern out-custom\\..\\file.ext"""
        file_path = update_path(r'out-custom\folder\file.txt', 'input_dir')
        expected = r'input_dir\documents\out-custom\folder\file.txt'
        self.assertEqual(file_path, expected, "Problem with test for match out-custom")


if __name__ == '__main__':
    unittest.main()
