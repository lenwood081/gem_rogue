from menus.PuaseMenu import PuaseMenu
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    K_p
)

# decides on which menus to display

class MenuManager:
    def __init__(self):
        self.pauseMenu = PuaseMenu()

        self.menuIndex = 0
        self.menus = []
        
        # add menus 
        self.menus.append(self.pauseMenu)
    
    # choose the menu to show returns true or false (false mean unpause)
    def update(self, screen):

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
        self.menus[self.menuIndex].draw(screen)
