from character import *
#import event
import fonts
import settings
from ascii_gfx import StyledString
import entity
import message

player_fstr = StyledString(settings.player_symbol, fonts.normal, settings.player_color)

class PConfig:
    name = settings.player_name
    visual_desc = "He is a totally awesome guy."
    from ai import default
    ai_module = None
    sprite_idx = entity.add_sprite(player_fstr.create_surface())
    stats_file = "player_stats.txt"


class Player(Character):
    """Contains all data about the player in Death God."""
    def __init__(self, game, position):
        Character.__init__(self, game, position, PConfig)
        message.Message.add_handler(self.handle_message)
        self.type = "Player"
        self.messageLog = []
    
    
    def show_stats(self):
        """Displays the player's Character sheet."""
        pass
    
    
    def handle_message(self, e):
        self.messageLog.append(e)
        if len(self.messageLog) > 100:
            self.messageLog.pop(0)


if __name__ == "__main__":
    print Player.__doc__
