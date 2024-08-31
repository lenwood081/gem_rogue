from menus.PuaseMenu import PuaseMenu
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    K_p
)

# decides on which menus to display

class MenuManager:
    def __init__(self):
        self.menu = PuaseMenu()

        
    
    # choose the menu to show returns true or false (false mean unpause)
    def update(self, screen, events):
        self.quit_handler(events)

        new_menu = self.menu.update(events)
        if new_menu:
            self.menu = new_menu

        self.draw(screen)
        return True
    
    def quit_handler(self, events):
        for event in events:
            # quit checks
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                # for pauseing
                elif event.key == K_p:
                    return False
            return True
        

    def draw(self, screen):
        self.menu.draw(screen)