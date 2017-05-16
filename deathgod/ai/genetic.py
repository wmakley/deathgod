"""
genetic.py

by William Makley

Hooks into game and manages a bunch of monsters and their AI's

Honestly some decent monster AI can be had just from a very simple
test as to whether the monster's health is low and either approaching
the player or running away depending, so this is pretty much just for
fun and to see if a reasonably smart one can evolve hampered by all
these unnecessary genes.

members:

act
fitness
GATest
DecisionTree
DTreeNode
"""

import random
from . import tests
from . import actions
from ..monster import Monster
from ..monsters import giant_frog
from .. import character
from .. import event

random.seed()

MAX_DEPTH = len(tests.members) # right now my trees are stupid simple so this is accurate

# any monster using this better already be given a d_tree variable somehow
def act(game, monster):
    """The actual genetic AI function called when the monster's turn comes up."""
    action = monster.d_tree.get_action(game)
    action(game, monster)


class GATest:
    """Spawns a bunch of monsters and manages their AI genetically.

    Yes, this class is the meat of the project. The rest is just data
    structures and algorithms I needed to make it all work.
    """
    def __init__(self, game, eval_interval=5):
        self.game = game
        self.turns_since_eval = 0
        self.eval_interval = eval_interval
        self.generations = 0
        self.running = False
        self.monsters = []
        self.current_mark = 0

        self.p_breed = [0.20, 0.30, 0.40, 0.50, 0.60]
        # replacement probabilities are just the inverse

        character.CharacterDeath.add_handler(self.handle_character_death)
        event.TurnEnded.add_handler(self.handle_turn_ended)


    def start(self, monster_count=30):
        self.running = True
        current_map = self.game.get_map()
        for i in range(monster_count):
            pos, t_tile = current_map.choose_open_tile()
            mon = Monster(self.game, pos, giant_frog)
            mon.ai_func = act
            mon.d_tree = DecisionTree(mon)
            mon.d_tree.init_random()
            self.monsters.append(mon)
            self.game.add_entity(mon)
            self.game.activate_entity(mon)


    def handle_turn_ended(self, e):
        """Turn ended handler.

        This class needs to know every time a turn passes. At certain
        intervals it will do the GA thing on all the AI's.
        """
        if not self.running:
            return

        if self.turns_since_eval == self.eval_interval:
            self.generations = self.generations + 1
            print("generation %d beginning" % self.generations)
            self.turns_since_eval = 0
            avg_fitness = 0.0
            # iterate through all monsters, evaluate fitness, sort, mutate
            for mon in self.monsters:
                mon.fitness = fitness(mon)
                avg_fitness = avg_fitness + mon.fitness
                # it doesn't really matter if we mutate now or later,
                # so may as well catch this for loop
                mon.d_tree.mutate(1.0 / (float(MAX_DEPTH) * 2.0 + 1.0))

            self.monsters.sort(key=lambda m: m.sorting_priority)

            avg_fitness = float(avg_fitness) / float(len(self.monsters))
            print("avg. fitness = %f, worst = %d, best = %d" % (avg_fitness, self.monsters[0].fitness, self.monsters[-1].fitness))

            # pick 5 monsters at random
            sample = random.sample(self.monsters, 5)
            #print "type(sample) = " + str(type(sample)) + ", sample = " + str(sample)
            # order from worst to best
            sample.sort(key=lambda m: m.sorting_priority)

            to_breed = []
            to_replace = []
            # iterate through the sample randomly adding monsters to breeding or replacement pools
            # based on their position in the list
            i = 0
            for mon in sample:
                if random.uniform(0, 1) < self.p_breed[i]:
                    to_breed.append(mon)
                if random.uniform(0, 1) > self.p_breed[i]:
                    to_replace.append(mon)

                i = i + 1

            # make sure the two quantities are the same
            # seriously, how the hell are you supposed to do this?
            while len(to_breed) > len(to_replace):
                to_replace.append(random.choice(self.monsters[0:len(self.monsters)//2]))
            if len(to_replace) > len(to_breed):
                diff = len(to_replace) - len(to_breed)
                to_replace = to_replace[0:-diff]

            new_d_trees = []
            for mon in to_breed:
                # breed with random choice of the best half of self.monsters
                # is this too much selection pressure?
                new_d_tree = breed(mon.d_tree,
                                   random.choice(self.monsters[-len(self.monsters)//2:]).d_tree)
                new_d_trees.append(new_d_tree)

            # put those new d_trees in to_replace
            # since this is effectively a new monster, reset it
            while new_d_trees:
                mon = to_replace.pop(0)
                mon.d_tree = new_d_trees.pop(0)
                mon.reset()


        self.turns_since_eval = self.turns_since_eval + 1


    def handle_character_death(self, e):
        """Character death handler.

        This is necessary to reactivate any dead monsters.
        """
        if not self.running:
            return

        mon = e.ch
        if mon.name == giant_frog.name:
            new_pos, t_tile = self.game.get_map().choose_open_tile()
            mon.mark = self.current_mark
            print("putting frog which was at %s back at %s, marking it as %d" % (str(mon.position), str(new_pos), mon.mark))
            mon.position = new_pos
            self.current_mark = self.current_mark + 1
            self.game.add_entity(mon)
            self.game.activate_entity(mon)


def fitness(monster):
    """Evaluates the fitness of a monster's AI function based on the monster's performance."""
    # kills and damage are most important
    fitness = (monster.kills * 10) + monster.damage_dealt

    # getting killed is crappy
    if monster.got_killed:
        fitness = fitness - 10

    return fitness


def breed(tree1, tree2):
    """My breeding function.

    Basically makes a copy of tree1, and swaps sub-trees with tree2 at
    a random depth. Pretty much relies on my simplistic tree structure.

    I have no fucking clue if this will work. I can't even debug it since
    I have no way of printing my tree.

    Right now it can only swap sub-trees, which kinda sucks but the
    alternative is a far more complex algorithm than I have time for.
    """
    cpy = tree1.copy()

    start_depth = random.randint(0, MAX_DEPTH-2)

    node1_parent = cpy.get_left_node_at_depth(start_depth)
    node2 = tree2.get_left_node_at_depth(start_depth+1)
    node1_parent.left = node2

    return cpy


class DecisionTree:
    """My decision tree class.

    Public Members:

    get_action
    init_random
    init_sane
    mutate
    copy
    """
    def __init__(self, owner, root=None):
        self.root = root
        self.owner = owner
        self.node_count = 0 # used for mutation probability
        self.node_list = [] # this is not really used


    def get_action(self, game):
        return self.get_action_aux(game, self.root)


    def get_action_aux(self, game, node):
        # base case
        if node.is_external:
            return node.action

        else:
            # choose left branch if test result is True (arbitrary)
            if node.test(game, self.owner) is True:
                return self.get_action_aux(game, node.left)
            else:
                return self.get_action_aux(game, node.right)


    def get_left_node_at_depth(self, depth):
        """Returns a list of all nodes at a given depth in the tree."""
        return self.get_left_node_at_depth_aux(depth, self.root)


    def get_left_node_at_depth_aux(self, depth, node):
        if depth == 0:
            return node
        else:
            depth = depth - 1
            return self.get_left_node_at_depth_aux(depth, node.left)


    def init_random(self, test_set=tests.members, action_set=actions.members):
        """Initializes the tree randomly from a set of tests and actions.

        Right now the tree is just sort of a linear affair with each node
        having a left branch to another test and a right branch to an action.
        Less than ideal?
        """
        self.root = self.init_random_aux(test_set, action_set)


    def init_random_aux(self, test_set, action_set):
        """Should return the top node of the tree."""
        # base case is tests is empty, meaning all have been used,
        # so we make an action node instead
        if not test_set:
            action = random.choice(action_set)
            node = DTreeNode(self, action)
            return node

        else:
            # choose a test
            test = random.choice(test_set)

            # make a new list of tests without the one used here
            new_tests = list(test_set)
            new_tests.remove(test)

            # the left branch is another test, the right branch is an action
            left = self.init_random_aux(new_tests, action_set)
            right = self.init_random_aux([], action_set)

            node = DTreeNode(self, None, test, left, right)
            return node


    def init_sane(self):
        """Generates a tree manually for testing."""
        self.root = DTreeNode(self, None, tests.less_than_half_life)
        self.root.left = DTreeNode(self, actions.run_away)
        #self.root.right = DTreeNode(actions.move_towards_player)

        # for testing "adjacent_to_player"
        self.root.right = DTreeNode(self, None, tests.adjacent_to_player)
        self.root.right.left = DTreeNode(self, actions.attack_player)
        self.root.right.right = DTreeNode(self, actions.move_towards_player)


    def mutate(self, probability=(1.0 / (float(MAX_DEPTH) * 2.0 + 1.0))):
        """Randomly moves some nodes around."""
        self.__mutate_aux(probability, self.root)


    def __mutate_aux(self, probability, node):
        """Recursive version of mutate."""
        # decide whether to mutate
        if random.uniform(0, 1) < probability:
            mutate = True
        else:
            mutate = False

        # base case
        if node.is_external:
            # choose a new action randomly
            if mutate:
                node.action = random.choice(actions.members)
            return
        else:
            # choose a new test randomly, do recursive calls regardless
            # of whether a mutation happened:
            if mutate:
                node.test = random.choice(tests.members)
            self.__mutate_aux(probability, node.left)
            self.__mutate_aux(probability, node.right)
            return


    def copy(self):
        """Returns a copy of the Tree"""
        cpy = DecisionTree(self.owner)
        cpy.root = self.root.copy_recursive(cpy)
        return cpy


class DTreeNode:
    """My decision tree node class.

    It can take two forms:

    Form 1: A binary test with two leaf nodes
    Form 2: An action function, with no test or leaves
    """
    def __init__(self, parent_tree, action=None, test=None, left=None, right=None):
        """init function!

        You have to pass a parent_tree so that Tree's node_count can be
        incremented.
        """
        self.action = action

        self.test = test
        self.left = left
        self.right = right

        self.parent_tree = parent_tree
        parent_tree.node_count = parent_tree.node_count + 1
        parent_tree.node_list.append(self)


    @property
    def is_external(self):
        """Returns True if the node is an action node (form 2)."""
        # if this is ever wrong, the tree was generated wrong
        if self.action is not None:
            return True
        else:
            return False


    def copy_recursive(self, parent_tree):
        """Returns a copy of the node referencing new copies of its leaves."""
        if self.is_external:
            left = None
            right = None
        else:
            left = self.left.copy_recursive(parent_tree)
            right = self.right.copy_recursive(parent_tree)

        cpy = DTreeNode(parent_tree, self.action, self.test, left, right)
        return cpy
