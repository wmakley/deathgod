"""This module defines functions for possible actions an agent can perform."""

from .. import game_map
from ..ordered_pair import x, y


def attack_player(game, agent):
    """have and agent attack the player"""
    game.combat(agent, game.get_player())


def move_towards_player(game, ch):
    """Have an agent try to move towards the player.

    This is basically a very simple uninformed search.

    If adjacent the player, this calls attack_player instead.

    I think for purposes of balancing the actual game I will
    have to make it so monsters don't usually move diagonally
    because it's just a huge pain for the player to deal with
    and kind of counterintuitive.
    """
    ch_pos = ch.position
    pl_pos = game.get_player().position

    # get possible positions to move to
    possibilities = get_move_possibilities(game, ch)

    # if none are left just do nothing
    if not possibilities:
        wait(game, ch)
        return

    # get the costs of all the possible moves
    costs = []
    for pos in possibilities:
        costs.append(cost(ch_pos, pos, pl_pos))

    # find the lowest one
    lowest = 0
    for i in range(1, len(costs)):
        if costs[i] < costs[lowest]:
            lowest = i

    move = possibilities[lowest]
    # if the move is the player, attack instead of moving
    if move == pl_pos:
        attack_player(game, ch)
        #print "best move towards player is the player"
    else:
        result = game.move_entity(ch, move)
        if result is not True:
            print("wtf")


def run_away(game, ch):
    """This is a copy paste of move_towards with one test flipped. lazy much?"""
    ch_pos = ch.position
    pl_pos = game.get_player().position

    # get possible positions to move to
    possibilities = get_move_possibilities(game, ch)

    # if none are left just do nothing
    if not possibilities:
        wait(game, ch)
        return

    # get the costs of all the possible moves
    costs = []
    for pos in possibilities:
        costs.append(cost(ch_pos, pos, pl_pos))

    # find the HIGHEST one
    highest = 0
    for i in range(1, len(costs)):
        if costs[i] > costs[highest]:
            highest = i

    move = possibilities[highest]
    # if the move is the player, attack instead of moving
    if costs[highest] == -3:
        attack_player(game, ch)
    else:
        result = game.move_entity(ch, move)
        if result is not True:
            print("wtf")


def wait(game, agent):
    """Do nothing."""
    pass


members = [
    attack_player,
    move_towards_player,
    run_away,
    wait
]


def get_move_possibilities(game, ch):
    """Get all the adjacent tiles that an agent could move into."""
    ch_pos = ch.position
    pl_pos = game.get_player().position
    current_map = game.get_map()

    # get possible positions to move to
    possibilities = game_map.get_adjacent_coords(ch_pos)
    # remove impassable ones
    possibilities_cpy = list(possibilities)
    for pos in possibilities_cpy:
        target_tile = current_map.get_tile(pos)
        if not target_tile.character_can_enter(ch) and pos != pl_pos:
            possibilities.remove(pos)

    return possibilities


def cost(start, move, end):
    """Return values:

    1 if move goes farther from target
    0 if move accomplishes nothing or increases one distance while decreasing the other
    -1 if move reduces either x or y distance WITHOUT increasing the other (to avoid diagonals)
    -2 if move reduces both x and y distance
    -3 if move is target
    """
    if move == end:
        return -3

    d_start = distance(start, end)
    d_move = distance(move, end)

    if d_start == d_move:
        return 0

    if d_move[x] < d_start[x]:
        x_dist_reduced = True
    else:
        x_dist_reduced = False

    if d_move[y] < d_start[y]:
        y_dist_reduced = True
    else:
        y_dist_reduced = False

    if x_dist_reduced and y_dist_reduced:
        return -2
    elif (x_dist_reduced and not y_dist_reduced) or (y_dist_reduced and not x_dist_reduced):
        return -1
    else:
        return 0


def distance(p1, p2):
    """Get the distance between two points on the grid."""
    dist = [p1[x] - p2[x], p1[y] - p2[y]]

    if dist[x] < 0:
        dist[x] = dist[x] * -1
    if dist[y] < 0:
        dist[y] = dist[y] * -1

    return dist
