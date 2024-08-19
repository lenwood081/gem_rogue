import pygame
from config import *
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)

class Menu:
    def __init__(self):
        pass
    
    @staticmethod
    def start_menu():
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

            # update screen
            pygame.display.flip()

            # framerate
            clock.tick(FRAMERATE)

