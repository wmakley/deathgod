#!/usr/bin/env python
# encoding: utf-8
"""
action.py

Created by William Makley on 2008-06-29.

The scripting interface for deathgod.
"""

from . import event


class Action:
    def __init__(self, function, objects):
        self.function = function
        self.objects = objects
    
    def run(self):
        self.function(self.objects)



if __name__ == '__main__':
    print(__doc__)

