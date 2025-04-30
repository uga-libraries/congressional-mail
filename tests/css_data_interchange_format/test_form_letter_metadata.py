"""
Preliminary test for form_letter_metadata()
We're not sure yet if we're going to use it, so this is to check development rather than comprehensive.
"""
import os
import unittest
from css_data_interchange_format import form_letter_metadata
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the report, if made by the test"""
        report_path = os.path.join('test_data', 'form_letter_metadata.csv')
        if os.path.exists(report_path):
            os.remove(report_path)

    def test(self):
        # Makes variables to use as test input and runs the function.
        input_dir = os.path.join('test_data', 'form_letter_metadata')
        output_dir = 'test_data'
        form_letter_metadata(input_dir, output_dir)

        # Tests the contents of formletter_metadata.csv.
        result = csv_to_list(os.path.join('test_data', 'form_letter_metadata.csv'))
        expected = [['document_id', 'version', 'document_grouping_id', 'document_type', 'document_display_name', 
                     'document_description', 'document_name_x', 'created_by', 'revised_by', 'approved_by', 
                     'creation_date', 'revision_date', 'last_used_date', 'status', 'inactive_flag', 
                     'virtual_directory', 'fill-in_field_name', 'label', 'code', 'code_type', 'document_name_y', 
                     'user_id', 'attached_date', 'text', 'form_letter_attachment_flag', 'file_name', 'owned_by'],
                    ['000001', '1', '123456', 'Form', 'Economy', 'nan', r'..\doc\formletter\econ.pdf', '17',
                     'JSmith', '17', '20101212', '20110101', '20150101', 'Approved', 'nan', 'Form Letters',
                     'position', 'nan', 'LABOR', 'DOC', r'..\doc\formletter\econ.pdf', '17', '20120101', 'text',
                     'Y', 'econ.pdf', '17'],
                    ['000001', '1', '123456', 'Form', 'Economy', 'nan', r'..\doc\formletter\econ.pdf', '17',
                     'JSmith', '17', '20101212', '20110101', '20150101', 'Approved', 'nan', 'Form Letters',
                     'position', 'nan', 'TRADE', 'DOC', r'..\doc\formletter\econ.pdf', '17', '20120101', 'text',
                     'Y', 'econ.pdf', '17'],
                    ['000002', '1', '123456', 'Form', 'Courts', 'Basic info on justice system',
                     r'..\doc\formletter\court.pdf', 'JSmith', '17', 'JSmith', '20101212', '20110101', '20150101',
                     'Inactive', 'Y', 'Form Letters', 'staff_member', 'Full Name:', 'COURT', 'COM',
                     r'..\doc\formletter\court.pdf', 'JSmith', '20120101', 'text', 'Y', 'court.pdf', 'JSmith']]
        self.assertEqual(result, expected, "Problem with test for form letter metadata function")


if __name__ == '__main__':
    unittest.main()
