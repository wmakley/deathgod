"""
Entry point of the game
"""
import pickle
import pygame
from . import settings
from . import dg_input
from . import display
from . import event
from . import entity
from .player import Player
from . import game_map
from . import map_generators
from . import colors
from .ordered_pair import x, y
from .message import Message


class Game:
    """
    This class is pretty much the core of the logical flow of deathgod.

    E.G. When the player does something, this class takes care of the
    rest. It manages everything on the playing field, and implements
    methods that entities or abilities or pretty much anything that
    does anything can call to create complex behavior. Or, that's the
    current plan anyway.

    In the MVC paradigm, I guess this is the controller.

    Public Members:

    get_player
    get_map
    end_turn
    move_entity
    move_entity_in_direction
    add_entity
    delete_entity
    activate_entity
    deactivate_entity
    move_player_in_direction
    combat
    """

    def __init__(self):
        # model!
        self.player = Player(self, settings.player_start)
        self.current_map = game_map.GameMap(
            settings.world_dimensions,
            self.player.position,
            map_generators.test_generator
        )

        # view!
        self.display = display.Display(self.player, self.current_map)

        # other local variables!
        self.done = False

        self.inactive_entities = []
        self.active_entities = []
        self.turns = 0

        self.add_entity(self.player)
        self.activate_entity(self.player)

        # create some test stuff
        from .monster import Monster
        from . import monsters
        from .ai import genetic
        test_monster = Monster(self, (24, 1), monsters.giant_frog)
        test_monster.ai_func = genetic.act
        test_monster.d_tree = genetic.DecisionTree(test_monster)
        test_monster.d_tree.init_sane()

        test_entity = entity.Entity(self, (22, 20), "Test e")
        test_entity.sorting_priority = (20)
        test_entity.visible = True

        self.add_entity(test_monster)
        self.add_entity(test_entity)
        self.activate_entity(test_monster)

        # uncomment for genetic ai test:
        self.ga_test = genetic.GATest(self)
        self.ga_test.start()

    def start(self):
        """Starts the game loop"""
        self.display.update()
        while not self.done:
            evt = dg_input.wait_for_event(pygame.locals.KEYDOWN)
            dg_input.parse_keydown(evt.key, self)

    def get_map(self):
        """Returns the current map object"""
        return self.current_map

    def get_player(self):
        """Returns the player object"""
        return self.player


    def end_turn(self):
        """Ends the turn, calls update on all active entities."""
        #print "ending turn %d" % self.turns
        self.player.turns = self.player.turns + 1

        # update all active entities
        # TODO add speed mechanics here
        for ent in self.active_entities:
            ent.update()


        # some things still rely on this event being instantiated every turn, alas
        event.TurnEnded().dispatch()

        # show all the messages that have accumulated due to the events of the turn
        self.display.message_view.show_messages()

        # update the display
        self.display.update()


    def move_entity(self, ent, destination):
        """Takes any given entity and relocates it to a destination tile.

        Returns True if the movement occurred, False if there is something in the way"""
        target = self.current_map.get_tile(destination)
        moved = True
        if target.passable is True:
            for target_entity in target.entities:
                if target_entity.passable is False:
                    if ent.type == "Player":
                        target_entity.interact(ent)
                    moved = False
                    break
            if moved is True:
                self.current_map.move_entity_to_tile(ent, target)
                ent.position = destination
        else:
            moved = False
            if ent.type == "Player":
                Message(("There is something in the way.", colors.white)).dispatch()
                Message(("You hit your head on it.", colors.white),
                        (" Ouch.", colors.red)).dispatch()

        return moved


    def move_entity_in_direction(self, ent, direction):
        """Moves an entity in a given direction."""
        target = self.current_map.get_coord_in_direction(ent.position, direction)
        return self.move_entity(ent, target)


    def add_entity(self, ent):
        """Add an entity to the current map: ent = the Entity object"""
        self.inactive_entities.append(ent)
        self.current_map.add_entity(ent)


    def remove_entity(self, ent):
        """Remove an entity from the current map: ent = the Entity object"""
        if ent.active is True:
            self.active_entities.remove(ent)
        else:
            self.inactive_entities.remove(ent)
        self.current_map.remove_entity(ent)


    def activate_entity(self, ent):
        """Move an entity to the active entities list: ent = the Entity object"""
        self.active_entities.append(ent)
        self.inactive_entities.remove(ent)
        ent.active = True


    def deactivate_entity(self, ent):
        """Remove an entity from the active entities list: ent = the Entity object"""
        self.active_entities.remove(ent)
        self.inactive_entities.append(ent)
        ent.active = False


    def move_player_in_direction(self, direction):
        """This method should typically be called when the movement keys are pressed.

        It tries to move the player in a direction, if the tile is not passable for
        some reason nothing happens, and if there is an entity in the destination
        tile, it is assumed that the player wants to interact with it."""
        self.move_entity_in_direction(self.player, direction)
        self.end_turn()


    def get_nearby_entities(self, ent, spread):
        """Should return a list of all the entities in (spread) around (ent)

        Basically if spread == 1, this will get everything one tile from (ent),
        including diagonals (so it gets entities in a square)
        """
        position = ent.position
        tile_slice = self.current_map.get_tile_slice(
            position[x]-spread, position[x]+spread,
            position[y]-spread, position[y]+spread
        )
        entities = []

        for column in tile_slice:
            for tile in column:
                if tile.has_entity:
                    entities.extend(tile.entities)

        #entities.remove(ent)
        return entities


    def save_game(self, file_name):
        """Saves the current game to a file."""
        f = open(file_name, "w")
        pickle.dump(self.current_map, f)
        f.close()


    def load_game(self, file_name):
        """Loads a saved game from a file."""
        try:
            f = open(file_name, "r")
            try:
                self.current_map = pickle.load(f)
            except IOError:
                print("Couldn't read " + file_name)
            finally:
                f.close()
        except IOError:
            print("Couldn't open " + file_name)


    def combat(self, attacker, victim):
        """Primary combat logic.

        This probably should go in the Character class now that I think about it,
        since it is basically a method that uses and alters character data.

        Anyway, this is basically cobbled together for testing, so a rewrite is in
        order when I decide on some actual game mechanics, and that is when I will
        move it to Character.
        """
        a_pos = attacker.position
        v_pos = victim.position
        if not ((-1 <= a_pos[x] - v_pos[x] <= 1) and (-1 <= a_pos[y] - v_pos[y] <= 1)):
            #print "combat for %s illegal" % attacker.name
            return

        a_offense = attacker.offense
        v_defense = victim.defense

        damage = a_offense - v_defense
        if damage < 0:
            damage = 0

        victim.stats.hp = victim.stats.hp - damage

        # log some stuff for the GA
        attacker.damage_dealt = attacker.damage_dealt + damage

        # decide if the victim died
        if victim.stats.hp <= 0:
            death = True
        else:
            death = False

        # create a message with the result of the combat
        if attacker.type == "Player":
            name1 = "You"
            verb = "hit"
        else:
            name1 = attacker.name
            verb = "hits"

        if victim.type == "Player":
            name2 = "you"
            the = ""
        else:
            name2 = victim.name
            the = "the "

        Message(("%s %s %s%s for %d damage." % (name1, verb, the, name2, damage),
                 colors.white)).dispatch()

        if death:
            attacker.kills = attacker.kills + 1

            if victim.type != "Player":
                Message(("You have slain the %s." % name2, colors.white)).dispatch()
                self.deactivate_entity(victim)
                self.remove_entity(victim)
                victim.die()
            else:
                Message(("You die. ", colors.red),
                        ("Your health has been reset.", colors.green)).dispatch()
                self.player.stats.hp = self.player.stats.max_hp # player can't die yet



if __name__ == "__main__":
    print(Game.__doc__)
