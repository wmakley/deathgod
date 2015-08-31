#!/usr/bin/env python
# encoding: utf-8

"""deathgod.py -- the entry point for Death God

That is to say, this starts the game.

Public Members:

main

"""

import sys, os
import pygame
from game import Game
# from modules import game


def main(argv=None):
    """This is Death God's main function."""
    
    # initialize the game
    import game
    game_obj = Game()
    
    # initialize psyco for SPEED
    # (actually it doesn't seem to do much)
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "failed to load psyco, hope your computer is fast" 
    
    # start the game loop
    game_obj.start()
    
    # exit
    pygame.quit()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))