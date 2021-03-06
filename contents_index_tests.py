'''
Unit tests for articles modules
'''

import unittest
from contents_index import ContentsIndex


class ContentsIndexTests(unittest.TestCase):
    '''
    Unit tests for contents_index module.
    '''

    def test_curate_line_one_file_many_pkg(self):
        '''
        Test fucntion ContentsIndex._curate_line_test(raw_string)
        Case when there are multiple packages as a comma-separated list
        '''

        # Setup the test data
        raw_line = 'bin/busybox        utils/busybox,shells/busybox-static'
        expected_result = [
            ['bin/busybox', 'utils/busybox'],
            ['bin/busybox', 'shells/busybox-static'],
        ]

        result = ContentsIndex.curate_line(raw_line)

        self.assertListEqual(expected_result, result)

    def test_curate_line_one_file_one_pkg(self):
        '''
        Test fucntion ContentsIndex._curate_line_test(raw_string)
        Simple case: one file, one package
        '''

        # Setup the test data
        raw_line = 'bin/busybox        utils/busybox'
        expected_result = [
            ['bin/busybox', 'utils/busybox']
        ]

        result = ContentsIndex.curate_line(raw_line)

        self.assertListEqual(expected_result, result)

    def test_curate_line_filename_with_whitespaces(self):
        '''
        Test fucntion ContentsIndex._curate_line_test(raw_string)
        Simple case: filename with spaces, multiple packages
        '''

        # Setup the test data
        raw_line = 'bin/busy box        utils/busybox,shells/busybox-static'
        expected_result = [
            ['bin/busy box', 'utils/busybox'],
            ['bin/busy box', 'shells/busybox-static'],
        ]

        result = ContentsIndex.curate_line(raw_line)

        self.assertListEqual(expected_result, result)

    def test_calc_packages_size(self):
        '''
        Test case:
        '''

        # Setup test data
        expected_result = {
            'debian-installer/ca-certificates-udeb': 1,
            'qwe/asd': 3,
            'debian-installer/fonts-freefont-udeb': 1,
            'debian-installer/ttf-freefont-udeb': 1,
            'sound/zynaddsubfx-data': 1
        }

        my_contents_index = ContentsIndex('test')
        # A sample of Contents-test.gz is prepared and placed
        # in the current directory
        my_contents_index.calc_packages_size()

        self.assertDictEqual(my_contents_index._packages_size, expected_result)


if __name__ == '__main__':
    unittest.main()
