import os
import unittest
from additional_deletion import check_arguments


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when four correct arguments are provided"""
        valid_dir = os.path.join(os.getcwd(), 'test_data')
        arg_list = ['additional_deletion.py', 'css_arch', valid_dir, valid_dir, valid_dir]
        export_type, delete_directory, input_directory, output_directory, errors_list = check_arguments(arg_list)
        self.assertEqual('css_arch', export_type, "Problem with test for correct, export_type")
        self.assertEqual(valid_dir, delete_directory, "Problem with test for correct, delete_directory")
        self.assertEqual(valid_dir, input_directory, "Problem with test for correct, input_directory")
        self.assertEqual(valid_dir, output_directory, "Problem with test for correct, output_directory")
        self.assertEqual([], errors_list, "Problem with test for correct, errors_list")

    def test_error_1(self):
        """Test for when the first argument (export_type) is not an expected value"""
        valid_dir = os.path.join(os.getcwd(), 'test_data')
        arg_list = ['additional_deletion.py', 'error_type', valid_dir, valid_dir, valid_dir]
        export_type, delete_directory, input_directory, output_directory, errors_list = check_arguments(arg_list)
        self.assertEqual(None, export_type, "Problem with test for error_1, export_type")
        self.assertEqual(valid_dir, delete_directory, "Problem with test for error_1, delete_directory")
        self.assertEqual(valid_dir, input_directory, "Problem with test for error_1, input_directory")
        self.assertEqual(valid_dir, output_directory, "Problem with test for error_1, output_directory")
        self.assertEqual(["export_type is not an expected value"], errors_list, "Problem with test for error_1, errors_list")

    def test_error_2(self):
        """Test for when the second argument (delete_directory) is not a valid directory"""
        valid_dir = os.path.join(os.getcwd(), 'test_data')
        arg_list = ['additional_deletion.py', 'cms_dif', os.path.join(os.getcwd(), 'error'), valid_dir, valid_dir]
        export_type, delete_directory, input_directory, output_directory, errors_list = check_arguments(arg_list)
        self.assertEqual('cms_dif', export_type, "Problem with test for error_2, export_type")
        self.assertEqual(None, delete_directory, "Problem with test for error_2, delete_directory")
        self.assertEqual(valid_dir, input_directory, "Problem with test for error_2, input_directory")
        self.assertEqual(valid_dir, output_directory, "Problem with test for error_2, output_directory")
        self.assertEqual(["delete_directory is not a valid directory"], errors_list, "Problem with test for error_2, errors_list")
        
    def test_error_3(self):
        """Test for when the third argument (input_directory) is not a valid directory"""
        valid_dir = os.path.join(os.getcwd(), 'test_data')
        arg_list = ['additional_deletion.py', 'css_arch', valid_dir, os.path.join(os.getcwd(), 'error'), valid_dir]
        export_type, delete_directory, input_directory, output_directory, errors_list = check_arguments(arg_list)
        self.assertEqual('css_arch', export_type, "Problem with test for error_3, export_type")
        self.assertEqual(valid_dir, delete_directory, "Problem with test for error_3, delete_directory")
        self.assertEqual(None, input_directory, "Problem with test for error_3, input_directory")
        self.assertEqual(valid_dir, output_directory, "Problem with test for error_3, output_directory")
        self.assertEqual(["input_directory is not a valid directory"], errors_list, "Problem with test for error_3, errors_list")

    def test_error_4(self):
        """Test for when the fourth argument (output_directory) is not a valid directory"""
        valid_dir = os.path.join(os.getcwd(), 'test_data')
        arg_list = ['additional_deletion.py', 'css_dif', valid_dir, valid_dir, os.path.join(os.getcwd(), 'error')]
        export_type, delete_directory, input_directory, output_directory, errors_list = check_arguments(arg_list)
        self.assertEqual('css_dif', export_type, "Problem with test for error_4, export_type")
        self.assertEqual(valid_dir, delete_directory, "Problem with test for error_4, delete_directory")
        self.assertEqual(valid_dir, input_directory, "Problem with test for error_4, input_directory")
        self.assertEqual(None, output_directory, "Problem with test for error_4, output_directory")
        self.assertEqual(["output_directory is not a valid directory"], errors_list, "Problem with test for error_4, errors_list")
        
    def test_error_all(self):
        """Test for when the first argument (export_type) is not an expected value"""
        not_valid_dir = os.path.join(os.getcwd(), 'error')
        arg_list = ['additional_deletion.py', 'error_type', not_valid_dir, not_valid_dir, not_valid_dir]
        export_type, delete_directory, input_directory, output_directory, errors_list = check_arguments(arg_list)
        self.assertEqual(None, export_type, "Problem with test for error_all, export_type")
        self.assertEqual(None, delete_directory, "Problem with test for error_all, delete_directory")
        self.assertEqual(None, input_directory, "Problem with test for error_all, input_directory")
        self.assertEqual(None, output_directory, "Problem with test for error_all, output_directory")
        self.assertEqual(["export_type is not an expected value", "delete_directory is not a valid directory",
                          "input_directory is not a valid directory", "output_directory is not a valid directory"],
                         errors_list, "Problem with test for error_all, errors_list")
        
    def test_too_few(self):
        """Test for when less than four arguments are provided"""
        arg_list = ['additional_deletion.py', 'error']
        export_type, delete_directory, input_directory, output_directory, errors_list = check_arguments(arg_list)
        self.assertEqual(None, export_type, "Problem with test for too_few, export_type")
        self.assertEqual(None, delete_directory, "Problem with test for too_few, delete_directory")
        self.assertEqual(None, input_directory, "Problem with test for too_few, input_directory")
        self.assertEqual(None, output_directory, "Problem with test for too_few, output_directory")
        self.assertEqual(["At least one of the four required arguments is missing"], errors_list, 
                         "Problem with test for too_few, errors_list")

    def test_too_many(self):
        """Test for when more than four arguments are provided"""
        valid_dir = os.path.join(os.getcwd(), 'test_data')
        arg_list = ['additional_deletion.py', 'css_arch', valid_dir, valid_dir, valid_dir, 'error_extra']
        export_type, delete_directory, input_directory, output_directory, errors_list = check_arguments(arg_list)
        self.assertEqual(None, export_type, "Problem with test for too_many, export_type")
        self.assertEqual(None, delete_directory, "Problem with test for too_many, delete_directory")
        self.assertEqual(None, input_directory, "Problem with test for too_many, input_directory")
        self.assertEqual(None, output_directory, "Problem with test for too_many, output_directory")
        self.assertEqual(["More than the expected four required arguments were provided"], errors_list, 
                         "Problem with test for too_many, errors_list")

if __name__ == '__main__':
    unittest.main()
