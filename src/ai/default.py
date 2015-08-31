import event
from message import Message
import colors

def act(game, monster):
    Message(("The %s stares at you." % monster.name, colors.yellow)).dispatch()
    #pass