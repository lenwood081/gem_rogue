from config import *
from menus.Menu import Menu
import pygame

# pause menu should estentually pause the game (no updates)

class PuaseMenu(Menu):
    def __init__(self):
        super().__init__()

        # set up buttons
        self.add_button("testing", 500, 500, 200, 100, PuaseMenu)
        
    
