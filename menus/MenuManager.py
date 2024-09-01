from menus.PuaseMenu import PuaseMenu
from menus.Menu import Menu
from menus.ExitMenu import ExitMenu
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    K_p
)

# decides on which menus to display

class MenuManager:
    def __init__(self):
        self.quit_menu = ExitMenu
        self.menu = PuaseMenu(self.quit_menu)
        

    # choose the menu to show returns true or false (false mean unpause)
    def update(self, screen, events):
        # check for quit events
        if self.quit_handler(events) == False:
            return False

        new_menu = self.menu.update(events)
        if new_menu:
            if isinstance(new_menu, ExitMenu):
                self.menu = PuaseMenu(self.quit_menu)
                return False
            else:
                self.menu = new_menu

        self.draw(screen)
        return True
    
    def quit_handler(self, events):
        for event in events:
            # upause check (no matter what level of menu)
            if event.type == KEYDOWN:
                if event.key == K_p:
                    self.menu = PuaseMenu(self.quit_menu)
                    return False
            return True
        

    def draw(self, screen):
        self.menu.draw(screen)