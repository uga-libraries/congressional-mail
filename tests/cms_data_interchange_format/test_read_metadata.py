"""
Tests for the function read_metadata(), which combines all metadata into a dataframe.
"""
import os
import unittest
from cms_data_interchange_format import read_metadata
from test_read_metadata_file import df_to_list


def make_paths_dict(test_folder):
    """Make the paths_dict, which is identical for each test except the test_folder name"""
    paths = {'1B': os.path.join('test_data', 'read', test_folder, '1B.out'),
             '2A': os.path.join('test_data', 'read', test_folder, '2A.out'),
             '2B': os.path.join('test_data', 'read', test_folder, '2B.out'),
             '2C': os.path.join('test_data', 'read', test_folder, '2C.out'),
             '2D': os.path.join('test_data', 'read', test_folder, '2D.out'),
             '8A': os.path.join('test_data', 'read', test_folder, '8A.out')}
    return paths


class MyTestCase(unittest.TestCase):
    
    def test_match(self):
        """Test for when all IDs for all rows match 2A once"""
        # Makes variable for the function and runs the function.
        paths_dict = make_paths_dict('match')
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        result = df_to_list(md_df)
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['LETTER', 'Staffer_1', '20220110', '20220110', 'BLANK', '20220110', 'LETTER', 'City One',
                     'GA', '30001', 'USA', '15001', 'CON', '1', 'main', 'taxes_con.docx', 'BLANK', 'text1',
                     'COR', '15001', 'Taxes', 'Y'],
                    ['EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK', '20220220', 'EMAIL', 'City Two',
                     'GA', '30002', 'USA', '15002', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK', 'text2',
                     'COR', '15002', 'Minimum Wage', 'BLANK'],
                    ['EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK', '20220330', 'EMAIL', 'City Three',
                     'GA', '30003', 'USA', '15003', 'NEU', '1', 'main', 'rights_pro.docx', 'BLANK', 'text3',
                     'COR', '15003', 'Rights > Workers', 'Y']]
        self.assertEqual(expected, result, "Problem with test for match")

    def test_match_multiple(self):
        """Test for when at least one row for all three IDs matches 2A more than once"""
        # Makes variable for the function and runs the function.
        paths_dict = make_paths_dict('match_multiple')
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        result = df_to_list(md_df)
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['LETTER', 'Staffer_1', '20220110', '20220110', 'BLANK', '20220110', 'LETTER', 'City One',
                     'GA', '30001', 'USA', '15001', 'CON', '1', 'main', 'taxes_con.docx', 'BLANK', 'text1',
                     'COR', '15001', 'Taxes', 'Y'],
                    ['EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK', '20220220', 'EMAIL', 'City Two',
                     'GA', '30002', 'USA', '15002', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK', 'text2',
                     'COR', '15002', 'Minimum Wage', 'BLANK'],
                    ['EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK', '20220220', 'EMAIL', 'City Five',
                     'GA', '30005', 'USA', '15002', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK', 'text2',
                     'COR', '15002', 'Minimum Wage', 'BLANK'],
                    ['EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK', '20220330', 'EMAIL', 'City Three',
                     'GA', '30003', 'USA', '15003', 'NEU', '1', 'main', 'rights_pro.docx', 'BLANK', 'text3',
                     'COR', '15003', 'Rights > Workers', 'Y'],
                    ['EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK', '20220330', 'EMAIL', 'City Three',
                     'GA', '30003', 'USA', '15003', 'NEU', '2', 'main', 'rights_update.docx', 'BLANK', 'text3',
                     'COR', '15003', 'Rights > Workers', 'Y'],
                    ['EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK', '20220330', 'EMAIL', 'City Three',
                     'GA', '30003', 'USA', '15003', 'PRO', '1', 'main', 'rights_pro.docx', 'BLANK', 'text3',
                     'COR', '15003', 'Rights > Workers', 'Y'],
                    ['EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK', '20220330', 'EMAIL', 'City Three',
                     'GA', '30003', 'USA', '15003', 'PRO', '2', 'main', 'rights_update.docx', 'BLANK', 'text3',
                     'COR', '15003', 'Rights > Workers', 'Y'],
                    ['EMAIL', 'Staffer_4', '20220440', '20220440', 'BLANK', '20220440', 'EMAIL', 'City Four',
                     'GA', '30004', 'USA', '15004', 'MEH', '1', 'main', 'undecided.docx', 'BLANK', 'text4',
                     'COR', '15004', 'Support', 'BLANK'],
                    ['EMAIL', 'Staffer_4', '20220440', '20220440', 'BLANK', '20220440', 'EMAIL', 'City Four',
                     'GA', '30004', 'USA', '15004', 'MEH', '1', 'main', 'undecided.docx', 'BLANK', 'text4',
                     'COR', '15004', 'Support > A', 'BLANK'],
                    ['EMAIL', 'Staffer_4', '20220440', '20220440', 'BLANK', '20220440', 'EMAIL', 'City Four',
                     'GA', '30004', 'USA', '15004', 'MEH', '1', 'main', 'undecided.docx', 'BLANK', 'text4',
                     'COR', '15004', 'Support > B', 'BLANK'],
                    ['LETTER', 'Staffer_5', '20220550', '20220550', 'BLANK', '20220550', 'LETTER', 'City One',
                     'GA', '30001', 'USA', '15001', 'CON', '1', 'main', 'taxes_con.docx', 'BLANK', 'text1',
                     'COR', '15001', 'Taxes', 'Y']]
        self.assertEqual(expected, result, "Problem with test for match_multiple")

    def test_no_match_constituent_id(self):
        """Test for when the constituent_id in 1B does not match 2A"""
        # Makes variable for the function and runs the function.
        paths_dict = make_paths_dict('no_match_constituent_id')
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        result = df_to_list(md_df)
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['LETTER', 'Staffer_1', '20220110', '20220110', 'BLANK', '20220110', 'LETTER', 'BLANK',
                     'BLANK', 'BLANK', 'BLANK', '15001', 'CON', '1', 'main', 'taxes_con.docx', 'BLANK', 'text1',
                     'COR', '15001', 'Taxes', 'Y'],
                    ['EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK', '20220220', 'EMAIL', 'BLANK',
                     'BLANK', 'BLANK', 'BLANK', '15002', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK', 'text2',
                     'COR', '15002', 'Minimum Wage', 'BLANK'],
                    ['EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK', '20220330', 'EMAIL', 'BLANK',
                     'BLANK', 'BLANK', 'BLANK', '15003', 'NEU', '1', 'main', 'rights_pro.docx', 'BLANK', 'text3',
                     'COR', '15003', 'Rights > Workers', 'Y']]
        self.assertEqual(expected, result, "Problem with test for no_match_constituent_id")

    def test_no_match_correspondence_code(self):
        """Test for when the correspondence_code in 2B does not match the code in 8A"""
        # Makes variable for the function and runs the function.
        paths_dict = make_paths_dict('no_match_correspondence_code')
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        result = df_to_list(md_df)
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['LETTER', 'Staffer_1', '20220110', '20220110', 'BLANK', '20220110', 'LETTER', 'City One',
                     'GA', '30001', 'USA', '15001', 'CON', '1', 'main', 'taxes_con.docx', 'BLANK', 'text1',
                     'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK', '20220220', 'EMAIL', 'City Two',
                     'GA', '30002', 'USA', '15002', 'PRO', '1', 'main', 'min_wage_pro.docx', 'BLANK', 'text2',
                     'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK', '20220330', 'EMAIL', 'City Three',
                     'GA', '30003', 'USA', '15003', 'NEU', '1', 'main', 'rights_pro.docx', 'BLANK', 'text3',
                     'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for no_match_correspondence_code")

    def test_no_match_correspondence_id(self):
        """Test for when the correspondence_id in 2B, 2C, and/or 2D does not match 2A"""
        # Makes variable for the function and runs the function.
        paths_dict = make_paths_dict('no_match_correspondence_id')
        md_df = read_metadata(paths_dict)

        # Tests the value of md_df
        result = df_to_list(md_df)
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
                     '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
                     'correspondence_text', 'code_type', 'code', 'code_description', 'inactive_flag'],
                    ['LETTER', 'Staffer_1', '20220110', '20220110', 'BLANK', '20220110', 'LETTER', 'City One',
                     'GA', '30001', 'USA', 'BLANK', 'BLANK', '1', 'main', 'taxes_con.docx', 'BLANK', 'text1',
                     'BLANK', 'BLANK', 'BLANK', 'BLANK'],
                    ['EMAIL', 'Staffer_2', '20220220', '20220220', 'BLANK', '20220220', 'EMAIL', 'City Two',
                     'GA', '30002', 'USA', '15002', 'PRO', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'COR', '15002', 'Minimum Wage', 'BLANK'],
                    ['EMAIL', 'Staffer_3', '20220330', '20220330', 'BLANK', '20220330', 'EMAIL', 'City Three',
                     'GA', '30003', 'USA', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK', 'BLANK',
                     'BLANK', 'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(expected, result, "Problem with test for no_match_correspondence_id")


if __name__ == '__main__':
    unittest.main()
