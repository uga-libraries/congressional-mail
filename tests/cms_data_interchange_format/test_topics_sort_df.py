import numpy as np
import pandas as pd
import unittest
from cms_data_interchange_format import topics_sort_df
from test_read_metadata import df_to_list


def make_df(rows):
    """Make a df for test input with all columns, where rows just has the values that change for each test"""
    full_rows = []
    for row in rows:
        new_row = ['*', '*', '*', '*', '*', '*', '*', '*', '*', row[0], '*', '*', '*', '*', '*', row[1],
                   '*', '*', '*', row[2], '*']
        full_rows.append(new_row)
    columns = ['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
               'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code', 'position',
               '2C_sequence_number', 'document_type', 'correspondence_document_name', 'file_location',
               'code_type', 'code', 'code_description', 'inactive_flag']
    df = pd.DataFrame(full_rows, columns=columns)
    return df


class MyTestCase(unittest.TestCase):

    def test_basic(self):
        """Test for when there are no blanks and the function just adds a column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'path\\file1.txt', 'apple'],
                      ['30602', 'path\\file2.txt', 'berry'],
                      ['30603', 'path\\file3.txt', 'pears'],
                      ['30604', 'path\\file1.txt', 'apple']])
        df_topics = topics_sort_df(df)

        # Verifies the contents of the df_topics are correct.
        result = df_to_list(df_topics)
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code',
                     'position', '2C_sequence_number', 'document_type', 'correspondence_document_name',
                     'correspondence_document_name_present', 'file_location', 'code_type', 'code',
                     'code_description', 'inactive_flag'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30601', '*', '*', '*', '*', '*',
                     'path\\file1.txt', 'TBD', '*', '*', '*', 'apple', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30602', '*', '*', '*', '*', '*',
                     'path\\file2.txt', 'TBD', '*', '*', '*', 'berry', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30603', '*', '*', '*', '*', '*',
                     'path\\file3.txt', 'TBD', '*', '*', '*', 'pears', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30604', '*', '*', '*', '*', '*',
                     'path\\file1.txt', 'TBD', '*', '*', '*', 'apple', '*']]
        self.assertEqual(expected, result, "Problem with test for basic")

    def test_blanks(self):
        """Test for when there are blanks"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'path\\file1.txt', 'apple'],
                      ['30602', np.nan, 'berry'],
                      ['30603', 'path\\file3.txt', 'pears'],
                      ['30604', 'path\\file4.txt', np.nan],
                      ['30605', np.nan, np.nan]])
        df_topics = topics_sort_df(df)

        # Verifies the contents of the df_topics are correct.
        result = df_to_list(df_topics)
        expected = [['correspondence_type', 'staff', 'date_in', 'date_out', 'tickler_date', 'update_date',
                     'response_type', 'city', 'state', 'zip_code', 'country', 'correspondence_code',
                     'position', '2C_sequence_number', 'document_type', 'correspondence_document_name',
                     'correspondence_document_name_present', 'file_location', 'code_type', 'code',
                     'code_description', 'inactive_flag'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30601', '*', '*', '*', '*', '*',
                     'path\\file1.txt', 'TBD', '*', '*', '*', 'apple', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '30603', '*', '*', '*', '*', '*',
                     'path\\file3.txt', 'TBD', '*', '*', '*', 'pears', '*']]
        self.assertEqual(expected, result, "Problem with test for blanks")


if __name__ == '__main__':
    unittest.main()
