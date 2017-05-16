#!/usr/bin/env python
# encoding: utf-8
"""
ascii_gfx.py defines functions and classes that are useful for creating textual graphics.

Public members:

StyledString

"""
from . import fonts

class StyledString:
    """A string with attributes such as font & color.

    This class combines three attributes:

    - a string, which is a standard python string
    - a color, which is an RGB tuple
    - a font, which is a reference to a pygame Font object
      (pygame.font.Font)

    The default font is fonts.normal, and the default color is black.
    The font parameter requires a pygame.font.Font object, and the
    color should be specified as an RGB tuple. By default, antialiasing
    is on, but another value may be specified.

    Public members:

    create_surface
    font
    set_font
    color
    set_color
    string
    set_string
    antialias
    set_antialias

    The following are simply shorter-to-type ways to call some of the
    Font object's methods, e.g.

    "my_f_string.font().get_height()" becomes "my_f_string.height()":

    height
    linesize
    ascent
    descent

    """

    def __init__(self, string="", font=fonts.normal, color=(0, 0, 0), antialias=True):
        """Initialize the StyledString.

        Arguments:

        string
            -- the string (default "")
        font
            -- the pygame Font object to use (default fonts.normal)
        color
            -- the color as an rgb tuple (default (0, 0, 0))
        antialias
            -- whether or not to antialias the string when rendering
               (default True)

        """
        self.__font = font
        self.__string = string
        self.__color = color
        self.__antialias = antialias

    def create_surface(self, color_key=None):
        """Returns a pygame.Surface of the rendered string.

        Arguments:

        color_key
            -- an RGB tuple: if specified, the surface is
               created with this as its color key instead of
               an alpha channel for transparency. (default None)

        """
        if color_key is not None:
            return self.__font.render(self.__string, self.__antialias, self.__color, color_key)
        else:
            return self.__font.render(self.__string, self.__antialias, self.__color)

    create_sprite = create_surface

    def get_font(self):
        """Returns the CharDescs's Font object."""
        return self.__font

    def set_font(self, font):
        """Changes the font to another pygame.font.Font object."""
        self.__font = font

    font = property(get_font, set_font)

    def get_color(self):
        """Returns the color as an RGB tuple."""
        return self.__color

    def set_color(self, color):
        """Changes the CharDesc's color to the specified RGB tuple."""
        self.__color = color

    color = property(get_color, set_color)

    def get_string(self):
        """Returns the string component."""
        return self.__string

    def set_string(self, string):
        """Sets the string value."""
        self.__string = string

    string = property(get_string, set_string)

    def set_antialias(self, val):
        """Sets whether the font will render with antialiasing."""
        self.__antialias = val

    def get_antialias(self):
        """Returns True if the string is antialiased, False if not."""
        return self.__antialias

    antalias = property(get_antialias, set_antialias)

    # the following properties are simply shortcuts to methods of the Font object

    @property
    def height(self):
        """(int) the height, in pixels, of the font

        From http://www.pygame.org/docs/ref/font.html:

        Return the height in pixels for a line of text with the font.
        When rendering multiple lines of text this is the recommended
        amount of space between lines.

        """
        return self.__font.get_height()


    @property
    def linesize(self):
        """(int) the linespace of the font.

        Pasted from http://www.pygame.org/docs/ref/font.html:

        When rendering multiple lines of text this is the recommended
        amount of space between lines.

        """
        return self.__font.get_linesize()


    @property
    def ascent(self):
        """Returns the ascent of the font as an integer.

        Pasted from http://www.pygame.org/docs/ref/font.html:

        Return the height in pixels for the font ascent.
        The ascent is the number of pixels from the font baseline to
        the top of the font.

        """
        return self.__font.get_ascent()


    @property
    def descent(self):
        """Returns the descent of the font as an integer

        Pasted from http://www.pygame.org/docs/ref/font.html:

        Return the height in pixels for the font descent.
        The descent is the number of pixels from the font
        baseline to the bottom of the font.

        """
        return self.__font.get_descent()


if __name__ == '__main__':
    print(__doc__)
    print("StyledString:\n\n", StyledString.__doc__)
