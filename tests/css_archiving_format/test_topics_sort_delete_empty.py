import os
import shutil
import unittest
from css_archiving_format import topics_sort_delete_empty


def check_paths():
    """Checks if the three paths exist and returns as a list of Booleans"""
    topic_path = os.path.join('test_data', 'topics_sort_delete_empty', 'topic')
    check = [os.path.exists(topic_path),
             os.path.exists(os.path.join(topic_path, 'from_constituents')),
             os.path.exists(os.path.join(topic_path, 'to_constituents'))]
    return check


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the copy of the test data, if made and not completely deleted by the test"""
        test_data = os.path.join('test_data', 'topics_sort_delete_empty', 'topic')
        if os.path.exists(test_data):
            shutil.rmtree(test_data)

    def test_both_empty(self):
        """Test for when both to and from folders are empty, so the topic is also empty"""
        # Copies the test data, because the function alters it, and runs the function.
        shutil.copytree(os.path.join('test_data', 'topics_sort_delete_empty', 'both_empty'),
                        os.path.join('test_data', 'topics_sort_delete_empty', 'topic'))
        topics_sort_delete_empty(os.path.join(os.getcwd(), 'test_data', 'topics_sort_delete_empty', 'topic'))

        # Verifies all folders were deleted.
        result = check_paths()
        expected = [False, False, False]
        self.assertEqual(expected, result, "Problem with test for both_empty")

    def test_from_empty(self):
        """Test for when the from_constituents folder is empty"""
        # Copies the test data, because the function alters it, and runs the function.
        shutil.copytree(os.path.join('test_data', 'topics_sort_delete_empty', 'from_empty'),
                        os.path.join('test_data', 'topics_sort_delete_empty', 'topic'))
        topics_sort_delete_empty(os.path.join('test_data', 'topics_sort_delete_empty', 'topic'))

        # Verifies all folders were deleted.
        result = check_paths()
        expected = [True, False, True]
        self.assertEqual(expected, result, "Problem with test for from_empty")

    def test_neither_empty(self):
        """Test for when to and from folders are not empty, so nothing is deleted"""
        # Copies the test data, because the function alters it, and runs the function.
        shutil.copytree(os.path.join('test_data', 'topics_sort_delete_empty', 'neither_empty'),
                        os.path.join('test_data', 'topics_sort_delete_empty', 'topic'))
        topics_sort_delete_empty(os.path.join('test_data', 'topics_sort_delete_empty', 'topic'))

        # Verifies all folders were deleted.
        result = check_paths()
        expected = [True, True, True]
        self.assertEqual(expected, result, "Problem with test for neither_empty")

    def test_to_empty(self):
        """Test for when the to_constituents folder is empty"""
        # Copies the test data, because the function alters it, and runs the function.
        shutil.copytree(os.path.join('test_data', 'topics_sort_delete_empty', 'to_empty'),
                        os.path.join('test_data', 'topics_sort_delete_empty', 'topic'))
        topics_sort_delete_empty(os.path.join('test_data', 'topics_sort_delete_empty', 'topic'))

        # Verifies all folders were deleted.
        result = check_paths()
        expected = [True, True, False]
        self.assertEqual(expected, result, "Problem with test for to_empty")


if __name__ == '__main__':
    unittest.main()
