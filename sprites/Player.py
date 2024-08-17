import pygame
from config import *
from classes.Point import Point
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
)

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
        self.pos = Point(BG_WIDTH/2, BG_HEIGHT/2)
        

    def update(self, keys_pressed):
        # player movement
        if keys_pressed[K_s]:
            self.pos.move(0, PL_SPEED)
        if keys_pressed[K_w]:
            self.pos.move(0, -PL_SPEED)
        if keys_pressed[K_d]:
            self.pos.move(PL_SPEED, 0)
        if keys_pressed[K_a]:
            self.pos.move(-PL_SPEED, 0)

        # movement restriction (BG_WIDTH and BG_HEIGHT)
        if self.pos.x > BG_WIDTH - PL_WIDTH/2:
            self.pos.x = BG_WIDTH - PL_WIDTH/2
        if self.pos.x < PL_WIDTH/2:
            self.pos.x = PL_WIDTH/2
        if self.pos.y > BG_HEIGHT - PL_HEIGHT/2:
            self.pos.y = BG_HEIGHT - PL_HEIGHT/2
        if self.pos.y < PL_HEIGHT/2:
            self.pos.y = PL_HEIGHT/2