'''
This module makes some interface and tooling backend to work with Debian Contents indexes.
'''

import gzip
import requests
from heapq import nlargest

class ContentsIndex:
    '''
    This class represents "Contents" indices which is described here:
    https://bit.ly/2IDN6pu

    Usage:
    Instantiating:
        Set debian mirror URL to use.
        Set ARCH we dealing with which identifies Contents index file.
        Get Contents index file
        Ungzip obtained Contents index file

    Possible public actions:
        - calculate number of files in each deb package from
            Contents index file
        - get top N packages by number of files

    Potential private actions:
        - constructor
        - ungzip obtained Contents index file
        - download Contents index file for a given arch
        - curate each line of Contents index file
    '''

    def __init__(self, arch):
        '''
        This is a constructor for this class.
        '''

        # For simplicity we will use just a single debian mirror
        # and just fail if it not available.
        self._debian_mirror = 'http://ftp.debian.org/debian/dists/stable/main'
        self.arch = arch
        self._contents_index_filename = 'Contents-' + self.arch + '.gz'
        self._contents_index_file_url = \
            self._debian_mirror + '/' + self._contents_index_filename

        # This dict will store number of files in each package:
        # {
        #   package_0: number_of_files_0,
        #   package_1: number_of_files_1,
        #   ...
        #   package_N: number_of_files_N,
        # }
        self._packages_size = {}

    @staticmethod
    def curate_line(raw_line):
        '''
        This method processes a line of "Contents" indices file by:
        - first space-separate string will be considered as filename
        - second space-separated string will be considered as
            comma-separated list of packages.

        Given a raw line:
        'bin/busybox        utils/busybox,shells/busybox-static'

        It will return a list of strings:
        [
        'bin/busybox utils/busybox',
        'bin/busybox shells/busybox-static',
        ]

        If raw line specifies just one package,
        'bin/bzcat        utils/bzip2'
        then it will return a list with a single string:
        [
        'bin/bzcat utils/bzip2',
        ]

        If malformed raw string is passed which does not follow "Contents" indices spec
        Then result is... I need to think about it.
        '''

        # Split space-separated raw line:
        # 'bin/busy box        utils/busybox,shells/busybox-static'
        # into list:
        # ['bin/busy box       ', ' ', 'utils/busybox,shells/busybox-static']
        raw_list = raw_line.rpartition(" ")

        # First element will always be filename
        file = raw_list[0].strip()

        # Third element will always be comma-separated list of packages
        # From comma-separated string:
        #   '       utils/busybox,shells/busybox-static'
        # Extract packages list:
        #   ['utils/busybox', 'shells/busybox-static']
        packages = raw_list[2].split(",")

        # Set empty list for storing result which we will be
        # populated with strings and returned
        result = []

        # When this is a comma-separated packages list
        for package in packages:
            # Add list [file, package] to result list
            result.append([file, package])

        return result

    def download_contents_index(self):
        '''
        This function will download Contents index file from Debian repo
        for a given architecture and save it in the current directory.
        E.g. http://ftp.debian.org/debian/dists/stable/main/Contents-amd64.gz
        '''

        # Download gzipped file from Debian mirror and
        # save it in the currenrt directory
        response = requests.get(self._contents_index_file_url, stream=True)
        with open(self._contents_index_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=256):
                file.write(chunk)

    def get_packages_size(self):
        '''
        This function will actually scan the Contents index
        file and populate self._packages_size dict.
        '''

        with gzip.open(self._contents_index_filename, 'rb') as file:
            for raw_line in file:
                # Some observation I made: default data after gzip.open
                # is byte type. Which is essentially Latin1.
                # Converting it to utf-8 :)
                raw_line = raw_line.decode('utf-8').strip()
                # A line can be 'file  name    package1,package2,...,packageN'
                # We will curate it via self.curate_line(raw_line)
                for line in self.curate_line(raw_line):
                    # After curating the second space-separated element
                    # is always a single package name
                    package = line[1]

                    # Implementing algorithm described in readme.
                    if package not in self._packages_size:
                        # If package name does not found in dict
                        # self._packages_size, this means we hit the first
                        # file of this package.
                        self._packages_size[package] = 1
                    else:
                        # If package name is found in dict
                        # self._packages_size, this means we have faced this
                        # file before, hence increment counter.
                        self._packages_size[package] += 1

    def get_top(self, num):
        '''
        This function will get top num packages from
        the obtained self._packages_size dict
        '''

        return nlargest(num, self._packages_size.items(), key=lambda i: i[1])
