import os
import shutil
import unittest
from aip_prep import metadata_aip


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the output folder, if made"""
        aips_dir = os.path.join(os.getcwd(), 'metadata_aip', 'aips_dir')
        if os.path.exists(aips_dir):
            shutil.rmtree(aips_dir)

    def test_function(self):
        """No meaningful variations in how this function works"""
        # Makes aips_dir, which is typically made earlier in the script, and runs the function.
        input_dir = os.path.join(os.getcwd(), 'metadata_aip', 'export')
        aips_dir = os.path.join(os.getcwd(), 'metadata_aip', 'aips_dir')
        os.mkdir(aips_dir)
        metadata_aip(input_dir, aips_dir)

        # Tests the contents of the aips_dir.
        result = []
        for root, dirs, files in os.walk(aips_dir):
            for file in files:
                result.append(os.path.join(root, file))
        expected = [os.path.join(aips_dir, 'metadata', 'metadata_1.txt'),
                    os.path.join(aips_dir, 'metadata', 'metadata_2.txt'),
                    os.path.join(aips_dir, 'metadata', 'metadata_3.txt')]
        self.assertEqual(expected, result, "Problem with test for metadata_aip function")


if __name__ == '__main__':
    unittest.main()
