from .. import message
from .. import colors

def act(game, monster):
    message.Message(("The %s stares at you." % monster.name, colors.yellow)).dispatch()
    #pass
