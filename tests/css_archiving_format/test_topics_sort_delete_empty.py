import os
import shutil
import unittest
from css_archiving_format import topics_sort_delete_empty
from test_script import make_dir_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the copy of the test data, if made and not completely deleted by the test"""
        test_data = os.path.join('test_data', 'topics_sort_delete_empty', 'by_topic')
        if os.path.exists(test_data):
            shutil.rmtree(test_data)

    def test_empty_topic(self):
        """Test for when the topic folder is empty and is deleted"""
        # Copies the test data, because the function alters it, and runs the function.
        by_topic_path = os.path.join('test_data', 'topics_sort_delete_empty', 'by_topic')
        shutil.copytree(os.path.join('test_data', 'topics_sort_delete_empty', 'empty_topic'), by_topic_path)
        topics_sort_delete_empty(by_topic_path)

        # Checks the contents of by_topic to verify the correct folders were deleted.
        result = make_dir_list(by_topic_path)
        expected = []
        self.assertEqual(expected, result, "Problem with test for empty_topic")

    def test_empty_type(self):
        """Test for when the type folder within a topic folder is empty and is deleted"""
        # Copies the test data, because the function alters it, and runs the function.
        by_topic_path = os.path.join('test_data', 'topics_sort_delete_empty', 'by_topic')
        shutil.copytree(os.path.join('test_data', 'topics_sort_delete_empty', 'empty_type'), by_topic_path)
        topics_sort_delete_empty(by_topic_path)

        # Checks the contents of by_topic to verify the correct folders were deleted.
        result = make_dir_list(by_topic_path)
        expected = [os.path.join(by_topic_path, 'banana'),
                    os.path.join(by_topic_path, 'banana', 'objects'),
                    os.path.join(by_topic_path, 'banana', 'objects', 'letter.txt')]
        self.assertEqual(expected, result, "Problem with test for empty_type")

    def test_empty_type_subfolder(self):
        """Test for when the subfolder within a type folder is empty and is deleted"""
        # Copies the test data, because the function alters it, and runs the function.
        by_topic_path = os.path.join('test_data', 'topics_sort_delete_empty', 'by_topic')
        shutil.copytree(os.path.join('test_data', 'topics_sort_delete_empty', 'empty_type_subfolder'), by_topic_path)
        topics_sort_delete_empty(by_topic_path)

        # Checks the contents of by_topic to verify the correct folders were deleted.
        result = make_dir_list(by_topic_path)
        expected = [os.path.join(by_topic_path, 'banana'),
                    os.path.join(by_topic_path, 'banana', 'form'),
                    os.path.join(by_topic_path, 'banana', 'form', 'dessert'),
                    os.path.join(by_topic_path, 'banana', 'form', 'dessert', 'letter.txt')]
        self.assertEqual(expected, result, "Problem with test for empty_type_subfolder")

    def test_no_empty(self):
        """Test for when no folders are empty, so nothing is deleted"""
        # Copies the test data, because the function alters it, and runs the function.
        by_topic_path = os.path.join('test_data', 'topics_sort_delete_empty', 'by_topic')
        shutil.copytree(os.path.join('test_data', 'topics_sort_delete_empty', 'no_empty'), by_topic_path)
        topics_sort_delete_empty(by_topic_path)

        # Checks the contents of by_topic to verify no folders were deleted.
        result = make_dir_list(by_topic_path)
        expected = [os.path.join(by_topic_path, 'apple'),
                    os.path.join(by_topic_path, 'banana'),
                    os.path.join(by_topic_path, 'apple', 'form'),
                    os.path.join(by_topic_path, 'apple', 'form', 'letter.txt'),
                    os.path.join(by_topic_path, 'banana', 'form'),
                    os.path.join(by_topic_path, 'banana', 'form', 'pro'),
                    os.path.join(by_topic_path, 'banana', 'form', 'pro', 'letter.txt')]
        self.assertEqual(expected, result, "Problem with test for no_empty")


if __name__ == '__main__':
    unittest.main()
