from config import *
from menus.Menu import Menu

# pause menu should estentually pause the game (no updates)

class PuaseMenu(Menu):
    def __init__(self, previous_menu):
        super().__init__(previous_menu)

        self.type = PuaseMenu

        # set up buttons
        self.add_button("Continue", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, PuaseMenu)
        self.add_button("Equipment Bindings", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150, PuaseMenu)
        self.add_button("Exit", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 300, previous_menu)
        
    
