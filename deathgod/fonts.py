#!/usr/bin/env python
# encoding: utf-8
"""
fonts.py -- contains some pre-made font objects & related functions

Public Members:

pre-made fonts:

regular
bold
italic
bolditalic

create a new font:

Font
Bold
Italic
BoldItalic

font storage system:

get
add
"""

import pygame
from . import settings

pygame.font.init()

"""
Create a new font.
"""
def Font(font_file, size):
    return pygame.font.Font(font_file, size)

"""
Create a new 'regular' font.
"""
def Regular(size):
    return Font(settings.font_regular, size)

"""
Create a new 'bold' font.
"""
def Bold(size):
    return Font(settings.font_bold, size)

"""
Create a new 'italic' font.
"""
def Italic(size):
    Font(settings.font_italic, size)

"""
Create a new 'bold italic' font.
"""
def BoldItalic(size):
    Font(settings.font_bolditalic, size)

regular = Regular(settings.map_font_size)
bold = Bold(settings.map_font_size)
italic = Italic(settings.map_font_size)
bolditalic = BoldItalic(settings.map_font_size)


_fonts = {}

def get(key):
    return _fonts[key]

def add(key, font):
    _fonts[key] = font

add("regular", regular)
add("bold", bold)
add("italic", italic)
add("bolditalic", bolditalic)


if __name__ == "__main__":
    print(__doc__)
