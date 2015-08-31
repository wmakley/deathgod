from .tile import *
from .directions import *
from .ordered_pair import *

def get_adjacent_coords(pos):
    return [[pos[x], pos[y]+1],
            [pos[x], pos[y]-1],
            [pos[x]+1, pos[y]],
            [pos[x]+1, pos[y]+1],
            [pos[x]+1, pos[y]-1],
            [pos[x]-1, pos[y]],
            [pos[x]-1, pos[y]+1],
            [pos[x]-1, pos[y]-1]]
    
class GameMap:
    """Defines a map in Death God and everything that entails. Terrain, Entities, the works"""
    def __init__(self, size, player_position, generator_function):
        self.size = size
        self.width = size[x]
        self.height = size[y]
        #self.player_position = list(player_position)
        self.tiles = generator_function(size, player_position)
        
    def get_tile(self, position):
        """ Returns the Tile object reference at a given coordinate on the map """
        return self.tiles[position[x]][position[y]]
    
    def choose_open_tile(self):
        """Chooses a random tile from the map that's open.
        
        Returns the coordinates of the tile, and the tile itself.
        Does this by iterating through random tiles until it finds an
        open one, so not really a bulletproof algorithm at the moment.
        Perhaps a list of open tiles should be maintained.
        """
        import random
        found = False
        while not found:
            pos = [random.randint(0, self.width-1),
                   random.randint(0, self.height-1)]
            target_tile = self.get_tile(pos)
            if target_tile.character_can_enter():
                found = True
                
        return pos, target_tile
    
    def get_tile_slice(self, x_min, x_max, y_min, y_max):
        """I don't even know if this works."""
        result = self.tiles[x_min:x_max]
        for column in result:
            column = column[y_min:y_max]
        return result
    
    def move_entity(self, ent, dest):
        """ Locates an entity based on its stored position value and moves it to another point on the map
        - does not update the entity's internal data!!!"""
        
        # remove entity from its current tile
        self.tiles[ent.position[x]][ent.position[y]].remove_entity(ent)
        # append to destination tile
        self.tiles[dest[x]][dest[y]].add_entity(ent)
        
    def move_entity_to_tile(self, ent, dest_tile):
        """Moves the entity to a destination Tile object reference
        - does not update the entity's internal data!!!"""
        self.get_tile(ent.position).remove_entity(ent)
        dest_tile.add_entity(ent)
        
    def add_entity(self, ent):
        """ add an entity to the map """
        self.tiles[ent.position[x]][ent.position[y]].add_entity(ent)
        
    def remove_entity(self, ent):
        """ removes the entity from the map """
        self.tiles[ent.position[x]][ent.position[y]].remove_entity(ent)
        
    def set_player_tile(self, tile_coords):
        """BROKEN AND MAY BE POINTLESS DO NOT USE"""
        #self.tiles[ self.player_position[0] ][ self.player_position[1] ].has_player = False
        self.player_position = list(tile_coords)
        #self.tiles[ self.player_position[0] ][ self.player_position[1] ].has_player = True
        
    #def getPlayerTile(self):
    #   return self.tiles[ self.player_tile[0] ][ self.player_tile[1] ]
        
    def get_tile_in_direction(self, position, direction):
        """returns the tile directly adjacent in a given direction from a starting point"""
        border = { 'north': False, 'east': False, 'south': False, 'west': False }
        
        if position[0] >= self.width - 1:
            border['east'] = True
        if position[0] <= 0:
            border['west'] = True
        if position[1] >= self.height - 1:
            border['north'] = True
        if position[1] <= 0:
            border['south'] = True
            
        # north
        if direction == NORTH:
            if border['north']:
                return Tile(Tiles.NULL, False)
            else:
                return self.tiles[ position[0] ][ position[1] + 1 ]
        # north-east
        elif direction == NORTHEAST:
            if border['north'] and border['east']:
                return Tile(Tiles.NULL, False)
            else:
                return self.tiles[ position[0] + 1 ][ position[1] + 1 ]
        # east
        elif direction == EAST:
            if border['east']:
                return Tile(Tiles.NULL, False)
            else:
                return self.tiles[ position[0] + 1 ][ position[1] ]
        # south-east
        elif direction == SOUTHEAST:
            if border['south'] and border['east']:
                return Tile(Tiles.NULL, False)
            else:
                return (self.tiles[ position[0] + 1 ][ position[1] - 1 ])
        # south
        elif direction == SOUTH:
            if border['south']:
                return( Tile(Tiles.NULL, False) )
            else:
                return(self.tiles[ position[0] ][ position[1] - 1 ])
        # south-west
        elif direction == SOUTHWEST:
            if border['south'] and border['west']:
                return( Tile(Tiles.NULL, False) )
            else:
                return(self.tiles[ position[0] - 1 ][ position[1] - 1 ])
        # west
        elif direction == WEST:
            if border['west']:
                return( Tile(Tiles.NULL, False) )
            else:
                return(self.tiles[ position[0] - 1 ][ position[1] ])
        # north-west
        else: # direction == NORTHWEST:
            if border['north'] and border['west']:
                return( Tile(Tiles.NULL, False) )
            else:
                return(self.tiles[ position[0] - 1 ][ position[1] + 1 ])

            
    def get_coord_in_direction(self, position, direction):
        """Returns the coordinate of a tile in a given direction. (x,y)"""
        x_r = position[x]
        y_r = position[y]
        if direction == NORTH:
            y_r = y_r + 1
        elif direction == NORTHEAST:
            x_r = x_r + 1
            y_r = y_r + 1
        elif direction == EAST:
            x_r = x_r + 1
        elif direction == SOUTHEAST:
            x_r = x_r + 1
            y_r = y_r - 1
        elif direction == SOUTH:
            y_r = y_r - 1
        elif direction == SOUTHWEST:
            x_r = x_r - 1
            y_r = y_r - 1
        elif direction == WEST:
            x_r = x_r - 1
        else: # direction == NORTHWEST
            x_r = x_r - 1
            y_r = y_r + 1
            
        return (x_r, y_r)
        
if __name__ == "__main__":
    printGameMap__doc__