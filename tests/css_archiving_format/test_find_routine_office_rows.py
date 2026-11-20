import numpy as np
import unittest
from css_archiving_format import find_routine_office_rows
from test_df_search import make_df
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_in_topic(self):
        """Test for when column in_topic contains one of the topics indicating routine office"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'Flag Request', '', '', '', '', '', '', ''],
                ['30601', 'Flag', '', '', '', '', '', '', ''],
                ['30602', 'congrats^scouts', '', '', '', '', '', '', ''],
                ['30603', 'scouts', '', '', '', '', '', '', ''],
                ['30604', 'Flag Request', '', '', '', '', '', '', ''],
                ['30605', '', '', '', '', '', '', '', ''],
                ['30606', np.nan, '', '', '', '', '', '', ''],
                ['30607', 'Flag Request', '', '', '', '', '', '', '']]
        md_df = make_df(rows)
        df_routine = find_routine_office_rows(md_df)

        # Tests the values in df_routine are correct.
        result = df_to_list(df_routine)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', 'Flag Request', '', '', '', '', '', '', '', 'Routine_Office'],
                    ['30602', 'congrats^scouts', '', '', '', '', '', '', '', 'Routine_Office'],
                    ['30604', 'Flag Request', '', '', '', '', '', '', '', 'Routine_Office'],
                    ['30607', 'Flag Request', '', '', '', '', '', '', '', 'Routine_Office']]
        self.assertEqual(expected, result, "Problem with test for in_topic")

    def test_none(self):
        """Test for when no patterns indicating routine office are present"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', 'Farms', '', '', '', '', 'Note', '', ''],
                ['30601', 'congrats', np.nan, np.nan, np.nan, 'Cats', np.nan, np.nan, np.nan],
                ['30602', 'Flag', '', '', '', 'Econ Plan', '', '..\\doc\\econ-outlook.doc', '']]
        md_df = make_df(rows)
        df_routine = find_routine_office_rows(md_df)

        # Tests the values in df_routine are correct.
        result = df_to_list(df_routine)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category']]
        self.assertEqual(expected, result, "Problem with test for none (no patterns matched)")

    def test_out_topic(self):
        """Test for when column out_topic contains one of the topics indicating routine office"""
        # Makes a dataframe to use as test input and runs the function.
        rows = [['30600', '', '', '', '', 'congrats^scouts', '', '', ''],
                ['30601', '', '', '', '', 'scouting', '', '', ''],
                ['30602', '', '', '', '', 'Admin', '', '', ''],
                ['30603', '', '', '', '', 'Flag Request', '', '', ''],
                ['30604', '', '', '', '', 'congrats^scouts', '', '', '']]
        md_df = make_df(rows)
        df_routine = find_routine_office_rows(md_df)

        # Tests the values in df_routine are correct.
        result = df_to_list(df_routine)
        expected = [['zip', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_topic', 'out_text',
                     'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30600', '', '', '', '', 'congrats^scouts', '', '', '', 'Routine_Office'],
                    ['30603', '', '', '', '', 'Flag Request', '', '', '', 'Routine_Office'],
                    ['30604', '', '', '', '', 'congrats^scouts', '', '', '', 'Routine_Office']]
        self.assertEqual(expected, result, "Problem with test for out_topic")

        
if __name__ == '__main__':
    unittest.main()
