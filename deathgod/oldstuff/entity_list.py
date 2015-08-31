#!/usr/bin/env python
# encoding: utf-8
"""
entity_list.py

Created by William Makley on 2008-04-02.
Copyright (c) 2008 Tritanium Enterprises. All rights reserved.
"""

def compare_elist(e1, e2):
    """Comparison function for entities."""
    sp1 = e1.sorting_priority
    sp2 = e2.sorting_priority
    if sp1 > sp2:
        return 1
    elif sp1 == sp2:
        return 0
    else:
        return -1

class EntityList(list):
    """A container for a bunch of entities. Keeps them sorted."""
    def __init__(self):
        list.__init__(self)
        
    def add_entity(self, entity):
        """Add an entity to the list"""
        self.append(entity)
        if self.size() > 0:
            self.sort()
        
    def remove_entity(self, entity):
        """Remove an entity from the list"""
        return self.remove(entity)
        
    def sort(self):
        """Sorts the EntityList"""
        list.sort(self, compare_elist)
        
    def size(self):
        return len(self)
        
    def hasVisibleEntity(self):
        ret = False
        for e in self:
            if e.isVisible() == True:
                ret = True
                break
        return ret
        
    def topVisibleEntity(self):
        """Returns the entity at the top of the list that's visible"""
        if self.size() == 0:
            return None
                
        i = self.size() - 1
        while i >= 0:
            e = self[i]
            if e.isVisible() == True:
                return e
            i = i - 1
        return None

def main():
    print(EntityList.__doc__)


if __name__ == '__main__':
    main()

