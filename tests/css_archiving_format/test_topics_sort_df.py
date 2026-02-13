import numpy as np
import unittest
from css_archiving_format import topics_sort_df
from test_read_metadata import df_to_list
from test_topics_sort import make_df


class MyTestCase(unittest.TestCase):

    def test_both(self):
        """Test for when in_topic and out_topic have multiple topics"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'apple^pear', 'file1.txt', 'jam^pie', 'file11.txt'],
                      ['30602', 'A A^A-A', 'file2.txt', 'B^Q_R^X Y Z', 'file22.txt'],
                      ['30604', np.nan, 'file3.txt', np.nan, 'file33.txt']])
        df_topics = topics_sort_df(df)

        # Verifies the contents of the df_topics are correct.
        result = df_to_list(df_topics)
        expected = [['zip', 'in_topic', 'in_document_name', 'out_topic', 'out_document_name',
                     'in_topic_split', 'out_topic_split'],
                    ['30601', 'apple^pear', 'file1.txt', 'jam^pie', 'file11.txt', 'apple', 'jam'],
                    ['30601', 'apple^pear', 'file1.txt', 'jam^pie', 'file11.txt', 'apple', 'pie'],
                    ['30601', 'apple^pear', 'file1.txt', 'jam^pie', 'file11.txt', 'pear', 'jam'],
                    ['30601', 'apple^pear', 'file1.txt', 'jam^pie', 'file11.txt', 'pear', 'pie'],
                    ['30602', 'A A^A-A', 'file2.txt', 'B^Q_R^X Y Z', 'file22.txt', 'A A', 'B'],
                    ['30602', 'A A^A-A', 'file2.txt', 'B^Q_R^X Y Z', 'file22.txt', 'A A', 'Q_R'],
                    ['30602', 'A A^A-A', 'file2.txt', 'B^Q_R^X Y Z', 'file22.txt', 'A A', 'X Y Z'],
                    ['30602', 'A A^A-A', 'file2.txt', 'B^Q_R^X Y Z', 'file22.txt', 'A-A', 'B'],
                    ['30602', 'A A^A-A', 'file2.txt', 'B^Q_R^X Y Z', 'file22.txt', 'A-A', 'Q_R'],
                    ['30602', 'A A^A-A', 'file2.txt', 'B^Q_R^X Y Z', 'file22.txt', 'A-A', 'X Y Z'],
                    ['30604', 'blank', 'file3.txt', 'blank', 'file33.txt', 'blank', 'blank']]
        self.assertEqual(expected, result, "Problem with test for both")

    def test_in_only(self):
        """Test for when in_topic is the only column with multiple topics"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'apple^pear', 'file1.txt', 'U', 'file11.txt'],
                      ['30602', 'A^A-A^B', 'file2.txt', 'V', 'file22.txt'],
                      ['30603', 'farm app^park and rec', 'file3.txt', 'X', 'file33.txt'],
                      ['30604', np.nan, 'file4.txt', 'Y', 'file44.txt'],
                      ['30605', 'rec', 'file5.txt', 'Z', 'file55.txt']])
        df_topics = topics_sort_df(df)

        # Verifies the contents of the df_topics are correct.
        result = df_to_list(df_topics)
        expected = [['zip', 'in_topic', 'in_document_name', 'out_topic', 'out_document_name',
                     'in_topic_split', 'out_topic_split'],
                    ['30601', 'apple^pear', 'file1.txt', 'U', 'file11.txt', 'apple', 'U'],
                    ['30601', 'apple^pear', 'file1.txt', 'U', 'file11.txt', 'pear', 'U'],
                    ['30602', 'A^A-A^B', 'file2.txt', 'V', 'file22.txt', 'A', 'V'],
                    ['30602', 'A^A-A^B', 'file2.txt', 'V', 'file22.txt', 'A-A', 'V'],
                    ['30602', 'A^A-A^B', 'file2.txt', 'V', 'file22.txt', 'B', 'V'],
                    ['30603', 'farm app^park and rec', 'file3.txt', 'X', 'file33.txt', 'farm app', 'X'],
                    ['30603', 'farm app^park and rec', 'file3.txt', 'X', 'file33.txt', 'park and rec', 'X'],
                    ['30604', 'blank', 'file4.txt', 'Y', 'file44.txt', 'blank', 'Y'],
                    ['30605', 'rec', 'file5.txt', 'Z', 'file55.txt', 'rec', "Z"]]
        self.assertEqual(expected, result, "Problem with test for in_only")

    def test_none(self):
        """Test for when neither topic column has multiple topics"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'pear', 'file1.txt', 'U', 'file11.txt'],
                      ['30602', 'A-A', 'file2.txt', 'V', 'file22.txt'],
                      ['30603', np.nan, 'file3.txt', 'X', 'file33.txt'],
                      ['30604', 'farm app', 'file4.txt', 'Y', 'file44.txt']])
        df_topics = topics_sort_df(df)

        # Verifies the contents of the df_topics are correct.
        result = df_to_list(df_topics)
        expected = [['zip', 'in_topic', 'in_document_name', 'out_topic', 'out_document_name',
                     'in_topic_split', 'out_topic_split'],
                    ['30601', 'pear', 'file1.txt', 'U', 'file11.txt', 'pear', 'U'],
                    ['30602', 'A-A', 'file2.txt', 'V', 'file22.txt', 'A-A', 'V'],
                    ['30603', 'blank', 'file3.txt', 'X', 'file33.txt', 'blank', 'X'],
                    ['30604', 'farm app', 'file4.txt', 'Y', 'file44.txt', 'farm app', 'Y']]
        self.assertEqual(expected, result, "Problem with test for none")

    def test_out_only(self):
        """Test for when out_topic is the only column with multiple topics"""
        # Makes a dataframe to use as test input and runs the function being tested.
        df = make_df([['30601', 'AAAA', 'file1.txt', 'U-V^XYZ', 'file11.txt'],
                      ['30602', 'BBBB', 'file2.txt', 'B 1^B.2', 'file22.txt'],
                      ['30603', np.nan, 'file3.txt', np.nan, 'file33.txt'],
                      ['30604', 'CCCC', 'file4.txt', 'W^X^Y^Z', 'file44.txt'],
                      ['30605', 'DDDD', 'file5.txt', 'ZZZZZZZ', 'file55.txt']])
        df_topics = topics_sort_df(df)

        # Verifies the contents of the df_topics are correct.
        result = df_to_list(df_topics)
        expected = [['zip', 'in_topic', 'in_document_name', 'out_topic', 'out_document_name',
                     'in_topic_split', 'out_topic_split'],
                    ['30601', 'AAAA', 'file1.txt', 'U-V^XYZ', 'file11.txt', 'AAAA', 'U-V'],
                    ['30601', 'AAAA', 'file1.txt', 'U-V^XYZ', 'file11.txt', 'AAAA', 'XYZ'],
                    ['30602', 'BBBB', 'file2.txt', 'B 1^B.2', 'file22.txt', 'BBBB', 'B 1'],
                    ['30602', 'BBBB', 'file2.txt', 'B 1^B.2', 'file22.txt', 'BBBB', 'B.2'],
                    ['30603', 'blank', 'file3.txt', 'blank', 'file33.txt', 'blank', 'blank'],
                    ['30604', 'CCCC', 'file4.txt', 'W^X^Y^Z', 'file44.txt', 'CCCC', 'W'],
                    ['30604', 'CCCC', 'file4.txt', 'W^X^Y^Z', 'file44.txt', 'CCCC', 'X'],
                    ['30604', 'CCCC', 'file4.txt', 'W^X^Y^Z', 'file44.txt', 'CCCC', 'Y'],
                    ['30604', 'CCCC', 'file4.txt', 'W^X^Y^Z', 'file44.txt', 'CCCC', 'Z'],
                    ['30605', 'DDDD', 'file5.txt', 'ZZZZZZZ', 'file55.txt', 'DDDD', 'ZZZZZZZ']]
        self.assertEqual(expected, result, "Problem with test for out_only")


if __name__ == '__main__':
    unittest.main()
