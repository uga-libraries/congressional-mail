import os
import unittest
from css_archiving_format import read_csv
from test_read_metadata import df_to_list


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the csv is present"""
        md_df = read_csv(os.path.join('test_data', 'read_csv', 'appraisal_delete_log.csv'))

        # Tests the values in the returned dataframe are correct.
        result = df_to_list(md_df)
        expected = [['zip', 'in_type', 'in_topic', 'in_text', 'in_document_name', 'in_fillin', 'out_type',
                     'out_topic', 'out_text', 'out_document_name', 'out_fillin', 'Appraisal_Category'],
                    ['30601', 'CASE', 'sunshine', 'in_note', 'sunshine.txt', 'in_fill',
                     'CASE', 'sun', 'out_note', 'formA.txt', 'out_fill', 'Casework'],
                    ['30602', 'CASE', 'rainbows', 'in_note', 'bow.txt', 'in_fill',
                     'CASE', 'bow', 'out_note', 'formB.txt', 'out_fill', 'Casework'],
                    ['30603', 'GEN', 'academy-app', 'in_note', '123.txt', 'in_fill',
                     'GEN', 'academy', 'out_note', 'yes.txt', 'out_fill', 'Academy Application']]
        self.assertEqual(expected, result, "Problem with test for correct")

    def test_missing(self):
        """Test for when the csv is missing"""
        with self.assertRaises(FileNotFoundError):
            md_df = read_csv(os.path.join('test_data', 'read_csv', 'missing.csv'))


if __name__ == '__main__':
    unittest.main()
