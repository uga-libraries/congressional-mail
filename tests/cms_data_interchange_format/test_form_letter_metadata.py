import os
import unittest
from cms_data_interchange_format import form_letter_metadata
from test_script import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the function output, if made"""
        md_path = os.path.join('test_data', 'form_letter_metadata', 'form_letter_metadata.csv')
        if os.path.exists(md_path):
            os.remove(md_path)

    def test_correct(self):
        """Test for when the form letter file is present and can be read"""
        # Make variables and run the function being tested.
        input_dir = os.path.join('test_data', 'form_letter_metadata', 'export')
        output_dir = os.path.join('test_data', 'form_letter_metadata')
        form_letter_metadata(input_dir, output_dir)

        # Confirm the contents of form_letter_metadata.csv.
        result = csv_to_list(os.path.join(output_dir, 'form_letter_metadata.csv'))
        expected = [['letter_code', 'letter_description', 'document_name', 'owner', 'creation_date', 'revision_date',
                     'archive_flag', '1', '2', '3', '4'],
                    ['60', 'BLANK', 'BLANK', '958584', '20150518', '20170522', 'Closed', 'BLANK',
                     'Small Business & Grants Workshop', 'enewsletters\\60.html', 'eNewsletter'],
                    ['68', 'Version:3 Letter_Name:DEF- Air Tanker Contract', 'forms\\68.doc', '321897', '20080703',
                     '20150109', 'Closed', 'Version:3 Letter_Name:DEF- Air Tanker Contract', 'Newsletter',
                     'forms\\68.html', 'Standard'],
                    ['69', 'Version:5 Letter_Name:DEF- MHADA (Thanks)', 'forms\\69.doc', '321897', '20080703',
                     '20150109', 'Closed', 'Version:5 Letter_Name:DEF- MHADA (Thanks)', 'Newsletter',
                     'forms\\69.html', 'Standard'],
                    ['71', 'Version:1 Letter_Name:ENV- Clean Boating Act of 2008_HR5949', 'forms\\71.doc', '321897',
                     '20080707', '20150109', 'Closed', 'Version:1 Letter_Name:ENV- Clean Boating Act of 2008_HR5949',
                     'Newsletter', 'forms\\71.html', 'Standard'],
                    ['79', 'Information:Letter to be sent with first privacy waiver. Version:1 Letter_Name:Privacy Waiver Letter',
                     'forms\\79.doc', '321897', '20070917', '20150212', 'Closed',
                     'Information:Letter to be sent with first privacy waiver. Version:1 Letter_Name:Privacy Waiver Letter',
                     'Newsletter', 'forms\\79.html', 'Standard'],
                    ['489', 'Version:11 Letter_Name:Social Security - GEN', 'forms\\489.doc', '321897', '20111025',
                     '20150109', 'Closed', 'Version:11 Letter_Name:Social Security - GEN', 'Newsletter',
                     'forms\\489.html', 'Standard'],
                    ['1273', 'AR-114-Red Wolves', 'forms\\1273.doc', '958583', '20150318', '20210818', 'Closed',
                     'AR-114-Red Wolves', 'Newsletter', 'forms\\1273.html', 'Standard'],
                    ['1287', 'CN-114-Chicago PD Homan Square 4.16.15', 'forms\\1287.doc', '958583', '20150428',
                     '20210818', 'Closed', 'CN-114-Chicago PD Homan Square 4.16.15', 'Newsletter',
                     'forms\\1287.html', 'Standard']]
        self.assertEqual(expected, result, "Problem with test for correct")


if __name__ == '__main__':
    unittest.main()
