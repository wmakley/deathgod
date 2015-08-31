from .view import View
import pygame
from pygame.locals import *
from .ordered_pair import *

class StatusView(View):
    def __init__(self, screen, rect, backgroundColor, font1, font2, color1, color2):
        View.__init__(self, screen, rect, backgroundColor)
        self.extraStatus = []
        
        self.font1 = font1
        self.font2 = font2
        self.color1 = color1
        self.color2 = color2
        
        self.offset = (5, 0)
        
        self.lineHeight = font1.get_height()
        
        self.nameImage = None
        self.expLabel = self.font1.render("EXP:", True, self.color1, self.get_clear_color())
        self.hpLabel = self.font1.render("HP:", True, self.color1, self.get_clear_color())
        
        #import text_views
        #import colors
        #import fonts
        #self.add_view(text_views.StringView(self, (50, 50), "child of statusView",
        #    fonts.normal, colors.black, colors.green))
        
    def addStatus(self, text, color, position):
        statusImg = self.font1.render(text, True, color)
        self.extraStatus.insert(position, statusImg)
        
    def removeStatus(self, position):
        self.extraStatus.remove(position)
        
    def update(self, player_state):
        self.clear()
        if self.nameImage == None:
            self.nameImage = self.font1.render( str(player_state.name), True, self.color1, self.get_clear_color())
            
        expImage = self.font2.render( str(player_state.stats.exp), True, self.color2, self.get_clear_color())
        hpImage = self.font2.render( str(player_state.stats.hp), True, self.color2, self.get_clear_color())
        
        i = 0
        self.add_image_with_offset(self.nameImage, (0, self.lineHeight * i), self.offset)
        i = i + 1
        self.add_image_with_offset(self.expLabel, (0, self.lineHeight), self.offset)
        self.add_image_with_offset(expImage, (self.expLabel.get_width() + 5, self.lineHeight), self.offset)
        i = i + 1
        self.add_image_with_offset(self.hpLabel, (0, self.lineHeight * i), self.offset)
        self.add_image_with_offset(hpImage, (self.hpLabel.get_width() + 5, self.lineHeight * i), self.offset)
        i = i + 1
        
        
if __name__ == "__main__":
    print(StatusView.__doc__)