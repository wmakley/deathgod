#!/usr/bin/env python
# encoding: utf-8
"""
text_views.py - some classes for putting text into a View

Created by William Makley on 2008-04-08.
Totally free to use knock yourself out.
"""

from . import colors
from . import fonts
from .view import View
from .ascii_gfx import StyledString
from pygame.locals import *
from .ordered_pair import *

# TODO finish ListView


class StringView(View):
    """Encapsulates a StyledString in a View for automatic drawing."""

    def __init__(self, parent, string, position=(0, 0), font=fonts.regular,
                 color=colors.white, background=colors.black, antialias=True):
        """Args:

        parent
            -- the parent of the view
        string
            -- the string
        position
            -- the position of the view (defalt (0,0))
        font
            -- the pygame Font to use (default fonts.regular)
        color
            -- the text color (default colors.white)
        background
            -- the background color (default colors.black)
        antialias
            -- whether to antialias the text (default True)
        """
        self.styled_string = StyledString(string, font, color, antialias)
        img = self.styled_string.create_surface(background)
        View.__init__(self, parent=parent, rect=Rect(position, img.get_size()),
                      clear_color=background, surface=img)


class TextArea(View):
    """Just a view that has methods to automatically put text."""

    def __init__(self, parent, rect, background):
        """Constructor.

        Args:
            parent
                -- the containing view
            rect
                -- the view's size & position
            background
                -- the background color (default colors.black)
        """
        View.__init__(self, parent, rect, background)

    def put_string(self, string, position=(0, 0),
                   color=colors.white, background=None, fonts=fonts.regular):
        """Add a string with colors somewhere in the TextArea.

        Args:

        string
            -- the string
        position
            -- where to add the string (default (0,0))
        color
            -- the color to use (default colors.white)
        background
            -- the background color of the string, uses the parent's
               background color if None (default None)
        font
            -- the pygame Font to use (default fonts.regular)
        """
        if background is None:
            background = self.background
        str_v = StringView(self, position, string, font, color, background, antialias)
        self.add_view(str_v)

(_TOP, _RIGHT, _BOTTOM, _LEFT) = list(range(4))

class WrappedTextArea(View):
    """
    Shows a bunch of text in one font with variable color.

    Has methods to add text as if it were being typed,
    automatically handles wrapping.

    Public Members:

    add_string
    font
    newline (aliases: add_newline, add_linebreak)
    max_lines
    """

    def __init__(self, parent, rect, background=colors.black, font=fonts.regular, padding=[0,0,0,0]):
        """Constructor.

        Args:
            parent
                -- the containing view
            rect
                -- the view's size & position
            background
                -- the background color (default colors.black)
            font
                -- the font to use (default fonts.regular)
            padding
                -- the view's padding, syntax is the same as
                   css: top,right,bottom,left (default [0,0,0,0])
        """
        View.__init__(self, parent, rect, background)
        self.__font = font
        self.__padding = padding
        self.__line_space = self.__font.get_linesize()
        self.__line_count = 0
        self.__max_lines = int((self.height - padding[_TOP] - padding[_BOTTOM]) / self.__line_space)

        # points to a line position in the view
        # text is added on a line-by-line basis
        self.__cursor = [padding[_LEFT], padding[_TOP]]


    def add_string(self, string, indent=0, color=colors.white, background=None, antialias=True):
        """Adds a string to the view with automatic positioning & wrap.

        Assumed to be a text block, which will not be displayed inline
        with surrounding text. It will remove multiple spaces, sorry.

        Args:

        string
            -- the string to add
        indent
            -- how much to indent the resultant paragraph in spaces
               (default 0)
        color
            -- the color the of the string (default colors.white)
        background
            -- the background color of the string (will be the same as
               the view if none is specified) (default None)
        antialias
            -- whether to antialias the string (default True)
        """
        if background is None:
            background = self.background

        #position = (self.__cursor[x] + self.__font.size(" " * indent), self.__cursor[y])
        self.__cursor[x] = self.__cursor[x] + self.__font.size(" " * indent)[x]
        max_line_width = self.width - self.__cursor[x] - self.__padding[_RIGHT]

        words = string.split()
        #print "words = %s" % str(words)
        lines = []

        # separate words into lines
        first = True
        line = ""
        i = 0
        for word in words:
            if self.__line_count == self.__max_lines:
                print("in add_string: overflow on \'%s %s\'" % (line, word))
                break;

            # build the line
            #print "word = %s" % word
            if first is not True:
                word = " " + word

            if self.__font.size(line + word)[x] <= max_line_width or first is True:
                line = line + word
                #print "appended %s, line = %s" % (word, line)
                first = False
            else:
                lines.append(line)
                self.__line_count = self.__line_count + 1
                line = word[1:]
                #print "reset: line = %s, lines = %s" % (line, str(lines))

            # if this is the last word, end the line
            if i == len(words) - 1:
                lines.append(line)
                self.__line_count = self.__line_count + 1
                #print "hit end, lines = %s" % str(lines)

            i = i + 1


        for line in lines:
            str_v = StringView(self,
                string = line,
                position = (self.__cursor[x], self.__cursor[y]),
                font = self.__font,
                color = color,
                background = background,
                antialias = antialias
            )
            self.add_view(str_v)
            self.newline()

        self.reset_cursor()


    def newline(self, count=1):
        """Inserts [count] number of blank lines."""
        i = 0
        while i < count:
            self.__cursor[y] = self.__cursor[y] + self.__line_space
            i = i + 1

    add_newline = newline
    add_linebreak = newline

    def reset_cursor(self):
        """Puts the cursor back to base indent level."""
        self.__cursor[x] = self.__padding[_LEFT]


    @property
    def max_lines(self):
        """(int) returns maximum number of lines the view can display"""
        return self.__max_lines


    @property
    def line_count(self):
        """(int) returns the number of lines of text currently in the view"""
        return self.__line_count


    def get_font(self):
        """(Font) Returns the View's font."""
        return self.__font

    font = property(get_font)


class ListView(View):
    def __init__(self, parent, rect, items=[], background=colors.black):
        View.__init__(self, parent, rect, background)
        self.__items = items



if __name__ == '__main__':
    print(__doc__)
