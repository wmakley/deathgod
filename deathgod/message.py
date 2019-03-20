"""message_view.py

Public Members:

Message
MessageView
"""
import pygame
from .event import Event
from .ordered_pair import *
from .view import View
from . import fonts
from . import dg_input
from . import event
from . import settings

PROMPT = "- more -"
HILIGHT_COLOR = settings.message_hilight_color
MSG_TEXT_PART = 0
MSG_COLOR_PART = 1


class Message(Event, list):
    """
    Sends a message to MessageViews.

    Subclasses list so it may be joined with
    other messages and other cool things like that.

    Public Members:

    get_width
    """
    handlers = []
    def __init__(self, *args):
        """Initialize the event.

        Arguments:

        args
            -- the message to send, tuples of string and color pairs
               e.g. ("Hello world", colors.white), (" LOL", (80,255,80)), ...
        """
        Event.__init__(self)
        list.__init__(self)

        #print args
        self.extend(args)
        #print self


    def get_width(self, font):
        """Returns width (pixels) of rendering the message with a given font."""
        size = 0
        for m in self:
            size = size + font.size(m[MSG_TEXT_PART])[x]

        return size



class MessageView(View):
    """
    Outputs game messages, pauses for prompts.

    Public Members:

    show_next
    is_empty
    size
    dequeue_msg
    enqueue_msg
    """

    def __init__(self, parent, rect, bg_color=(0,0,0), font=fonts.regular):
        View.__init__(self, parent, rect, bg_color)

        Message.add_handler(self.handle_message)
        event.add_handler(self.handle_flush_messages, event.FlushMessages)
        event.add_handler(self.handle_key_pressed, event.KeyPressed)

        self.__msg_q = []
        self.__font = font
        #self._max_chars = max_chars

        self.__msg_offset = (5, 0)
        self.__max_line_length = self.width - (2 * self.__msg_offset[x])
        self.__space_width = self.__font.size(" ")[x]
        self.__space_msg = Message((" ", (0,0,0)))

        self.__prompt_img = self.__font.render(
            PROMPT, True, HILIGHT_COLOR,
            self.get_clear_color())


    def _blit_msg(self, msg, more=False):
        """Prints a text string onto the view, dispatches redraw event."""
        self.clear()
        cursor = list(self.__msg_offset)

        #print "in _blit_msg, got msg=",msg
        # go through each color segment of the message
        for m in msg:
            #print "in _blit_msg, got m=",m
            img = self.__font.render(m[0], True, m[1], self.background)
            self.add_image(img, cursor)
            cursor[x] = cursor[x] + img.get_width()

        if more:
            cursor[x] = cursor[x] + self.__space_width
            self.add_image(self.__prompt_img, cursor)

        event.DisplayNeedsUpdate().dispatch()


    def show_messages(self):
        """Displays all the messages in the queue.

        Displays a prompt and waits for a key press to continue as
        needed if all the messages wont fit in the view at once.
        """
        if self.size == 0:
            #print "clearing message view due to empty queue"
            self.clear()
            event.DisplayNeedsUpdate().dispatch()
            return

        while self.size > 0:
            more = False
            msg = self.dequeue_msg()
            # if there is another message, check if it will fit with this one
            if self.size > 0:
                more = True
                if msg.get_width(self.__font) + 2*self.__space_width + self.__msg_q[0].get_width(self.__font)\
                        + self.__prompt_img.get_width() <= self.__max_line_length:
                    msg.extend(self.__space_msg)
                    msg.extend(self.dequeue_msg())
                    # if, after adding this message, there are no messages left,
                    # we don't actually need to pause
                    if self.size == 0:
                        more = False

            self._blit_msg(msg, more)
            if more:
                e = dg_input.wait_for_event(pygame.locals.KEYDOWN)


    def dequeue_msg(self):
        """Dequeue the last message off the queue."""
        return self.__msg_q.pop(0)


    def enqueue_msg(self, message):
        """Adds a message to the message queue."""
        #print "message view got msg: %s" % str(message)
        self.__msg_q.append(message)
        #print "in MessageView: enqueue_msg: _msg_q = " + str(self.__msg_q)


    @property
    def is_empty(self):
        """Obvious."""
        return not self.__msg_q


    @property
    def size(self):
        """(int) returns the size of the current message queue"""
        return len(self.__msg_q)


    @property
    def font(self):
        """Returns the View's font."""
        return self.__font


    def handle_message(self, e):
        self.enqueue_msg(e)


    def handle_flush_messages(self, e):
        self.show_messages()


    def handle_key_pressed(self, e):
        self.show_messages()


if __name__ == "__main__":
    print(__doc__)
