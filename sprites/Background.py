import pygame
from config import *

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.surf = pygame.Surface((BG_WIDTH, BG_HEIGHT))
        self.surf.fill(BG_COLOR)
        self.rect = self.surf.get_rect()

        # for determining position of background
        self.x = BG_WIDTH/2 - SCREEN_WIDTH/2
        self.y = BG_HEIGHT/2 - SCREEN_HEIGHT/2

    def update(self, player_x, player_y):
        # correct x and y
        x = self.x + SCREEN_WIDTH/2
        y = self.y - SCREEN_HEIGHT/2

        # check playeris in correct position
        if player_x == self.x and player_y == self.y:
            return
        
        # move background if else 
        self.x = player_x
        self.y = player_y