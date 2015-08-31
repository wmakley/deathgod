#!/usr/bin/env python
# encoding: utf-8
"""
event2.py - an attempt at a new event system for Death God

Every Event class must have a "static" list of handler functions, which
are all called every time an event of the class is instantiated and its
"dispatch" method is called. (The event is passed to every handler
function it calls, so hanlder functions must accept one argument.)

To register a handler with an Event class, call the add_handler
function: "add_handler(handler, event_class)"

The beauty of it is I no longer even need a "Listener" class!

Public Members:

add_handler
remove_handler
Event
GameStateChanged
DisplayNeedsUpdate
MessageViewState
Message
DisplayInited
ProgramShouldExit
KeyPressed
PlayerMoved
FlushMessages

"""

import sys
from ordered_pair import *


def add_handler(handler, event_class):
    """Registers a handler function with an event class.
    
    The handler function must accept one argument - the event object
    being handled.
    
    Arguments:
    
    handler
        -- the handler function
    event_class
        -- the class to register the handler with
    """
    event_class.handlers.append(handler)
    
    
def remove_handler(handler, event_class):
    """The opposite of add_handler."""
    event_class.handlers.remove(handler)
    

class Event:
    """The new and improved event class.
    
    The way this works is every sub-class NEEDS to have its own
    "handlers = []" "static" variable.
    
    Instance Attributes:
    
    dispatch
    val
    
    Class Attributes:
    
    add_handler
    """
    # very important that all subclasses have their own handlers attribute!!!
    handlers = []
    
    def __init__(self, val=""):
        """Accepts a parameter (default "") for debugging."""
        self.val = val
        
    def dispatch(self):
        """Calls every function in the class' handler list."""
        for f in self.__class__.handlers:
            f(self)
            
    @classmethod
    def add_handler(cls, h):
        cls.handlers.append(h)
    
    
class GameStateChanged(Event):
    """Created by the game pretty much whenever anything happens.
    
    Public Members:
    
    map_state
    player_state
    """
    handlers = []
    def __init__(self, player_state, map_state):
        """Arguments:
        
        map_state
            -- the currentGameMapobject (that the player is exploring)
        player_state
            -- the player object (so stats can be displayed)
        """
        Event.__init__(self)
        self.map_state = map_state
        self.player_state = player_state
        

class DisplayNeedsUpdate(Event):
    """Signals the Display to redraw everything."""
    handlers = []
    def __init__(self):
        Event.__init__(self)


class DisplayInited(Event):
    """Created by Display when it's done setting up."""
    handlers = []
    def __init__(self):
        Event.__init__(self)
        
        
class ProgramShouldExit(Event):
    """Dispatched when the program should quit."""
    handlers = []
    def __init__(self):
        Event.__init__(self)
        

class KeyPressed(Event):
    """Dispatched whenever a key is pressed."""
    handlers = []
    def __init__(self):
        Event.__init__(self)
        
        
class PlayerMoved(Event):
    """Created by InputManager when the Player should move.
    
    Public Members:
    
    direction
        -- the direction the player should move (an integer, as defined
           in directions.py)
    """
    handlers = []
    def __init__(self, direction):
        """Arguments:

           direction
               -- the direction (as defined in directions.py) that the
                  player should move
        """
        Event.__init__(self)
        self.direction = direction
    

class TurnEnded(Event):
    handlers = []
    def __init__(self):
        Event.__init__(self)
        
        
class FlushMessages(Event):
    """Causes MessageViews to move through their queue."""
    handlers = []
    def __init__(self):
        Event.__init__(self)
        
        
class SaveGame(Event):
    """Sends out the message that the game needs to be saved."""
    handlers = []
    def __init__(self):
        Event.__init__(self)
        
        
class LoadGame(Event):
    """Starts game loading process."""
    handlers = []
    def __init__(self):
        Event.__init__(self)
    

# some stuff for testing:
# turns out you don't need to subclass anything to handle events! Huzzah!

class Event2(Event):
    """test event"""
    handlers = []
    def __init__(self, val=0):
       Event.__init__(self, val)

class Listener:
    """a test class"""
    
    def __init__(self, name=""):
        self.name = name
        
    def handle_event(self, e):
        print self.name, "got Event with val", e.val
        
class Listener2(Listener):
    """a test class"""
    
    def __init__(self, name=""):
        Listener.__init__(self, name)
        add_handler(self.handle_event2, Event2)
        add_handler(self.handle_state_event, GameStateChanged)
        
    def handle_state_event(self, e):
        print self.name, "got GameStateChangedEvent with val", e.val
        
    def handle_event2(self, e):
        print self.name, "got Event2 with val", e.val
        
    
    
def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    a = Listener("a")
    add_handler(a.handle_event, Event)
    
    b = Listener2("b")
    
    Event(1).dispatch()
    Event2(2).dispatch()
    GameStateChanged(None, None).dispatch()
    Event(9).dispatch()
    

if __name__ == '__main__':
    print __doc__
    main(sys.argv[1:])

