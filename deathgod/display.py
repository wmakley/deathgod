#!/usr/bin/env python
# encoding: utf-8
"""
display.py is the portion of Death God that manages the screen.

by William Makley

"""
import pygame
from pygame.locals import Rect
from . import colors
from . import settings
from . import fonts
from .map_view import MapView
from . import message
from .status_view import StatusView
from . import event
from . import tile
from .view import View

(ASCII, TILES) = list(range(2))

class Screen(View):
    """Wraps the pygame screen in a View."""

    def __init__(self):
        self.__window = pygame.display.set_mode(settings.screen_dimensions)
        pygame.display.set_caption(settings.window_caption)
        screen = pygame.display.get_surface()
        View.__init__(self, None, Rect(0, 0, screen.get_width(), screen.get_height()), colors.black, screen)
        event.add_handler(self.handle_display_needs_update, event.DisplayNeedsUpdate)

    @property
    def window(self):
        return self.__window

    def refresh(self):
        pygame.display.flip()

    def paint(self):
        View.paint(self)
        self.refresh()

    def handle_display_needs_update(self, e):
        self.paint()


screen = Screen()

class Display(View):
    """The display class.

    It is a special type of View that paints directly to the screen
    instead of a parent view.
    """
    def __init__(self, player_object, map_object):
        self.player_object = player_object
        self.map_object = map_object

        View.__init__(self,
                      parent = screen,
                      rect = Rect(0, 0, screen.width, screen.height),
                      clear_color = colors.black)
        # whoops, so much for the surface made by View.__init__

        # set up event handlers
        event.add_handler(
            self.handle_game_state_changed,
            event.GameStateChanged
        )

        self.set_clear_on_paint(True)

        self.map_view = MapView(self,
            Rect(settings.map_view_position, settings.map_view_size),
            settings.map_center_color,
            settings.num_tiles_displayed
        )

        self.map_view.sprite_list = tile.get_tile_sprites(self.map_view.tile_size)

        self.message_view = message.MessageView(self,
            Rect(settings.message_view_position, settings.message_view_size),
            settings.message_view_bg_color,
            fonts.CourierNew(settings.message_text_size)
        )

        self.status_view = StatusView(self,
            Rect(settings.status_view_position, settings.status_view_size),
            settings.status_view_color,
            pygame.font.Font(settings.font_normal, settings.status_view_font_size),
            pygame.font.Font(settings.font_normal, settings.status_view_font_size),
            colors.green, colors.yellow
        )


        # self.t_area = text_views.WrappedTextArea(
        #     parent = self,
        #     rect = Rect(100, 100, 200, 200),
        #     background = colors.black,
        #     font = fonts.normal,
        #     padding = (10,10,10,10)
        # )
        # self.add_view(self.t_area)
        #
        # self.t_area.add_string(
        #     string = "The quick brown fox jumped over the lazy dog.",
        #     indent = 4,
        #     color = colors.white,
        #     background = (50, 50, 50)
        # )
        #
        # self.t_area.newline(2)
        #
        # self.t_area.add_string("Also I am really smart.",
        #    0, colors.blue)
        #
        # self.t_area.add_string("The quick brown fox jumped over the lazy dog\n and there was much rejoicing.")

        # event.DisplayInited().dispatch()
        from .ui.menu import Menu
        test_menu = Menu(self)

    # new
    def update(self):
        self.map_view.update(self.player_object, self.map_object)
        self.status_view.update(self.player_object)
        self.parent.paint()

    #old
    def handle_game_state_changed(self, e):
        self.map_view.update(e.player_state, e.map_state)
        self.status_view.update(e.player_state)
        self.parent.paint()




if __name__ == "__main__":
    print(__doc__)
