from config import *
from menu_assests.Button import Button
import pygame

# pause menu should estentually pause the game (no updates)

class Menu:
    def __init__(self, player):

        # base surface
        self.base_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.base_surf.fill((20, 20, 20))
        self.base_surf.set_alpha(100)

        # menu settings
        self.on_menu = True
        self.current_menu = None

        # list of button path pairs (button, menu)
        self.buttons = []

        # refernce to player
        self.player = player


    # draw method should be overriden
    def draw(self, screen):
        if self.on_menu:
            screen.blit(self.base_surf, (0, 0))

            for button in self.buttons:
                button[0].draw(screen)
        else:
            if self.current_menu:
                self.current_menu.draw(screen)

    # event_handler
    def event_handler(self, events, ):
        for event in events:
            # go back check (no matter what level of menu)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return False
            return True

        
    # retrun a menu object that represent the next menu to be displayed
    def update(self, events):
        if self.event_handler(events) == False:
            return False

        # check if one menu
        if self.on_menu:
            for buttons, menu in self.buttons:
                if buttons.update(events):
                    self.on_menu = False
                    if menu:
                        self.current_menu = menu(self.player)
                    else:
                        # None value => go back
                        self.on_menu = True
                        return False
                    break
        else:
            #if None casscade a False value (essentually go back a menu)
            if self.current_menu.update(events) == False:
                self.on_menu = True
            
        return True
                
    # add a button
    def add_button(self, text, x, y, type, font_size=32):
        button = Button(text, x, y, font_size=font_size)
        self.buttons.append((button, type))


# base menu for pausing
class PauseMenu(Menu):
    def __init__(self, player):
        super().__init__(player)

        # set up buttons
        self.add_button("Continue", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150, None)
        self.add_button("Equipment Bindings", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, PauseMenu)
        self.add_button("Exit Game", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150, None)


# for changing equipment keys
class EquipmentWindow(Menu):
    def __init__(self, player):
        super().__init__(player)

        

        