"""
dg_input.py - input-oriented classes

Public Members:

wait_for_event
InputManager
Prompt

TODO finish Prompt class

"""

import pygame
from pygame.locals import *
from .event import *
from . import directions


def parse_keydown(key, game):
    """Sends calls appropriate methods in game depending on what key was pressed.

    Arguments:

    key
        -- the key that was pressed (as defined in pygame.locals)
    game
        -- the game object to run the appropriate action on
    """
    if key == K_ESCAPE or key == K_q:
        game.done = True
    # north
    elif key == K_UP or key == K_KP8:
        game.move_player_in_direction(directions.NORTH)
        #PlayerMoved(directions.NORTH).dispatch()
    # northeast
    elif key == K_QUOTE or key == K_KP9:
        game.move_player_in_direction(directions.NORTHEAST)
        # PlayerMoved(directions.NORTHEAST).dispatch()
    # east
    elif key == K_RIGHT or key == K_KP6:
        game.move_player_in_direction(directions.EAST)
        # PlayerMoved(directions.EAST).dispatch()
    # southeast
    elif key == K_SLASH or key == K_KP3:
        game.move_player_in_direction(directions.SOUTHEAST)
        # PlayerMoved(directions.SOUTHEAST).dispatch()
    # south
    elif key == K_DOWN or key == K_KP2:
        game.move_player_in_direction(directions.SOUTH)
        # PlayerMoved(directions.SOUTH).dispatch()
    # southwest
    elif key == K_PERIOD or key == K_KP1:
        game.move_player_in_direction(directions.SOUTHWEST)
        # PlayerMoved(directions.SOUTHWEST).dispatch()
    # west
    elif key == K_LEFT or key == K_KP4:
        game.move_player_in_direction(directions.WEST)
        # PlayerMoved(directions.WEST).dispatch()
    # northwest
    elif key == K_SEMICOLON or key == K_KP7:
        game.move_player_in_direction(directions.NORTHWEST)
        # PlayerMoved(directions.NORTHWEST).dispatch()
    else:
        KeyPressed().dispatch()


def wait_for_event(event_type=None):
    """Waits for a pygame event and returns it.

    Arguments:

    event_type
        -- You may specify what specific type of event you want to wait
           for. All others will be ignored until an event of this type
           is received. (default None)
    """
    found = False
    while not found:
        evt = pygame.event.wait()
        if event_type is not None:
            if evt.type == event_type:
                found = True
        else:
            found = True

    return evt


class Prompt:
    """Displays a message, waits for input, handles input.

    Takes a bit of setup, so should primarily be sub-classed.
    """

    def __init__(self, msg, actions={}):
        self._prompt_msg = msg
        self._actions = actions

    def run_prompt(self):
        self._prompt_msg.dispatch()
        evt = wait_for_event(KEYDOWN)
        func = self._actions[evt.key]
        func()



if __name__ == '__main__':
    print(__doc__)
