#!/usr/bin/env python
# encoding: utf-8
"""

fonts.py -- contains some pre-made font objects & related functions

Public Members:

pre-made fonts:

monaco
courier_new
normal
bold
italic
bolditalic

font generators:

Font
Monaco
CourierNew
CourierNewBold
CourierNewItalic
CourierNewBoldItalic

font storage system:

get
add

"""

from . import settings
import pygame
pygame.font.init()

monaco = pygame.font.Font(settings.monaco, settings.map_font_size)
courier_new = pygame.font.Font(settings.courier_new, settings.map_font_size)

normal = pygame.font.Font(settings.font_normal, settings.map_font_size)
bold = pygame.font.Font(settings.font_bold, settings.map_font_size)
italic = pygame.font.Font(settings.font_italic, settings.map_font_size)
bolditalic = pygame.font.Font(settings.font_bolditalic, settings.map_font_size)

def Font(font_file, size):
    return pygame.font.Font(font_file, size)

def Monaco(size):
    return Font(settings.monaco, size)
    
def CourierNew(size):
    return Font(settings.courier_new, size)
    
def CourierNewBold(size):
    return Font(settings.courier_new_bold, size)
    
def CourierNewItalic(size):
    return Font(settings.courier_new_italic, size)

def CourierNewBoldItalic(size):
    return Font(settings.courier_new_bold_italic, size)
    

_fonts = {}

def get(key):
    return _fonts[key]

def add(key, font):
    _fonts[key] = font

add("monaco", monaco)
add("courier_new", courier_new)
add("normal", normal)
add("bold", bold)
add("italic", italic)
add("bolditalic", bolditalic)

    
if __name__ == "__main__":
    print(__doc__)