#!/usr/bin/env python
# encoding: utf-8
""" map_view.py - module containing classes for drawing the game map. """

import pygame
from pygame.locals import *
from . import settings
from .view import View
from .ordered_pair import x, y
from . import colors

class MapView(View):
    """This is a view that can show a portion of a GameMap object centered around the player."""

    def update(self, player_state, map_state):
        """Redraws the MapView with a given map and player state."""
        # clear all tiles
        self.clear()

        # determine what portion of the map is visible,
        # negative or invalid coordinates are handled later
        viewable_x_min = player_state.position[x] - (self.tile_count[x] // 2)
        viewable_x_max = viewable_x_min + self.tile_count[x]
        x_range = range(viewable_x_min, viewable_x_max)
        #print "x_range = " + str(x_range)

        viewable_y_min = player_state.position[y] - (self.tile_count[y] // 2)
        viewable_y_max = viewable_y_min + self.tile_count[y]
        y_range = range(viewable_y_min, viewable_y_max)
        #print "y_range = " + str(y_range)
        #print "viewable x_min = %d, x_max = %d, y_min = %d, y_max = %d" %\
        #   (viewable_x_min, viewable_x_max, viewable_y_min, viewable_y_max)

        # draw the map view
        k = 0 # these variables keep track of where we are on the screen
        l = 0
        for i in x_range:
            for j in y_range:
                #print "in draw loop: i = %d, j = %d, k = %d, l = %d" % (i, j, k, l)

                # skip drawing the tile if the coordinates fall outside the map
                if not (i < 0 or j < 0 or i >= map_state.width or j >= map_state.height):
                    tile = map_state.tiles[i][j]

                    # first draw the tile's background color
                    self.add_image(self.sprite_list[tile.tile_type]['bg']['v'],
                                   self.tile_mapping_points[k][l])

                    # if tile has an entity, draw that
                    e_top = tile.get_top_visible_entity()
                    if e_top is not None:
                        self.add_image_with_offset(
                            e_top.sprite,
                            self.tile_mapping_points[k][l],
                            self.draw_offset
                        )
                    else: # draw the tile
                        self.add_image_with_offset(
                            self.sprite_list[tile.tile_type]['char']['v'],\
                            self.tile_mapping_points[k][l],\
                            self.draw_offset
                        )

                    #if self.hilight_on and i == self.hilight_position[x] and j == self.hilight_position[y]:
                    #    self.add_image(self.hilight_img,
                    #        (self.tile_mapping_points[self.hilight_position[x]],
                    #         self.tile_mapping_points[self.hilight_position[y]]))
                l = l + 1
            l = 0
            k = k + 1


        #for i in range(self.tile_count[x]):
        #   for j in range(self.tile_count[y]):
        #       self.add_image_with_offset(self.testTile, self.tile_mapping_points[i][j], self.draw_offset)

    def _gen_tile_points(self):
        """Creates 2D array of screen coordinates of all tile positions,
        where (i, j) = (0, 0) is the bottom left corner
        - using these mapping points to place tiles allows us to assume the origin
        of the screen is the lower left corner when working on the tile level"""
        columns = []
        for i in range(self.tile_count[x]):
            column = []
            for j in range(self.tile_count[y]):
                tm = (self.tile_width * i, self.height - (self.tile_height * (j+1)))
                column.append(tm)
            columns.append(tuple(column))

        return tuple(columns)

    def __init__(self, screen, rect, background_color, tile_count, sprite_list=None):
        View.__init__(self, screen, rect, background_color)

        self.sprite_list = sprite_list
        self.tile_count = tile_count

        # calculate tile dimensions
        self.tile_width = int(self.width / tile_count[x])
        self.tile_height = int(self.height / tile_count[y])
        self.tile_size = (self.tile_width, self.tile_height)
        x_diff = self.width- (self.tile_width * tile_count[x])
        y_diff = self.height- (self.tile_height * tile_count[y])
        print("tile dimensions = %s, x_diff = %d, y_diff = %d" % \
         (str([self.tile_width, self.tile_height]), x_diff, y_diff))
        self.draw_offset = (settings.map_draw_offset[x] + (x_diff/2),
                            settings.map_draw_offset[y] + (y_diff/2))

        self.tile_mapping_points = self._gen_tile_points()

        self.hilight_img = pygame.Surface((self.tile_width, self.tile_height))
        self.hilight_img.fill(colors.yellow)
        self.hilight_img.set_alpha(110)
        self.hilight_on = True
        self.hilight_position = [10, 10]

        #self.testTile = pygame.Surface((self.tileWidth, self.tile_height))
        #self.testTile.fill(colors.blue)
        #over = pygame.Surface((self.tileWidth-2, self.tile_height-2))
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
