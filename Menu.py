import pygame
from config import *
from menu_assests.Button import Button
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)


# TODO impliment Menu differently, essentually use the same game loop as the game
class Menu:
    def __init__(self):
        self._buttons = pygame.sprite.Group()
        self._back_color = (0, 0, 0)

    # add a button
    def add_button(self, text, x, y, font_size=32):
        button = Button(text, x, y, font_size=font_size)
        self._buttons.add(button)
    
    # method for the menu loop
    # all buttons and every thing must be declared before this
    def start_menu(self, screen):
        # clock
        clock = pygame.time.Clock()

        running = True
        while running:
            e = pygame.event.get()
            # check for quiting out
            for event in e:
                # quit checks
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return False
                elif event.type == QUIT:
                    return False

            # set back screen color
            screen.fill(self._back_color)

            # blit buttons
            for button in self._buttons:
                button.draw(screen)

            # update buttons
            for button in self._buttons:
                if button.update(e):
                    running = False

            # update screen
            pygame.display.update()

            # framerate
            clock.tick(FRAMERATE)

        return True

