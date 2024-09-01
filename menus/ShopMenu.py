from config import *
from menus.Menu import Menu
from menus.ExitMenu import ExitMenu


# pause menu should estentually pause the game (no updates)

class ShopMenu(Menu):
    def __init__(self, previous_menu):
        super().__init__(previous_menu)

        self.type = ShopMenu

        # set up buttons
        self.add_button("Back", 100, 100, self.previous_menu, font_size=16)

