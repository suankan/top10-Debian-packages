# Description

This python tool analyses Debian mirror and finds top 10 packages by number of files.

# How to use this tool

## Run the tool

Execute it with specifying arch as a positional arg cmd option e.g. amd64, arm64, armel, armhf, i386 etc.

```bash
$ python3 ./package_statistics.py i386
TOP_N DEBIAN PACKAGE               NUM FILES
1.    x11/numix-icon-theme           68920
2.    games/flightgear-data-base     64707
3.    fonts/texlive-fonts-extra      45910
4.    rust/rust-doc                  45641
5.    doc/trilinos-doc               45567
6.    games/widelands-data           34985
7.    misc/moka-icon-theme           32533
8.    doc/vtk6-doc                   29464
9.    gnome/faenza-icon-theme        29400
10.   fonts/fonts-mathjax-extras     29035
```

The utility does:
- Download corresponding Contents index file from Debian repo e.g. http://ftp.debian.org/debian/dists/stable/main/Contents-i386.gz
- Parse content as described below.
- Find out and list top 10 biggest packages for this architechture.

## Run unit tests

You can also execute unit tests and see how they go:
```bash
$ python3 ./contents_index_tests.py -v
test_calc_packages_size (__main__.ContentsIndexTests) ... ok
test_curate_line_filename_with_whitespaces (__main__.ContentsIndexTests) ... ok
test_curate_line_one_file_many_pkg (__main__.ContentsIndexTests) ... ok
test_curate_line_one_file_one_pkg (__main__.ContentsIndexTests) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.004s

OK
```

# "Contents" indices

From [here](https://wiki.debian.org/DebianRepository/Format?action=show&redirect=RepositoryFormat#A.22Contents.22_indices)

The files dists/$DIST/$COMP/Contents-$SARCH.gz (and dists/$DIST/$COMP/Contents-udeb-$SARCH.gz for udebs) are so called Contents indices. The variable $SARCH means either a binary architecture or the pseudo-architecture "source" that represents source packages. They are optional indices describing which files can be found in which packages. Prior to Debian wheezy, the files were located below "dists/$DIST/Contents-$SARCH.gz".

Contents indices begin with zero or more lines of free form text followed by a table mapping filenames to one or more packages. The table SHALL have two columns, separated by one or more spaces. The first row of the table SHOULD have the columns "FILE" and "LOCATION", the following rows shall have the following columns:

A filename relative to the root directory, without leading .
A list of qualified package names, separated by comma. A qualified package name has the form [[$AREA/]$SECTION/]$NAME, where $AREA is the archive area, $SECTION the package section, and $NAME the name of the package. Inclusion of the area in the name should be considered deprecated.
Clients should ignore lines not conforming to this scheme. Clients should correctly handle file names containing white space characters (possibly taking advantage of the fact that package names cannot include white space characters).

# Example study on Contents-amd64.gz

I've taken just one contents index file
http://ftp.uk.debian.org/debian/dists/stable/main/Contents-amd64.gz

## File structure

Despite debian docs say that the first row of the table SHOULD have the columns "FILE" and "LOCATION", this is not the case in Contents-amd64.gz. In fact, actual data goes straight away.

```
bin/ash                                                 shells/ash
bin/bash                                                shells/bash
bin/bash-static                                         shells/bash-static
bin/bsd-csh                                             shells/csh
bin/btrfs                                               admin/btrfs-progs
bin/btrfs-calc-size                                     admin/btrfs-progs
bin/btrfs-convert                                       admin/btrfs-progs
bin/btrfs-debug-tree                                    admin/btrfs-progs
bin/btrfs-find-root                                     admin/btrfs-progs
bin/btrfs-image                                         admin/btrfs-progs
bin/btrfs-map-logical                                   admin/btrfs-progs
bin/btrfs-select-super                                  admin/btrfs-progs
bin/btrfs-show-super                                    admin/btrfs-progs
bin/btrfs-zero-log                                      admin/btrfs-progs
bin/btrfsck                                             admin/btrfs-progs
bin/btrfstune                                           admin/btrfs-progs
bin/bunzip2                                             utils/bzip2
bin/busybox                                             utils/busybox,shells/busybox-static
bin/bzcat                                               utils/bzip2
```

The Contents index file seems to be sorted by the first column in this way:

1. the first word before forward slash
2. the second word after the first forward slash
3. the third word after the second forward slash
4. the forth word after the third forward slash
...
etc.

## Size

The above Contents-amd64.gz file is 31369550 bytes gzipped.

Ungzipped it is 454658746 bytes and 5143829 lines.

```bash
$ cat Contents-amd64 | wc -l
 5143829
```

## Total number of packages

```bash
$ cat Contents-arm64 | awk '{print $2}' | sort -u | wc -l
   53434
```

# Task paraphrasing and understanding

Phrase "Top 10 packages that have the most files associated with them" means
- we need to know how many files belong to packages
- we need to find 10 biggest packages by number of files

# First thoughts on algorithm

We will read the whole Contents file line by line.

We will use a dict `packages` with package name as key and number of files as value.

Package names are good for dict keys because they are unique and hashable.
And as we go through the Contents index and our dict will be growing, lookup if every next package name from Contents index is already in the dict will be a constant time operation.

```
for each line:
  if line.package_name not in packages:
    it means that we have not seen files belownging to this package yet
    we need to start counting the number of files for it.
    since this is a first file of this package we set count to 1
    packages['line.package_name'] = 1
  else:
    it means that we have already seen some files of this package
    so we update dict `packages` and increment value by 1 of corresponding package
    packages['line.package_name'] += 1
```

In the end, our dict `packages` will have all the packages from Contents index and number of files for each of them

```
{
  package_1: num_files_1,
  package_2: num_files_2,
  ...
  package_N: num_files_M
}
```

In Python 3.6 the result dict will be insert ordered.

# Find top L biggest packages by number of their files

We can do it do, e.g. by heapq.nlargest()

Or we can do it via collections.Counter() but that uses heapq.nlargest() under the hood.
