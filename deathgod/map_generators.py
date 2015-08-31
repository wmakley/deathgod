# TODO make this be part of a package where each module has a standard generate function

from .tile import *

def test_generator(dimensions, player_position):
    width = dimensions[0]
    height = dimensions[1]
    
    columns = []
    for i in range(width):
        column = []
        for j in range (height):
            if i == 0 or j == 0 or i == (width-1) or j == (height-1) \
             or (i == 6 and j == 7) or (i == 7 and j == 6)\
             or ((5 <= i <= 10) and (21 <= j <= 25))\
             or (i == 25 and (0 < j < 10))\
             or (i == 23 and (0 < j < 8))\
             or ((i-4 == j) and (5 < j < 15)) or ((i-6 == j) and (5 < j < 15)):
                tile = Tile('wall', False, 3)
            elif i == j or (i-1) == (j) or (i-1) == (j+1):
                tile = Tile('water', True)
            else:
                tile = Tile('ground', True)
                
            """if (i, j) == tuple(player_position):
                print "in map gen: player at %d, %d" % (i, j)
                tile.has_player = True"""
            column.append(tile)
        columns.append(column)
    
    return columns
