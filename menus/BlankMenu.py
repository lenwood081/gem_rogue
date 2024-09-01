from menus.Menu import Menu

# menu that when retruned indicates the agme process

class BlankMenu(Menu):
    def __init__(self):
        super().__init__(None, None) 


    def draw(self, screen):
        pass