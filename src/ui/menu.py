from view import View
import colors

class Menu(View):
    """A menu"""
    
    def __init__(self, parent):
        self.__inited = False
        self.__parent = parent
        self.__menu_items = []
        
    def add_menu_item(self, item):
        self.__menu_items.append(item)