"""Includes base class and events for all characters in the game world
"""
import random
from . import cfg_parser
from . import ascii_gfx
from . import entity
from . import fonts
from .entity import Entity
from .event import Event

random.seed()
default_character_fstr = ascii_gfx.StyledString('C', fonts.normal, (180, 180, 0), True)
default_sprite_idx = entity.add_sprite(default_character_fstr.create_surface())

class CharacterDeath(Event):
    """Dispatched when a Character dies"""
    handlers = []
    def __init__(self, ch):
        Event.__init__(self)
        self.ch = ch


class Character(Entity):
    """A character is anything in the game that can engage in combat.

    No character may occupy the same tile as another character.
    Characters are initialized via a config object due to the large
    number of attributes and to facilitate creating "types"
    of Characters. The config object can simply be a module, but
    a class as seen in player.py is a good way to go if you want to
    make a hard-coded sub-class.

    The config file may specify an AI function. If none is given, the
    Character will be stationary. Otherwise, every time it is given a turn
    the AI function will be called. It has access to all the methods
    defined in game.py to affect the game world.

    Additionally, by default nothing will happen if characters try to
    occupy each others' tiles. To make the "interact" method do anything,
    a sub-class is necessary. This is used by monsters, so that the
    player can automatically attack them.
    """
    hp_regen_interval = 6
    re_regen_interval = 4

    def __init__(self, game, position, config):
        """Initialize Character

        Parameters:

        game -- the game object
        position -- the position of the character
        config -- the config object to use to configure the character
        """
        # copy some attributes out of config needed to initialize Entity
        name = config.name

        if config.sprite_idx is not None:
            sprite_idx = config.sprite_idx
        else:
            sprite_idx = default_sprite_idx

        Entity.__init__(self, game, position, name, sprite_idx)

        self.set_sort_priority(10)
        self.type = "Character"
        self.passable = False
        self.visible = True

        # set up some variables & containers that all characters have
        self.turns = 0
        self.turns_since_regen = 0
        self.regen_rate = 5
        self.inventory = None # needs to be an item container object
        self.equipment = {'head':None, 'neck':None, 'about_body':None, 'body':None, 'legs':None, 'feet':None,
                          'on_lh':None, 'on_rh':None, 'in_lh':None, 'in_rh':None}

        # copy more attributes out of config
        self.visual_desc = config.visual_desc

        if config.ai_module is not None:
            self.ai_func = config.ai_module.act
        else:
            self.ai_func = None

        self.stats = StatStruct(1, config.stats_file)

        self.hp = self.stats.max_hp

        # logging for GA project
        self.damage_dealt = 0
        self.kills = 0
        self.got_killed = False
        self.fitness = 0


    def update(self):
        """Called every turn by Game."""

        if self.ai_func is not None:
            self.ai_func(self.game, self)

        self.turns = self.turns + 1
        if self.stats.hp < self.stats.max_hp:
            self.turns_since_regen = self.turns_since_regen + 1

        if self.turns_since_regen >= self.regen_rate:
            self.stats.hp = self.stats.hp + 1
            self.turns_since_regen = 0


    def die(self):
        """Informs the Character that is has been killed."""
        self.got_killed = True
        CharacterDeath(self).dispatch() # used by the GA


    def reset(self):
        """Resets the Character's performance logging variables."""
        self.damage_dealt = 0
        self.kills = 0
        self.got_killed = False
        self.fitness = 0


    def __str__(self):
        return self.name + " fitness: " + str(self.fitness)


    @property
    def description(self):
        """(string) Returns flavor text for the Character."""
        return self.visual_desc


    # The following properties calculate useful things from the Character's stats
    # and are used by higher level systems. I guess these are kind invisible "meta"
    # stats.

    @property
    def offense(self):
        """(int) Returns the Character's offense value."""
        #return self.stats.strength + self.stats.level
        return 1

    @property
    def defense(self):
        """(int) Returns the Character's defense value."""
        #return self.stats.dexterity + (self.stats.reiatsu * self.stats.density)
        return 1

    @property
    def speed(self):
        """(int) Returns the Character's speed."""
        return 1 # speed system not implemented yet


class StatStruct:
    """Container for all of a Character's attributes"""

    def __init__(self, level=1, file=None):
        if file is not None:
            try:
                cfg_parser.parse_and_apply(file, self)
            except IOError:
                print("error creating StatStruct from %s" % file)

        else:
            # spirit force system, level dependent?
            self.manipulation = 1
            self.power = 1
            self.density = 1

            # elemental affinities
            self.lightning = 0
            self.ice = 0
            self.water = 0
            self.fire = 0

            # classic stats
            self.strength = 1
            self.dexterity = 1
            self.intelligence = 1
            self.constitution = 1 # part of reiatsu system?

            # skills (fixed?)
            self.plot_importance = 0
            self.perception = 0

        # basic, level dependent
        self.level = level
        self.exp = 0
        self.max_hp = self.constitution
        self.hp = self.max_hp
        self.reiatsu = self.intelligence


def compare_characters(ch1, ch2):
    """Compare the fitness of one character to another.

    Returns:
        * 1 if ch1 is higher than ch2,
        * 0 if they are equal,
        * -1 if ch2 is more fit than ch1.
    """
    fit1 = ch1.fitness
    fit2 = ch2.fitness
    if fit1 > fit2:
        return 1
    elif fit1 == fit2:
        return 0
    else:
        return -1


if __name__ == "__main__":
    print(Character.__doc__)
