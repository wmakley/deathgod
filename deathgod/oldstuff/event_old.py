class EventHandler:
    def __init__(self):
        pass

# the base event types
(EXIT, COMMAND_EVENT, GAME_STATE_CHANGED, DISPLAY_INITED, MESSAGE,\
 MESSAGE_VIEW_STATE_CHANGED, ANY_KEY, DISPLAY_NEEDS_UPDATE, MESSAGE_FLUSH) = list(range(9))

class Event:
    def __init__(self, event_type):
        self.type = event_type
        
class StateChangeEvent(Event):
    def __init__(self, player_state, map_state):
        self.player_state = player_state
        self.map_state = map_state
        Event.__init__(self, GAME_STATE_CHANGED)

# command event types
(CE_PLAYER_MOVED, CE_MORE, CE_CONFIRM) = list(range(3))

class CommandEvent(Event):
    def __init__(self, ce_type, ce_data=[0]):
        self.ce_type = ce_type
        self.ce_data = ce_data
        Event.__init__(self, COMMAND_EVENT)
        
# message view state change types
        
(QUEUE_EMPTY, QUEUE_NOT_EMPTY) = list(range(2))
        
class MessageViewStateEvent(Event):
    def __init__(self, state):
        self.state = state
        Event.__init__(self, MESSAGE_VIEW_STATE_CHANGED)

class MessageEvent(Event):
    def __init__(self, msg):
        self.msg = msg
        Event.__init__(self, MESSAGE)