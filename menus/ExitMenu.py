from config import *
from menus.Menu import Menu

# menu that when retruned indicates the menu process is over

class ExitMenu(Menu):
    def __init__(self, previous_menu):
        super().__init__(previous_menu) 