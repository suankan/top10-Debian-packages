#!/usr/local/bin/python
import argparse
from contents_index import ContentsIndex

parser = argparse.ArgumentParser()
parser.add_argument(
    "arch", help="Arch of Debian Contents index \
        e.g. Contents-amd64.gz in Contents-amd64.gz")
args = parser.parse_args()

# Get the Contents index file for a given arch
my_contents_index = ContentsIndex(args.arch)
my_contents_index.download_contents_index()
my_contents_index.calc_packages_size()
# Get 10 biggest packages by nuber of files
top_10 = my_contents_index.get_top(10)

# Prepare to print the obtained stats.
# Calc widths of each column.
pkg_width = max(len(str(line[0])) for line in top_10) + 2
num_width = max(len(str(line[1])) for line in top_10) + 2
# Print header according to calulated column widths
print('{:<5} {:<{pkg_width}} {:>{num_width}}'.format(
    'TOP_N', 'DEBIAN PACKAGE', 'NUM FILES',
    pkg_width=pkg_width, num_width=num_width))

num = 1
for item in top_10:
    # Print each stat according to calulated column widths
    print('{:<5} {:<{pkg_width}} {:>{num_width}}'.format(
        str(num) + '.', item[0], item[1],
        pkg_width=pkg_width, num_width=num_width))
    num += 1
