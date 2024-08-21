import pygame
from config import *
from classes.Point import Point

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("assets/background/pebble-rock-ground.png").convert_alpha(), (BG_WIDTH, BG_HEIGHT))
        self.rect = self.surf.get_rect()

        # for determining position of background
        self.location = Point(SCREEN_WIDTH/2 - BG_WIDTH/2, SCREEN_HEIGHT/2 - BG_HEIGHT/2)

    def update(self, player_pos):
        # the player x and y represent where the center of the screen should be
        self.location.x = SCREEN_WIDTH/2 - player_pos.x
        self.location.y = SCREEN_HEIGHT/2 + player_pos.y