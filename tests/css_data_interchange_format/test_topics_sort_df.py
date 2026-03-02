import numpy as np
import pandas as pd
import unittest
from css_data_interchange_format import topics_sort_df
from test_read_metadata import df_to_list


def make_df(rows):
    """Make a df for test input with all columns, where rows just has the values that change for each test"""
    full_rows = []
    for row in rows:
        new_row = ['*', '*', '*', '*', '*', '*', '*', '*', row[0], '*', '*', row[1], '*', '*', row[2], '*', '*', '*']
        full_rows.append(new_row)
    columns = ['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date', 'update_date',
               'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country', 'document_type',
               'communication_document_name', 'communication_document_id', 'file_location', 'file_name']
    df = pd.DataFrame(full_rows, columns=columns)
    return df


class MyTestCase(unittest.TestCase):

    def test_basic(self):
        """Test for when there are no blanks and the function just adds a column"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['apple', '30601', 'path\\file1.txt'],
                      ['berry', '30602', 'path\\file2.txt'],
                      ['pears', '30603', 'path\\file3.txt'],
                      ['berry', '30604', 'path\\file2.txt']])
        df_topics = topics_sort_df(df)

        # Verifies the contents of the df_topics are correct.
        result = df_to_list(df_topics)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_name_present',
                     'communication_document_id', 'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'apple', '*', '*', '30601', '*', '*',
                     'path\\file1.txt', 'TBD', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'berry', '*', '*', '30602', '*', '*',
                     'path\\file2.txt', 'TBD', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'pears', '*', '*', '30603', '*', '*',
                     'path\\file3.txt', 'TBD', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'berry', '*', '*', '30604', '*', '*',
                     'path\\file2.txt', 'TBD', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for basic")

    def test_blanks(self):
        """Test for when there are blanks in one or both of group_name and communication_document_name"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['apple', '30601', 'path\\file1.txt'],
                      [np.nan, '30602', 'path\\file2.txt'],
                      ['pears', '30603', np.nan],
                      ['pears', '30604', 'path\\file4.txt'],
                      [np.nan, '30605', np.nan]])
        df_topics = topics_sort_df(df)

        # Verifies the contents of the df_topics are correct.
        result = df_to_list(df_topics)
        expected = [['communication_type', 'approved_by', 'status', 'date_in', 'date_out', 'reminder_date',
                     'update_date', 'response_type', 'group_name', 'city', 'state_code', 'zip_code', 'country',
                     'document_type', 'communication_document_name', 'communication_document_name_present',
                     'communication_document_id', 'file_location', 'file_name'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'apple', '*', '*', '30601', '*', '*',
                     'path\\file1.txt', 'TBD', '*', '*', '*'],
                    ['*', '*', '*', '*', '*', '*', '*', '*', 'pears', '*', '*', '30604', '*', '*',
                     'path\\file4.txt', 'TBD', '*', '*', '*']]
        self.assertEqual(expected, result, "Problem with test for blanks")


if __name__ == '__main__':
    unittest.main()
