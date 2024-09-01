from config import *
from menu_assests.Button import Button
import pygame

# pause menu should estentually pause the game (no updates)

class Menu:
    def __init__(self, previous_menu, forward_menu):

        # base surface
        self.base_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.base_surf.fill((20, 20, 20))
        self.base_surf.set_alpha(100)

        # list of button path pairs (button, menu)
        self.buttons = []
        self.previous_menu = previous_menu
        self.forward_menu = forward_menu


    # draw method should be overriden
    def draw(self, screen):
        screen.blit(self.base_surf, (0, 0))

        for button, menu in self.buttons:
            button.draw(screen)

    # event_handler
    def event_handler(self, events):
        for event in events:
            # upause check (no matter what level of menu)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.previous_menu()
            return True

        
    # retrun a menu object that represent the next menu to be displayed
    def update(self, events):

        for buttons in self.buttons:
            if buttons[0].update(events):
                return buttons[1]
            
    # add a button
    def add_button(self, text, x, y, type, font_size=32):
        button = Button(text, x, y, font_size=font_size)
        self.buttons.append((button, type))