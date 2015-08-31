"""
item.py -- contains classes and functions relating to items

Public Members:

ItemArchetype
Item
ItemStack
add_archetype
get_archetype

"""

from .entity import Entity

class Item():
    """Defines an item in Death God.
    
    More when I decide how the hell this will work
    """
    
    def __init__(self):
        pass
        
        
class ItemArchetype():
    """who knows"""
    def __init__(self):
        pass
        

class ItemList(list):
    """A container for a bunch of items."""
    def __init__(self, items):
        list.__init__(self)
        for item in item:
            self.add_item(item)
            
    def add_item(self, item):
        self.append(item)
        
        
class ItemStack(ItemList, Entity):
    """An ItemList that's on the game map."""
    def __init__(self):
        pass
        
_archetypes = []

def add_archetype(arch):
    """docstring for add_archetype"""
    idx = len(_item_types)
    _archetypes.append(arch)
    return idx
    
def get_archetype(idx):
    """docstring for get_archetype"""
    return _archetypes[idx]
    

if __name__ == '__main__':
    print(__doc__)