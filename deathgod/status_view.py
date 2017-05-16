""" status_view.py """
from .view import View

class StatusView(View):
    """ Renders the characer's status pane showing current HP, etc. """

    def __init__(self, screen, rect, background_color, font1, font2, color1, color2):
        View.__init__(self, screen, rect, background_color)
        self.extra_status = []

        self.font1 = font1
        self.font2 = font2
        self.color1 = color1
        self.color2 = color2

        self.offset = (5, 0)

        self.line_height = font1.get_height()

        self.name_image = None
        self.exp_label = self.font1.render("EXP:", True, self.color1, self.get_clear_color())
        self.hp_label = self.font1.render("HP:", True, self.color1, self.get_clear_color())

        #import text_views
        #import colors
        #import fonts
        #self.add_view(text_views.StringView(self, (50, 50), "child of statusView",
        #    fonts.normal, colors.black, colors.green))

    def add_status(self, text, color, position):
        status_img = self.font1.render(text, True, color)
        self.extra_status.insert(position, status_img)

    def remove_status(self, position):
        self.extra_status.remove(position)

    def update(self, player_state):
        self.clear()
        if self.name_image == None:
            self.name_image = self.font1.render( str(player_state.name), True, self.color1, self.get_clear_color())

        exp_image = self.font2.render( str(player_state.stats.exp), True, self.color2, self.get_clear_color())
        hp_image = self.font2.render( str(player_state.stats.hp), True, self.color2, self.get_clear_color())

        i = 0
        self.add_image_with_offset(self.name_image, (0, self.line_height * i), self.offset)
        i = i + 1
        self.add_image_with_offset(self.exp_label, (0, self.line_height), self.offset)
        self.add_image_with_offset(exp_image, (self.exp_label.get_width() + 5, self.line_height), self.offset)
        i = i + 1
        self.add_image_with_offset(self.hp_label, (0, self.line_height * i), self.offset)
        self.add_image_with_offset(hp_image, (self.hp_label.get_width() + 5, self.line_height * i), self.offset)
        i = i + 1


if __name__ == "__main__":
    print(StatusView.__doc__)