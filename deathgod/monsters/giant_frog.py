name = "Giant Frog"
visual_desc = "It is a large amphibian, approximately 4 feet in length. It has slimey green skin and moves erratically."
stats = "giant_frog_stat.txt"
char = 'F'
color = (0, 255, 0)

from .. import ai
ai_module = ai.default


from .. import entity
from .. import ascii_gfx
from .. import fonts
fstr = ascii_gfx.StyledString(char, fonts.normal, color)
sprite_idx = entity.add_sprite(fstr.create_sprite())

import os
stats_file = os.path.join("deathgod", "monsters", stats)
