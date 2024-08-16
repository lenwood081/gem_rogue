import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rec(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
        ))

    def update(self):
        # player movement
        pass