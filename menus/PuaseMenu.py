from config import *
from menus.Menu import Menu
from menus.ExitGame import ExitGame

# pause menu should estentually pause the game (no updates)

class PuaseMenu(Menu):
    def __init__(self, previous_menu):
        super().__init__(previous_menu)

        self.type = PuaseMenu

        # set up buttons
        self.add_button("Continue", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, previous_menu)
        self.add_button("Equipment Bindings", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150, PuaseMenu)
        self.add_button("Exit Game", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 300, ExitGame)
        
    
