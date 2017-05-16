#!/usr/bin/env python
# encoding: utf-8
"""
entity.py -- defines the Entity class and some relevant globals

The Entity class is anything on a Death God map that is not part
of the terrain.

This module also maintains a list of all the sprites used by entities
in the current program. (Rather than each entity owning its own bitmap,
multiple entities can reference the same bitmap.)

public members:

Entity
EntityList
compare_entities
add_sprite
get_sprite
default_entity_fstr

"""

from pygame.sprite import Sprite
from .directions import *
from .ordered_pair import x, y
from . import fonts
from .ascii_gfx import StyledString


class Entity(Sprite):
    """
    An entity is anything on the map that's not part of the terrain.

    - Entities can either be passable or impassable by other entities.
      If a single impassable Entity is on a tile, no other impassable
      entities may move onto that tile.
    - Entities should specify a name for the look command, and
      optionally a description
    - Every turn, the update method of all active entities is called
      unless that entity is not active
    - If any entity attempts to move into a square occupied by another
      entity, that entity's interact method is called (maybe this
      mechanic needs to be less simplistic?)
    - Entities may either be visible or invisible. Invisible Entities
      are simply not drawn on the map
    - Because an Entity is a Listener, it may post events to its
      evManager object reference

    Public Members:

        update
        interact
        sprite
        position
        description
        visible
        passable
        sorting_priority
        move_in_direction
    """

    def __init__(self, game, position, name, sprite_idx=0):
        """
        Initialize Entity.

        Arguments:

        game
            -- a reference to the game object with methods the entity
            can call to manipulate its surroundings
        position
            -- the position of the entity on the map (relative to
               lower left corner of said map)
        name
            -- the name of the entity, appears when the player uses
               the look command
        sprite_idx
            -- the index of the entity's sprite (default 0)

        """
        Sprite.__init__(self)
        self.type = "Entity"
        self.__game = game
        self.__name = name
        self.__position = list(position)
        self.__sprite = sprite_idx
        self.__visible = False
        self.__passable = True
        self.__sorting_priority = 0
        self.active = False
        self.mark = -1


    def update(self):
        """
        What the entity should do every time the player moves.

        For sub-classes to override.

        """
        pass


    def interact(self, antagonist):
        """
        Called whenever another entity attempts to move into this one.

        For sub-classes to override.

        """
        pass



    @property
    def game(self):
        return self.__game


    def get_description(self):
        """(string) The Entity's description for the look command."""
        return "It is an Entity."


    @property
    def name_starts_with_vowel(self):
        char = self.name[0:1]
        if char == 'A' or char == 'a' or\
           char == 'E' or char == 'e' or\
           char == 'I' or char == 'i' or\
           char == 'O' or char == 'o' or\
           char == 'U' or char == 'u':
            return True
        else:
            return False


    def get_name(self):
        """The Entity's name."""
        return self.__name

    def set_name(self, name):
        self.__name = name

    name = property(get_name, set_name)


    def get_sprite(self):
        return get_sprite(self.__sprite)

    def set_sprite(self, sprite_idx):
        self.__sprite = sprite_idx

    sprite = property(get_sprite, set_sprite)


    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position[0] = position[0]
        self.__position[1] = position[1]

    position = property(get_position, set_position)


    def is_visible(self):
        return self.__visible

    def set_visible(self, value):
        self.__visible = value

    visible = property(is_visible, set_visible)


    def is_passable(self):
        return self.__passable

    def set_passable(self, value):
        self.__passable = value

    passable = property(is_passable, set_passable)


    def set_sort_priority(self, priority):
        """Sets the entity's sorting priority"""
        self.__sorting_priority = priority

    def get_sort_priority(self):
        """Returns the entity's sorting priority"""
        return self.__sorting_priority

    sorting_priority = property(get_sort_priority, set_sort_priority)


    def move_in_direction(self, direction):
        """Moves Entity one tile in a specified direction.

        Directions are defined in directions.py

        """
        if direction == NORTH:
            self.__position[y] += 1
        elif direction == NORTHEAST:
            self.__position[x] += 1
            self.__position[y] += 1
        elif direction == EAST:
            self.__position[x] += 1
        elif direction == SOUTHEAST:
            self.__position[x] += 1
            self.__position[y] -= 1
        elif direction == SOUTH:
            self.__position[y] -= 1
        elif direction == SOUTHWEST:
            self.__position[x] -= 1
            self.__position[y] -= 1
        elif direction == WEST:
            self.__position[x] -= 1
        elif direction == NORTHWEST:
            self.__position[x] -= 1
            self.__position[y] += 1


# includes one default sprite
default_entity_fstr = StyledString('e', fonts.normal, (255, 0, 0), True)

_sprite_list = [default_entity_fstr.create_surface()]

def add_sprite(s):
    """
    Returns the index of a sprite added to the global entity sprite list.

    Arguments:

    sprite -- The sprite to add.

    """
    idx = len(_sprite_list)
    _sprite_list.append(s)
    return idx


def get_sprite(idx):
    """Returns the sprite in the global entity sprite list at the specified index."""
    #print "in get_sprite: idx = %s" % str(idx)
    return _sprite_list[idx]


types = []
def add_type(t):
    ret = len(types)
    types.append(t)
    return ret


def compare_entities(e1, e2):
    """
    Comparison function for entities.

    Compares sorting priority.
    Returns:
        1 if e1 is higher
        0 if e1 and e2 are equal
       -1 if e2 is higher
    """
    sp1 = e1.sorting_priority
    sp2 = e2.sorting_priority
    if sp1 > sp2:
        return 1
    elif sp1 == sp2:
        return 0
    else:
        return -1


class EntityList(list):
    """A container for a bunch of entities. Keeps them sorted.

    Currently this is implemented with the entity with index 0 being the bottom
    of the pile. I'm not sure why I did this, but there may very well have been a reason.
    It probably doesn't matter. Bottom line it may be best to avoid indexing into this
    container directly.
    """
    def __init__(self):
        list.__init__(self)


    def add_entity(self, entity):
        """Add an entity to the list.

        Arguments:
            entity - the entity to add
        """
        self.append(entity)
        if self.size > 0:
            self.sort()


    def remove_entity(self, entity):
        """Remove an entity from the list.

        Really just a more verbose way to call remove, but should be
        used in case the implementation changes.

        Arguments:
            entity - the entity to remove
        """
        #if entity.mark != -1:
            #print "in EntityList: remove_entity: trying to remove entity with mark %d" % entity.mark
        return self.remove(entity)


    def sort(self):
        """Sorts the EntityList."""
        list.sort(self, key=lambda e: e.sorting_priority)


    @property
    def size(self):
        """Returns integer - the size of the list."""
        return len(self)


    @property
    def has_visible_entity(self):
        """Check whether any Entity in the list is visible.

        Returns:
            True if there is at least one visible Entity
            False if not
        """
        ret = False
        for e in self:
            if e.is_visible() == True:
                ret = True
                break
        return ret


    @property
    def top_visible_entity(self):
        """Returns the entity at the top of the list that's visible."""
        if self.size == 0:
            return None

        i = self.size - 1
        while i >= 0:
            e = self[i]
            if e.visible:
                return e
            i = i - 1
        return None


if __name__ == "__main__":
    print(__doc__, Entity.__doc__)

