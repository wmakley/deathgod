#!/usr/bin/env python
# encoding: utf-8
"""
clean_pyc.py

Usage: clean_pyc.py [target_directory]

Walks a directory structure and removes all byte-code-compiled
".pyc" files. Default target_directory is "./src"

Created by William Makley on 2008-10-09.
No rights reserved/don't care/etc
"""

import sys
import os
import re


REGEX = re.compile(r"""
^           # start of file name
.+          # one or more any character
\.pyc       # ".pyc"
$
""", re.VERBOSE)


def main(argv):
    if len(argv) < 2:
        target_dir = "./src"
    else:
        target_dir = argv[1]

    print("Removing .pyc files... ")

    for root, _, files in os.walk(target_dir):
        for f in files:
            match = re.search(REGEX, f)
            if match is not None:
                file_to_remove = os.path.join(root, f)
                print("Removing ", file_to_remove)
                os.remove(os.path.join(root, f))

    print("Success!")

    return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv))

