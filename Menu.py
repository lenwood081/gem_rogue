import pygame
from config import *
from menu_assests.Button import Button
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)

class Menu:
    def __init__(self):
        self.buttons = pygame.sprite.Group()
        self.back_color = (0, 0, 0)

    # add a button
    def add_button(self, image_url, x, y, width, height):
        button = Button(image_url, x, y, width, height)
        self.buttons.add(button)
    
    # method for the menu loop
    # all buttons and every thing must be declared before this
    def start_menu(self, screen):
        # clock
        clock = pygame.time.Clock()

        running = True
        while running:
            # check for quiting out
            for event in pygame.event.get():
                # quit checks
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False

            # set back screen color
            screen.fill(self.back_color)

            # update screen
            pygame.display.update()

            # framerate
            clock.tick(FRAMERATE)

        if running == False:
            return False

        return True

