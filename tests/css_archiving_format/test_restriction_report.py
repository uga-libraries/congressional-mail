"""
Tests for the function topics_report(), which makes a report of the number of times each topic is used.
To simplify testing, md_df has only a few of the columns that are in a normal export.
"""
import numpy as np
import os
import pandas as pd
import unittest
from css_archiving_format import restriction_report
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the report, if made by the test"""
        report_path = os.path.join('test_data', 'restriction_review.csv')
        if os.path.exists(report_path):
            os.remove(report_path)

    def test_delimiter_in(self):
        """Test for when in_topic contains delimiters"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', np.nan, 'Safe'],
                              ['30601', 'OK^Safe', 'Safe'],
                              ['30602', 'citizen^safe', 'Restrict one'],
                              ['30603', 'crime^court^criminal justice', 'Restrict three'],
                              ['30604', 'safe', 'Safe'],
                              ['30605', 'court', 'Restrict']],
                             columns=['zip', 'in_topic', 'out_topic'])
        restriction_report(md_df, 'test_data')

        # Tests the contents of the restriction_review.csv.
        result = csv_to_list(os.path.join('test_data', 'restriction_review.csv'))
        expected = [['zip', 'in_topic', 'out_topic', 'in_topic_split', 'out_topic_split'],
                    [30602, 'citizen^safe', 'Restrict one', 'citizen', 'Restrict one'],
                    [30603, 'crime^court^criminal justice', 'Restrict three', 'crime', 'Restrict three'],
                    [30603, 'crime^court^criminal justice', 'Restrict three', 'court', 'Restrict three'],
                    [30603, 'crime^court^criminal justice', 'Restrict three', 'criminal justice', 'Restrict three'],
                    [30605, 'court', 'Restrict', 'court', 'Restrict']]
        self.assertEqual(expected, result, "Problem with test for delimiter_in")

    def test_delimiter_in_out(self):
        """Test for when in_topic and out_topic contain delimiters"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Safe', np.nan],
                              ['30601', 'Safe^ok', 'ok^Safe'],
                              ['30602', 'immigrant^safe', 'safe^immigration'],
                              ['30603', 'migrant^citizen^immigration', 'court^immigration'],
                              ['30604', 'Safe', 'basketball court'],
                              ['30605', 'citizen', 'refugee^court']],
                             columns=['zip', 'in_topic', 'out_topic'])
        restriction_report(md_df, 'test_data')

        # Tests the contents of the restriction_review.csv.
        result = csv_to_list(os.path.join('test_data', 'restriction_review.csv'))
        expected = [['zip', 'in_topic', 'out_topic', 'in_topic_split', 'out_topic_split'],
                    [30602, 'immigrant^safe', 'safe^immigration', 'immigrant', 'safe'],
                    [30602, 'immigrant^safe', 'safe^immigration', 'immigrant', 'immigration'],
                    [30602, 'immigrant^safe', 'safe^immigration', 'safe', 'immigration'],
                    [30603, 'migrant^citizen^immigration', 'court^immigration', 'migrant', 'court'],
                    [30603, 'migrant^citizen^immigration', 'court^immigration', 'migrant', 'immigration'],
                    [30603, 'migrant^citizen^immigration', 'court^immigration', 'citizen', 'court'],
                    [30603, 'migrant^citizen^immigration', 'court^immigration', 'citizen', 'immigration'],
                    [30603, 'migrant^citizen^immigration', 'court^immigration', 'immigration', 'court'],
                    [30603, 'migrant^citizen^immigration', 'court^immigration', 'immigration', 'immigration'],
                    [30605, 'citizen', 'refugee^court', 'citizen', 'refugee'],
                    [30605, 'citizen', 'refugee^court', 'citizen', 'court']]
        self.assertEqual(expected, result, "Problem with test for delimiter_in_out")

    def test_delimiter_out(self):
        """Test for when out_topic contains delimiters"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Safe', np.nan],
                              ['30601', 'Safe', 'OK^Safe'],
                              ['30602', 'Restrict one', 'citizenship^safe'],
                              ['30603', 'Restrict three', 'citizen^immigration^refugee'],
                              ['30604', 'Safe', 'basketball court'],
                              ['30605', 'Restrict', 'immigrant']],
                             columns=['zip', 'in_topic', 'out_topic'])
        restriction_report(md_df, 'test_data')

        # Tests the contents of the restriction_review.csv.
        result = csv_to_list(os.path.join('test_data', 'restriction_review.csv'))
        expected = [['zip', 'in_topic', 'out_topic', 'in_topic_split', 'out_topic_split'],
                    [30602, 'Restrict one', 'citizenship^safe', 'Restrict one', 'citizenship'],
                    [30603, 'Restrict three', 'citizen^immigration^refugee', 'Restrict three', 'citizen'],
                    [30603, 'Restrict three', 'citizen^immigration^refugee', 'Restrict three', 'immigration'],
                    [30603, 'Restrict three', 'citizen^immigration^refugee', 'Restrict three', 'refugee'],
                    [30605, 'Restrict', 'immigrant', 'Restrict', 'immigrant']]
        self.assertEqual(expected, result, "Problem with test for delimiter_out")

    def test_none(self):
        """Test for when there are no restricted topics"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', np.nan, 'Safe'],
                              ['30601', 'Safe', 'Safe'],
                              ['30604', 'basketball court', 'Safe']],
                             columns=['zip', 'in_topic', 'out_topic'])
        restriction_report(md_df, 'test_data')

        # Tests that no restriction_review.csv was made.
        result = os.path.exists(os.path.join('test_data', 'restriction_review.csv'))
        expected = False
        self.assertEqual(expected, result, "Problem with test for none")

    def test_restrict_in(self):
        """Test for when the restricted topic is in in_topic"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', np.nan, 'Safe'],
                              ['30601', 'Safe', 'Safe'],
                              ['30602', 'citizen', 'Restrict'],
                              ['30603', 'crime', 'Restrict'],
                              ['30604', 'basketball court', 'Safe'],
                              ['30605', 'court', 'Restrict']],
                             columns=['zip', 'in_topic', 'out_topic'])
        restriction_report(md_df, 'test_data')

        # Tests the contents of the restriction_review.csv.
        result = csv_to_list(os.path.join('test_data', 'restriction_review.csv'))
        expected = [['zip', 'in_topic', 'out_topic', 'in_topic_split', 'out_topic_split'],
                    [30602, 'citizen', 'Restrict', 'citizen', 'Restrict'],
                    [30603, 'crime', 'Restrict', 'crime', 'Restrict'],
                    [30605, 'court', 'Restrict', 'court', 'Restrict']]
        self.assertEqual(expected, result, "Problem with test for restrict_in")

    def test_restrict_in_out(self):
        """Test for when the restricted topic is in in_topic and out_topic"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Safe', np.nan],
                              ['30601', 'Safe', 'Safe'],
                              ['30602', 'immigrant', 'immigration'],
                              ['30603', 'migrant', 'migrant'],
                              ['30604', 'Safe', 'basketball court'],
                              ['30605', 'citizen', 'refugee']],
                             columns=['zip', 'in_topic', 'out_topic'])
        restriction_report(md_df, 'test_data')

        # Tests the contents of the restriction_review.csv.
        result = csv_to_list(os.path.join('test_data', 'restriction_review.csv'))
        expected = [['zip', 'in_topic', 'out_topic', 'in_topic_split', 'out_topic_split'],
                    [30602, 'immigrant', 'immigration', 'immigrant', 'immigration'],
                    [30603, 'migrant', 'migrant', 'migrant', 'migrant'],
                    [30605, 'citizen', 'refugee', 'citizen', 'refugee']]
        self.assertEqual(expected, result, "Problem with test for restrict_in_out")

    def test_restrict_out(self):
        """Test for when the restricted topic is in out_topic"""
        # Makes a dataframe to use as test input and runs the function.
        md_df = pd.DataFrame([['30600', 'Safe', np.nan],
                              ['30601', 'Safe', 'Safe'],
                              ['30602', 'Restrict', 'citizenship'],
                              ['30603', 'Restrict', 'criminal justice'],
                              ['30604', 'Safe', 'basketball court'],
                              ['30605', 'Restrict', 'immigrant']],
                             columns=['zip', 'in_topic', 'out_topic'])
        restriction_report(md_df, 'test_data')

        # Tests the contents of the restriction_review.csv.
        result = csv_to_list(os.path.join('test_data', 'restriction_review.csv'))
        expected = [['zip', 'in_topic', 'out_topic', 'in_topic_split', 'out_topic_split'],
                    [30602, 'Restrict', 'citizenship', 'Restrict', 'citizenship'],
                    [30603, 'Restrict', 'criminal justice', 'Restrict', 'criminal justice'],
                    [30605, 'Restrict', 'immigrant', 'Restrict', 'immigrant']]
        self.assertEqual(expected, result, "Problem with test for restrict_out")


if __name__ == '__main__':
    unittest.main()
