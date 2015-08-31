#!/usr/bin/env python
# encoding: utf-8

# TODO revise variable naming style

import pygame
from pygame.locals import *
from . import settings
from .view import View
from . import tile
from .ordered_pair import *
from . import colors

class MapView(View):
    """This is a view that can show a portion of a GameMap object centered around the player."""

    def update(self, player_state, map_state):
        """Redraws the MapView with a given map and player state."""
        # clear all tiles
        self.clear()

        # determine what portion of the map is visible,
        # negative or invalid coordinates are handled later
        viewable_x_min = player_state.position[x] - (self.tileCount[x] // 2)
        viewable_x_max = viewable_x_min + self.tileCount[x]
        x_range = range(viewable_x_min, viewable_x_max)
        #print "x_range = " + str(x_range)

        viewable_y_min = player_state.position[y] - (self.tileCount[y] // 2)
        viewable_y_max = viewable_y_min + self.tileCount[y]
        y_range = range(viewable_y_min, viewable_y_max)
        #print "y_range = " + str(y_range)
        #print "viewable x_min = %d, x_max = %d, y_min = %d, y_max = %d" %\
        #   (viewable_x_min, viewable_x_max, viewable_y_min, viewable_y_max)

        # draw the map view
        k = 0 # these variables keep track of where we are on the screen
        l = 0
        # TODO: make this use slices of the map tiles instead of indexes
        for i in x_range:
            for j in y_range:
                #print "in draw loop: i = %d, j = %d, k = %d, l = %d" % (i, j, k, l)

                # skip drawing the tile if the coordinates fall outside the map
                if not (i < 0 or j < 0 or i >= map_state.width or j >= map_state.height):
                    tile = map_state.tiles[i][j]

                    # first draw the tile's background color
                    self.add_image(self.spriteList[tile.tile_type]['bg']['v'],
                                    self.tileMappingPoints[k][l])

                    # if tile has an entity, draw that
                    e_top = tile.get_top_visible_entity()
                    if e_top is not None:
                        self.add_image_with_offset(
                            e_top.sprite,
                            self.tileMappingPoints[k][l],
                            self.drawOffset
                        )
                    else: # draw the tile
                        self.add_image_with_offset(
                            self.spriteList[tile.tile_type]['char']['v'],\
                            self.tileMappingPoints[k][l],\
                            self.drawOffset
                        )

                    #if self.hilight_on and i == self.hilight_position[x] and j == self.hilight_position[y]:
                    #    self.add_image(self.hilight_img,
                    #        (self.tileMappingPoints[self.hilight_position[x]],
                    #         self.tileMappingPoints[self.hilight_position[y]]))
                l = l + 1
            l = 0
            k = k + 1


        #for i in range(self.tileCount[x]):
        #   for j in range(self.tileCount[y]):
        #       self.add_image_with_offset(self.testTile, self.tileMappingPoints[i][j], self.drawOffset)

    def _gen_tile_points(self):
        """Creates 2D array of screen coordinates of all tile positions,
        where (i, j) = (0, 0) is the bottom left corner
        - using these mapping points to place tiles allows us to assume the origin
        of the screen is the lower left corner when working on the tile level"""
        columns = []
        for i in range(self.tileCount[x]):
            column = []
            for j in range(self.tileCount[y]):
                tm = ( self.tileWidth * i, self.height - (self.tileHeight * (j+1)) )
                column.append(tm)
            columns.append( tuple(column) )

        return ( tuple(columns) )

    def __init__(self, screen, rect, background_color, tileCount, spriteList=None):
        View.__init__(self, screen, rect, background_color)

        self.spriteList = spriteList
        self.tileCount = tileCount

        # calculate tile dimensions
        self.tileWidth = int(self.width / tileCount[x])
        self.tileHeight = int(self.height / tileCount[y])
        self.tile_size = (self.tileWidth, self.tileHeight)
        x_diff = self.width- (self.tileWidth * tileCount[x])
        y_diff = self.height- (self.tileHeight * tileCount[y])
        print("tile dimensions = %s, x_diff = %d, y_diff = %d" % \
         (str([self.tileWidth, self.tileHeight]), x_diff, y_diff))
        self.drawOffset = (settings.map_draw_offset[x] + (x_diff/2),
         settings.map_draw_offset[y] + (y_diff/2))

        self.tileMappingPoints = self._gen_tile_points()

        self.hilight_img = pygame.Surface((self.tileWidth, self.tileHeight))
        self.hilight_img.fill(colors.yellow)
        self.hilight_img.set_alpha(110)
        self.hilight_on = True
        self.hilight_position = [10, 10]

        #self.testTile = pygame.Surface((self.tileWidth, self.tileHeight))
        #self.testTile.fill(colors.blue)
        #over = pygame.Surface((self.tileWidth-2, self.tileHeight-2))
        #over.fill(colors.black)
        #self.testTile.blit(over, (1, 1))

        #import text_views
        #import fonts
        #self.add_view( text_views.StringView(self, (100, 100),
        #    "child of MapView", fonts.Monaco(10), colors.blue, colors.yellow) )
        #
        #self.add_view( text_views.StringView(self, (140, 140),
        #    "child of MapView", fonts.CourierNewItalic(13), colors.black, colors.white) )


if __name__ == "__main__":
    print(MapView.__doc__)
