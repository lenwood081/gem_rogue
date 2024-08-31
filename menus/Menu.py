from config import *
from menu_assests.Button import Button
import pygame

# pause menu should estentually pause the game (no updates)

class Menu:
    def __init__(self) -> None:

        # base surface
        self.base_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.base_surf.fill((20, 20, 20))
        self.base_surf.set_alpha(100)

        # list of button path pairs (button, menu)
        self.buttons = []


    # draw method should be overriden
    def draw(self, screen):
        screen.blit(self.base_surf, (0, 0))

        for button, menu in self.buttons:
            button.draw(screen)

        
    # retrun a menu object that represent the next menu to be displayed
    def update(self, events):
        for button, menu in self.buttons:
            if button.update(events):
                return menu
            
    # add a button
    def add_button(self, text, x, y, width, height, type):
        button = Button(text, x, y, width, height)
        menu = type()
        self.buttons.add((button, menu))