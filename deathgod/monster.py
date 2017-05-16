"""Includes Monster; the base class for monsters.
"""
from .character import Character

class Monster(Character):
    """The class defines a monster in the game

    It is basically like any other character, but if the player
    interacts with it (attempts to move onto its square) combat
    ensues.
    """
    def __init__(self, game, position, config):
        Character.__init__(self, game, position, config)
        self.type = "Monster"


    def interact(self, antagonist):
        self.game.combat(antagonist, self)


if __name__ == "__main__":
    print(__doc__)
