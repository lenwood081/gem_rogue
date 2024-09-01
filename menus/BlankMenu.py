from menus.Menu import Menu

# menu that when retruned indicates the agme process

class BlankMenu(Menu):
    def __init__(self, previous_menu):
        super().__init__(previous_menu) 


    def draw(self, screen):
        pass