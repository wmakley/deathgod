"""This is sort of a global settings module for the engine.

The modus operandi here is "what variables would someone
making a game with this engine want to have easy access to?"

I don't really claim to have followed this, and some of the variables
in here should probably be in other "config" type files, so it's a WIP.

-William
"""

import os
import cfg_parser
from ordered_pair import *

debug = True;
player_name = "William"

# primary directories, relative to the modules directory
cfg_dir = "cfg"
data_dir = "data"
save_dir = "save"
monster_dir = "monsters"

# subdirectories
fonts_dir = os.path.join(data_dir, "fonts")

# config file paths
# HAHA what a joke why the fuck did I bother with this, a python module
# is perfectly good as a config file and a lot more flexible
primary_config = os.path.join(cfg_dir, "config.cfg")
user_config = os.path.join(cfg_dir, "autoexec.cfg")

graphics_mode = 0 # ASCII graphics! don't change this - no other modes are implemented

#fonts
monaco = os.path.join(fonts_dir, "Monaco.ttf")
courier_new = os.path.join(fonts_dir, "Courier_New.ttf")
courier_new_bold = os.path.join(fonts_dir, "Courier_New_Bold.ttf")
courier_new_italic = os.path.join(fonts_dir, "Courier_New_Italic.ttf")
courier_new_bold_italic = os.path.join(fonts_dir, "Courier_New_Bold_Italic.ttf")

font_normal = courier_new
font_bold = courier_new_bold
font_italic = courier_new_italic
font_bolditalic = courier_new_bold_italic

# player stuff
player_symbol = '@'
player_color = (255, 255, 100)

# =========================
# = DISPLAY CONFIGURATION =
# =========================

window_caption = "Death God"

# message view stuff
message_text_size = 16
message_max_chars = 55
message_normalFont = os.path.join(fonts_dir, "Courier_New.ttf")
message_hilightFont = os.path.join(fonts_dir, "Courier_New_Bold.ttf")
message_view_margin_bottom = 8
message_view_size = (800, message_text_size + message_view_margin_bottom)
message_view_position = (150, 0)
message_text_color = (255, 255, 255)
message_hilight_color = (100, 120, 255)
message_view_bg_color = (0, 50, 0)
message_log_size = 10

# map view stuff
map_font_size = 16
map_center_color = (20, 20, 20)
map_bg_color = map_center_color
#map_border_color = (0, 0, 60)
map_font_size = 16
map_view_size = (800, 600)
map_view_position = (150, message_view_size[y])
num_tiles_displayed = (40, 30)
map_draw_offset = (4, 0)

# status view stuff
status_view_font_size = 16
status_view_size = (150, 400)
status_view_position = (0, 0)
status_view_color = (60, 0, 10)

player_start = (10, 10)
world_dimensions = (30, 30)
screen_dimensions = (map_view_size[x] + status_view_size[x], message_view_size[y] + map_view_size[y])

if __name__ == "__main__":
    print __doc__