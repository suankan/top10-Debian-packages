class contents_index:
  '''
  This class represents "Contents" indices which is described here:
  https://wiki.debian.org/DebianRepository/Format?action=show&redirect=RepositoryFormat#A.22Contents.22_indices
  '''

  # This dict will store number of files in each package:
  # {
  #   package_0: number_of_files_0,
  #   package_1: number_of_files_1,
  #   ...
  #   package_N: number_of_files_N,
  # }
  _packages_size = {}

  # For simplicity we will use just a single debian mirror and just fail if it not available.
  # TODO: Implement trying iterations over different mirrors.
  _debian_mirror = 'http://ftp.debian.org/debian/dists/stable/main/'

  def __init__(self, file, arch):
    '''
    This is a constructor for this class
    '''
    # TODO why is it needed and what should be here.
    pass

  def _curate_line(self, raw_line):
    '''
    This method processes a line of "Contents" indices file by:
    - first space-separate string will be considered as filename
    - second space-separated string will be considered as comma-separated list of packages.

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

    pass


  def _get_contents_file(self, arch):
    '''
    This function will download Contents index file from Debian repo for a given architecture.
    E.g. http://ftp.debian.org/debian/dists/stable/main/Contents-amd64.gz
    '''
    pass

  def _ungz_contents_file(self):
    '''
    This function will unarchive gz contents file.
    '''

    # import gzip
    # import shutil
    # with gzip.open('file.txt.gz', 'rb') as f_in:
    #   with open('file.txt', 'wb') as f_out:
    #     shutil.copyfileobj(f_in, f_out)
    pass

  def _get_packages_size(self):
    '''
    This function will actually scan the Contents index file and populate self._packages_size dict.
    '''

    # for package in curr_packages:
    #   if package not in _packages:
    #     _packages[package] = 1
    #   else:
    #     _packages[package] += 1
    pass

  def _get_top(self, n):
    '''
    This function will get top n packages from the obtained self._packages_size dict
    '''

    # from heapq import nlargest
    # from collections import Counter
    # print heapq.nlargest(n, packages.items(), key=lambda i: i[1])
    # print Counter(packages).most_common(10)
    pass
