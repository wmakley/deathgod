"""tile.py - everything to do with tiles

Sorry, it's kind of a mess since I haven't been able to get the
best way to organize this straight in my head. To add new types of
terrain to the game, edit the _tile_attrs list.

public members:

Tile
CharDescription
TileDescription
map_font
get_tile_sprites
get_tile_desc
"""

import pygame
import settings
import fonts
from pygame.sprite import *
import entity
from ascii_gfx import *

class Tile:
    """Every single tile you see on the map in Death God is one of these."""
    
    def __init__(self, tile_type, passable, height=0):
        """Arguments:
        
        tile_type
            -- (string) the key word for the type of tile that this will appear as
               (edit "_tile_attrs" in this module to alter this list)
        passable
            -- (boolean) whether or not the tile is passable
               since this is separate from the display type, you can make passable
               walls for secret passages etc.
        height
            -- no height system is implemented currently, and it is uncertain
               if it is even a good idea. (default 0)
        """
        self.tile_type = tile_type
        self.passable = passable
        self.height = height
        self.explored = False
        self.entities = entity.EntityList()
    
    def add_entity(self, entity):
        """Adds an entity to the tile's entity list"""
        self.entities.add_entity(entity)
    
    def remove_entity(self, entity):
        """Removes an entity from the tile's entity list"""
        return self.entities.remove_entity(entity)
    
    @property
    def has_entity(self):
        """Returns True if there is at least one visible entity, False if not"""
        if self.entities.size > 0:
            return True
        else:
            return False
    
    def get_top_visible_entity(self):
        """Returns the entity that should be drawn on top"""
        return self.entities.top_visible_entity
    
    
    def character_can_enter(self, ch=None):
        """Returns True if Character (ch) can enter this tile, False if not
        
        Honestly at this point there is no system in place for some Characters
        to be impassable and others not, so it doesn't matter if you pass a Character
        into this method, as the result will always be the answer to the question:
        "Is is this tile passable and are all the entities on it passable?"
        """
        if not self.passable:
            return False
        
        for e in self.entities:
            if not e.passable:
                return False
        
        return True


class CharDescription(Sprite):
    """Class to associate a character with a font and color.
    
    These attributes can be used to generate a surface from the
    character.
    """
    
    def __init__(self, font=fonts.normal, char=" ", color=(0,0,0)):
        """Arguments:
        
        font
            -- the pygame Font object to use (default fonts.normal)
        char
            -- the character (honestly there is nothing stopping you
               from putting a whole string in here) default: space
        color
            -- the font color
        """
        Sprite.__init__(self)
        self.font = font
        self.char = char
        self.color = color
    
    def create_sprite(self, bg_color=None):
        """Returns the pygame surface of this character rasterized.
        
        Arguments:
        
        bg_color -- the color key to use for transparency (default None)
        """
        return self.font.render(self.char, True, self.color, bg_color)


class TileDescription(CharDescription):
    """Basically each different type of terrain is defined by an instance of this class.
    
    Man what a mess. I can't believe I wrote this crap, but it basically works.
    It subclasses "CharDescription" simply to save having to type like three variables
    into the __init__ method apparently. Then it saves a bunch of other data, like
    a normal color (v) vs. fog of war color (h). I'm pretty sure it doesn't currently
    use color keys for the text rendering since invisible portions of the resultant
    rasterized text kept overflowing tiles and there was no way to make it look right.
    
    (Too bad too, because the color key text blitting was way faster.)
    
    A tile is currently drawn using four pygame surfaces, that the methods in this class
    generate:
        
        - a square surface filled with the background color (if defined)
        - a rendered surface of the tile's ASCII character
        - alternate color fog war versions of each
    
    Public Members:
    
    create_sprite
    create_bg_surface
    create_sprites
    """
    
    def __init__(self, font=fonts.normal, char='', color=(0,0,0),
                 solid_bg=False, bg_color=settings.map_center_color):
        """Arguments:
        
        font
            -- the font to use to render the tile (default fonts.normal)
        char
            -- the ASCII character used to represent the tile (default '')
        solid_bg
            -- whether the tile has its own background color that the character
               will be rendered on top of. Will still be visible even if the character
               is covered by something. (default False)
        bg_color
            -- if solid_bg is True, this is the background color. RGB tuple.
               (default (0, 0, 0))
        """
        CharDescription.__init__(self, font, char, color)
        self.color_v = self.color
        self.color_h = tuple([ele/2 for ele in self.color_v]) # make fog of war color
        self.solid_bg = solid_bg
        self.bg_color_v = bg_color
        self.bg_color_h = tuple([ele/2 for ele in self.bg_color_v]) # make fog of war color
        #print "color_v = %s, color_h = %s" % (self.color_v, self.color_h)
    
    def create_sprite(self, visible=True):
        """Render the tile's character. Returns a pygame Surface.
        
        Arguments:
        
        visible -- whether to render the fog of war version of the tile
                   (default False)
        """
        if visible:
            color = self.color_v
            bg_color = self.bg_color_v
        else:
            color = self.color_h
            bg_color = self.bg_color_h
            
        s = self.font.render(self.char, True, color, bg_color)
            
        return s
    
    def create_bg_surface(self, size, visible=True):
        """Returns a Surface filled with the tile's background color.
        
        visible
            -- whether to render it using the faded fog of war color
               (default False)
        """
        s = pygame.Surface(size)
        
        if visible:
            bg_color = self.bg_color_v
        else:
            bg_color = self.bg_color_h
            
        s.fill(bg_color)
        return s;
    
    def create_sprites(self, size):
        """Returns a dictionary of all the surfaces needed to display the tile.
        
        The structure's a little too complicated so pay attention:
        
        return {
            the character surface 'char': {
                normal color 'v',
                fog of war color 'h'
            }
            the background color surface 'bg' :{
                normal color 'v'
                fog of war color 'h'
            }
        }
        
        Though background squares are generated even if the tile doesn't have a
        background color, the map display algorithm won't draw said background
        unless "solid_bg" is True.
        """
        return {
            'char': {
                'v':self.create_sprite(True),
                'h':self.create_sprite(False)
            },
            'bg': {
                'v':self.create_bg_surface(size, True),
                'h':self.create_bg_surface(size, True)
            }
        }


map_font = fonts.CourierNew(16)

# edit this list to add new types of terrain:
_tile_attrs = {'null':TileDescription(),
               'ground':TileDescription(map_font, '.', (110,110,110)),
               'wall':TileDescription(map_font, '', (255, 255, 255), True, (100, 100, 100)),
               'grass':TileDescription(map_font, ',', (0, 255, 0)),
               'water':TileDescription(map_font, '~', (0, 0, 255), True, (0, 0, 50))}
               

def get_tile_sprites(size):
    """Returns a dictionary of the results of calling create_sprites on everything in _tile_attrs
    
    Basically just returns _tile_attrs with each key pointing to a dictionary of the
    structure described in the create_sprites documentation instead of a TileDescription object.
    
    That explanation sucked so here is how I can get the fog of war character of the "grass"
    tile out of the results of this function:
    
    sprites['grass']['char']['h']
    
    Is there a less confusing way to manage this data? Fucking probably. Oh well.
    """
    sprites = {}
    for key in _tile_attrs.keys():
        sprites[key] = _tile_attrs[key].create_sprites(size)
    return sprites


def get_tile_desc(key):
    """An accessor for _tile_attrs"""
    return _tile_attrs[key]
    
