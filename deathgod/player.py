from .character import *
#import event
from . import fonts
from . import settings
from .ascii_gfx import StyledString
from . import entity
from . import message

player_fstr = StyledString(settings.player_symbol, fonts.regular, settings.player_color)

class PConfig:
    name = settings.player_name
    visual_desc = "He is a totally awesome guy."
    from .ai import default
    ai_module = None
    sprite_idx = entity.add_sprite(player_fstr.create_surface())
    stats_file = "deathgod/player_stats.txt"


class Player(Character):
    """Contains all data about the player in Death God."""
    def __init__(self, game, position):
        Character.__init__(self, game, position, PConfig)
        message.Message.add_handler(self.handle_message)
        self.type = "Player"
        self.message_log = []


    def show_stats(self):
        """Displays the player's Character sheet."""
        pass


    def handle_message(self, event):
        """Append message events to the log."""
        self.message_log.append(event)
        if len(self.message_log) > 100:
            self.message_log.pop(0)


if __name__ == "__main__":
    print(Player.__doc__)
