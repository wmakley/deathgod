"""
view.py -- defines a View class which is an area on a pygame surface.

public members:

View

"""

from . import settings
from .ordered_pair import *
from . import colors
from . import fonts
import pygame
from pygame.sprite import *
from pygame.locals import *

class View(Sprite):
    
    """This class defines an area on a pygame surface. 
    
    It basically has a pygame.Surface that can be blitted to, and then
    when the paint method is invoked it blits this surface onto the
    screen.
    
    Public members:
    
    clear
    fill
    clear_color
    background
    paint
    add_image
    add_image_with_offset
    add_text
    rect
    position
    width
    height
    parent
    add_view
    remove_view
    
    """
    
    def __init__(self, parent, rect, clear_color=colors.black, surface=None):
        """Initializes the View.
        
        Arguments:
        
        parent
            - the containing view
        rect
            - a pygame Rect defining the position and size of the view
              if None, the view will be completely invisible, and all its
              children will be painted onto this view's parent view
        clear_color
            - an RGB tuple defining the base background color of the view
        surface
            - a reference to a pygame surface object for the view to use to draw on
              if None, a new surface will be created. (default None)
        
        """
        Sprite.__init__(self)
        self.__views = []
        self.__parent = parent
        if self.__parent is not None:
            self.__parent.add_view(self)
        
        self.__clear_color = clear_color
        self.__clear_on_paint = False
        
        if rect is not None:
            self.set_rect(rect)
            if surface is None:
                self.__surface = pygame.Surface(self.__rect.size)
                self.__surface.fill(self.__clear_color)
            else:
                self.__surface = surface
            
    def get_surface(self):
        return self.__surface
        
    #def set_surface(self, surface):
    #    self.__surface = surface
    @property   
    def surface(self):
        return self.__surface
        
    def clear(self):
        """Fills the View with its clear color"""
        self.__surface.fill(self.__clear_color)
        
    def fill(self, color):
        """Fills the View with a specified color (takes RGB tuple)."""
        self.__surface.fill(color)
        
    def set_clear_color(self, color):
        """Changes the views clear color (takes RGB tuple)"""
        self.__clear_color = color
        
    def get_clear_color(self):
        """Returns the clear color as an RGB tuple."""
        return self.__clear_color
        
    def set_clear_on_paint(self, val):
        self.__clear_on_paint = val
        
    def get_clear_on_paint(self):
        return self.__clear_on_paint
        
    clear_on_paint = property(get_clear_on_paint, set_clear_on_paint)
    
    background = property(get_clear_color, set_clear_color)
    clear_color = property(get_clear_color, set_clear_color)
         
    def paint(self):
        """Draws the current content of view's surface to the parent."""
        # paint all sub-views
        if self.__clear_on_paint == True:
            self.clear()
            
        for v in self.__views:
            v.paint()
        # paint self
        if self.__parent is not None:
            self.__parent.add_image(self.__surface, self.__position)
        
    def add_image(self, image, position=(0, 0)):
        """Blits an image (a pygame surface) to a given position in the view.
        
        Arguments:
        
        image -- the pygame.Surface
        position -- where to add the image, relative to the upper-left
                    corner of the view (default (0,0))
                    
        """
        self.__surface.blit(image, position)
        
    def add_image_with_offset(self, image, position=(0, 0), offset=(0, 0)):
        """An alternative to addImage that takes an additional offset argument.
        
        The offset is simply added to the position. This can be useful
        to correct for some annoyances.
        
        Arguments:
        
        image -- the pygame.Surface
        position -- where to add the image, relative to the upper-left
                    corner of the view (default (0, 0))
        offset -- an tuple added to position when blitting
                  the image (default (0, 0)
        
        """
        self.add_image(image, (position[x] + offset[x], position[y] + offset[y]))
        
    def add_text(self, text, font=fonts.normal, color=(0, 0, 0), antialias=True,
                position=(0, 0), offset=(0, 0)):
        """Takes a string with attributes, renders it, and blits it to the View.
        
        Arguments:
        
        text -- the string to use
        font -- the pygame.font.Font object to use (default fonts.normal)
        color -- the color to render the text in (default (0, 0, 0))
        antialias -- whether or not to antialias the text when rendering
        position -- where to add the text, relative to the upper-left
                    corner of the view (default (0, 0))
        offset -- a tuple added to position when blitting the text
                  (default (0, 0))
        
        """
        img = font.render(text, antialias, color, self.background)
        self.add_image_with_offset(img, position, offset)
        
    def add_view(self, v):
        """Add a View."""
        if self.__rect is None:
            v.set_parent(self.__parent)
        self.__views.append(v)
        
    def remove_view(self, v):
        """Remove a View."""
        self.__views.remove(v)
        
    def set_rect(self, rect):
        """Changes the View's rect.
        
        Avoid using this to change the size of a View, since there are
        no provisions in the engine currently for resizing Views.
        """
        assert(rect is not None)
        self.__rect = rect
        self.__position = rect.topleft
        self.__width = rect.width
        self.__height = rect.height
        
    def get_rect(self):
        """Returns the View's rect."""
        return self.__rect
        
    rect = property(get_rect, set_rect)
        
    def get_parent(self):
        """Returns the View's parent View."""
        return self.__parent
    
    def set_parent(self, parent):
        self.__parent = parent
        
    parent = property(get_parent, set_parent)
    
    @property
    def position(self):
        """Returns the view's position."""
        return self.__position
    
    @property
    def width(self):
        """Returns the width, in pixels, of the View."""
        return self.__width
      
    @property 
    def height(self):
        """Returns the height, in pixels, of the View."""
        return self.__height
    

class ProgressBar(View):
    def __init__(self, parent, position, width=10, min_val=0, max_val=9, initial_val=0):
        rect = Rect(position, (font.get_height(), font.size("|" + ("*" * width) + "|")))
        View.__init__(self, parent, rect)
        self.__font = fonts.normal
        self.__width = width
        self.__min = min_val
        self.__max = max_val
        self.__value = initial_val
    
    def set_value(self, value):
        self.__value = value
    
    def set_min(self, value):
        self.__min = value
    
    def set_max(self, value):
        self.__max = value
    
    def paint(self):
        View.paint(self)


if __name__ == "__main__":
    print(__doc__, View.__doc__)
