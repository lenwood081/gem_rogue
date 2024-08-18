import pygame
from config import *
from classes.Point import Point
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
)
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((PL_WIDTH, PL_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
        ))

        # position reletive to background (centered)
        self.pos = Point(BG_WIDTH/2, -BG_HEIGHT/2)
        

    def update(self, keys_pressed):
        x = 0
        y = 0

        # player movement
        if keys_pressed[K_s]:
            y = -PL_SPEED
        if keys_pressed[K_w]:
            y = PL_SPEED
        if keys_pressed[K_d]:
            x = PL_SPEED
        if keys_pressed[K_a]:
            x = -PL_SPEED

        # check for diagonal speed irregularity
        if x != 0 and y != 0:
            x /= math.sqrt(2)
            y /= math.sqrt(2)

        self.pos.move(x, y)

        # movement restriction (BG_WIDTH and BG_HEIGHT)
        if self.pos.x > BG_WIDTH - PL_WIDTH/2:
            self.pos.x = BG_WIDTH - PL_WIDTH/2
        if self.pos.x < PL_WIDTH/2:
            self.pos.x = PL_WIDTH/2
        if self.pos.y < -BG_HEIGHT + PL_HEIGHT/2:
            self.pos.y = -BG_HEIGHT + PL_HEIGHT/2
        if self.pos.y > -PL_HEIGHT/2:
            self.pos.y = -PL_HEIGHT/2