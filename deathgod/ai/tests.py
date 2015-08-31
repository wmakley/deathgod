"""
tests.py

by William Makley

Contains a bunch of tests the genetic algorithm can use
to assemble a decision tree AI
"""

from .. import game_map

from ..ordered_pair import *

def full_life(game, ch):
    if ch.stats.hp == ch.stats.max_hp:
        return True
    else:
        return False

def less_than_half_life(game, ch):
    """(bool) Returns true if ch has less than half life."""
    if ch.stats.hp < ch.stats.max_hp / 2:
        return True

def more_than_half_life(game, ch):
    """Redundant really"""
    if less_than_half_life(game, ch) is True:
        return False
    else:
        return True

def about_to_die(game, ch, threshold=5):
    if ch.stats.hp > 0 and ch.stats.hp < threshold:
        return True
    else:
        return False

def player_about_to_die(game, ch, threshold=5):
    if game.player.stats.hp > 0 and game.player.stats.hp < threshold:
        return True
    else:
        return False

def can_kill_player(game, ch):
    if ch.offense - game.player.defense >= game.player.stats.hp:
        return True
    else:
        return False

def friends_nearby(game, ch, threshold=3, radius=5):
    entities = game.get_nearby_entities(ch, radius)
    count = 0

    for e in entities:
        if e.type == ch.type:
            count = count + 1

    if count >= threshold:
        return True
    else:
        return False


def adjacent_to_player(game, ch):
    pl_pos = game.player.position
    ch_pos = ch.position

    adj_coords = game_map.get_adjacent_coords(ch_pos)
    for c in adj_coords:
        if c == pl_pos:
            return True

    return False


members = [full_life,
           less_than_half_life,
           more_than_half_life,
           about_to_die,
           player_about_to_die,
           can_kill_player,
           friends_nearby,
           adjacent_to_player]
