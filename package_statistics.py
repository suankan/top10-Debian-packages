#!/usr/local/bin/python
import heapq
from collections import Counter

packages = {}

# return an object {filename,package}
def parse_line():
  pass

with open('tmp/Contents-amd64') as file:
  for line in file:
    line_pair = line.split(" ", 1)
    filename = line_pair[0]
    package = line_pair[1]
    if package not in packages:
      packages[package] = 1
    else:
      packages[package] += 1

n = 10

print heapq.nlargest(n, packages.items(), key=lambda i: i[1])

print Counter(packages).most_common(10)