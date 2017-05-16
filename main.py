#!/usr/bin/env python3
# encoding: utf-8

"""deathgod.py -- the entry point for Death God

That is to say, this starts the game.

Public Members:

main

"""

import sys
import pygame
from deathgod.game import Game

def main():
    """This is Death God's main function."""

    # create a new game object
    game_obj = Game()
    # start the game loop
    game_obj.start()

    # exit
    pygame.quit()
    return 0


if __name__ == '__main__':
    sys.exit(main())
